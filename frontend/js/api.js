/**
 * API Communication Module for Stock Market Predictor
 * Handles all API calls and data communication with the backend
 */

// API Configuration
const API_CONFIG = {
    baseURL: window.location.origin,
    timeout: 30000, // 30 seconds
    retryAttempts: 3,
    retryDelay: 1000 // 1 second
};

/**
 * Make an API call with error handling and retry logic
 * @param {string} endpoint - API endpoint (e.g., '/api/predict')
 * @param {string} method - HTTP method ('GET', 'POST', 'PUT', 'DELETE')
 * @param {Object} data - Request data (for POST/PUT requests)
 * @param {Object} options - Additional options
 * @returns {Promise} API response data
 */
async function apiCall(endpoint, method = 'GET', data = null, options = {}) {
    const url = `${API_CONFIG.baseURL}${endpoint}`;
    
    const requestOptions = {
        method: method.toUpperCase(),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            ...options.headers
        },
        signal: AbortSignal.timeout(API_CONFIG.timeout),
        ...options
    };
    
    // Add request body for POST/PUT requests
    if (data && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
        requestOptions.body = JSON.stringify(data);
    }
    
    let lastError;
    
    // Retry logic
    for (let attempt = 0; attempt < API_CONFIG.retryAttempts; attempt++) {
        try {
            console.log(`API Call (attempt ${attempt + 1}): ${method.toUpperCase()} ${url}`, data);
            
            const response = await fetch(url, requestOptions);
            
            // Handle HTTP errors
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new APIError(
                    errorData.error || `HTTP ${response.status}: ${response.statusText}`,
                    response.status,
                    errorData
                );
            }
            
            // Parse JSON response
            const responseData = await response.json();
            console.log(`API Response: ${method.toUpperCase()} ${url}`, responseData);
            
            return responseData;
            
        } catch (error) {
            lastError = error;
            
            // Don't retry for certain error types
            if (error instanceof APIError && error.status >= 400 && error.status < 500) {
                throw error;
            }
            
            // Don't retry on the last attempt
            if (attempt === API_CONFIG.retryAttempts - 1) {
                break;
            }
            
            // Wait before retrying
            await sleep(API_CONFIG.retryDelay * (attempt + 1));
            console.warn(`API call failed, retrying in ${API_CONFIG.retryDelay * (attempt + 1)}ms...`, error);
        }
    }
    
    // If all retries failed, throw the last error
    throw lastError;
}

/**
 * Custom API Error class
 */
class APIError extends Error {
    constructor(message, status, data = {}) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Sleep utility function
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise}
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Stock Prediction API calls
 */
const StockAPI = {
    /**
     * Predict stock price
     * @param {string} symbol - Stock symbol
     * @param {number} daysAhead - Number of days to predict
     * @returns {Promise} Prediction data
     */
    async predict(symbol, daysAhead = 5) {
        return await apiCall('/api/predict', 'POST', {
            symbol: symbol,
            days_ahead: daysAhead
        });
    },
    
    /**
     * Get stock information
     * @param {string} symbol - Stock symbol
     * @returns {Promise} Stock information
     */
    async getStockInfo(symbol) {
        return await apiCall(`/api/stock/${symbol}/info`);
    },
    
    /**
     * Search stocks
     * @param {string} query - Search query
     * @returns {Promise} Search results
     */
    async searchStocks(query) {
        return await apiCall(`/api/stock/search?q=${encodeURIComponent(query)}`);
    },
    
    /**
     * Get chart data
     * @param {string} symbol - Stock symbol
     * @param {string} chartType - Chart type (candlestick, renko, kagi, etc.)
     * @param {string} period - Time period
     * @returns {Promise} Chart data
     */
    async getChartData(symbol, chartType = 'candlestick', period = '1y') {
        return await apiCall(`/api/chart-data/${symbol}?type=${chartType}&period=${period}`);
    },
    
    /**
     * Get technical analysis
     * @param {string} symbol - Stock symbol
     * @returns {Promise} Technical analysis data
     */
    async getTechnicalAnalysis(symbol) {
        return await apiCall(`/api/stock/${symbol}/analysis`);
    }
};

/**
 * Market Data API calls
 */
