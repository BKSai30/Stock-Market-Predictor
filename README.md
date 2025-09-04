# Stock Market Growth/Decay Predictor - Indian Market Web Application

A comprehensive AI-powered stock market prediction system specifically designed for the Indian stock market (NSE/BSE). This application combines machine learning models, technical analysis, and real-time news sentiment analysis to predict stock price movements.

![Stock Market Predictor](https://img.shields.io/badge/Stock-Predictor-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

## 🌟 Features

### AI-Powered Predictions
- **Multiple ML Models**: LSTM, Random Forest, XGBoost, SVM for accurate predictions
- **Ensemble Approach**: Combines multiple models for enhanced accuracy
- **5-30 Day Forecasting**: Predict stock prices for up to 30 days ahead
- **Confidence Scoring**: Get confidence levels for each prediction

### Technical Analysis
- **Multiple Chart Types**: Candlestick, Renko, Kagi, Point & Figure, Breakout charts
- **Technical Indicators**: RSI, MACD, Bollinger Bands, SMA, EMA, ATR
- **Pattern Recognition**: Automatic detection of chart patterns
- **Support & Resistance**: Identify key price levels

### Sentiment Analysis
- **Real-time News Analysis**: Process financial news from major Indian sources
- **Sector-wise Sentiment**: Get sentiment for specific sectors
- **Market Sentiment**: Overall market mood indicator
- **Multi-source Integration**: Combine news, social media, and market reports

### Indian Market Focus
- **NSE & BSE Integration**: Support for both major Indian exchanges
- **NIFTY 50 & SENSEX**: Track major indices
- **Indian Stock Symbols**: Optimized for Indian stock naming conventions
- **Rupee-based Pricing**: All prices displayed in Indian Rupees

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live market data and predictions
- **Interactive Charts**: Zoom, pan, and explore data
- **Volatility Classification**: Safe, Moderate, and High volatility stocks

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14+ (for development tools)
- Git

### Installation

1. **Clone the Repository**
   ```bash
   cd /d D:\SAI\Computer Learn
   git clone <your-repository-url>
   cd Stock-Market-Predictor
   ```

2. **Create Project Structure**
   ```bash
   # Windows Command Prompt
   mkdir backend backend\models backend\routes backend\utils backend\data backend\data\models backend\data\cache
   mkdir frontend frontend\css frontend\js frontend\assets frontend\assets\images
   mkdir docs tests
   ```

3. **Set Up Python Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-secret-key-here
   ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
   NEWS_API_KEY=your-news-api-key
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

6. **Initialize the Application**
   ```bash
   cd backend
   python app.py
   ```

7. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
Stock-Market-Predictor/
├── backend/                    # Flask backend application
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # ML models and prediction logic
│   │   ├── stock_predictor.py # Main prediction models
│   │   ├── sentiment_analyzer.py # News sentiment analysis
│   │   └── chart_analyzer.py  # Technical chart analysis
│   ├── routes/                # API routes
│   │   ├── stock_routes.py    # Stock-related endpoints
│   │   ├── news_routes.py     # News and sentiment endpoints
│   │   └── volatility_routes.py # Volatility classification
│   ├── utils/                 # Utility modules
│   │   ├── data_fetcher.py    # Data fetching utilities
│   │   ├── chart_generator.py # Chart generation
│   │   └── helpers.py         # Helper functions
│   └── data/                  # Data storage
│       ├── models/            # Saved ML models
│       └── cache/             # Cached data
├── frontend/                  # Frontend web application
│   ├── index.html            # Main HTML file
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   ├── main.js           # Main application logic
│   │   ├── charts.js         # Chart handling
│   │   └── api.js            # API communication
│   └── assets/
│       └── images/           # Image assets
├── docs/                     # Documentation
│   ├── README.md            # This file
│   ├── API_Documentation.md  # API endpoint docs
│   └── Setup_Guide.md       # Detailed setup guide
└── tests/                   # Test files
    ├── test_models.py       # Model tests
    ├── test_routes.py       # API route tests
    └── test_utils.py        # Utility tests
```

## 🔧 Configuration

### API Keys Required

1. **Alpha Vantage API** (Free tier available)
   - Sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Get your free API key
   - Add to `.env` file

2. **News API** (Optional, for enhanced news sentiment)
   - Sign up at [News API](https://newsapi.org/)
   - Get your API key
   - Add to `.env` file

### Environment Configuration

Edit `backend/config.py` to customize:

```python
# Stock market settings
MARKET_OPEN_TIME = "09:15"  # IST
MARKET_CLOSE_TIME = "15:30"  # IST
MARKET_TIMEZONE = "Asia/Kolkata"

# Prediction settings
DEFAULT_PREDICTION_DAYS = 5
MAX_PREDICTION_DAYS = 30
MIN_HISTORICAL_DAYS = 365 * 5  # 5 years minimum

# Model settings
MODEL_RETRAIN_INTERVAL = timedelta(days=7)  # Retrain models weekly
```

## 📊 Usage

### Making Predictions

1. **Select a Stock**: Enter NSE symbol (e.g., RELIANCE, TCS, HDFCBANK)
2. **Choose Prediction Period**: 5, 10, 15, or 30 days
3. **Click Predict**: Get AI-powered price predictions
4. **View Results**: See predicted prices, confidence scores, and recommendations

### Analyzing Charts

1. **Select Chart Type**: Choose from Candlestick, Renko, Kagi, Point & Figure
2. **View Technical Indicators**: RSI, MACD, Bollinger Bands automatically calculated
3. **Identify Patterns**: System highlights important chart patterns
4. **Support/Resistance**: See key price levels

### Top Stocks by Volatility

1. **Safe Stocks**: Low volatility, stable performance
2. **Moderate Volatility**: Balanced risk-reward stocks
3. **High Volatility**: Higher risk, potentially higher returns

## 🔍 API Endpoints

### Stock Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "symbol": "RELIANCE",
  "days_ahead": 5
}
```

### Get Chart Data
```http
GET /api/chart-data/RELIANCE?type=candlestick&period=1y
```

### Top Stocks
```http
GET /api/top-stocks?category=safe
```

### Stock Sentiment
```http
GET /api/news/RELIANCE/sentiment
```

For complete API documentation, see [API_Documentation.md](docs/API_Documentation.md)

## 🧠 Machine Learning Models

### Implemented Models

1. **LSTM (Long Short-Term Memory)**
   - Best for time series prediction
   - Captures long-term dependencies
   - 60-day sequence length

2. **Random Forest**
   - Robust to overfitting
   - Feature importance analysis
   - Ensemble of decision trees

3. **XGBoost**
   - Gradient boosting algorithm
   - High performance on structured data
   - Handles missing values well

4. **Support Vector Regression (SVR)**
   - Effective for non-linear relationships
   - Good generalization capability
   - Kernel-based approach

### Feature Engineering

- **Price Features**: OHLC, price changes, ratios
- **Technical Indicators**: 20+ indicators including RSI, MACD, Bollinger Bands
- **Volume Features**: Volume ratios, volume moving averages
- **Lag Features**: Historical price and volume lags
- **Momentum Features**: Rate of change, momentum indicators

### Model Training

Models are retrained weekly with the latest data to maintain accuracy. The system uses:

- **80/20 Train-Test Split**: For model evaluation
- **Cross-Validation**: For robust performance assessment
- **Ensemble Methods**: Combining multiple models for better predictions
- **Feature Selection**: Automated selection of most relevant features

## 📈 Technical Indicators

### Trend Indicators
- **Simple Moving Average (SMA)**: 10, 20, 50, 200 periods
- **Exponential Moving Average (EMA)**: 12, 26 periods
- **MACD**: Moving Average Convergence Divergence

### Momentum Indicators
- **RSI**: Relative Strength Index (14 periods)
- **Stochastic**: %K and %D oscillators
- **Rate of Change (ROC)**: Price momentum

### Volatility Indicators
- **Bollinger Bands**: 20-period with 2 standard deviations
- **Average True Range (ATR)**: 14-period volatility measure
- **Volatility**: Rolling standard deviation

### Volume Indicators
- **Volume SMA**: 20-period volume average
- **Volume Ratio**: Current vs average volume

## 📰 Sentiment Analysis

### News Sources
- Economic Times
- Business Standard
- Livemint
- Moneycontrol
- Additional financial news APIs

### Sentiment Processing
1. **Text Preprocessing**: Clean and normalize news text
2. **Keyword Extraction**: Identify stock-specific keywords
3. **Sentiment Scoring**: Using VADER and TextBlob
4. **Relevance Weighting**: Weight by relevance to specific stock
5. **Time Decay**: Recent news has higher impact

### Sentiment Integration
- **Bullish/Bearish Classification**: Based on sentiment scores
- **Confidence Levels**: How certain the sentiment analysis is
- **Sector Sentiment**: Aggregate sentiment for stock sectors
- **Market Sentiment**: Overall market mood

## ⚠️ Disclaimers

**IMPORTANT: This application is for educational and research purposes only.**

- Stock predictions are not guaranteed and should not be used as the sole basis for investment decisions
- Past performance does not guarantee future results
- Always consult with qualified financial advisors before making investment decisions
- The developers are not responsible for any financial losses incurred from using this application
- Market conditions can change rapidly and unpredictably

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_models.py

# Run with coverage
python -m pytest --cov=backend tests/
```

### Test Coverage

- **Model Tests**: Validate ML model predictions and accuracy
- **API Tests**: Test all API endpoints for correct responses
- **Utility Tests**: Test data fetching and processing functions
- **Integration Tests**: End-to-end testing of complete workflows

## 🚀 Deployment

### Development Deployment

```bash
cd backend
python app.py
```

### Production Deployment

1. **Configure Production Settings**
   ```python
   # In config.py
   class ProductionConfig(Config):
       DEBUG = False
       TESTING = False
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

3. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   ```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY frontend/ ./static/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code style
- Use meaningful commit messages
- Add tests for new features
- Update documentation for any changes
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Yahoo Finance**: For providing free stock market data
- **Alpha Vantage**: For comprehensive financial APIs
- **News API**: For financial news aggregation
- **Chart.js & Plotly**: For powerful charting capabilities
- **Bootstrap**: For responsive UI components
- **scikit-learn & TensorFlow**: For machine learning capabilities

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Documentation**: Review this README and API docs
2. **Search Issues**: Look through existing GitHub issues
3. **Create an Issue**: If you find a bug or have a feature request
4. **Contact**: Reach out to the development team

## 🔮 Future Enhancements

### Planned Features
- **Real-time Data Streaming**: WebSocket-based live updates
- **Portfolio Management**: Track multiple stocks and portfolios
- **Alert System**: Price and indicator-based alerts
- **Mobile App**: React Native mobile application
- **Advanced ML Models**: Transformer-based models for better predictions
- **Options Trading**: Support for options and derivatives analysis
- **Backtesting**: Historical strategy testing capabilities

### Technical Improvements
- **Caching Layer**: Redis for improved performance
- **Database Integration**: PostgreSQL for persistent data storage
- **Microservices**: Split into smaller, focused services
- **Container Orchestration**: Kubernetes deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Performance Monitoring**: Application performance tracking

---

**Happy Trading! 📈**

*Remember: Always do your own research and never invest more than you can afford to lose.*