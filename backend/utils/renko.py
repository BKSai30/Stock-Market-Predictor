# utils/renko.py

"""
Renko Chart Implementation for Stock Market Analysis
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Renko:
    """
    Renko chart implementation for financial data analysis
    """
    
    def __init__(self, brick_size: Optional[float] = None, data: Optional[pd.Series] = None):
        """
        Initialize Renko chart
        
        Args:
            brick_size: Size of each brick (auto-calculated if None)
            data: Price data series
        """
        self.brick_size = brick_size
        self.data = data
        self.bricks = []
        self.current_price = None
        self.current_direction = None
        
    def create_renko(self, price_data: Optional[pd.Series] = None) -> List[Dict[str, Any]]:
        """
        Create Renko bricks from price data
        
        Args:
            price_data: Price data series (uses self.data if None)
            
        Returns:
            List of Renko bricks
        """
        try:
            if price_data is not None:
                self.data = price_data
                
            if self.data is None or len(self.data) == 0:
                logger.warning("No price data provided for Renko chart")
                return []
            
            # Calculate brick size if not provided
            if self.brick_size is None:
                self.brick_size = self._calculate_brick_size()
            
            # Initialize with first price
            prices = self.data.values if hasattr(self.data, 'values') else self.data
            self.current_price = float(prices[0])
            
            # Create bricks
            for price in prices[1:]:
                self._process_price(float(price))
            
            return self.bricks
            
        except Exception as e:
            logger.error(f"Error creating Renko chart: {str(e)}")
            return []
    
    def _calculate_brick_size(self) -> float:
        """
        Calculate optimal brick size based on price data
        
        Returns:
            Calculated brick size
        """
        try:
            if len(self.data) < 20:
                # Use 1% of average price for small datasets
                avg_price = self.data.mean()
                return avg_price * 0.01
            
            # Calculate Average True Range (ATR) for brick size
            high_low = self.data.rolling(2).apply(lambda x: abs(x.iloc[1] - x.iloc[0]), raw=False)
            atr = high_low.rolling(14).mean().iloc[-1]
            
            # Use ATR or 0.5% of current price, whichever is larger
            current_price = float(self.data.iloc[-1])
            min_brick_size = current_price * 0.005
            
            brick_size = max(atr, min_brick_size)
            
            # Round to reasonable precision
            if brick_size < 1:
                return round(brick_size, 4)
            elif brick_size < 10:
                return round(brick_size, 2)
            else:
                return round(brick_size, 1)
                
        except Exception as e:
            logger.warning(f"Error calculating brick size: {str(e)}")
            # Fallback to 1% of last price
            return float(self.data.iloc[-1]) * 0.01
    
    def _process_price(self, price: float):
        """
        Process a single price point and create bricks if needed
        
        Args:
            price: Current price
        """
        try:
            price_diff = price - self.current_price
            
            if abs(price_diff) < self.brick_size:
                # Price movement too small, no new brick
                return
            
            # Determine direction
            new_direction = 1 if price_diff > 0 else -1
            
            if self.current_direction is None:
                # First brick
                self.current_direction = new_direction
                self._create_brick(self.current_price, price, new_direction)
                self.current_price = self._round_to_brick(price, new_direction)
                
            elif self.current_direction == new_direction:
                # Same direction, create brick(s)
                bricks_count = int(abs(price_diff) / self.brick_size)
                
                for i in range(bricks_count):
                    brick_start = self.current_price
                    brick_end = self.current_price + (self.brick_size * new_direction)
                    self._create_brick(brick_start, brick_end, new_direction)
                    self.current_price = brick_end
                    
            else:
                # Direction change - need at least 2 bricks to reverse
                required_move = self.brick_size * 2
                
                if abs(price_diff) >= required_move:
                    # Reversal confirmed
                    self.current_direction = new_direction
                    bricks_count = int(abs(price_diff) / self.brick_size)
                    
                    for i in range(bricks_count):
                        brick_start = self.current_price
                        brick_end = self.current_price + (self.brick_size * new_direction)
                        self._create_brick(brick_start, brick_end, new_direction)
                        self.current_price = brick_end
                        
        except Exception as e:
            logger.warning(f"Error processing price {price}: {str(e)}")
    
    def _create_brick(self, start_price: float, end_price: float, direction: int):
        """
        Create a single Renko brick
        
        Args:
            start_price: Brick starting price
            end_price: Brick ending price
            direction: Brick direction (1 for up, -1 for down)
        """
        brick_type = 'up' if direction == 1 else 'down'
        
        brick = {
            'open': round(start_price, 2),
            'close': round(end_price, 2),
            'type': brick_type,
            'direction': direction,
            'size': self.brick_size
        }
        
        self.bricks.append(brick)
    
    def _round_to_brick(self, price: float, direction: int) -> float:
        """
        Round price to nearest brick boundary
        
        Args:
            price: Price to round
            direction: Direction of movement
            
        Returns:
            Rounded price
        """
        if direction == 1:
            # Round up for upward movement
            return np.ceil(price / self.brick_size) * self.brick_size
        else:
            # Round down for downward movement
            return np.floor(price / self.brick_size) * self.brick_size
    
    def get_trend_summary(self) -> Dict[str, Any]:
        """
        Get trend summary from Renko bricks
        
        Returns:
            Dictionary with trend analysis
        """
        try:
            if not self.bricks:
                return {
                    'trend': 'No data',
                    'strength': 0,
                    'consecutive_bricks': 0,
                    'total_bricks': 0
                }
            
            # Count consecutive bricks of same type
            consecutive_count = 1
            last_type = self.bricks[-1]['type']
            
            for i in range(len(self.bricks) - 2, -1, -1):
                if self.bricks[i]['type'] == last_type:
                    consecutive_count += 1
                else:
                    break
            
            # Overall trend analysis
            up_bricks = sum(1 for brick in self.bricks if brick['type'] == 'up')
            down_bricks = sum(1 for brick in self.bricks if brick['type'] == 'down')
            
            if up_bricks > down_bricks:
                overall_trend = 'Bullish'
            elif down_bricks > up_bricks:
                overall_trend = 'Bearish'
            else:
                overall_trend = 'Neutral'
            
            # Calculate trend strength (0-100)
            total_bricks = len(self.bricks)
            if total_bricks > 0:
                strength = abs(up_bricks - down_bricks) / total_bricks * 100
            else:
                strength = 0
            
            return {
                'trend': overall_trend,
                'current_direction': last_type.capitalize(),
                'strength': round(strength, 1),
                'consecutive_bricks': consecutive_count,
                'total_bricks': total_bricks,
                'up_bricks': up_bricks,
                'down_bricks': down_bricks,
                'brick_size': self.brick_size
            }
            
        except Exception as e:
            logger.error(f"Error getting trend summary: {str(e)}")
            return {
                'trend': 'Error',
                'strength': 0,
                'consecutive_bricks': 0,
                'total_bricks': 0
            }
    
    def get_signals(self) -> List[Dict[str, Any]]:
        """
        Get trading signals from Renko chart
        
        Returns:
            List of trading signals
        """
        try:
            signals = []
            
            if len(self.bricks) < 3:
                return signals
            
            # Look for trend reversals
            for i in range(2, len(self.bricks)):
                current_brick = self.bricks[i]
                prev_brick = self.bricks[i-1]
                prev_prev_brick = self.bricks[i-2]
                
                # Bullish reversal signal
                if (prev_prev_brick['type'] == 'down' and 
                    prev_brick['type'] == 'down' and 
                    current_brick['type'] == 'up'):
                    
                    signals.append({
                        'type': 'buy',
                        'strength': 'medium',
                        'reason': 'Bullish reversal after downtrend',
                        'price': current_brick['close'],
                        'brick_index': i
                    })
                
                # Bearish reversal signal
                elif (prev_prev_brick['type'] == 'up' and 
                      prev_brick['type'] == 'up' and 
                      current_brick['type'] == 'down'):
                    
                    signals.append({
                        'type': 'sell',
                        'strength': 'medium',
                        'reason': 'Bearish reversal after uptrend',
                        'price': current_brick['close'],
                        'brick_index': i
                    })
            
            # Strong trend continuation signals
            consecutive_up = 0
            consecutive_down = 0
            
            for brick in reversed(self.bricks):
                if brick['type'] == 'up':
                    consecutive_up += 1
                    consecutive_down = 0
                else:
                    consecutive_down += 1
                    consecutive_up = 0
                
                # Strong uptrend
                if consecutive_up >= 5:
                    signals.append({
                        'type': 'strong_buy',
                        'strength': 'high',
                        'reason': f'Strong uptrend with {consecutive_up} consecutive up bricks',
                        'price': self.bricks[-1]['close'],
                        'brick_index': len(self.bricks) - 1
                    })
                    break
                
                # Strong downtrend
                elif consecutive_down >= 5:
                    signals.append({
                        'type': 'strong_sell',
                        'strength': 'high',
                        'reason': f'Strong downtrend with {consecutive_down} consecutive down bricks',
                        'price': self.bricks[-1]['close'],
                        'brick_index': len(self.bricks) - 1
                    })
                    break
            
            return signals
            
        except Exception as e:
            logger.error(f"Error getting Renko signals: {str(e)}")
            return []
    
    def export_data(self) -> pd.DataFrame:
        """
        Export Renko data as DataFrame
        
        Returns:
            DataFrame with Renko brick data
        """
        try:
            if not self.bricks:
                return pd.DataFrame()
            
            data = []
            for i, brick in enumerate(self.bricks):
                data.append({
                    'brick_number': i + 1,
                    'open': brick['open'],
                    'close': brick['close'],
                    'type': brick['type'],
                    'direction': brick['direction'],
                    'brick_size': brick['size']
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Error exporting Renko data: {str(e)}")
            return pd.DataFrame()