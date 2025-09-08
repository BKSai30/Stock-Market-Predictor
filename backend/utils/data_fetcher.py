"""
Data Fetcher Utility for Stock Market Predictor
Handles fetching stock data from multiple sources including Yahoo Finance, NSE, BSE
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import logging
import time
import json
from typing import Optional, List, Dict, Any
import os
from config import Config

logger = logging.getLogger(__name__)

class DataFetcher:
    """
    Handles data fetching from various stock market APIs and sources
    """
    
    def __init__(self):
        self.config = Config()
        self.cache_dir = "data/cache"
        self.ensure_cache_dir()
        
        # NSE/BSE stock symbol mappings
        self.nse_stocks = self.config.NIFTY_50_STOCKS
        self.bse_stocks = self.config.BSE_SENSEX_STOCKS
        
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_stock_data(self, symbol: str, period: str = "5y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            period: Period for data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            # Check cache first
            cache_key = f"{symbol}_{period}_{interval}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data is not None:
                return cached_data
            
            logger.info(f"Fetching data for {symbol} with period {period}")
            
            # Add .NS suffix for NSE stocks if not present
            if '.' not in symbol and symbol in [s.replace('.NS', '') for s in self.nse_stocks]:
                symbol = f"{symbol}.NS"
            
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return None
            
            # Clean and prepare data
            data = self._clean_stock_data(data)
            
            # Cache the data
            self._cache_data(cache_key, data)
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed stock information
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock information or None if failed
        """
        try:
            if '.' not in symbol and symbol in [s.replace('.NS', '') for s in self.nse_stocks]:
                symbol = f"{symbol}.NS"
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            stock_info = {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'current_price': info.get('currentPrice', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0)
            }
            
            return stock_info
            
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return None
    
    def get_safe_stocks(self) -> List[Dict[str, Any]]:
        """
        Get top 5 safe (low volatility) stocks
        
        Returns:
            List of stock dictionaries with basic info
        """
        return self._get_stocks_by_volatility('safe')
    
    def get_volatile_stocks(self) -> List[Dict[str, Any]]:
        """
        Get top 5 moderately volatile stocks
        
        Returns:
            List of stock dictionaries with basic info
        """
        return self._get_stocks_by_volatility('volatile')
    
    def get_highly_volatile_stocks(self) -> List[Dict[str, Any]]:
        """
        Get top 5 highly volatile stocks
        
        Returns:
            List of stock dictionaries with basic info
        """
        return self._get_stocks_by_volatility('highly_volatile')
    
    def _get_stocks_by_volatility(self, category: str) -> List[Dict[str, Any]]:
        """
        Get stocks filtered by volatility category
        
        Args:
            category: 'safe', 'volatile', or 'highly_volatile'
            
        Returns:
            List of stock dictionaries
        """
        try:
            stocks_with_volatility = []
            
            # Sample some stocks from NIFTY 50 for demonstration
            sample_stocks = self.nse_stocks[:20]  # Limit to reduce API calls
            
            for symbol in sample_stocks:
                try:
                    # Get recent data to calculate volatility
                    data = self.get_stock_data(symbol, period="3mo", interval="1d")
                    if data is None or len(data) < 30:
                        continue
                    
                    # Calculate volatility (standard deviation of returns)
                    returns = data['Close'].pct_change().dropna()
                    volatility = returns.std() * 100 * np.sqrt(252)  # Annualized volatility
                    
                    # Get current price and change
                    current_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2]
                    price_change = ((current_price - prev_price) / prev_price) * 100
                    
                    # Get stock info
                    info = self.get_stock_info(symbol)
                    if not info:
                        continue
                    
                    stock_data = {
                        'symbol': symbol,
                        'name': info.get('name', symbol),
                        'current_price': round(current_price, 2),
                        'price_change': round(price_change, 2),
                        'volatility': round(volatility, 2),
                        'volume': info.get('volume', 0),
                        'market_cap': info.get('market_cap', 0)
                    }
                    
                    # Filter by volatility category
                    vol_config = self.config.VOLATILITY_CATEGORIES[category]
                    if vol_config['min_vol'] <= volatility <= vol_config['max_vol']:
                        stocks_with_volatility.append(stock_data)
                    
                    # Add small delay to avoid hitting rate limits
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.warning(f"Error processing {symbol}: {str(e)}")
                    continue
            
            # Sort by volume and return top 5
            stocks_with_volatility.sort(key=lambda x: x['volume'], reverse=True)
            return stocks_with_volatility[:5]
            
        except Exception as e:
            logger.error(f"Error getting {category} stocks: {str(e)}")
            return []
    
    def get_market_indices(self) -> Dict[str, Any]:
        """
        Get major Indian market indices data
        
        Returns:
            Dictionary with index data
        """
        try:
            indices = {
                'NIFTY': '^NSEI',
                'SENSEX': '^BSESN',
                'BANKNIFTY': '^NSEBANK',
                'NIFTYIT': '^CNXIT'
            }
            
            index_data = {}
            
            for name, symbol in indices.items():
                try:
                    data = self.get_stock_data(symbol, period="1d", interval="1m")
                    if data is not None and not data.empty:
                        current_price = data['Close'].iloc[-1]
                        prev_close = data['Close'].iloc[0]
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100
                        
                        index_data[name] = {
                            'current_price': round(current_price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_percent, 2),
                            'volume': int(data['Volume'].iloc[-1]) if 'Volume' in data.columns else 0
                        }
                except Exception as e:
                    logger.warning(f"Error fetching {name}: {str(e)}")
                    continue
            
            return index_data
            
        except Exception as e:
            logger.error(f"Error fetching market indices: {str(e)}")
            return {}
    
    def search_stocks(self, query: str) -> List[Dict[str, str]]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search query
            
        Returns:
            List of matching stocks
        """
        try:
            results = []
            query = query.upper()
            
            # Search in predefined stock lists
            all_stocks = self.nse_stocks + self.bse_stocks
            
            for symbol in all_stocks:
                if query in symbol or query in symbol.replace('.NS', '').replace('.BS', ''):
                    info = self.get_stock_info(symbol)
                    if info:
                        results.append({
                            'symbol': symbol,
                            'name': info.get('name', symbol),
                            'exchange': 'NSE' if '.NS' in symbol else 'BSE'
                        })
                
                if len(results) >= 10:  # Limit results
                    break
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching stocks: {str(e)}")
            return []
    
    def _clean_stock_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare stock data
        
        Args:
            data: Raw stock data
            
        Returns:
            Cleaned stock data
        """
        try:
            # Remove any rows with NaN values
            data = data.dropna()
            
            # Ensure numeric types
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_columns:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
            
            # Remove any remaining NaN values after conversion
            data = data.dropna()
            
            # Sort by date
            data = data.sort_index()
            
            return data
            
        except Exception as e:
            logger.error(f"Error cleaning stock data: {str(e)}")
            return data
    
    def _get_cached_data(self, cache_key: str) -> Optional[pd.DataFrame]:
        """
        Get data from cache if available and not expired
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached DataFrame or None
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
            
            if os.path.exists(cache_file):
                # Check if cache is still valid
                cache_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                if datetime.now() - cache_time < self.config.DATA_CACHE_DURATION:
                    data = pd.read_pickle(cache_file)
                    logger.debug(f"Using cached data for {cache_key}")
                    return data
                else:
                    # Remove expired cache
                    os.remove(cache_file)
            
            return None
            
        except Exception as e:
            logger.warning(f"Error reading cache for {cache_key}: {str(e)}")
            return None
    
    def _cache_data(self, cache_key: str, data: pd.DataFrame):
        """
        Cache data to disk
        
        Args:
            cache_key: Cache key
            data: Data to cache
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
            data.to_pickle(cache_file)
            logger.debug(f"Cached data for {cache_key}")
            
        except Exception as e:
            logger.warning(f"Error caching data for {cache_key}: {str(e)}")
    
    def clear_cache(self):
        """Clear all cached data"""
        try:
            import glob
            cache_files = glob.glob(os.path.join(self.cache_dir, "*.pkl"))
            for file in cache_files:
                os.remove(file)
            logger.info("Cache cleared successfully")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
    
    def get_real_time_price(self, symbol: str) -> Optional[float]:
        """
        Get real-time price for a stock
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current price or None if failed
        """
        try:
            if '.' not in symbol:
                symbol = f"{symbol}.NS"

            # 0) Try Finnhub if API key is available (more precise during market hours)
            try:
                if getattr(self.config, 'FINNHUB_API_KEY', None):
                    import finnhub
                    client = finnhub.Client(api_key=self.config.FINNHUB_API_KEY)
                    finnhub_symbol = symbol
                    q = client.quote(finnhub_symbol)
                    if q and isinstance(q, dict):
                        last_price = q.get('c')
                        if last_price and float(last_price) > 0:
                            return float(last_price)
            except Exception:
                pass

            # 1) Try yfinance fast_info first (more reliable than info)
            try:
                ticker = yf.Ticker(symbol)
                fast_info = getattr(ticker, 'fast_info', None)
                if fast_info:
                    price = fast_info.get('last_price') or fast_info.get('lastPrice')
                    if price is None:
                        price = fast_info.get('regular_market_price') or fast_info.get('regularMarketPrice')
                    if price:
                        return float(price)
            except Exception:
                pass

            # 2) Fallback to info
            try:
                info = ticker.info
                price = info.get('currentPrice') or info.get('regularMarketPrice')
                if price:
                    return float(price)
            except Exception:
                pass

            # 3) Fallback: recent history close
            try:
                hist = ticker.history(period="1d", interval="1m")
                if not hist.empty:
                    return float(hist['Close'].dropna().iloc[-1])
            except Exception:
                pass

            return None

        except Exception as e:
            logger.error(f"Error fetching real-time price for {symbol}: {str(e)}")
            return None

    def get_real_time_prices_bulk(self, symbols: List[str]) -> Dict[str, Optional[float]]:
        """
        Get real-time prices for multiple symbols efficiently

        Args:
            symbols: List of stock symbols (without exchange suffix)

        Returns:
            Dict mapping symbol -> price (or None)
        """
        results: Dict[str, Optional[float]] = {}
        for sym in symbols:
            clean_sym = sym.replace('.NS', '')
            results[clean_sym] = self.get_real_time_price(clean_sym)
        return results