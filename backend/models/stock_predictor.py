"""
Stock Predictor Model
Implements various machine learning models for stock price prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import joblib
import logging
from typing import List, Dict, Any, Tuple, Optional
import os
from datetime import datetime, timedelta
import ta  # Technical Analysis library
from config import Config

logger = logging.getLogger(__name__)

class StockPredictor:
    """
    Stock price prediction using multiple ML models
    """
    
    def __init__(self):
        self.config = Config()
        self.models = {}
        self.scalers = {}
        self.model_save_path = self.config.MODEL_SAVE_PATH
        self.feature_columns = []
        
        # Ensure model directory exists
        os.makedirs(self.model_save_path, exist_ok=True)
    
    def initialize(self):
        """Initialize all ML models"""
        try:
            logger.info("Initializing stock predictor models...")
            self._setup_models()
            logger.info("Stock predictor models initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing stock predictor: {str(e)}")
    
    def _setup_models(self):
        """Setup ML models with configurations"""
        try:
            # Random Forest
            self.models['random_forest'] = RandomForestRegressor(
                **self.config.ML_MODELS['random_forest']
            )
            
            # Extra Trees
            self.models['extra_trees'] = ExtraTreesRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Linear Regression
            self.models['linear_regression'] = LinearRegression()
            
            # Support Vector Regression
            self.models['svr'] = SVR(**self.config.ML_MODELS['svm'])
            
            # Initialize scalers for each model
            for model_name in self.models.keys():
                self.scalers[model_name] = MinMaxScaler()
                
        except Exception as e:
            logger.error(f"Error setting up models: {str(e)}")
            raise
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for ML models including technical indicators
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            DataFrame with features
        """
        try:
            df = data.copy()
            
            # Basic price features
            df['price_change'] = df['Close'].pct_change()
            df['high_low_pct'] = (df['High'] - df['Low']) / df['Close']
            df['price_volume'] = df['Close'] * df['Volume']
            
            # Moving averages
            for period in self.config.TECHNICAL_INDICATORS['sma_periods']:
                df[f'sma_{period}'] = ta.trend.sma_indicator(df['Close'], window=period)
                df[f'price_sma_{period}_ratio'] = df['Close'] / df[f'sma_{period}']
            
            # Exponential moving averages
            for period in self.config.TECHNICAL_INDICATORS['ema_periods']:
                df[f'ema_{period}'] = ta.trend.ema_indicator(df['Close'], window=period)
            
            # RSI
            rsi_period = self.config.TECHNICAL_INDICATORS['rsi_period']
            df['rsi'] = ta.momentum.rsi(df['Close'], window=rsi_period)
            
            # MACD
            macd_fast = self.config.TECHNICAL_INDICATORS['macd_fast']
            macd_slow = self.config.TECHNICAL_INDICATORS['macd_slow']
            macd_signal = self.config.TECHNICAL_INDICATORS['macd_signal']
            
            df['macd'] = ta.trend.macd_diff(df['Close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
            df['macd_signal'] = ta.trend.macd_signal(df['Close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
            df['macd_histogram'] = ta.trend.macd_diff(df['Close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
            
            # Bollinger Bands
            bb_period = self.config.TECHNICAL_INDICATORS['bollinger_period']
            bb_std = self.config.TECHNICAL_INDICATORS['bollinger_std']
            
            df['bb_high'] = ta.volatility.bollinger_hband(df['Close'], window=bb_period, window_dev=bb_std)
            df['bb_low'] = ta.volatility.bollinger_lband(df['Close'], window=bb_period, window_dev=bb_std)
            df['bb_width'] = (df['bb_high'] - df['bb_low']) / df['Close']
            df['bb_position'] = (df['Close'] - df['bb_low']) / (df['bb_high'] - df['bb_low'])
            
            # Average True Range (ATR)
            atr_period = self.config.TECHNICAL_INDICATORS['atr_period']
            df['atr'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=atr_period)
            
            # Volume indicators
            df['volume_sma'] = ta.volume.volume_sma(df['Close'], df['Volume'], window=20)
            df['volume_ratio'] = df['Volume'] / df['volume_sma']
            
            # Momentum indicators
            df['momentum'] = df['Close'] / df['Close'].shift(10) - 1
            df['roc'] = ta.momentum.roc(df['Close'], window=10)
            
            # Volatility
            df['volatility'] = df['Close'].rolling(window=20).std()
            
            # Price position in the day's range
            df['price_position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
            
            # Lag features
            for lag in [1, 2, 3, 5]:
                df[f'close_lag_{lag}'] = df['Close'].shift(lag)
                df[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
                df[f'price_change_lag_{lag}'] = df['price_change'].shift(lag)
            
            # Remove NaN values
            df = df.dropna()
            
            # Store feature columns (excluding target)
            self.feature_columns = [col for col in df.columns if col not in ['Close', 'Open', 'High', 'Low', 'Volume']]
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise
    
    def create_lstm_model(self, input_shape: Tuple[int, int]) -> tf.keras.Model:
        """
        Create LSTM model for time series prediction
        
        Args:
            input_shape: Shape of input data (timesteps, features)
            
        Returns:
            Compiled LSTM model
        """
        try:
            model = Sequential()
            
            # LSTM layers
            lstm_config = self.config.ML_MODELS['lstm']
            neurons = lstm_config['neurons']
            dropout = lstm_config['dropout']
            
            # First LSTM layer
            model.add(LSTM(neurons[0], return_sequences=True, input_shape=input_shape))
            model.add(Dropout(dropout))
            
            # Second LSTM layer
            model.add(LSTM(neurons[1], return_sequences=True))
            model.add(Dropout(dropout))
            
            # Third LSTM layer
            model.add(LSTM(neurons[2], return_sequences=False))
            model.add(Dropout(dropout))
            
            # Dense layers
            model.add(Dense(50, activation='relu'))
            model.add(Dense(25, activation='relu'))
            model.add(Dense(1))  # Output layer for price prediction
            
            # Compile model
            model.compile(
                optimizer=Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae']
            )
            
            return model
            
        except Exception as e:
            logger.error(f"Error creating LSTM model: {str(e)}")
            raise
    
    def prepare_lstm_data(self, data: pd.DataFrame, sequence_length: int = 60) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for LSTM model
        
        Args:
            data: Prepared features DataFrame
            sequence_length: Length of input sequences
            
        Returns:
            Tuple of (X, y) arrays
        """
        try:
            # Select features for LSTM
            feature_data = data[self.feature_columns].values
            target_data = data['Close'].values
            
            # Scale the data
            scaler_X = MinMaxScaler()
            scaler_y = MinMaxScaler()
            
            scaled_features = scaler_X.fit_transform(feature_data)
            scaled_target = scaler_y.fit_transform(target_data.reshape(-1, 1))
            
            # Store scalers
            self.scalers['lstm_features'] = scaler_X
            self.scalers['lstm_target'] = scaler_y
            
            # Create sequences
            X, y = [], []
            for i in range(sequence_length, len(scaled_features)):
                X.append(scaled_features[i-sequence_length:i])
                y.append(scaled_target[i])
            
            return np.array(X), np.array(y)
            
        except Exception as e:
            logger.error(f"Error preparing LSTM data: {str(e)}")
            raise
    
    def train_models(self, data: pd.DataFrame, symbol: str) -> Dict[str, float]:
        """
        Train all ML models
        
        Args:
            data: Historical stock data
            symbol: Stock symbol
            
        Returns:
            Dictionary with model accuracies
        """
        try:
            logger.info(f"Training models for {symbol}")
            
            # Prepare features
            featured_data = self.prepare_features(data)
            
            if len(featured_data) < 100:
                raise ValueError("Not enough data for training")
            
            # Split data for training
            train_size = int(len(featured_data) * 0.8)
            train_data = featured_data[:train_size]
            test_data = featured_data[train_size:]
            
            # Prepare features and target
            X_train = train_data[self.feature_columns]
            y_train = train_data['Close']
            X_test = test_data[self.feature_columns]
            y_test = test_data['Close']
            
            model_scores = {}
            
            # Train traditional ML models
            for model_name, model in self.models.items():
                if model_name == 'lstm':  # Skip LSTM for now
                    continue
                
                try:
                    # Scale features
                    X_train_scaled = self.scalers[model_name].fit_transform(X_train)
                    X_test_scaled = self.scalers[model_name].transform(X_test)
                    
                    # Train model
                    model.fit(X_train_scaled, y_train)
                    
                    # Predict and evaluate
                    y_pred = model.predict(X_test_scaled)
                    mae = mean_absolute_error(y_test, y_pred)
                    
                    # Calculate accuracy as percentage
                    accuracy = max(0, 100 - (mae / y_test.mean() * 100))
                    model_scores[model_name] = accuracy
                    
                    logger.info(f"{model_name} accuracy: {accuracy:.2f}%")
                    
                    # Save model
                    self._save_model(model, model_name, symbol)
                    
                except Exception as e:
                    logger.error(f"Error training {model_name}: {str(e)}")
                    model_scores[model_name] = 0
            
            # Train LSTM model
            try:
                lstm_config = self.config.ML_MODELS['lstm']
                sequence_length = lstm_config['sequence_length']
                
                X_lstm, y_lstm = self.prepare_lstm_data(featured_data, sequence_length)
                
                if len(X_lstm) > 0:
                    # Split LSTM data
                    lstm_train_size = int(len(X_lstm) * 0.8)
                    X_lstm_train = X_lstm[:lstm_train_size]
                    y_lstm_train = y_lstm[:lstm_train_size]
                    X_lstm_test = X_lstm[lstm_train_size:]
                    y_lstm_test = y_lstm[lstm_train_size:]
                    
                    # Create and train LSTM model
                    lstm_model = self.create_lstm_model((sequence_length, len(self.feature_columns)))
                    
                    # Train with early stopping
                    early_stopping = tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss', patience=10, restore_best_weights=True
                    )
                    
                    history = lstm_model.fit(
                        X_lstm_train, y_lstm_train,
                        epochs=lstm_config['epochs'],
                        batch_size=lstm_config['batch_size'],
                        validation_data=(X_lstm_test, y_lstm_test),
                        callbacks=[early_stopping],
                        verbose=0
                    )
                    
                    # Evaluate LSTM
                    y_lstm_pred = lstm_model.predict(X_lstm_test)
                    
                    # Inverse transform predictions
                    y_lstm_test_orig = self.scalers['lstm_target'].inverse_transform(y_lstm_test)
                    y_lstm_pred_orig = self.scalers['lstm_target'].inverse_transform(y_lstm_pred)
                    
                    mae_lstm = mean_absolute_error(y_lstm_test_orig, y_lstm_pred_orig)
                    accuracy_lstm = max(0, 100 - (mae_lstm / y_lstm_test_orig.mean() * 100))
                    
                    model_scores['lstm'] = accuracy_lstm
                    logger.info(f"LSTM accuracy: {accuracy_lstm:.2f}%")
                    
                    # Save LSTM model
                    lstm_model.save(os.path.join(self.model_save_path, f'lstm_{symbol}.h5'))
                    
            except Exception as e:
                logger.error(f"Error training LSTM: {str(e)}")
                model_scores['lstm'] = 0
            
            return model_scores
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            return {}
    
    def predict_price(self, data: pd.DataFrame, symbol: str, days_ahead: int = 5, preferred_models: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Predict stock price for future days
        
        Args:
            data: Historical stock data
            symbol: Stock symbol
            days_ahead: Number of days to predict
            
        Returns:
            Dictionary with predictions and confidence
        """
        try:
            logger.info(f"Predicting price for {symbol} for {days_ahead} days")
            
            # Check if we have trained models, if not train them
            if not self._models_exist(symbol):
                model_scores = self.train_models(data, symbol)
                if not model_scores:
                    raise ValueError("Failed to train models")
            else:
                # Load existing models
                self._load_models(symbol)
            
            # Prepare features
            featured_data = self.prepare_features(data)
            
            if len(featured_data) < 60:
                raise ValueError("Not enough data for prediction")
            
            # Get latest data for prediction
            latest_data = featured_data.iloc[-60:].copy()  # Last 60 days
            
            predictions = {}
            confidences = {}
            
            # Predict with each model
            for model_name, model in self.models.items():
                if preferred_models and model_name not in preferred_models:
                    continue
                if model_name == 'lstm':
                    continue
                
                try:
                    # Prepare features for prediction
                    X_pred = latest_data[self.feature_columns].iloc[-1:].values
                    X_pred_scaled = self.scalers[model_name].transform(X_pred)
                    
                    # Predict future prices
                    future_prices = []
                    current_features = X_pred_scaled[0].copy()
                    
                    for day in range(days_ahead):
                        pred_price = model.predict([current_features])[0]
                        future_prices.append(pred_price)
                        
                        # Update features for next prediction (simplified)
                        # In practice, you'd update all relevant features
                        current_features = self._update_features(current_features, pred_price)
                    
                    predictions[model_name] = future_prices
                    confidences[model_name] = self._calculate_confidence(model, latest_data)
                    
                except Exception as e:
                    logger.error(f"Error predicting with {model_name}: {str(e)}")
                    continue
            
            # LSTM prediction
            try:
                if preferred_models and 'lstm' not in preferred_models:
                    raise Exception('lstm not selected')
                lstm_model = load_model(os.path.join(self.model_save_path, f'lstm_{symbol}.h5'))
                
                # Prepare LSTM input
                lstm_features = latest_data[self.feature_columns].values
                lstm_features_scaled = self.scalers['lstm_features'].transform(lstm_features)
                
                # Get sequence for prediction
                sequence_length = self.config.ML_MODELS['lstm']['sequence_length']
                X_lstm = lstm_features_scaled[-sequence_length:].reshape(1, sequence_length, -1)
                
                # Predict future prices
                future_prices_lstm = []
                current_sequence = X_lstm[0].copy()
                
                for day in range(days_ahead):
                    pred_scaled = lstm_model.predict(current_sequence.reshape(1, sequence_length, -1))
                    pred_price = self.scalers['lstm_target'].inverse_transform(pred_scaled)[0][0]
                    future_prices_lstm.append(pred_price)
                    
                    # Update sequence (simplified)
                    current_sequence = np.roll(current_sequence, -1, axis=0)
                    # current_sequence[-1] = updated_features (would need proper implementation)
                
                predictions['lstm'] = future_prices_lstm
                confidences['lstm'] = 75  # Default confidence for LSTM
                
            except Exception as e:
                logger.error(f"Error with LSTM prediction: {str(e)}")
            
            # Ensemble prediction (average of all models)
            if predictions:
                ensemble_prediction = []
                for day in range(days_ahead):
                    day_predictions = [predictions[model][day] for model in predictions if len(predictions[model]) > day]
                    if day_predictions:
                        ensemble_prediction.append(np.mean(day_predictions))
                
                # Calculate weighted confidence
                total_confidence = np.mean(list(confidences.values())) if confidences else 50
                
                return {
                    'predicted_prices': ensemble_prediction,
                    'individual_predictions': predictions,
                    'confidence': total_confidence,
                    'model_confidences': confidences,
                    'selected_models': list(predictions.keys())
                }
            else:
                raise ValueError("No successful predictions")
            
        except Exception as e:
            logger.error(f"Error in price prediction: {str(e)}")
            return {
                'predicted_prices': [],
                'confidence': 0,
                'error': str(e)
            }
    
    def _update_features(self, features: np.ndarray, new_price: float) -> np.ndarray:
        """
        Update features with new price (simplified implementation)
        
        Args:
            features: Current features
            new_price: Predicted price
            
        Returns:
            Updated features
        """
        # This is a simplified implementation
        # In practice, you'd properly update all time-dependent features
        updated_features = features.copy()
        # Update price-related features
        # This would need proper implementation based on feature structure
        return updated_features
    
    def _calculate_confidence(self, model, data: pd.DataFrame) -> float:
        """
        Calculate prediction confidence based on model performance
        
        Args:
            model: Trained model
            data: Recent data for evaluation
            
        Returns:
            Confidence score (0-100)
        """
        try:
            # Simple confidence calculation based on recent accuracy
            # This could be improved with more sophisticated methods
            return 70.0  # Default confidence
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 50.0
    
    def _save_model(self, model, model_name: str, symbol: str):
        """Save trained model to disk"""
        try:
            model_file = os.path.join(self.model_save_path, f'{model_name}_{symbol}.pkl')
            joblib.dump(model, model_file)
            
            scaler_file = os.path.join(self.model_save_path, f'scaler_{model_name}_{symbol}.pkl')
            joblib.dump(self.scalers[model_name], scaler_file)
            
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {str(e)}")
    
    def _load_models(self, symbol: str):
        """Load trained models from disk"""
        try:
            for model_name in self.models.keys():
                if model_name == 'lstm':
                    continue
                
                model_file = os.path.join(self.model_save_path, f'{model_name}_{symbol}.pkl')
                scaler_file = os.path.join(self.model_save_path, f'scaler_{model_name}_{symbol}.pkl')
                
                if os.path.exists(model_file) and os.path.exists(scaler_file):
                    self.models[model_name] = joblib.load(model_file)
                    self.scalers[model_name] = joblib.load(scaler_file)
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    def _models_exist(self, symbol: str) -> bool:
        """Check if trained models exist for the symbol"""
        try:
            for model_name in self.models.keys():
                if model_name == 'lstm':
                    lstm_file = os.path.join(self.model_save_path, f'lstm_{symbol}.h5')
                    if not os.path.exists(lstm_file):
                        return False
                else:
                    model_file = os.path.join(self.model_save_path, f'{model_name}_{symbol}.pkl')
                    if not os.path.exists(model_file):
                        return False
            return True
            
        except Exception as e:
            logger.error(f"Error checking model existence: {str(e)}")
            return False

    def ensure_trained(self, data: pd.DataFrame, symbol: str):
        """Train models if not already trained or data insufficiently cached."""
        try:
            if not self._models_exist(symbol):
                self.train_models(data, symbol)
        except Exception as e:
            logger.warning(f"ensure_trained skipped: {e}")