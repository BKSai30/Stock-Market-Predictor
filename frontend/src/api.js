const API_BASE_URL = 'http://localhost:5000/api';

export const stockAPI = {
    // Get stock prediction
    predict: async (symbol, days) => {
        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    symbol: symbol,
                    days_ahead: days
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Prediction API error:', error);
            throw error;
        }
    },

    // Get chart data
    getChartData: async (symbol, type = 'candlestick') => {
        try {
            const response = await fetch(`${API_BASE_URL}/chart-data/${symbol}?type=${type}`);
            return await response.json();
        } catch (error) {
            console.error('Chart data API error:', error);
            throw error;
        }
    },

    // Get top stocks
    getTopStocks: async (category = 'safe') => {
        try {
            const response = await fetch(`${API_BASE_URL}/top-stocks?category=${category}`);
            return await response.json();
        } catch (error) {
            console.error('Top stocks API error:', error);
            throw error;
        }
    }
};
