// Enhanced Real-time JavaScript for Stock Market Predictor
// Global variables for real-time updates
let realtimeInterval;
let predictionChart = null;
let technicalChart = null;
let heroChart = null;
let currentSymbols = new Set();
let lastUpdateTime = null;
let isMarketOpen = false;

// Initialize the enhanced application
function initializeApp() {
    console.log('Initializing enhanced stock market predictor...');
    
    initializeTheme();
    initializeHeroChart();
    startRealtimeUpdates();
    loadMarketIndices();
    loadTopStocks('safe', 5);
    setupEventListeners();
    checkPredictStock();
    setupRealtimePortfolioUpdates();
    
    // Show market status
    updateMarketStatus();
    
    console.log('Enhanced application initialized successfully');
}

// Theme Management (enhanced)
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

function toggleTheme() {
    const html = document.documentElement;
    const themeIcon = document.getElementById('themeIcon');
    
    if (html.getAttribute('data-theme') === 'light') {
        html.setAttribute('data-theme', 'dark');
        if (themeIcon) themeIcon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'dark');
    } else {
        html.setAttribute('data-theme', 'light');
        if (themeIcon) themeIcon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'light');
    }
    
    updateChartsForTheme();
}

// Real-time Updates System
function startRealtimeUpdates() {
    console.log('Starting real-time update system...');
    
    // Update every 60 seconds during market hours, every 5 minutes when closed
    const updateInterval = isMarketOpen ? 60000 : 300000; // 1 min or 5 min
    
    if (realtimeInterval) {
        clearInterval(realtimeInterval);
    }
    
    realtimeInterval = setInterval(() => {
        updateRealtimePrices();
        updateMarketIndices();
        updatePortfolioValues();
    }, updateInterval);
    
    // Initial update
    updateRealtimePrices();
}

