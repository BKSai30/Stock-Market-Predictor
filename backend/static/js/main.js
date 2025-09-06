// Main JavaScript file for Stock Market Predictor
// Global variables
let predictionChart = null;
let technicalChart = null;
let heroChart = null;

// Initialize the application
function initializeApp() {
    initializeTheme();
    initializeHeroChart();
    loadMarketIndices();
    loadTopStocks('safe', 5);
    setupEventListeners();
    checkPredictStock();
}

// Theme Management
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
    
    // Update charts if they exist
    updateChartsForTheme();
}

// Setup Event Listeners
function setupEventListeners() {
    // Prediction form
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }
    
    // Search stock button
    const searchStockBtn = document.getElementById('searchStockBtn');
    if (searchStockBtn) {
        searchStockBtn.addEventListener('click', searchStock);
    }
    
    // Quick stock buttons
    document.querySelectorAll('.quick-stock-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectQuickStock(this.dataset.symbol);
        });
    });
    
    // Volatility buttons
    document.querySelectorAll('.volatility-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectVolatilityCategory(this.dataset.category);
        });
    });
    
    // Chart type selector
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', function() {
            updateTechnicalChart(this.value);
        });
    }
    
    // Calibrate button
    const calibrateBtn = document.getElementById('calibrateBtn');
    if (calibrateBtn) {
        calibrateBtn.addEventListener('click', calibrateModel);
    }
}

// Check if there's a stock to predict from localStorage
function checkPredictStock() {
    const stockToPredict = localStorage.getItem('predictStock');
    if (stockToPredict) {
        document.getElementById('stockInput').value = stockToPredict;
        localStorage.removeItem('predictStock');
        // Auto-submit prediction form
        setTimeout(() => {
            handlePredictionSubmit(null, stockToPredict);
        }, 500);
    }
}

// Market Indices
async function loadMarketIndices() {
    const indices = [
        { name: 'Nifty 50', value: '19,674.35', change: '+0.64%', positive: true },
        { name: 'Sensex', value: '65,835.64', change: '+0.60%', positive: true },
        { name: 'Bank Nifty', value: '44,239.80', change: '-0.32%', positive: false },
        { name: 'IT Index', value: '31,847.25', change: '+2.11%', positive: true }
    ];
    
    const container = document.getElementById('marketIndices');
    if (container) {
        container.innerHTML = indices.map(index => `
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <h5 class="mb-1">${index.value}</h5>
                    <div class="small text-muted">${index.name}</div>
                    <div class="small ${index.positive ? 'text-success' : 'text-danger'}">
                        <i class="fas fa-arrow-${index.positive ? 'up' : 'down'} me-1"></i>
                        ${index.change}
                    </div>
                </div>
            </div>
        `).join('');
    }
}

// Hero Chart
function initializeHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;
    
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    
    heroChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => {
                const date = new Date();
                date.setDate(date.getDate() - 29 + i);
                return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Market Trend',
                data: generateSampleData(30, 19000, 20000),
                borderColor: 'rgba(255, 255, 255, 0.8)',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        }
    });
}

// Stock Prediction Functions
async function handlePredictionSubmit(event, stockSymbol = null) {
    if (event) event.preventDefault();
    
    const symbol = stockSymbol || document.getElementById('stockInput').value.trim();
    const days = document.getElementById('predictionDays').value;
    
    if (!symbol) {
        showToast('Error', 'Please enter a stock symbol', 'error');
        return;
    }
    
    showPredictionLoading(true);
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol: symbol, days_ahead: parseInt(days) })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayPredictionResults(data);
            updateTechnicalChart('candlestick', data.symbol);
        } else {
            throw new Error(data.error || 'Prediction failed');
        }
        
    } catch (error) {
        console.error('Prediction error:', error);
        showToast('Error', error.message, 'error');
        showPredictionInitial();
    } finally {
        showPredictionLoading(false);
    }
}

function showPredictionLoading(show) {
    const elements = {
        loading: document.getElementById('predictionLoading'),
        initial: document.getElementById('predictionInitial'),
        results: document.getElementById('predictionResults')
    };
    
    if (show) {
        elements.loading.style.display = 'block';
        elements.initial.style.display = 'none';
        elements.results.classList.add('d-none');
    } else {
        elements.loading.style.display = 'none';
    }
}

