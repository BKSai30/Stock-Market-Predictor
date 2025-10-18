"""
Helper Utilities for Stock Market Predictor
Contains common utility functions used across the application
"""

import logging
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import pytz
from config import Config

def setup_logging():
    """Setup application logging"""
    try:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log'),
                logging.StreamHandler()
            ]
        )
        
        # Set specific loggers to WARNING to reduce noise
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")

def get_market_timezone():
    """Get Indian market timezone"""
    return pytz.timezone('Asia/Kolkata')

def is_market_open():
    """
    Check if Indian stock market is currently open
    
    Returns:
        bool: True if market is open, False otherwise
    """
    try:
        tz = get_market_timezone()
        now = datetime.now(tz)
        
        # Check if it's a weekday (Monday = 0, Sunday = 6)
        if now.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Market hours: 9:15 AM to 3:30 PM IST
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open <= now <= market_close
        
    except Exception as e:
        logging.error(f"Error checking market status: {str(e)}")
        return False

def format_currency(amount: float, currency: str = '₹') -> str:
    """
    Format currency for Indian market
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    try:
        if amount >= 10000000:  # 1 Crore
            return f"{currency}{amount/10000000:.2f}Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"{currency}{amount/100000:.2f}L"
        elif amount >= 1000:  # 1 Thousand
            return f"{currency}{amount/1000:.2f}K"
        else:
            return f"{currency}{amount:.2f}"
    except Exception as e:
        logging.error(f"Error formatting currency: {str(e)}")
        return f"{currency}{amount}"

def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate if a stock symbol is valid for Indian markets
    
    Args:
        symbol: Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not symbol or len(symbol) < 2:
            return False
        
        # Remove exchange suffix for validation
        clean_symbol = symbol.replace('.NS', '').replace('.BS', '').upper()
        
        # Basic validation: alphanumeric characters only
        if not clean_symbol.isalnum():
            return False
        
        # Length check (Indian stock symbols are typically 3-10 characters)
        if len(clean_symbol) < 3 or len(clean_symbol) > 10:
            return False
        
        return True
        
    except Exception as e:
        logging.error(f"Error validating stock symbol: {str(e)}")
        return False

def normalize_stock_symbol(symbol: str, exchange: str = 'NS') -> str:
    """
    Normalize stock symbol for API calls
    
    Args:
        symbol: Stock symbol
        exchange: Exchange suffix (NS for NSE, BS for BSE)
        
    Returns:
        Normalized symbol
    """
    try:
        if not symbol:
            return ''
        
        # Clean the symbol
        clean_symbol = symbol.replace('.NS', '').replace('.BS', '').upper().strip()
        
        # Add exchange suffix if not present
        if '.' not in symbol:
            return f"{clean_symbol}.{exchange}"
        
        return symbol.upper()
        
    except Exception as e:
        logging.error(f"Error normalizing stock symbol: {str(e)}")
        return symbol

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    try:
        if old_value == 0:
            return 0.0
        return ((new_value - old_value) / old_value) * 100
    except Exception as e:
        logging.error(f"Error calculating percentage change: {str(e)}")
        return 0.0

def get_trading_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """
    Get list of trading days between two dates (excludes weekends)
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        List of trading days
    """
    try:
        trading_days = []
        current_date = start_date
        
        while current_date <= end_date:
            # Exclude weekends (Saturday = 5, Sunday = 6)
            if current_date.weekday() < 5:
                trading_days.append(current_date)
            current_date += timedelta(days=1)
        
        return trading_days
        
    except Exception as e:
        logging.error(f"Error calculating trading days: {str(e)}")
        return []

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Division result or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except Exception as e:
        logging.error(f"Error in safe division: {str(e)}")
        return default

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a pandas DataFrame by removing NaN values and ensuring proper data types
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    try:
        # Remove rows with any NaN values
        df_clean = df.dropna()
        
        # Ensure numeric columns are actually numeric
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove any rows that became NaN after conversion
        df_clean = df_clean.dropna()
        
        # Sort by index (should be dates)
        df_clean = df_clean.sort_index()
        
        return df_clean
        
    except Exception as e:
        logging.error(f"Error cleaning DataFrame: {str(e)}")
        return df

def json_serializer(obj):
    """
    JSON serializer for objects not serializable by default json code
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serializable representation
    """
    if isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def save_to_cache(data: Any, cache_key: str, cache_dir: str = "data/cache") -> bool:
    """
    Save data to cache
    
    Args:
        data: Data to cache
        cache_key: Cache key
        cache_dir: Cache directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, f"{cache_key}.json")
        
        cache_data = {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'cache_key': cache_key
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, default=json_serializer, indent=2)
        
        return True
        
    except Exception as e:
        logging.error(f"Error saving to cache: {str(e)}")
        return False

def load_from_cache(cache_key: str, cache_dir: str = "data/cache", max_age_hours: int = 24) -> Optional[Any]:
    """
    Load data from cache
    
    Args:
        cache_key: Cache key
        cache_dir: Cache directory
        max_age_hours: Maximum age of cache in hours
        
    Returns:
        Cached data or None if not found/expired
    """
    try:
        cache_file = os.path.join(cache_dir, f"{cache_key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        # Check if cache is expired
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - cache_time > timedelta(hours=max_age_hours):
            return None
        
        return cache_data['data']
        
    except Exception as e:
        logging.error(f"Error loading from cache: {str(e)}")
        return None

def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        True if valid, False otherwise
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Check if start is before end
        if start >= end:
            return False
        
        # Check if dates are not in the future
        if end > datetime.now():
            return False
        
        # Check if range is not too large (max 10 years)
        if (end - start).days > 365 * 10:
            return False
        
        return True
        
    except Exception as e:
        logging.error(f"Error validating date range: {str(e)}")
        return False

def get_business_days_between(start_date: datetime, end_date: datetime) -> int:
    """
    Get number of business days between two dates
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Number of business days
    """
    try:
        return len(pd.bdate_range(start_date, end_date))
    except Exception as e:
        logging.error(f"Error calculating business days: {str(e)}")
        return 0

def format_large_number(number: float) -> str:
    """
    Format large numbers with appropriate suffixes
    
    Args:
        number: Number to format
        
    Returns:
        Formatted number string
    """
    try:
        if abs(number) >= 1e12:
            return f"{number/1e12:.2f}T"
        elif abs(number) >= 1e9:
            return f"{number/1e9:.2f}B"
        elif abs(number) >= 1e6:
            return f"{number/1e6:.2f}M"
        elif abs(number) >= 1e3:
            return f"{number/1e3:.2f}K"
        else:
            return f"{number:.2f}"
    except Exception as e:
        logging.error(f"Error formatting large number: {str(e)}")
        return str(number)

def retry_on_failure(func, max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        delay: Delay between retries in seconds
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    logging.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
                else:
                    logging.error(f"All {max_retries + 1} attempts failed: {str(e)}")
        
        raise last_exception
    
    return wrapper

class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_ohlc_data(data: pd.DataFrame) -> bool:
        """
        Validate OHLC data
        
        Args:
            data: OHLC DataFrame
            
        Returns:
            True if valid, False otherwise
        """
        try:
            required_columns = ['Open', 'High', 'Low', 'Close']
            
            # Check if all required columns exist
            if not all(col in data.columns for col in required_columns):
                return False
            
            # Check if High >= Low
            if not (data['High'] >= data['Low']).all():
                return False
            
            # Check if High >= Open and High >= Close
            if not (data['High'] >= data['Open']).all() or not (data['High'] >= data['Close']).all():
                return False
            
            # Check if Low <= Open and Low <= Close
            if not (data['Low'] <= data['Open']).all() or not (data['Low'] <= data['Close']).all():
                return False
            
            # Check for reasonable price ranges (not negative or extremely large)
            for col in required_columns:
                if (data[col] <= 0).any() or (data[col] > 1e6).any():
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Error validating OHLC data: {str(e)}")
            return False
    
    @staticmethod
    def validate_prediction_input(symbol: str, days_ahead: int) -> Dict[str, Any]:
        """
        Validate prediction input parameters
        
        Args:
            symbol: Stock symbol
            days_ahead: Number of days to predict
            
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Validate symbol
        if not validate_stock_symbol(symbol):
            errors.append("Invalid stock symbol")
        
        # Validate days_ahead
        if not isinstance(days_ahead, int) or days_ahead < 1 or days_ahead > 30:
            errors.append("Days ahead must be between 1 and 30")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'normalized_symbol': normalize_stock_symbol(symbol) if errors == [] else symbol
        }
