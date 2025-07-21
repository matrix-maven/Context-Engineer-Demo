# Context Engineering Demo

A Streamlit application demonstrating how AI responses transform when context is applied across different industries.

## 🚀 Quick Start

### Demo Runner (Recommended)

Use the demo runner for easy version switching:

```bash
# Install dependencies
pip install -r requirements.txt

# Run static version (safe fallback)
python run_demo.py static

# Run AI-powered version (requires API key)
python run_demo.py ai
```

### Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- **Streamlit**: Web application framework
- **OpenAI, Anthropic, Gemini**: AI provider libraries
- **Faker**: Realistic data generation for context
- **Pydantic**: Configuration validation and settings management
- **Structlog**: Enhanced logging capabilities

**Optional Dependencies:**
- **pytest**: Testing framework with async support
- **responses**: HTTP mocking for testing
- **Development tools**: black, flake8, mypy (commented out by default)

> 📚 **Detailed Installation Guide**: See [Dependencies and Installation Guide](docs/dependencies-and-installation.md) for comprehensive installation instructions, troubleshooting, and dependency details.

#### 2. Choose Your Version

**Option A: Static Demo (Safe Fallback)**
```bash
streamlit run app.py
```
- Uses hardcoded responses
- No API key required
- Perfect for demos and testing

**Option B: AI-Powered Demo (Full Experience)**
```bash
# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_openai_api_key_here

# Validate setup (optional)
python validate_openai.py

# Run AI-powered version
streamlit run main.py
```

#### 3. Advanced Configuration (AI Version Only)

For the AI-powered version, you can configure multiple providers:

```bash
# Required: At least one AI provider
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OR  
GEMINI_API_KEY=your_gemini_api_key_here
# OR
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

#### 4. Validate Configuration (AI Version)

The application includes a comprehensive validation system to test all components:

```bash
# Validate entire application configuration
python config/validation.py

# Test specific AI providers and services
python utils/validate_openai.py           # OpenAI provider validation
python utils/validate_anthropic.py        # Anthropic provider validation
python utils/validate_prompt_service.py   # Prompt Service validation
python utils/validate_context_service.py  # Context Service validation
python utils/validate_error_handling.py   # Error handling system validation
python utils/validate_main_integration.py # Main application integration validation
python utils/validate_response_formatting.py # Response Format Guidelines validation
```

**Recent Improvements**: All validation scripts now use standardized path resolution for reliable execution from any directory. See [Validation System Improvements](docs/validation-system-improvements.md) for detailed information about the validation system enhancements.

**Key Benefits of the Enhanced Validation System:**
- ✅ **Reliable Execution**: Scripts work from any directory within the project
- ✅ **Consistent Import Behavior**: Standardized path resolution across all scripts
- ✅ **CI/CD Ready**: Proper exit codes and environment variable support
- ✅ **Comprehensive Testing**: Each script tests specific functionality thoroughly
- ✅ **Clear Feedback**: Color-coded output with detailed error messages

#### 5. Configuration Options

The AI-powered version supports multiple configuration options:

```bash
# AI Provider Selection (defaults to OpenAI if multiple are configured)
AI_PROVIDER=openai              # Options: openai, anthropic, gemini, openrouter

# Global AI Settings
AI_TEMPERATURE=0.7              # Response creativity (0.0-2.0)
AI_MAX_TOKENS=500              # Maximum response length
AI_TIMEOUT=30                  # Request timeout in seconds

# Performance Settings
ENABLE_CACHING=true            # Enable response caching
CACHE_TTL=3600                # Cache time-to-live in seconds

# Logging
LOG_LEVEL=INFO                 # Logging level (DEBUG, INFO, WARNING, ERROR)
DEBUG=false                    # Enable debug mode
```

## 🏗️ Project Structure

```
├── app.py                    # Static demo version (safe fallback)
├── main.py                   # AI-powered demo version (full experience)
├── run_demo.py              # Demo runner script for easy version switching
├── config/                   # Configuration management
│   ├── __init__.py
│   ├── settings.py          # Application settings with Pydantic validation
│   ├── ai_config.py         # AI provider configurations and validation
│   └── validation.py        # Configuration validation utilities
├── services/                 # Business logic services
│   ├── __init__.py
│   ├── ai_service.py        # AI service infrastructure with provider abstraction
│   ├── ai_orchestrator.py   # Multi-provider AI orchestration with fallback
│   ├── openai_provider.py   # OpenAI provider implementation
│   ├── anthropic_provider.py # Anthropic provider implementation
│   ├── gemini_provider.py   # Google Gemini provider implementation
│   ├── openrouter_provider.py # OpenRouter provider implementation
│   ├── context_service.py   # Context generation service with Faker integration
│   ├── context_factories.py # Industry-specific context factories
│   └── prompt_service.py    # Prompt management system with industry-specific templates
├── demos/                    # Industry demo modules
│   ├── __init__.py
│   ├── base_demo.py         # Abstract base class for all industry demos
│   ├── demo_factory.py      # Factory for creating demo instances
│   ├── restaurant_demo.py   # Restaurant reservations demo implementation
│   ├── healthcare_demo.py   # Healthcare demo implementation
│   ├── ecommerce_demo.py    # E-commerce demo implementation
│   ├── financial_demo.py    # Financial services demo implementation
│   ├── education_demo.py    # Education demo implementation
│   └── real_estate_demo.py  # Real estate demo implementation
├── docs/                     # Documentation
│   ├── ai-orchestrator-integration.md # AI Service Orchestrator integration guide
│   ├── base-demo-api-update.md # BaseDemo API changes and system message handling
│   ├── context-service.md   # Context Service documentation
│   ├── prompt-management.md # Prompt Service documentation
│   ├── prompt-service-updates.md # Recent Prompt Service updates and changes
│   ├── customer-focused-prompts.md # Customer-focused prompt template features
│   ├── ecommerce-template-enhancement.md # E-commerce template customer-focused improvements
│   ├── error-handling-and-logging.md # Advanced error handling and logging system
│   ├── restaurant-smart-context-generation.md # Restaurant Demo Smart Context Generation guide
│   ├── ui-components.md     # UI Components System documentation
│   ├── configuration.md     # Configuration and environment setup guide
│   ├── dependencies-and-installation.md # Installation and dependency guide
│   ├── gemini-model-update.md # Gemini model update documentation
│   └── main-application-architecture.md # Main application architecture and implementation guide
├── ui/                       # UI components and layout management
│   ├── __init__.py
│   ├── components.py        # Reusable Streamlit UI components and layout utilities
│   └── layout.py            # Page layout and responsive design components
├── utils/                    # Utility functions
│   ├── __init__.py
│   ├── logger.py            # Logging configuration and utilities
│   ├── error_handler.py     # Advanced error handling with retry logic, circuit breakers, and user-friendly messages
│   └── error_recovery.py    # Error recovery utilities and fallback mechanisms
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_ai_service.py   # Comprehensive AI service tests
│   ├── test_ai_orchestrator.py # AI orchestrator tests
│   ├── test_context_service.py # Context service tests
│   ├── test_context_factories.py # Context factories tests
│   ├── test_context_integration.py # Context integration tests
│   ├── test_prompt_service.py # Prompt service unit tests
│   ├── test_openai_provider.py     # OpenAI provider unit tests
│   ├── test_openai_integration.py  # OpenAI integration tests
│   ├── test_anthropic_provider.py  # Anthropic provider unit tests
│   ├── test_anthropic_integration.py # Anthropic integration tests
│   ├── test_gemini_provider.py     # Gemini provider unit tests
│   └── test_openrouter_provider.py # OpenRouter provider unit tests
├── .env.example             # Environment configuration template
├── requirements.txt         # Python dependencies
├── validate_config.py       # Configuration validation script
├── validate_openai.py       # OpenAI provider validation script
└── validate_anthropic.py    # Anthropic provider validation script
```

## 📱 Application Versions

### Static Demo (`app.py`)
- **Purpose**: Safe fallback version with comprehensive static response generators
- **Use Case**: Demos, testing, when AI providers are unavailable
- **Features**: 
  - All UI functionality with realistic static responses
  - Industry-specific response generators for all 6 verticals
  - Context-aware static responses using customer/user data
  - Pattern-based query matching for relevant responses
- **Requirements**: No API keys needed, minimal dependencies

#### Static Response Generators

The static demo includes sophisticated response generators for each industry:

**E-commerce (`generate_fallback_generic_response`, `generate_fallback_contextual_response`)**
- **Enhanced Generic Responses**: Customer-focused, conversational messaging with emojis and interactive elements
  - Product categories: headphones, shoes, laptops, gifts, order tracking
  - Engaging format with "Top Picks I'd Suggest" and follow-up questions
  - Helpful guidance like "What's your main use?" and "Tell me more about what you need them for"
- **Sophisticated Contextual Responses**: Comprehensive personalization using detailed customer profiles
  - **Customer Profile**: Name, email, loyalty tier (Bronze/Silver/Gold/Platinum), location, member since date
  - **Shopping Behavior**: Preferred categories, price sensitivity, shopping frequency, device preference
  - **Current Session**: Cart items, cart value, browsing time, pages viewed, search history
  - **Purchase History**: Total orders, average order value, last purchase, favorite brands, return rate
  - **Preferences**: Shipping speed, payment method, communication preferences, review reading habits
- **Advanced Personalization Features**:
  - Loyalty tier-based discounts and perks
  - Brand preference matching from purchase history
  - Price range suggestions based on average order value
  - Personalized shipping and payment options
  - Member-specific benefits and services

**Financial Services (`generate_generic_financial_response`, `generate_contextual_financial_response`)**
- Generic advice for investments, debt management, and retirement planning
- Contextual responses using client age, income, savings, debt, risk tolerance, and goals
- Personalized investment strategies and debt payoff plans

**Education (`generate_generic_education_response`, `generate_contextual_education_response`)**
- Generic study resources for math, science, history, and general learning
- Contextual responses using student grade level, learning style, strengths, challenges, and interests
- Personalized study plans and learning strategies

**Real Estate (`RealEstateDemo` class with comprehensive context generation)**
- Generic guidance for buying, selling, renting, and real estate investing
- Sophisticated contextual responses using comprehensive client profiles including:
  - **Client Profile**: Name, type (buyer/seller/renter/investor), age, family status, employment, location
  - **Financial Profile**: Income, credit score, down payment, pre-approval status, debt-to-income ratio, savings
  - **Property Preferences**: Type, bedrooms/bathrooms, square footage, price range, preferred areas, must-haves, deal-breakers
  - **Current Situation**: Timeline, urgency reason, current housing, commute requirements
  - **Market Context**: Local market conditions, inventory levels, price trends, interest rates, seasonal factors
  - **Experience & History**: First-time buyer status, previous transactions, knowledge level, communication preferences
- Advanced fallback responses with market analysis, financing calculations, and personalized recommendations
- Intelligent price range parsing and affordability calculations
- Market-aware strategies (buyer's vs seller's market conditions)

### AI-Powered Demo (`main.py`)
- **Purpose**: Full AI integration with real responses using the AI Service Orchestrator for multi-provider support
- **Use Case**: Production use, showcasing real AI capabilities with dynamic context and intelligent provider management
- **Features**: 
  - **Multi-Provider AI Integration**: Supports OpenAI, Anthropic, Gemini, and OpenRouter providers
  - **Intelligent Provider Management**: Automatic provider selection, fallback, and connection validation
  - **AI Service Orchestrator**: Unified interface with caching, retry logic, and performance monitoring
  - **Dynamic Context Generation**: Uses Faker library for realistic industry-specific data
  - **Side-by-side Comparison**: Generic vs contextual AI responses with real-time generation
  - **All 6 Industry Demos**: Restaurant, Healthcare, E-commerce, Financial, Education, Real Estate
  - **Automatic Fallback**: Graceful degradation to static responses when AI is unavailable
  - **Advanced Error Handling**: Comprehensive error handling with user-friendly messages
  - **Debug Information Panel**: Real-time provider status and configuration details
  - **Prompt Service Integration**: Industry-specific prompt templates and validation
- **Requirements**: At least one AI provider API key, full dependencies including AI provider libraries

### Demo Runner (`run_demo.py`)
- **Purpose**: Easy switching between versions
- **Usage**: `python run_demo.py [static|ai]`
- **Features**: Automatic setup validation, clear status indicators

## 🤖 AI-Powered Demo Implementation

The AI-powered version (`main.py`) uses the AI Service Orchestrator for intelligent multi-provider AI integration:

### AI Service Orchestrator Integration

The application now uses the `AIServiceOrchestrator` for unified AI provider management:

```python
# Initialize AI provider with orchestrator
@st.cache_resource
def initialize_ai_provider():
    """Initialize AI provider with caching using the configured default provider."""
    # Get the default provider from configuration
    default_provider = get_default_provider()
    
    # Initialize the AI orchestrator
    orchestrator = AIServiceOrchestrator()
    
    # Test connection with the default provider
    if default_provider and orchestrator.validate_provider_connection(default_provider):
        return orchestrator, default_provider
    else:
        return None, None
```

### AIResponseGenerator Class

The enhanced response generator now works with the orchestrator:

```python
class AIResponseGenerator:
    """Handles AI response generation with fallback to static responses."""
    
    def __init__(self, orchestrator_and_provider=None):
        if orchestrator_and_provider:
            self.orchestrator, self.provider_name = orchestrator_and_provider
            self.use_ai = True
        else:
            self.orchestrator = None
            self.provider_name = None
            self.use_ai = False
    
    def generate_response(self, query: str, context: Dict[str, Any], 
                         system_message: str, is_contextual: bool = True, 
                         industry: Optional[Industry] = None) -> str:
        """Generate AI response using orchestrator with fallback to static responses."""
```

**Key Features:**
- **Multi-Provider Support**: Works with OpenAI, Anthropic, Gemini, and OpenRouter
- **Intelligent Provider Selection**: Uses configured default provider with automatic fallback
- **Prompt Service Integration**: Uses industry-specific prompt templates and validation
- **Automatic Fallback**: Gracefully falls back to static responses when AI is unavailable
- **Context-Aware Prompting**: Uses different prompting strategies for generic vs contextual responses
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading Indicators**: Shows "🤖 AI is thinking..." spinner during API calls

### Dynamic Context Generation

Each industry demo generates realistic context data using the Faker library:

**Restaurant Demo Context:**
The Restaurant Demo now features **Smart Context Generation** that intelligently adapts to user queries:

```python
# Basic context structure
user_context = {
    "customer_profile": {
        "name": fake.name(),
        "member_since": "2022-08-15",
        "loyalty_tier": "Gold",
        "total_visits": 15
    },
    "location": f"{fake.city()}, {fake.state()}",
    "dietary_restrictions": ["Vegetarian", "Gluten-free"],
    "cuisine_preferences": ["Italian", "Mediterranean", "Asian"],
    "budget": "$35-55 per person",
    "party_size": 3,
    "preferred_time": "Early dinner (5-7 PM)",
    "special_occasion": "Anniversary dinner",
    "past_visits": ["Tony's Pizzeria", "Mama Rosa's", "Villa Italiana"]
}
```

**Smart Context Features:**
- **Cuisine Intelligence**: Automatically detects cuisine mentions (Indian, Italian, Asian, Mexican) and generates culturally-aware context including authentic restaurant names, appropriate locations, and cuisine-specific preferences
- **Occasion Detection**: Recognizes special occasions (anniversary, birthday, business meeting) and adjusts party size, budget, and atmosphere preferences accordingly
- **Query-Aware Adaptation**: Analyzes user queries to provide relevant context that enhances the AI's ability to give personalized recommendations

> 📚 **Detailed Documentation**: See [Restaurant Smart Context Generation Guide](docs/restaurant-smart-context-generation.md) for comprehensive documentation of the intelligent context generation system, including pattern matching, cultural awareness features, and usage examples.

**Healthcare Demo Context:**
```python
patient_context = {
    "age": random.randint(25, 65),
    "gender": random.choice(["Male", "Female"]),
    "medical_history": random.sample(["Hypertension", "Diabetes Type 2", "Seasonal allergies", "Asthma"], 2),
    "current_medications": random.sample(["Lisinopril 10mg", "Metformin 500mg", "Claritin"], 2),
    "allergies": random.sample(["Penicillin", "Shellfish", "Peanuts", "Latex", "Sulfa drugs"], 2),
    "recent_symptoms": random.sample(["Fatigue (3 days)", "Mild fever", "Headaches", "Joint pain"], 2),
    "vital_signs": {
        "BP": f"{random.randint(110, 150)}/{random.randint(70, 95)}",
        "HR": f"{random.randint(65, 85)}",
        "Temp": f"{random.uniform(98.0, 100.5):.1f}°F",
        "Weight": f"{random.randint(120, 200)} lbs"
    }
}
```

### Industry-Specific System Messages

Each demo uses enhanced prompt templates with customer-focused features to guide AI behavior:

**Restaurant Assistant:**
```python
system_message = """You are a professional concierge service specializing in dining experiences. Help customers find the perfect restaurants, make reservations, and provide personalized dining recommendations based on their preferences, dietary restrictions, and occasion. Be knowledgeable about different cuisines, restaurant atmospheres, and dining options to create memorable experiences."""
```

**Healthcare Assistant:**
```python
system_message = """You are a knowledgeable healthcare professional providing medical information and health guidance. Be caring, informative, and supportive while helping patients understand their health concerns. Always emphasize the importance of consulting with qualified healthcare providers for specific medical concerns and remind users that this information is for educational purposes only and not a substitute for professional medical advice."""
```

**E-commerce Shopping Assistant:**
```python
system_message = """You are a helpful personal shopping assistant. Your goal is to help customers find exactly what they're looking for by providing product recommendations, comparing options, and guiding them through their purchasing decisions. Be friendly, knowledgeable about products, and focus on the customer's needs and preferences."""
```

### Status Indicators and Debug Information

The application provides clear status indicators:
- **🤖 AI Mode**: Real AI responses enabled with provider name (e.g., "OpenAI", "Anthropic")
- **📝 Fallback Mode**: Using static responses when AI providers are unavailable

Debug panel shows:
- Current AI Provider connection status
- Default provider configuration
- API key configuration status
- Provider-specific library availability

## 🔄 Recent Updates: AI Service Orchestrator Integration

The AI-powered demo (`main.py`) has been significantly enhanced with multi-provider AI support through the AI Service Orchestrator. This represents a major architectural improvement from the previous single-provider approach.

### Key Changes Made

1. **Multi-Provider Support**: Now supports OpenAI, Anthropic, Gemini, and OpenRouter providers
2. **Intelligent Provider Management**: Automatic provider selection based on configuration
3. **Enhanced Error Handling**: Comprehensive error handling with graceful fallback
4. **Improved Configuration**: Environment-based provider configuration with validation
5. **Better Status Reporting**: Real-time provider status and connection information

### Migration from Single Provider

**Previous Architecture (OpenAI only):**
```python
# Old approach - single provider
from services.openai_provider import OpenAIProvider
provider = OpenAIProvider(config)
```

**New Architecture (Multi-provider with orchestrator):**
```python
# New approach - orchestrator with multiple providers
from services.ai_orchestrator import AIServiceOrchestrator
from config.ai_config import get_default_provider

