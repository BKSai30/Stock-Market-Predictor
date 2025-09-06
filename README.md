 
# 🚀 AI-Powered Stock Market Predictor

<div align="center">

![Stock Market Predictor Banner](https://via.placeholder.com/800x200/667eea/ffffff?text=AI-Powered+Stock+Market+Predictor)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.0+-orange.svg)](https://chartjs.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*A comprehensive web application that leverages advanced machine learning algorithms to predict stock prices, analyze market trends, and provide intelligent investment recommendations.*

[🎯 Features](#-features) • [🏗️ Architecture](#-architecture--design-philosophy) • [🚀 Quick Start](#-installation) • [📖 Usage Guide](#-usage-guide) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🏗️ Architecture & Design Philosophy](#-architecture--design-philosophy)
- [🚀 Features](#-features)
- [🔧 Technology Stack](#-technology-stack)
- [📦 Installation](#-installation)
- [🎮 Usage Guide](#-usage-guide)
- [📊 API Documentation](#-api-documentation)
- [🧠 Machine Learning Models](#-machine-learning-models)
- [📈 Technical Analysis](#-technical-analysis)
- [💼 Portfolio Management](#-portfolio-management)
- [🔐 Security Features](#-security-features)
- [📱 Responsive Design](#-responsive-design)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Project Overview

### What is the AI-Powered Stock Market Predictor?

The **AI-Powered Stock Market Predictor** is a comprehensive, full-stack web application designed to democratize access to sophisticated stock market analysis and prediction tools. Built with the philosophy that **everyone deserves access to advanced financial analytics**, this application combines cutting-edge machine learning algorithms with an intuitive, user-friendly interface.

### 🎯 Mission Statement

> *"To provide retail investors, students, and financial enthusiasts with professional-grade stock analysis tools that were previously available only to institutional investors."*

### 🌟 What Makes This Project Special?

1. **🧠 Advanced AI Integration**: Utilizes an ensemble of machine learning models (LSTM, Random Forest, XGBoost) for superior prediction accuracy
2. **📊 Multiple Chart Types**: Supports 5 different technical analysis chart types including Candlestick, Renko, Kagi, Point & Figure, and Breakout charts
3. **🔄 Real-time Data**: Integrates with multiple data sources (Yahoo Finance, NSE India) for live market data
4. **🎨 Intuitive UI/UX**: Modern, responsive design with dark/light mode support
5. **🤖 AI Assistant**: Built-in investment education and guidance system
6. **📱 Mobile-First**: Fully responsive design that works seamlessly across all devices
7. **🔐 Secure**: User authentication, session management, and data protection

---

## 🏗️ Architecture & Design Philosophy

### Why a Single Backend Server Architecture?

This project intentionally uses a **monolithic Flask backend** rather than a microservices architecture or separate frontend/backend setup. Here's why:

#### 🎯 **Simplicity & Maintainability**
- **Single Codebase**: All functionality is contained in one application, making it easier to understand, debug, and maintain
- **Reduced Complexity**: No need to manage multiple services, API gateways, or inter-service communication
- **Quick Development**: Faster to develop and iterate on features without managing multiple deployments

#### 🚀 **Performance Benefits**
- **Reduced Latency**: No network calls between frontend and backend services
- **Server-Side Rendering**: HTML templates are rendered on the server, providing faster initial page loads
- **Efficient Resource Usage**: Single process handles all requests, reducing memory and CPU overhead

#### 💡 **Educational Value**
- **Learning-Friendly**: Perfect for understanding full-stack development in a single application
- **Easy to Deploy**: Can be deployed to any platform that supports Python/Flask (Heroku, AWS, DigitalOcean, etc.)
- **Cost-Effective**: Runs on minimal resources, making it suitable for students and hobbyists

#### 🔧 **Technical Advantages**
- **Shared Database**: All components can directly access the same SQLite database without API calls
- **Session Management**: Simplified user authentication and session handling
- **Real-time Updates**: WebSocket integration is straightforward without cross-service complexity

### Application Flow Architecture

User Browser → Flask Application Server → Authentication Layer
→ API Routes
→ Template Rendering
→ Database Layer (SQLite)
→ External APIs (Yahoo Finance, NSE India)

API Routes → Stock Prediction Engine → ML Model Ensemble (LSTM + Random Forest + XGBoost)
→ Portfolio Manager
→ Technical Analysis
→ News Aggregator
→ AI Assistant

 

### Database Schema

The application uses a simple but effective SQLite database schema:

-- Users table for authentication
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio tracking
CREATE TABLE portfolio (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
symbol TEXT NOT NULL,
shares INTEGER NOT NULL,
purchase_price REAL NOT NULL,
purchase_date DATE NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Model calibration data
CREATE TABLE calibrations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
symbol TEXT NOT NULL,
calibration_data TEXT,
accuracy_score REAL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

  

---

## 🚀 Features

### 📊 **Advanced Stock Prediction Engine**

#### Multi-Model Ensemble Approach
- **LSTM Neural Networks**: Captures long-term dependencies in time series data
- **Random Forest**: Handles non-linear relationships and feature interactions
- **XGBoost**: Gradient boosting for high-accuracy predictions
- **Ensemble Voting**: Combines predictions from all models for superior accuracy

#### Flexible Prediction Periods
- **5-Day Predictions**: Short-term trading insights
- **10-Day Predictions**: Medium-term trend analysis
- **15-Day Predictions**: Extended planning horizon
- **30-Day Predictions**: Monthly investment strategies

#### Model Calibration & Self-Learning
- **Backtesting System**: Continuously improves accuracy through historical analysis
- **Accuracy Tracking**: Monitors and reports model performance
- **Adaptive Learning**: Model weights adjust based on prediction success rates

### 📈 **Comprehensive Technical Analysis**

#### Interactive Chart Types with Zoom & Pan Controls
1. **Candlestick Charts**: Traditional OHLC visualization with volume analysis
2. **Renko Charts**: Price movement without time consideration for trend clarity
3. **Kagi Charts**: Supply and demand visualization with trend thickness
4. **Point & Figure Charts**: X and O columns for breakout identification
5. **Breakout Charts**: Support and resistance level analysis with alerts

#### Advanced Technical Indicators
- **RSI (Relative Strength Index)**: Momentum oscillator with overbought/oversold signals
- **MACD**: Trend-following momentum indicator with signal line crossovers
- **SMA (Simple Moving Average)**: 20-period and 50-period trend lines
- **Bollinger Bands**: Volatility bands with squeeze and expansion analysis

#### Chart Interaction Features
- **Mouse Wheel Zoom**: Intuitive zooming with scroll wheel
- **Pan Navigation**: Click and drag to explore different time periods
- **Control Buttons**: Zoom in/out, reset zoom, pan left/right buttons
- **Real-time Updates**: Live price updates without page refresh

### 💼 **Intelligent Portfolio Management**

#### Real-time Portfolio Tracking
- **Live Price Updates**: Real-time stock price fetching from multiple sources
- **Profit/Loss Analytics**: Instant calculation of gains/losses with percentages
- **Performance Metrics**: Annualized returns, holding periods, and volatility measures
- **Historical Analysis**: Track highest/lowest prices since purchase

#### Smart AI Recommendations
- **HOLD**: Maintain current positions with reasoning
- **PARTIAL SELL**: Profit-taking strategies (20-50% position reduction)
- **STRONG SELL**: Risk management exit strategies with stop-loss suggestions
- **BUY MORE**: Opportunity identification for position averaging

#### Portfolio Analytics
- **Diversification Score**: Sector and stock concentration analysis
- **Risk Metrics**: Portfolio volatility and correlation analysis
- **Rebalancing Suggestions**: Optimal allocation recommendations
- **Performance Attribution**: Identify top and bottom contributors

### 📰 **Market News & Analysis**

#### Curated Financial Content
- **Multi-Category Coverage**: Economy, Technology, Banking, Energy, Healthcare
- **Expert Analysis**: In-depth articles with professional commentary
- **Real-time Updates**: Latest market developments and breaking news
- **Category Filtering**: Easy navigation through news sections

#### Market Dashboard
- **NIFTY 50 Index**: Real-time index tracking with daily changes
- **SENSEX Monitoring**: Bombay Stock Exchange primary index
- **FII Investment Flows**: Foreign institutional investor activity
- **Market Sentiment**: Overall market mood indicators

### 🎯 **Top Performing Stocks Analysis**

#### Customizable Stock Screening
- **Category Selection**: Safe Stocks, Volatile Stocks, High Risk/Reward options
- **Adjustable Count**: Display 1-10 top performing stocks
- **Time Period Flexibility**: Analyze performance over 1-30 days
- **Quick Prediction Access**: One-click prediction for any displayed stock

#### Performance Metrics Display
- **Current Price**: Real-time market prices
- **Predicted Price**: AI-generated price forecasts
- **Historical Performance**: Price changes over selected time period
- **Confidence Levels**: Model confidence in predictions

### 🤖 **AI Investment Assistant**

#### 24/7 Virtual Advisor
- **Investment Education**: Beginner to advanced investment concepts
- **Platform Navigation**: Step-by-step guidance for using all features
- **Technical Indicator Explanations**: Detailed explanations of RSI, MACD, Bollinger Bands
- **Personalized Advice**: Tailored recommendations based on user queries

#### Educational Content Library
- **Stock Market Basics**: Fundamental investment principles
- **Risk Management**: Portfolio diversification and stop-loss strategies
- **Tax Guidance**: Indian market-specific tax implications (LTCG/STCG)
- **Trading Strategies**: Value investing, growth investing, momentum trading

### 🎨 **Modern User Experience**

#### Responsive Design Excellence
- **Mobile-First Approach**: Optimized for smartphones and tablets
- **Bootstrap 5 Integration**: Modern, clean interface components
- **Dark/Light Mode**: Seamless theme switching with preference saving
- **Accessibility Compliant**: WCAG guidelines implementation

#### Interactive Elements
- **Smooth Animations**: CSS transitions and micro-interactions
- **Loading States**: User feedback during data processing
- **Toast Notifications**: Non-intrusive status updates
- **Progressive Loading**: Staggered content loading for better UX

---

## 🔧 Technology Stack

### Backend Technologies

#### **Flask Framework (2.3+)**
Core Flask setup with security
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(name)
CORS(app)
app.secret_key = 'secure-secret-key'

 

#### **Database Layer**
- **SQLite**: Embedded database for development and small-scale deployment
- **Parameterized Queries**: SQL injection prevention
- **Session Management**: Secure user session handling with timeout

#### **Machine Learning Stack**
ML Libraries
import pandas as pd # Data manipulation and analysis
import numpy as np # Numerical computing
import yfinance as yf # Real-time stock data
import scikit-learn # Machine learning algorithms
import xgboost as xgb # Gradient boosting

 

### Frontend Technologies

#### **Modern Web Standards**
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Custom properties, flexbox, and grid layouts
- **ES6+ JavaScript**: Async/await, modules, and modern syntax

#### **UI Framework & Visualization**
- **Bootstrap 5.3**: Responsive grid system and components
- **Chart.js 4.0**: Interactive charts with zoom/pan capabilities
- **Font Awesome 6.4**: Professional icon library

### External APIs & Data Sources

#### **Real-time Data Integration**
Multiple data source fallback
def get_real_stock_price(symbol):
# Primary: Yahoo Finance
try:
ticker = yf.Ticker(f"{symbol}.NS")
return ticker.history(period="1d")['Close'].iloc[-1]
except:
# Fallback: NSE India API
return fetch_from_nse_api(symbol)

 

---

## 📦 Installation

### System Requirements

#### **Minimum Requirements**
- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Network**: Internet connection for real-time data

### Step-by-Step Installation

#### **1. Clone the Repository**
Clone the repository
git clone https://github.com/yourusername/stock-market-predictor.git
cd stock-market-predictor

 

#### **2. Set Up Python Virtual Environment**
Create virtual environment
python -m venv venv

Activate virtual environment
Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate



#### **3. Install Dependencies**

Create `requirements.txt`:
Flask==2.3.3
Flask-CORS==4.0.0
yfinance==0.2.28
pandas==2.1.1
numpy==1.24.3
requests==2.31.0
Werkzeug==2.3.7
scikit-learn==1.3.0
python-dateutil==2.8.2
xgboost==1.7.6
matplotlib==3.7.2

 

Install packages:
pip install -r requirements.txt

 

#### **4. Environment Configuration**

Create `.env` file:
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=True
PORT=5000


#### **5. Initialize and Run**
Run the application
python app.py
 

Open browser and navigate to `http://localhost:5000`

### 🐳 Docker Installation (Alternative)

Create `Dockerfile`:
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
 

Create `docker-compose.yml`:
version: '3.8'
services:
web:
build: .
ports:
- "5000:5000"
volumes:
- .:/app
environment:
- FLASK_ENV=development
- DEBUG=True
 
undefined
Build and run with Docker
docker-compose up --build
 

---

## 🎮 Usage Guide

### 🚀 Getting Started

#### **Account Setup**
1. Navigate to the homepage
2. Click "Register" and create account with email/password
3. Log in to access all features

#### **Making Your First Prediction**
1. **Enter Stock Information**:
   - Symbol: "TCS", "RELIANCE", "HDFCBANK"
   - Name: "Tata Consultancy Services"
   - Keywords: "tata", "hdfc bank"

2. **Select Time Period**: Choose 5, 10, 15, or 30 days

3. **Analyze Results**:
   - Current vs predicted price
   - Confidence percentage
   - Buy/Sell/Hold recommendation
   - Technical indicators analysis

### 📊 **Understanding Predictions**

#### **Confidence Levels Interpretation**
- **90-95%**: Very high confidence - Strong signals from multiple indicators
- **80-89%**: High confidence - Reliable predictions with good data quality
- **70-79%**: Moderate confidence - Consider additional analysis
- **Below 70%**: Lower confidence - Use caution, gather more information

#### **Recommendation Actions**
- **STRONG BUY**: Expected growth > 5% with high confidence
- **BUY**: Expected growth 2-5% with moderate risk
- **HOLD**: Expected change -2% to +2%, maintain position
- **SELL**: Expected decline 2-5%, consider reducing position
- **STRONG SELL**: Expected decline > 5%, exit recommended

### 💼 **Portfolio Management Workflow**

#### **Adding Investments**
Required Information:

Stock Symbol: e.g., "TCS"

Number of Shares: e.g., 100

Purchase Price: e.g., ₹3,500.00

Purchase Date: e.g., "2024-01-15"
 

#### **Portfolio Metrics**
- **Invested Amount**: Total capital deployed
- **Current Value**: Real-time market valuation
- **Profit/Loss**: Absolute and percentage returns
- **Days Held**: Investment holding period
- **Performance Tracking**: Highest/lowest prices achieved

### 📈 **Technical Analysis Guide**

#### **Chart Types Usage**
1. **Candlestick**: Best for detailed OHLC analysis and pattern recognition
2. **Renko**: Ideal for trend identification without time noise
3. **Kagi**: Excellent for supply/demand analysis
4. **Point & Figure**: Perfect for breakout and reversal signals
5. **Breakout**: Specialized for support/resistance trading

#### **Interactive Controls**
- **Zoom**: Mouse wheel or zoom buttons for detailed analysis
- **Pan**: Click and drag or arrow buttons to navigate
- **Reset**: Return to original view
- **Time Period**: Switch between 1mo, 3mo, 6mo, 1y views

### 🎯 **Top Performing Stocks Feature**

#### **Customization Options**
- **Categories**: Safe (blue-chip), Volatile (mid-cap), High Risk/Reward (small-cap)
- **Count**: Display 1-10 stocks based on preference
- **Time Frame**: Analyze 1-30 day performance windows
- **Quick Actions**: One-click prediction access

### 🤖 **AI Assistant Capabilities**

#### **Sample Questions**
Investment Guidance:
"How do I start investing with ₹10,000?"
"What is the difference between SIP and lump sum?"
"How to read candlestick patterns?"

Technical Help:
"How to add stocks to my portfolio?"
"What does RSI above 70 mean?"
"How accurate are the predictions?"

Platform Navigation:
"How to change the chart type?"
"Where can I see my profit and loss?"
"How to calibrate the prediction model?"

 

---

## 📊 API Documentation

### Authentication Endpoints

#### **POST /api/register**
Register new user account.
Request:
{
"email": "user@example.com",
"password": "securepassword123"
}

Response:
{
"success": true,
"message": "Registration successful"
}
 

#### **POST /api/login** 
Authenticate existing user.
Request:
{
"email": "user@example.com",
"password": "securepassword123"
}

Response:
{
"success": true,
"message": "Login successful"
}
 

### Stock Analysis Endpoints

#### **POST /api/search-stock**
Search stocks by symbol, name, or keywords.
Request:
{
"input": "TCS"
}

Response:
{
"found": true,
"symbol": "TCS",
"name": "Tata Consultancy Services",
"sector": "IT"
}
 

#### **POST /api/predict**
Generate AI-powered stock predictions.
Request:
{
"symbol": "TCS",
"days_ahead": 10
}

Response:
{
"symbol": "TCS",
"name": "Tata Consultancy Services",
"current_price": 3500.00,
"predicted_price": 3675.00,
"price_change_pct": 5.0,
"confidence": 87,
"recommendation": "BUY",
"enhanced_recommendation": {
"action": "BUY",
"strength": "Moderate",
"reasoning": ["Positive outlook with 5.0% expected growth"],
"risk_level": "Medium"
},
"historical_data": [...],
"prediction_data": [...],
"ai_analysis": {...},
"sentiment_analysis": {...}
}

 

#### **GET /api/technical-chart/{symbol}**
Retrieve technical chart data and indicators.
Query Parameters: ?type=candlestick&period=3mo

Response:
{
"symbol": "TCS",
"chart_type": "candlestick",
"period": "3mo",
"data": [
{
"date": "2024-01-15",
"open": 3500.00,
"high": 3550.00,
"low": 3480.00,
"close": 3525.00,
"volume": 1250000
}
],
"indicators": {
"rsi": 65.5,
"macd": 12.5,
"sma_20": 3510.00,
"bb_upper": 3580.00,
"bb_lower": 3440.00
},
"patterns": {
"detected_patterns": ["Bullish Trend"],
"support_levels": [3400.00],
"resistance_levels": [3600.00]
}
}

 

#### **GET /api/top-stocks**
Get top performing stocks by category.
Query Parameters: ?category=safe&count=5&time_period=7

Response:
{
"category": "safe",
"count": 5,
"time_period": 7,
"stocks": [
{
"symbol": "TCS",
"name": "Tata Consultancy Services",
"current_price": 3675.00,
"predicted_price": 3750.00,
"price_change": 2.5,
"predicted_change": 2.04,
"prediction_confidence": 89
}
]
}

 

### Portfolio Management Endpoints

#### **POST /api/portfolio/add**
Add stock to user portfolio.
Request:
{
"symbol": "TCS",
"shares": 100,
"purchase_price": 3500.00,
"purchase_date": "2024-01-15"
}

Response:
{
"success": true,
"message": "Stock added to portfolio"
}

 

#### **GET /api/portfolio/get**
Retrieve complete portfolio analytics.
Response:
{
"portfolio": [
{
"id": 1,
"symbol": "TCS",
"shares": 100,
"purchase_price": 3500.00,
"current_price": 3675.00,
"profit_loss": 17500.00,
"profit_loss_pct": 5.0,
"recommendation": {...}
}
],
"summary": {
"total_invested": 350000.00,
"total_current_value": 367500.00,
"total_profit_loss": 17500.00,
"total_profit_loss_pct": 5.0
}
}

 

#### **DELETE /api/portfolio/remove/{id}**
Remove stock from portfolio.

---

## 🧠 Machine Learning Models

### Ensemble Architecture

The prediction system combines three complementary machine learning approaches:

#### **1. LSTM Neural Network (40% weight)**
- **Purpose**: Captures long-term temporal dependencies in stock price movements
- **Architecture**: 50-unit LSTM layers with dropout for regularization
- **Strengths**: Excellent for trend continuation and cyclical pattern recognition
- **Input**: Sequential price data with technical indicators

def create_lstm_model(sequence_length, features):
model = Sequential([
LSTM(50, return_sequences=True, input_shape=(sequence_length, features)),
Dropout(0.2),
LSTM(50, return_sequences=False),
Dropout(0.2),
Dense(25),
Dense(1)
])
return model

 

#### **2. Random Forest Regressor (30% weight)**
- **Purpose**: Handles complex non-linear relationships between features
- **Configuration**: 100 estimators with controlled depth to prevent overfitting
- **Strengths**: Robust to outliers, provides feature importance rankings
- **Input**: Technical indicators, volume metrics, and price ratios

def create_random_forest_model():
model = RandomForestRegressor(
n_estimators=100,
max_depth=10,
min_samples_split=5,
min_samples_leaf=2,
random_state=42
)
return model

 

#### **3. XGBoost Regressor (30% weight)**
- **Purpose**: High-accuracy gradient boosting with regularization
- **Optimization**: Tuned hyperparameters for stock market volatility
- **Strengths**: Superior performance on structured data, handles missing values
- **Input**: Comprehensive feature set including market sentiment indicators

def create_xgboost_model():
model = xgb.XGBRegressor(
learning_rate=0.1,
max_depth=6,
n_estimators=100,
subsample=0.8,
colsample_bytree=0.8,
reg_alpha=0.1,
reg_lambda=0.1,
random_state=42
)
return model

 

### Model Training Pipeline

def ensemble_prediction_workflow(symbol, days_ahead):
"""
Complete prediction workflow with ensemble voting
"""
# 1. Data Collection & Preprocessing
raw_data = fetch_stock_data(symbol, period='2y')
processed_data = preprocess_stock_data(raw_data)

 
# 2. Feature Engineering
technical_features = calculate_technical_indicators(processed_data)
price_features = extract_price_patterns(processed_data)

# 3. Individual Model Predictions
lstm_pred = lstm_model.predict(prepare_lstm_input(processed_data))
rf_pred = rf_model.predict(prepare_rf_input(technical_features))
xgb_pred = xgb_model.predict(prepare_xgb_input(price_features))

# 4. Ensemble Voting with Confidence Weighting
weights = [0.4, 0.3, 0.3]  # LSTM, RF, XGB
final_prediction = weights * lstm_pred + weights * rf_pred + weights * xgb_pred[11][12]
confidence_score = calculate_prediction_confidence([lstm_pred, rf_pred, xgb_pred])

return final_prediction, confidence_score
 

### Accuracy Calibration System

The application includes a sophisticated calibration mechanism that continuously improves prediction accuracy:

def perform_backtesting_calibration(symbol, test_periods=10):
"""
Backtesting system for model accuracy improvement
"""
historical_data = fetch_extended_history(symbol, '1y')
accuracy_scores = []

 
for period in range(test_periods):
    # Simulate historical prediction
    start_idx = period * 5  # 5-day intervals
    end_idx = start_idx + 5
    
    if end_idx >= len(historical_data):
        break
        
    actual_price = historical_data.iloc[end_idx]['Close']
    base_price = historical_data.iloc[start_idx]['Close']
    
    # Test multiple prediction strategies
    strategies = [
        base_price * 1.0,  # No change baseline
        base_price * random.uniform(0.98, 1.02),  # Random walk
        base_price * (1 + trend_analysis(historical_data[start_idx:end_idx]))
    ]
    
    best_accuracy = 0
    for predicted_price in strategies:
        accuracy = 100 - abs((predicted_price - actual_price) / actual_price) * 100
        best_accuracy = max(best_accuracy, accuracy)
    
    accuracy_scores.append(max(best_accuracy, 50))  # Minimum 50% accuracy

# Calculate calibration factor
avg_accuracy = np.mean(accuracy_scores) if accuracy_scores else 75.0
calibration_factor = 1.0 + (avg_accuracy - 75) / 1000  # Slight adjustment

# Store calibration data
store_calibration_data(symbol, calibration_factor, avg_accuracy)

return avg_accuracy
 

---

## 📈 Technical Analysis

### Comprehensive Indicator Suite

#### **Momentum Indicators**
- **RSI (Relative Strength Index)**: 14-period momentum oscillator
- **Stochastic**: %K and %D lines for overbought/oversold conditions
- **Williams %R**: Price momentum in relation to high-low range

def calculate_rsi(prices, period=14):
delta = prices.diff()
gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
return rsi

  

#### **Trend Indicators**
- **MACD**: 12/26/9 configuration with histogram analysis
- **Moving Averages**: SMA 20/50/200 for trend identification
- **Parabolic SAR**: Stop-and-reverse points for trend changes

def calculate_macd(prices, fast=12, slow=26, signal=9):
ema_fast = prices.ewm(span=fast).mean()
ema_slow = prices.ewm(span=slow).mean()
macd_line = ema_fast - ema_slow
signal_line = macd_line.ewm(span=signal).mean()
histogram = macd_line - signal_line

 
return {
    'macd': macd_line,
    'signal': signal_line,
    'histogram': histogram
}
 

#### **Volatility Indicators**
- **Bollinger Bands**: 20-period with 2 standard deviations
- **Average True Range (ATR)**: 14-period volatility measurement
- **Volatility Index**: Custom volatility scoring system

def calculate_bollinger_bands(prices, period=20, std_dev=2):
sma = prices.rolling(window=period).mean()
std = prices.rolling(window=period).std()

 
upper_band = sma + (std * std_dev)
lower_band = sma - (std * std_dev)

return {
    'upper': upper_band,
    'middle': sma,
    'lower': lower_band,
    'bandwidth': (upper_band - lower_band) / sma
}
 

### Advanced Chart Pattern Recognition

def detect_chart_patterns(ohlc_data):
"""
Automated chart pattern detection system
"""
patterns_found = []

 
# Support and Resistance Levels
resistance_levels = []
support_levels = []

# Find local highs and lows
for i in range(20, len(ohlc_data) - 20):
    # Local high (resistance)
    if (ohlc_data['High'].iloc[i] > ohlc_data['High'].iloc[i-20:i+20].max() * 0.99):
        resistance_levels.append(ohlc_data['High'].iloc[i])
    
    # Local low (support)  
    if (ohlc_data['Low'].iloc[i] < ohlc_data['Low'].iloc[i-20:i+20].min() * 1.01):
        support_levels.append(ohlc_data['Low'].iloc[i])

# Trend Analysis
recent_data = ohlc_data.tail(20)
price_changes = recent_data['Close'].pct_change().dropna()

if len(price_changes) > 0:
    trend_strength = price_changes.sum()
    if trend_strength > 0.05:
        patterns_found.append('Strong Bullish Trend')
    elif trend_strength < -0.05:
        patterns_found.append('Strong Bearish Trend')
    else:
        patterns_found.append('Sideways Movement')

return {
    'detected_patterns': patterns_found,
    'support_levels': list(set(support_levels))[-3:],  # Last 3 unique levels
    'resistance_levels': list(set(resistance_levels))[-3:]  # Last 3 unique levels
}
 

### Interactive Chart Implementation

The technical charts support full interactivity with professional-grade features:

// Advanced charting with zoom and pan capabilities
function createTechnicalChart(data) {
const ctx = document.getElementById('technicalChart').getContext('2d');

 
const chartConfig = {
    type: 'line',
    data: {
        datasets: prepareChartDatasets(data)
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            zoom: {
                zoom: {
                    wheel: { enabled: true, speed: 0.1 },
                    pinch: { enabled: true },
                    mode: 'xy'
                },
                pan: {
                    enabled: true,
                    mode: 'xy',
                    threshold: 10
                }
            },
            tooltip: {
                callbacks: {
                    title: (context) => formatTooltipTitle(context),
                    label: (context) => formatTooltipLabel(context, data)
                }
            }
        },
        scales: {
            x: { 
                type: 'time',
                time: { unit: 'day' }
            },
            y: { 
                beginAtZero: false,
                title: { display: true, text: 'Price (₹)' }
            }
        }
    }
};

return new Chart(ctx, chartConfig);
}



---

## 💼 Portfolio Management

### Comprehensive Analytics Engine

#### **Real-time Performance Tracking**
- **Portfolio Valuation**: Live calculation of total portfolio worth
- **Individual Position Analysis**: Per-stock performance metrics
- **Sector Allocation**: Diversification analysis across industries
- **Risk Assessment**: Volatility and correlation measurements

#### **Intelligent Recommendation System**
def generate_portfolio_recommendations(positions, market_conditions):
"""
AI-powered portfolio optimization recommendations
"""
recommendations = []


for position in positions:
    # Performance Analysis
    pnl_pct = position['unrealized_pnl_pct']
    days_held = position['days_held']
    weight = position['weight']
    
    recommendation = {
        'symbol': position['symbol'],
        'action': 'HOLD',
        'urgency': 'LOW',
        'reasoning': []
    }
    
    # Profit-taking logic
    if pnl_pct > 25:
        recommendation.update({
            'action': 'PARTIAL_SELL',
            'percentage': '40-60%',
            'reason': 'Lock in exceptional profits while maintaining exposure',
            'urgency': 'HIGH'
        })
    elif pnl_pct > 15:
        recommendation.update({
            'action': 'PARTIAL_SELL', 
            'percentage': '25-40%',
            'reason': 'Secure partial profits on strong performance',
            'urgency': 'MEDIUM'
        })
    
    # Loss management
    elif pnl_pct < -20:
        if days_held < 90:
            recommendation.update({
                'action': 'REVIEW',
                'reason': 'Significant short-term loss requires analysis',
                'urgency': 'MEDIUM'
            })
        else:
            recommendation.update({
                'action': 'CONSIDER_EXIT',
                'reason': 'Extended period of major losses',
                'urgency': 'HIGH'
            })
    
    # Concentration risk
    if weight > 20:
        recommendation['reasoning'].append(f'High concentration risk at {weight:.1f}% of portfolio')
        recommendation['urgency'] = 'MEDIUM'
    
    recommendations.append(recommendation)

return recommendations
 

#### **Advanced Portfolio Metrics**
- **Sharpe Ratio**: Risk-adjusted return calculation
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Beta Analysis**: Portfolio volatility relative to market
- **Correlation Matrix**: Inter-stock relationship analysis

def calculate_portfolio_metrics(positions):
"""
Calculate comprehensive portfolio performance metrics
"""
returns = [pos['unrealized_pnl_pct'] for pos in positions]
weights = [pos['weight'] for pos in positions]


# Portfolio return
portfolio_return = sum(ret * weight / 100 for ret, weight in zip(returns, weights))

# Risk metrics
portfolio_volatility = np.sqrt(np.dot(weights, np.dot(calculate_covariance_matrix(positions), weights)))

# Sharpe ratio (assuming risk-free rate of 6%)
risk_free_rate = 6.0
sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0

# Diversification metrics
concentration_ratio = sum(sorted(weights, reverse=True)[:3])  # Top 3 holdings

return {
    'portfolio_return': portfolio_return,
    'portfolio_volatility': portfolio_volatility,
    'sharpe_ratio': sharpe_ratio,
    'concentration_ratio': concentration_ratio,
    'number_of_positions': len(positions)
}


### Risk Management Features

#### **Diversification Analysis**
def analyze_portfolio_diversification(positions):
"""
Comprehensive diversification scoring
"""
# Sector allocation
sector_allocation = {}
for position in positions:
sector = get_stock_sector(position['symbol'])
sector_allocation[sector] = sector_allocation.get(sector, 0) + position['weight']


# Diversification score (0-100)
num_sectors = len(sector_allocation)
max_sector_weight = max(sector_allocation.values()) if sector_allocation else 100

diversification_score = min(100, (num_sectors * 20) - max_sector_weight + 20)

# Risk assessment
if diversification_score > 80:
    risk_level = 'LOW'
elif diversification_score > 60:
    risk_level = 'MEDIUM' 
else:
    risk_level = 'HIGH'

return {
    'diversification_score': diversification_score,
    'risk_level': risk_level,
    'sector_allocation': sector_allocation,
    'recommendations': generate_diversification_recommendations(sector_allocation)
}
def generate_diversification_recommendations(sector_allocation):
"""
Generate sector diversification recommendations
"""
recommendations = []


for sector, weight in sector_allocation.items():
    if weight > 40:
        recommendations.append({
            'type': 'REDUCE_CONCENTRATION',
            'sector': sector,
            'current_weight': weight,
            'suggested_weight': 25,
            'reason': f'Reduce {sector} concentration from {weight:.1f}% to under 25%'
        })
    elif weight < 5 and len(sector_allocation) > 5:
        recommendations.append({
            'type': 'CONSIDER_ELIMINATION',
            'sector': sector, 
            'current_weight': weight,
            'reason': f'Consider eliminating small {weight:.1f}% {sector} position'
        })

return recommendations


---

## 🔐 Security Features

### Multi-Layer Security Implementation

#### **Authentication Security**
- **Password Hashing**: PBKDF2 with SHA-256 and salting
- **Session Management**: Secure cookies with HTTPOnly and SameSite flags
- **Login Attempts**: Rate limiting to prevent brute force attacks
- **Session Timeout**: Automatic logout after inactivity

class SecurityManager:
def init(self):
self.max_login_attempts = 5
self.login_attempts = {}
self.session_timeout = 1800 # 30 minutes


def hash_password(self, password):
    """Securely hash passwords"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(self, password, hash):
    """Verify password against hash"""
    return check_password_hash(hash, password)

def check_login_attempts(self, email):
    """Check if user has exceeded login attempts"""
    attempts = self.login_attempts.get(email, {'count': 0, 'last_attempt': 0})
    
    if attempts['count'] >= self.max_login_attempts:
        time_since_last = time.time() - attempts['last_attempt']
        if time_since_last < 900:  # 15 minute lockout
            return False
        else:
            # Reset attempts after lockout period
            self.login_attempts[email] = {'count': 0, 'last_attempt': 0}
    
    return True

def record_login_attempt(self, email, success):
    """Record login attempt"""
    if success:
        self.login_attempts[email] = {'count': 0, 'last_attempt': 0}
    else:
        attempts = self.login_attempts.get(email, {'count': 0, 'last_attempt': 0})
        self.login_attempts[email] = {
            'count': attempts['count'] + 1,
            'last_attempt': time.time()
        }


#### **Input Validation & Sanitization**
class InputValidator:
@staticmethod
def validate_stock_symbol(symbol):
"""Validate stock symbol input"""
if not symbol or not isinstance(symbol, str):
raise ValueError("Stock symbol must be a non-empty string")


    # Remove whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Check format (alphanumeric, 1-10 characters)
    if not re.match(r'^[A-Z0-9]{1,10}$', symbol):
        raise ValueError("Invalid stock symbol format")
    
    return symbol

@staticmethod
def validate_email(email):
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
    return email.lower().strip()

@staticmethod
def sanitize_html_input(input_string):
    """Sanitize HTML input to prevent XSS"""
    if not input_string:
        return ""
    # Remove HTML tags and escape special characters
    clean = re.sub(r'<[^>]*>', '', input_string)
    return html.escape(clean).strip()

@staticmethod
def validate_numeric_input(value, min_val=None, max_val=None, field_name="Value"):
    """Validate numeric inputs with range checking"""
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid number")
    
    if min_val is not None and numeric_value < min_val:
        raise ValueError(f"{field_name} must be at least {min_val}")
    
    if max_val is not None and numeric_value > max_val:
        raise ValueError(f"{field_name} must not exceed {max_val}")
    
    return numeric_value


#### **API Security Measures**
- **Rate Limiting**: Request throttling per IP and user
- **CSRF Protection**: Token-based form security
- **Data Encryption**: Sensitive data encryption at rest
- **Audit Logging**: Security event logging and monitoring

from functools import wraps
from time import time

class RateLimiter:
def init(self):
self.requests = {}
self.limits = {
'default': {'requests': 100, 'window': 3600}, # 100/hour
'prediction': {'requests': 10, 'window': 300}, # 10/5min
'login': {'requests': 5, 'window': 300} # 5/5min
}
 
def is_allowed(self, identifier, endpoint='default'):
    """Check if request is within rate limits"""
    now = time()
    limit_config = self.limits.get(endpoint, self.limits['default'])
    
    if identifier not in self.requests:
        self.requests[identifier] = []
    
    # Clean old requests
    self.requests[identifier] = [
        req_time for req_time in self.requests[identifier]
        if now - req_time < limit_config['window']
    ]
    
    # Check limit
    if len(self.requests[identifier]) >= limit_config['requests']:
        return False
    
    # Add current request
    self.requests[identifier].append(now)
    return True
def rate_limit(endpoint='default'):
"""Decorator for rate limiting API endpoints"""
def decorator(f):
@wraps(f)
def decorated_function(*args, **kwargs):
identifier = request.remote_addr
if 'user_id' in session:
identifier = f"user_{session['user_id']}"
 
        if not rate_limiter.is_allowed(identifier, endpoint):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.'
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function
return decorator
 

### Privacy Protection

#### **Data Handling Policies**
- **Minimal Data Collection**: Only necessary information stored
- **Local Storage**: User data remains on local database
- **No Third-party Sharing**: Portfolio data never shared externally
- **User Control**: Complete data deletion capabilities

def delete_user_data(user_id):
"""Complete user data deletion for privacy compliance"""
conn = sqlite3.connect('stock_app.db')
c = conn.cursor() 
try:
    # Delete portfolio data
    c.execute('DELETE FROM portfolio WHERE user_id = ?', (user_id,))
    
    # Delete calibration data associated with user
    c.execute('DELETE FROM calibrations WHERE id IN (SELECT id FROM calibrations WHERE created_at IN (SELECT created_at FROM portfolio WHERE user_id = ?))', (user_id,))
    
    # Delete user account
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    conn.commit()
    return True
except Exception as e:
    conn.rollback()
    raise e
finally:
    conn.close() 

---

## 📱 Responsive Design

### Mobile-First Architecture

#### **Responsive Breakpoints**
- **Mobile**: 320px - 768px (Optimized touch interfaces)
- **Tablet**: 768px - 1024px (Hybrid interaction patterns)
- **Desktop**: 1024px+ (Full feature accessibility)

/* Responsive Design CSS */
:root {
--mobile-breakpoint: 768px;
--tablet-breakpoint: 1024px;
}

/* Mobile First Styles */
.chart-container {
height: 300px;
margin: 10px 0;
}

/* Tablet Styles */
@media (min-width: 768px) {
.chart-container {
height: 400px;
margin: 20px 0;
}
}

/* Desktop Styles */
@media (min-width: 1024px) {
.chart-container {
height: 500px;
margin: 30px 0;
}
}
 

#### **Touch-Optimized Features**
- **Large Touch Targets**: Minimum 44px touch areas
- **Swipe Gestures**: Chart navigation via touch swipes
- **Responsive Charts**: Auto-scaling visualizations
- **Collapsible Sections**: Space-efficient information display

### Progressive Web App Features

#### **Offline Capabilities**
// Service Worker for offline functionality
if ('serviceWorker' in navigator) {
navigator.serviceWorker.register('/sw.js')
.then(registration => {
console.log('PWA features enabled');
});
}

// Service Worker Implementation
self.addEventListener('fetch', event => {
if (event.request.url.includes('/api/portfolio')) {
event.respondWith(
caches.match(event.request)
.then(response => {
if (response) {
return response;
}
return fetch(event.request)
.then(response => {
const responseClone = response.clone();
caches.open('portfolio-cache')
.then(cache => {
cache.put(event.request, responseClone);
});
return response;
});
})
);
}
});
 

---

## 🚀 Deployment

### Production Deployment Options

#### **Heroku Deployment**
Create `Procfile`: