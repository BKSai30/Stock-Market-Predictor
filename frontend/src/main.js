// Smooth scrolling function
window.scrollToSection = function(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
};

// Global variable to store current chart instance
let currentTechnicalChart = null;

// Initialize the application
window.initializeApp = function() {
    console.log('Initializing Stock Market Predictor...');
    
    // Set up form submission handler
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }
    
    // Set up quick stock buttons
    const quickStockButtons = document.querySelectorAll('.quick-stock-btn');
    quickStockButtons.forEach(button => {
        button.addEventListener('click', function() {
            const symbol = this.dataset.symbol;
            document.getElementById('stockSymbol').value = symbol;
            // Highlight selected button
            quickStockButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Set up volatility filter buttons
    const volatilityButtons = document.querySelectorAll('.volatility-btn');
    volatilityButtons.forEach(button => {
        button.addEventListener('click', function() {
            volatilityButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const category = this.dataset.category;
            loadTopStocks(category);
        });
    });
    
    // Initialize technical charts
    initializeTechnicalCharts();
    
    // Load default top stocks
    loadTopStocks('safe');
    
    console.log('App initialized successfully!');
};

// Initialize technical chart functionality
function initializeTechnicalCharts() {
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', function() {
            const selectedStock = document.getElementById('stockSymbol').value;
            if (selectedStock) {
                loadTechnicalChart(selectedStock, this.value);
            }
        });
    }
}

// Handle prediction form submission
function handlePredictionSubmit(event) {
    event.preventDefault();
    
    const symbol = document.getElementById('stockSymbol').value.trim();
    const days = document.getElementById('predictionDays').value;
    
    if (!symbol) {
        showToast('Error', 'Please enter a stock symbol', 'error');
        return;
    }
    
    makePrediction(symbol, days);
}

// Make prediction API call
async function makePrediction(symbol, days) {
    // Show loading state
    document.getElementById('predictionInitial').style.display = 'none';
    document.getElementById('predictionResults').classList.add('d-none');
    document.getElementById('predictionLoading').classList.remove('d-none');
    
    try {
        // Call Flask API
        const response = await fetch('http://localhost:5000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbol: symbol.toUpperCase(),
                days_ahead: parseInt(days)
            })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading, show results
        document.getElementById('predictionLoading').classList.add('d-none');
        document.getElementById('predictionResults').classList.remove('d-none');
        
        // Update UI with results
        updatePredictionResults(data);
        
        // Load technical chart for the predicted stock
        const chartType = document.getElementById('chartTypeSelect')?.value || 'candlestick';
        loadTechnicalChart(symbol, chartType);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Hide loading
        document.getElementById('predictionLoading').classList.add('d-none');
        document.getElementById('predictionInitial').style.display = 'block';
        
        // Show error message
        showToast('Prediction Error', `Failed to get prediction: ${error.message}`, 'error');
    }
}

// Update UI with prediction results
function updatePredictionResults(data) {
    // Update stock info
    document.getElementById('stockName').textContent = data.name || data.symbol || 'Unknown Stock';
    document.getElementById('currentPrice').textContent = `₹${data.current_price || 'N/A'}`;
    document.getElementById('predictedPrice').textContent = `₹${data.predicted_price || 'N/A'}`;
    
    // Update price change
    const priceChange = data.predicted_price - data.current_price;
    const priceChangeElement = document.getElementById('priceChange');
    if (priceChange > 0) {
        priceChangeElement.textContent = `+₹${priceChange.toFixed(2)} (+${((priceChange/data.current_price)*100).toFixed(2)}%)`;
        priceChangeElement.className = 'price-change text-success';
    } else {
        priceChangeElement.textContent = `-₹${Math.abs(priceChange).toFixed(2)} (${((priceChange/data.current_price)*100).toFixed(2)}%)`;
        priceChangeElement.className = 'price-change text-danger';
    }
    
    // Update confidence
    const confidence = data.confidence || 50;
    document.getElementById('confidenceBar').style.width = `${confidence}%`;
    document.getElementById('confidenceBar').textContent = `${confidence}%`;
    
    // Update recommendation
    const recommendationBadge = document.getElementById('recommendationBadge');
    const recommendation = data.recommendation || 'HOLD';
    recommendationBadge.textContent = recommendation;
    
    if (recommendation === 'BUY') {
        recommendationBadge.className = 'badge fs-6 bg-success';
    } else if (recommendation === 'SELL') {
        recommendationBadge.className = 'badge fs-6 bg-danger';
    } else {
        recommendationBadge.className = 'badge fs-6 bg-warning';
    }
    
    // Create prediction chart
    createPredictionChart(data.historical_data, data.prediction_data);
    
    // Update AI Analysis
    updateAIAnalysis(data.ai_analysis);
    
    // Update Sentiment Analysis
    updateSentimentAnalysis(data.sentiment_analysis);
}