orchestrator = AIServiceOrchestrator()
default_provider = get_default_provider()
```

### Configuration Updates

The new architecture supports flexible provider configuration:

```bash
# Configure multiple providers (any combination)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GEMINI_API_KEY=your_gemini_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Set preferred default provider (optional)
AI_PROVIDER=anthropic  # Options: openai, anthropic, gemini, openrouter
```

### Benefits of the New Architecture

- **Reliability**: Automatic fallback if primary provider fails
- **Flexibility**: Easy switching between AI providers
- **Performance**: Response caching and retry logic
- **Monitoring**: Provider statistics and health monitoring
- **Scalability**: Easy addition of new AI providers

For detailed information about the AI Service Orchestrator integration, see [AI Orchestrator Integration Guide](docs/ai-orchestrator-integration.md).

## 🔄 Recent Updates: Response Format Guidelines Enhancement

### Prompt Service Enhancement

All industry prompt templates have been enhanced with comprehensive **Response Format Guidelines** that provide specific instructions for AI response structure, tone, and formatting. This major update ensures consistent, professional, and user-friendly AI responses across all industries.

### Key Features Added

**Response Format Guidelines Include:**
- **Structured Response Instructions**: Clear formatting guidelines for AI responses
- **Industry-Specific Formatting**: Tailored guidelines for each industry's unique needs
- **Conversational Flow Patterns**: Guidelines for natural, engaging dialogue
- **Call-to-Action Integration**: Specific instructions for helpful follow-up suggestions
- **Accessibility Focus**: Emphasis on scannable, easy-to-read response formats

**Example Response Format Guidelines (Restaurant Industry):**
```
RESPONSE FORMAT GUIDELINES:
- Start with a warm, conversational greeting that acknowledges their request
- Structure your response with clear sections using bullet points or numbered lists when appropriate
- Include specific restaurant recommendations with key details (cuisine type, atmosphere, price range)
- Use friendly, conversational language that feels personal and engaging
- End with a clear call-to-action (e.g., "Would you like me to help you make a reservation?")
- Keep paragraphs short and scannable for easy reading
```

### Industries Enhanced with Response Format Guidelines

- ✅ **Restaurant**: Warm, conversational dining recommendations with clear sections
- ✅ **Healthcare**: Caring, empathetic health guidance with structured information
- ✅ **E-commerce**: Friendly, enthusiastic shopping assistance with product organization
- ✅ **Financial**: Professional, trustworthy financial advice with clear sections
- ✅ **Education**: Encouraging, supportive academic guidance with learning recommendations
- ✅ **Real Estate**: Professional, knowledgeable property guidance with market insights

### Benefits of Response Format Guidelines

1. **Consistency**: All AI responses follow predictable, professional formatting
2. **Readability**: Structured responses are easier to scan and understand
3. **Engagement**: Clear call-to-actions encourage continued interaction
4. **Accessibility**: Short paragraphs and bullet points improve readability
5. **Professional Quality**: Responses feel more polished and helpful

### Template Structure Enhancement

All templates now follow this enhanced structure:
1. **Professional Role Definition**: Clear persona for the AI assistant
2. **Industry-Specific Guidance**: Tailored advice for the specific industry context
3. **Response Format Guidelines**: Detailed formatting and structure instructions
4. **Personalization Instructions**: How to use context data effectively
5. **Call-to-Action Requirements**: Specific guidance for helpful follow-ups

### Impact on AI Responses

This update enables:
- **Structured Responses**: All AI responses follow consistent formatting patterns
- **Industry-Appropriate Tone**: Each industry uses the most suitable communication style
- **Better User Experience**: Responses are more scannable and actionable
- **Enhanced Engagement**: Clear call-to-actions encourage continued interaction
- **Professional Quality**: All responses meet high standards for customer-facing interactions

The enhancement is automatically applied to all existing integrations and doesn't require any code changes, but significantly improves the quality and consistency of AI-generated responses across all industry demonstrations.

## 🚨 Advanced Error Handling System

The Context Engineering Demo includes a comprehensive error handling and logging system designed to provide robust error management, retry logic, and user-friendly error messages.

### Key Error Handling Features

#### 🔄 Retry Logic with Exponential Backoff

Automatic retry mechanisms for transient failures:

```python
from utils.error_handler import retry_with_exponential_backoff, RetryConfig

@retry_with_exponential_backoff(
    retry_config=RetryConfig(max_retries=3, base_delay=1.0),
    exceptions=(AIProviderError, NetworkError)
)
def call_ai_provider(request):
    return ai_provider.generate_response(request)
```

**Features:**
- Configurable retry attempts and delays
- Exponential backoff with jitter to prevent thundering herd
- Exception filtering for specific error types
- Comprehensive logging of retry attempts

#### ⚡ Circuit Breaker Pattern

Prevents cascading failures in distributed systems:

```python
from utils.error_handler import ErrorHandler

circuit_breaker = ErrorHandler.create_circuit_breaker(
    failure_threshold=5,     # Open circuit after 5 failures
    recovery_timeout=60      # Attempt recovery after 60 seconds
)

@circuit_breaker
def call_external_service():
    return external_api.call()
```

**Benefits:**
- Fail fast when services are known to be down
- Automatic recovery testing
- Resource protection from repeated failed calls
- Prevents cascading failure propagation

#### 🎯 Centralized Error Handler

Unified error processing with user-friendly messages:

```python
from utils.error_handler import ErrorHandler

try:
    result = risky_operation()
except Exception as error:
    user_message = ErrorHandler.handle_error(error)
    st.error(user_message)  # Display friendly message to user
```

**Error Message Examples:**
- **Rate Limit**: "⚠️ The OpenAI service is currently busy. Please try again in a moment."
- **Authentication**: "🔑 There's an issue with the OpenAI API configuration. Please check your settings."
- **Network**: "🌐 Network connection issue. Please check your internet connection and try again."

#### 📊 Performance Monitoring

Automatic tracking of function execution times and success rates:

```python
ErrorHandler.log_performance_metrics(
    func_name="ai_request",
    execution_time=1.5,
    success=True
)
```

### Custom Exception Hierarchy

Structured exception classes for different error types:

```python
from utils.error_handler import (
    ContextDemoError,      # Base exception
    AIProviderError,       # AI provider failures
    ConfigurationError,    # Configuration issues
    NetworkError,          # Network connectivity problems
    ValidationError,       # Input validation failures
    ContextError          # Context generation issues
)
```

### Integration with AI Services

The error handling system integrates seamlessly with the AI Service Orchestrator:

- **Automatic Retry**: AI provider calls automatically retry on transient failures
- **Circuit Breaker Protection**: Prevents overwhelming failing AI providers
- **Graceful Degradation**: Falls back to static responses when AI services are unavailable
- **User-Friendly Messages**: Converts technical errors into actionable user guidance

### Configuration

No additional configuration required - the error handling system uses existing logging configuration and integrates automatically with all AI provider calls.

For detailed documentation, see [Error Handling and Logging Guide](docs/error-handling-and-logging.md).

## 🏭 Demo Framework Architecture

The application uses a modular demo framework that provides consistent functionality across all industry demonstrations while allowing for industry-specific customization.

### BaseDemo Abstract Class

All industry demos extend the `BaseDemo` abstract class, which provides:

```python
from demos.base_demo import BaseDemo
from typing import Dict, List, Any

class BaseDemo(ABC):
    """Abstract base class for industry demonstrations."""
    
    def __init__(self, industry_name: str, industry_enum: Optional[Industry] = None, 
                 ai_service=None, context_service=None):
        self.industry_name = industry_name
        self.industry_enum = industry_enum
        self.ai_service = ai_service
        self.context_service = context_service
        self.use_ai = ai_service is not None
    
    # Abstract methods that must be implemented by subclasses
    @abstractmethod
    def generate_context(self) -> Dict[str, Any]
    @abstractmethod
    def get_sample_queries(self) -> List[str]
    @abstractmethod
    def get_query_placeholder(self) -> str
    @abstractmethod
    def get_system_message_generic(self) -> str
    @abstractmethod
    def get_system_message_contextual(self) -> str
    @abstractmethod
    def generate_fallback_generic_response(self, query: str) -> str
    @abstractmethod
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str
    
    # Response generation methods (system messages handled internally by AI service)
    def generate_generic_response(self, query: str) -> str
    def generate_contextual_response(self, query: str, context: Dict[str, Any]) -> str
```

### Demo Implementation Pattern

All demo classes follow a consistent implementation pattern with proper Industry enum integration:

```python
from demos.restaurant_demo import RestaurantDemo

class RestaurantDemo(BaseDemo):
    """Restaurant reservations demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        super().__init__("Restaurant Reservations", Industry.RESTAURANT, ai_service, context_service)
```

**Industry Enum Integration Pattern:**
Each demo class now properly imports and uses the Industry enum from the prompt service:

```python
# All demo classes follow this pattern:
def __init__(self, ai_service=None, context_service=None):
    from services.prompt_service import Industry
    super().__init__("Industry Name", Industry.ENUM_VALUE, ai_service, context_service)
```

**Current Industry Mappings:**
- **RestaurantDemo**: `Industry.RESTAURANT`
- **HealthcareDemo**: `Industry.HEALTHCARE` 
- **EcommerceDemo**: `Industry.ECOMMERCE`
- **FinancialDemo**: `Industry.FINANCIAL`
- **EducationDemo**: `Industry.EDUCATION`
- **RealEstateDemo**: `Industry.REAL_ESTATE`
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic restaurant context using Faker."""
        return {
            "location": f"{fake.city()}, {fake.state()}",
            "dietary_restrictions": random.sample(
                ["Vegetarian", "Vegan", "Gluten-free", "Keto", "Dairy-free"], 2
            ),
            "cuisine_preferences": random.sample(
                ["Italian", "Mediterranean", "Asian", "Mexican", "French", "American"], 3
            ),
            "budget": random.choice(["$20-40 per person", "$50-80 per person", "$80-120 per person"]),
            "party_size": random.randint(2, 6),
            "preferred_time": random.choice(["Lunch (12-2 PM)", "Early dinner (5-7 PM)", "Late dinner (7-9 PM)"]),
            "special_occasion": random.choice([None, "Anniversary", "Birthday", "Business meeting", "Date night"]),
            "past_visits": [fake.company() + " Restaurant" for _ in range(3)]
        }
```

### Demo Factory Pattern

The `DemoFactory` class manages demo creation and registration:

```python
from demos.demo_factory import DemoFactory

