# routes/__init__.py

"""
Routes package for Stock Market Predictor
Contains all API route blueprints
"""

from .stock_routes import stock_bp
from .news_routes import news_bp  
from .volatility_routes import volatility_bp

__all__ = [
    'stock_bp',
    'news_bp',
    'volatility_bp'
]