# Prompt Service Documentation

This document provides comprehensive documentation for the Prompt Service system, including the customer-focused transformation and professional role implementation across all industries.

## Table of Contents
1. [System Overview](#system-overview)
2. [Customer-Focused Transformation](#customer-focused-transformation)
3. [Professional Roles by Industry](#professional-roles-by-industry)
4. [Template Structure and Usage](#template-structure-and-usage)
5. [Response Format Guidelines](#response-format-guidelines)
6. [Implementation Examples](#implementation-examples)
7. [Recent Updates](#recent-updates)

## System Overview

The Prompt Service system provides a comprehensive framework for managing AI prompt templates across multiple industries. The system has been transformed from a business consultation approach to a customer-focused professional service model, where AI assistants act as industry-specific professionals helping customers directly.

### Key Components

- **PromptTemplate Class**: Enhanced with customer-focused attributes
- **Industry-Specific Templates**: Tailored for six major industries
- **Professional Role System**: Defines AI personas for authentic interactions
- **Response Format Guidelines**: Ensures consistent, professional responses
- **Validation Framework**: Maintains quality and appropriateness of templates

### Supported Industries

1. **E-commerce**: Shopping assistance and product recommendations
2. **Healthcare**: Medical guidance and health information
3. **Restaurant**: Dining recommendations and reservation assistance
4. **Financial**: Personal financial advice and planning
5. **Education**: Academic guidance and learning support
6. **Real Estate**: Property assistance and market insights

## Customer-Focused Transformation

The system underwent a fundamental transformation from business consultation to customer service:

### The Problem
Originally, the AI responded to customer queries with business advice:
- **User**: "Show me running shoes for women"
- **Old AI**: "Here are best practices for selling women's running shoes online..."

### The Solution
Now, the AI responds as a helpful professional:
- **User**: "Show me running shoes for women"
- **New AI**: "I'd be happy to help you find the perfect running shoes! Here are some excellent options..."

### Transformation Benefits
- **Relevant Responses**: Users get direct help with their actual needs
- **Professional Experience**: Interactions feel authentic and helpful
- **Personalized Service**: Recommendations tailored to user context
- **Natural Conversations**: Responses match customer expectations

## Professional Roles by Industry

Each industry has a defined professional role that the AI assumes:

### E-commerce: Personal Shopping Assistant
- **Role**: Friendly shopping assistant helping customers find products
- **Approach**: Product recommendations, comparisons, shopping guidance
- **Tone**: Enthusiastic, helpful, customer-focused
- **Specialties**: Product knowledge, price comparisons, feature explanations

### Healthcare: Medical Practitioner
- **Role**: Knowledgeable healthcare professional
- **Approach**: Health guidance, medical information, wellness tips
- **Tone**: Caring, empathetic, professional
- **Specialties**: Health conditions, preventive care, medical disclaimers

### Restaurant: Concierge Service
- **Role**: Professional dining concierge
- **Approach**: Restaurant recommendations, reservation assistance, dining guidance
- **Tone**: Warm, hospitable, knowledgeable
- **Specialties**: Cuisine expertise, atmosphere matching, special occasions

### Financial: Personal Financial Advisor
- **Role**: Dedicated financial advisor
- **Approach**: Financial planning, investment guidance, goal-oriented advice
- **Tone**: Professional, trustworthy, educational
- **Specialties**: Investment strategies, financial planning, risk assessment

### Education: Academic Advisor
- **Role**: Supportive educator and academic advisor
- **Approach**: Learning guidance, academic advice, educational resources
- **Tone**: Encouraging, supportive, knowledgeable
- **Specialties**: Learning styles, career guidance, academic planning

### Real Estate: Professional Agent
- **Role**: Experienced real estate agent
- **Approach**: Property guidance, market insights, buying/selling advice
- **Tone**: Professional, knowledgeable, client-focused
- **Specialties**: Market conditions, property values, neighborhood expertise

## Template Structure and Usage

### Template Types

#### System Message Templates
Define the AI's professional role and overall approach:
```python
# Example: E-commerce System Message
"You are a helpful personal shopping assistant. Your goal is to help customers find exactly what they're looking for by providing product recommendations, comparing options, and guiding them through their purchasing decisions."
```

#### Generic Templates
Handle general queries without specific customer context:
```python
# Example: E-commerce Generic Template
"""A customer is asking: {query}

As their personal shopping assistant, provide helpful product recommendations and shopping guidance. Be specific, friendly, and focus on helping them find what they need."""
```

#### Contextual Templates
Use customer data for personalized responses:
```python
# Example: E-commerce Contextual Template
"""You are helping a specific customer with their shopping needs.

Customer Query: {query}
Customer Profile: {context}

Use their purchase history, preferences, and profile to provide personalized product recommendations."""
```

### Enhanced Template Attributes

```python
@dataclass
class PromptTemplate:
    name: str                                    # Unique identifier
    template: str                               # Template content with placeholders
    prompt_type: PromptType                     # GENERIC, CONTEXTUAL, or SYSTEM
    industry: Optional[Industry] = None         # Industry specialization
    professional_role: str = ""                 # Professional role (e.g., "shopping assistant")
    customer_focus: bool = False                # Whether template is customer-facing
    response_style: str = "professional"        # Response tone and style
    personalization_elements: List[str] = []    # Context elements for personalization
    variables: List[str] = []                   # Required template variables
    description: str = ""                       # Human-readable description
    metadata: Dict[str, Any] = {}              # Additional metadata
```

## Response Format Guidelines

Each industry includes specific response format guidelines to ensure consistent, professional interactions:

### Universal Guidelines
1. **Warm Opening**: Acknowledge the customer's request
2. **Clear Structure**: Use bullet points or numbered lists for organization
3. **Specific Information**: Include detailed, actionable recommendations
4. **Conversational Tone**: Match the industry's appropriate style
5. **Clear Call-to-Action**: End with helpful follow-up suggestions

### Industry-Specific Examples

#### E-commerce Response Format
```
RESPONSE FORMAT GUIDELINES:
- Start with an enthusiastic acknowledgment of their shopping request
- Structure product recommendations with clear categories or bullet points
- Include specific details like prices, features, and benefits
- Use friendly, conversational language that feels personal
- End with a clear call-to-action about next steps
- Keep paragraphs short and scannable
```

#### Healthcare Response Format
```
RESPONSE FORMAT GUIDELINES:
- Start with a caring acknowledgment of their health concern
- Structure health information with clear sections using bullet points
- Include specific, actionable health guidance
- Use empathetic, supportive language showing genuine concern
- Always include appropriate medical disclaimers
- End with guidance about when to consult healthcare providers
```

#### Restaurant Response Format
```
RESPONSE FORMAT GUIDELINES:
- Start with a warm, conversational greeting acknowledging their request
- Structure restaurant recommendations with key details (cuisine, atmosphere, price)
- Use friendly, conversational language that feels personal and engaging
- Include specific recommendations with reasoning
- End with offers to help with reservations or additional information
- Keep information organized and easy to scan
```

## Implementation Examples

### Creating Customer-Focused Templates

```python
from services.prompt_service import PromptTemplate, PromptType, Industry

# E-commerce shopping assistant template
ecommerce_template = PromptTemplate(
    name="ecommerce_shopping_assistant",
    template="""A customer is asking: {query}

As their personal shopping assistant, I'll help them find exactly what they need. Let me provide specific product recommendations with details about features, prices, and benefits to make their decision easier.

RESPONSE FORMAT GUIDELINES:
- Start with enthusiasm about helping them shop
- Organize recommendations with bullet points
- Include specific product details and prices
- Use friendly, conversational language
- End with a helpful call-to-action
- Keep information scannable and easy to read""",
    prompt_type=PromptType.GENERIC,
    industry=Industry.ECOMMERCE,
    professional_role="personal shopping assistant",
    customer_focus=True,
    response_style="friendly",
    personalization_elements=["purchase_history", "preferences", "budget"],
    description="Customer-focused e-commerce shopping assistance"
)
```

### Using Templates in Applications

```python
from services.prompt_service import get_prompt_service
from services.ai_orchestrator import AIServiceOrchestrator

# Initialize services
prompt_service = get_prompt_service()
orchestrator = AIServiceOrchestrator()

# Generate customer-focused response
def generate_customer_response(query: str, context: dict, industry: Industry):
    # Get system message for professional role
    system_message = prompt_service.generate_system_message(industry)
    
    # Generate contextual prompt if context available
    if context:
        prompt = prompt_service.generate_contextual_prompt(query, context, industry)
    else:
        prompt = prompt_service.generate_generic_prompt(query, industry)
    
    # Generate response with professional persona
    request = PromptRequest(
        prompt=prompt,
        system_message=system_message,
        context=context
    )
    
    return orchestrator.generate_response(request)
```

### Validation and Quality Assurance

```python
# Validate customer-focused templates
def validate_customer_templates():
    prompt_service = get_prompt_service()
    
    for template_name in prompt_service.list_templates():
        template = prompt_service.get_template(template_name)
        
        if template.customer_focus:
            errors = template.validate()
            if errors:
                print(f"Template {template_name} has issues: {errors}")
            else:
                print(f"Template {template_name} is valid")
                
            # Check professional role consistency
            if not template.professional_role:
                print(f"Warning: {template_name} lacks professional role definition")
```

## Recent Updates

### January 2025 - Response Format Guidelines Enhancement

**Change Summary:**
All industry prompt templates have been enhanced with comprehensive **Response Format Guidelines** that provide specific instructions for AI response structure, tone, and formatting. This update ensures consistent, professional, and user-friendly AI responses across all industries.

**Key Features Added:**
- **Structured Response Guidelines**: Clear formatting instructions for AI responses
- **Industry-Specific Formatting**: Tailored guidelines for each industry's unique needs
- **Conversational Flow**: Guidelines for natural, engaging dialogue patterns
- **Call-to-Action Integration**: Specific instructions for helpful follow-up suggestions
- **Accessibility Focus**: Emphasis on scannable, easy-to-read response formats

**Industries Enhanced:**
- ✅ **Restaurant**: Warm, conversational dining recommendations with clear sections
- ✅ **Healthcare**: Caring, empathetic health guidance with structured information
- ✅ **E-commerce**: Friendly, enthusiastic shopping assistance with product organization
- ✅ **Financial**: Professional, trustworthy financial advice with clear sections
- ✅ **Education**: Encouraging, supportive academic guidance with learning recommendations
- ✅ **Real Estate**: Professional, knowledgeable property guidance with market insights

**Example Response Format Guidelines (Restaurant Industry):**
```
RESPONSE FORMAT GUIDELINES:
- Start with a warm, conversational greeting that acknowledges their request
- Structure your response with clear sections using bullet points or numbered lists when appropriate
- Include specific restaurant recommendations with key details (cuisine type, atmosphere, price range)
- Use friendly, conversational language that feels personal and engaging
- End with a clear call-to-action (e.g., "Would you like me to help you make a reservation?" or "Let me know if you'd like more details about any of these options!")
- Keep paragraphs short and scannable for easy reading
```

**Template Structure Enhancement:**
All templates now follow this enhanced structure:
1. **Professional Role Definition**: Clear persona for the AI assistant
2. **Industry-Specific Guidance**: Tailored advice for the specific industry context
3. **Response Format Guidelines**: Detailed formatting and structure instructions
4. **Personalization Instructions**: How to use context data effectively
5. **Call-to-Action Requirements**: Specific guidance for helpful follow-ups

**Benefits of Response Format Guidelines:**
- **Consistency**: All AI responses follow predictable, professional formatting
- **Readability**: Structured responses are easier to scan and understand
- **Engagement**: Clear call-to-actions encourage continued interaction
- **Accessibility**: Short paragraphs and bullet points improve readability
- **Professional Quality**: Responses feel more polished and helpful

### January 2025 - E-commerce Template Enhancement

**Change Summary:**
Both the e-commerce system message template (`system_ecommerce`) and generic template (`generic_ecommerce`) have been updated to focus on customer-facing shopping assistance rather than business consultation.

**System Message Template Changes:**

#### Before:
```python
template="You are an e-commerce and digital retail consultant. Provide expert advice on online business operations, digital marketing, customer experience, and e-commerce best practices."
```

#### After:
```python
template="You are a helpful personal shopping assistant. Your goal is to help customers find exactly what they're looking for by providing product recommendations, comparing options, and guiding them through their purchasing decisions. Be friendly, knowledgeable about products, and focus on the customer's needs and preferences."
```

**Generic Template Changes:**

#### Before:
```python
template="""User Query: {query}

Please provide e-commerce and online retail guidance. Focus on best practices for online sales, customer experience, digital marketing, and business operations."""
```

#### After:
```python
template="""A customer is asking: {query}

As their personal shopping assistant, provide helpful product recommendations and shopping guidance. Be specific, friendly, and focus on helping them find what they need. Include product suggestions, comparisons when relevant, and practical shopping advice to make their purchasing decision easier."""
```

**New Template Attributes:**
- `professional_role`: "shopping assistant"
- `customer_focus`: `True`
- `response_style`: "friendly"

**Impact:**
- **AI Behavior**: The AI now acts as a personal shopping assistant rather than a business consultant
- **Customer Experience**: More customer-centric language and approach
- **Response Style**: Friendlier, more approachable tone suitable for retail interactions
- **Focus Shift**: From business operations advice to product recommendations and purchase guidance

**Benefits:**
1. **Better Customer Alignment**: The AI persona now matches what customers expect from an e-commerce interaction
2. **Improved User Experience**: More helpful and relevant responses for shopping-related queries
3. **Consistent Branding**: Aligns with customer-focused approach across all industry templates
4. **Enhanced Personalization**: Better integration with customer context data for product recommendations

## Template Enhancement Features

### Customer-Focused Language Validation

The `PromptTemplate` class now includes validation to ensure customer-focused templates use appropriate language:

**Validation Checks:**
- **Business Consultation Language Detection**: Identifies and flags business-oriented phrases that should be avoided in customer-facing templates
- **Customer Service Language Requirements**: Ensures customer-focused templates include appropriate service-oriented language
- **Professional Role Validation**: Requires customer-focused templates to specify a professional role

**Example Validation:**
```python
# This would trigger a validation warning
business_template = PromptTemplate(
    name="bad_customer_template",
    template="I am a business consultant providing operational guidance...",
    customer_focus=True  # Conflicts with business consultation language
)

errors = business_template.validate()
# Returns: ["Customer-focused template should avoid business consultation language: 'business consultant'"]
```

### Enhanced Template Attributes

All system message templates now support enhanced customer-focused attributes:

```python
@dataclass
class PromptTemplate:
    # ... existing fields ...
    professional_role: str = ""           # The professional role the AI should assume
    customer_focus: bool = False          # Whether this template is for customer interactions
    response_style: str = "professional"  # Style of response (friendly, professional, etc.)
    personalization_elements: List[str] = field(default_factory=list)  # Context elements for personalization
```

## Migration Guide

### For Existing E-commerce Integrations

If you're using the e-commerce system message template, no code changes are required. The template will automatically use the new customer-focused approach.

**Before (automatic):**
```python
system_message = prompt_service.generate_system_message(Industry.ECOMMERCE)
# Returns business consultant persona
```

**After (automatic):**
```python
system_message = prompt_service.generate_system_message(Industry.ECOMMERCE)
# Returns shopping assistant persona
```

### For Custom Templates

If you have custom e-commerce templates, consider updating them to align with the new customer-focused approach:

```python
# Update custom templates to use customer-focused attributes
custom_ecommerce_template = PromptTemplate(
    name="custom_ecommerce_greeting",
    template="Hello! I'm your personal shopping assistant. How can I help you find the perfect products today?",
    prompt_type=PromptType.GENERIC,
    industry=Industry.ECOMMERCE,
    professional_role="shopping assistant",
    customer_focus=True,
    response_style="friendly",
    description="Customer-focused e-commerce greeting"
)
```

## Testing and Validation

### Validation Script

You can test the updated templates using the validation script:

```bash
python validate_prompt_service.py
```

This will verify that all templates, including the updated e-commerce template, pass validation checks.

### Manual Testing

Test the updated e-commerce system message:

```python
from services.prompt_service import get_prompt_service, Industry

prompt_service = get_prompt_service()
system_message = prompt_service.generate_system_message(Industry.ECOMMERCE)
print(system_message)

# Should output the new shopping assistant message
```

## Future Enhancements

### Planned Updates

1. **Additional Industry Templates**: Similar customer-focused updates for other industries
2. **Dynamic Role Selection**: AI chooses the most appropriate professional role based on context
3. **Response Style Adaptation**: Automatic style adjustment based on customer interaction patterns
4. **A/B Testing Framework**: Built-in testing for different template variations

### Contributing Template Updates

When updating templates, follow these guidelines:

1. **Customer-First Approach**: Focus on customer needs rather than business operations
2. **Clear Professional Roles**: Define specific, recognizable professional roles
3. **Appropriate Response Styles**: Match the style to the industry and customer expectations
4. **Validation Compliance**: Ensure templates pass all validation checks
5. **Documentation**: Update relevant documentation when making changes

## Troubleshooting

### Common Issues After Updates

1. **Unexpected AI Behavior**: If the AI responses seem different, check if you're using cached system messages
2. **Validation Errors**: New validation rules may flag existing custom templates
3. **Style Mismatches**: Ensure response styles align with your brand guidelines

### Debug Commands

```python
# Check current template content
template = prompt_service.get_template("system_ecommerce")
print(f"Template: {template.template}")
print(f"Professional Role: {template.professional_role}")
print(f"Customer Focus: {template.customer_focus}")
print(f"Response Style: {template.response_style}")

# Validate template
errors = template.validate()
print(f"Validation: {errors or 'Valid'}")
```

## Feedback and Support

If you encounter issues with the updated templates or have suggestions for improvements:

1. Check the validation output for specific error messages
2. Review the template content to ensure it matches your expectations
3. Test with sample queries to verify the AI behavior
4. Update custom templates to align with the new customer-focused approach

## Documentation and Resources

### Comprehensive Documentation Suite

The customer-focused prompt transformation includes extensive documentation:

#### Core Documentation
- **[Customer-Focused Transformation Guide](customer-focused-transformation-guide.md)** - Complete overview of the business-to-customer transformation
- **[Professional Response Examples](professional-response-examples.md)** - Detailed examples of professional responses for each industry
- **[Professional Role Consistency Guidelines](professional-role-consistency-guidelines.md)** - Guidelines for maintaining authentic professional roles

#### Implementation Resources
- **Template Validation**: Built-in validation for customer-focused language
- **Response Format Guidelines**: Industry-specific formatting standards
- **Quality Assurance Checklists**: Systematic approach to maintaining response quality
- **Professional Role Standards**: Clear definitions and boundaries for each industry role

### Key Transformation Benefits

#### For Users
- **Relevant Responses**: Direct help with actual customer needs
- **Professional Experience**: Authentic industry expert interactions
- **Personalized Service**: Recommendations tailored to individual context
- **Natural Conversations**: Responses match customer service expectations

#### For Developers
- **Clear Guidelines**: Well-defined professional roles and response patterns
- **Consistent Quality**: Validation ensures appropriate language and tone
- **Flexible Framework**: Easy extension to new industries or roles
- **Maintainable Code**: Clear separation between business logic and customer service

#### For Businesses
- **Better Engagement**: More relevant, helpful customer responses
- **Brand Alignment**: AI interactions match customer service standards
- **Competitive Advantage**: Superior customer experience through personalized AI
- **Scalable Solution**: Framework supports multiple industries and use cases

### Professional Role Summary

| Industry | Professional Role | Key Focus | Response Style |
|----------|------------------|-----------|----------------|
| **E-commerce** | Personal Shopping Assistant | Product recommendations, shopping guidance | Friendly, enthusiastic |
| **Healthcare** | Medical Practitioner | Health guidance, medical information | Caring, professional |
| **Restaurant** | Concierge Service | Dining recommendations, reservations | Warm, hospitable |
| **Financial** | Personal Financial Advisor | Financial planning, investment advice | Professional, trustworthy |
| **Education** | Academic Advisor | Learning guidance, career advice | Supportive, encouraging |
| **Real Estate** | Professional Agent | Property guidance, market insights | Professional, knowledgeable |

### Implementation Best Practices

#### Template Development
1. **Define Clear Professional Roles**: Each industry needs specific, recognizable professional personas
2. **Focus on Customer Service**: All templates should prioritize customer needs over business operations
3. **Include Response Guidelines**: Provide specific formatting and structure instructions
4. **Validate Customer Language**: Use built-in validation to ensure appropriate customer-focused language

#### Quality Assurance
1. **Regular Role Consistency Audits**: Ensure AI maintains professional personas throughout conversations
2. **Customer Feedback Integration**: Monitor satisfaction and adjust approaches accordingly
3. **Professional Standards Compliance**: Maintain industry-appropriate disclaimers and ethical guidelines
4. **Response Quality Metrics**: Track engagement, helpfulness, and professional authenticity

#### Maintenance and Updates
1. **Industry Standards Monitoring**: Keep current with professional best practices
2. **Template Performance Analysis**: Identify and improve underperforming templates
3. **User Experience Optimization**: Continuously refine based on customer interactions
4. **Documentation Currency**: Maintain up-to-date guidelines and examples

The prompt service continues to evolve to provide better customer experiences while maintaining flexibility for customization and extension. The customer-focused transformation represents a fundamental shift toward more valuable, engaging, and professionally authentic AI interactions across all supported industries.