function showPredictionInitial() {
    const elements = {
        loading: document.getElementById('predictionLoading'),
        initial: document.getElementById('predictionInitial'),
        results: document.getElementById('predictionResults')
    };
    
    elements.loading.style.display = 'none';
    elements.initial.style.display = 'block';
    elements.results.classList.add('d-none');
}

function displayPredictionResults(data) {
    // Hide loading and initial states
    document.getElementById('predictionLoading').style.display = 'none';
    document.getElementById('predictionInitial').style.display = 'none';
    document.getElementById('predictionResults').classList.remove('d-none');
    
    // Update basic info
    document.getElementById('stockName').textContent = `${data.symbol} - ${data.name}`;
    document.getElementById('currentPrice').textContent = `₹${data.current_price}`;
    document.getElementById('predictedPrice').textContent = `₹${data.predicted_price}`;
    document.getElementById('predictionPeriodLabel').textContent = `(${data.days_ahead}-day)`;
    
    // Update price change
    const priceChange = data.predicted_price - data.current_price;
    const priceChangeElement = document.getElementById('priceChange');
    const changeClass = priceChange >= 0 ? 'profit' : 'loss';
    const changeIcon = priceChange >= 0 ? 'up' : 'down';
    
    priceChangeElement.textContent = `${priceChange >= 0 ? '+' : ''}₹${Math.abs(priceChange).toFixed(2)} (${data.price_change_pct >= 0 ? '+' : ''}${data.price_change_pct}%)`;
    priceChangeElement.className = `price-change ${changeClass}`;
    
    // Update confidence
    const confidenceBar = document.getElementById('confidenceBar');
    confidenceBar.style.width = `${data.confidence}%`;
    confidenceBar.textContent = `${data.confidence}%`;
    
    // Update recommendation badge
    const recommendationBadge = document.getElementById('recommendationBadge');
    recommendationBadge.textContent = data.recommendation;
    recommendationBadge.className = `badge ${getRecommendationClass(data.recommendation)}`;
    
    // Show calibrate button
    document.getElementById('calibrateBtn').style.display = 'inline-block';
    
    // Update prediction chart
    updatePredictionChart(data);
    
    // Update enhanced recommendation
    updateEnhancedRecommendation(data.enhanced_recommendation);
    
    // Update AI analysis
    updateAIAnalysis(data.ai_analysis);
    
    // Update sentiment analysis
    updateSentimentAnalysis(data.sentiment_analysis);
}

function updatePredictionChart(data) {
    const ctx = document.getElementById('predictionChart');
    if (!ctx) return;
    
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#ffffff' : '#212529';
    const gridColor = isDark ? '#404040' : '#dee2e6';
    
    // Combine historical and prediction data
    const allData = [...data.historical_data, ...data.prediction_data.slice(1)];
    const labels = allData.map(item => item.date);
    const prices = allData.map(item => item.price);
    
    // Split data for different styling
    const historicalPrices = data.historical_data.map(item => item.price);
    const predictionPrices = new Array(historicalPrices.length - 1).fill(null);
    predictionPrices.push(data.current_price);
    predictionPrices.push(...data.prediction_data.slice(1).map(item => item.price));
    
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: [...historicalPrices, ...new Array(data.prediction_data.length - 1).fill(null)],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Predicted Price',
                    data: predictionPrices,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return '₹' + value.toFixed(2);
                        }
                    },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

// Technical Analysis Functions
async function updateTechnicalChart(chartType, symbol = null) {
    const stockInput = document.getElementById('stockInput');
    const currentSymbol = symbol || stockInput?.value.trim();
    
    if (!currentSymbol) return;
    
    try {
        const response = await fetch(`/api/technical-chart/${currentSymbol}?type=${chartType}`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayTechnicalChart(data, chartType);
            displayChartPatterns(data.patterns);
            displayTechnicalIndicators(data.indicators);
        } else {
            console.error('Failed to load technical chart:', data.error);
        }
        
    } catch (error) {
        console.error('Technical chart error:', error);
    }
}

