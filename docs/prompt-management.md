# Prompt Management System

The Context Engineering Demo includes a comprehensive prompt management system that provides structured, industry-specific prompt templates for AI interactions. This system ensures consistent, high-quality prompts across different industries and use cases.

## Overview

The Prompt Management System consists of several key components:

- **PromptTemplate**: Template class with variable substitution
- **PromptService**: Central service for managing templates
- **PromptValidator**: Validation utilities for prompts and context
- **Industry-Specific Templates**: Pre-built templates for each supported industry

## Core Components

### PromptTemplate Class

The `PromptTemplate` class represents a reusable prompt template with variable substitution and enhanced customer-focused features:

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

# Create a custom template with enhanced features
template = PromptTemplate(
    name="custom_restaurant_greeting",
    template="Welcome to {restaurant_name}! We specialize in {cuisine_type}. How can we help you today?",
    prompt_type=PromptType.GENERIC,
    industry=Industry.RESTAURANT,
    description="Custom restaurant greeting template",
    professional_role="restaurant host",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=["restaurant_name", "cuisine_type", "customer_preferences"]
)

# Render the template
rendered = template.render(
    restaurant_name="Mario's Italian Bistro",
    cuisine_type="authentic Italian cuisine"
)
print(rendered)
# Output: "Welcome to Mario's Italian Bistro! We specialize in authentic Italian cuisine. How can we help you today?"
```

#### Template Features

- **Variable Extraction**: Automatically detects `{variable_name}` patterns
- **Validation**: Built-in validation for template structure and content
- **Serialization**: Convert to/from dictionary for storage
- **Metadata Support**: Additional metadata for template management
- **Professional Role Definition**: Specify the professional role the AI should assume
- **Customer Focus**: Flag templates designed for customer-facing interactions
- **Response Style Control**: Define the tone and style of AI responses
- **Personalization Elements**: Track which context elements enable personalization

#### Enhanced Customer-Focused Features

The `PromptTemplate` class now includes specialized fields for creating more effective customer-facing AI interactions:

**Professional Role (`professional_role`)**
- Defines the specific professional role the AI should assume
- Examples: "shopping assistant", "medical practitioner", "financial advisor", "restaurant host"
- Helps establish appropriate expertise and communication style

**Customer Focus (`customer_focus`)**
- Boolean flag indicating if the template is designed for direct customer interactions
- Enables special handling for customer-facing scenarios
- Helps differentiate between internal tools and customer-facing applications

**Response Style (`response_style`)**
- Controls the tone and manner of AI responses
- Options: "conversational", "professional", "friendly", "formal", "casual"
- Ensures consistent communication style across interactions

**Personalization Elements (`personalization_elements`)**
- List of context elements that enable personalization
- Tracks which data points should be used for customizing responses
- Helps optimize context usage for better personalization

```python
# Example of customer-focused template
customer_service_template = PromptTemplate(
    name="customer_support_greeting",
    template="Hello {customer_name}! I'm your {professional_role} and I'm here to help with {inquiry_type}. Based on your {customer_tier} status, I can provide specialized assistance.",
    prompt_type=PromptType.CONTEXTUAL,
    industry=Industry.ECOMMERCE,
    description="Customer service greeting with personalization",
    professional_role="customer support specialist",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=["customer_name", "customer_tier", "purchase_history", "preferences"]
)
```

### PromptService Class

The central service for managing prompt templates:

```python
from services.prompt_service import get_prompt_service, Industry

# Get the global prompt service instance
prompt_service = get_prompt_service()

# Generate a generic prompt
generic_prompt = prompt_service.generate_generic_prompt(
    query="I need help with menu planning",
    industry=Industry.RESTAURANT
)

# Generate a contextual prompt
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

# Generate system message
system_message = prompt_service.generate_system_message(Industry.RESTAURANT)
```

### PromptValidator Class

Validation utilities for ensuring prompt quality and security:

```python
from services.prompt_service import PromptValidator

# Validate prompt content
issues = PromptValidator.validate_prompt_content(
    "This is a test prompt for validation"
)

# Validate context data
context_issues = PromptValidator.validate_context_data({
    "user": "John Doe",
    "preferences": ["Italian", "Mexican"],
    "budget": 50
})

if not issues and not context_issues:
    print("Prompt and context are valid!")
