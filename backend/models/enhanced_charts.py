# Enhanced Charts for Stock Market Technical Analysis
"""
Enhanced chart implementations including advanced technical analysis
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Dict, List, Any, Optional, Tuple
import ta
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedCharts:
    """
    Advanced chart implementations for technical analysis
    """
    
    def __init__(self):
        self.chart_cache = {}
        
    def create_advanced_candlestick(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Create advanced candlestick chart with volume and indicators
        """
        try:
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=(f'{symbol} - Price Action', 'Volume', 'RSI'),
                vertical_spacing=0.05,
                row_heights=[0.6, 0.2, 0.2]
            )
            
            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # Moving averages
            if len(data) >= 20:
                sma_20 = ta.trend.sma_indicator(data['Close'], window=20)
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=sma_20,
                        mode='lines',
                        name='SMA 20',
                        line=dict(color='orange', width=1)
                    ),
                    row=1, col=1
                )
            
            if len(data) >= 50:
                sma_50 = ta.trend.sma_indicator(data['Close'], window=50)
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=sma_50,
                        mode='lines',
                        name='SMA 50',
                        line=dict(color='blue', width=1)
                    ),
                    row=1, col=1
                )
            
            # Bollinger Bands
            if len(data) >= 20:
                bb_high = ta.volatility.bollinger_hband(data['Close'], window=20)
                bb_low = ta.volatility.bollinger_lband(data['Close'], window=20)
                
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=bb_high,
                        mode='lines',
                        name='BB Upper',
                        line=dict(color='gray', width=1, dash='dash'),
                        opacity=0.5
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=bb_low,
                        mode='lines',
                        name='BB Lower',
                        line=dict(color='gray', width=1, dash='dash'),
                        opacity=0.5,
                        fill='tonexty',
                        fillcolor='rgba(128,128,128,0.1)'
                    ),
                    row=1, col=1
                )
            
            # Volume bars
            colors = ['red' if data['Close'].iloc[i] < data['Open'].iloc[i] else 'green' 
                     for i in range(len(data))]
            
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # RSI
            if len(data) >= 14:
                rsi = ta.momentum.rsi(data['Close'], window=14)
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=rsi,
                        mode='lines',
                        name='RSI',
                        line=dict(color='purple', width=2)
                    ),
                    row=3, col=1
                )
                
                # RSI overbought/oversold lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
                fig.add_hline(y=50, line_dash="dot", line_color="gray", row=3, col=1)
            
            # Update layout
            fig.update_layout(
                title=f'{symbol} - Advanced Technical Analysis',
                xaxis_rangeslider_visible=False,
                height=800,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Update y-axis labels
            fig.update_yaxes(title_text="Price", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])
            
            return {
                'chart_data': fig.to_dict(),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating advanced candlestick chart: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_renko_chart(self, data: pd.DataFrame, symbol: str, brick_size: float = None) -> Dict[str, Any]:
        """
        Create Renko chart
        """
        try:
            if brick_size is None:
                # Calculate brick size based on ATR
                if len(data) >= 14:
                    atr = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], window=14)
                    brick_size = atr.iloc[-1] * 0.5
                else:
                    brick_size = data['Close'].std() * 0.1
            
            renko_data = self._calculate_renko_bricks(data['Close'], brick_size)
            
            fig = go.Figure()
            
            colors = ['green' if brick['direction'] == 1 else 'red' for brick in renko_data]
            
            fig.add_trace(
                go.Bar(
                    x=list(range(len(renko_data))),
                    y=[brick['size'] for brick in renko_data],
                    base=[brick['low'] for brick in renko_data],
                    marker_color=colors,
                    name='Renko Bricks',
                    width=0.8
                )
            )
            
            fig.update_layout(
                title=f'{symbol} - Renko Chart (Brick Size: {brick_size:.2f})',
                xaxis_title='Brick Number',
                yaxis_title='Price',
                height=600,
                showlegend=False
            )
            
            return {
                'chart_data': fig.to_dict(),
                'brick_size': brick_size,
                'total_bricks': len(renko_data),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating Renko chart: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_point_figure_chart(self, data: pd.DataFrame, symbol: str, 
                                  box_size: float = None, reversal_amount: int = 3) -> Dict[str, Any]:
        """
        Create Point & Figure chart
        """
        try:
            if box_size is None:
                if len(data) >= 14:
                    atr = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], window=14)
                    box_size = atr.iloc[-1] * 0.3
                else:
                    box_size = data['Close'].std() * 0.05
            
            pf_data = self._calculate_point_figure(data['Close'], box_size, reversal_amount)
            
            fig = go.Figure()
            
            # Plot X columns (bullish)
            x_columns = [(i, point) for i, point in enumerate(pf_data) if point['type'] == 'X']
            if x_columns:
                x_positions, x_points = zip(*x_columns)
                fig.add_trace(
                    go.Scatter(
                        x=list(x_positions),
                        y=[point['price'] for point in x_points],
                        mode='markers',
                        marker=dict(symbol='x', size=12, color='green', line=dict(width=2)),
                        name='X (Bullish)',
                        showlegend=True
                    )
                )
            
            # Plot O columns (bearish)
            o_columns = [(i, point) for i, point in enumerate(pf_data) if point['type'] == 'O']
            if o_columns:
                o_positions, o_points = zip(*o_columns)
                fig.add_trace(
                    go.Scatter(
                        x=list(o_positions),
                        y=[point['price'] for point in o_points],
                        mode='markers',
                        marker=dict(symbol='circle-open', size=12, color='red', line=dict(width=2)),
                        name='O (Bearish)',
                        showlegend=True
                    )
                )
            
            fig.update_layout(
                title=f'{symbol} - Point & Figure Chart (Box: {box_size:.2f}, Reversal: {reversal_amount})',
                xaxis_title='Column Number',
                yaxis_title='Price',
                height=600,
                showlegend=True
            )
            
            return {
                'chart_data': fig.to_dict(),
                'box_size': box_size,
                'reversal_amount': reversal_amount,
                'total_points': len(pf_data),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating Point & Figure chart: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_kagi_chart(self, data: pd.DataFrame, symbol: str, reversal_amount: float = 0.02) -> Dict[str, Any]:
        """
        Create Kagi chart
        """
        try:
            kagi_data = self._calculate_kagi_lines(data['Close'], reversal_amount)
            
            fig = go.Figure()
            
            # Plot Kagi lines
            for i, line in enumerate(kagi_data):
                color = 'green' if line['type'] == 'yang' else 'red'
                width = 3 if line['type'] == 'yang' else 1
                
                fig.add_trace(
                    go.Scatter(
                        x=[i, i+1],
                        y=[line['start'], line['end']],
                        mode='lines',
                        line=dict(color=color, width=width),
                        name=f"{'Yang' if line['type'] == 'yang' else 'Yin'} Line",
                        showlegend=i == 0,
                        legendgroup=line['type']
                    )
                )
            
            fig.update_layout(
                title=f'{symbol} - Kagi Chart (Reversal: {reversal_amount*100:.1f}%)',
                xaxis_title='Time Period',
                yaxis_title='Price',
                height=600,
                showlegend=True
            )
            
            return {
                'chart_data': fig.to_dict(),
                'reversal_amount': reversal_amount,
                'total_lines': len(kagi_data),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating Kagi chart: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_macd_chart(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Create MACD indicator chart
        """
        try:
            if len(data) < 26:
                raise ValueError("Insufficient data for MACD calculation")
            
            macd = ta.trend.macd_diff(data['Close'])
            macd_signal = ta.trend.macd_signal(data['Close'])
            macd_histogram = macd - macd_signal
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=(f'{symbol} - Price', 'MACD'),
                vertical_spacing=0.1,
                row_heights=[0.7, 0.3]
            )
            
            # Price chart
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
            
            # MACD line
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=macd,
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=2)
                ),
                row=2, col=1
            )
            
            # MACD signal line
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=macd_signal,
                    mode='lines',
                    name='Signal',
                    line=dict(color='red', width=2)
                ),
                row=2, col=1
            )
            
            # MACD histogram
            colors = ['green' if val >= 0 else 'red' for val in macd_histogram.fillna(0)]
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=macd_histogram,
                    name='Histogram',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'{symbol} - MACD Analysis',
                height=600,
                showlegend=True
            )
            
            fig.update_yaxes(title_text="Price", row=1, col=1)
            fig.update_yaxes(title_text="MACD", row=2, col=1)
            
            return {
                'chart_data': fig.to_dict(),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating MACD chart: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_renko_bricks(self, prices: pd.Series, brick_size: float) -> List[Dict]:
        """Calculate Renko bricks"""
        bricks = []
        current_price = float(prices.iloc[0])
        
        for price in prices[1:]:
            price_diff = price - current_price
            bricks_needed = int(abs(price_diff) / brick_size)
            
            if bricks_needed > 0:
                direction = 1 if price_diff > 0 else -1
                
                for _ in range(bricks_needed):
                    brick_low = current_price if direction == 1 else current_price - brick_size
                    brick_high = current_price + brick_size if direction == 1 else current_price
                    
                    bricks.append({
                        'low': brick_low,
                        'high': brick_high,
                        'size': brick_size,
                        'direction': direction
                    })
                    
                    current_price += brick_size * direction
        
        return bricks
    
    def _calculate_point_figure(self, prices: pd.Series, box_size: float, reversal_amount: int) -> List[Dict]:
        """Calculate Point & Figure data"""
        points = []
        current_price = float(prices.iloc[0])
        current_column = 'X'
        column_count = 0
        
        for price in prices[1:]:
            if current_column == 'X':
                # In X column (bullish)
                if price > current_price + box_size:
                    # Continue X column
                    boxes_up = int((price - current_price) / box_size)
                    for i in range(boxes_up):
                        points.append({
                            'type': 'X',
                            'price': current_price + (i + 1) * box_size,
                            'column': column_count
                        })
                    current_price = current_price + boxes_up * box_size
                elif price < current_price - (reversal_amount * box_size):
                    # Switch to O column
                    current_column = 'O'
                    column_count += 1
                    boxes_down = int((current_price - price) / box_size)
                    for i in range(min(boxes_down, reversal_amount)):
                        points.append({
                            'type': 'O',
                            'price': current_price - (i + 1) * box_size,
                            'column': column_count
                        })
                    current_price = current_price - min(boxes_down, reversal_amount) * box_size
            else:
                # In O column (bearish)
                if price < current_price - box_size:
                    # Continue O column
                    boxes_down = int((current_price - price) / box_size)
                    for i in range(boxes_down):
                        points.append({
                            'type': 'O',
                            'price': current_price - (i + 1) * box_size,
                            'column': column_count
                        })
                    current_price = current_price - boxes_down * box_size
                elif price > current_price + (reversal_amount * box_size):
                    # Switch to X column
                    current_column = 'X'
                    column_count += 1
                    boxes_up = int((price - current_price) / box_size)
                    for i in range(min(boxes_up, reversal_amount)):
                        points.append({
                            'type': 'X',
                            'price': current_price + (i + 1) * box_size,
                            'column': column_count
                        })
                    current_price = current_price + min(boxes_up, reversal_amount) * box_size
        
        return points
    
    def _calculate_kagi_lines(self, prices: pd.Series, reversal_amount: float) -> List[Dict]:
        """Calculate Kagi lines"""
        lines = []
        current_price = float(prices.iloc[0])
        current_direction = None
        yang_line = False
        
        for price in prices[1:]:
            price_change = abs(price - current_price) / current_price
            
            if current_direction is None:
                # First movement
                if price > current_price:
                    current_direction = 'up'
                    yang_line = True
                else:
                    current_direction = 'down'
                    yang_line = False
                
                lines.append({
                    'start': current_price,
                    'end': price,
                    'type': 'yang' if yang_line else 'yin'
                })
                current_price = price
                
            elif current_direction == 'up' and price_change >= reversal_amount and price < current_price:
                # Reversal down
                current_direction = 'down'
                yang_line = not yang_line
                lines.append({
                    'start': current_price,
                    'end': price,
                    'type': 'yang' if yang_line else 'yin'
                })
                current_price = price
                
            elif current_direction == 'down' and price_change >= reversal_amount and price > current_price:
                # Reversal up
                current_direction = 'up'
                yang_line = not yang_line
                lines.append({
                    'start': current_price,
                    'end': price,
                    'type': 'yang' if yang_line else 'yin'
                })
                current_price = price
                
            elif (current_direction == 'up' and price > current_price) or (current_direction == 'down' and price < current_price):
                # Continue in same direction
                if lines:
                    lines[-1]['end'] = price
                current_price = price
        
        return lines
