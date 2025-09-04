/**
 * Main JavaScript file for Stock Market Predictor
 * Handles application initialization, user interactions, and API communications
 */

// Global variables
let currentStock = null;
let predictionChart = null;
let heroChart = null;
let currentChartData = null;

// Application initialization
function initializeApp() {
    console.log('Initializing Stock Market Predictor...');
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Load market indices
    loadMarketIndices();
    
    // Initialize hero chart
    initializeHeroChart();
    
    // Load initial top stocks
    loadTopStocks('safe');
    
    console.log('Application initialized successfully');
}

// Initialize all event listeners
function initializeEventListeners() {
    // Prediction form
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }
    
    // Quick stock buttons
    const quickStockButtons = document.querySelectorAll('.quick-stock-btn');
    quickStockButtons.forEach(button => {
        button.addEventListener('click', function() {
            const symbol = this.getAttribute('data-symbol');
            document.getElementById('stockSymbol').value = symbol;
            handlePredictionSubmit({ preventDefault: () => {} });
        });
    });
    
    // Volatility category buttons
    const volatilityButtons = document.querySelectorAll('.volatility-btn');
    volatilityButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            volatilityButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            loadTopStocks(category);
        });
    });
    
    // Chart type selector
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', function() {
            if (currentStock) {
                loadTechnicalChart(currentStock, this.value);
            }
        });
    }
    
    // Search stock button
    const searchStockBtn = document.getElementById('searchStockBtn');
    if (searchStockBtn) {
        searchStockBtn.addEventListener('click', function() {
            const symbol = document.getElementById('stockSymbol').value;
            if (symbol) {
                searchStock(symbol);
            }
        });
    }
    
    // Stock symbol input - search on Enter
    const stockSymbolInput = document.getElementById('stockSymbol');
    if (stockSymbolInput) {
        stockSymbolInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchStock(this.value);
            }
        });
        
        // Auto-complete functionality (basic)
        stockSymbolInput.addEventListener('input', function() {
            // Implement auto-complete logic here if needed
        });
    }
}

// Handle prediction form submission
async function handlePredictionSubmit(event) {
    event.preventDefault();
    
    const stockSymbol = document.getElementById('stockSymbol').value.trim();
    const predictionDays = parseInt(document.getElementById('predictionDays').value);
    
    if (!stockSymbol) {
        showNotification('Error', 'Please enter a stock symbol', 'error');
        return;
    }
    
    currentStock = stockSymbol.toUpperCase();
    
    // Show loading state
    showPredictionLoading();
    
    try {
        // Make prediction API call
        const predictionData = await apiCall('/api/predict', 'POST', {
            symbol: currentStock,
            days_ahead: predictionDays
        });
        
        if (predictionData.error) {
            throw new Error(predictionData.error);
        }
        
        // Display prediction results
        displayPredictionResults(predictionData);
        
        // Load technical charts
        loadTechnicalChart(currentStock, 'candlestick');
        
        showNotification('Success', `Prediction completed for ${currentStock}`, 'success');
        
    } catch (error) {
        console.error('Prediction error:', error);
        showNotification('Error', `Failed to predict ${currentStock}: ${error.message}`, 'error');
        hidePredictionLoading();
    }
}