// Create prediction chart
function createPredictionChart(historicalData, predictionData) {
    const canvas = document.getElementById('predictionChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.predictionChartInstance) {
        window.predictionChartInstance.destroy();
    }
    
    // Prepare data
    const historicalDates = historicalData.map(d => d.date);
    const historicalPrices = historicalData.map(d => d.price);
    const predictionDates = predictionData.map(d => d.date);
    const predictionPrices = predictionData.map(d => d.price);
    
    // Combine dates for x-axis
    const allDates = [...historicalDates, ...predictionDates.slice(1)]; // Avoid duplicate current date
    
    window.predictionChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allDates,
            datasets: [
                {
                    label: 'Historical Price',
                    data: [...historicalPrices, ...Array(predictionDates.length - 1).fill(null)],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Predicted Price',
                    data: [...Array(historicalDates.length - 1).fill(null), ...predictionPrices],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Stock Price Prediction'
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Update AI Analysis section
function updateAIAnalysis(analysis) {
    const container = document.getElementById('aiAnalysis');
    if (!container || !analysis) return;
    
    container.innerHTML = `
        <div class="mb-3">
            <h6 class="text-primary">Trend Analysis</h6>
            <p><strong>Trend:</strong> ${analysis.trend}</p>
            <p><strong>Strength:</strong> ${analysis.strength}</p>
            <p><strong>Risk Level:</strong> <span class="badge ${getRiskBadgeClass(analysis.risk_level)}">${analysis.risk_level}</span></p>
        </div>
        
        <div class="mb-3">
            <h6 class="text-primary">Key Factors</h6>
            <ul class="list-unstyled">
                ${analysis.key_factors.map(factor => `<li><i class="fas fa-chevron-right text-muted me-2"></i>${factor}</li>`).join('')}
            </ul>
        </div>
        
        <div class="mb-3">
            <h6 class="text-primary">Model Information</h6>
            <p><strong>Model:</strong> ${analysis.model_used}</p>
            <p><strong>Data Quality:</strong> ${analysis.data_quality}</p>
        </div>
    `;
}

// Update Sentiment Analysis section
function updateSentimentAnalysis(analysis) {
    const container = document.getElementById('sentimentAnalysis');
    if (!container || !analysis) return;
    
    container.innerHTML = `
        <div class="mb-3">
            <h6 class="text-primary">Overall Sentiment</h6>
            <div class="d-flex align-items-center mb-2">
                <span class="badge ${getSentimentBadgeClass(analysis.overall_sentiment)} me-2">${analysis.overall_sentiment}</span>
                <span class="text-muted">Score: ${analysis.sentiment_score}</span>
            </div>
        </div>
        
        <div class="mb-3">
            <h6 class="text-primary">Sentiment Breakdown</h6>
            <p><strong>News Sentiment:</strong> ${analysis.news_sentiment}</p>
            <p><strong>Social Sentiment:</strong> ${analysis.social_sentiment}</p>
        </div>
        
        <div class="mb-3">
            <h6 class="text-primary">Key Themes</h6>
            <div class="d-flex flex-wrap gap-1">
                ${analysis.key_themes.map(theme => `<span class="badge bg-secondary">${theme}</span>`).join('')}
            </div>
        </div>
        
        <div class="mb-3">
            <h6 class="text-primary">Sources</h6>
            <p class="text-muted small">${analysis.sentiment_sources.join(', ')}</p>
        </div>
    `;
}

// Load technical chart data
async function loadTechnicalChart(symbol, chartType = 'candlestick') {
    if (!symbol) return;
    
    try {
        console.log(`Loading ${chartType} chart for ${symbol}`);
        
        const response = await fetch(`http://localhost:5000/api/technical-chart/${symbol}?type=${chartType}`);
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        
        const data = await response.json();
        
        if (data.success) {
            displayTechnicalChart(data);
            displayChartPatternAnalysis(data.patterns, data.indicators);
        } else {
            throw new Error(data.error || 'Failed to load chart data');
        }
        
    } catch (error) {
        console.error('Failed to load technical chart:', error);
        showTechnicalChartError(error.message);
    }
}

// Display technical chart based on type
function displayTechnicalChart(data) {
    const container = document.getElementById('technicalChart');
    if (!container) return;
    
    // Clear existing content
    container.innerHTML = '';
    
    // Create chart container
    const chartContainer = document.createElement('div');
    chartContainer.id = 'technicalChartContainer';
    chartContainer.style.height = '400px';
    container.appendChild(chartContainer);
    
    switch (data.chart_type) {
        case 'candlestick':
            displayCandlestickChart(data.data, data.symbol);
            break;
        case 'renko':
            displayRenkoChart(data.data, data.symbol);
            break;
        case 'kagi':
            displayKagiChart(data.data, data.symbol);
            break;
        case 'point_figure':
            displayPointFigureChart(data.data, data.symbol);
            break;
        case 'breakout':
            displayBreakoutChart(data.data, data.symbol);
            break;
        default:
            displayCandlestickChart(data.data, data.symbol);
    }
}

// Display candlestick chart using Plotly
function displayCandlestickChart(data, symbol) {
    const trace = {
        x: data.map(d => d.date),
        close: data.map(d => d.close),
        decreasing: { line: { color: '#ff4444' } },
        high: data.map(d => d.high),
        increasing: { line: { color: '#00ff00' } },
        low: data.map(d => d.low),
        open: data.map(d => d.open),
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
    };
    
    const layout = {
        title: `${symbol} - Candlestick Chart`,
        xaxis: { title: 'Date', rangeslider: { visible: false } },
        yaxis: { title: 'Price (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    Plotly.newPlot('technicalChartContainer', [trace], layout);
}

// Display Renko chart
function displayRenkoChart(data, symbol) {
    const traces = [];
    
    data.forEach((brick, index) => {
        const color = brick.direction === 1 ? '#00ff00' : '#ff4444';
        
        traces.push({
            x: [index, index + 1, index + 1, index, index],
            y: [brick.open, brick.open, brick.close, brick.close, brick.open],
            fill: 'toself',
            fillcolor: color,
            line: { color: color },
            mode: 'lines',
            name: `Brick ${index + 1}`,
            showlegend: false
        });
    });
    
    const layout = {
        title: `${symbol} - Renko Chart`,
        xaxis: { title: 'Brick Number' },
        yaxis: { title: 'Price (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    Plotly.newPlot('technicalChartContainer', traces, layout);
}

// Display Kagi chart
function displayKagiChart(data, symbol) {
    const x = [];
    const y = [];
    const colors = [];
    
    data.forEach((point, index) => {
        x.push(index);
        y.push(point.price);
        colors.push(point.direction === 1 ? '#00ff00' : '#ff4444');
    });
    
    const trace = {
        x: x,
        y: y,
        mode: 'lines+markers',
        line: { color: '#333333', width: 2 },
        marker: { 
            color: colors,
            size: 6,
            symbol: data.map(d => d.reversal ? 'diamond' : 'circle')
        },
        type: 'scatter'
    };
    
    const layout = {
        title: `${symbol} - Kagi Chart`,
        xaxis: { title: 'Time Points' },
        yaxis: { title: 'Price (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    Plotly.newPlot('technicalChartContainer', [trace], layout);
}

// Display Point & Figure chart
function displayPointFigureChart(data, symbol) {
    const traces = [];
    let columnIndex = 0;
    
    data.forEach((column, index) => {
        const symbol_char = column.type === 'X' ? 'X' : 'O';
        const color = column.type === 'X' ? '#00ff00' : '#ff4444';
        
        for (let i = 0; i < column.count; i++) {
            traces.push({
                x: [columnIndex],
                y: [column.price + (i * (column.price / column.count))],
                mode: 'text',
                text: [symbol_char],
                textfont: { color: color, size: 16 },
                showlegend: false
            });
        }
        columnIndex++;
    });
    
    const layout = {
        title: `${symbol} - Point & Figure Chart`,
        xaxis: { title: 'Column' },
        yaxis: { title: 'Price (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    Plotly.newPlot('technicalChartContainer', traces, layout);
}

// Display Breakout chart
function displayBreakoutChart(data, symbol) {
    const trace1 = {
        x: data.map(d => d.date),
        y: data.map(d => d.price),
        mode: 'lines',
        name: 'Price',
        line: { color: '#007bff' }
    };
    
    const trace2 = {
        x: data.map(d => d.date),
        y: data.map(d => d.resistance),
        mode: 'lines',
        name: 'Resistance',
        line: { color: '#ff4444', dash: 'dash' }
    };
    
    const trace3 = {
        x: data.map(d => d.date),
        y: data.map(d => d.support),
        mode: 'lines',
        name: 'Support',
        line: { color: '#00ff00', dash: 'dash' }
    };
    
    const layout = {
        title: `${symbol} - Breakout Chart`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    Plotly.newPlot('technicalChartContainer', [trace1, trace2, trace3], layout);
}

// Display chart pattern analysis
function displayChartPatternAnalysis(patterns, indicators) {
    // Show pattern analysis section
    const patternSection = document.getElementById('chartPatternAnalysis');
    if (patternSection) {
        patternSection.style.display = 'block';
    }
    
    // Update candlestick patterns
    const candlestickPatternsContainer = document.getElementById('candlestickPatterns');
    if (candlestickPatternsContainer && patterns.detected_patterns) {
        candlestickPatternsContainer.innerHTML = `
            <h6 class="text-primary mb-3">Detected Patterns</h6>
            ${patterns.detected_patterns.map(pattern => 
                `<div class="mb-2">
                    <span class="badge bg-info">${pattern}</span>
                </div>`
            ).join('')}
        `;
    }
    
    // Update technical indicators
    const technicalIndicatorsContainer = document.getElementById('technicalIndicators');
    if (technicalIndicatorsContainer && indicators) {
        technicalIndicatorsContainer.innerHTML = `
            <h6 class="text-primary mb-3">Key Indicators</h6>
            <div class="mb-2"><strong>RSI:</strong> ${indicators.rsi ? indicators.rsi.toFixed(2) : 'N/A'}</div>
            <div class="mb-2"><strong>MACD:</strong> ${indicators.macd ? indicators.macd.toFixed(2) : 'N/A'}</div>
            <div class="mb-2"><strong>SMA 20:</strong> ₹${indicators.sma_20 ? indicators.sma_20.toFixed(2) : 'N/A'}</div>
            <div class="mb-2"><strong>SMA 50:</strong> ₹${indicators.sma_50 ? indicators.sma_50.toFixed(2) : 'N/A'}</div>
        `;
    }
    
    // Update support & resistance
    const supportResistanceContainer = document.getElementById('supportResistance');
    if (supportResistanceContainer && patterns) {
        supportResistanceContainer.innerHTML = `
            <h6 class="text-primary mb-3">Key Levels</h6>
            <div class="mb-2"><strong>Resistance:</strong> 
                ${patterns.resistance_levels.map(level => `₹${level}`).join(', ')}
            </div>
            <div class="mb-2"><strong>Support:</strong> 
                ${patterns.support_levels.map(level => `₹${level}`).join(', ')}
            </div>
        `;
    }
}

// Show technical chart error
function showTechnicalChartError(message) {
    const container = document.getElementById('technicalChart');
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5 text-danger">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem;"></i>
                <p class="mt-2">Error loading chart: ${message}</p>
            </div>
        `;
    }
}

// Load and display top stocks
async function loadTopStocks(category) {
    try {
        console.log(`Loading top stocks for category: ${category}`);
        const response = await fetch(`http://localhost:5000/api/top-stocks?category=${category}`);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        displayTopStocks(data.stocks);
        
    } catch (error) {
        console.error('Failed to load top stocks:', error);
        showToast('Error', `Failed to load top stocks: ${error.message}`, 'error');
    }
}

// Display top stocks in the UI
function displayTopStocks(stocks) {
    const container = document.getElementById('topStocksList');
    if (!container) {
        console.error('Top stocks container not found');
        return;
    }
    
    container.innerHTML = '';
    
    stocks.forEach(stock => {
        const stockCard = createStockCard(stock);
        container.appendChild(stockCard);
    });
}

// Create a stock card element
function createStockCard(stock) {
    const card = document.createElement('div');
    card.className = 'col-lg-4 col-md-6 mb-4';
    
    const priceChangeClass = stock.price_change >= 0 ? 'text-success' : 'text-danger';
    const priceChangeIcon = stock.price_change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
    
    card.innerHTML = `
        <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6 class="mb-0">${stock.symbol}</h6>
                <span class="badge bg-secondary">${stock.sector}</span>
            </div>
            <div class="card-body">
                <h6 class="card-title">${stock.name}</h6>
                <div class="mb-3">
                    <div class="d-flex justify-content-between">
                        <span>Current Price:</span>
                        <strong>₹${stock.current_price}</strong>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Predicted Price:</span>
                        <strong class="text-success">₹${stock.predicted_price}</strong>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Change:</span>
                        <span class="${priceChangeClass}">
                            <i class="fas ${priceChangeIcon}"></i>
                            ${Math.abs(stock.price_change).toFixed(2)}%
                        </span>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Confidence:</span>
                        <span>${stock.prediction_confidence}%</span>
                    </div>
                </div>
                <button class="btn btn-sm btn-primary w-100" onclick="selectStockForAnalysis('${stock.symbol}')">
                    Analyze Stock
                </button>
            </div>
        </div>
    `;
    
    return card;
}

// Select stock for detailed analysis
window.selectStockForAnalysis = function(symbol) {
    document.getElementById('stockSymbol').value = symbol;
    scrollToSection('prediction');
};

// Helper functions for styling
function getRiskBadgeClass(riskLevel) {
    switch(riskLevel.toLowerCase()) {
        case 'low': return 'bg-success';
        case 'medium': return 'bg-warning';
        case 'high': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

function getSentimentBadgeClass(sentiment) {
    switch(sentiment.toLowerCase()) {
        case 'positive': return 'bg-success';
        case 'negative': return 'bg-danger';
        case 'neutral': return 'bg-warning';
        default: return 'bg-secondary';
    }
}

// Show toast notifications
function showToast(title, message, type = 'info') {
    console.log(`Toast: ${title} - ${message}`);
    
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const toast = document.getElementById('notificationToast');
    
    if (toastTitle && toastMessage && toast) {
        toastTitle.textContent = title;
        toastMessage.textContent = message;
        
        // Show toast using Bootstrap (if available)
        if (typeof bootstrap !== 'undefined') {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
        }
    } else {
        // Fallback to alert
        alert(`${title}: ${message}`);
    }
}

// Make functions globally available
window.makePrediction = makePrediction;
window.showToast = showToast;
window.loadTopStocks = loadTopStocks;
window.loadTechnicalChart = loadTechnicalChart;
