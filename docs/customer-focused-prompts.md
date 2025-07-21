# Customer-Focused Prompt Templates

The Context Engineering Demo has been enhanced with customer-focused prompt template features that enable more effective, personalized AI interactions for customer-facing applications.

## Overview

The enhanced `PromptTemplate` class now includes specialized fields designed to improve customer experience through better AI persona definition, response style control, and personalization tracking.

## New Features

### Professional Role Definition

The `professional_role` field allows you to specify the exact professional role the AI should assume when interacting with customers.

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

# Define a customer service template
template = PromptTemplate(
    name="customer_support",
    template="Hello {customer_name}, I'm your {professional_role} and I'm here to help...",
    professional_role="customer support specialist",
    customer_focus=True
)
```

**Common Professional Roles by Industry:**

| Industry | Professional Roles |
|----------|-------------------|
| **Restaurant** | restaurant host, sommelier, dining consultant, reservation specialist |
| **Healthcare** | healthcare advisor, patient coordinator, wellness consultant, medical assistant |
| **E-commerce** | shopping assistant, product specialist, customer support specialist, personal shopper |
| **Financial** | financial advisor, investment consultant, banking specialist, loan officer |
| **Education** | academic advisor, learning consultant, course coordinator, student success coach |
| **Real Estate** | real estate agent, property consultant, market analyst, buyer's agent |

### Customer Focus Flag

The `customer_focus` boolean flag identifies templates specifically designed for direct customer interactions, enabling special handling and optimization.

```python
# Customer-facing template
customer_template = PromptTemplate(
    name="customer_greeting",
    template="Welcome {customer_name}! How can I assist you today?",
    customer_focus=True,  # Enables customer-specific optimizations
    response_style="friendly"
)

# Internal tool template
internal_template = PromptTemplate(
    name="internal_analysis",
    template="Analyze the following data: {data}",
    customer_focus=False,  # Internal use only
    response_style="professional"
)
```

### Response Style Control

The `response_style` field controls the tone and manner of AI responses to ensure consistent communication style.

**Available Response Styles:**

- **`"professional"`** - Formal, business-appropriate tone
- **`"friendly"`** - Warm, approachable, conversational
- **`"conversational"`** - Natural, casual dialogue style
- **`"formal"`** - Highly structured, official tone
- **`"casual"`** - Relaxed, informal communication

```python
# Professional financial advisor
financial_template = PromptTemplate(
    name="investment_advice",
    template="Based on your portfolio of {portfolio_value}, I recommend...",
    professional_role="financial advisor",
    response_style="professional",
    customer_focus=True
)