function displayTechnicalChart(data, chartType) {
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
    
    // Configure chart based on type
    let chartConfig = {
        type: 'line',
        data: { labels: [], datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: textColor } }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return '₹' + value.toFixed(2);
                        }
                    },
                    grid: { color: gridColor }
                }
            }
        }
    };
    
    if (chartType === 'candlestick') {
        // For candlestick, we'll use a line chart as approximation
        chartConfig.data = {
            labels: data.data.map(item => item.date),
            datasets: [{
                label: `${data.symbol} Price`,
                data: data.data.map(item => item.close),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: false,
                tension: 0.1
            }]
        };
    } else {
        // Handle other chart types similarly
        chartConfig.data = {
            labels: data.data.map(item => item.date || new Date().toISOString().split('T')[0]),
            datasets: [{
                label: `${data.symbol} - ${chartType.charAt(0).toUpperCase() + chartType.slice(1)}`,
                data: data.data.map(item => item.price || item.close || 0),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: false,
                tension: 0.1
            }]
        };
    }
    
    technicalChart = new Chart(ctx, chartConfig);
    
    // Show chart pattern analysis
    document.getElementById('chartPatternAnalysis').style.display = 'block';
}

function displayChartPatterns(patterns) {
    const container = document.getElementById('candlestickPatterns');
    if (!container) return;
    
    if (patterns && patterns.detected_patterns && patterns.detected_patterns.length > 0) {
        container.innerHTML = patterns.detected_patterns.map(pattern => 
            `<div class="mb-2">
                <span class="badge bg-primary">${pattern}</span>
            </div>`
        ).join('');
    } else {
        container.innerHTML = '<small class="text-muted">No significant patterns detected</small>';
    }
}

function displayTechnicalIndicators(indicators) {
    const container = document.getElementById('technicalIndicators');
    if (!container) return;
    
    const indicatorsList = [
        { key: 'rsi', label: 'RSI (14)', tooltip: 'Relative Strength Index - measures overbought/oversold conditions. Values above 70 suggest overbought, below 30 suggest oversold.' },
        { key: 'macd', label: 'MACD', tooltip: 'Moving Average Convergence Divergence - trend-following momentum indicator. Positive values suggest bullish momentum.' },
        { key: 'sma_20', label: 'SMA (20)', tooltip: 'Simple Moving Average (20 days) - average price over last 20 days. Price above SMA suggests uptrend.' },
        { key: 'bb_upper', label: 'BB Upper', tooltip: 'Bollinger Bands Upper - price touching upper band may indicate overbought condition.' },
        { key: 'bb_lower', label: 'BB Lower', tooltip: 'Bollinger Bands Lower - price touching lower band may indicate oversold condition.' }
    ];
    
    container.innerHTML = indicatorsList.map(indicator => {
        const value = indicators[indicator.key];
        const displayValue = value !== null && value !== undefined ? 
            (typeof value === 'number' ? value.toFixed(2) : value) : 'N/A';
        
        return `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span>${indicator.label}
                    <i class="fas fa-info-circle info-tooltip ms-1">
                        <div class="tooltip-content">${indicator.tooltip}</div>
                    </i>
                </span>
                <strong>${displayValue}</strong>
            </div>
        `;
    }).join('');
}

// Top Stocks Functions
async function loadTopStocks(category = 'safe', count = 5) {
    try {
        const response = await fetch(`/api/top-stocks?category=${category}&count=${count}`);
        const data = await response.json();
        
        if (response.ok) {
            displayTopStocks(data.stocks);
        } else {
            throw new Error(data.error || 'Failed to load top stocks');
        }
        
    } catch (error) {
        console.error('Top stocks error:', error);
        showToast('Error', 'Failed to load top stocks', 'error');
    }
}

