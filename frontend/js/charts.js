/**
 * Charts Module for Stock Market Predictor
 * Handles chart creation, updates, and interactions using Chart.js and Plotly
 */

// Chart configuration and themes
const CHART_CONFIG = {
    colors: {
        primary: '#2563eb',
        success: '#22c55e',
        danger: '#ef4444',
        warning: '#f59e0b',
        info: '#06b6d4',
        light: '#f8fafc',
        dark: '#1f2937'
    },
    fonts: {
        family: "'Roboto', sans-serif",
        size: 12,
        weight: 'normal'
    },
    animations: {
        duration: 750,
        easing: 'easeInOutQuart'
    }
};

// Chart.js default configuration
Chart.defaults.font.family = CHART_CONFIG.fonts.family;
Chart.defaults.font.size = CHART_CONFIG.fonts.size;
Chart.defaults.animation.duration = CHART_CONFIG.animations.duration;
Chart.defaults.animation.easing = CHART_CONFIG.animations.easing;

/**
 * Stock Price Chart Class
 */
class StockPriceChart {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.chart = null;
        this.options = {
            responsive: true,
            maintainAspectRatio: false,
            ...options
        };
    }
    
    /**
     * Create a line chart for stock prices
     * @param {Object} data - Chart data
     * @param {Object} config - Chart configuration
     */
    createLineChart(data, config = {}) {
        this.destroyExisting();
        
        const chartConfig = {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: data.datasets || []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    title: {
                        display: !!config.title,
                        text: config.title,
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
                        cornerRadius: 6,
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += '₹' + context.parsed.y.toFixed(2);
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: config.xAxisLabel || 'Date'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: config.yAxisLabel || 'Price (₹)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                ...config.options
            }
        };
        
        this.chart = new Chart(this.ctx, chartConfig);
        return this.chart;
    }
    
    /**
     * Create a candlestick chart
     * @param {Object} data - OHLC data
     * @param {Object} config - Chart configuration
     */
    createCandlestickChart(data, config = {}) {
        // For candlestick charts, we'll use Plotly since Chart.js doesn't have native support
        const plotlyData = [{
            x: data.map(d => d.date),
            open: data.map(d => d.open),
            high: data.map(d => d.high),
            low: data.map(d => d.low),
            close: data.map(d => d.close),
            type: 'candlestick',
            name: 'OHLC',
            increasing: {
                line: { color: CHART_CONFIG.colors.success }
            },
            decreasing: {
                line: { color: CHART_CONFIG.colors.danger }
            }
        }];
        
        const layout = {
            title: config.title || 'Candlestick Chart',
            xaxis: {
                title: 'Date',
                rangeslider: { visible: false }
            },
            yaxis: {
                title: 'Price (₹)'
            },
            font: {
                family: CHART_CONFIG.fonts.family,
                size: CHART_CONFIG.fonts.size
            },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            ...config.layout
        };
        
        const plotConfig = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['lasso2d', 'select2d'],
            ...config.plotConfig
        };
        
        Plotly.newPlot(this.canvas, plotlyData, layout, plotConfig);
    }
    
    /**
     * Update chart data
     * @param {Object} newData - New chart data
     */
    updateData(newData) {
        if (!this.chart) return;
        
        this.chart.data.labels = newData.labels || this.chart.data.labels;
        
        if (newData.datasets) {
            newData.datasets.forEach((dataset, index) => {
                if (this.chart.data.datasets[index]) {
                    Object.assign(this.chart.data.datasets[index], dataset);
                } else {
                    this.chart.data.datasets.push(dataset);
                }
            });
        }
        
        this.chart.update('active');
    }
    
    /**
     * Add real-time data point
     * @param {Object} dataPoint - New data point
     */
    addDataPoint(dataPoint) {
        if (!this.chart) return;
        
        this.chart.data.labels.push(dataPoint.label);
        
        this.chart.data.datasets.forEach((dataset, index) => {
            if (dataPoint.values && dataPoint.values[index] !== undefined) {
                dataset.data.push(dataPoint.values[index]);
            }
        });
        
        // Keep only last 100 points for performance
        if (this.chart.data.labels.length > 100) {
            this.chart.data.labels.shift();
            this.chart.data.datasets.forEach(dataset => {
                dataset.data.shift();
            });
        }
        
        this.chart.update('none');
    }
    
    /**
     * Destroy existing chart
     */
    destroyExisting() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
    
    /**
     * Export chart as image
     * @param {string} format - Image format ('png', 'jpeg')
     * @returns {string} Base64 image data
     */
    exportAsImage(format = 'png') {
        if (!this.chart) return null;
        return this.chart.toBase64Image(`image/${format}`, 1.0);
    }
}

