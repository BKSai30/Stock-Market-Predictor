"""
Sentiment Analyzer for Stock Market News
Analyzes news sentiment and its impact on stock prices
"""

import requests
import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
import time
from config import Config
import json
import os

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Analyzes sentiment from news articles and social media related to stocks
    """
    
    def __init__(self):
        self.config = Config()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.news_cache = {}
        self.cache_file = "data/cache/news_cache.json"
        
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        
        # Load cached news if exists
        self._load_news_cache()
        
        # Stock-related keywords for filtering
        self.stock_keywords = {
            'bullish': ['growth', 'profit', 'buy', 'upgrade', 'positive', 'rise', 'gain', 'increase', 'bull', 'strong'],
            'bearish': ['loss', 'sell', 'downgrade', 'negative', 'fall', 'decline', 'drop', 'bear', 'weak', 'crash'],
            'neutral': ['stable', 'hold', 'maintain', 'steady', 'unchanged']
        }
        
        # Indian stock market specific terms
        self.indian_market_terms = [
            'nse', 'bse', 'nifty', 'sensex', 'rupee', 'sebi', 'fii', 'dii',
            'mutual fund', 'ipo', 'india', 'mumbai', 'delhi', 'bangalore'
        ]
    
    def initialize(self):
        """Initialize sentiment analyzer"""
        try:
            logger.info("Initializing sentiment analyzer...")
            # Test VADER analyzer
            test_sentiment = self.vader_analyzer.polarity_scores("This is a test sentence")
            logger.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing sentiment analyzer: {str(e)}")
    
    def analyze_stock_sentiment(self, symbol: str, days_back: int = 7) -> float:
        """
        Analyze overall sentiment for a stock symbol
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE')
            days_back: Number of days to look back for news
            
        Returns:
            Sentiment score between -1 (negative) and 1 (positive)
        """
        try:
            logger.info(f"Analyzing sentiment for {symbol}")
            
            # Get company name from symbol
            company_name = self._get_company_name(symbol)
            
            # Fetch news articles
            news_articles = self._fetch_news_articles(company_name, days_back)
            
            if not news_articles:
                logger.warning(f"No news articles found for {symbol}")
                return 0.0
            
            # Analyze sentiment of each article
            sentiments = []
            for article in news_articles:
                try:
                    # Combine title and description for analysis
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    
                    if len(text.strip()) < 10:  # Skip very short texts
                        continue
                    
                    # Get sentiment scores
                    vader_score = self._get_vader_sentiment(text)
                    textblob_score = self._get_textblob_sentiment(text)
                    
                    # Weight by relevance to stock
                    relevance_weight = self._calculate_relevance_weight(text, symbol, company_name)
                    
                    # Combine scores
                    combined_score = (vader_score * 0.6 + textblob_score * 0.4) * relevance_weight
                    
                    sentiments.append({
                        'score': combined_score,
                        'weight': relevance_weight,
                        'date': article.get('publishedAt', ''),
                        'title': article.get('title', '')
                    })
                    
                except Exception as e:
                    logger.warning(f"Error analyzing article sentiment: {str(e)}")
                    continue
            
            if not sentiments:
                return 0.0
            
            # Calculate weighted average sentiment
            total_weighted_score = sum(s['score'] * s['weight'] for s in sentiments)
            total_weight = sum(s['weight'] for s in sentiments)
            
            if total_weight == 0:
                return 0.0
            
            overall_sentiment = total_weighted_score / total_weight
            
            # Apply time decay (recent news has more impact)
            time_weighted_sentiment = self._apply_time_decay(sentiments)
            
            # Combine current and time-weighted sentiment
            final_sentiment = (overall_sentiment * 0.7 + time_weighted_sentiment * 0.3)
            
            # Clamp to [-1, 1] range
            final_sentiment = max(-1.0, min(1.0, final_sentiment))
            
            logger.info(f"Final sentiment for {symbol}: {final_sentiment:.3f}")
            return final_sentiment
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {symbol}: {str(e)}")
            return 0.0
    
    def get_sector_sentiment(self, sector: str) -> float:
        """
        Get sentiment for a specific sector
        
        Args:
            sector: Sector name (e.g., 'banking', 'IT', 'pharma')
            
        Returns:
            Sector sentiment score
        """
        try:
            # Fetch sector-specific news
            news_articles = self._fetch_sector_news(sector)
            
            if not news_articles:
                return 0.0
            
            sentiments = []
            for article in news_articles:
                text = f"{article.get('title', '')} {article.get('description', '')}"
                
                vader_score = self._get_vader_sentiment(text)
                textblob_score = self._get_textblob_sentiment(text)
                
                combined_score = vader_score * 0.6 + textblob_score * 0.4
                sentiments.append(combined_score)
            
            return np.mean(sentiments) if sentiments else 0.0
            
        except Exception as e:
            logger.error(f"Error getting sector sentiment: {str(e)}")
            return 0.0
    
    def get_market_sentiment(self) -> Dict[str, float]:
        """
        Get overall market sentiment
        
        Returns:
            Dictionary with market sentiment indicators
        """
        try:
            # Get general market news
            market_news = self._fetch_market_news()
            
            if not market_news:
                return {'overall': 0.0, 'confidence': 0.0}
            
            sentiments = []
            for article in market_news:
                text = f"{article.get('title', '')} {article.get('description', '')}"
                
                vader_score = self._get_vader_sentiment(text)
                textblob_score = self._get_textblob_sentiment(text)
                
                combined_score = vader_score * 0.6 + textblob_score * 0.4
                sentiments.append(combined_score)
            
            overall_sentiment = np.mean(sentiments) if sentiments else 0.0
            confidence = len(sentiments) / 50  # Normalize by expected number of articles
            
            return {
                'overall': overall_sentiment,
                'confidence': min(1.0, confidence),
                'article_count': len(sentiments)
            }
            
        except Exception as e:
            logger.error(f"Error getting market sentiment: {str(e)}")
            return {'overall': 0.0, 'confidence': 0.0}
    
    def _get_vader_sentiment(self, text: str) -> float:
        """Get VADER sentiment score"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return scores['compound']
        except Exception as e:
            logger.warning(f"Error in VADER analysis: {str(e)}")
            return 0.0
    
    def _get_textblob_sentiment(self, text: str) -> float:
        """Get TextBlob sentiment score"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            logger.warning(f"Error in TextBlob analysis: {str(e)}")
            return 0.0
    
    def _calculate_relevance_weight(self, text: str, symbol: str, company_name: str) -> float:
        """
        Calculate how relevant the text is to the stock
        
        Args:
            text: Article text
            symbol: Stock symbol
            company_name: Company name
            
        Returns:
            Relevance weight (0.1 to 1.0)
        """
        try:
            text_lower = text.lower()
            
            # Base weight
            weight = 0.1
            
            # Check for direct mentions
            if symbol.lower() in text_lower:
                weight += 0.4
            
            if company_name and company_name.lower() in text_lower:
                weight += 0.3
            
            # Check for stock market related terms
            market_terms_found = sum(1 for term in self.indian_market_terms if term in text_lower)
            weight += min(0.2, market_terms_found * 0.05)
            
            # Check for financial keywords
            bullish_count = sum(1 for word in self.stock_keywords['bullish'] if word in text_lower)
            bearish_count = sum(1 for word in self.stock_keywords['bearish'] if word in text_lower)
            
            if bullish_count > 0 or bearish_count > 0:
                weight += 0.1
            
            return min(1.0, weight)
            
        except Exception as e:
            logger.warning(f"Error calculating relevance weight: {str(e)}")
            return 0.5
    
    def _apply_time_decay(self, sentiments: List[Dict]) -> float:
        """
        Apply time decay to sentiment scores (recent news has more impact)
        
        Args:
            sentiments: List of sentiment dictionaries with dates
            
        Returns:
            Time-weighted sentiment score
        """
        try:
            if not sentiments:
                return 0.0
            
            now = datetime.now()
            weighted_scores = []
            
            for sentiment in sentiments:
                try:
                    # Parse date
                    if sentiment.get('date'):
                        article_date = datetime.fromisoformat(sentiment['date'].replace('Z', '+00:00'))
                        article_date = article_date.replace(tzinfo=None)  # Remove timezone for comparison
                    else:
                        article_date = now  # Assume recent if no date
                    
                    # Calculate days ago
                    days_ago = (now - article_date).days
                    
                    # Apply exponential decay (half-life of 2 days)
                    time_weight = np.exp(-days_ago * np.log(2) / 2)
                    
                    weighted_score = sentiment['score'] * time_weight
                    weighted_scores.append(weighted_score)
                    
                except Exception as e:
                    logger.warning(f"Error processing sentiment date: {str(e)}")
                    weighted_scores.append(sentiment['score'] * 0.5)  # Default weight
            
            return np.mean(weighted_scores) if weighted_scores else 0.0
            
        except Exception as e:
            logger.warning(f"Error applying time decay: {str(e)}")
            return 0.0
    
    def _fetch_news_articles(self, company_name: str, days_back: int) -> List[Dict]:
        """
        Fetch news articles for a company
        
        Args:
            company_name: Name of the company
            days_back: Number of days to look back
            
        Returns:
            List of news articles
        """
        try:
            # Check cache first
            cache_key = f"{company_name}_{days_back}"
            if cache_key in self.news_cache:
                cached_data = self.news_cache[cache_key]
                if datetime.now() - datetime.fromisoformat(cached_data['timestamp']) < self.config.NEWS_CACHE_DURATION:
                    return cached_data['articles']
            
            # If no cache or expired, fetch new data
            articles = []
            
            # Try multiple approaches to get news
            
            # 1. Free news sources (dummy implementation - replace with actual APIs)
            dummy_articles = self._get_dummy_news_articles(company_name)
            articles.extend(dummy_articles)
            
            # 2. If you have News API key, uncomment and use this:
            # if self.config.NEWS_API_KEY and self.config.NEWS_API_KEY != 'your-news-api-key':
            #     api_articles = self._fetch_from_news_api(company_name, days_back)
            #     articles.extend(api_articles)
            
            # Cache the results
            self.news_cache[cache_key] = {
                'articles': articles,
                'timestamp': datetime.now().isoformat()
            }
            self._save_news_cache()
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching news articles: {str(e)}")
            return []
    
    def _get_dummy_news_articles(self, company_name: str) -> List[Dict]:
        """
        Generate dummy news articles for demonstration
        Replace this with actual news API calls
        """
        try:
            # This is dummy data for demonstration
            # In production, replace with actual news API
            
            dummy_articles = [
                {
                    'title': f'{company_name} reports strong quarterly earnings',
                    'description': f'{company_name} shows impressive growth in latest quarter with increased revenue and profit margins.',
                    'publishedAt': (datetime.now() - timedelta(days=1)).isoformat(),
                    'source': {'name': 'Business Standard'}
                },
                {
                    'title': f'Analysts upgrade {company_name} stock rating',
                    'description': f'Multiple analysts have upgraded their rating for {company_name} citing strong fundamentals and growth prospects.',
                    'publishedAt': (datetime.now() - timedelta(days=2)).isoformat(),
                    'source': {'name': 'Economic Times'}
                },
                {
                    'title': f'{company_name} announces new strategic partnership',
                    'description': f'{company_name} enters into strategic partnership to expand market reach and improve operational efficiency.',
                    'publishedAt': (datetime.now() - timedelta(days=3)).isoformat(),
                    'source': {'name': 'Livemint'}
                }
            ]
            
            return dummy_articles
            
        except Exception as e:
            logger.error(f"Error generating dummy articles: {str(e)}")
            return []
    
    def _fetch_from_news_api(self, company_name: str, days_back: int) -> List[Dict]:
        """
        Fetch news from News API (requires API key)
        """
        try:
            if not self.config.NEWS_API_KEY or self.config.NEWS_API_KEY == 'your-news-api-key':
                return []
            
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f'"{company_name}" AND (stock OR share OR market)',
                'from': from_date,
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': self.config.NEWS_API_KEY,
                'pageSize': 50
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('articles', [])
            
        except Exception as e:
            logger.error(f"Error fetching from News API: {str(e)}")
            return []
    
    def _fetch_sector_news(self, sector: str) -> List[Dict]:
        """Fetch sector-specific news"""
        try:
            # Dummy implementation - replace with actual API calls
            sector_terms = {
                'banking': ['bank', 'banking', 'finance', 'loan', 'credit'],
                'IT': ['technology', 'software', 'IT', 'digital'],
                'pharma': ['pharmaceutical', 'drug', 'medicine', 'healthcare']
            }
            
            terms = sector_terms.get(sector.lower(), [sector])
            query = ' OR '.join(terms)
            
            # Return dummy articles for demonstration
            return self._get_dummy_news_articles(f"{sector} sector")
            
        except Exception as e:
            logger.error(f"Error fetching sector news: {str(e)}")
            return []
    
    def _fetch_market_news(self) -> List[Dict]:
        """Fetch general market news"""
        try:
            # Return dummy market news for demonstration
            return self._get_dummy_news_articles("Indian stock market")
            
        except Exception as e:
            logger.error(f"Error fetching market news: {str(e)}")
            return []
    
    def _get_company_name(self, symbol: str) -> str:
        """
        Get company name from stock symbol
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Company name
        """
        try:
            # Remove exchange suffix
            clean_symbol = symbol.replace('.NS', '').replace('.BS', '')
            
            # Common symbol to name mappings for Indian stocks
            symbol_to_name = {
                'RELIANCE': 'Reliance Industries',
                'TCS': 'Tata Consultancy Services',
                'HDFCBANK': 'HDFC Bank',
                'INFY': 'Infosys',
                'HINDUNILVR': 'Hindustan Unilever',
                'ICICIBANK': 'ICICI Bank',
                'KOTAKBANK': 'Kotak Mahindra Bank',
                'BHARTIAIRTEL': 'Bharti Airtel',
                'ITC': 'ITC Limited',
                'SBIN': 'State Bank of India',
                'BAJFINANCE': 'Bajaj Finance',
                'ASIANPAINT': 'Asian Paints',
                'MARUTI': 'Maruti Suzuki',
                'HCLTECH': 'HCL Technologies',
                'AXISBANK': 'Axis Bank',
                'LT': 'Larsen & Toubro',
                'WIPRO': 'Wipro',
                'SUNPHARMA': 'Sun Pharmaceutical',
                'TITAN': 'Titan Company'
            }
            
            return symbol_to_name.get(clean_symbol, clean_symbol)
            
        except Exception as e:
            logger.warning(f"Error getting company name for {symbol}: {str(e)}")
            return symbol
    
    def _load_news_cache(self):
        """Load news cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.news_cache = json.load(f)
        except Exception as e:
            logger.warning(f"Error loading news cache: {str(e)}")
            self.news_cache = {}
    
    def _save_news_cache(self):
        """Save news cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.news_cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Error saving news cache: {str(e)}")
    
    def clear_cache(self):
        """Clear news cache"""
        try:
            self.news_cache = {}
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            logger.info("News cache cleared")
        except Exception as e:
            logger.error(f"Error clearing news cache: {str(e)}")
    
    def get_sentiment_summary(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive sentiment summary for a stock
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with sentiment analysis summary
        """
        try:
            # Get main sentiment
            main_sentiment = self.analyze_stock_sentiment(symbol)
            
            # Get sector sentiment
            stock_info = self._get_stock_sector(symbol)
            sector_sentiment = self.get_sector_sentiment(stock_info.get('sector', '')) if stock_info else 0.0
            
            # Get market sentiment
            market_sentiment = self.get_market_sentiment()
            
            # Classify sentiment
            def classify_sentiment(score):
                if score > 0.1:
                    return 'Positive'
                elif score < -0.1:
                    return 'Negative'
                else:
                    return 'Neutral'
            
            return {
                'stock_sentiment': {
                    'score': main_sentiment,
                    'classification': classify_sentiment(main_sentiment)
                },
                'sector_sentiment': {
                    'score': sector_sentiment,
                    'classification': classify_sentiment(sector_sentiment)
                },
                'market_sentiment': {
                    'score': market_sentiment.get('overall', 0.0),
                    'classification': classify_sentiment(market_sentiment.get('overall', 0.0)),
                    'confidence': market_sentiment.get('confidence', 0.0)
                },
                'overall_sentiment': {
                    'score': (main_sentiment * 0.6 + sector_sentiment * 0.2 + market_sentiment.get('overall', 0.0) * 0.2),
                    'classification': classify_sentiment(main_sentiment * 0.6 + sector_sentiment * 0.2 + market_sentiment.get('overall', 0.0) * 0.2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment summary: {str(e)}")
            return {
                'stock_sentiment': {'score': 0.0, 'classification': 'Neutral'},
                'sector_sentiment': {'score': 0.0, 'classification': 'Neutral'},
                'market_sentiment': {'score': 0.0, 'classification': 'Neutral'},
                'overall_sentiment': {'score': 0.0, 'classification': 'Neutral'}
            }
    
    def _get_stock_sector(self, symbol: str) -> Dict[str, str]:
        """Get stock sector information (dummy implementation)"""
        try:
            # This would ideally fetch from a stock info API
            # For now, return dummy data
            sector_mapping = {
                'RELIANCE': {'sector': 'Energy'},
                'TCS': {'sector': 'IT'},
                'HDFCBANK': {'sector': 'Banking'},
                'INFY': {'sector': 'IT'},
                'HINDUNILVR': {'sector': 'FMCG'},
                'ICICIBANK': {'sector': 'Banking'},
                'KOTAKBANK': {'sector': 'Banking'},
                'BHARTIAIRTEL': {'sector': 'Telecom'},
                'ITC': {'sector': 'FMCG'},
                'SBIN': {'sector': 'Banking'}
            }
            
            clean_symbol = symbol.replace('.NS', '').replace('.BS', '')
            return sector_mapping.get(clean_symbol, {'sector': 'Other'})
            
        except Exception as e:
            logger.warning(f"Error getting stock sector: {str(e)}")
            return {'sector': 'Other'}