// Display prediction results
function displayPredictionResults(data) {
    console.log('Displaying prediction results:', data);
    
    // Hide loading and initial states
    hidePredictionLoading();
    document.getElementById('predictionInitial').classList.add('d-none');
    
    // Show results container
    const resultsContainer = document.getElementById('predictionResults');
    resultsContainer.classList.remove('d-none');
    resultsContainer.classList.add('fade-in');
    
    // Update stock information
    document.getElementById('stockName').textContent = data.symbol;
    document.getElementById('currentPrice').textContent = `₹${data.current_price}`;
    
    // Calculate and display price change (dummy calculation for demo)
    const priceChangeElement = document.getElementById('priceChange');
    const avgChange = data.average_change || 0;
    priceChangeElement.textContent = `${avgChange > 0 ? '+' : ''}${avgChange.toFixed(2)}%`;
    priceChangeElement.className = `price-change ${avgChange >= 0 ? 'positive' : 'negative'}`;
    
    // Update predicted price
    const predictedPrice = data.predicted_prices && data.predicted_prices.length > 0 
        ? data.predicted_prices[data.predicted_prices.length - 1] 
        : data.current_price;
    document.getElementById('predictedPrice').textContent = `₹${predictedPrice.toFixed(2)}`;
    
    // Update confidence score
    const confidence = data.confidence_score || data.confidence || 0;
    const confidenceBar = document.getElementById('confidenceBar');
    confidenceBar.style.width = `${confidence}%`;
    confidenceBar.textContent = `${confidence.toFixed(0)}%`;
    confidenceBar.className = `progress-bar ${getConfidenceColor(confidence)}`;
    
    // Update recommendation
    const recommendation = data.recommendation || { action: 'Hold', confidence: confidence };
    const recommendationBadge = document.getElementById('recommendationBadge');
    recommendationBadge.textContent = recommendation.action || 'Hold';
    recommendationBadge.className = `badge fs-6 ${getRecommendationColor(recommendation.action)}`;
    
    // Update prediction chart
    updatePredictionChart(data);
    
    // Update analysis sections
    updateAIAnalysis(data);
    updateSentimentAnalysis(data);
    
    // Scroll to results
    setTimeout(() => {
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Update prediction chart
function updatePredictionChart(data) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    // Destroy existing chart
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    // Prepare chart data
    const labels = [];
    const historicalPrices = [];
    const predictedPrices = [];
    
    // Add some historical data points (mock data)
    const today = new Date();
    for (let i = 30; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toISOString().split('T')[0]);
        
        if (i === 0) {
            historicalPrices.push(data.current_price);
        } else {
            // Generate mock historical data around current price
            const variation = (Math.random() - 0.5) * 0.1;
            historicalPrices.push(data.current_price * (1 + variation));
        }
    }
    
    // Add predicted data points
    if (data.predicted_prices && data.predicted_prices.length > 0) {
        data.predicted_prices.forEach((price, index) => {
            const date = new Date(today);
            date.setDate(date.getDate() + index + 1);
            labels.push(date.toISOString().split('T')[0]);
            historicalPrices.push(null);
            predictedPrices.push(price);
        });
    }
    
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: historicalPrices,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                },
                {
                    label: 'Predicted Price',
                    data: [...historicalPrices.slice(0, -1), data.current_price, ...data.predicted_prices],
                    borderColor: 'rgb(239, 68, 68)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: 'rgb(239, 68, 68)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                title: {
                    display: true,
                    text: `${data.symbol} - Price Prediction`,
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: 'white',
                    bodyColor: 'white',
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ₹${context.parsed.y?.toFixed(2) || 'N/A'}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        }
    });
}

// Update AI Analysis section
function updateAIAnalysis(data) {
    const aiAnalysisContainer = document.getElementById('aiAnalysis');
    
    const confidence = data.confidence_score || data.confidence || 0;
    const avgChange = data.average_change || 0;
    
    let analysisHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Model Confidence</span>
            <span class="analysis-value">${confidence.toFixed(1)}%</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Expected Change</span>
            <span class="analysis-value ${avgChange >= 0 ? 'bullish' : 'bearish'}">
                ${avgChange > 0 ? '+' : ''}${avgChange.toFixed(2)}%
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Trend Direction</span>
            <span class="analysis-value ${avgChange >= 0 ? 'bullish' : 'bearish'}">
                ${avgChange >= 0 ? 'Upward' : 'Downward'}
            </span>
        </div>
    `;
    
    // Add model-specific confidences if available
    if (data.model_confidences) {
        analysisHTML += '<hr><small class="text-muted">Model Breakdown:</small>';
        Object.entries(data.model_confidences).forEach(([model, conf]) => {
            analysisHTML += `
                <div class="analysis-item">
                    <span class="analysis-label">${model.toUpperCase()}</span>
                    <span class="analysis-value">${conf.toFixed(1)}%</span>
                </div>
            `;
        });
    }
    
    aiAnalysisContainer.innerHTML = analysisHTML;
}

// Update Sentiment Analysis section
function updateSentimentAnalysis(data) {
    const sentimentContainer = document.getElementById('sentimentAnalysis');
    
    const sentimentScore = data.sentiment_score || 0;
    const sentimentClass = sentimentScore > 0.1 ? 'positive' : sentimentScore < -0.1 ? 'negative' : 'neutral';
    const sentimentText = sentimentScore > 0.1 ? 'Positive' : sentimentScore < -0.1 ? 'Negative' : 'Neutral';
    
    const sentimentHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Overall Sentiment</span>
            <span class="analysis-value ${sentimentClass}">${sentimentText}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Sentiment Score</span>
            <span class="analysis-value">${sentimentScore.toFixed(3)}</span>
        </div>
        <div class="mb-3">
            <div class="sentiment-meter">
                <div class="sentiment-fill ${sentimentClass}" 
                     style="width: ${Math.abs(sentimentScore) * 100}%"></div>
            </div>
            <small class="text-muted">Based on recent news analysis</small>
        </div>
        <div class="alert alert-info alert-sm">
            <i class="fas fa-info-circle me-2"></i>
            <small>Sentiment analysis combines news headlines, market reports, and social media mentions.</small>
        </div>
    `;
    
    sentimentContainer.innerHTML = sentimentHTML;
}