/**
 * Technical Indicators Chart Class
 */
class TechnicalIndicatorsChart {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.charts = new Map();
    }
    
    /**
     * Create RSI chart
     * @param {Array} data - RSI data
     * @param {Object} config - Chart configuration
     */
    createRSIChart(data, config = {}) {
        const canvas = this.createCanvas('rsi-chart');
        const ctx = canvas.getContext('2d');
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.date),
                datasets: [{
                    label: 'RSI',
                    data: data.map(d => d.rsi),
                    borderColor: CHART_CONFIG.colors.primary,
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'RSI (Relative Strength Index)'
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 2
                    }
                }
            }
        });
        
        this.charts.set('rsi', chart);
        return chart;
    }
    
    /**
     * Create MACD chart
     * @param {Array} data - MACD data
     * @param {Object} config - Chart configuration
     */
    createMACDChart(data, config = {}) {
        const canvas = this.createCanvas('macd-chart');
        const ctx = canvas.getContext('2d');
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.date),
                datasets: [
                    {
                        label: 'MACD',
                        data: data.map(d => d.macd),
                        borderColor: CHART_CONFIG.colors.primary,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        type: 'line'
                    },
                    {
                        label: 'Signal',
                        data: data.map(d => d.signal),
                        borderColor: CHART_CONFIG.colors.danger,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        type: 'line'
                    },
                    {
                        label: 'Histogram',
                        data: data.map(d => d.histogram),
                        backgroundColor: data.map(d => d.histogram >= 0 ? CHART_CONFIG.colors.success : CHART_CONFIG.colors.danger),
                        borderWidth: 0,
                        type: 'bar'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'MACD (Moving Average Convergence Divergence)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        this.charts.set('macd', chart);
        return chart;
    }
    
    /**
     * Create Bollinger Bands chart
     * @param {Array} priceData - Price data
     * @param {Array} bollingerData - Bollinger bands data
     */
    createBollingerBandsChart(priceData, bollingerData) {
        const canvas = this.createCanvas('bollinger-chart');
        const ctx = canvas.getContext('2d');
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: priceData.map(d => d.date),
                datasets: [
                    {
                        label: 'Upper Band',
                        data: bollingerData.map(d => d.upper),
                        borderColor: CHART_CONFIG.colors.warning,
                        backgroundColor: 'transparent',
                        borderWidth: 1,
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Middle Band (SMA)',
                        data: bollingerData.map(d => d.middle),
                        borderColor: CHART_CONFIG.colors.primary,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Lower Band',
                        data: bollingerData.map(d => d.lower),
                        borderColor: CHART_CONFIG.colors.warning,
                        backgroundColor: 'transparent',
                        borderWidth: 1,
                        borderDash: [5, 5],
                        fill: '-2'
                    },
                    {
                        label: 'Price',
                        data: priceData.map(d => d.close),
                        borderColor: CHART_CONFIG.colors.dark,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Bollinger Bands'
                    },
                    filler: {
                        propagate: false
                    }
                },
                interaction: {
                    intersect: false
                }
            }
        });
        
        this.charts.set('bollinger', chart);
        return chart;
    }
    
    /**
     * Create canvas element
     * @param {string} id - Canvas ID
     * @returns {HTMLCanvasElement} Canvas element
     */
    createCanvas(id) {
        const canvas = document.createElement('canvas');
        canvas.id = id;
        canvas.style.marginBottom = '20px';
        this.container.appendChild(canvas);
        return canvas;
    }
    
    /**
     * Clear all charts
     */
    clearAll() {
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
        this.container.innerHTML = '';
    }
}

/**
 * Volume Chart Class
 */
class VolumeChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.chart = null;
    }
    
    /**
     * Create volume chart
     * @param {Array} data - Volume data
     * @param {Array} priceData - Price data for color coding
     */
    create(data, priceData = []) {
        this.destroyExisting();
        
        // Color bars based on price movement
        const backgroundColors = data.map((volume, index) => {
            if (priceData[index] && priceData[index - 1]) {
                return priceData[index].close >= priceData[index - 1].close
                    ? CHART_CONFIG.colors.success
                    : CHART_CONFIG.colors.danger;
            }
            return CHART_CONFIG.colors.info;
        });
        
        this.chart = new Chart(this.ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.date),
                datasets: [{
                    label: 'Volume',
                    data: data.map(d => d.volume),
                    backgroundColor: backgroundColors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Trading Volume'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return (value / 1000000).toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
        
        return this.chart;
    }
    
    destroyExisting() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}

/**
 * Alternative Chart Types (Renko, Kagi, Point & Figure)
 */
class AlternativeCharts {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }
    
    /**
     * Create Renko chart using Plotly
     * @param {Array} data - Renko brick data
     * @param {Object} config - Chart configuration
     */
    createRenkoChart(data, config = {}) {
        const traces = [];
        
        data.forEach((brick, index) => {
            const color = brick.type === 'up' ? CHART_CONFIG.colors.success : CHART_CONFIG.colors.danger;
            
            traces.push({
                x: [index, index + 1, index + 1, index, index],
                y: [brick.open, brick.open, brick.close, brick.close, brick.open],
                fill: 'toself',
                fillcolor: color,
                line: { color: color, width: 1 },
                mode: 'lines',
                showlegend: false,
                hoverinfo: 'text',
                text: `Open: ₹${brick.open}<br>Close: ₹${brick.close}<br>Type: ${brick.type}`
            });
        });
        
        const layout = {
            title: config.title || 'Renko Chart',
            xaxis: { title: 'Brick Number' },
            yaxis: { title: 'Price (₹)' },
            showlegend: false,
            hovermode: 'closest'
        };
        
        Plotly.newPlot(this.container, traces, layout, { responsive: true });
    }
    
    /**
     * Create Kagi chart using Plotly
     * @param {Array} data - Kagi line data
     * @param {Object} config - Chart configuration
     */
    createKagiChart(data, config = {}) {
        const yangPoints = data.filter(d => d.type === 'yang');
        const yinPoints = data.filter(d => d.type === 'yin');
        
        const traces = [
            {
                x: yangPoints.map(d => d.x),
                y: yangPoints.map(d => d.y),
                mode: 'lines',
                line: { color: CHART_CONFIG.colors.success, width: 4 },
                name: 'Yang (Thick)',
                connectgaps: false
            },
            {
                x: yinPoints.map(d => d.x),
                y: yinPoints.map(d => d.y),
                mode: 'lines',
                line: { color: CHART_CONFIG.colors.danger, width: 2 },
                name: 'Yin (Thin)',
                connectgaps: false
            }
        ];
        
        const layout = {
            title: config.title || 'Kagi Chart',
            xaxis: { title: 'Time' },
            yaxis: { title: 'Price (₹)' },
            hovermode: 'closest'
        };
        
        Plotly.newPlot(this.container, traces, layout, { responsive: true });
    }
    
    /**
     * Create Point & Figure chart using Plotly
     * @param {Array} data - Point & Figure data
     * @param {Object} config - Chart configuration
     */
    createPointFigureChart(data, config = {}) {
        const xData = data.filter(d => d.symbol === 'X');
        const oData = data.filter(d => d.symbol === 'O');
        
        const traces = [
            {
                x: xData.map(d => d.column),
                y: xData.map(d => d.box),
                mode: 'markers',
                marker: {
                    symbol: 'x',
                    size: 15,
                    color: CHART_CONFIG.colors.success,
                    line: { width: 2 }
                },
                name: 'X (Up)',
                text: xData.map(d => `₹${d.price}`),
                hovertemplate: '%{text}<extra></extra>'
            },
            {
                x: oData.map(d => d.column),
                y: oData.map(d => d.box),
                mode: 'markers',
                marker: {
                    symbol: 'circle-open',
                    size: 15,
                    color: CHART_CONFIG.colors.danger,
                    line: { width: 2 }
                },
                name: 'O (Down)',
                text: oData.map(d => `₹${d.price}`),
                hovertemplate: '%{text}<extra></extra>'
            }
        ];
        
        const layout = {
            title: config.title || 'Point & Figure Chart',
            xaxis: { title: 'Column' },
            yaxis: { title: 'Box Level' },
            hovermode: 'closest'
        };
        
        Plotly.newPlot(this.container, traces, layout, { responsive: true });
    }
}

/**
 * Chart Utilities
 */