# Friendly restaurant host
restaurant_template = PromptTemplate(
    name="dining_recommendation",
    template="I'd love to help you find the perfect spot for {occasion}!",
    professional_role="restaurant host",
    response_style="friendly",
    customer_focus=True
)
```

### Personalization Elements Tracking

The `personalization_elements` list tracks which context elements should be used for customizing responses, helping optimize personalization strategies.

```python
# E-commerce personalization template
ecommerce_template = PromptTemplate(
    name="product_recommendation",
    template="Based on your {purchase_history} and {preferences}, here are some items you might love...",
    professional_role="personal shopping assistant",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=[
        "customer_name",
        "purchase_history", 
        "browsing_history",
        "preferences",
        "budget_range",
        "size_preferences",
        "brand_preferences"
    ]
)
```

## Industry-Specific Examples

### Restaurant Industry

```python
restaurant_contextual = PromptTemplate(
    name="restaurant_contextual_enhanced",
    template="""As your {professional_role}, I'll help you find the perfect dining experience in {location}. 
    
    Based on your preferences for {cuisine_preferences} and budget of {budget}, along with your dietary needs ({dietary_restrictions}), I can recommend restaurants that will make your {occasion} truly special.
    
    Given your past visits to {past_visits}, I'll suggest something new that matches your taste.""",
    
    prompt_type=PromptType.CONTEXTUAL,
    industry=Industry.RESTAURANT,
    professional_role="restaurant concierge",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=[
        "location",
        "cuisine_preferences", 
        "dietary_restrictions",
        "budget",
        "occasion",
        "past_visits",
        "party_size"
    ],
    description="Enhanced restaurant recommendation with full personalization"
)
```

### Healthcare Industry

```python
healthcare_contextual = PromptTemplate(
    name="healthcare_contextual_enhanced",
    template="""As your {professional_role}, I'll provide personalized health guidance based on your medical profile.
    
    Considering your medical history of {medical_history}, current medications ({current_medications}), and recent symptoms ({recent_symptoms}), I can offer relevant health insights.
    
    Your vital signs ({vital_signs}) and known allergies ({allergies}) are important factors in my recommendations.
    
    Please remember to consult with your healthcare provider for any serious concerns.""",
    
    prompt_type=PromptType.CONTEXTUAL,
    industry=Industry.HEALTHCARE,
    professional_role="healthcare advisor",
    customer_focus=True,
    response_style="professional",
    personalization_elements=[
        "medical_history",
        "current_medications",
        "allergies",
        "recent_symptoms",
        "vital_signs",
        "age",
        "gender"
    ],
    description="Enhanced healthcare guidance with comprehensive personalization"
)
```

### E-commerce Industry

Both the e-commerce system message and generic templates have been enhanced to focus on personal shopping assistance rather than business consultation:

```python
# Updated E-commerce System Template (system_ecommerce)
ecommerce_system = PromptTemplate(
    name="system_ecommerce",
    template="You are a helpful personal shopping assistant. Your goal is to help customers find exactly what they're looking for by providing product recommendations, comparing options, and guiding them through their purchasing decisions. Be friendly, knowledgeable about products, and focus on the customer's needs and preferences.",
    prompt_type=PromptType.SYSTEM,
    industry=Industry.ECOMMERCE,
    description="E-commerce industry system message",
    professional_role="shopping assistant",
    customer_focus=True,
    response_style="friendly"
)

# Updated E-commerce Generic Template (generic_ecommerce)
ecommerce_generic = PromptTemplate(
    name="generic_ecommerce",
    template="A customer is asking: {query}\n\nAs their personal shopping assistant, provide helpful product recommendations and shopping guidance. Be specific, friendly, and focus on helping them find what they need. Include product suggestions, comparisons when relevant, and practical shopping advice to make their purchasing decision easier.",
    prompt_type=PromptType.GENERIC,
    industry=Industry.ECOMMERCE,
    description="Generic e-commerce shopping assistant template",
    professional_role="shopping assistant",
    customer_focus=True,
    response_style="friendly"
)

# Enhanced Contextual Template Example
ecommerce_contextual = PromptTemplate(
    name="ecommerce_contextual_enhanced",
    template="""As your {professional_role}, I'm excited to help you find exactly what you're looking for!
    
    Based on your purchase history ({purchase_history}) and browsing patterns ({browsing_history}), I can see you have great taste in {preferred_categories}.
    
    With your budget of {budget} and preferences for {brand_preferences}, I'll show you items that perfectly match your style and needs.""",
    
    prompt_type=PromptType.CONTEXTUAL,
    industry=Industry.ECOMMERCE,
    professional_role="personal shopping assistant",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=[
        "customer_name",
        "purchase_history",
        "browsing_history", 
        "preferred_categories",
        "budget",
        "brand_preferences",
        "size_preferences",
        "style_preferences"
    ],
    description="Enhanced e-commerce assistance with comprehensive personalization"
)
```

**Key Changes in E-commerce Templates:**
- **Professional Role**: Changed from "e-commerce consultant" to "shopping assistant"
- **Focus Shift**: From business operations advice to customer shopping assistance
- **Customer-Centric Language**: Emphasizes helping customers find products and make purchasing decisions
- **Friendly Tone**: Uses warm, approachable language suitable for retail interactions

## Implementation Guide

### Step 1: Define Customer-Focused Templates

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

def create_customer_template(industry: Industry, role: str, style: str):
    """Create a customer-focused template for an industry."""
    return PromptTemplate(
        name=f"customer_{industry.value}_{role.replace(' ', '_')}",
        template="As your {professional_role}, I'm here to provide personalized assistance...",
        prompt_type=PromptType.CONTEXTUAL,
        industry=industry,
        professional_role=role,
        customer_focus=True,
        response_style=style,
        personalization_elements=get_personalization_elements(industry)
    )

def get_personalization_elements(industry: Industry) -> List[str]:
    """Get relevant personalization elements for an industry."""
    elements_map = {
        Industry.RESTAURANT: ["location", "cuisine_preferences", "dietary_restrictions", "budget", "occasion"],
        Industry.HEALTHCARE: ["medical_history", "current_medications", "symptoms", "age"],
        Industry.ECOMMERCE: ["purchase_history", "preferences", "budget", "brand_preferences"],
        Industry.FINANCIAL: ["income", "savings", "goals", "risk_tolerance", "age"],
        Industry.EDUCATION: ["grade_level", "learning_style", "subjects", "goals"],
        Industry.REAL_ESTATE: ["budget", "location_preferences", "property_type", "timeline"]
    }
    return elements_map.get(industry, [])
```