async function updateRealtimePrices() {
    if (currentSymbols.size === 0) return;
    
    try {
        const symbolsArray = Array.from(currentSymbols);
        const response = await fetch('/api/real-time-prices?' + new URLSearchParams({
            symbols: symbolsArray.join(',')
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.prices) {
            updatePriceDisplays(data.prices);
            isMarketOpen = data.market_open;
            lastUpdateTime = new Date(data.timestamp);
            
            // Update market status indicator
            updateMarketStatus();
            
            // Show real-time indicator
            showRealtimeIndicator();
        }
        
    } catch (error) {
        console.error('Error updating real-time prices:', error);
        showRealtimeError();
    }
}

function updatePriceDisplays(prices) {
    // Update prices throughout the interface
    Object.keys(prices).forEach(symbol => {
        const priceData = prices[symbol];
        if (priceData.price) {
            updatePriceElements(symbol, priceData.price, priceData.is_real);
        }
    });
}

function updatePriceElements(symbol, price, isReal) {
    // Update all elements showing this symbol's price
    const priceElements = document.querySelectorAll(`[data-symbol="${symbol}"]`);
    
    priceElements.forEach(element => {
        const formattedPrice = `₹${parseFloat(price).toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;
        
        element.textContent = formattedPrice;
        
        // Add real-time indicator
        element.classList.toggle('real-price', isReal);
        element.classList.toggle('cached-price', !isReal);
        
        // Animate price change
        element.classList.add('price-updated');
        setTimeout(() => element.classList.remove('price-updated'), 1000);
    });
}

async function updateMarketIndices() {
    try {
        const response = await fetch('/api/market-indices');
        const data = await response.json();
        
        if (data.indices) {
            displayMarketIndices(data.indices);
            isMarketOpen = data.market_open;
        }
        
    } catch (error) {
        console.error('Error updating market indices:', error);
    }
}

function displayMarketIndices(indices) {
    const container = document.getElementById('marketIndices');
    if (!container) return;
    
    const indicesHTML = Object.keys(indices).map(name => {
        const index = indices[name];
        const displayName = name.replace('_', ' ').replace('NIFTY', 'Nifty').replace('SENSEX', 'Sensex');
        const changeClass = index.change >= 0 ? 'text-success' : 'text-danger';
        const changeIcon = index.change >= 0 ? 'up' : 'down';
        
        return `
            <div class="col-md-3 mb-3">
                <div class="text-center market-index" data-symbol="${name}">
                    <h5 class="mb-1" data-symbol="${name}">${index.current_price.toLocaleString('en-IN')}</h5>
                    <div class="small text-muted">${displayName}</div>
                    <div class="small ${changeClass}">
                        <i class="fas fa-arrow-${changeIcon} me-1"></i>
                        ${index.change >= 0 ? '+' : ''}${index.change.toFixed(2)} (${index.change_pct >= 0 ? '+' : ''}${index.change_pct.toFixed(2)}%)
                    </div>
                    <small class="text-muted d-block">
                        ${new Date(index.timestamp).toLocaleTimeString('en-IN')}
                    </small>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = indicesHTML;
}

function updateMarketStatus() {
    const statusElements = document.querySelectorAll('.market-status');
    const statusText = isMarketOpen ? 'Market Open' : 'Market Closed';
    const statusClass = isMarketOpen ? 'text-success' : 'text-danger';
    
    statusElements.forEach(element => {
        element.textContent = statusText;
        element.className = `market-status ${statusClass}`;
    });
    
    // Update page title with market status
    const titleElement = document.querySelector('title');
    if (titleElement && !titleElement.textContent.includes('●')) {
        const indicator = isMarketOpen ? '🟢' : '🔴';
        titleElement.textContent = `${indicator} ${titleElement.textContent}`;
    }
}

function showRealtimeIndicator() {
    // Show a subtle indicator that prices are updating
    const indicator = document.getElementById('realtimeIndicator');
    if (!indicator) {
        const div = document.createElement('div');
        div.id = 'realtimeIndicator';
        div.className = 'realtime-indicator';
        div.innerHTML = `
            <i class="fas fa-circle text-success pulse"></i>
            <span class="ms-2">Live</span>
        `;
        document.body.appendChild(div);
    }
    
    const timeString = lastUpdateTime ? lastUpdateTime.toLocaleTimeString('en-IN') : 'Now';
    indicator.title = `Last updated: ${timeString}`;
}

function showRealtimeError() {
    const indicator = document.getElementById('realtimeIndicator');
    if (indicator) {
        indicator.innerHTML = `
            <i class="fas fa-exclamation-triangle text-warning"></i>
            <span class="ms-2">Connection Issue</span>
        `;
    }
}

// Enhanced Portfolio Updates
function setupRealtimePortfolioUpdates() {
    // Get portfolio symbols and add to real-time tracking
    const portfolioSymbols = document.querySelectorAll('[data-portfolio-symbol]');
    portfolioSymbols.forEach(element => {
        const symbol = element.getAttribute('data-portfolio-symbol');
        if (symbol) {
            currentSymbols.add(symbol);
        }
    });
}

async function updatePortfolioValues() {
    try {
        const response = await fetch('/api/portfolio/get');
        const data = await response.json();
        
        if (data.portfolio) {
            updatePortfolioDisplay(data.portfolio, data.summary);
        }
        
    } catch (error) {
        console.error('Error updating portfolio values:', error);
    }
}

function updatePortfolioDisplay(portfolio, summary) {
    // Update portfolio summary with real-time values
    if (summary) {
        const totalInvested = document.getElementById('totalInvested');
        const currentValue = document.getElementById('currentValue');
        const totalProfitLoss = document.getElementById('totalProfitLoss');
        const totalProfitLossPct = document.getElementById('totalProfitLossPct');
        
        if (totalInvested) totalInvested.textContent = `₹${summary.total_invested.toLocaleString()}`;
        if (currentValue) currentValue.textContent = `₹${summary.total_current_value.toLocaleString()}`;
        
        if (totalProfitLoss) {
            totalProfitLoss.textContent = `₹${Math.abs(summary.total_profit_loss).toLocaleString()}`;
            totalProfitLoss.className = summary.total_profit_loss >= 0 ? 'summary-value profit' : 'summary-value loss';
        }
        
        if (totalProfitLossPct) {
            totalProfitLossPct.textContent = `${summary.total_profit_loss_pct >= 0 ? '+' : ''}${summary.total_profit_loss_pct.toFixed(2)}%`;
            totalProfitLossPct.className = summary.total_profit_loss_pct >= 0 ? 'summary-value profit' : 'summary-value loss';
        }
    }
}

// Enhanced Prediction with Real-time Data
async function handlePredictionSubmit(event, stockSymbol = null) {
    if (event) event.preventDefault();
    
    const symbol = stockSymbol || document.getElementById('stockInput').value.trim();
    const days = document.getElementById('daysAhead') ? document.getElementById('daysAhead').value : '5';
    
    if (!symbol) {
        showAdvancedToast('Error', 'Please enter a stock symbol', 'error');
        return;
    }
    
    // Add symbol to real-time tracking
    currentSymbols.add(symbol.toUpperCase());
    
    showPredictionLoading(true);
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                symbol: symbol, 
                days_ahead: parseInt(days) 
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayEnhancedPredictionResults(data);
        updateTechnicalChart('candlestick', data.symbol);
        
        // Show success message with market status
        const marketMsg = data.market_open ? 'using live market data' : 'using last available prices';
        showAdvancedToast('Prediction Complete', `Analysis completed ${marketMsg}`, 'success');
        
    } catch (error) {
        console.error('Prediction error:', error);
        showAdvancedToast('Prediction Failed', error.message, 'error');
        showPredictionInitial();
    } finally {
        showPredictionLoading(false);
    }
}

function displayEnhancedPredictionResults(data) {
    // Hide loading and show results
    document.getElementById('predictionLoading').style.display = 'none';
    document.getElementById('predictionInitial').style.display = 'none';
    document.getElementById('predictionResults').classList.remove('d-none');
    
    // Update basic info with real-time indicator
    const stockNameElement = document.getElementById('stockName');
    const currentPriceElement = document.getElementById('currentPrice');
    const predictedPriceElement = document.getElementById('predictedPrice');
    
    if (stockNameElement) {
        stockNameElement.textContent = `${data.symbol} - ${data.name}`;
    }
    
    if (currentPriceElement) {
        currentPriceElement.textContent = `₹${data.current_price.toLocaleString()}`;
        currentPriceElement.setAttribute('data-symbol', data.symbol);
        currentPriceElement.classList.add(data.is_real_price ? 'real-price' : 'cached-price');
    }
    
    if (predictedPriceElement) {
        predictedPriceElement.textContent = `₹${data.predicted_price.toLocaleString()}`;
    }
    
    // Update prediction period label
    const periodLabel = document.getElementById('predictionPeriodLabel');
    if (periodLabel) {
        periodLabel.textContent = `(${data.days_ahead}-day prediction)`;
    }
    
    // Update price change with enhanced styling
    const priceChange = data.predicted_price - data.current_price;
    const priceChangeElement = document.getElementById('priceChange');
    if (priceChangeElement) {
        const changeClass = priceChange >= 0 ? 'profit' : 'loss';
        const changeIcon = priceChange >= 0 ? 'up' : 'down';
        
        priceChangeElement.textContent = `${priceChange >= 0 ? '+' : ''}₹${Math.abs(priceChange).toLocaleString()} (${data.price_change_pct >= 0 ? '+' : ''}${data.price_change_pct.toFixed(2)}%)`;
        priceChangeElement.className = `price-change ${changeClass}`;
        priceChangeElement.innerHTML = `
            <i class="fas fa-arrow-${changeIcon} me-1"></i>
            ${priceChangeElement.textContent}
        `;
    }
    
    // Update confidence with enhanced display
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    if (confidenceBar && confidenceText) {
        confidenceBar.style.width = `${data.confidence}%`;
        confidenceBar.className = `progress-bar ${getConfidenceClass(data.confidence)}`;
        confidenceText.textContent = `${data.confidence}%`;
    }
    
    // Update recommendation with enhanced badge
    const recommendationBadge = document.getElementById('recommendationBadge');
    if (recommendationBadge) {
        recommendationBadge.textContent = data.recommendation;
        recommendationBadge.className = `badge ${getRecommendationClass(data.recommendation)}`;
    }
    
    // Update model accuracy display
    const accuracyElement = document.getElementById('modelAccuracy');
    if (accuracyElement) {
        accuracyElement.textContent = `Model Accuracy: ${data.model_accuracy}%`;
        accuracyElement.className = `small text-muted ${getAccuracyClass(data.model_accuracy)}`;
    }
    
    // Update real-time status
    const statusElement = document.getElementById('dataStatus');
    if (statusElement) {
        const statusText = data.is_real_price ? 'Real-time Data' : 'Last Available Price';
        const statusIcon = data.is_real_price ? 'circle text-success pulse' : 'clock text-warning';
        statusElement.innerHTML = `<i class="fas fa-${statusIcon} me-1"></i>${statusText}`;
    }
    
    // Update enhanced prediction chart
    updateEnhancedPredictionChart(data);
    
    // Show calibrate button
    const calibrateBtn = document.getElementById('calibrateBtn');
    if (calibrateBtn) {
        calibrateBtn.style.display = 'inline-block';
    }
}

function getConfidenceClass(confidence) {
    if (confidence >= 85) return 'bg-success';
    if (confidence >= 70) return 'bg-warning';
    return 'bg-danger';
}

function getRecommendationClass(recommendation) {
    const rec = recommendation.toLowerCase();
    if (rec.includes('strong buy')) return 'bg-success';
    if (rec.includes('buy')) return 'bg-primary';
    if (rec.includes('strong sell')) return 'bg-danger';
    if (rec.includes('sell')) return 'bg-warning';
    return 'bg-secondary';
}

function getAccuracyClass(accuracy) {
    if (accuracy >= 85) return 'text-success';
    if (accuracy >= 70) return 'text-warning';
    return 'text-danger';
}

function updateEnhancedPredictionChart(data) {
    const ctx = document.getElementById('predictionChart');
    if (!ctx) return;
    
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#ffffff' : '#212529';
    const gridColor = isDark ? '#404040' : '#dee2e6';
    
    // Prepare chart data
    const historicalLabels = data.historical_data.map(item => item.date);
    const historicalPrices = data.historical_data.map(item => item.price);
    const predictionLabels = data.prediction_data.map(item => item.date);
    const predictionPrices = data.prediction_data.map(item => item.price);
    const confidenceValues = data.prediction_data.map(item => item.confidence || data.confidence);
    
    // Combine labels
    const allLabels = [...historicalLabels, ...predictionLabels];
    
    // Prepare datasets
    const historicalData = [...historicalPrices, ...new Array(predictionLabels.length).fill(null)];
    const predictionData = [...new Array(historicalLabels.length - 1).fill(null), historicalPrices[historicalPrices.length - 1], ...predictionPrices];
    
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: historicalData,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 2,
                    pointHoverRadius: 4
                },
                {
                    label: 'Predicted Price',
                    data: predictionData,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.1,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#28a745'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: textColor },
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        afterBody: function(context) {
                            const dataIndex = context[0].dataIndex;
                            if (dataIndex >= historicalLabels.length && confidenceValues[dataIndex - historicalLabels.length]) {
                                return `Confidence: ${confidenceValues[dataIndex - historicalLabels.length].toFixed(1)}%`;
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor },
                    title: {
                        display: true,
                        text: 'Date',
                        color: textColor
                    }
                },
                y: {
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    },
                    grid: { color: gridColor },
                    title: {
                        display: true,
                        text: 'Price (₹)',
                        color: textColor
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

// Enhanced Calibration
async function calibrateModel() {
    const stockInput = document.getElementById('stockInput');
    const daysSelect = document.getElementById('daysAhead');
    
    if (!stockInput || !daysSelect) {
        showAdvancedToast('Error', 'Please select a stock first', 'error');
        return;
    }
    
    const symbol = stockInput.value.trim();
    const days = parseInt(daysSelect.value);
    
    if (!symbol) {
        showAdvancedToast('Error', 'Please select a stock first', 'error');
        return;
    }
    
    const calibrateBtn = document.getElementById('calibrateBtn');
    const originalText = calibrateBtn ? calibrateBtn.innerHTML : '';
    
    if (calibrateBtn) {
        calibrateBtn.innerHTML = '<i class="fas fa-cog fa-spin me-2"></i>Calibrating Model...';
        calibrateBtn.disabled = true;
    }
    
    try {
        showAdvancedToast('Calibration Started', 'Running backtests to improve accuracy...', 'info');
        
        const response = await fetch('/api/calibrate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol: symbol, days_ahead: days })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Show detailed calibration results
        showCalibrationResults(data);
        
        // Re-run prediction with calibrated model
        setTimeout(() => {
            handlePredictionSubmit(null, symbol);
        }, 1500);
        
    } catch (error) {
        console.error('Calibration error:', error);
        showAdvancedToast('Calibration Failed', error.message, 'error');
    } finally {
        if (calibrateBtn) {
            calibrateBtn.innerHTML = originalText;
            calibrateBtn.disabled = false;
        }
    }
}

function showCalibrationResults(data) {
    const accuracy = data.accuracy_score;
    const testCount = data.test_count || 0;
    
    let accuracyLevel, accuracyColor;
    if (accuracy >= 85) {
        accuracyLevel = 'Excellent';
        accuracyColor = 'success';
    } else if (accuracy >= 75) {
        accuracyLevel = 'Good';
        accuracyColor = 'primary';
    } else if (accuracy >= 65) {
        accuracyLevel = 'Fair';
        accuracyColor = 'warning';
    } else {
        accuracyLevel = 'Poor';
        accuracyColor = 'danger';
    }
    
    const message = `
        <div class="calibration-result">
            <h6>Calibration Complete!</h6>
            <p><strong>Accuracy:</strong> <span class="badge bg-${accuracyColor}">${accuracy.toFixed(1)}% (${accuracyLevel})</span></p>
            <p><strong>Tests Performed:</strong> ${testCount} backtests</p>
            <p class="small text-muted">${data.message}</p>
        </div>
    `;
    
    showAdvancedToast('Calibration Results', message, accuracyColor, 8000);
}

// Enhanced Technical Analysis
async function updateTechnicalChart(chartType, symbol = null) {
    const stockInput = document.getElementById('stockInput');
    const currentSymbol = symbol || (stockInput ? stockInput.value.trim() : '');
    
    if (!currentSymbol) return;
    
    // Add symbol to real-time tracking
    currentSymbols.add(currentSymbol.toUpperCase());
    
    try {
        const period = document.getElementById('chartPeriodSelect') ? 
            document.getElementById('chartPeriodSelect').value : '3mo';
        
        const response = await fetch(`/api/technical-chart/${currentSymbol}?type=${chartType}&period=${period}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.data) {
            displayEnhancedTechnicalChart(data, chartType);
            displayTechnicalIndicators(data.indicators);
            
            // Show technical charts section
            const chartsSection = document.getElementById('technicalChartsSection');
            if (chartsSection) {
                chartsSection.style.display = 'block';
            }
        } else {
            throw new Error(data.error || 'Failed to load chart data');
        }
        
    } catch (error) {
        console.error('Technical chart error:', error);
        showAdvancedToast('Chart Error', 'Failed to load technical chart', 'error');
    }
}

function displayEnhancedTechnicalChart(data, chartType) {
    const container = document.getElementById('technicalChart');
    if (!container) return;
    
    // Clear existing chart
    container.innerHTML = '<canvas id="technicalChartCanvas"></canvas>';
    
    const ctx = document.getElementById('technicalChartCanvas');
    if (!ctx) return;
    
    if (technicalChart) {
        technicalChart.destroy();
    }
    
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#ffffff' : '#212529';
    const gridColor = isDark ? '#404040' : '#dee2e6';
    
    let chartConfig = {
        type: chartType === 'candlestick' ? 'bar' : 'line',
        data: { labels: [], datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    labels: { color: textColor },
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor },
                    title: { display: true, text: 'Date', color: textColor }
                },
                y: {
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    },
                    grid: { color: gridColor },
                    title: { display: true, text: 'Price (₹)', color: textColor }
                }
            }
        }
    };
    
    if (chartType === 'candlestick' && data.data[0] && data.data[0].open !== undefined) {
        // Professional candlestick chart
        const candlestickData = data.data;
        const labels = candlestickData.map(item => item.date);
        const ohlcData = candlestickData.map(item => ({
            x: item.date,
            o: item.open,
            h: item.high,
            l: item.low,
            c: item.close
        }));
        
        chartConfig.type = 'candlestick';
        chartConfig.data = {
            datasets: [{
                label: `${data.symbol} Candlestick`,
                data: ohlcData,
                backgroundColors: candlestickData.map(item => item.color || (item.close >= item.open ? '#00ff88' : '#ff4444')),
                borderColors: candlestickData.map(item => item.close >= item.open ? '#00bb44' : '#bb0000'),
                borderWidth: 1
            }]
        };
    } else {
        // Line chart for other types
        chartConfig.data = {
            labels: data.data.map(item => item.date),
            datasets: [{
                label: `${data.symbol} - ${chartType.charAt(0).toUpperCase() + chartType.slice(1)}`,
                data: data.data.map(item => item.price || item.close || 0),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: false,
                tension: 0.1,
                pointRadius: 1,
                pointHoverRadius: 4
            }]
        };
    }
    
    // Add volume dataset if available
    if (data.data[0] && data.data[0].volume !== undefined) {
        chartConfig.data.datasets.push({
            label: 'Volume',
            data: data.data.map(item => item.volume),
            type: 'bar',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            yAxisID: 'y1'
        });
        
        // Add second y-axis for volume
        chartConfig.options.scales.y1 = {
            type: 'linear',
            display: true,
            position: 'right',
            ticks: { color: textColor },
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Volume', color: textColor }
        };
    }
    
    technicalChart = new Chart(ctx, chartConfig);
    
    // Update chart type indicator
    const indicator = document.getElementById('chartTypeIndicator');
    if (indicator) {
        indicator.textContent = chartType.charAt(0).toUpperCase() + chartType.slice(1);
    }
}

function displayTechnicalIndicators(indicators) {
    const container = document.getElementById('technicalIndicators');
    if (!container) return;
    
    const indicatorsList = [
        { key: 'rsi', label: 'RSI (14)', format: 'number', range: [30, 70] },
        { key: 'macd', label: 'MACD', format: 'number', range: null },
        { key: 'sma_20', label: 'SMA (20)', format: 'currency', range: null },
        { key: 'sma_50', label: 'SMA (50)', format: 'currency', range: null },
        { key: 'bb_upper', label: 'BB Upper', format: 'currency', range: null },
        { key: 'bb_lower', label: 'BB Lower', format: 'currency', range: null }
    ];
    
    container.innerHTML = indicatorsList.map(indicator => {
        const value = indicators[indicator.key];
        let displayValue = 'N/A';
        let statusClass = '';
        let statusText = '';
        
        if (value !== null && value !== undefined) {
            if (indicator.format === 'currency') {
                displayValue = `₹${parseFloat(value).toLocaleString()}`;
            } else {
                displayValue = parseFloat(value).toFixed(2);
            }
            
            // Add status indication for RSI
            if (indicator.key === 'rsi') {
                if (value > 70) {
                    statusClass = 'text-danger';
                    statusText = 'Overbought';
                } else if (value < 30) {
                    statusClass = 'text-success';
                    statusText = 'Oversold';
                } else {
                    statusClass = 'text-warning';
                    statusText = 'Neutral';
                }
            }
        }
        
        return `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="indicator-label">
                    ${indicator.label}
                    <i class="fas fa-info-circle text-muted ms-1" 
                       title="Technical indicator value"></i>
                </span>
                <div class="text-end">
                    <strong class="${statusClass}">${displayValue}</strong>
                    ${statusText ? `<br><small class="${statusClass}">${statusText}</small>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Enhanced Toast System
function showAdvancedToast(title, message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle',
        primary: 'info-circle'
    };
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-${iconMap[type] || 'info-circle'} me-2"></i>
                        <div>
                            <strong>${title}</strong>
                            <div class="toast-message">${message}</div>
                        </div>
                    </div>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElement, { delay: duration });
    
    bsToast.show();
    
    // Auto-remove from DOM after hiding
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Utility Functions
function addSymbolToTracking(symbol) {
    currentSymbols.add(symbol.toUpperCase());
}

function removeSymbolFromTracking(symbol) {
    currentSymbols.delete(symbol.toUpperCase());
}

function formatCurrency(amount, currency = '₹') {
    return `${currency}${parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
}

function formatPercentage(value) {
    return `${value >= 0 ? '+' : ''}${parseFloat(value).toFixed(2)}%`;
}

// Event Listeners Setup
function setupEventListeners() {
    // Prediction form
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }
    
    // Chart controls
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', function() {
            updateTechnicalChart(this.value);
        });
    }
    
    // Period controls
    const chartPeriodSelect = document.getElementById('chartPeriodSelect');
    if (chartPeriodSelect) {
        chartPeriodSelect.addEventListener('change', function() {
            const currentChartType = document.getElementById('chartTypeSelect')?.value || 'candlestick';
            updateTechnicalChart(currentChartType);
        });
    }
    
    // Portfolio refresh
    const refreshBtn = document.getElementById('refreshPortfolio');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            updatePortfolioValues();
            showAdvancedToast('Portfolio Updated', 'Latest prices loaded', 'success');
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    
    // Add CSS for real-time indicators
    const style = document.createElement('style');
    style.textContent = `
        .realtime-indicator {
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            z-index: 1000;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .price-updated {
            animation: priceFlash 1s ease-in-out;
        }
        
        @keyframes priceFlash {
            0% { background-color: rgba(40, 167, 69, 0.3); }
            100% { background-color: transparent; }
        }
        
        .real-price {
            color: #28a745 !important;
        }
        
        .cached-price {
            color: #ffc107 !important;
        }
        
        .market-index {
            transition: all 0.3s ease;
        }
        
        .market-index:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .toast-message {
            font-size: 0.9rem;
            margin-top: 2px;
        }
        
        .calibration-result {
            text-align: left;
        }
        
        .indicator-label {
            font-weight: 500;
        }
    `;
    document.head.appendChild(style);
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (realtimeInterval) {
        clearInterval(realtimeInterval);
    }
});

// Export functions for global access
window.initializeApp = initializeApp;
window.toggleTheme = toggleTheme;
window.handlePredictionSubmit = handlePredictionSubmit;
window.calibrateModel = calibrateModel;
window.updateTechnicalChart = updateTechnicalChart;
window.showAdvancedToast = showAdvancedToast;
window.addSymbolToTracking = addSymbolToTracking;
window.removeSymbolFromTracking = removeSymbolFromTracking;