```

## Supported Industries

The system includes pre-built templates for six industries:

### Restaurant Industry
- **Generic**: General restaurant advice and recommendations
- **Contextual**: Personalized recommendations based on dining preferences
- **System**: Restaurant consultant persona

### Healthcare Industry
- **Generic**: General healthcare practice guidance
- **Contextual**: Practice-specific recommendations
- **System**: Healthcare administration consultant persona

### E-commerce Industry
- **Generic**: Online retail best practices
- **Contextual**: Business-specific e-commerce advice
- **System**: Personal shopping assistant persona (updated to focus on customer assistance rather than business consultation)

### Financial Services Industry
- **Generic**: Financial industry best practices
- **Contextual**: Institution-specific guidance
- **System**: Financial services consultant persona

### Education Industry
- **Generic**: Educational best practices and methods
- **Contextual**: Institution-specific recommendations
- **System**: Educational consultant persona

### Real Estate Industry
- **Generic**: Real estate industry guidance
- **Contextual**: Market and client-specific advice
- **System**: Real estate expert persona

## Template Types

### PromptType Enum

```python
class PromptType(str, Enum):
    GENERIC = "generic"              # General responses without context
    CONTEXTUAL = "contextual"        # Personalized responses with context
    SYSTEM = "system"                # System messages for AI providers
    INDUSTRY_SPECIFIC = "industry_specific"  # Industry-specialized templates
```

### Industry Enum

```python
class Industry(str, Enum):
    RESTAURANT = "restaurant"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    FINANCIAL = "financial"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
```

## Usage Examples

### Basic Template Management

```python
from services.prompt_service import get_prompt_service, PromptTemplate, PromptType

prompt_service = get_prompt_service()

# Register a custom template with enhanced features
custom_template = PromptTemplate(
    name="custom_greeting",
    template="Hello {name}, welcome to our {service_type} service!",
    prompt_type=PromptType.GENERIC,
    description="Custom greeting template",
    professional_role="customer service representative",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=["name", "service_type", "customer_history"]
)

prompt_service.register_template(custom_template)

# List all templates
all_templates = prompt_service.list_templates()

# List templates by type
generic_templates = prompt_service.list_templates(prompt_type=PromptType.GENERIC)

# List templates by industry
restaurant_templates = prompt_service.list_templates(industry=Industry.RESTAURANT)

# Filter customer-focused templates
customer_templates = [t for t in all_templates if t.customer_focus]
```

### Advanced Template Usage

```python
# Get a specific template
template = prompt_service.get_template("contextual_restaurant")

if template:
    # Validate template
    errors = template.validate()
    if not errors:
        # Render with context
        rendered = template.render(
            query="Find me a romantic dinner spot",
            context=json.dumps({
                "location": "New York, NY",
                "budget": "$80-120 per person",
                "occasion": "anniversary"
            }, indent=2)
        )
        print(rendered)
```

### Integration with AI Providers

```python
from services.ai_service import PromptRequest
from services.prompt_service import get_prompt_service, Industry

prompt_service = get_prompt_service()

# Generate prompts for AI provider
user_query = "I need help choosing a restaurant"
user_context = {
    "location": "San Francisco, CA",
    "dietary_restrictions": ["vegetarian"],
    "budget": "$30-50 per person"
}

# Generate contextual prompt
contextual_prompt = prompt_service.generate_contextual_prompt(
    query=user_query,
    context=user_context,
    industry=Industry.RESTAURANT
)

# Generate system message
system_message = prompt_service.generate_system_message(Industry.RESTAURANT)

# Create AI request
ai_request = PromptRequest(
    prompt=contextual_prompt,
    system_message=system_message,
    context=user_context
)

# Send to AI provider
# response = ai_provider.generate_response(ai_request)
```

## Template Structure

### Default Templates

The system includes default templates for each combination of prompt type and industry:

#### Generic Templates
- `generic_default`: Basic generic response template
- `generic_restaurant`: Restaurant-specific generic template
- `generic_healthcare`: Healthcare-specific generic template
- `generic_ecommerce`: E-commerce-specific generic template
- `generic_financial`: Financial services generic template
- `generic_education`: Education-specific generic template
- `generic_real_estate`: Real estate generic template

#### Contextual Templates
- `contextual_default`: Basic contextual response template
- `contextual_restaurant`: Restaurant-specific contextual template
- `contextual_healthcare`: Healthcare-specific contextual template
- `contextual_ecommerce`: E-commerce-specific contextual template
- `contextual_financial`: Financial services contextual template
- `contextual_education`: Education-specific contextual template
- `contextual_real_estate`: Real estate contextual template

#### System Templates
- `system_default`: Basic system message
- `system_restaurant`: Restaurant consultant persona
- `system_healthcare`: Healthcare consultant persona
- `system_ecommerce`: Personal shopping assistant persona (updated from e-commerce consultant)
- `system_financial`: Financial consultant persona
- `system_education`: Educational consultant persona
- `system_real_estate`: Real estate expert persona

## Validation and Security

### Content Validation

The system includes comprehensive validation to ensure prompt quality and security:

```python
# Prompt content validation checks for:
# - Empty or too short content
# - Excessive length (>8000 characters)
# - Suspicious injection patterns
# - Excessive word repetition

issues = PromptValidator.validate_prompt_content(prompt_text)
```

### Context Data Validation

```python
# Context validation checks for:
# - Proper dictionary structure
# - JSON serializability
# - Reasonable size (<50KB)
# - Nesting depth (<10 levels)