// Load market indices
async function loadMarketIndices() {
    try {
        // For demo purposes, using mock data
        // In production, this would call: const indices = await apiCall('/api/market-indices');
        const indices = {
            'NIFTY 50': { current_price: 19800.45, change: 145.30, change_percent: 0.74 },
            'SENSEX': { current_price: 66150.20, change: -89.45, change_percent: -0.13 },
            'BANK NIFTY': { current_price: 44250.80, change: 256.70, change_percent: 0.58 },
            'NIFTY IT': { current_price: 28950.15, change: -125.40, change_percent: -0.43 }
        };
        
        displayMarketIndices(indices);
    } catch (error) {
        console.error('Error loading market indices:', error);
    }
}

// Display market indices
function displayMarketIndices(indices) {
    const container = document.getElementById('marketIndices');
    
    let indicesHTML = '';
    Object.entries(indices).forEach(([name, data]) => {
        const changeClass = data.change >= 0 ? 'positive' : 'negative';
        const changeIcon = data.change >= 0 ? '↑' : '↓';
        
        indicesHTML += `
            <div class="col-6 col-lg-3 mb-3">
                <div class="market-index-card">
                    <div class="index-name">${name}</div>
                    <div class="index-price">${data.current_price.toFixed(2)}</div>
                    <div class="index-change ${changeClass}">
                        ${changeIcon} ${Math.abs(data.change).toFixed(2)} (${Math.abs(data.change_percent).toFixed(2)}%)
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = indicesHTML;
}

// Load top stocks by volatility category
async function loadTopStocks(category) {
    try {
        showLoadingOverlay();
        
        const stocks = await apiCall(`/api/top-stocks?category=${category}`);
        displayTopStocks(stocks.stocks || [], category);
        
    } catch (error) {
        console.error(`Error loading ${category} stocks:`, error);
        showNotification('Error', `Failed to load ${category} stocks`, 'error');
        
        // Display mock data for demo
        displayMockTopStocks(category);
    } finally {
        hideLoadingOverlay();
    }
}

// Display top stocks
function displayTopStocks(stocks, category) {
    const container = document.getElementById('topStocksList');
    
    if (!stocks || stocks.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No stocks found for ${category} category
                </div>
            </div>
        `;
        return;
    }
    
    let stocksHTML = '';
    stocks.forEach(stock => {
        const changeClass = stock.price_change >= 0 ? 'positive' : 'negative';
        const changeIcon = stock.price_change >= 0 ? '↑' : '↓';
        
        stocksHTML += `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="stock-card" onclick="selectStock('${stock.symbol}')">
                    <div class="stock-symbol">${stock.symbol}</div>
                    <div class="stock-name">${stock.name}</div>
                    <div class="stock-price-info">
                        <div class="stock-current-price">₹${stock.current_price}</div>
                        <div class="stock-change ${changeClass}">
                            ${changeIcon} ${Math.abs(stock.price_change).toFixed(2)}%
                        </div>
                    </div>
                    <div class="volatility-indicator">
                        <span class="text-muted small">Volatility: ${stock.volatility?.toFixed(1) || 'N/A'}%</span>
                        <div class="volatility-bar ${category}"></div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = stocksHTML;
}

// Display mock top stocks for demo
function displayMockTopStocks(category) {
    const mockStocks = {
        safe: [
            { symbol: 'HDFCBANK', name: 'HDFC Bank Ltd', current_price: 1542.30, price_change: 0.85, volatility: 12.5 },
            { symbol: 'TCS', name: 'Tata Consultancy Services', current_price: 3420.75, price_change: 1.20, volatility: 14.2 },
            { symbol: 'INFY', name: 'Infosys Ltd', current_price: 1456.90, price_change: -0.45, volatility: 13.8 },
            { symbol: 'WIPRO', name: 'Wipro Ltd', current_price: 425.60, price_change: 0.65, volatility: 11.9 },
            { symbol: 'ITC', name: 'ITC Ltd', current_price: 412.30, price_change: -0.25, volatility: 10.5 }
        ],
        volatile: [
            { symbol: 'RELIANCE', name: 'Reliance Industries', current_price: 2456.80, price_change: 2.15, volatility: 18.7 },
            { symbol: 'ICICIBANK', name: 'ICICI Bank Ltd', current_price: 945.25, price_change: -1.85, volatility: 19.3 },
            { symbol: 'BHARTIAIRTEL', name: 'Bharti Airtel Ltd', current_price: 825.40, price_change: 1.95, volatility: 17.6 },
            { symbol: 'MARUTI', name: 'Maruti Suzuki India', current_price: 9245.60, price_change: -2.40, volatility: 20.1 },
            { symbol: 'ASIANPAINT', name: 'Asian Paints Ltd', current_price: 3156.30, price_change: 1.75, volatility: 16.8 }
        ],
        highly_volatile: [
            { symbol: 'ADANIENTS', name: 'Adani Enterprises', current_price: 2845.70, price_change: 4.25, volatility: 35.2 },
            { symbol: 'TATAMOTORS', name: 'Tata Motors Ltd', current_price: 725.90, price_change: -3.85, volatility: 32.8 },
            { symbol: 'BAJFINANCE', name: 'Bajaj Finance Ltd', current_price: 6420.15, price_change: 5.10, volatility: 28.9 },
            { symbol: 'KOTAKBANK', name: 'Kotak Mahindra Bank', current_price: 1789.45, price_change: -4.20, volatility: 31.5 },
            { symbol: 'HINDALCO', name: 'Hindalco Industries', current_price: 415.80, price_change: 6.75, volatility: 38.1 }
        ]
    };
    
    displayTopStocks(mockStocks[category] || [], category);
}

// Select stock from top stocks list
function selectStock(symbol) {
    document.getElementById('stockSymbol').value = symbol;
    currentStock = symbol;
    
    // Scroll to prediction section
    scrollToSection('prediction');
    
    // Auto-trigger prediction
    setTimeout(() => {
        handlePredictionSubmit({ preventDefault: () => {} });
    }, 500);
}

// Load technical chart
async function loadTechnicalChart(symbol, chartType) {
    try {
        const chartData = await apiCall(`/api/chart-data/${symbol}?type=${chartType}`);
        displayTechnicalChart(chartData, chartType);
        
        // Load chart pattern analysis
        loadChartPatternAnalysis(symbol);
        
    } catch (error) {
        console.error('Error loading technical chart:', error);
        displayMockTechnicalChart(symbol, chartType);
    }
}

// Display technical chart using Plotly
function displayTechnicalChart(chartData, chartType) {
    const chartContainer = document.getElementById('technicalChart');
    
    if (chartType === 'candlestick') {
        displayCandlestickChart(chartContainer, chartData);
    } else {
        displayAlternativeChart(chartContainer, chartData, chartType);
    }
    
    // Show pattern analysis
    document.getElementById('chartPatternAnalysis').style.display = 'block';
}

// Display candlestick chart
function displayCandlestickChart(container, data) {
    if (!data.data || data.data.length === 0) {
        container.innerHTML = '<div class="text-center py-5 text-muted">No chart data available</div>';
        return;
    }
    
    const trace = {
        x: data.data.map(d => d.x),
        open: data.data.map(d => d.open),
        high: data.data.map(d => d.high),
        low: data.data.map(d => d.low),
        close: data.data.map(d => d.close),
        type: 'candlestick',
        name: 'OHLC',
        increasing: { line: { color: '#22c55e' } },
        decreasing: { line: { color: '#ef4444' } }
    };
    
    const layout = {
        title: data.title || 'Candlestick Chart',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price (₹)' },
        height: 500,
        showlegend: false
    };
    
    Plotly.newPlot(container, [trace], layout, { responsive: true });
}

// Display alternative charts (Renko, Kagi, etc.)
function displayAlternativeChart(container, data, chartType) {
    // For demo purposes, display a simple message
    container.innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-chart-area fa-3x text-muted mb-3"></i>
            <h5>${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Chart</h5>
            <p class="text-muted">Chart visualization for ${currentStock}</p>
            <small class="text-muted">Advanced chart types are being processed...</small>
        </div>
    `;
}

// Display mock technical chart for demo
function displayMockTechnicalChart(symbol, chartType) {
    const container = document.getElementById('technicalChart');
    
    // Generate mock candlestick data
    const mockData = generateMockCandlestickData();
    displayCandlestickChart(container, { data: mockData, title: `${symbol} - ${chartType} Chart` });
    
    // Show pattern analysis
    document.getElementById('chartPatternAnalysis').style.display = 'block';
    loadMockChartPatternAnalysis();
}

// Generate mock candlestick data
function generateMockCandlestickData() {
    const data = [];
    const today = new Date();
    let price = 1000 + Math.random() * 500; // Starting price
    
    for (let i = 50; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        
        const open = price;
        const change = (Math.random() - 0.5) * 20;
        const close = Math.max(open + change, 10);
        const high = Math.max(open, close) + Math.random() * 10;
        const low = Math.min(open, close) - Math.random() * 10;
        
        data.push({
            x: date.toISOString().split('T')[0],
            open: parseFloat(open.toFixed(2)),
            high: parseFloat(high.toFixed(2)),
            low: parseFloat(Math.max(low, 10).toFixed(2)),
            close: parseFloat(close.toFixed(2))
        });
        
        price = close;
    }
    
    return data;
}

// Load chart pattern analysis
async function loadChartPatternAnalysis(symbol) {
    try {
        // In production, this would call the actual API
        // const analysis = await apiCall(`/api/stock/${symbol}/analysis`);
        loadMockChartPatternAnalysis();
    } catch (error) {
        console.error('Error loading chart pattern analysis:', error);
        loadMockChartPatternAnalysis();
    }
}

// Load mock chart pattern analysis
function loadMockChartPatternAnalysis() {
    // Candlestick Patterns
    const candlestickPatterns = document.getElementById('candlestickPatterns');
    candlestickPatterns.innerHTML = `
        <div class="pattern-item">
            <span>Doji Pattern</span>
            <span class="pattern-strength moderate">Moderate</span>
        </div>
        <div class="pattern-item">
            <span>Hammer</span>
            <span class="pattern-strength strong">Strong</span>
        </div>
        <div class="pattern-item">
            <span>Engulfing</span>
            <span class="pattern-strength weak">Weak</span>
        </div>
    `;
    
    // Technical Indicators
    const technicalIndicators = document.getElementById('technicalIndicators');
    technicalIndicators.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">RSI (14)</span>
            <span class="analysis-value">65.4</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">MACD</span>
            <span class="analysis-value bullish">Bullish</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">SMA (20)</span>
            <span class="analysis-value">₹1,245.60</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Bollinger Bands</span>
            <span class="analysis-value neutral">Neutral</span>
        </div>
    `;
    
    // Support & Resistance
    const supportResistance = document.getElementById('supportResistance');
    supportResistance.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Resistance 1</span>
            <span class="analysis-value">₹1,350.00</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Resistance 2</span>
            <span class="analysis-value">₹1,420.00</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Support 1</span>
            <span class="analysis-value">₹1,200.00</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Support 2</span>
            <span class="analysis-value">₹1,150.00</span>
        </div>
    `;
}

// Initialize hero chart
function initializeHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;
    
    // Generate sample market data
    const labels = [];
    const data = [];
    const today = new Date();
    
    for (let i = 30; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString());
        data.push(18000 + Math.random() * 2000 + i * 10);
    }
    
    heroChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Market Index',
                data: data,
                borderColor: 'rgba(255, 255, 255, 0.8)',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
}

// Search stock function
async function searchStock(symbol) {
    try {
        // In production, this would search for stock suggestions
        const suggestions = await apiCall(`/api/search-stocks?q=${symbol}`);
        // For now, just update the input with the formatted symbol
        document.getElementById('stockSymbol').value = symbol.toUpperCase();
    } catch (error) {
        console.error('Error searching stock:', error);
    }
}

// Show prediction loading state
function showPredictionLoading() {
    document.getElementById('predictionInitial').classList.add('d-none');
    document.getElementById('predictionResults').classList.add('d-none');
    document.getElementById('predictionLoading').classList.remove('d-none');
}

// Hide prediction loading state
function hidePredictionLoading() {
    document.getElementById('predictionLoading').classList.add('d-none');
}

// Show/hide loading overlay
function showLoadingOverlay() {
    document.getElementById('loadingOverlay').classList.remove('d-none');
}

function hideLoadingOverlay() {
    document.getElementById('loadingOverlay').classList.add('d-none');
}

// Utility functions
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function getConfidenceColor(confidence) {
    if (confidence >= 80) return 'bg-success';
    if (confidence >= 60) return 'bg-warning';
    return 'bg-danger';
}

function getRecommendationColor(action) {
    switch (action?.toLowerCase()) {
        case 'strong buy':
        case 'buy':
            return 'bg-success';
        case 'strong sell':
        case 'sell':
            return 'bg-danger';
        case 'hold':
        default:
            return 'bg-warning';
    }
}

function showNotification(title, message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Remove existing type classes
    toast.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info');
    
    // Add appropriate type class
    switch (type) {
        case 'success':
            toast.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            toast.classList.add('bg-danger', 'text-white');
            break;
        case 'warning':
            toast.classList.add('bg-warning');
            break;
        default:
            toast.classList.add('bg-info', 'text-white');
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Export functions for use in other modules
window.initializeApp = initializeApp;
window.scrollToSection = scrollToSection;