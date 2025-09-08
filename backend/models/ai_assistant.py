# models/ai_assistant.py

"""
AI Assistant for Stock Market Predictor
Provides intelligent responses to user queries about investing and market analysis
"""

import logging
import re
from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AIAssistant:
    """
    AI Assistant for providing investment advice and explanations
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.response_templates = self._initialize_response_templates()
        self.conversation_history = []
        
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize the knowledge base with financial terms and concepts"""
        return {
            'technical_indicators': {
                'rsi': {
                    'full_name': 'Relative Strength Index',
                    'description': 'Momentum oscillator measuring speed and change of price movements',
                    'range': '0-100',
                    'interpretation': {
                        'overbought': 'Above 70 - potential sell signal',
                        'oversold': 'Below 30 - potential buy signal',
                        'neutral': '30-70 - no clear signal'
                    }
                },
                'macd': {
                    'full_name': 'Moving Average Convergence Divergence',
                    'description': 'Trend-following momentum indicator',
                    'components': ['MACD Line', 'Signal Line', 'Histogram'],
                    'interpretation': {
                        'bullish': 'MACD line above signal line',
                        'bearish': 'MACD line below signal line'
                    }
                },
                'bollinger_bands': {
                    'full_name': 'Bollinger Bands',
                    'description': 'Volatility indicator with upper and lower bands',
                    'interpretation': {
                        'squeeze': 'Bands narrow - low volatility, potential breakout',
                        'expansion': 'Bands wide - high volatility',
                        'upper_touch': 'Price at upper band - potential resistance',
                        'lower_touch': 'Price at lower band - potential support'
                    }
                }
            },
            'chart_types': {
                'candlestick': 'Shows open, high, low, close prices in visual format',
                'renko': 'Price-based chart ignoring time, shows trend clearly',
                'kagi': 'Line chart that changes thickness based on price reversals',
                'point_figure': 'Uses X and O columns to show price movements'
            },
            'investment_strategies': {
                'value_investing': 'Buying undervalued stocks with strong fundamentals',
                'growth_investing': 'Investing in companies with high growth potential',
                'dividend_investing': 'Focus on stocks that pay regular dividends',
                'momentum_investing': 'Following trends and price momentum'
            },
            'risk_management': {
                'diversification': 'Spreading investments across different assets',
                'stop_loss': 'Automatic sell order to limit losses',
                'position_sizing': 'Determining how much to invest in each stock',
                'rebalancing': 'Adjusting portfolio allocation periodically'
            }
        }
    
    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """Initialize response templates for different query types"""
        return {
            'greeting': [
                "Hello! I'm your AI investment assistant. How can I help you with your investing journey today?",
                "Welcome! I'm here to help you with stock analysis, investment strategies, and market insights.",
                "Hi there! Ready to explore the world of investing together?"
            ],
            'technical_analysis': [
                "Let me explain this technical indicator for you:",
                "Here's what this chart pattern means:",
                "Technical analysis insight:"
            ],
            'investment_advice': [
                "Based on investment principles, here's my guidance:",
                "From an investment perspective:",
                "Consider these investment factors:"
            ],
            'risk_warning': [
                "⚠️ Important: Remember that all investments carry risk.",
                "⚠️ Please note: Past performance doesn't guarantee future results.",
                "⚠️ Reminder: Always do your own research before investing."
            ]
        }
    
    def get_response(self, user_query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate AI response to user query
        
        Args:
            user_query: User's question or statement
            context: Optional context information (portfolio, current stock, etc.)
            
        Returns:
            AI assistant response
        """
        try:
            # Store conversation
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'user_query': user_query,
                'context': context
            })
            
            # Normalize query
            query_lower = user_query.lower().strip()
            
            # Determine query type and generate response
            if self._is_greeting(query_lower):
                return self._handle_greeting()
                
            elif self._is_technical_question(query_lower):
                return self._handle_technical_question(query_lower, context)
                
            elif self._is_investment_question(query_lower):
                return self._handle_investment_question(query_lower, context)
                
            elif self._is_platform_question(query_lower):
                return self._handle_platform_question(query_lower)
                
            elif self._is_portfolio_question(query_lower):
                return self._handle_portfolio_question(query_lower, context)
                
            elif self._is_market_question(query_lower):
                return self._handle_market_question(query_lower)
                
            else:
                return self._handle_general_question(query_lower, context)
                
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return self._get_error_response()
    
    def _is_greeting(self, query: str) -> bool:
        """Check if query is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in query for greeting in greetings)
    
    def _is_technical_question(self, query: str) -> bool:
        """Check if query is about technical analysis"""
        technical_terms = [
            'rsi', 'macd', 'bollinger', 'moving average', 'chart', 'candlestick',
            'renko', 'kagi', 'point figure', 'support', 'resistance', 'trend',
            'indicator', 'overbought', 'oversold', 'breakout'
        ]
        return any(term in query for term in technical_terms)
    
    def _is_investment_question(self, query: str) -> bool:
        """Check if query is about investment strategies"""
        investment_terms = [
            'invest', 'strategy', 'portfolio', 'diversification', 'risk',
            'buy', 'sell', 'hold', 'stock pick', 'when to', 'how much',
            'allocation', 'rebalance', 'dividend', 'growth', 'value'
        ]
        return any(term in query for term in investment_terms)
    
    def _is_platform_question(self, query: str) -> bool:
        """Check if query is about platform usage"""
        platform_terms = [
            'how to use', 'navigate', 'feature', 'prediction', 'calibrate',
            'portfolio page', 'dashboard', 'chart type', 'add stock'
        ]
        return any(term in query for term in platform_terms)
    
    def _is_portfolio_question(self, query: str) -> bool:
        """Check if query is about portfolio management"""
        portfolio_terms = [
            'my portfolio', 'my stocks', 'performance', 'profit', 'loss',
            'holding', 'should i sell', 'should i buy more'
        ]
        return any(term in query for term in portfolio_terms)
    
    def _is_market_question(self, query: str) -> bool:
        """Check if query is about market conditions"""
        market_terms = [
            'market', 'nifty', 'sensex', 'economy', 'inflation', 'interest rate',
            'sector', 'bull market', 'bear market', 'correction'
        ]
        return any(term in query for term in market_terms)
    
    def _handle_greeting(self) -> str:
        """Handle greeting queries"""
        greeting = random.choice(self.response_templates['greeting'])
        
        suggestions = [
            "\n\n**I can help you with:**",
            "• **Technical Analysis** - RSI, MACD, chart patterns",
            "• **Investment Strategies** - Value, growth, dividend investing", 
            "• **Risk Management** - Diversification, stop-losses",
            "• **Platform Usage** - How to use prediction tools",
            "• **Portfolio Management** - Tracking and optimization",
            "\n*What would you like to explore first?*"
        ]
        
        return greeting + '\n'.join(suggestions)
    
    def _handle_technical_question(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Handle technical analysis questions"""
        response = random.choice(self.response_templates['technical_analysis'])
        
        # RSI questions
        if 'rsi' in query:
            rsi_info = self.knowledge_base['technical_indicators']['rsi']
            return f"""{response}

## RSI (Relative Strength Index)

**What it is:** {rsi_info['description']}

**Range:** {rsi_info['range']}

**How to interpret:**
• **Above 70:** {rsi_info['interpretation']['overbought']}
• **Below 30:** {rsi_info['interpretation']['oversold']}
• **30-70:** {rsi_info['interpretation']['neutral']}

**Trading Tips:**
• Look for divergences between price and RSI
• RSI above 50 generally indicates bullish momentum
• Use with other indicators for confirmation

{random.choice(self.response_templates['risk_warning'])}"""

        # MACD questions
        elif 'macd' in query:
            macd_info = self.knowledge_base['technical_indicators']['macd']
            return f"""{response}

## MACD (Moving Average Convergence Divergence)

**What it is:** {macd_info['description']}

**Components:**
• **MACD Line:** 12-day EMA minus 26-day EMA
• **Signal Line:** 9-day EMA of MACD line
• **Histogram:** MACD line minus Signal line

**Signals:**
• **Bullish:** {macd_info['interpretation']['bullish']}
• **Bearish:** {macd_info['interpretation']['bearish']}
• **Crossovers:** When MACD crosses signal line

**Best Practices:**
• Use on daily or longer timeframes
• Combine with trend analysis
• Watch for histogram convergence/divergence"""

        # Bollinger Bands
        elif 'bollinger' in query:
            bb_info = self.knowledge_base['technical_indicators']['bollinger_bands']
            return f"""{response}

## Bollinger Bands

**What it is:** {bb_info['description']}

**Interpretation:**
• **Band Squeeze:** {bb_info['interpretation']['squeeze']}
• **Band Expansion:** {bb_info['interpretation']['expansion']}
• **Upper Band Touch:** {bb_info['interpretation']['upper_touch']}
• **Lower Band Touch:** {bb_info['interpretation']['lower_touch']}

**Trading Strategies:**
• **Bollinger Bounce:** Buy at lower band, sell at upper band
• **Bollinger Squeeze:** Prepare for breakout when bands narrow
• **Band Walking:** Strong trends can walk along bands"""

        # Chart types
        elif any(chart in query for chart in ['candlestick', 'renko', 'kagi', 'point figure']):
            return self._explain_chart_types(query)
        
        else:
            return f"""{response}

## Technical Analysis Overview

Technical analysis studies price patterns and indicators to predict future movements.

**Key Concepts:**
• **Trend Analysis:** Direction of price movement
• **Support/Resistance:** Key price levels
• **Volume Analysis:** Trading activity confirmation
• **Momentum Indicators:** Speed of price changes

**Popular Indicators:**
• **RSI:** Overbought/oversold conditions
• **MACD:** Trend following momentum
• **Moving Averages:** Trend direction
• **Bollinger Bands:** Volatility and mean reversion

**Best Practices:**
• Use multiple indicators for confirmation
• Consider timeframe for your trading style
• Combine with fundamental analysis

*Ask me about any specific indicator for detailed explanation!*"""
    
    def _handle_investment_question(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Handle investment strategy questions"""
        response = random.choice(self.response_templates['investment_advice'])
        
        if any(word in query for word in ['beginner', 'start', 'new to']):
            return f"""{response}

## Investment Guide for Beginners

**🎯 Getting Started:**
1. **Emergency Fund First:** 6-12 months expenses in savings
2. **Start Small:** Begin with amounts you can afford to lose
3. **Educate Yourself:** Learn basics before investing large amounts
4. **Set Clear Goals:** Define your investment timeline and objectives

**📊 Investment Basics:**
• **Diversification:** Don't put all eggs in one basket
• **Time Horizon:** Longer timeline = more growth potential
• **Risk Tolerance:** Only take risks you're comfortable with
• **Regular Investing:** SIP approach reduces timing risk

**🏢 Stock Selection for Beginners:**
• **Blue Chip Stocks:** Start with established companies (TCS, HDFC Bank)
• **Index Funds:** Broad market exposure with lower risk
• **Sector Diversification:** IT, Banking, FMCG, Healthcare
• **Research:** Use our platform's AI predictions and analysis

**⚠️ Common Mistakes to Avoid:**
• Panic selling during market dips
• Trying to time the market perfectly
• Putting all money in one stock
• Following tips without research

{random.choice(self.response_templates['risk_warning'])}"""

        elif any(word in query for word in ['strategy', 'approach']):
            return f"""{response}

## Investment Strategies Overview

**🌱 Value Investing:**
• Buy undervalued quality companies
• Focus on fundamentals: P/E ratio, debt levels
• Long-term approach (Warren Buffett style)
• Best for: Patient investors

**🚀 Growth Investing:**
• Invest in fast-growing companies
• Higher potential returns, higher risk
• Focus on revenue/earnings growth
• Best for: Aggressive investors

**💰 Dividend Investing:**
• Focus on stocks paying regular dividends
• Provides steady income stream
• Lower volatility, slower growth
• Best for: Income-focused investors

**📈 Momentum Investing:**
• Follow price trends and market momentum
• Buy rising stocks, sell falling ones
• Requires active monitoring
• Best for: Active traders

**🎯 Index Investing:**
• Buy entire market through index funds
• Automatic diversification
• Lower fees, matches market returns
• Best for: Passive investors

**Choose based on your:**
• Risk tolerance
• Time commitment
• Financial goals
• Investment timeline"""

        elif any(word in query for word in ['risk', 'management', 'protect']):
            return self._explain_risk_management()
        
        else:
            return f"""{response}

## General Investment Principles

**🎯 Core Principles:**
• **Time in Market > Timing the Market**
• **Diversification is your best friend**
• **Invest regularly, not in lump sums**
• **Stay informed but don't panic**

**📊 Portfolio Allocation Tips:**
• **Age-based:** 100 minus your age in stocks
• **Risk-based:** Adjust based on risk tolerance
• **Goal-based:** Different goals, different strategies
• **Rebalance:** Review and adjust quarterly

**🔍 Research Checklist:**
• Company fundamentals (earnings, debt, growth)
• Industry trends and competition
• Management quality and vision
• Technical indicators and chart patterns

**💡 Use Our Platform:**
• AI predictions for price targets
• Technical analysis charts
• Portfolio tracking and recommendations
• Market news and sentiment analysis

*What specific aspect of investing would you like to explore further?*"""
    
    def _handle_platform_question(self, query: str) -> str:
        """Handle platform usage questions"""
        if any(word in query for word in ['predict', 'prediction']):
            return """## How to Use Stock Predictions

**🎯 Making Predictions:**
1. **Enter Stock:** Type symbol, name, or keywords (e.g., "TCS", "Reliance")
2. **Select Period:** Choose 5, 10, 15, or 30 days
3. **Click Predict:** Get AI-powered analysis
4. **Review Results:** Current price, predicted price, confidence level

**📊 Understanding Results:**
• **Confidence Level:** Higher is better (70%+ is good)
• **Price Change %:** Expected percentage movement
• **Recommendation:** BUY/SELL/HOLD based on analysis
• **Technical Indicators:** RSI, MACD, Bollinger Bands

**🔧 Calibration Feature:**
• Click "Calibrate Model" to improve accuracy
• Uses historical data to fine-tune predictions
• Run calibration when accuracy seems low

**📈 Chart Analysis:**
• Switch between chart types (Candlestick, Renko, etc.)
• Zoom and pan for detailed view
• Hover for exact values and explanations

**💡 Pro Tips:**
• Use predictions as guidance, not absolute truth
• Combine with your own research
• Check multiple timeframes
• Consider market conditions"""

        elif any(word in query for word in ['portfolio', 'manage']):
            return """## Portfolio Management Guide

**➕ Adding Stocks:**
1. Go to Portfolio page
2. Fill in stock details:
   • Symbol (e.g., TCS, RELIANCE)
   • Number of shares
   • Purchase price
   • Purchase date
3. Click "Add to Portfolio"

**📊 Portfolio Features:**
• **Real-time Tracking:** Live P&L calculations
• **Performance Metrics:** Total returns, percentages
• **AI Recommendations:** Hold/Sell suggestions
• **Historical Data:** Highest/lowest since purchase

**🎯 Smart Recommendations:**
• **HOLD:** Keep current position
• **PARTIAL SELL:** Book some profits
• **SELL:** Exit position
• **BUY MORE:** Add on dips

**📈 Analysis Tools:**
• Click "Stock Analysis" for detailed prediction
• View technical charts and indicators
• Get sentiment analysis
• Track news impact

**💡 Best Practices:**
• Review portfolio monthly
• Rebalance when needed
• Set stop-losses for risk management
• Don't put all money in one stock"""

        else:
            return """## Platform Navigation Guide

**🏠 Dashboard:**
• Main prediction interface
• Enter stocks and get AI analysis
• View charts and technical indicators
• Access top performing stocks

**💼 Portfolio:**
• Add and track your investments
• View profit/loss in real-time
• Get personalized recommendations
• Detailed stock analysis

**📰 News:**
• Latest market news
• Sentiment analysis
• Filter by categories
• AI explanations of market impact

**🤖 AI Features:**
• Stock price predictions
• Technical chart analysis
• Portfolio recommendations
• Market sentiment analysis
• Intelligent chat assistance

**🔧 Tools & Settings:**
• Dark/Light theme toggle
• Chart zoom and pan controls
• Model calibration options
• Historical data views

**💡 Quick Tips:**
• Use search to find stocks quickly
• Try different chart types for insights
• Check confidence levels on predictions
• Ask me anything in this chat!"""
    
    def _handle_portfolio_question(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Handle portfolio-specific questions"""
        if context and 'portfolio' in context:
            portfolio_data = context['portfolio']
            # Provide personalized advice based on portfolio
            return self._generate_portfolio_advice(portfolio_data)
        
        return """## Portfolio Management Advice

**🎯 Portfolio Optimization:**
• **Diversification:** Spread across 8-12 stocks minimum
• **Sector Balance:** Don't concentrate in one sector
• **Size Mix:** Combine large, mid, and small cap stocks
• **Review Frequency:** Monthly assessment recommended

**📊 Performance Tracking:**
• Monitor total returns vs benchmark (Nifty 50)
• Track individual stock performance
• Set alerts for significant price changes
• Document investment thesis for each stock

**⚖️ Rebalancing Strategy:**
• Trim positions that exceed 10% of portfolio
• Add to underperforming quality stocks
• Maintain target allocation percentages
• Consider tax implications

**🚫 When to Sell:**
• Fundamental deterioration in company
• Better opportunities available
• Reached price target (book profits)
• Risk tolerance changed

**💡 Use Our Tools:**
• Portfolio tracker shows real-time P&L
• AI recommendations for each holding
• Technical analysis for entry/exit points
• News sentiment for decision support

*Share your portfolio details for personalized advice!*"""
    
    def _handle_market_question(self, query: str) -> str:
        """Handle market-related questions"""
        if any(word in query for word in ['nifty', 'sensex', 'index']):
            return """## Indian Stock Market Indices

**📊 Major Indices:**

**NIFTY 50:**
• Top 50 companies by market cap
• Benchmark for large-cap performance
• Sectors: IT, Banking, Consumer, Energy
• Good for: Long-term wealth creation

**SENSEX:**
• 30 most actively traded stocks on BSE
• Oldest index in India
• Market sentiment indicator
• Good for: Market direction reference

**Sector Indices:**
• **Bank Nifty:** Banking sector performance
• **IT Index:** Technology stocks
• **Pharma Index:** Pharmaceutical companies
• **Auto Index:** Automotive sector

**📈 Investment Options:**
• **Index Funds:** Passive investment in indices
• **ETFs:** Trade like stocks, track indices
• **Index Futures:** Derivatives for hedging
• **Direct Stocks:** Pick individual companies

**💡 Index Investing Benefits:**
• Instant diversification
• Lower costs than active funds
• Matches market returns
• Reduces single-stock risk

**Current Market Trends:**
• Check our dashboard for live index values
• Use technical analysis for timing
• Consider SIP for regular investment"""

        elif any(word in query for word in ['sector', 'industry']):
            return """## Sector Analysis Guide

**🏦 Banking Sector:**
• **Leaders:** HDFC Bank, ICICI Bank, Kotak Bank
• **Drivers:** Interest rates, credit growth, NPAs
• **Outlook:** Benefits from economic growth
• **Risk:** Interest rate sensitivity

**💻 IT Sector:**
• **Leaders:** TCS, Infosys, Wipro, HCL Tech
• **Drivers:** Digital transformation, AI adoption
• **Outlook:** Strong global demand
• **Risk:** Currency fluctuation, visa issues

**🛍️ FMCG Sector:**
• **Leaders:** Hindustan Unilever, ITC, Britannia
• **Drivers:** Rural demand, consumer spending
• **Outlook:** Stable, defensive sector
• **Risk:** Raw material cost inflation

**⚡ Energy Sector:**
• **Leaders:** Reliance, ONGC, BPCL, NTPC
• **Drivers:** Oil prices, government policies
• **Outlook:** Transition to renewables
• **Risk:** Commodity price volatility

**🏥 Healthcare/Pharma:**
• **Leaders:** Sun Pharma, Dr. Reddy's, Cipla
• **Drivers:** Global demand, R&D capabilities
• **Outlook:** Aging population tailwinds
• **Risk:** Regulatory changes, patent cliffs

**💡 Sector Rotation Strategy:**
• Rotate based on economic cycles
• Use our sector performance tracking
• Monitor policy changes and regulations
• Diversify across multiple sectors"""

        else:
            return """## Market Analysis Overview

**📊 Market Conditions:**
• **Bull Market:** Rising prices, optimism
• **Bear Market:** Falling prices, pessimism  
• **Correction:** 10-20% decline from highs
• **Volatility:** Normal price fluctuations

**🎯 Market Factors:**
• **Economic Growth:** GDP, industrial production
• **Interest Rates:** RBI policy decisions
• **Inflation:** Price stability concerns
• **Global Events:** International market trends

**📈 Investment Climate:**
• **FII Flows:** Foreign institutional investment
• **DII Activity:** Domestic institutional buying
• **Retail Participation:** Individual investor activity
• **IPO Market:** New listings and demand

**🔍 Market Analysis Tools:**
• Technical indicators (RSI, MACD)
• Price-to-earnings ratios
• Market breadth indicators
• Sector rotation patterns

**💡 Market Timing Tips:**
• Don't try to time perfectly
• Use SIP for regular investment
• Buy quality stocks in corrections
• Stay informed but don't panic

*Use our platform's technical analysis and AI predictions to make informed decisions!*"""
    
    def _explain_chart_types(self, query: str) -> str:
        """Explain different chart types"""
        if 'candlestick' in query:
            return """## Candlestick Charts

**What it shows:** Each candle represents one time period (day/hour) with:
• **Open:** Starting price
• **High:** Highest price  
• **Low:** Lowest price
• **Close:** Ending price

**Colors:**
• **Green/White:** Close > Open (bullish)
• **Red/Black:** Close < Open (bearish)

**Key Patterns:**
• **Doji:** Open = Close (indecision)
• **Hammer:** Long lower shadow (reversal)
• **Engulfing:** Large candle engulfs previous (reversal)
• **Star:** Small body with gaps (reversal)

**Best for:**
• Detailed price action analysis
• Pattern recognition
• Entry/exit timing
• Short to medium-term trading"""

        elif 'renko' in query:
            return """## Renko Charts

**What it shows:** Price-based bricks ignoring time
• Each brick = fixed price movement
• Only shows significant price changes
• Filters out market noise

**How it works:**
• **Up Brick:** Price rises by brick size
• **Down Brick:** Price falls by brick size
• **No Time:** Only price matters

**Advantages:**
• Clear trend identification
• Removes minor fluctuations
• Easy to spot reversals
• Less emotional trading

**Best for:**
• Trend following strategies
• Reducing noise in analysis
• Long-term position trading
• Beginner-friendly analysis"""

        else:
            return """## Chart Types Overview

**📊 Available Chart Types:**

**Candlestick Charts:**
• Most detailed price information
• Shows open, high, low, close
• Best for pattern recognition

**Renko Charts:**
• Price-based bricks, no time axis
• Filters market noise
• Clear trend identification

**Kagi Charts:**
• Line thickness changes with reversals
• Shows supply/demand shifts
• Good for trend analysis

**Point & Figure:**
• Uses X's and O's for price moves
• Eliminates time and volume
• Focuses on significant price changes

**💡 Choosing the Right Chart:**
• **Day Trading:** Candlestick (detailed)
• **Trend Following:** Renko (clean)
• **Swing Trading:** Candlestick + indicators
• **Long-term:** Any type with longer timeframes

*Try different chart types on our platform to see which works best for your analysis style!*"""
    
    def _explain_risk_management(self) -> str:
        """Explain risk management concepts"""
        return """## Risk Management Guide

**🛡️ Core Principles:**

**Position Sizing:**
• Never risk more than 2-3% per trade
• Diversify across 10+ stocks minimum
• Limit single stock to 10% of portfolio
• Adjust size based on volatility

**Stop-Loss Strategy:**
• Set stop-loss at 15-20% below entry
• Use technical levels (support/resistance)
• Trailing stops for profit protection
• Honor stops without emotions

**Diversification:**
• **Across Sectors:** IT, Banking, FMCG, etc.
• **Market Caps:** Large, mid, small cap mix
• **Investment Styles:** Growth, value, dividend
• **Time Horizons:** Short, medium, long-term

**Portfolio Allocation:**
• **Age Rule:** 100 - age = % in stocks
• **Risk Tolerance:** Conservative to aggressive
• **Emergency Fund:** 6-12 months expenses separate
• **Rebalancing:** Quarterly review and adjust

**🚨 Warning Signs:**
• Overconcentration in one stock/sector
• Borrowing money to invest
• Ignoring stop-losses consistently
• Making emotional decisions

**💡 Risk Assessment:**
• **Low Risk:** Blue-chip stocks, index funds
• **Medium Risk:** Quality mid-cap stocks
• **High Risk:** Small-cap, sector bets
• **Very High Risk:** Penny stocks, speculation

**Tools for Risk Management:**
• Our portfolio tracker shows concentration
• AI recommendations flag high-risk positions
• Technical analysis for stop-loss levels
• News alerts for company-specific risks

{random.choice(self.response_templates['risk_warning'])}"""
    
    def _handle_general_question(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Handle general questions"""
        return """## I'm Here to Help! 🤖

I can assist you with various aspects of investing and our platform:

**📈 Investment Topics:**
• Stock analysis and predictions
• Technical indicators (RSI, MACD, etc.)
• Portfolio management strategies
• Risk management techniques
• Market trends and sectors

**🛠️ Platform Features:**
• How to use prediction tools
• Portfolio tracking and management
• Chart analysis and interpretation
• News and sentiment analysis

**📚 Learning Resources:**
• Investment basics for beginners
• Advanced trading strategies
• Market terminology explanations
• Best practices and tips

**💡 Example Questions:**
• "How do I interpret RSI values?"
• "What's the best portfolio allocation?"
• "How accurate are the predictions?"
• "Should I sell my losing stocks?"
• "How to use Renko charts?"

*Feel free to ask me anything specific about investing, market analysis, or using our platform!*

**Quick Tips:**
• Be specific in your questions for better help
• Mention your experience level (beginner/advanced)
• Include context about your situation when relevant"""
    
    def _generate_portfolio_advice(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate personalized portfolio advice"""
        try:
            total_value = portfolio_data.get('total_value', 0)
            total_pl = portfolio_data.get('total_pl', 0)
            pl_pct = portfolio_data.get('pl_pct', 0)
            holdings_count = portfolio_data.get('holdings_count', 0)
            
            advice = "## Personalized Portfolio Analysis\n\n"
            
            # Portfolio size analysis
            if holdings_count < 5:
                advice += "**🎯 Diversification Alert:** Consider adding more stocks (8-12 recommended) to reduce risk.\n\n"
            elif holdings_count > 20:
                advice += "**📊 Portfolio Focus:** You might want to consolidate to 10-15 best positions for better tracking.\n\n"
            
            # Performance analysis
            if pl_pct > 15:
                advice += f"**🎉 Great Performance:** Your portfolio is up {pl_pct:.1f}%! Consider booking partial profits on big winners.\n\n"
            elif pl_pct < -10:
                advice += f"**⚠️ Portfolio Review:** Down {abs(pl_pct):.1f}%. Review fundamentals and consider stop-losses.\n\n"
            else:
                advice += f"**📈 Steady Progress:** Portfolio showing {pl_pct:.1f}% return. Stay the course!\n\n"
            
            # General recommendations
            advice += """**💡 Personalized Recommendations:**
• Use our AI predictions for each holding
• Set stop-losses at -20% from purchase price  
• Rebalance monthly if any stock exceeds 15% allocation
• Consider our top-performing stocks for new additions

**📊 Next Steps:**
• Review individual stock recommendations
• Check technical charts for timing
• Monitor news sentiment for your holdings
• Set price alerts for key levels"""
            
            return advice
            
        except Exception as e:
            logger.error(f"Error generating portfolio advice: {str(e)}")
            return self._handle_portfolio_question("", None)
    
    def _get_error_response(self) -> str:
        """Get error response when something goes wrong"""
        return """I apologize, but I encountered an error processing your question. 

Let me help you in other ways:

**🤖 I can assist with:**
• Stock analysis and predictions
• Technical chart interpretation  
• Investment strategies and advice
• Platform navigation and features
• Portfolio management tips

**💡 Try asking:**
• "How do I use the prediction tool?"
• "What does RSI mean?"
• "How should I manage my portfolio?"
• "Explain candlestick charts"

*Please rephrase your question and I'll do my best to help!*"""
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation history"""
        try:
            if not self.conversation_history:
                return {'message': 'No conversation history yet'}
            
            recent_queries = [entry['user_query'] for entry in self.conversation_history[-5:]]
            query_types = []
            
            for query in recent_queries:
                if self._is_technical_question(query.lower()):
                    query_types.append('technical')
                elif self._is_investment_question(query.lower()):
                    query_types.append('investment')
                elif self._is_platform_question(query.lower()):
                    query_types.append('platform')
                else:
                    query_types.append('general')
            
            return {
                'total_queries': len(self.conversation_history),
                'recent_queries': recent_queries,
                'query_types': query_types,
                'main_interests': max(set(query_types), key=query_types.count) if query_types else 'general'
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {str(e)}")
            return {'message': 'Error retrieving conversation history'}