issues = PromptValidator.validate_context_data(context_dict)
```

### Template Validation

```python
# Template validation checks for:
# - Non-empty template content
# - Balanced braces for variables
# - Valid variable names
# - Reasonable template length

template = PromptTemplate(name="test", template="Hello {name}!", prompt_type=PromptType.GENERIC)
errors = template.validate()
```

## Best Practices

### Template Design

1. **Clear Variable Names**: Use descriptive variable names like `{user_name}` instead of `{n}`
2. **Consistent Formatting**: Follow consistent formatting patterns across templates
3. **Appropriate Length**: Keep templates concise but comprehensive
4. **Industry Relevance**: Ensure templates are relevant to their target industry

### Context Management

1. **Structured Data**: Use well-structured dictionaries for context data
2. **Reasonable Size**: Keep context data under 50KB for performance
3. **Validation**: Always validate context data before use
4. **Sensitive Data**: Avoid including sensitive information in context

### Security Considerations

1. **Input Validation**: Always validate user inputs and context data
2. **Injection Prevention**: The system automatically checks for suspicious patterns
3. **Content Filtering**: Review generated prompts for inappropriate content
4. **Access Control**: Implement appropriate access controls for template management

## Error Handling

The prompt service includes comprehensive error handling:

```python
try:
    # Template rendering with missing variables
    rendered = template.render(name="John")  # Missing required variable
except ValueError as e:
    print(f"Template error: {e}")

try:
    # Invalid context data
    prompt = prompt_service.generate_contextual_prompt(
        query="test",
        context="invalid_context"  # Should be dict
    )
except ValueError as e:
    print(f"Context error: {e}")
```

## Integration Points

### AI Service Integration

The Prompt Service integrates seamlessly with the AI Service infrastructure:

```python
# The AI providers can use the prompt service for consistent prompting
from services.ai_orchestrator import AIServiceOrchestrator
from services.prompt_service import get_prompt_service, Industry

orchestrator = AIServiceOrchestrator()
prompt_service = get_prompt_service()

# Generate industry-specific prompts
system_message = prompt_service.generate_system_message(Industry.HEALTHCARE)
contextual_prompt = prompt_service.generate_contextual_prompt(
    query=user_query,
    context=patient_context,
    industry=Industry.HEALTHCARE
)

# Use with orchestrator
request = PromptRequest(
    prompt=contextual_prompt,
    system_message=system_message,
    context=patient_context
)

response = orchestrator.generate_response(request)
```

### Demo Framework Integration

The demo framework can leverage the prompt service for consistent prompting:

```python
# In demo implementations
class RestaurantDemo(BaseDemo):
    def __init__(self, ai_service=None, context_service=None):
        super().__init__("Restaurant Reservations", ai_service, context_service)
        self.prompt_service = get_prompt_service()
    
    def get_system_message_contextual(self) -> str:
        return self.prompt_service.generate_system_message(Industry.RESTAURANT)
```

## Configuration

The Prompt Service uses the application's configuration system:

```python
# Configuration is loaded from config/settings.py
from config.settings import get_settings

settings = get_settings()
# Prompt service automatically uses application settings
```

## Extensibility

### Adding Custom Templates

```python
# Create and register custom templates
custom_template = PromptTemplate(
    name="custom_industry_template",
    template="Custom template for {industry} with {context_type}",
    prompt_type=PromptType.INDUSTRY_SPECIFIC,
    industry=Industry.RESTAURANT,
    description="Custom industry-specific template"
)

prompt_service.register_template(custom_template)
```

### Custom Industries

To add support for new industries:

1. Extend the `Industry` enum
2. Create templates for the new industry
3. Register templates with the prompt service
4. Update demo framework if needed

## Performance Considerations

- **Template Caching**: Templates are cached in memory for fast access
- **Context Validation**: Validation is performed once per context
- **Lazy Loading**: Templates are loaded on service initialization
- **Memory Usage**: Monitor memory usage with large numbers of custom templates

## Troubleshooting

### Common Issues

1. **Missing Variables**: Ensure all template variables are provided during rendering
2. **Invalid Context**: Validate context data structure and content
3. **Template Conflicts**: Check for name conflicts when registering templates
4. **Validation Errors**: Review validation messages for specific issues

### Debug Information

```python
# Enable debug logging
import logging
logging.getLogger('PromptService').setLevel(logging.DEBUG)

# Check template registration
templates = prompt_service.list_templates()
print(f"Registered templates: {[t.name for t in templates]}")

# Validate specific template
template = prompt_service.get_template("contextual_restaurant")
if template:
    errors = template.validate()
    print(f"Template validation: {errors or 'Valid'}")
```

This prompt management system provides a robust foundation for consistent, industry-specific AI interactions while maintaining flexibility for customization and extension.