function displayTopStocks(stocks) {
    const container = document.getElementById('topStocksList');
    if (!container) return;
    
    container.innerHTML = stocks.map(stock => {
        const changeClass = stock.price_change >= 0 ? 'text-success' : 'text-danger';
        const changeIcon = stock.price_change >= 0 ? 'up' : 'down';
        
        return `
            <div class="d-flex justify-content-between align-items-center mb-3 p-2 rounded" 
                 style="background: var(--bg-secondary); cursor: pointer;"
                 onclick="selectStock('${stock.symbol}')">
                <div>
                    <strong>${stock.symbol}</strong>
                    <div class="small text-muted">${stock.name}</div>
                    <div class="small text-muted">${stock.sector}</div>
                </div>
                <div class="text-end">
                    <div>₹${stock.current_price}</div>
                    <div class="small ${changeClass}">
                        <i class="fas fa-arrow-${changeIcon}"></i>
                        ${stock.price_change >= 0 ? '+' : ''}${stock.price_change.toFixed(2)}%
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function selectStock(symbol) {
    document.getElementById('stockInput').value = symbol;
    handlePredictionSubmit(null, symbol);
}

// Helper Functions
function selectQuickStock(symbol) {
    // Update active state
    document.querySelectorAll('.quick-stock-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Set input and predict
    document.getElementById('stockInput').value = symbol;
    handlePredictionSubmit(null, symbol);
}

function selectVolatilityCategory(category) {
    // Update active state
    document.querySelectorAll('.volatility-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load stocks for category
    const count = document.getElementById('stockCount')?.value || 5;
    loadTopStocks(category, count);
}

async function searchStock() {
    const symbol = document.getElementById('stockInput').value.trim();
    if (!symbol) return;
    
    try {
        const response = await fetch('/api/search-stock', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: symbol })
        });
        
        const data = await response.json();
        
        if (data.found) {
            showToast('Success', `Found: ${data.name} (${data.symbol})`, 'success');
            document.getElementById('stockInput').value = data.symbol;
        } else {
            showToast('Info', data.message, 'info');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        showToast('Error', 'Search failed', 'error');
    }
}

async function calibrateModel() {
    const stockInput = document.getElementById('stockInput');
    const daysSelect = document.getElementById('predictionDays');
    
    const symbol = stockInput.value.trim();
    const days = parseInt(daysSelect.value);
    
    if (!symbol) {
        showToast('Error', 'Please select a stock first', 'error');
        return;
    }
    
    const calibrateBtn = document.getElementById('calibrateBtn');
    const originalText = calibrateBtn.innerHTML;
    
    calibrateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Calibrating...';
    calibrateBtn.disabled = true;
    
    try {
        const response = await fetch('/api/calibrate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol: symbol, days_ahead: days })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Success', `Calibration completed! Accuracy: ${data.accuracy_score.toFixed(2)}%`, 'success');
            
            // Re-run prediction with calibrated model
            setTimeout(() => {
                handlePredictionSubmit(null, symbol);
            }, 1000);
        } else {
            throw new Error(data.error || 'Calibration failed');
        }
        
    } catch (error) {
        console.error('Calibration error:', error);
        showToast('Error', error.message, 'error');
    } finally {
        calibrateBtn.innerHTML = originalText;
        calibrateBtn.disabled = false;
    }
}

// UI Helper Functions
function updateEnhancedRecommendation(recommendation) {
    const container = document.getElementById('enhancedRecommendation');
    if (!container || !recommendation) return;
    
    container.innerHTML = `
        <div class="mb-3">
            <span class="badge ${getRecommendationClass(recommendation.action)} mb-2">
                ${recommendation.action}
            </span>
            <div class="small"><strong>Strength:</strong> ${recommendation.strength}</div>
        </div>
        <div class="mb-3">
            <strong>Analysis:</strong>
            <ul class="mt-2 mb-0">
                ${recommendation.reasoning.map(reason => `<li><small>${reason}</small></li>`).join('')}
            </ul>
        </div>
        ${recommendation.risk_level ? `
            <div class="small">
                <strong>Risk Level:</strong> 
                <span class="badge bg-${getRiskLevelClass(recommendation.risk_level)}">${recommendation.risk_level}</span>
            </div>
        ` : ''}
    `;
}

function updateAIAnalysis(analysis) {
    const container = document.getElementById('aiAnalysis');
    if (!container || !analysis) return;
    
    container.innerHTML = `
        <div class="row mb-3">
            <div class="col-6">
                <strong>Trend:</strong> ${analysis.trend}
            </div>
            <div class="col-6">
                <strong>Strength:</strong> ${analysis.strength}
            </div>
        </div>
        <div class="mb-3">
            <strong>Key Factors:</strong>
            <ul class="mt-2 mb-3">
                ${analysis.key_factors.map(factor => `<li><small>${factor}</small></li>`).join('')}
            </ul>
        </div>
        <div class="row small">
            <div class="col-6">
                <strong>Model:</strong> ${analysis.model_used}
            </div>
            <div class="col-6">
                <strong>Data Quality:</strong> ${analysis.data_quality}
            </div>
        </div>
    `;
}

function updateSentimentAnalysis(sentiment) {
    const container = document.getElementById('sentimentAnalysis');
    if (!container || !sentiment) return;
    
    const sentimentClass = sentiment.overall_sentiment.toLowerCase() === 'positive' ? 'text-success' :
                          sentiment.overall_sentiment.toLowerCase() === 'negative' ? 'text-danger' : 'text-warning';
    
    container.innerHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="text-center">
                    <div class="h4 ${sentimentClass}">${sentiment.overall_sentiment}</div>
                    <div class="small">Overall Sentiment</div>
                    <div class="small text-muted">Score: ${sentiment.sentiment_score}</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="small mb-2">
                    <strong>News:</strong> ${sentiment.news_sentiment}<br>
                    <strong>Social:</strong> ${sentiment.social_sentiment}
                </div>
            </div>
        </div>
        <div class="mb-3">
            <strong>Key Themes:</strong>
            <div class="mt-2">
                ${sentiment.key_themes.map(theme => 
                    `<span class="badge bg-secondary me-1 mb-1">${theme}</span>`
                ).join('')}
            </div>
        </div>
        <div class="small text-muted">
            <strong>Sources:</strong> ${sentiment.sentiment_sources.join(', ')}
        </div>
    `;
}

function getRecommendationClass(recommendation) {
    const rec = recommendation.toLowerCase();
    if (rec.includes('buy')) return 'bg-success';
    if (rec.includes('sell')) return 'bg-danger';
    if (rec.includes('hold')) return 'bg-warning';
    return 'bg-secondary';
}

function getRiskLevelClass(riskLevel) {
    const risk = riskLevel.toLowerCase();
    if (risk === 'high') return 'danger';
    if (risk === 'medium') return 'warning';
    if (risk === 'low') return 'success';
    return 'secondary';
}

function generateSampleData(count, min, max) {
    const data = [];
    let current = (min + max) / 2;
    
    for (let i = 0; i < count; i++) {
        const change = (Math.random() - 0.5) * (max - min) * 0.1;
        current = Math.max(min, Math.min(max, current + change));
        data.push(Math.round(current));
    }
    
    return data;
}

function showToast(title, message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    
    if (!toast) return;
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Reset classes
    toast.className = 'toast';
    
    // Add type-specific classes
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'error') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning', 'text-dark');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function updateChartsForTheme() {
    // Update existing charts for theme change
    if (predictionChart) {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#ffffff' : '#212529';
        const gridColor = isDark ? '#404040' : '#dee2e6';
        
        predictionChart.options.plugins.legend.labels.color = textColor;
        predictionChart.options.scales.x.ticks.color = textColor;
        predictionChart.options.scales.x.grid.color = gridColor;
        predictionChart.options.scales.y.ticks.color = textColor;
        predictionChart.options.scales.y.grid.color = gridColor;
        predictionChart.update();
    }
    
    if (technicalChart) {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#ffffff' : '#212529';
        const gridColor = isDark ? '#404040' : '#dee2e6';
        
        technicalChart.options.plugins.legend.labels.color = textColor;
        technicalChart.options.scales.x.ticks.color = textColor;
        technicalChart.options.scales.x.grid.color = gridColor;
        technicalChart.options.scales.y.ticks.color = textColor;
        technicalChart.options.scales.y.grid.color = gridColor;
        technicalChart.update();
    }
    
    if (heroChart) {
        heroChart.update();
    }
}

// Export functions for global access
window.initializeApp = initializeApp;
window.toggleTheme = toggleTheme;
window.handlePredictionSubmit = handlePredictionSubmit;
window.loadTopStocks = loadTopStocks;
window.selectStock = selectStock;
window.calibrateModel = calibrateModel;
window.showToast = showToast;
