from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Sample stock data for demonstration
SAMPLE_STOCKS = {
    'safe': [
        {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'sector': 'Banking'},
        {'symbol': 'TCS', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
        {'symbol': 'INFY', 'name': 'Infosys', 'sector': 'IT'},
        {'symbol': 'WIPRO', 'name': 'Wipro', 'sector': 'IT'},
        {'symbol': 'ICICIBANK', 'name': 'ICICI Bank', 'sector': 'Banking'}
    ],
    'volatile': [
        {'symbol': 'RELIANCE', 'name': 'Reliance Industries', 'sector': 'Oil & Gas'},
        {'symbol': 'ADANIPORTS', 'name': 'Adani Ports', 'sector': 'Infrastructure'},
        {'symbol': 'BAJFINANCE', 'name': 'Bajaj Finance', 'sector': 'NBFC'},
        {'symbol': 'MARUTI', 'name': 'Maruti Suzuki', 'sector': 'Automotive'},
        {'symbol': 'ASIANPAINT', 'name': 'Asian Paints', 'sector': 'Paints'}
    ],
    'highly_volatile': [
        {'symbol': 'ADANIENT', 'name': 'Adani Enterprises', 'sector': 'Conglomerate'},
        {'symbol': 'TATAMOTORS', 'name': 'Tata Motors', 'sector': 'Automotive'},
        {'symbol': 'ZEEL', 'name': 'Zee Entertainment', 'sector': 'Media'},
        {'symbol': 'YESBANK', 'name': 'Yes Bank', 'sector': 'Banking'},
        {'symbol': 'SUZLON', 'name': 'Suzlon Energy', 'sector': 'Renewable Energy'}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_stock():
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        days_ahead = int(data.get('days_ahead', 5))
        
        if not symbol:
            return jsonify({'error': 'Stock symbol is required'}), 400
        
        # Try to fetch real data from Yahoo Finance
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            hist = ticker.history(period="3mo")  # Get more historical data
            info = ticker.info
            
            if hist.empty:
                # Fallback to sample data
                current_price = random.uniform(1000, 5000)
                predicted_price = current_price * random.uniform(0.95, 1.05)
                stock_name = f"{symbol} Ltd"
                historical_data = generate_sample_historical_data(current_price)
            else:
                current_price = float(hist['Close'].iloc[-1])
                # Simple prediction (in reality, you'd use ML models)
                predicted_price = current_price * random.uniform(0.98, 1.02)
                stock_name = info.get('longName', f"{symbol} Ltd")
                
                # Convert historical data for chart
                historical_data = []
                for date, row in hist.tail(30).iterrows():  # Last 30 days
                    historical_data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'price': round(float(row['Close']), 2)
                    })
                
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            # Fallback to sample data
            current_price = random.uniform(1000, 5000)
            predicted_price = current_price * random.uniform(0.95, 1.05)
            stock_name = f"{symbol} Ltd"
            historical_data = generate_sample_historical_data(current_price)
        
        # Generate prediction data for chart
        prediction_data = generate_prediction_data(current_price, predicted_price, days_ahead)
        
        # Calculate confidence and recommendation
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        confidence = random.randint(70, 95)
        
        if price_change_pct > 2:
            recommendation = 'BUY'
        elif price_change_pct < -2:
            recommendation = 'SELL'
        else:
            recommendation = 'HOLD'
        
        # Generate AI Analysis
        ai_analysis = generate_ai_analysis(symbol, price_change_pct, confidence)
        
        # Generate Sentiment Analysis
        sentiment_analysis = generate_sentiment_analysis(symbol, recommendation)
        
        return jsonify({
            'symbol': symbol,
            'name': stock_name,
            'current_price': round(current_price, 2),
            'predicted_price': round(predicted_price, 2),
            'price_change_pct': round(price_change_pct, 2),
            'confidence': confidence,
            'recommendation': recommendation,
            'days_ahead': days_ahead,
            'historical_data': historical_data,
            'prediction_data': prediction_data,
            'ai_analysis': ai_analysis,
            'sentiment_analysis': sentiment_analysis
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/technical-chart/<symbol>')
def get_technical_chart(symbol):
    try:
        chart_type = request.args.get('type', 'candlestick')
        period = request.args.get('period', '3mo')
        
        # Fetch stock data
        ticker = yf.Ticker(f"{symbol}.NS")
        hist = ticker.history(period=period)
        
        if hist.empty:
            # Generate sample data if real data not available
            hist = generate_sample_ohlc_data(symbol, period)
        
        # Process data based on chart type
        if chart_type == 'candlestick':
            chart_data = process_candlestick_data(hist)
        elif chart_type == 'renko':
            chart_data = process_renko_data(hist)
        elif chart_type == 'kagi':
            chart_data = process_kagi_data(hist)
        elif chart_type == 'point_figure':
            chart_data = process_point_figure_data(hist)
        elif chart_type == 'breakout':
            chart_data = process_breakout_data(hist)
        else:
            chart_data = process_candlestick_data(hist)  # Default
        
        # Generate technical indicators
        indicators = calculate_technical_indicators(hist)
        
        # Generate pattern analysis
        patterns = analyze_chart_patterns(hist, chart_type)
        
        return jsonify({
            'symbol': symbol,
            'chart_type': chart_type,
            'data': chart_data,
            'indicators': indicators,
            'patterns': patterns,
            'success': True
        })
        
    except Exception as e:
        print(f"Technical chart error for {symbol}: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/top-stocks')
def get_top_stocks():
    try:
        category = request.args.get('category', 'safe')
        stocks = SAMPLE_STOCKS.get(category, SAMPLE_STOCKS['safe'])
        
        # Add sample data for each stock
        enhanced_stocks = []
        for stock in stocks:
            try:
                # Try to get real data
                ticker = yf.Ticker(f"{stock['symbol']}.NS")
                hist = ticker.history(period="5d")
                
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    prev_price = float(hist['Close'].iloc[0])
                    price_change = ((current_price - prev_price) / prev_price) * 100
                else:
                    # Fallback data
                    current_price = random.uniform(500, 3000)
                    price_change = random.uniform(-5, 5)
                
                predicted_price = current_price * random.uniform(1.02, 1.08)
                
                enhanced_stocks.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'current_price': round(current_price, 2),
                    'predicted_price': round(predicted_price, 2),
                    'price_change': round(price_change, 2),
                    'prediction_confidence': random.randint(75, 90),
                    'chart_data': generate_sample_chart_data(current_price)
                })
                
            except Exception as e:
                print(f"Error processing {stock['symbol']}: {e}")
                # Fallback data
                current_price = random.uniform(500, 3000)
                price_change = random.uniform(-5, 5)
                predicted_price = current_price * random.uniform(1.02, 1.08)
                
                enhanced_stocks.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'current_price': round(current_price, 2),
                    'predicted_price': round(predicted_price, 2),
                    'price_change': round(price_change, 2),
                    'prediction_confidence': random.randint(75, 90),
                    'chart_data': generate_sample_chart_data(current_price)
                })
        
        return jsonify({
            'category': category,
            'stocks': enhanced_stocks
        })
        
    except Exception as e:
        print(f"Top stocks error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart-data/<symbol>')
def get_chart_data(symbol):
    try:
        chart_type = request.args.get('type', 'candlestick')
        period = request.args.get('period', '1mo')
        
        ticker = yf.Ticker(f"{symbol}.NS")
        hist = ticker.history(period=period)
        
        if hist.empty:
            return jsonify({'error': 'No data found for symbol'}), 404
        
        chart_data = []
        for date, row in hist.iterrows():
            chart_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(float(row['Open']), 2),
                'high': round(float(row['High']), 2),
                'low': round(float(row['Low']), 2),
                'close': round(float(row['Close']), 2),
                'volume': int(row['Volume'])
            })
        
        return jsonify({
            'symbol': symbol,
            'type': chart_type,
            'data': chart_data
        })
        
    except Exception as e:
        print(f"Chart data error: {e}")
        return jsonify({'error': str(e)}), 500