### Step 2: Register Templates with Prompt Service

```python
from services.prompt_service import get_prompt_service

prompt_service = get_prompt_service()

# Create and register customer-focused templates
industries_and_roles = [
    (Industry.RESTAURANT, "restaurant concierge", "friendly"),
    (Industry.HEALTHCARE, "healthcare advisor", "professional"),
    (Industry.ECOMMERCE, "personal shopping assistant", "friendly"),
    (Industry.FINANCIAL, "financial advisor", "professional"),
    (Industry.EDUCATION, "academic advisor", "conversational"),
    (Industry.REAL_ESTATE, "real estate consultant", "professional")
]

for industry, role, style in industries_and_roles:
    template = create_customer_template(industry, role, style)
    prompt_service.register_template(template)
```

### Step 3: Use Templates in AI Interactions

```python
from services.ai_orchestrator import AIServiceOrchestrator
from services.ai_service import PromptRequest

# Initialize AI orchestrator
orchestrator = AIServiceOrchestrator()

# Generate customer-focused response
def generate_customer_response(query: str, context: dict, industry: Industry):
    # Get customer-focused template
    template = prompt_service.get_template(f"customer_{industry.value}_contextual")
    
    if template and template.customer_focus:
        # Generate contextual prompt using customer-focused template
        contextual_prompt = prompt_service.generate_contextual_prompt(
            query=query,
            context=context,
            industry=industry
        )
        
        # Generate system message with professional role
        system_message = f"You are a {template.professional_role}. Respond in a {template.response_style} manner."
        
        # Create AI request
        request = PromptRequest(
            prompt=contextual_prompt,
            system_message=system_message,
            context=context
        )
        
        # Generate response
        return orchestrator.generate_response(request)
    
    return None
```

## Best Practices

### Professional Role Selection

1. **Industry Alignment**: Choose roles that are recognized and trusted in the industry
2. **Expertise Level**: Match the role to the complexity of queries you expect
3. **Customer Expectations**: Use roles that customers would expect to interact with
4. **Consistency**: Maintain the same role throughout a conversation session

### Response Style Guidelines

1. **Audience Appropriate**: Match style to your target customer demographic
2. **Brand Alignment**: Ensure style aligns with your brand voice and values
3. **Context Sensitive**: Consider the situation (emergency vs. casual inquiry)
4. **Cultural Awareness**: Adapt style for different cultural contexts

### Personalization Element Strategy

1. **Privacy First**: Only include elements you have permission to use
2. **Relevance**: Focus on elements that genuinely improve the experience
3. **Data Quality**: Ensure personalization data is accurate and up-to-date
4. **Fallback Handling**: Design graceful degradation when personalization data is missing

## Integration with Existing Systems

### Demo Framework Integration

```python
# Enhanced demo base class usage
class RestaurantDemo(BaseDemo):
    def __init__(self, ai_service=None, context_service=None):
        super().__init__("Restaurant Reservations", Industry.RESTAURANT, ai_service, context_service)
        self.prompt_service = get_prompt_service()
    
    def get_system_message_contextual(self) -> str:
        """Get customer-focused system message."""
        template = self.prompt_service.get_template("customer_restaurant_contextual")
        if template and template.customer_focus:
            return f"You are a {template.professional_role}. Respond in a {template.response_style} manner, using the provided context to personalize your recommendations."
        return super().get_system_message_contextual()
```

### AI Orchestrator Integration

The customer-focused templates work seamlessly with the existing AI Service Orchestrator:

```python
# The orchestrator automatically uses enhanced templates
orchestrator = AIServiceOrchestrator()

# Customer-focused templates are automatically selected when available
response = orchestrator.generate_response(request)
```

## Monitoring and Analytics

### Template Performance Tracking

```python
def track_template_usage(template: PromptTemplate, response_quality: float):
    """Track how customer-focused templates perform."""
    metrics = {
        'template_name': template.name,
        'customer_focus': template.customer_focus,
        'professional_role': template.professional_role,
        'response_style': template.response_style,
        'personalization_elements_used': len(template.personalization_elements),
        'response_quality_score': response_quality
    }
    
    # Log metrics for analysis
    logger.info("Template usage", extra=metrics)
```

### Customer Satisfaction Correlation

```python
def analyze_customer_satisfaction():
    """Analyze correlation between template features and satisfaction."""
    # Example analysis of which features correlate with higher satisfaction
    customer_focused_satisfaction = get_satisfaction_by_feature('customer_focus', True)
    response_style_satisfaction = get_satisfaction_by_response_style()
    role_satisfaction = get_satisfaction_by_professional_role()
    
    return {
        'customer_focused_avg': customer_focused_satisfaction,
        'response_style_breakdown': response_style_satisfaction,
        'professional_role_breakdown': role_satisfaction
    }
```

## Migration Guide

### Updating Existing Templates

```python
# Before: Basic template
old_template = PromptTemplate(
    name="restaurant_greeting",
    template="Welcome! How can I help you?",
    prompt_type=PromptType.GENERIC
)

# After: Customer-focused template
new_template = PromptTemplate(
    name="restaurant_greeting",
    template="Welcome to our restaurant! I'm your {professional_role} and I'm delighted to help you find the perfect dining experience.",
    prompt_type=PromptType.GENERIC,
    professional_role="restaurant host",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=["dining_preferences", "occasion", "party_size"]
)
```

### Backward Compatibility

All existing templates continue to work without modification. The new fields have sensible defaults:

- `professional_role`: Empty string (no specific role)
- `customer_focus`: False (not customer-focused)
- `response_style`: "professional" (default professional tone)
- `personalization_elements`: Empty list (no tracked elements)

## Future Enhancements

### Planned Features

1. **Dynamic Role Selection**: AI chooses the most appropriate professional role based on query context
2. **Style Adaptation**: Automatic response style adjustment based on customer interaction history
3. **Personalization Scoring**: Automatic scoring of how well personalization elements are utilized
4. **A/B Testing Framework**: Built-in testing for different template variations
5. **Multi-language Support**: Professional roles and response styles adapted for different languages

### Extension Points

The customer-focused template system is designed for easy extension:

```python
# Custom response style
class CustomResponseStyle(str, Enum):
    EMPATHETIC = "empathetic"
    TECHNICAL = "technical"
    CONSULTATIVE = "consultative"

# Custom professional role categories
class ProfessionalRoleCategory(str, Enum):
    ADVISOR = "advisor"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    CONSULTANT = "consultant"
```

This customer-focused prompt template system provides a solid foundation for creating more engaging, personalized AI interactions that better serve customer needs across different industries and use cases.
</content>