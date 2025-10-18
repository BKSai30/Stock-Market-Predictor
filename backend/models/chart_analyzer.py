"""
Chart Analyzer for Stock Market Technical Analysis
Handles various chart types including Candlestick, Renko, Kagi, Point & Figure, and Breakout charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Dict, List, Any, Optional, Tuple
import ta
import os
from datetime import datetime
from config import Config
import io
import base64
from renko import Renko

logger = logging.getLogger(__name__)

class ChartAnalyzer:
    """
    Analyzes various types of financial charts and provides technical analysis
    """
    
    def __init__(self):
        self.config = Config()
        self.chart_cache = {}
        
    def initialize(self):
        """Initialize chart analyzer"""
        try:
            logger.info("Initializing chart analyzer...")
            # Test basic functionality
            test_data = pd.DataFrame({
                'Open': [100, 101, 102, 103],
                'High': [105, 106, 107, 108],
                'Low': [99, 100, 101, 102],
                'Close': [104, 105, 106, 107],
                'Volume': [1000, 1100, 1200, 1300]
            })
            # Test if we can create a basic candlestick chart
            chart_data = self.generate_candlestick_data(test_data)
            logger.info("Chart analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing chart analyzer: {str(e)}")
    
    def analyze_all_charts(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze all supported chart types and return comprehensive analysis
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with analysis results from all chart types
        """
        try:
            analysis = {}
            
            # Candlestick analysis
            analysis['candlestick'] = self.analyze_candlestick_patterns(data)
            
            # Renko analysis
            analysis['renko'] = self.analyze_renko_patterns(data)
            
            # Kagi analysis
            analysis['kagi'] = self.analyze_kagi_patterns(data)
            
            # Point & Figure analysis
            analysis['point_figure'] = self.analyze_point_figure_patterns(data)
            
            # Breakout analysis
            analysis['breakout'] = self.analyze_breakout_patterns(data)
            
            # Technical indicators
            analysis['technical_indicators'] = self.calculate_technical_indicators(data)
            
            # Overall trend analysis
            analysis['trend_analysis'] = self.analyze_overall_trend(data)
            
            # Support and resistance levels
            analysis['support_resistance'] = self.find_support_resistance_levels(data)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive chart analysis: {str(e)}")
            return {}
    
    def generate_candlestick_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate candlestick chart data for frontend visualization
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with chart data in JSON format
        """
        try:
            # Prepare data for candlestick chart
            chart_data = []
            
            for index, row in data.iterrows():
                chart_data.append({
                    'x': index.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume']) if 'Volume' in row else 0
                })
            
            # Calculate moving averages for overlay
            data_with_ma = data.copy()
            data_with_ma['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
            data_with_ma['SMA_50'] = ta.trend.sma_indicator(data['Close'], window=50)
            data_with_ma['EMA_12'] = ta.trend.ema_indicator(data['Close'], window=12)
            
            # Add moving averages to chart data
            ma_data = []
            for index, row in data_with_ma.iterrows():
                ma_data.append({
                    'x': index.strftime('%Y-%m-%d'),
                    'sma_20': round(row['SMA_20'], 2) if not pd.isna(row['SMA_20']) else None,
                    'sma_50': round(row['SMA_50'], 2) if not pd.isna(row['SMA_50']) else None,
                    'ema_12': round(row['EMA_12'], 2) if not pd.isna(row['EMA_12']) else None
                })
            
            return {
                'type': 'candlestick',
                'data': chart_data,
                'moving_averages': ma_data,
                'title': 'Candlestick Chart with Moving Averages'
            }
            
        except Exception as e:
            logger.error(f"Error generating candlestick data: {str(e)}")
            return {'type': 'candlestick', 'data': [], 'error': str(e)}
    
    def generate_renko_data(self, data: pd.DataFrame, brick_size: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate Renko chart data
        
        Args:
            data: OHLCV DataFrame
            brick_size: Size of Renko bricks (auto-calculated if None)
            
        Returns:
            Dictionary with Renko chart data
        """
        try:
            # Calculate brick size based on ATR if not provided
            if brick_size is None:
                atr = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], window=14)
                brick_size = round(atr.iloc[-1], 2)
            
            # Create Renko chart using the renko library
            renko = Renko(brick_size=brick_size, data=data['Close'])
            renko.create_renko()
            
            # Convert Renko bricks to chart data
            renko_data = []
            for i, brick in enumerate(renko.bricks):
                brick_type = brick.get('type', 'unknown')
                color = 'green' if brick_type == 'up' else 'red' if brick_type == 'down' else 'gray'
                
                renko_data.append({
                    'x': i,
                    'open': round(brick.get('open', 0), 2),
                    'close': round(brick.get('close', 0), 2),
                    'type': brick_type,
                    'color': color
                })
            
            return {
                'type': 'renko',
                'data': renko_data,
                'brick_size': brick_size,
                'title': f'Renko Chart (Brick Size: {brick_size})'
            }
            
        except Exception as e:
            logger.error(f"Error generating Renko data: {str(e)}")
            return {'type': 'renko', 'data': [], 'error': str(e)}
    
    def generate_kagi_data(self, data: pd.DataFrame, reversal_amount: float = 0.02) -> Dict[str, Any]:
        """
        Generate Kagi chart data
        
        Args:
            data: OHLCV DataFrame
            reversal_amount: Reversal percentage (default 2%)
            
        Returns:
            Dictionary with Kagi chart data
        """
        try:
            prices = data['Close'].values
            kagi_data = []
            
            if len(prices) < 2:
                return {'type': 'kagi', 'data': [], 'error': 'Insufficient data'}
            
            # Initialize Kagi chart
            current_price = prices[0]
            current_direction = None
            last_extreme = current_price
            yang_line = False  # Thick line (bullish)
            
            kagi_points = [(0, current_price, 'start')]
            
            for i, price in enumerate(prices[1:], 1):
                price_change = abs(price - last_extreme) / last_extreme
                
                if current_direction is None:
                    # First movement
                    if price > current_price:
                        current_direction = 'up'
                        yang_line = True
                    else:
                        current_direction = 'down'
                        yang_line = False
                    
                    kagi_points.append((i, price, 'yang' if yang_line else 'yin'))
                    last_extreme = price
                    current_price = price
                
                elif current_direction == 'up':
                    if price > last_extreme:
                        # Continue up
                        kagi_points.append((i, price, 'yang' if yang_line else 'yin'))
                        last_extreme = price
                        current_price = price
                    elif price_change >= reversal_amount:
                        # Reversal down
                        current_direction = 'down'
                        yang_line = not yang_line
                        kagi_points.append((i, price, 'yang' if yang_line else 'yin'))
                        last_extreme = price
                        current_price = price
                
                elif current_direction == 'down':
                    if price < last_extreme:
                        # Continue down
                        kagi_points.append((i, price, 'yang' if yang_line else 'yin'))
                        last_extreme = price
                        current_price = price
                    elif price_change >= reversal_amount:
                        # Reversal up
                        current_direction = 'up'
                        yang_line = not yang_line
                        kagi_points.append((i, price, 'yang' if yang_line else 'yin'))
                        last_extreme = price
                        current_price = price
            
            # Convert to chart data
            for i, (x, y, line_type) in enumerate(kagi_points):
                kagi_data.append({
                    'x': x,
                    'y': round(y, 2),
                    'type': line_type,
                    'thickness': 'thick' if line_type == 'yang' else 'thin'
                })
            
            return {
                'type': 'kagi',
                'data': kagi_data,
                'reversal_amount': reversal_amount,
                'title': f'Kagi Chart (Reversal: {reversal_amount*100}%)'
            }
            
        except Exception as e:
            logger.error(f"Error generating Kagi data: {str(e)}")
            return {'type': 'kagi', 'data': [], 'error': str(e)}
    
    def generate_point_figure_data(self, data: pd.DataFrame, box_size: Optional[float] = None, reversal_amount: int = 3) -> Dict[str, Any]:
        """
        Generate Point & Figure chart data
        
        Args:
            data: OHLCV DataFrame
            box_size: Size of each box (auto-calculated if None)
            reversal_amount: Number of boxes for reversal
            
        Returns:
            Dictionary with Point & Figure chart data
        """
        try:
            prices = data['Close'].values
            
            # Calculate box size based on ATR if not provided
            if box_size is None:
                atr = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], window=14)
                box_size = round(atr.iloc[-1] * 0.5, 2)  # Half of ATR
            
            if box_size <= 0:
                box_size = 1.0
            
            pf_data = []
            columns = []
            
            if len(prices) < 2:
                return {'type': 'point_figure', 'data': [], 'error': 'Insufficient data'}
            
            # Initialize first column
            start_price = prices[0]
            start_box = int(start_price / box_size)
            current_column = 0
            current_direction = None
            current_high = start_box
            current_low = start_box
            
            for price in prices[1:]:
                current_box = int(price / box_size)
                
                if current_direction is None:
                    # Determine initial direction
                    if current_box > start_box:
                        current_direction = 'X'
                        current_high = current_box
                        # Add X's from start to current
                        for box in range(start_box, current_box + 1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'X',
                                'price': box * box_size
                            })
                    elif current_box < start_box:
                        current_direction = 'O'
                        current_low = current_box
                        # Add O's from start to current
                        for box in range(start_box, current_box - 1, -1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'O',
                                'price': box * box_size
                            })
                
                elif current_direction == 'X':
                    if current_box > current_high:
                        # Add more X's
                        for box in range(current_high + 1, current_box + 1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'X',
                                'price': box * box_size
                            })
                        current_high = current_box
                    elif current_box <= current_high - reversal_amount:
                        # Reversal to O's
                        current_column += 1
                        current_direction = 'O'
                        current_low = current_box
                        for box in range(current_high - 1, current_box - 1, -1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'O',
                                'price': box * box_size
                            })
                
                elif current_direction == 'O':
                    if current_box < current_low:
                        # Add more O's
                        for box in range(current_low - 1, current_box - 1, -1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'O',
                                'price': box * box_size
                            })
                        current_low = current_box
                    elif current_box >= current_low + reversal_amount:
                        # Reversal to X's
                        current_column += 1
                        current_direction = 'X'
                        current_high = current_box
                        for box in range(current_low + 1, current_box + 1):
                            pf_data.append({
                                'column': current_column,
                                'box': box,
                                'symbol': 'X',
                                'price': box * box_size
                            })
            
            return {
                'type': 'point_figure',
                'data': pf_data,
                'box_size': box_size,
                'reversal_amount': reversal_amount,
                'title': f'Point & Figure Chart (Box: {box_size}, Reversal: {reversal_amount})'
            }
            
        except Exception as e:
            logger.error(f"Error generating Point & Figure data: {str(e)}")
            return {'type': 'point_figure', 'data': [], 'error': str(e)}
    
    def analyze_candlestick_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze candlestick patterns for trading signals
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with pattern analysis
        """
        try:
            patterns = {}
            
            # Doji patterns
            patterns['doji'] = self._detect_doji_patterns(data)
            
            # Hammer patterns
            patterns['hammer'] = self._detect_hammer_patterns(data)
            
            # Engulfing patterns
            patterns['engulfing'] = self._detect_engulfing_patterns(data)
            
            # Morning/Evening Star patterns
            patterns['star'] = self._detect_star_patterns(data)
            
            # Overall pattern strength
            bullish_signals = sum(1 for p in patterns.values() if p.get('signal') == 'bullish')
            bearish_signals = sum(1 for p in patterns.values() if p.get('signal') == 'bearish')
            
            patterns['summary'] = {
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals,
                'overall_signal': 'bullish' if bullish_signals > bearish_signals else 'bearish' if bearish_signals > bullish_signals else 'neutral'
            }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing candlestick patterns: {str(e)}")
            return {}
    
    def analyze_renko_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Renko chart patterns
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with Renko analysis
        """
        try:
            # Create Renko chart
            atr = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], window=14)
            brick_size = round(atr.iloc[-1], 2)
            
            renko = Renko(brick_size=brick_size, data=data['Close'])
            renko.create_renko()
            
            # Analyze Renko patterns
            bricks = renko.bricks
            if len(bricks) < 3:
                return {'trend': 'insufficient_data'}
            
            # Count consecutive bricks
            consecutive_up = 0
            consecutive_down = 0
            
            for brick in reversed(bricks):
                if brick.get('type') == 'up':
                    consecutive_up += 1
                    break
                elif brick.get('type') == 'down':
                    consecutive_down += 1
                    break
            
            # Trend analysis
            recent_bricks = bricks[-10:] if len(bricks) >= 10 else bricks
            up_count = sum(1 for brick in recent_bricks if brick.get('type') == 'up')
            down_count = sum(1 for brick in recent_bricks if brick.get('type') == 'down')
            
            trend = 'bullish' if up_count > down_count else 'bearish' if down_count > up_count else 'neutral'
            trend_strength = abs(up_count - down_count) / len(recent_bricks) * 100
            
            return {
                'trend': trend,
                'trend_strength': round(trend_strength, 2),
                'consecutive_up': consecutive_up,
                'consecutive_down': consecutive_down,
                'brick_size': brick_size,
                'total_bricks': len(bricks)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Renko patterns: {str(e)}")
            return {'trend': 'error', 'error': str(e)}
    
    def analyze_kagi_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Kagi chart patterns
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with Kagi analysis
        """
        try:
            # Generate Kagi data first
            kagi_result = self.generate_kagi_data(data)
            kagi_data = kagi_result.get('data', [])
            
            if not kagi_data:
                return {'trend': 'insufficient_data'}
            
            # Analyze Kagi patterns
            yang_count = sum(1 for point in kagi_data if point.get('type') == 'yang')
            yin_count = sum(1 for point in kagi_data if point.get('type') == 'yin')
            
            # Current line type
            current_line = kagi_data[-1].get('type', 'unknown') if kagi_data else 'unknown'
            
            # Trend analysis
            if yang_count > yin_count:
                trend = 'bullish'
            elif yin_count > yang_count:
                trend = 'bearish'
            else:
                trend = 'neutral'
            
            # Calculate trend strength
            total_lines = yang_count + yin_count
            trend_strength = abs(yang_count - yin_count) / total_lines * 100 if total_lines > 0 else 0
            
            return {
                'trend': trend,
                'trend_strength': round(trend_strength, 2),
                'current_line': current_line,
                'yang_lines': yang_count,
                'yin_lines': yin_count,
                'total_reversals': len(kagi_data)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Kagi patterns: {str(e)}")
            return {'trend': 'error', 'error': str(e)}
    
    def analyze_point_figure_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Point & Figure chart patterns
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with Point & Figure analysis
        """
        try:
            # Generate Point & Figure data
            pf_result = self.generate_point_figure_data(data)
            pf_data = pf_result.get('data', [])
            
            if not pf_data:
                return {'trend': 'insufficient_data'}
            
            # Count X's and O's
            x_count = sum(1 for point in pf_data if point.get('symbol') == 'X')
            o_count = sum(1 for point in pf_data if point.get('symbol') == 'O')
            
            # Get current column type
            max_column = max(point.get('column', 0) for point in pf_data)
            current_column_data = [point for point in pf_data if point.get('column') == max_column]
            current_symbol = current_column_data[0].get('symbol', 'unknown') if current_column_data else 'unknown'
            
            # Trend analysis
            if x_count > o_count:
                trend = 'bullish'
            elif o_count > x_count:
                trend = 'bearish'
            else:
                trend = 'neutral'
            
            # Calculate trend strength
            total_symbols = x_count + o_count
            trend_strength = abs(x_count - o_count) / total_symbols * 100 if total_symbols > 0 else 0
            
            return {
                'trend': trend,
                'trend_strength': round(trend_strength, 2),
                'current_symbol': current_symbol,
                'x_count': x_count,
                'o_count': o_count,
                'total_columns': max_column + 1,
                'box_size': pf_result.get('box_size', 0)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Point & Figure patterns: {str(e)}")
            return {'trend': 'error', 'error': str(e)}
    
    def analyze_breakout_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze breakout patterns
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with breakout analysis
        """
        try:
            # Find support and resistance levels
            support_resistance = self.find_support_resistance_levels(data)
            
            current_price = data['Close'].iloc[-1]
            recent_high = data['High'].iloc[-20:].max()
            recent_low = data['Low'].iloc[-20:].min()
            
            # Volume analysis
            avg_volume = data['Volume'].mean()
            recent_volume = data['Volume'].iloc[-5:].mean()
            volume_surge = recent_volume > avg_volume * 1.5
            
            # Breakout detection
            resistance_levels = support_resistance.get('resistance', [])
            support_levels = support_resistance.get('support', [])
            
            upward_breakout = False
            downward_breakout = False
            
            # Check for upward breakout
            for resistance in resistance_levels:
                if current_price > resistance * 1.02:  # 2% above resistance
                    upward_breakout = True
                    break
            
            # Check for downward breakout
            for support in support_levels:
                if current_price < support * 0.98:  # 2% below support
                    downward_breakout = True
                    break
            
            # Price volatility
            volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
            
            breakout_signal = False
            breakout_direction = 'none'
            
            if upward_breakout and volume_surge:
                breakout_signal = True
                breakout_direction = 'upward'
            elif downward_breakout and volume_surge:
                breakout_signal = True
                breakout_direction = 'downward'
            
            return {
                'breakout_signal': breakout_signal,
                'breakout_direction': breakout_direction,
                'volume_surge': volume_surge,
                'current_price': round(current_price, 2),
                'recent_high': round(recent_high, 2),
                'recent_low': round(recent_low, 2),
                'volatility': round(volatility, 2),
                'resistance_levels': [round(r, 2) for r in resistance_levels[:3]],
                'support_levels': [round(s, 2) for s in support_levels[:3]]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing breakout patterns: {str(e)}")
            return {'breakout_signal': False, 'error': str(e)}
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate various technical indicators
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with technical indicators
        """
        try:
            indicators = {}
            
            # Moving Averages
            indicators['sma_20'] = round(ta.trend.sma_indicator(data['Close'], window=20).iloc[-1], 2)
            indicators['sma_50'] = round(ta.trend.sma_indicator(data['Close'], window=50).iloc[-1], 2)
            indicators['ema_12'] = round(ta.trend.ema_indicator(data['Close'], window=12).iloc[-1], 2)
            indicators['ema_26'] = round(ta.trend.ema_indicator(data['Close'], window=26).iloc[-1], 2)
            
            # RSI
            indicators['rsi'] = round(ta.momentum.rsi(data['Close'], window=14).iloc[-1], 2)
            
            # MACD
            macd_line = ta.trend.macd_diff(data['Close'])
            macd_signal = ta.trend.macd_signal(data['Close'])
            indicators['macd'] = round(macd_line.iloc[-1], 4)
            indicators['macd_signal'] = round(macd_signal.iloc[-1], 4)
            indicators['macd_histogram'] = round(macd_line.iloc[-1] - macd_signal.iloc[-1], 4)
            
            # Bollinger Bands
            bb_high = ta.volatility.bollinger_hband(data['Close'])
            bb_low = ta.volatility.bollinger_lband(data['Close'])
            indicators['bb_upper'] = round(bb_high.iloc[-1], 2)
            indicators['bb_lower'] = round(bb_low.iloc[-1], 2)
            indicators['bb_width'] = round((bb_high.iloc[-1] - bb_low.iloc[-1]) / data['Close'].iloc[-1] * 100, 2)
            
            # ATR
            indicators['atr'] = round(ta.volatility.average_true_range(data['High'], data['Low'], data['Close']).iloc[-1], 2)
            
            # Stochastic
            stoch_k = ta.momentum.stoch(data['High'], data['Low'], data['Close'])
            stoch_d = ta.momentum.stoch_signal(data['High'], data['Low'], data['Close'])
            indicators['stoch_k'] = round(stoch_k.iloc[-1], 2)
            indicators['stoch_d'] = round(stoch_d.iloc[-1], 2)
            
            # Volume indicators
            indicators['volume_sma'] = round(ta.volume.volume_sma(data['Close'], data['Volume']).iloc[-1], 0)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            return {}
    
    def analyze_overall_trend(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze overall trend across different timeframes
        
        Args:
            data: OHLCV DataFrame
            
        Returns:
            Dictionary with trend analysis
        """
        try:
            current_price = data['Close'].iloc[-1]
            
            # Short-term trend (5 days)
            short_term_start = data['Close'].iloc[-5] if len(data) >= 5 else data['Close'].iloc[0]
            short_term_change = (current_price - short_term_start) / short_term_start * 100
            
            # Medium-term trend (20 days)
            medium_term_start = data['Close'].iloc[-20] if len(data) >= 20 else data['Close'].iloc[0]
            medium_term_change = (current_price - medium_term_start) / medium_term_start * 100
            
            # Long-term trend (50 days)
            long_term_start = data['Close'].iloc[-50] if len(data) >= 50 else data['Close'].iloc[0]
            long_term_change = (current_price - long_term_start) / long_term_start * 100
            
            # Moving average trends
            sma_20 = ta.trend.sma_indicator(data['Close'], window=20).iloc[-1]
            sma_50 = ta.trend.sma_indicator(data['Close'], window=50).iloc[-1]
            
            ma_trend = 'bullish' if current_price > sma_20 > sma_50 else 'bearish' if current_price < sma_20 < sma_50 else 'neutral'
            
            # Overall trend classification
            def classify_trend(change):
                if change > 5:
                    return 'strong_bullish'
                elif change > 2:
                    return 'bullish'
                elif change > -2:
                    return 'neutral'
                elif change > -5:
                    return 'bearish'
                else:
                    return 'strong_bearish'
            
            return {
                'short_term': {
                    'trend': classify_trend(short_term_change),
                    'change_percent': round(short_term_change, 2)
                },
                'medium_term': {
                    'trend': classify_trend(medium_term_change),
                    'change_percent': round(medium_term_change, 2)
                },
                'long_term': {
                    'trend': classify_trend(long_term_change),
                    'change_percent': round(long_term_change, 2)
                },
                'moving_average_trend': ma_trend,
                'current_price': round(current_price, 2),
                'price_vs_sma20': round((current_price / sma_20 - 1) * 100, 2),
                'price_vs_sma50': round((current_price / sma_50 - 1) * 100, 2)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing overall trend: {str(e)}")
            return {}
    
    def find_support_resistance_levels(self, data: pd.DataFrame, window: int = 20) -> Dict[str, List[float]]:
        """
        Find support and resistance levels using pivot points
        
        Args:
            data: OHLCV DataFrame
            window: Window size for pivot detection
            
        Returns:
            Dictionary with support and resistance levels
        """
        try:
            highs = data['High'].values
            lows = data['Low'].values
            
            # Find pivot highs (resistance)
            resistance_levels = []
            for i in range(window, len(highs) - window):
                if highs[i] == max(highs[i-window:i+window+1]):
                    resistance_levels.append(highs[i])
            
            # Find pivot lows (support)
            support_levels = []
            for i in range(window, len(lows) - window):
                if lows[i] == min(lows[i-window:i+window+1]):
                    support_levels.append(lows[i])
            
            # Remove duplicates and sort
            resistance_levels = sorted(list(set(resistance_levels)), reverse=True)
            support_levels = sorted(list(set(support_levels)))
            
            # Keep only the most relevant levels (top 5 each)
            resistance_levels = resistance_levels[:5]
            support_levels = support_levels[-5:]
            
            return {
                'resistance': resistance_levels,
                'support': support_levels
            }
            
        except Exception as e:
            logger.error(f"Error finding support/resistance levels: {str(e)}")
            return {'resistance': [], 'support': []}
    
    def _detect_doji_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect Doji candlestick patterns"""
        try:
            # Simple Doji detection
            recent_data = data.tail(5)
            body_size = abs(recent_data['Close'] - recent_data['Open'])
            candle_range = recent_data['High'] - recent_data['Low']
            
            doji_threshold = 0.1  # 10% of the candle range
            doji_count = sum(body_size < candle_range * doji_threshold)
            
            signal = 'neutral' if doji_count > 0 else 'none'
            
            return {
                'pattern': 'doji',
                'signal': signal,
                'strength': min(doji_count / 5 * 100, 100),
                'count': doji_count
            }
        except Exception as e:
            return {'pattern': 'doji', 'signal': 'none', 'error': str(e)}
    
    def _detect_hammer_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect Hammer candlestick patterns"""
        try:
            recent_data = data.tail(3)
            
            hammer_signals = []
            for _, row in recent_data.iterrows():
                body = abs(row['Close'] - row['Open'])
                lower_shadow = min(row['Open'], row['Close']) - row['Low']
                upper_shadow = row['High'] - max(row['Open'], row['Close'])
                
                # Hammer criteria: long lower shadow, small body, minimal upper shadow
                if lower_shadow > body * 2 and upper_shadow < body * 0.5:
                    hammer_signals.append('bullish')
                elif upper_shadow > body * 2 and lower_shadow < body * 0.5:
                    hammer_signals.append('bearish')
            
            signal = 'bullish' if 'bullish' in hammer_signals else 'bearish' if 'bearish' in hammer_signals else 'none'
            
            return {
                'pattern': 'hammer',
                'signal': signal,
                'strength': len(hammer_signals) / 3 * 100,
                'count': len(hammer_signals)
            }
        except Exception as e:
            return {'pattern': 'hammer', 'signal': 'none', 'error': str(e)}
    
    def _detect_engulfing_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect Engulfing candlestick patterns"""
        try:
            if len(data) < 2:
                return {'pattern': 'engulfing', 'signal': 'none'}
            
            recent_data = data.tail(2)
            prev_candle = recent_data.iloc[0]
            curr_candle = recent_data.iloc[1]
            
            # Bullish engulfing
            if (prev_candle['Close'] < prev_candle['Open'] and  # Previous red candle
                curr_candle['Close'] > curr_candle['Open'] and  # Current green candle
                curr_candle['Open'] < prev_candle['Close'] and  # Opens below previous close
                curr_candle['Close'] > prev_candle['Open']):    # Closes above previous open
                signal = 'bullish'
            
            # Bearish engulfing
            elif (prev_candle['Close'] > prev_candle['Open'] and  # Previous green candle
                  curr_candle['Close'] < curr_candle['Open'] and  # Current red candle
                  curr_candle['Open'] > prev_candle['Close'] and  # Opens above previous close
                  curr_candle['Close'] < prev_candle['Open']):    # Closes below previous open
                signal = 'bearish'
            else:
                signal = 'none'
            
            return {
                'pattern': 'engulfing',
                'signal': signal,
                'strength': 80 if signal != 'none' else 0
            }
        except Exception as e:
            return {'pattern': 'engulfing', 'signal': 'none', 'error': str(e)}
    
    def _detect_star_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect Morning/Evening Star patterns"""
        try:
            if len(data) < 3:
                return {'pattern': 'star', 'signal': 'none'}
            
            recent_data = data.tail(3)
            candle1, candle2, candle3 = recent_data.iloc[0], recent_data.iloc[1], recent_data.iloc[2]
            
            # Morning Star (bullish)
            if (candle1['Close'] < candle1['Open'] and  # First candle is red
                abs(candle2['Close'] - candle2['Open']) < abs(candle1['Close'] - candle1['Open']) * 0.5 and  # Second candle is small
                candle3['Close'] > candle3['Open'] and  # Third candle is green
                candle3['Close'] > (candle1['Open'] + candle1['Close']) / 2):  # Third closes above first's midpoint
                signal = 'bullish'
            
            # Evening Star (bearish)
            elif (candle1['Close'] > candle1['Open'] and  # First candle is green
                  abs(candle2['Close'] - candle2['Open']) < abs(candle1['Close'] - candle1['Open']) * 0.5 and  # Second candle is small
                  candle3['Close'] < candle3['Open'] and  # Third candle is red
                  candle3['Close'] < (candle1['Open'] + candle1['Close']) / 2):  # Third closes below first's midpoint
                signal = 'bearish'
            else:
                signal = 'none'
            
            return {
                'pattern': 'star',
                'signal': signal,
                'strength': 85 if signal != 'none' else 0
            }
        except Exception as e:
            return {'pattern': 'star', 'signal': 'none', 'error': str(e)}