const MarketAPI = {
    /**
     * Get market indices
     * @returns {Promise} Market indices data
     */
    async getIndices() {
        return await apiCall('/api/market/indices');
    },
    
    /**
     * Get top stocks by volatility
     * @param {string} category - Volatility category (safe, volatile, highly_volatile)
     * @returns {Promise} Top stocks data
     */
    async getTopStocks(category = 'safe') {
        return await apiCall(`/api/top-stocks?category=${category}`);
    },
    
    /**
     * Get market overview
     * @returns {Promise} Market overview data
     */
    async getMarketOverview() {
        return await apiCall('/api/market/overview');
    }
};

/**
 * News and Sentiment API calls
 */
const NewsAPI = {
    /**
     * Get stock sentiment
     * @param {string} symbol - Stock symbol
     * @returns {Promise} Sentiment data
     */
    async getSentiment(symbol) {
        return await apiCall(`/api/news/${symbol}/sentiment`);
    },
    
    /**
     * Get stock news
     * @param {string} symbol - Stock symbol
     * @param {number} days - Number of days to look back
     * @returns {Promise} News articles
     */
    async getStockNews(symbol, days = 7) {
        return await apiCall(`/api/news/${symbol}?days=${days}`);
    },
    
    /**
     * Get market sentiment
     * @returns {Promise} Market sentiment data
     */
    async getMarketSentiment() {
        return await apiCall('/api/news/market-sentiment');
    }
};

/**
 * Volatility Classification API calls
 */
const VolatilityAPI = {
    /**
     * Classify stock volatility
     * @param {string} symbol - Stock symbol
     * @returns {Promise} Volatility classification
     */
    async classifyVolatility(symbol) {
        return await apiCall(`/api/volatility/${symbol}/classify`);
    },
    
    /**
     * Get volatility metrics
     * @param {string} symbol - Stock symbol
     * @returns {Promise} Volatility metrics
     */
    async getVolatilityMetrics(symbol) {
        return await apiCall(`/api/volatility/${symbol}/metrics`);
    }
};

/**
 * Utility API calls
 */
const UtilityAPI = {
    /**
     * Health check
     * @returns {Promise} Health status
     */
    async healthCheck() {
        return await apiCall('/api/health');
    },
    
    /**
     * Get system status
     * @returns {Promise} System status
     */
    async getSystemStatus() {
        return await apiCall('/api/status');
    }
};

/**
 * Cache management for API responses
 */
class APICache {
    constructor(maxSize = 100, ttl = 300000) { // Default 5 minutes TTL
        this.cache = new Map();
        this.maxSize = maxSize;
        this.ttl = ttl;
    }
    
    /**
     * Generate cache key
     * @param {string} endpoint 
     * @param {string} method 
     * @param {Object} data 
     * @returns {string} Cache key
     */
    generateKey(endpoint, method, data) {
        return `${method}:${endpoint}:${JSON.stringify(data || {})}`;
    }
    
    /**
     * Get cached response
     * @param {string} key - Cache key
     * @returns {any} Cached data or null
     */
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        // Check if expired
        if (Date.now() > item.expires) {
            this.cache.delete(key);
            return null;
        }
        
        return item.data;
    }
    
    /**
     * Set cached response
     * @param {string} key - Cache key
     * @param {any} data - Data to cache
     */
    set(key, data) {
        // Remove oldest items if cache is full
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        
        this.cache.set(key, {
            data: data,
            expires: Date.now() + this.ttl
        });
    }
    
    /**
     * Clear cache
     */
    clear() {
        this.cache.clear();
    }
    
    /**
     * Get cache statistics
     * @returns {Object} Cache stats
     */
    getStats() {
        return {
            size: this.cache.size,
            maxSize: this.maxSize,
            ttl: this.ttl
        };
    }
}

// Create global cache instance
const apiCache = new APICache();

/**
 * Enhanced API call with caching
 * @param {string} endpoint 
 * @param {string} method 
 * @param {Object} data 
 * @param {Object} options 
 * @returns {Promise} API response
 */