const ChartUtils = {
    /**
     * Generate gradient for chart backgrounds
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     * @param {string} startColor - Start color
     * @param {string} endColor - End color
     * @returns {CanvasGradient} Gradient object
     */
    createGradient(ctx, startColor, endColor) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, startColor);
        gradient.addColorStop(1, endColor);
        return gradient;
    },
    
    /**
     * Format price for display
     * @param {number} price - Price value
     * @returns {string} Formatted price
     */
    formatPrice(price) {
        return '₹' + price.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    },
    
    /**
     * Format volume for display
     * @param {number} volume - Volume value
     * @returns {string} Formatted volume
     */
    formatVolume(volume) {
        if (volume >= 10000000) {
            return (volume / 10000000).toFixed(1) + 'Cr';
        } else if (volume >= 100000) {
            return (volume / 100000).toFixed(1) + 'L';
        } else if (volume >= 1000) {
            return (volume / 1000).toFixed(1) + 'K';
        }
        return volume.toString();
    },
    
    /**
     * Calculate technical indicators
     * @param {Array} prices - Price data
     * @param {number} period - Period for calculation
     * @returns {Object} Technical indicators
     */
    calculateIndicators(prices, period = 14) {
        const sma = this.calculateSMA(prices, period);
        const rsi = this.calculateRSI(prices, period);
        const macd = this.calculateMACD(prices);
        
        return { sma, rsi, macd };
    },
    
    /**
     * Calculate Simple Moving Average
     * @param {Array} prices - Price data
     * @param {number} period - Period for SMA
     * @returns {Array} SMA values
     */
    calculateSMA(prices, period) {
        const sma = [];
        for (let i = period - 1; i < prices.length; i++) {
            const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
            sma.push(sum / period);
        }
        return sma;
    },
    
    /**
     * Calculate RSI (Relative Strength Index)
     * @param {Array} prices - Price data
     * @param {number} period - Period for RSI
     * @returns {Array} RSI values
     */
    calculateRSI(prices, period = 14) {
        const changes = [];
        for (let i = 1; i < prices.length; i++) {
            changes.push(prices[i] - prices[i - 1]);
        }
        
        const rsi = [];
        for (let i = period - 1; i < changes.length; i++) {
            const gains = changes.slice(i - period + 1, i + 1).filter(x => x > 0);
            const losses = changes.slice(i - period + 1, i + 1).filter(x => x < 0).map(x => Math.abs(x));
            
            const avgGain = gains.length > 0 ? gains.reduce((a, b) => a + b, 0) / period : 0;
            const avgLoss = losses.length > 0 ? losses.reduce((a, b) => a + b, 0) / period : 0;
            
            const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
            const rsiValue = 100 - (100 / (1 + rs));
            
            rsi.push(rsiValue);
        }
        
        return rsi;
    },
    
    /**
     * Calculate MACD (Moving Average Convergence Divergence)
     * @param {Array} prices - Price data
     * @returns {Object} MACD values
     */
    calculateMACD(prices) {
        const ema12 = this.calculateEMA(prices, 12);
        const ema26 = this.calculateEMA(prices, 26);
        
        const macdLine = [];
        const minLength = Math.min(ema12.length, ema26.length);
        
        for (let i = 0; i < minLength; i++) {
            macdLine.push(ema12[ema12.length - minLength + i] - ema26[ema26.length - minLength + i]);
        }
        
        const signalLine = this.calculateEMA(macdLine, 9);
        const histogram = [];
        
        for (let i = 0; i < signalLine.length; i++) {
            histogram.push(macdLine[macdLine.length - signalLine.length + i] - signalLine[i]);
        }
        
        return {
            macd: macdLine,
            signal: signalLine,
            histogram: histogram
        };
    },
    
    /**
     * Calculate EMA (Exponential Moving Average)
     * @param {Array} prices - Price data
     * @param {number} period - Period for EMA
     * @returns {Array} EMA values
     */
    calculateEMA(prices, period) {
        const ema = [];
        const multiplier = 2 / (period + 1);
        
        // First EMA is just the SMA
        let sum = 0;
        for (let i = 0; i < period; i++) {
            sum += prices[i];
        }
        ema.push(sum / period);
        
        // Calculate subsequent EMAs
        for (let i = period; i < prices.length; i++) {
            const emaValue = (prices[i] * multiplier) + (ema[ema.length - 1] * (1 - multiplier));
            ema.push(emaValue);
        }
        
        return ema;
    }
};

// Export classes and utilities for use in other modules
window.StockPriceChart = StockPriceChart;
window.TechnicalIndicatorsChart = TechnicalIndicatorsChart;
window.VolumeChart = VolumeChart;
window.AlternativeCharts = AlternativeCharts;
window.ChartUtils = ChartUtils;
window.CHART_CONFIG = CHART_CONFIG;