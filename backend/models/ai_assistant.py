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
        Generate AI response to user query using advanced AI models
        
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
            
            # Detect language
            detected_lang = self._detect_language(user_query)
            
            # Generate intelligent response using AI
            response = self._generate_intelligent_response(user_query, detected_lang, context)
            
            return response
                
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return self._get_error_response()
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'en'  # Default to English
    
    def _generate_intelligent_response(self, query: str, language: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate intelligent response using AI models - API ONLY"""
        try:
            # Create a comprehensive prompt for the AI
            system_prompt = self._create_system_prompt(language, context)
            
            # Only use external APIs - no hardcoded responses
            response = None
            
            # Try external APIs only
            try:
                response = self._use_external_apis(query, system_prompt, language)
                if response and len(response.strip()) > 10:
                    return response
            except Exception as e:
                logger.debug(f"External APIs failed: {e}")
            
            # If API fails, return a simple message asking to try again
            return "I'm having trouble connecting to the AI service. Please try again in a moment."
            
        except Exception as e:
            logger.error(f"Error in intelligent response generation: {e}")
            return "I'm having trouble connecting to the AI service. Please try again in a moment."
    
    def _create_system_prompt(self, language: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Create a comprehensive system prompt for the AI"""
        base_prompt = f"""You are an expert AI financial advisor and stock market analyst. You can communicate in multiple languages including English, Hindi, Telugu, Tamil, Spanish, French, and more.

Your expertise includes:
- Stock market analysis and predictions
- Technical analysis (RSI, MACD, Bollinger Bands, etc.)
- Investment strategies and portfolio management
- Market trends and economic indicators
- Risk assessment and financial planning
- Cryptocurrency and alternative investments

Current context: {context or 'General market discussion'}

Guidelines:
1. Always respond in the same language as the user's question
2. Provide accurate, helpful financial advice
3. Be conversational and engaging
4. Use emojis appropriately (📈📉💰💡)
5. If unsure about specific stock prices, mention that prices change frequently
6. Always include appropriate disclaimers about investment risks
7. Be encouraging and supportive
8. Ask follow-up questions when appropriate

Respond naturally and helpfully to the user's question."""

        return base_prompt
    
    def _use_local_ai(self, query: str, system_prompt: str, language: str) -> str:
        """Use local AI model for response generation - DISABLED to force API usage"""
        # Return None to force external API usage
        return None
    
    def _use_external_apis(self, query: str, system_prompt: str, language: str) -> str:
        """Use external APIs for response generation"""
        try:
            # Import the OpenRouter function from app.py
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from app import ask_openrouter_grok
            
            # Use OpenRouter Grok API
            response = ask_openrouter_grok(query, language)
            if response and len(response.strip()) > 10:
                logger.info(f"OpenRouter Grok API returned response for: {query[:50]}...")
                return response
            else:
                logger.warning(f"OpenRouter Grok API returned empty or short response")
                return None
                
        except Exception as e:
            logger.error(f"External API error: {e}")
            return None
    
    def _enhanced_rule_based_response(self, query: str, language: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Enhanced rule-based response system - DISABLED to force API usage"""
        # Return None to force external API usage
        return None
    
    def _generate_stock_analysis_response(self, query: str, language: str) -> str:
        """Generate stock analysis response"""
        responses = {
            'en': "📊 I'd be happy to analyze stocks for you! To give you the most accurate analysis, I can help you with:\n\n• Technical indicators (RSI, MACD, Bollinger Bands)\n• Price predictions and trends\n• Risk assessment\n• Entry/exit strategies\n\nWhich specific stock would you like me to analyze?",
            'hi': "📊 मैं आपके लिए स्टॉक का विश्लेषण करने में खुशी होगी! सबसे सटीक विश्लेषण देने के लिए, मैं आपकी मदद कर सकता हूं:\n\n• तकनीकी संकेतक (RSI, MACD, Bollinger Bands)\n• मूल्य भविष्यवाणी और रुझान\n• जोखिम मूल्यांकन\n• प्रवेश/निकास रणनीतियां\n\nआप किस विशिष्ट स्टॉक का विश्लेषण करना चाहते हैं?",
            'te': "📊 నేను మీ కోసం స్టాక్లను విశ్లేషించడంలో సంతోషిస్తాను! అత్యంత ఖచ్చితమైన విశ్లేషణ ఇవ్వడానికి, నేను మీకు సహాయపడగలను:\n\n• సాంకేతిక సూచికలు (RSI, MACD, Bollinger Bands)\n• ధర అంచనాలు మరియు ధోరణులు\n• రిస్క్ అసెస్మెంట్\n• ఎంట్రీ/ఎగ్జిట్ వ్యూహాలు\n\nమీరు ఏ నిర్దిష్ట స్టాక్ విశ్లేషించాలనుకుంటున్నారు?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_market_response(self, query: str, language: str) -> str:
        """Generate market analysis response"""
        responses = {
            'en': "📈 Market analysis is crucial for investment decisions! I can help you understand:\n\n• Current market trends and sentiment\n• NIFTY and SENSEX movements\n• Sector-wise performance\n• Global market influences\n• Economic indicators\n\nWhat specific aspect of the market interests you?",
            'hi': "📈 निवेश निर्णयों के लिए बाजार विश्लेषण महत्वपूर्ण है! मैं आपको समझने में मदद कर सकता हूं:\n\n• वर्तमान बाजार रुझान और भावना\n• NIFTY और SENSEX आंदोलन\n• क्षेत्र-वार प्रदर्शन\n• वैश्विक बाजार प्रभाव\n• आर्थिक संकेतक\n\nबाजार का कौन सा विशिष्ट पहलू आपको रुचिकर लगता है?",
            'te': "📈 పెట్టుబడి నిర్ణయాలకు మార్కెట్ విశ్లేషణ కీలకం! నేను మీకు అర్థం చేసుకోవడంలో సహాయపడగలను:\n\n• ప్రస్తుత మార్కెట్ ధోరణులు మరియు భావన\n• NIFTY మరియు SENSEX కదలికలు\n• సెక్టార్-వారి పనితీరు\n• గ్లోబల్ మార్కెట్ ప్రభావాలు\n• ఆర్థిక సూచికలు\n\nమార్కెట్ యొక్క ఏ నిర్దిష్ట అంశం మీకు ఆసక్తి కలిగిస్తుంది?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_technical_analysis_response(self, query: str, language: str) -> str:
        """Generate technical analysis response"""
        responses = {
            'en': "🔧 Technical analysis is a powerful tool for traders! I can explain:\n\n• RSI (Relative Strength Index) - momentum indicator\n• MACD (Moving Average Convergence Divergence)\n• Bollinger Bands - volatility indicator\n• Support and Resistance levels\n• Chart patterns and candlestick analysis\n\nWhich technical indicator would you like to learn about?",
            'hi': "🔧 तकनीकी विश्लेषण व्यापारियों के लिए एक शक्तिशाली उपकरण है! मैं समझा सकता हूं:\n\n• RSI (Relative Strength Index) - गति संकेतक\n• MACD (Moving Average Convergence Divergence)\n• Bollinger Bands - अस्थिरता संकेतक\n• समर्थन और प्रतिरोध स्तर\n• चार्ट पैटर्न और कैंडलस्टिक विश्लेषण\n\nआप किस तकनीकी संकेतक के बारे में जानना चाहते हैं?",
            'te': "🔧 సాంకేతిక విశ్లేషణ వ్యాపారులకు శక్తివంతమైన సాధనం! నేను వివరించగలను:\n\n• RSI (Relative Strength Index) - మొమెంటమ్ సూచిక\n• MACD (Moving Average Convergence Divergence)\n• Bollinger Bands - వేరియబిలిటీ సూచిక\n• సపోర్ట్ మరియు రెసిస్టెన్స్ స్థాయిలు\n• చార్ట్ ప్యాటర్న్లు మరియు క్యాండిల్ స్టిక్ విశ్లేషణ\n\nమీరు ఏ సాంకేతిక సూచిక గురించి తెలుసుకోవాలనుకుంటున్నారు?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_investment_advice_response(self, query: str, language: str) -> str:
        """Generate investment advice response"""
        responses = {
            'en': "💰 Smart investing requires careful planning! I can guide you on:\n\n• Portfolio diversification strategies\n• Risk management techniques\n• Long-term vs short-term investments\n• Sector allocation\n• Market timing considerations\n• Tax-efficient investing\n\nWhat's your investment goal and risk tolerance?",
            'hi': "💰 स्मार्ट निवेश के लिए सावधानीपूर्वक योजना की आवश्यकता है! मैं आपका मार्गदर्शन कर सकता हूं:\n\n• पोर्टफोलियो विविधीकरण रणनीतियां\n• जोखिम प्रबंधन तकनीक\n• दीर्घकालिक बनाम अल्पकालिक निवेश\n• क्षेत्र आवंटन\n• बाजार समय विचार\n• कर-कुशल निवेश\n\nआपका निवेश लक्ष्य और जोखिम सहनशीलता क्या है?",
            'te': "💰 స్మార్ట్ పెట్టుబడికి జాగ్రత్తగా ప్లానింగ్ అవసరం! నేను మీకు మార్గదర్శకత్వం చేయగలను:\n\n• పోర్ట్ఫోలియో డైవర్సిఫికేషన్ వ్యూహాలు\n• రిస్క్ మేనేజ్మెంట్ టెక్నిక్స్\n• దీర్ఘకాలిక vs స్వల్పకాలిక పెట్టుబడులు\n• సెక్టార్ అలోకేషన్\n• మార్కెట్ టైమింగ్ పరిగణనలు\n• టాక్స్-ఎఫిషియంట్ పెట్టుబడి\n\nమీ పెట్టుబడి లక్ష్యం మరియు రిస్క్ టాలరెన్స్ ఏమిటి?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_stock_specific_response(self, query: str, language: str) -> str:
        """Generate stock-specific response"""
        responses = {
            'en': "📊 Great choice! I can provide detailed analysis for this stock including:\n\n• Current price trends and momentum\n• Technical indicators (RSI, MACD, Bollinger Bands)\n• Support and resistance levels\n• Volume analysis\n• Price predictions\n• Risk assessment\n\nWould you like me to analyze this stock's current performance?",
            'hi': "📊 बेहतरीन विकल्प! मैं इस स्टॉक के लिए विस्तृत विश्लेषण प्रदान कर सकता हूं जिसमें शामिल है:\n\n• वर्तमान मूल्य रुझान और गति\n• तकनीकी संकेतक (RSI, MACD, Bollinger Bands)\n• समर्थन और प्रतिरोध स्तर\n• वॉल्यूम विश्लेषण\n• मूल्य भविष्यवाणी\n• जोखिम मूल्यांकन\n\nक्या आप चाहते हैं कि मैं इस स्टॉक के वर्तमान प्रदर्शन का विश्लेषण करूं?",
            'te': "📊 గొప్ప ఎంపిక! నేను ఈ స్టాక్ కోసం వివరణాత్మక విశ్లేషణను అందించగలను:\n\n• ప్రస్తుత ధర ధోరణులు మరియు మొమెంటమ్\n• సాంకేతిక సూచికలు (RSI, MACD, Bollinger Bands)\n• సపోర్ట్ మరియు రెసిస్టెన్స్ స్థాయిలు\n• వాల్యూమ్ విశ్లేషణ\n• ధర అంచనాలు\n• రిస్క్ అసెస్మెంట్\n\nఈ స్టాక్ యొక్క ప్రస్తుత పనితీరును విశ్లేషించాలనుకుంటున్నారా?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_market_trend_response(self, query: str, language: str) -> str:
        """Generate market trend response"""
        responses = {
            'en': "📈 Market trends are constantly evolving! Current market analysis shows:\n\n• Bull markets: Rising prices, positive sentiment\n• Bear markets: Falling prices, negative sentiment\n• Sideways markets: Range-bound trading\n• Volatility indicators and market sentiment\n• Sector rotation patterns\n\nWhat specific trend are you interested in analyzing?",
            'hi': "📈 बाजार के रुझान लगातार विकसित हो रहे हैं! वर्तमान बाजार विश्लेषण दिखाता है:\n\n• बुल मार्केट: बढ़ती कीमतें, सकारात्मक भावना\n• बियर मार्केट: गिरती कीमतें, नकारात्मक भावना\n• साइडवेज मार्केट: रेंज-बाउंड ट्रेडिंग\n• अस्थिरता संकेतक और बाजार भावना\n• क्षेत्र रोटेशन पैटर्न\n\nआप किस विशिष्ट रुझान का विश्लेषण करने में रुचि रखते हैं?",
            'te': "📈 మార్కెట్ ధోరణులు నిరంతరం అభివృద్ధి చెందుతున్నాయి! ప్రస్తుత మార్కెట్ విశ్లేషణ చూపిస్తుంది:\n\n• బుల్ మార్కెట్లు: పెరుగుతున్న ధరలు, సానుకూల భావన\n• బేర్ మార్కెట్లు: పడిపోతున్న ధరలు, ప్రతికూల భావన\n• సైడ్వేస్ మార్కెట్లు: రేంజ్-బౌండ్ ట్రేడింగ్\n• వేరియబిలిటీ సూచికలు మరియు మార్కెట్ భావన\n• సెక్టార్ రోటేషన్ ప్యాటర్న్లు\n\nమీరు ఏ నిర్దిష్ట ధోరణిని విశ్లేషించాలనుకుంటున్నారు?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_risk_assessment_response(self, query: str, language: str) -> str:
        """Generate risk assessment response"""
        responses = {
            'en': "⚠️ Risk assessment is crucial for successful investing! I can help you understand:\n\n• Different types of investment risks\n• Risk tolerance evaluation\n• Portfolio diversification strategies\n• Safe vs volatile investments\n• Risk-reward ratios\n• Market volatility indicators\n\nWhat's your current risk tolerance level?",
            'hi': "⚠️ सफल निवेश के लिए जोखिम मूल्यांकन महत्वपूर्ण है! मैं आपको समझने में मदद कर सकता हूं:\n\n• विभिन्न प्रकार के निवेश जोखिम\n• जोखिम सहनशीलता मूल्यांकन\n• पोर्टफोलियो विविधीकरण रणनीतियां\n• सुरक्षित बनाम अस्थिर निवेश\n• जोखिम-पुरस्कार अनुपात\n• बाजार अस्थिरता संकेतक\n\nआपका वर्तमान जोखिम सहनशीलता स्तर क्या है?",
            'te': "⚠️ విజయవంతమైన పెట్టుబడికి రిస్క్ అసెస్మెంట్ కీలకం! నేను మీకు అర్థం చేసుకోవడంలో సహాయపడగలను:\n\n• వివిధ రకాల పెట్టుబడి రిస్క్లు\n• రిస్క్ టాలరెన్స్ ఎవాల్యుయేషన్\n• పోర్ట్ఫోలియో డైవర్సిఫికేషన్ వ్యూహాలు\n• సేఫ్ vs వోలాటైల్ పెట్టుబడులు\n• రిస్క్-రివార్డ్ రేషియోలు\n• మార్కెట్ వేరియబిలిటీ సూచికలు\n\nమీ ప్రస్తుత రిస్క్ టాలరెన్స్ స్థాయి ఏమిటి?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_default_intelligent_response(self, query: str, language: str) -> str:
        """Generate default intelligent response"""
        responses = {
            'en': f"🤖 I understand you're asking about: '{query}'\n\nI'm here to help with all your financial and investment questions! I can assist with:\n\n• Stock analysis and predictions 📊\n• Market trends and insights 📈\n• Technical analysis 🔧\n• Investment strategies 💰\n• Portfolio management 📋\n• Risk assessment ⚠️\n\nCould you be more specific about what you'd like to know?",
            'hi': f"🤖 मैं समझता हूं कि आप पूछ रहे हैं: '{query}'\n\nमैं आपके सभी वित्तीय और निवेश प्रश्नों में मदद के लिए यहां हूं! मैं सहायता कर सकता हूं:\n\n• स्टॉक विश्लेषण और भविष्यवाणी 📊\n• बाजार रुझान और अंतर्दृष्टि 📈\n• तकनीकी विश्लेषण 🔧\n• निवेश रणनीतियां 💰\n• पोर्टफोलियो प्रबंधन 📋\n• जोखिम मूल्यांकन ⚠️\n\nक्या आप और अधिक विशिष्ट हो सकते हैं कि आप क्या जानना चाहते हैं?",
            'te': f"🤖 నేను అర్థం చేసుకున్నాను మీరు అడుగుతున్నది: '{query}'\n\nమీ అన్ని ఆర్థిక మరియు పెట్టుబడి ప్రశ్నలలో సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను! నేను సహాయపడగలను:\n\n• స్టాక్ విశ్లేషణ మరియు అంచనాలు 📊\n• మార్కెట్ ధోరణులు మరియు అంతర్దృష్టులు 📈\n• సాంకేతిక విశ్లేషణ 🔧\n• పెట్టుబడి వ్యూహాలు 💰\n• పోర్ట్ఫోలియో నిర్వహణ 📋\n• రిస్క్ అసెస్మెంట్ ⚠️\n\nమీరు ఏమి తెలుసుకోవాలనుకుంటున్నారో మరింత నిర్దిష్టంగా చెప్పగలరా?"
        }
        return responses.get(language, responses['en'])
    
    def _generate_general_intelligent_response(self, query: str, language: str) -> str:
        """Generate general intelligent response"""
        return self._generate_default_intelligent_response(query, language)
    
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