async function cachedApiCall(endpoint, method = 'GET', data = null, options = {}) {
    // Only cache GET requests by default
    const shouldCache = options.cache !== false && method.toUpperCase() === 'GET';
    
    if (shouldCache) {
        const cacheKey = apiCache.generateKey(endpoint, method, data);
        const cachedResponse = apiCache.get(cacheKey);
        
        if (cachedResponse) {
            console.log(`Cache hit: ${method.toUpperCase()} ${endpoint}`);
            return cachedResponse;
        }
    }
    
    const response = await apiCall(endpoint, method, data, options);
    
    if (shouldCache) {
        const cacheKey = apiCache.generateKey(endpoint, method, data);
        apiCache.set(cacheKey, response);
    }
    
    return response;
}

/**
 * Batch API calls
 * @param {Array} requests - Array of request objects
 * @param {Object} options - Batch options
 * @returns {Promise} Array of responses
 */
async function batchApiCalls(requests, options = {}) {
    const { concurrency = 5, failFast = false } = options;
    
    const results = [];
    
    // Process requests in batches
    for (let i = 0; i < requests.length; i += concurrency) {
        const batch = requests.slice(i, i + concurrency);
        
        const batchPromises = batch.map(async (request, index) => {
            try {
                const result = await apiCall(
                    request.endpoint,
                    request.method || 'GET',
                    request.data,
                    request.options
                );
                return { success: true, data: result, index: i + index };
            } catch (error) {
                if (failFast) throw error;
                return { success: false, error: error, index: i + index };
            }
        });
        
        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);
    }
    
    return results;
}

/**
 * File upload utility
 * @param {string} endpoint - Upload endpoint
 * @param {File} file - File to upload
 * @param {Object} options - Upload options
 * @returns {Promise} Upload response
 */
async function uploadFile(endpoint, file, options = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Add additional fields
    if (options.fields) {
        Object.entries(options.fields).forEach(([key, value]) => {
            formData.append(key, value);
        });
    }
    
    const requestOptions = {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(API_CONFIG.timeout * 3), // Longer timeout for uploads
        ...options.requestOptions
    };
    
    // Don't set Content-Type header for FormData - browser will set it with boundary
    delete requestOptions.headers?.['Content-Type'];
    
    const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, requestOptions);
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new APIError(
            errorData.error || `Upload failed: ${response.status}`,
            response.status,
            errorData
        );
    }
    
    return await response.json();
}

/**
 * Download file utility
 * @param {string} endpoint - Download endpoint
 * @param {string} filename - Desired filename
 * @param {Object} options - Download options
 */
async function downloadFile(endpoint, filename, options = {}) {
    const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
        method: 'GET',
        signal: AbortSignal.timeout(API_CONFIG.timeout * 3),
        ...options
    });
    
    if (!response.ok) {
        throw new APIError(`Download failed: ${response.status}`, response.status);
    }
    
    const blob = await response.blob();
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * WebSocket connection for real-time data
 */
class StockWebSocket {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.listeners = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }
    
    /**
     * Connect to WebSocket
     */
    connect() {
        try {
            this.ws = new WebSocket(this.url);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
                this.emit('connected');
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.emit('message', data);
                    
                    // Emit specific event types
                    if (data.type) {
                        this.emit(data.type, data);
                    }
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.emit('disconnected');
                this.attemptReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.emit('error', error);
            };
        } catch (error) {
            console.error('Error connecting to WebSocket:', error);
        }
    }
    
    /**
     * Disconnect from WebSocket
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
    
    /**
     * Send message
     * @param {Object} message - Message to send
     */
    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        }
    }
    
    /**
     * Add event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }
    
    /**
     * Remove event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }
    
    /**
     * Emit event
     * @param {string} event - Event name
     * @param {any} data - Event data
     */
    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in WebSocket event listener for ${event}:`, error);
                }
            });
        }
    }
    
    /**
     * Attempt to reconnect
     */
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
            this.emit('maxReconnectAttemptsReached');
        }
    }
}

// Export all functions and classes for use in other modules
window.apiCall = apiCall;
window.cachedApiCall = cachedApiCall;
window.batchApiCalls = batchApiCalls;
window.uploadFile = uploadFile;
window.downloadFile = downloadFile;
window.StockAPI = StockAPI;
window.MarketAPI = MarketAPI;
window.NewsAPI = NewsAPI;
window.VolatilityAPI = VolatilityAPI;
window.UtilityAPI = UtilityAPI;
window.APIError = APIError;
window.apiCache = apiCache;
window.StockWebSocket = StockWebSocket;