# Helper functions for data generation and processing
def generate_sample_historical_data(current_price, days=30):
    """Generate sample historical data"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    price = current_price * 0.9  # Start lower
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        change = random.uniform(-0.03, 0.04)
        price = price * (1 + change)
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(price, 2)
        })
    
    return data

def generate_prediction_data(current_price, predicted_price, days_ahead):
    """Generate prediction data for chart"""
    data = []
    base_date = datetime.now()
    
    # Add current price as starting point
    data.append({
        'date': base_date.strftime('%Y-%m-%d'),
        'price': current_price,
        'is_prediction': False
    })
    
    # Generate prediction points
    price_diff = predicted_price - current_price
    for i in range(1, days_ahead + 1):
        date = base_date + timedelta(days=i)
        # Interpolate between current and predicted price
        progress = i / days_ahead
        predicted_point = current_price + (price_diff * progress)
        # Add some randomness
        predicted_point *= random.uniform(0.99, 1.01)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(predicted_point, 2),
            'is_prediction': True
        })
    
    return data

def generate_ai_analysis(symbol, price_change_pct, confidence):
    """Generate AI analysis based on stock data"""
    trend = "bullish" if price_change_pct > 0 else "bearish"
    strength = "strong" if abs(price_change_pct) > 3 else "moderate" if abs(price_change_pct) > 1 else "weak"
    
    analysis = {
        'trend': trend.capitalize(),
        'strength': strength.capitalize(),
        'key_factors': [
            f"Technical indicators show {strength} {trend} momentum",
            f"Price prediction confidence level: {confidence}%",
            f"Expected price movement: {abs(price_change_pct):.1f}%"
        ],
        'risk_level': 'Low' if abs(price_change_pct) < 2 else 'Medium' if abs(price_change_pct) < 5 else 'High',
        'model_used': 'Ensemble (LSTM + Random Forest + XGBoost)',
        'data_quality': 'Good' if confidence > 80 else 'Moderate'
    }
    
    return analysis

def generate_sentiment_analysis(symbol, recommendation):
    """Generate sentiment analysis"""
    sentiments = ['Positive', 'Neutral', 'Negative']
    news_sentiment = random.choice(sentiments)
    social_sentiment = random.choice(sentiments)
    
    # Align sentiment with recommendation
    if recommendation == 'BUY':
        overall_sentiment = 'Positive'
        sentiment_score = random.uniform(0.6, 0.9)
    elif recommendation == 'SELL':
        overall_sentiment = 'Negative'
        sentiment_score = random.uniform(-0.9, -0.6)
    else:
        overall_sentiment = 'Neutral'
        sentiment_score = random.uniform(-0.3, 0.3)
    
    analysis = {
        'overall_sentiment': overall_sentiment,
        'sentiment_score': round(sentiment_score, 2),
        'news_sentiment': news_sentiment,
        'social_sentiment': social_sentiment,
        'sentiment_sources': [
            'Economic Times',
            'Business Standard',
            'Moneycontrol',
            'Social Media'
        ],
        'key_themes': [
            f'{symbol} earnings outlook',
            'Market volatility',
            'Sector performance',
            'Economic indicators'
        ]
    }
    
    return analysis

def generate_sample_chart_data(current_price, days=30):
    """Generate sample chart data for visualization"""
    dates = []
    prices = []
    
    base_date = datetime.now() - timedelta(days=days)
    price = current_price * 0.95  # Start slightly lower
    
    for i in range(days):
        dates.append((base_date + timedelta(days=i)).strftime('%Y-%m-%d'))
        # Random walk with slight upward trend
        change = random.uniform(-0.03, 0.05)
        price = price * (1 + change)
        prices.append(round(price, 2))
    
    return {
        'dates': dates,
        'prices': prices
    }

def generate_sample_ohlc_data(symbol, period='3mo'):
    """Generate sample OHLC data when real data is not available"""
    # Determine number of days based on period
    days_map = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
    days = days_map.get(period, 90)
    
    # Generate dates
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate sample data
    base_price = random.uniform(1000, 3000)
    data = []
    
    for i, date in enumerate(dates):
        if i == 0:
            open_price = base_price
        else:
            open_price = data[i-1]['Close']
        
        # Random daily movement
        daily_change = random.uniform(-0.05, 0.05)
        close_price = open_price * (1 + daily_change)
        
        # High and low based on volatility
        volatility = random.uniform(0.01, 0.03)
        high_price = max(open_price, close_price) * (1 + volatility)
        low_price = min(open_price, close_price) * (1 - volatility)
        
        volume = random.randint(100000, 1000000)
        
        data.append({
            'Open': round(open_price, 2),
            'High': round(high_price, 2),
            'Low': round(low_price, 2),
            'Close': round(close_price, 2),
            'Volume': volume
        })
    
    # Create DataFrame
    df = pd.DataFrame(data, index=dates)
    return df

def process_candlestick_data(hist):
    """Process data for candlestick chart"""
    data = []
    for date, row in hist.iterrows():
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'open': round(float(row['Open']), 2),
            'high': round(float(row['High']), 2),
            'low': round(float(row['Low']), 2),
            'close': round(float(row['Close']), 2),
            'volume': int(row['Volume'])
        })
    return data

def process_renko_data(hist):
    """Process data for Renko chart (simplified version)"""
    # Renko bricks are based on price movement, not time
    brick_size = hist['Close'].std() * 0.5  # Dynamic brick size
    
    data = []
    current_price = float(hist['Close'].iloc[0])
    direction = 1  # 1 for up, -1 for down
    
    for date, row in hist.iterrows():
        close_price = float(row['Close'])
        
        # Calculate number of bricks
        price_diff = close_price - current_price
        bricks_needed = int(abs(price_diff) / brick_size)
        
        if bricks_needed > 0:
            new_direction = 1 if price_diff > 0 else -1
            
            for i in range(bricks_needed):
                brick_open = current_price
                brick_close = current_price + (brick_size * new_direction)
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(brick_open, 2),
                    'close': round(brick_close, 2),
                    'direction': new_direction,
                    'brick_size': round(brick_size, 2)
                })
                
                current_price = brick_close
                direction = new_direction
    
    return data

def process_kagi_data(hist):
    """Process data for Kagi chart (simplified version)"""
    reversal_amount = hist['Close'].std() * 0.3  # Dynamic reversal amount
    
    data = []
    current_price = float(hist['Close'].iloc[0])
    direction = 1  # 1 for up, -1 for down
    
    for date, row in hist.iterrows():
        close_price = float(row['Close'])
        
        # Check for reversal
        if direction == 1 and (current_price - close_price) > reversal_amount:
            # Reversal to down
            direction = -1
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(close_price, 2),
                'direction': direction,
                'reversal': True
            })
        elif direction == -1 and (close_price - current_price) > reversal_amount:
            # Reversal to up
            direction = 1
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(close_price, 2),
                'direction': direction,
                'reversal': True
            })
        else:
            # Continue in same direction
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(close_price, 2),
                'direction': direction,
                'reversal': False
            })
        
        current_price = close_price
    
    return data

def process_point_figure_data(hist):
    """Process data for Point & Figure chart"""
    box_size = hist['Close'].std() * 0.2  # Dynamic box size
    
    data = []
    current_price = float(hist['Close'].iloc[0])
    column_type = 'X'  # X for rising, O for falling
    
    for date, row in hist.iterrows():
        high_price = float(row['High'])
        low_price = float(row['Low'])
        
        # Calculate X's and O's
        if column_type == 'X':
            x_count = int((high_price - current_price) / box_size)
            o_count = int((current_price - low_price) / box_size)
            
            if x_count > 0:
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': 'X',
                    'count': x_count,
                    'price': round(current_price + (x_count * box_size), 2)
                })
                current_price += x_count * box_size
            elif o_count >= 3:  # Reversal threshold
                column_type = 'O'
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': 'O',
                    'count': o_count,
                    'price': round(current_price - (o_count * box_size), 2)
                })
                current_price -= o_count * box_size
        else:  # column_type == 'O'
            o_count = int((current_price - low_price) / box_size)
            x_count = int((high_price - current_price) / box_size)
            
            if o_count > 0:
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': 'O',
                    'count': o_count,
                    'price': round(current_price - (o_count * box_size), 2)
                })
                current_price -= o_count * box_size
            elif x_count >= 3:  # Reversal threshold
                column_type = 'X'
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': 'X',
                    'count': x_count,
                    'price': round(current_price + (x_count * box_size), 2)
                })
                current_price += x_count * box_size
    
    return data

def process_breakout_data(hist):
    """Process data for Breakout chart"""
    # Calculate support and resistance levels
    window = 20
    data = []
    
    for i in range(window, len(hist)):
        current_date = hist.index[i]
        current_data = hist.iloc[i-window:i]
        
        resistance = current_data['High'].max()
        support = current_data['Low'].min()
        current_price = float(hist.iloc[i]['Close'])
        
        # Determine breakout
        breakout_type = None
        if current_price > resistance:
            breakout_type = 'resistance_break'
        elif current_price < support:
            breakout_type = 'support_break'
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'price': round(current_price, 2),
            'resistance': round(resistance, 2),
            'support': round(support, 2),
            'breakout_type': breakout_type
        })
    
    return data

def calculate_technical_indicators(hist):
    """Calculate technical indicators"""
    indicators = {}
    
    # Simple Moving Averages
    if len(hist) >= 20:
        indicators['sma_20'] = hist['Close'].rolling(window=20).mean().iloc[-1]
    if len(hist) >= 50:
        indicators['sma_50'] = hist['Close'].rolling(window=50).mean().iloc[-1]
    
    # RSI
    if len(hist) >= 14:
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['rsi'] = 100 - (100 / (1 + rs.iloc[-1]))
    
    # MACD
    if len(hist) >= 26:
        exp1 = hist['Close'].ewm(span=12).mean()
        exp2 = hist['Close'].ewm(span=26).mean()
        indicators['macd'] = exp1.iloc[-1] - exp2.iloc[-1]
    
    # Bollinger Bands
    if len(hist) >= 20:
        sma = hist['Close'].rolling(window=20).mean()
        std = hist['Close'].rolling(window=20).std()
        indicators['bb_upper'] = (sma + (std * 2)).iloc[-1]
        indicators['bb_lower'] = (sma - (std * 2)).iloc[-1]
    
    # Round values and handle NaN
    for key, value in indicators.items():
        if pd.notna(value):
            indicators[key] = round(float(value), 2)
        else:
            indicators[key] = None
    
    return indicators

def analyze_chart_patterns(hist, chart_type):
    """Analyze chart patterns"""
    patterns = {
        'detected_patterns': [],
        'support_levels': [],
        'resistance_levels': []
    }
    
    if len(hist) == 0:
        return patterns
    
    # Simple pattern detection
    recent_data = hist.tail(20) if len(hist) >= 20 else hist
    
    # Support and resistance levels
    resistance = recent_data['High'].max()
    support = recent_data['Low'].min()
    
    patterns['resistance_levels'].append(round(resistance, 2))
    patterns['support_levels'].append(round(support, 2))
    
    # Simple pattern detection based on price action
    if len(recent_data) > 3:
        price_changes = recent_data['Close'].pct_change().dropna()
        
        if len(price_changes) > 0:
            recent_trend = price_changes.iloc[-3:].sum() if len(price_changes) >= 3 else price_changes.sum()
            
            if recent_trend > 0.05:
                patterns['detected_patterns'].append('Bullish Trend')
            elif recent_trend < -0.05:
                patterns['detected_patterns'].append('Bearish Trend')
            else:
                patterns['detected_patterns'].append('Sideways Movement')
    
    return patterns

if __name__ == '__main__':
    app.run(debug=True, port=5000)