# Create a demo instance
demo = DemoFactory.create_demo("Restaurant Reservations", ai_service, context_service)

# Get available industries
industries = DemoFactory.get_available_industries()
# Returns: ["Restaurant Reservations", "Healthcare", "E-commerce", "Financial Services", "Education", "Real Estate"]

# Check if industry is supported
is_supported = DemoFactory.is_industry_supported("Restaurant Reservations")  # True
```

### Key Framework Features

#### Consistent UI Components
- **Query Input**: Standardized input field with industry-specific placeholders
- **Sample Queries**: Clickable buttons for common industry queries
- **Side-by-Side Comparison**: Generic vs contextual response columns
- **Context Display**: Expandable JSON view of generated context
- **Industry Icons**: Automatic emoji icons for each industry

#### Intelligent Response Generation
- **AI Integration**: Seamless integration with AI providers
- **Fallback Logic**: Automatic fallback to static responses when AI unavailable
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Context Awareness**: Different prompting strategies for generic vs contextual responses

#### Restaurant Demo Features

**Sample Queries:**
- "Book a table for two tonight"
- "Find a romantic dinner spot"
- "I need lunch recommendations"
- "Looking for vegetarian restaurants"
- "Best Italian places nearby"

**Context Generation:**
- **Location**: Realistic city and state using Faker
- **Dietary Restrictions**: Random selection from common dietary needs
- **Cuisine Preferences**: Multiple cuisine preferences for variety
- **Budget Range**: Realistic price ranges per person
- **Party Details**: Size, timing, and special occasions
- **History**: Past restaurant visits for personalization

**Fallback Responses:**
The restaurant demo includes sophisticated fallback logic that provides contextual responses even without AI:

```python
# Generic fallback for booking queries
"Here are some restaurant options:
- Olive Garden (Italian)
- Applebee's (American) 
- McDonald's (Fast Food)
- Red Lobster (Seafood)
- Taco Bell (Mexican)

Would you like me to make a reservation?"

# Contextual fallback using user context
f"""🎯 **Perfect Matches in {location}:**

🌟 **Top Recommendation:**
- **Verde Italiano** - Vegetarian Italian, $65/person, 0.3 miles
  - ✅ Accommodates {', '.join(dietary)} dietary needs
  - ✅ Matches your {cuisines[0]} preference
  - ✅ Within your {budget} budget
  - ✅ Available tonight 7-9 PM"""
