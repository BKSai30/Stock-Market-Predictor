"""
Configuration settings for Stock Market Predictor
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Basic Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    DEBUG = True
    
    # API Keys (You need to get these from respective services)
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY') or 'your-alpha-vantage-key'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'your-news-api-key'
    FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY') or os.environ.get('FINNHUB_TOKEN')
    PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY') or os.environ.get('PPLX_API_KEY')
    PERPLEXITY_MODEL = os.environ.get('PERPLEXITY_MODEL') or 'sonar-small-online'

    # OpenRouter (Grok) settings
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL') or 'xai/grok-2-latest'
    OPENROUTER_BASE_URL = os.environ.get('OPENROUTER_BASE_URL') or 'https://openrouter.ai/api/v1'
    
    # Data fetching settings
    DATA_CACHE_DURATION = timedelta(minutes=15)  # Cache data for 15 minutes
    
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
    MODEL_SAVE_PATH = "data/models/"
    
    # Chart settings
    CHART_CACHE_DURATION = timedelta(hours=1)
    SUPPORTED_CHART_TYPES = [
        'candlestick', 'line', 'bar', 'renko', 'kagi', 
        'point_figure', 'breakout'
    ]
    
    # News settings
    NEWS_SOURCES = [
        'economic-times',
        'business-standard', 
        'livemint',
        'moneycontrol'
    ]
    NEWS_CACHE_DURATION = timedelta(hours=2)
    
    # Volatility categories
    VOLATILITY_CATEGORIES = {
        'safe': {'min_vol': 0, 'max_vol': 15},
        'volatile': {'min_vol': 15, 'max_vol': 30},
        'highly_volatile': {'min_vol': 30, 'max_vol': 100}
    }
    
    # Indian stock market indices and popular stocks
    NIFTY_50_STOCKS = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'HDFC.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIAIRTEL.NS', 'ITC.NS',
        'SBIN.NS', 'BAJFINANCE.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'HCLTECH.NS',
        'AXISBANK.NS', 'LT.NS', 'DMART.NS', 'SUNPHARMA.NS', 'TITAN.NS',
        'ULTRACEMCO.NS', 'WIPRO.NS', 'NESTLEIND.NS', 'POWERGRID.NS', 'NTPC.NS',
        'TECHM.NS', 'M&M.NS', 'TATAMOTORS.NS', 'BAJAJFINSV.NS', 'ONGC.NS',
        'DIVISLAB.NS', 'HDFCLIFE.NS', 'SBILIFE.NS', 'BRITANNIA.NS', 'BPCL.NS',
        'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HINDALCO.NS',
        'HEROMOTOCO.NS', 'INDUSINDBK.NS', 'JSWSTEEL.NS', 'CIPLA.NS', 'TATASTEEL.NS',
        'UPL.NS', 'ADANIENTS.NS', 'APOLLOHOSP.NS', 'TATACONSUM.NS', 'LTIM.NS'
    ]
    
    BSE_SENSEX_STOCKS = [
        'RELIANCE.BS', 'TCS.BS', 'HDFCBANK.BS', 'INFY.BS', 'HINDUNILVR.BS',
        'HDFC.BS', 'ICICIBANK.BS', 'KOTAKBANK.BS', 'BHARTIAIRTEL.BS', 'ITC.BS',
        'SBIN.BS', 'BAJFINANCE.BS', 'ASIANPAINT.BS', 'MARUTI.BS', 'L&T.BS',
        'AXISBANK.BS', 'SUNPHARMA.BS', 'TITAN.BS', 'ULTRACEMCO.BS', 'WIPRO.BS',
        'NESTLEIND.BS', 'POWERGRID.BS', 'NTPC.BS', 'TECHM.BS', 'M&M.BS',
        'TATAMOTORS.BS', 'BAJAJFINSV.BS', 'ONGC.BS', 'HDFCLIFE.BS', 'SBILIFE.BS'
    ]
    
    # Machine Learning model parameters
    ML_MODELS = {
        'lstm': {
            'sequence_length': 60,
            'epochs': 50,
            'batch_size': 32,
            'neurons': [50, 50, 50],
            'dropout': 0.2
        },
        'random_forest': {
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': 42
        },
        'xgboost': {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'random_state': 42
        },
        'svm': {
            'kernel': 'rbf',
            'C': 1.0,
            'gamma': 'scale'
        }
    }
    
    # Technical indicators
    TECHNICAL_INDICATORS = {
        'sma_periods': [10, 20, 50, 200],
        'ema_periods': [12, 26],
        'rsi_period': 14,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'bollinger_period': 20,
        'bollinger_std': 2,
        'atr_period': 14
    }
    
    # Sentiment analysis settings
    SENTIMENT_CONFIG = {
        'news_lookback_days': 7,
        'social_media_weight': 0.3,
        'news_weight': 0.7,
        'sentiment_threshold': 0.1,
        'keywords_weight': {
            'bullish': ['growth', 'profit', 'buy', 'upgrade', 'positive', 'rise'],
            'bearish': ['loss', 'sell', 'downgrade', 'negative', 'fall', 'decline']
        }
    }
    
    # Logging configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'logs/app.log',
                'formatter': 'default'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            }
        },
        'loggers': {
            '': {
                'handlers': ['file', 'console'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with secure settings for production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'
    
    # Use environment variables for sensitive data
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    
    # Use test database
    DATA_CACHE_DURATION = timedelta(seconds=1)
    MODEL_RETRAIN_INTERVAL = timedelta(minutes=1)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}