```

#### Real Estate Demo Features

The Real Estate demo showcases the most sophisticated context generation and response logic in the application:

**Sample Queries:**
- "I'm looking to buy my first home"
- "What's my home worth in today's market?"
- "Show me properties in good school districts"
- "I need to sell quickly due to job relocation"
- "What are current mortgage rates?"

**Advanced Context Generation:**
The Real Estate demo generates comprehensive client profiles with 6 major context categories:

1. **Client Profile**: Name, client type (buyer/seller/renter/investor), demographics, employment status
2. **Financial Profile**: Income ranges, credit scores, down payment availability, pre-approval status, debt ratios
3. **Property Preferences**: Property types, size requirements, price ranges, location preferences, must-haves, deal-breakers
4. **Current Situation**: Timeline urgency, reasons for moving, current housing status, commute requirements
5. **Market Context**: Local market conditions, inventory levels, price trends, interest rates, seasonal factors
6. **Experience & History**: First-time buyer status, previous transactions, knowledge level, past challenges

**Intelligent Response Features:**
- **Price Range Parsing**: Converts text price ranges to numeric values for calculations
- **Market-Aware Strategies**: Different advice for buyer's vs seller's vs balanced markets
- **Financial Calculations**: Monthly payment estimates, affordability analysis, down payment percentages
- **Timeline-Based Urgency**: Tailored strategies for ASAP vs flexible timelines
- **Experience-Level Adaptation**: Different guidance for first-time vs experienced clients

**Sample Contextual Response Structure:**
```python
f"""🏠 **Personalized Home Buying Plan for {client['name']}:**

**Your Buyer Profile:**
- {"First-time buyer" if experience['first_time_buyer'] else "Experienced buyer"}
- Budget: {preferences['price_range']} (based on {financial['annual_income']} income)
- {"✅ Pre-approved" if financial['pre_approved'] else "⚠️ Need pre-approval"}

**Market Advantage Strategy:**
- **Current Market:** {market['local_market']} (avg {market['average_days_on_market']} days)
- **Your Timeline:** {situation['timeline']} (reason: {situation['urgency_reason']})
- **Interest Rate:** {market['interest_rates']} ({"act quickly" if market['price_trend'] == 'Rising' else "good timing"})

**Financing Estimate:**
- Monthly Payment: ~${int((price_range * 0.8) * 0.006):,} (estimated)
- Down Payment: ${financial['down_payment_available']:,} ({percentage}% down)
```

**Market Intelligence:**
- Adapts advice based on seller's market (competitive) vs buyer's market (negotiation opportunities)
- Considers seasonal factors and inventory levels
- Provides market-specific timing recommendations
- Integrates interest rate trends into urgency calculations

### Adding New Industry Demos

To add a new industry demo:

1. **Create Demo Class**: Extend `BaseDemo` and implement all abstract methods
2. **Register with Factory**: Add to `DemoFactory._demo_classes` registry
3. **Add to Settings**: Include in the `industries` list in `config/settings.py`
4. **Implement Context**: Create realistic context generation using Faker
5. **Design Fallbacks**: Create intelligent fallback responses for both generic and contextual scenarios

**Example New Demo Structure:**
```python
from demos.base_demo import BaseDemo

class TravelDemo(BaseDemo):
    def __init__(self, ai_service=None, context_service=None):
        super().__init__("Travel Planning", ai_service, context_service)
    
    def generate_context(self) -> Dict[str, Any]:
        return {
            "departure_city": fake.city(),
            "travel_dates": fake.date_between(start_date='+1d', end_date='+30d'),
            "budget": fake.random_element(["Budget", "Mid-range", "Luxury"]),
            "travel_style": fake.random_element(["Adventure", "Relaxation", "Cultural", "Business"]),
            "group_size": fake.random_int(min=1, max=6),
            "preferences": fake.random_elements(["Museums", "Beaches", "Mountains", "Cities"], length=2)
        }
    
    # ... implement other abstract methods
```

### Demo Response Data Model

The framework uses a standardized response model:

```python
@dataclass
class DemoResponse:
    """Container for demo response data"""
    generic_response: str           # AI/fallback response without context
    contextual_response: str        # AI/fallback response with context
    context_data: Dict[str, Any]   # Generated context data
    query: str                     # Original user query
    industry: str                  # Industry name
```

This architecture ensures consistency across all industry demos while providing the flexibility needed for industry-specific customization and realistic context generation.

## 🎨 UI Components System

The application features a comprehensive UI components system built on Streamlit, providing reusable, modular components for consistent user experience across all industry demonstrations.

### Core Components

#### UIComponents Class

The main class providing standardized UI elements:

```python
from ui.components import UIComponents, ResponseData, MetricsData

# Render page header
UIComponents.render_page_header(
    title="🧠 Context Engineering Demo",
    subtitle="**See how AI responses transform when context is applied**"
)

# Show AI status
UIComponents.render_ai_status_indicator(ai_enabled=True, provider_name="OpenAI")

# Display metrics dashboard
metrics = UIComponents.create_metrics_data(ai_enabled=True)
UIComponents.render_metrics_dashboard(metrics)
```

#### Key UI Components

**Page Structure:**
- `render_page_header()` - Main title and subtitle
- `render_ai_status_indicator()` - AI mode status display
- `render_metrics_dashboard()` - Top-level metrics overview
- `render_footer()` - Application footer with mode info

**Query Interface:**
- `render_query_input()` - Industry-specific query input field
- `render_sample_queries()` - Clickable sample query buttons
- `render_demo_placeholder()` - Placeholder when no query entered

**Response Display:**
- `render_comparison_columns()` - Side-by-side generic vs contextual responses
- `render_context_expander()` - Expandable context data display
- `render_loading_indicator()` - AI processing spinner

**Feedback & Status:**
- `render_error_display()` - Error messages with optional details
- `render_success_message()` - Success notifications
- `render_info_message()` - Informational messages

#### Data Models

**ResponseData:**
```python
@dataclass
class ResponseData:
    generic_response: str           # Generic AI response
    contextual_response: str        # Context-aware AI response
    context_data: Dict[str, Any]   # Context information used
    query: str                     # Original user query
    industry: str                  # Industry name
    timestamp: Optional[datetime]   # Response timestamp
```

**MetricsData:**
```python
@dataclass
class MetricsData:
    industries_count: int = 6       # Number of available industries
    context_points: str = "50+"     # Context data points available
    response_quality: str = "10x"   # Quality improvement indicator
    user_satisfaction: str = "95%"  # User satisfaction metric
    ai_enabled: bool = False        # AI enablement status
```

### Layout Management

#### LayoutManager Class

Utility class for responsive design and layout management:

```python
from ui.components import LayoutManager

# Create column layouts
left_col, right_col = LayoutManager.create_two_column_layout(left_ratio=0.6)
col1, col2, col3 = LayoutManager.create_three_column_layout([1, 2, 1])

# Create centered container
with LayoutManager.create_centered_container():
    st.write("Centered content")

# Add vertical spacing
LayoutManager.add_vertical_space(lines=2)

# Create sidebar sections
def render_debug_info():
    st.write("Debug information here")

LayoutManager.create_sidebar_section("Debug Info", render_debug_info)
```

### Usage Examples

#### Complete Demo Page Structure

```python
from ui.components import UIComponents, LayoutManager
from ui.components import render_demo_header, render_query_section, render_response_comparison

# Page setup
UIComponents.render_page_header()
UIComponents.render_ai_status_indicator(ai_enabled=True, provider_name="OpenAI")

# Metrics dashboard
metrics = UIComponents.create_metrics_data(ai_enabled=True, industries_count=6)
UIComponents.render_metrics_dashboard(metrics)

# Industry demo
render_demo_header("Restaurant Reservations", "🍽️")

# Query interface
sample_queries = [
    "Book a table for two tonight",
    "Find a romantic dinner spot",
    "I need lunch recommendations"
]

query = render_query_section(
    industry_name="Restaurant Reservations",
    placeholder="Enter your restaurant request...",
    sample_queries=sample_queries
)

# Response comparison
if query:
    with UIComponents.render_loading_indicator("🤖 AI is thinking..."):
        # Generate responses (AI or fallback)
        generic_response = generate_generic_response(query)
        contextual_response = generate_contextual_response(query, context)
    
    # Display comparison
    render_response_comparison(
        generic_response=generic_response,
        contextual_response=contextual_response,
        context_data=context,
        query=query,
        industry="Restaurant Reservations"
    )

# Footer
UIComponents.render_footer(ai_enabled=True)
```

#### Error Handling with UI Components

```python
try:
    response = ai_provider.generate_response(request)
    UIComponents.render_success_message(
        "Response generated successfully!",
        details=f"Used {response.tokens_used} tokens in {response.response_time:.2f}s"
    )
except Exception as e:
    UIComponents.render_error_display(
        error_message="Failed to generate AI response",
        error_type="Error",
        show_details=True,
        details=str(e)
    )
```

#### Context Display

```python
# Generate context data
context = {
    "user_profile": {"name": "John Doe", "age": 35},
    "preferences": {"cuisine": ["Italian", "Mexican"], "budget": "$50-80"},
    "location": "San Francisco, CA"
}

# Display in expandable section
UIComponents.render_context_expander(
    context_data=context,
    title="📊 Available Context Data"
)
```

### Convenience Functions

The module provides convenience functions for common UI patterns:

```python
from ui.components import render_demo_header, render_query_section, render_response_comparison

# Quick demo header
render_demo_header("Healthcare", "🏥")

# Complete query section with samples
query = render_query_section(
    industry_name="Healthcare",
    placeholder="Describe your health concern...",
    sample_queries=["I have a headache", "Check my symptoms", "Medication advice"]
)

# Full response comparison
render_response_comparison(
    generic_response="Generic health advice...",
    contextual_response="Personalized advice based on your profile...",
    context_data=patient_context,
    query=query,
    industry="Healthcare"
)
```

### Responsive Design Features

- **Adaptive Layouts**: Components automatically adjust to screen size
- **Mobile-Friendly**: Optimized for mobile and tablet viewing
- **Column Management**: Intelligent column layouts for different content types
- **Spacing Control**: Consistent vertical and horizontal spacing
- **Container Management**: Centered and responsive containers

### Customization Options

#### Theme Integration
- Components respect Streamlit's theme settings
- Consistent color scheme across all elements
- Dark/light mode compatibility

#### Icon System
- Industry-specific emoji icons
- Status indicators with appropriate symbols
- Consistent iconography throughout the application

#### Typography
- Hierarchical heading structure
- Consistent text formatting
- Readable font sizes and spacing

### Integration with Demo Framework

The UI components integrate seamlessly with the demo framework:

```python
from demos.base_demo import BaseDemo
from ui.components import UIComponents

class CustomDemo(BaseDemo):
    def render_demo_ui(self):
        # Use UI components for consistent interface
        UIComponents.render_page_header(f"🏢 {self.industry_name}")
        
        # Industry-specific query interface
        query = UIComponents.render_query_input(
            industry_name=self.industry_name,
            placeholder=self.get_query_placeholder()
        )
        
        # Sample queries
        UIComponents.render_sample_queries(
            queries=self.get_sample_queries(),
            industry_name=self.industry_name,
            input_key=f"{self.industry_name}_query"
        )
        
        return query
```

This UI components system ensures consistent, professional, and user-friendly interfaces across all industry demonstrations while maintaining flexibility for customization and extension.

## 🎯 Context Generation Service

The Context Service provides intelligent, industry-specific context generation using the Faker library for realistic data. This service is the foundation for creating personalized AI responses across different industries.

### Core Components

#### ContextService Class

The main service class that manages context generation across multiple industries:

```python
from services.context_service import ContextService, Industry

# Initialize context service
context_service = ContextService(locale='en_US', seed=42)

# Generate context for a specific industry
restaurant_context = context_service.generate_context(Industry.RESTAURANT)

# Access context data
print(f"User: {restaurant_context.user_profile['name']}")
print(f"Location: {restaurant_context.situational_data['location']}")
print(f"Preferences: {restaurant_context.preferences}")
```

#### IndustryContext Data Model

Standardized context structure for all industries:

```python
@dataclass
class IndustryContext:
    industry: Industry                    # Industry type
    user_profile: Dict[str, Any]         # User demographic and basic info
    situational_data: Dict[str, Any]     # Current situation/context
    preferences: Dict[str, Any]          # User preferences and choices
    history: Dict[str, Any]              # Past interactions/transactions
    constraints: Dict[str, Any]          # Limitations or requirements
    metadata: Dict[str, Any]             # Generation metadata
    generated_at: Optional[datetime]     # Timestamp
```

#### Supported Industries

- **RESTAURANT**: Dining preferences, dietary restrictions, location data
- **HEALTHCARE**: Patient profiles, medical history, symptoms, medications
- **ECOMMERCE**: Customer profiles, purchase history, browsing patterns
- **FINANCIAL**: Financial profiles, investment goals, risk tolerance
- **EDUCATION**: Student profiles, learning styles, academic progress
- **REAL_ESTATE**: Buyer profiles, property preferences, budget constraints

### Context Factory Pattern

Each industry uses a specialized factory for context generation:

```python
from services.context_service import BaseContextFactory, Industry

class RestaurantContextFactory(BaseContextFactory):
    def _get_industry(self) -> Industry:
        return Industry.RESTAURANT
    
    def generate_user_profile(self) -> Dict[str, Any]:
        return {
            "name": self.faker.name(),
            "age": self.faker.random_int(min=18, max=75),
            "location": f"{self.faker.city()}, {self.faker.state()}"
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        return {
            "party_size": self.faker.random_int(min=1, max=8),
            "occasion": self.faker.random_element([
                "casual dining", "date night", "business meeting", 
                "celebration", "family gathering"
            ]),
            "time_preference": self.faker.random_element([
                "lunch", "early dinner", "late dinner"
            ])
        }
```

### Key Features

#### Intelligent Caching
- **TTL-based caching**: Contexts are cached with configurable time-to-live
- **Industry-specific cache**: Each industry maintains separate cache
- **Force refresh**: Option to generate fresh context when needed

#### Quality Validation
- **Context validation**: Automatic validation of generated context data
- **Quality scoring**: 0.0-1.0 quality score based on completeness and richness
- **Error handling**: Comprehensive error handling with detailed error messages

#### Faker Integration
- **Realistic data**: Uses Faker library for authentic-looking generated data
- **Locale support**: Configurable locale for region-specific data
- **Reproducible generation**: Optional seed for consistent test data

### Usage Examples

#### Basic Context Generation

```python
from services.context_service import ContextService, Industry

# Initialize service
service = ContextService()

# Generate healthcare context
healthcare_context = service.generate_context(Industry.HEALTHCARE)

# Access generated data
patient = healthcare_context.user_profile
print(f"Patient: {patient['name']}, Age: {patient['age']}")
print(f"Medical History: {healthcare_context.history['conditions']}")
print(f"Current Medications: {healthcare_context.situational_data['medications']}")
```

#### Context Validation and Quality

```python
# Validate context
errors = service.validate_context(healthcare_context)
if errors:
    print(f"Validation errors: {errors}")

# Check quality score
quality = service.get_context_quality_score(healthcare_context)
print(f"Context quality: {quality:.2f}/1.0")

# Get context summary
summary = healthcare_context.get_context_summary()
print(f"Summary: {summary}")
```

#### Cache Management

```python
# Check cache status
cache_status = service.get_cache_status()
print(f"Cached industries: {cache_status['cached_industries']}")

# Force refresh specific industry
fresh_context = service.refresh_context(Industry.ECOMMERCE)

# Clear cache
service.clear_cache(Industry.RESTAURANT)  # Clear specific industry
service.clear_cache()  # Clear all cache
```

#### Reproducible Generation

```python
# Set seed for reproducible results
service.set_faker_seed(12345)

# Generate context - will be same each time with same seed
context1 = service.generate_context(Industry.FINANCIAL)
context2 = service.generate_context(Industry.FINANCIAL)
# context1 and context2 will have identical data
```

### Configuration

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CONTEXT_REFRESH_INTERVAL` | Cache TTL in seconds | `300` |
| `MAX_CONTEXT_SIZE` | Maximum context data size | `10000` |

#### Service Configuration

```python
# Custom configuration
service = ContextService(
    locale='en_GB',  # British English
    seed=42          # Reproducible generation
)

# Register custom factory
service.register_factory(CustomIndustryFactory)
```

### Error Handling

The Context Service includes comprehensive error handling:

```python
from services.context_service import ContextValidationError

try:
    context = service.generate_context(Industry.RESTAURANT)
except ContextValidationError as e:
    print(f"Context generation failed: {e}")
    print(f"Industry: {e.industry}")
    print(f"Validation errors: {e.validation_errors}")
```

### Integration with AI Providers

The Context Service integrates seamlessly with AI providers:

```python
# Generate context
context = service.generate_context(Industry.HEALTHCARE)

# Convert to AI prompt format
context_dict = context.to_dict()

# Use with AI provider
request = PromptRequest(
    prompt="What should I know about my medications?",
    context=context_dict,
    system_message="You are a helpful healthcare assistant."
)

response = ai_provider.generate_response(request)
```

## 🧪 Testing

The application includes a comprehensive test suite covering all major components:

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_prompt_service.py
pytest tests/test_ai_service.py
pytest tests/test_context_service.py

# Run tests with coverage
pytest --cov=services --cov=config --cov=demos

# Run tests with verbose output
pytest -v

# Run specific test categories
pytest -k "test_prompt" -v  # Run prompt-related tests
pytest -k "test_ai" -v      # Run AI service tests
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: Component interaction testing
- **Validation Tests**: Configuration and setup validation
- **Error Handling Tests**: Comprehensive error scenario testing

### Test Categories

#### Core Services
- **AI Service Tests** (`test_ai_service.py`): Base AI infrastructure, providers, error handling
- **AI Orchestrator Tests** (`test_ai_orchestrator.py`): Multi-provider orchestration, fallback logic
- **Prompt Service Tests** (`test_prompt_service.py`): Template management, validation, generation
- **Context Service Tests** (`test_context_service.py`): Context generation, caching, validation

#### AI Provider Tests
- **OpenAI Tests** (`test_openai_provider.py`, `test_openai_integration.py`): OpenAI provider functionality
- **Anthropic Tests** (`test_anthropic_provider.py`, `test_anthropic_integration.py`): Anthropic provider functionality
- **Gemini Tests** (`test_gemini_provider.py`): Google Gemini provider functionality
- **OpenRouter Tests** (`test_openrouter_provider.py`): OpenRouter provider functionality

#### Integration Tests
- **Context Integration** (`test_context_integration.py`): End-to-end context workflows
- **Context Factories** (`test_context_factories.py`): Industry-specific context generation
- **Industry Demos** (`test_industry_demos.py`): Demo framework functionality

### Validation Scripts

The application includes several validation scripts for setup verification:

```bash
# Comprehensive configuration validation
python validate_config.py

# AI provider-specific validation
python validate_openai.py
python validate_anthropic.py

# Service-specific validation
python validate_prompt_service.py
python validate_context_service.py
```

### Test Data and Mocking

- **Mock AI Providers**: Tests use mocked AI providers to avoid API calls
- **Faker Integration**: Realistic test data generation using Faker library
- **Fixture Management**: Comprehensive pytest fixtures for consistent test data
- **Error Simulation**: Controlled error injection for testing error handling

### Continuous Integration

The test suite is designed for CI/CD integration:

```bash
# CI-friendly test command
pytest --tb=short --maxfail=5 --disable-warnings

# Generate test reports
pytest --junitxml=test-results.xml --cov-report=xml
```

## 📚 Detailed Documentation

For comprehensive documentation on specific components:

- **[Context Service Documentation](docs/context-service.md)**: Complete guide to context generation
- **[Prompt Management Documentation](docs/prompt-management.md)**: Comprehensive prompt template system guide
- **[UI Components Documentation](docs/ui-components.md)**: Complete UI components system guide with API reference

## 🎨 Prompt Management System

The application includes a sophisticated prompt management system that provides structured, industry-specific prompt templates for consistent AI interactions across different use cases.

### Core Features

#### Template-Based Prompting
- **Reusable Templates**: Pre-built templates for generic, contextual, and system prompts
- **Variable Substitution**: Dynamic content insertion using `{variable}` syntax
- **Industry Specialization**: Tailored templates for each supported industry
- **Validation**: Built-in validation for template structure and content

#### Prompt Types
- **Generic**: General responses without specific context
- **Contextual**: Personalized responses using user context data
- **System**: AI provider system messages and personas
- **Industry-Specific**: Specialized templates for particular industries

### Usage Examples

#### Basic Prompt Generation

```python
from services.prompt_service import get_prompt_service, Industry

# Get the global prompt service
prompt_service = get_prompt_service()

# Generate a generic prompt
generic_prompt = prompt_service.generate_generic_prompt(
    query="I need help with menu planning",
    industry=Industry.RESTAURANT
)

# Generate a contextual prompt with user data
contextual_prompt = prompt_service.generate_contextual_prompt(
    query="I need help with menu planning",
    context={
        "restaurant_type": "fine dining",
        "cuisine": "French",
        "budget": "$50-80 per person",
        "season": "winter"
    },
    industry=Industry.RESTAURANT
)

# Generate system message for AI provider
system_message = prompt_service.generate_system_message(Industry.RESTAURANT)
```

#### Custom Template Creation

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

# Create a custom template
custom_template = PromptTemplate(
    name="custom_greeting",
    template="Welcome to {business_name}! We specialize in {specialty}. How can we help you with {service_type}?",
    prompt_type=PromptType.GENERIC,
    industry=Industry.RESTAURANT,
    description="Custom business greeting template"
)

# Register the template
prompt_service.register_template(custom_template)

# Use the template
rendered = custom_template.render(
    business_name="Mario's Bistro",
    specialty="authentic Italian cuisine",
    service_type="your dining experience"
)
```

### Industry-Specific Templates

The system includes pre-built templates for all supported industries:

- **Restaurant**: Dining recommendations, reservation assistance, menu guidance
- **Healthcare**: Patient care guidance, medical practice administration
- **E-commerce**: Product recommendations, customer service, business operations
- **Financial**: Investment advice, financial planning, risk management
- **Education**: Learning strategies, curriculum guidance, student support
- **Real Estate**: Property recommendations, market analysis, client consultation

### Template Validation and Security

```python
from services.prompt_service import PromptValidator

# Validate prompt content for security and quality
issues = PromptValidator.validate_prompt_content(prompt_text)

# Validate context data structure
context_issues = PromptValidator.validate_context_data(context_dict)

# Template validation
template_errors = template.validate()
```

The validation system checks for:
- **Security**: Injection patterns, suspicious content
- **Quality**: Length limits, repetition detection
- **Structure**: Proper variable syntax, balanced braces
- **Content**: Meaningful content, appropriate length

### Integration with AI Providers

The Prompt Service integrates seamlessly with the AI infrastructure:

```python
# Generate industry-specific prompts for AI providers
system_message = prompt_service.generate_system_message(Industry.HEALTHCARE)
contextual_prompt = prompt_service.generate_contextual_prompt(
    query=user_query,
    context=patient_context,
    industry=Industry.HEALTHCARE
)

# Use with AI orchestrator
request = PromptRequest(
    prompt=contextual_prompt,
    system_message=system_message,
    context=patient_context
)

response = ai_orchestrator.generate_response(request)
```

## 🚀 Getting Started

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Choose your version**: Static demo (`python run_demo.py static`) or AI-powered (`python run_demo.py ai`)
4. **Configure AI providers** (for AI version): Add API keys to `.env` file
5. **Validate setup**: Run `python validate_config.py`
6. **Start exploring**: Try different industries and see how context transforms AI responses!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite: `pytest`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ to demonstrate the power of context in AI interactions**ion

For comprehensive documentation including API reference, examples, and best practices, see:
- **[Context Service Documentation](docs/context-service.md)**: Complete guide to context generation
- **[Prompt Management Documentation](docs/prompt-management.md)**: Comprehensive prompt template system guide
- **[UI Components Documentation](docs/ui-components.md)**: Complete UI components system guide with API reference

## 🎨 Prompt Management System

The application includes a sophisticated prompt management system that provides structured, industry-specific prompt templates for consistent AI interactions across different use cases.

### Core Features

#### Template-Based Prompting
- **Reusable Templates**: Pre-built templates for generic, contextual, and system prompts
- **Variable Substitution**: Dynamic content insertion using `{variable}` syntax
- **Industry Specialization**: Tailored templates for each supported industry
- **Validation**: Built-in validation for template structure and content

#### Prompt Types
- **Generic**: General responses without specific context
- **Contextual**: Personalized responses using user context data
- **System**: AI provider system messages and personas
- **Industry-Specific**: Specialized templates for particular industries

### Usage Examples

#### Basic Prompt Generation

```python
from services.prompt_service import get_prompt_service, Industry

# Get the global prompt service
prompt_service = get_prompt_service()

# Generate a generic prompt
generic_prompt = prompt_service.generate_generic_prompt(
    query="I need help with menu planning",
    industry=Industry.RESTAURANT
)

# Generate a contextual prompt with user data
contextual_prompt = prompt_service.generate_contextual_prompt(
    query="I need help with menu planning",
    context={
        "restaurant_type": "fine dining",
        "cuisine": "French",
        "budget": "$50-80 per person",
        "season": "winter"
    },
    industry=Industry.RESTAURANT
)

# Generate system message for AI provider
system_message = prompt_service.generate_system_message(Industry.RESTAURANT)
```

#### Custom Template Creation

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

# Create a custom template
custom_template = PromptTemplate(
    name="custom_greeting",
    template="Welcome to {business_name}! We specialize in {specialty}. How can we help you with {service_type}?",
    prompt_type=PromptType.GENERIC,
    industry=Industry.RESTAURANT,
    description="Custom business greeting template"
)

# Register the template
prompt_service.register_template(custom_template)

# Use the template
rendered = custom_template.render(
    business_name="Mario's Bistro",
    specialty="authentic Italian cuisine",
    service_type="your dining experience"
)
```

### Industry-Specific Templates

The system includes pre-built templates for all supported industries:

- **Restaurant**: Dining recommendations, reservation assistance, menu guidance
- **Healthcare**: Patient care guidance, medical practice administration
- **E-commerce**: Product recommendations, customer service, business operations
- **Financial**: Investment advice, financial planning, risk management
- **Education**: Learning strategies, curriculum guidance, student support
- **Real Estate**: Property recommendations, market analysis, client consultation

### Template Validation and Security

```python
from services.prompt_service import PromptValidator

# Validate prompt content for security and quality
issues = PromptValidator.validate_prompt_content(prompt_text)

# Validate context data structure
context_issues = PromptValidator.validate_context_data(context_dict)

# Template validation
template_errors = template.validate()
```

The validation system checks for:
- **Security**: Injection patterns, suspicious content
- **Quality**: Length limits, repetition detection
- **Structure**: Proper variable syntax, balanced braces
- **Content**: Meaningful content, appropriate length

### Integration with AI Providers

The Prompt Service integrates seamlessly with the AI infrastructure:

```python
# Generate industry-specific prompts for AI providers
system_message = prompt_service.generate_system_message(Industry.HEALTHCARE)
contextual_prompt = prompt_service.generate_contextual_prompt(
    query=user_query,
    context=patient_context,
    industry=Industry.HEALTHCARE
)

# Use with AI orchestrator
request = PromptRequest(
    prompt=contextual_prompt,
    system_message=system_message,
    context=patient_context
)

response = ai_orchestrator.generate_response(request)ext Service Documentation](docs/context-service.md)** - Complete guide with examples and API reference

## 🤖 Supported AI Providers

- **OpenAI** (GPT-3.5, GPT-4) - **✅ Fully Implemented**
- **Anthropic** (Claude 3 Opus, Sonnet, Haiku) - **✅ Fully Implemented**
- **Google Gemini** - *Infrastructure Ready*
- **OpenRouter** (Multiple models) - *Infrastructure Ready*

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | Default AI provider | `openai` |
| `AI_TEMPERATURE` | Response creativity (0-2) | `0.7` |
| `AI_MAX_TOKENS` | Maximum response length | `500` |
| `AI_TIMEOUT` | Request timeout (seconds) | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENABLE_CACHING` | Enable response caching | `true` |
| `CONTEXT_REFRESH_INTERVAL` | Context cache TTL (seconds) | `300` |
| `MAX_CONTEXT_SIZE` | Maximum context data size | `10000` |

### AI Provider Setup

#### OpenAI
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo  # Optional
```

#### Anthropic
```bash
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-haiku-20240307  # Optional
```

#### Google Gemini
```bash
GEMINI_API_KEY=AI...
GEMINI_MODEL=gemini-1.5-flash  # Optional
```

#### OpenRouter
```bash
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=openai/gpt-3.5-turbo  # Optional
```

## 🔍 Validation Tools

The project includes comprehensive validation tools to ensure proper setup and configuration:

### Configuration Validation

```bash
# Complete application validation
python validate_config.py
```

This script validates:
- Python version compatibility (3.8+)
- Required dependencies installation
- Directory structure integrity
- Environment configuration
- AI provider setup
- Basic functionality tests

**Sample Output (Success):**
```
🎉 All checks passed! The application is ready to run.

To start the application:
   python run_demo.py static    # Safe fallback version
   python run_demo.py ai        # AI-powered version (requires API key)

Or run directly:
   streamlit run app.py         # Static version
   streamlit run main.py        # AI-powered version
```

### AI Provider Validation

#### OpenAI Provider Validation

```bash
# OpenAI-specific validation
python validate_openai.py
```

This script specifically tests:
- OpenAI library availability
- Configuration loading from environment
- Provider initialization
- Model information retrieval
- Real API calls (if API key provided)
- Connection validation

**Sample Output:**
```
🔍 Testing OpenAI Provider Implementation
==================================================
✅ OpenAI library is available
✅ OpenAI configuration loaded: model=gpt-3.5-turbo
✅ OpenAI provider initialized successfully
✅ Model info retrieved: gpt-3.5 model
   - Supports system messages: True
   - Supports context: True

🌐 Testing with real API call...
✅ Real API call successful!
   Response: Hello, World!
   Tokens used: 8
   Response time: 1.23s
✅ Connection validation passed

🎉 All OpenAI provider tests passed!
```

#### Anthropic Provider Validation

```bash
# Anthropic-specific validation
python validate_anthropic.py
```

This script specifically tests:
- Anthropic library availability
- Configuration loading from environment
- Provider initialization
- Model information retrieval
- Real API calls (if API key provided)
- Connection validation

**Sample Output:**
```
🔍 Testing Anthropic Provider Implementation
==================================================
✅ Anthropic library is available
✅ Anthropic configuration loaded: model=claude-3-haiku-20240307
✅ Anthropic provider initialized successfully
✅ Model info retrieved: claude-3-haiku model
   - Supports system messages: True
   - Supports context: True

🌐 Testing with real API call...
✅ Real API call successful!
   Response: Hello, World!
   Tokens used: 12
   Response time: 0.89s
✅ Connection validation passed

🎉 All Anthropic provider tests passed!
```

#### Context Service Validation

```bash
# Context Service validation
python validate_context_service.py
```

This script specifically tests:
- Context Service core functionality
- IndustryContext data model
- Faker integration for realistic data generation
- Context quality scoring system
- Reproducible generation with seeds
- Error handling and validation
- Cache management

**Sample Output:**
```
🔍 Testing Context Service Implementation
==================================================
✅ Context Service imports successful
✅ Context Service initialized successfully
✅ Context Service with custom config initialized
✅ Available industries: ['restaurant', 'healthcare', 'e-commerce', 'financial', 'education', 'real_estate']
✅ IndustryContext data model working correctly
✅ Faker integration working
✅ Cache status method working
✅ Quality scoring working correctly
✅ Reproducible generation working

🎉 All Context Service tests passed!
```

## 🧪 Development

### Running Tests
```bash
# Validate configuration
python validate_config.py

# Run all unit tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_ai_service.py -v          # Core AI service tests
python -m pytest tests/test_openai_provider.py -v     # OpenAI provider unit tests
python -m pytest tests/test_openai_integration.py -v  # OpenAI integration tests
python -m pytest tests/test_anthropic_provider.py -v  # Anthropic provider unit tests
python -m pytest tests/test_anthropic_integration.py -v # Anthropic integration tests

# Run tests with coverage
python -m pytest tests/ --cov=services --cov-report=html
```

### Adding New Industries

1. Create a new demo module in `demos/`
2. Implement the industry-specific context generation
3. Add the industry to the settings configuration
4. Update the main application to include the new demo

### AI Service API

The AI service infrastructure provides a standardized interface for working with multiple AI providers:

#### Core Classes

**AIResponse**: Standardized response object
```python
@dataclass
class AIResponse:
    content: str                    # AI-generated response text
    provider: AIProvider           # Which AI provider was used
    model: str                     # Model name (e.g., "gpt-3.5-turbo")
    status: ResponseStatus         # SUCCESS, ERROR, TIMEOUT, etc.
    tokens_used: Optional[int]     # Number of tokens consumed
    response_time: Optional[float] # Response time in seconds
    error_message: Optional[str]   # Error details if failed
    timestamp: Optional[datetime]  # When response was generated
    metadata: Optional[Dict[str, Any]] # Provider-specific metadata
```

**PromptRequest**: Standardized request object
```python
@dataclass
class PromptRequest:
    prompt: str                           # The main prompt text
    context: Optional[Dict[str, Any]]     # Additional context data
    temperature: Optional[float]          # Response creativity (0-2)
    max_tokens: Optional[int]            # Maximum response length
    system_message: Optional[str]        # System/role instruction
    metadata: Optional[Dict[str, Any]]   # Additional metadata
```

**BaseAIProvider**: Abstract base class for AI providers
```python
class BaseAIProvider(ABC):
    def generate_response(self, request: PromptRequest) -> AIResponse
    def validate_connection(self) -> bool
    def get_model_info(self) -> Dict[str, Any]
    def create_error_response(self, error: Exception) -> AIResponse
```

#### Implemented Providers

**OpenAIProvider**: Complete OpenAI integration
- Supports GPT-3.5, GPT-4, and other OpenAI models
- Handles chat completion API with system messages
- Comprehensive error handling and retry logic
- Token usage tracking and response time measurement
- Connection validation and model information

**AnthropicProvider**: Complete Anthropic integration
- Supports Claude 3 Opus, Sonnet, Haiku, and Claude 2 models
- Handles messages API with system message support
- Comprehensive error handling and retry logic
- Token usage tracking and response time measurement
- Connection validation and model information

#### Usage Examples

**OpenAI Provider:**
```python
from services.openai_provider import OpenAIProvider
from services.ai_service import PromptRequest
from config.ai_config import load_ai_config
from config.settings import AIProvider

# Load configuration from environment
config = load_ai_config(AIProvider.OPENAI)

# Create provider instance
provider = OpenAIProvider(config)

# Validate connection (optional)
if not provider.validate_connection():
    print("Failed to connect to OpenAI")
    exit(1)

# Create request
request = PromptRequest(
    prompt="Explain quantum computing",
    context={"audience": "beginners", "level": "introductory"},
    system_message="You are a helpful science teacher",
    temperature=0.7,
    max_tokens=200
)

# Generate response
response = provider.generate_response(request)

if response.success:
    print(f"Response: {response.content}")
    print(f"Tokens used: {response.tokens_used}")
    print(f"Response time: {response.response_time:.2f}s")
else:
    print(f"Error: {response.error_message}")
```

**Anthropic Provider:**
```python
from services.anthropic_provider import AnthropicProvider
from services.ai_service import PromptRequest
from config.ai_config import load_ai_config
from config.settings import AIProvider

# Load configuration from environment
config = load_ai_config(AIProvider.ANTHROPIC)

# Create provider instance
provider = AnthropicProvider(config)

# Validate connection (optional)
if not provider.validate_connection():
    print("Failed to connect to Anthropic")
    exit(1)

# Create request
request = PromptRequest(
    prompt="Explain quantum computing",
    context={"audience": "beginners", "level": "introductory"},
    system_message="You are a helpful science teacher",
    temperature=0.7,
    max_tokens=200
)

# Generate response
response = provider.generate_response(request)

if response.success:
    print(f"Response: {response.content}")
    print(f"Tokens used: {response.tokens_used}")
    print(f"Response time: {response.response_time:.2f}s")
else:
    print(f"Error: {response.error_message}")
```

#### OpenAI Provider Details

The `OpenAIProvider` class provides a complete implementation of the OpenAI API integration:

**Features:**
- **Chat Completion API**: Uses OpenAI's chat completion endpoint for all models
- **System Messages**: Supports system messages for role-based prompting
- **Context Integration**: Automatically formats context data into system messages
- **Token Tracking**: Monitors prompt, completion, and total token usage
- **Response Time Measurement**: Tracks API call duration for performance monitoring
- **Connection Validation**: Tests API connectivity with minimal requests
- **Model Information**: Provides detailed model capabilities and configuration

**Supported Models:**
- GPT-4 series (gpt-4, gpt-4-turbo, gpt-4-32k)
- GPT-3.5 series (gpt-3.5-turbo, gpt-3.5-turbo-16k)
- Legacy models (text-davinci-003, etc.)

**Configuration Options:**
```python
# Environment variables for OpenAI provider
OPENAI_API_KEY=sk-...                    # Required: Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo              # Optional: Model to use
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: Custom API endpoint
```

**Error Mapping:**
The provider maps OpenAI-specific errors to standardized exceptions:
- `AuthenticationError` → `AIProviderAuthenticationError`
- `RateLimitError` → `AIProviderRateLimitError`
- `TimeoutError` → `AIProviderTimeoutError`
- `BadRequestError` → `AIProviderInvalidRequestError`

#### Anthropic Provider Details

The `AnthropicProvider` class provides a complete implementation of the Anthropic API integration:

**Features:**
- **Messages API**: Uses Anthropic's messages endpoint for all Claude models
- **System Messages**: Supports system messages for role-based prompting
- **Context Integration**: Automatically formats context data into system messages
- **Token Tracking**: Monitors input, output, and total token usage
- **Response Time Measurement**: Tracks API call duration for performance monitoring
- **Connection Validation**: Tests API connectivity with minimal requests
- **Model Information**: Provides detailed model capabilities and configuration

**Supported Models:**
- Claude 3 Opus (claude-3-opus-20240229)
- Claude 3 Sonnet (claude-3-sonnet-20240229)
- Claude 3 Haiku (claude-3-haiku-20240307)
- Claude 2.1 (claude-2.1)
- Claude 2.0 (claude-2.0)
- Claude Instant (claude-instant-1.2)

**Configuration Options:**
```python
# Environment variables for Anthropic provider
ANTHROPIC_API_KEY=sk-ant-...             # Required: Your Anthropic API key
ANTHROPIC_MODEL=claude-3-haiku-20240307  # Optional: Model to use
ANTHROPIC_BASE_URL=https://api.anthropic.com  # Optional: Custom API endpoint
```

**Error Mapping:**
The provider maps Anthropic-specific errors to standardized exceptions:
- Authentication errors → `AIProviderAuthenticationError`
- Rate limit errors → `AIProviderRateLimitError`
- Timeout errors → `AIProviderTimeoutError`
- Invalid request errors → `AIProviderInvalidRequestError`

#### Error Handling

The service includes comprehensive error handling with specific exception types:

- `AIProviderError`: Base exception for all AI provider errors
- `AIProviderTimeoutError`: Request timeout errors
- `AIProviderRateLimitError`: Rate limit exceeded errors
- `AIProviderAuthenticationError`: Authentication/API key errors
- `AIProviderInvalidRequestError`: Invalid request format errors

#### Response Status Types

- `SUCCESS`: Request completed successfully
- `ERROR`: General error occurred
- `TIMEOUT`: Request timed out
- `RATE_LIMITED`: Rate limit exceeded
- `INVALID_REQUEST`: Request format was invalid

## 📝 Features

- **Multi-Provider AI Support**: Switch between different AI providers
- **Industry-Specific Demos**: Restaurant, Healthcare, E-commerce, Financial, Education, Real Estate
- **Context Comparison**: Side-by-side generic vs contextual responses
- **Realistic Data Generation**: Using Faker library for authentic demo data
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Configuration Validation**: Built-in validation for all settings
- **Enhanced Response Generators**: Comprehensive static response functions for all industry verticals

## 🔧 Troubleshooting

### Common Issues

1. **No AI providers configured**
   - Add at least one API key to your `.env` file
   - Run `python validate_config.py` to verify

2. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure you're in the project root directory

3. **API errors**
   - Check your API keys are valid
   - Verify you have sufficient credits/quota
   - Check network connectivity

### Getting Help

1. Run the configuration validator: `python validate_config.py`
2. Check the application logs for detailed error information
3. Ensure all required environment variables are set

## 📄 License

This project is licensed under the MIT License.

## 📝 Changelog

### Version 2.2.0 - Anthropic Provider Implementation

**New Features:**
- **Complete Anthropic Provider**: Full implementation of `AnthropicProvider` with Claude model support
- **Multi-Provider AI Integration**: Real support for both OpenAI and Anthropic providers in the AI-powered demo
- **Claude Model Support**: Support for Claude 3 Opus, Sonnet, Haiku, Claude 2, and Claude Instant models
- **Anthropic API Integration**: Complete integration with Anthropic's Messages API including system message support
- **Comprehensive Testing**: Full test suite for Anthropic provider with 25+ unit and integration tests
- **Validation Tools**: Dedicated `validate_anthropic.py` script for Anthropic provider validation

**Technical Implementation:**
- **Messages API Integration**: Uses Anthropic's messages endpoint with proper request formatting
- **System Message Support**: Full support for system messages and context integration
- **Token Usage Tracking**: Monitors input, output, and total token usage for cost tracking
- **Error Handling**: Comprehensive error mapping for Anthropic-specific exceptions
- **Connection Validation**: Automatic testing of Anthropic API connectivity
- **Model Information**: Detailed model capabilities and configuration reporting

**Provider Features:**
- **Context Integration**: Automatically formats context data into system messages
- **Response Time Measurement**: Tracks API call duration for performance monitoring
- **Error Recovery**: Graceful fallback mechanisms with user-friendly error messages
- **Configuration Validation**: Pydantic-based configuration with environment variable support

**Testing & Validation:**
- **Unit Tests**: Comprehensive unit tests covering all Anthropic provider functionality
- **Integration Tests**: End-to-end testing with mock API responses
- **Validation Script**: Dedicated validation tool for Anthropic provider setup
- **Error Scenario Testing**: Complete coverage of authentication, rate limit, and timeout errors

**Documentation:**
- **Usage Examples**: Complete code examples for Anthropic provider usage
- **Configuration Guide**: Detailed setup instructions for Anthropic API keys and models
- **Model Documentation**: Comprehensive list of supported Claude models with capabilities
- **Error Handling Guide**: Documentation of error types and resolution strategies

**Developer Experience:**
- **Easy Setup**: Simple environment variable configuration for Anthropic API
- **Debug Support**: Comprehensive logging and debug information for troubleshooting
- **Consistent Interface**: Same standardized interface as OpenAI provider for easy switching
- **Validation Tools**: One-command validation of Anthropic provider setup

### Version 2.1.0 - Complete AI-Powered Demo Implementation

**New Features:**
- **Complete AI-Powered Demo**: Full implementation of `main.py` with real OpenAI integration
- **AIResponseGenerator Class**: Intelligent response generation with automatic fallback to static responses
- **Dynamic Context Generation**: All 6 industry demos now generate realistic context using Faker library
- **Industry-Specific System Messages**: Tailored prompting strategies for each industry vertical
- **Real-Time AI Responses**: Live OpenAI API integration with loading indicators and error handling
- **Status Indicators**: Clear visual feedback showing AI mode vs fallback mode
- **Debug Information Panel**: Comprehensive debugging information in sidebar

**Industry Demos Enhanced:**
- **Restaurant Reservations**: Dynamic location, dietary restrictions, cuisine preferences, and budget context
- **Healthcare**: Realistic patient data including medical history, medications, allergies, and vital signs
- **E-commerce**: Customer profiles with purchase history, browsing patterns, and preferences
- **Financial Services**: Complete financial profiles with income, debt, investment experience, and goals
- **Education**: Student contexts with grade level, learning style, strengths, and challenges
- **Real Estate**: Buyer profiles with budget, family size, lifestyle, and location preferences

**Technical Implementation:**
- **Streamlit Integration**: Seamless integration with Streamlit caching and UI components
- **Error Handling**: Graceful degradation when AI services are unavailable
- **Connection Validation**: Automatic testing of AI provider connectivity on startup
- **Response Comparison**: Side-by-side display of generic vs contextual AI responses
- **Context Display**: Expandable JSON viewers for all generated context data

**User Experience:**
- **Automatic Fallback**: Seamless transition to static responses when AI is unavailable
- **Loading Indicators**: "🤖 AI is thinking..." spinners during API calls
- **Clear Status Messages**: Visual indicators for AI mode vs demo mode
- **Debug Panel**: Optional debug information for troubleshooting

### Version 2.0.0 - AI Service Infrastructure

**New Features:**
- **AI Service Infrastructure**: Complete modular AI provider system with abstract base classes
- **Multi-Provider Support**: Standardized interface for OpenAI, Anthropic, Gemini, and OpenRouter
- **Comprehensive Error Handling**: Specific exception types and user-friendly error messages
- **Response Models**: Standardized `AIResponse` and `PromptRequest` data models with full serialization
- **Configuration Validation**: Pydantic-based configuration with automatic validation
- **Comprehensive Testing**: Full test suite with 22+ unit tests covering all components
- **Validation Scripts**: Automated configuration and dependency validation tools

**Technical Improvements:**
- **Type Safety**: Full type hints and Pydantic models throughout
- **Logging**: Structured logging with configurable levels and detailed request/response tracking
- **Performance Monitoring**: Built-in response time measurement and token usage tracking
- **Error Recovery**: Graceful fallback mechanisms and retry logic support
- **Security**: Secure API key handling with environment variable validation

**Developer Experience:**
- **Documentation**: Comprehensive API documentation with usage examples
- **Configuration**: Simple environment-based configuration with validation
- **Testing**: Easy-to-run test suite with mock providers for development
- **Validation**: One-command validation of entire application setup

**Breaking Changes:**
- Refactored from monolithic structure to modular architecture
- New configuration system requires environment variables
- AI responses now use standardized data models

**Migration Guide:**
1. Copy `.env.example` to `.env` and configure API keys
2. Run `python validate_config.py` to verify setup
3. Install any missing dependencies with `pip install -r requirements.txt`