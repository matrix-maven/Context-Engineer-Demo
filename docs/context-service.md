# Context Service Documentation

The Context Service is a comprehensive system for generating realistic, industry-specific context data using the Faker library. It provides the foundation for creating personalized AI responses across different industries.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [Supported Industries](#supported-industries)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Extending the Service](#extending-the-service)
- [API Reference](#api-reference)

## Overview

The Context Service addresses the need for realistic, varied context data in AI applications. Instead of using static or hardcoded data, it generates dynamic, industry-specific contexts that make AI responses more personalized and relevant.

### Key Benefits

- **Realistic Data**: Uses Faker library for authentic-looking generated data
- **Industry-Specific**: Tailored context generation for different business domains
- **Caching**: Intelligent caching with TTL for performance optimization
- **Validation**: Comprehensive validation and quality scoring
- **Reproducible**: Optional seeding for consistent test data
- **Extensible**: Easy to add new industries and context types

## Architecture

The Context Service follows a factory pattern with the following components:

```
ContextService
├── BaseContextFactory (Abstract)
│   ├── RestaurantContextFactory
│   ├── HealthcareContextFactory
│   ├── EcommerceContextFactory
│   ├── FinancialContextFactory
│   ├── EducationContextFactory
│   └── RealEstateContextFactory
├── IndustryContext (Data Model)
├── ContextValidationError (Exception)
└── Industry (Enum)
```

## Core Components

### ContextService

The main service class that orchestrates context generation:

```python
class ContextService:
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None)
    def generate_context(self, industry: Industry, force_refresh: bool = False) -> IndustryContext
    def refresh_context(self, industry: Industry) -> IndustryContext
    def validate_context(self, context: IndustryContext) -> List[str]
    def get_context_quality_score(self, context: IndustryContext) -> float
    def clear_cache(self, industry: Optional[Industry] = None) -> None
```

### IndustryContext

Standardized data model for all industry contexts:

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

### BaseContextFactory

Abstract base class for industry-specific factories:

```python
class BaseContextFactory(ABC):
    @abstractmethod
    def generate_user_profile(self) -> Dict[str, Any]
    @abstractmethod
    def generate_situational_data(self) -> Dict[str, Any]
    @abstractmethod
    def generate_preferences(self) -> Dict[str, Any]
    @abstractmethod
    def generate_history(self) -> Dict[str, Any]
    def generate_constraints(self) -> Dict[str, Any]  # Optional override
```

## Supported Industries

### RESTAURANT
- **User Profile**: Name, age, location, dietary restrictions
- **Situational Data**: Party size, occasion, time preference, budget
- **Preferences**: Cuisine types, ambiance, service style
- **History**: Past restaurant visits, favorite dishes, reviews
- **Constraints**: Budget limits, accessibility needs, time constraints

### HEALTHCARE
- **User Profile**: Patient demographics, insurance, emergency contacts
- **Situational Data**: Current symptoms, vital signs, appointment type
- **Preferences**: Communication style, treatment preferences, provider preferences
- **History**: Medical history, medications, allergies, past visits
- **Constraints**: Insurance coverage, mobility limitations, time availability

### ECOMMERCE
- **User Profile**: Customer demographics, account info, loyalty status
- **Situational Data**: Current shopping session, cart contents, browsing behavior
- **Preferences**: Product categories, brands, price ranges, delivery options
- **History**: Purchase history, returns, reviews, wishlist items
- **Constraints**: Budget limits, delivery restrictions, payment methods

### FINANCIAL
- **User Profile**: Client demographics, employment, financial goals
- **Situational Data**: Current financial situation, recent transactions, market conditions
- **Preferences**: Risk tolerance, investment types, communication preferences
- **History**: Investment history, loan history, financial milestones
- **Constraints**: Budget limitations, regulatory restrictions, time horizons

### EDUCATION
- **User Profile**: Student demographics, academic level, learning style
- **Situational Data**: Current courses, assignments, academic performance
- **Preferences**: Subject interests, learning methods, study preferences
- **History**: Academic history, completed courses, achievements
- **Constraints**: Time availability, resource limitations, accessibility needs

### REAL_ESTATE
- **User Profile**: Buyer/seller demographics, family situation, employment
- **Situational Data**: Current housing situation, timeline, market conditions
- **Preferences**: Property types, locations, features, price ranges
- **History**: Previous transactions, property searches, agent interactions
- **Constraints**: Budget limits, financing pre-approval, location restrictions

## Usage Guide

### Basic Usage

```python
from services.context_service import ContextService, Industry

# Initialize service
service = ContextService()

# Generate context for restaurant industry
context = service.generate_context(Industry.RESTAURANT)

# Access context data
print(f"User: {context.user_profile['name']}")
print(f"Party Size: {context.situational_data['party_size']}")
print(f"Cuisine Preferences: {context.preferences['cuisines']}")
```

### Advanced Usage

```python
# Initialize with custom locale and seed
service = ContextService(locale='en_GB', seed=12345)

# Generate multiple contexts
contexts = {}
for industry in [Industry.HEALTHCARE, Industry.FINANCIAL, Industry.ECOMMERCE]:
    contexts[industry] = service.generate_context(industry)

# Validate and score contexts
for industry, context in contexts.items():
    errors = service.validate_context(context)
    quality = service.get_context_quality_score(context)
    print(f"{industry.value}: Quality {quality:.2f}, Errors: {len(errors)}")
```

### Caching and Performance

```python
# Check cache status
cache_status = service.get_cache_status()
print(f"Cached industries: {cache_status['cached_industries']}")

# Force refresh specific context
fresh_context = service.refresh_context(Industry.RESTAURANT)

# Clear cache for performance testing
service.clear_cache()  # Clear all
service.clear_cache(Industry.HEALTHCARE)  # Clear specific
```

### Integration with AI Providers

```python
from services.ai_service import PromptRequest

# Generate context
context = service.generate_context(Industry.HEALTHCARE)

# Create AI request with context
request = PromptRequest(
    prompt="What should I know about my current medications?",
    context=context.to_dict(),
    system_message="You are a helpful healthcare assistant."
)

# Use with any AI provider
response = ai_provider.generate_response(request)
```

## Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CONTEXT_REFRESH_INTERVAL` | Cache TTL in seconds | `300` | `600` |
| `MAX_CONTEXT_SIZE` | Maximum context data size | `10000` | `15000` |

### Service Configuration

```python
# Basic configuration
service = ContextService()

# Custom locale
service = ContextService(locale='fr_FR')  # French locale

# Reproducible generation
service = ContextService(seed=42)

# Combined configuration
service = ContextService(locale='en_GB', seed=12345)
```

### Faker Locales

Supported locales for region-specific data:

- `en_US` - United States English (default)
- `en_GB` - British English
- `fr_FR` - French (France)
- `de_DE` - German (Germany)
- `es_ES` - Spanish (Spain)
- `it_IT` - Italian (Italy)
- `ja_JP` - Japanese (Japan)
- `zh_CN` - Chinese (China)

## Error Handling

### ContextValidationError

The service raises `ContextValidationError` for validation failures:

```python
from services.context_service import ContextValidationError

try:
    context = service.generate_context(Industry.RESTAURANT)
except ContextValidationError as e:
    print(f"Validation failed: {e}")
    print(f"Industry: {e.industry}")
    print(f"Errors: {e.validation_errors}")
```

### Common Error Scenarios

1. **Missing Factory**: No factory registered for industry
2. **Validation Failure**: Generated context fails validation
3. **Data Quality**: Context doesn't meet quality thresholds
4. **Cache Issues**: Cache corruption or expiration problems

### Error Recovery

```python
def safe_generate_context(service, industry):
    """Generate context with error recovery."""
    try:
        return service.generate_context(industry)
    except ContextValidationError as e:
        # Log error and try force refresh
        logger.warning(f"Context generation failed: {e}")
        try:
            return service.generate_context(industry, force_refresh=True)
        except ContextValidationError:
            # Return minimal context as fallback
            return create_minimal_context(industry)
```

## Extending the Service

### Adding New Industries

1. **Define Industry Enum**:
```python
class Industry(str, Enum):
    # ... existing industries
    AUTOMOTIVE = "automotive"
```

2. **Create Factory Class**:
```python
class AutomotiveContextFactory(BaseContextFactory):
    def _get_industry(self) -> Industry:
        return Industry.AUTOMOTIVE
    
    def generate_user_profile(self) -> Dict[str, Any]:
        return {
            "name": self.faker.name(),
            "age": self.faker.random_int(min=18, max=75),
            "license_type": self.faker.random_element(["Standard", "Commercial", "Motorcycle"])
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        return {
            "vehicle_type": self.faker.random_element(["Sedan", "SUV", "Truck", "Motorcycle"]),
            "service_type": self.faker.random_element(["Maintenance", "Repair", "Purchase"]),
            "urgency": self.faker.random_element(["Low", "Medium", "High"])
        }
    
    # ... implement other required methods
```

3. **Register Factory**:
```python
service.register_factory(AutomotiveContextFactory)
```

### Custom Context Fields

Add industry-specific fields by overriding factory methods:

```python
class CustomRestaurantFactory(BaseContextFactory):
    def generate_preferences(self) -> Dict[str, Any]:
        base_prefs = super().generate_preferences()
        base_prefs.update({
            "wine_pairing": self.faker.boolean(),
            "chef_recommendations": self.faker.boolean(),
            "private_dining": self.faker.boolean()
        })
        return base_prefs
```

### Custom Validation

Add industry-specific validation rules:

```python
class HealthcareContextFactory(BaseContextFactory):
    def _validate_industry_specific(self, context: IndustryContext) -> List[str]:
        errors = []
        
        # Validate age is reasonable for medical context
        age = context.user_profile.get('age', 0)
        if age < 0 or age > 120:
            errors.append("Invalid age for healthcare context")
        
        # Validate required medical fields
        if not context.history.get('medical_conditions'):
            errors.append("Medical history is required")
        
        return errors
```

## API Reference

### ContextService Methods

#### `__init__(locale: str = 'en_US', seed: Optional[int] = None)`
Initialize the context service with optional locale and seed.

#### `generate_context(industry: Industry, force_refresh: bool = False) -> IndustryContext`
Generate context for specified industry. Uses cache unless force_refresh is True.

#### `refresh_context(industry: Industry) -> IndustryContext`
Force generation of fresh context, bypassing cache.

#### `refresh_all_contexts() -> Dict[Industry, IndustryContext]`
Refresh contexts for all registered industries.

#### `validate_context(context: IndustryContext) -> List[str]`
Validate context and return list of error messages.

#### `get_context_quality_score(context: IndustryContext) -> float`
Calculate quality score (0.0-1.0) based on completeness and richness.

#### `clear_cache(industry: Optional[Industry] = None) -> None`
Clear cache for specific industry or all industries.

#### `get_cache_status() -> Dict[str, Any]`
Get current cache status for debugging.

#### `set_faker_seed(seed: int) -> None`
Set Faker seed for reproducible generation.

### IndustryContext Methods

#### `to_dict() -> Dict[str, Any]`
Convert context to dictionary for serialization.

#### `is_valid() -> bool`
Check if context has required fields.

#### `get_context_summary() -> str`
Get human-readable summary of context.

### BaseContextFactory Methods

#### `generate_context() -> IndustryContext`
Generate complete industry context (calls all generate_* methods).

#### `validate_context(context: IndustryContext) -> List[str]`
Validate generated context and return error list.

## Performance Considerations

### Caching Strategy

- **TTL-based**: Contexts expire after configured interval
- **Industry-specific**: Each industry has separate cache
- **Memory efficient**: Automatic cleanup of expired entries

### Generation Performance

- **Lazy loading**: Factories created on-demand
- **Batch generation**: Support for generating multiple contexts
- **Seed optimization**: Reproducible generation for testing

### Memory Usage

- **Configurable limits**: MAX_CONTEXT_SIZE setting
- **Automatic cleanup**: Expired cache entries removed
- **Efficient serialization**: Optimized to_dict() methods

## Testing

### Unit Testing

```python
import pytest
from services.context_service import ContextService, Industry

def test_context_generation():
    service = ContextService(seed=42)  # Reproducible
    context = service.generate_context(Industry.RESTAURANT)
    
    assert context.industry == Industry.RESTAURANT
    assert context.user_profile['name']
    assert context.is_valid()

def test_context_validation():
    service = ContextService()
    context = service.generate_context(Industry.HEALTHCARE)
    errors = service.validate_context(context)
    
    assert len(errors) == 0  # Should be valid
```

### Integration Testing

```python
def test_ai_integration():
    service = ContextService()
    context = service.generate_context(Industry.FINANCIAL)
    
    # Test with AI provider
    request = PromptRequest(
        prompt="Help me with investment advice",
        context=context.to_dict()
    )
    
    response = ai_provider.generate_response(request)
    assert response.success
```

## Troubleshooting

### Common Issues

1. **Factory Not Found**: Ensure factory is registered for industry
2. **Validation Errors**: Check factory implementation for required fields
3. **Cache Issues**: Clear cache and regenerate contexts
4. **Memory Usage**: Reduce MAX_CONTEXT_SIZE or clear cache more frequently

### Debug Information

```python
# Get service status
print(service)  # Basic info
print(repr(service))  # Detailed info

# Check cache status
cache_status = service.get_cache_status()
print(f"Cache: {cache_status}")

# Validate specific context
context = service.generate_context(Industry.RESTAURANT)
errors = service.validate_context(context)
quality = service.get_context_quality_score(context)
print(f"Quality: {quality}, Errors: {errors}")
```

### Logging

Enable debug logging to see detailed context generation:

```python
import logging
logging.getLogger('ContextService').setLevel(logging.DEBUG)
logging.getLogger('BaseContextFactory').setLevel(logging.DEBUG)
```

## Best Practices

1. **Use Caching**: Don't disable caching in production
2. **Set Appropriate TTL**: Balance freshness vs performance
3. **Validate Contexts**: Always validate generated contexts
4. **Handle Errors**: Implement proper error handling and fallbacks
5. **Monitor Quality**: Track context quality scores over time
6. **Use Seeds for Testing**: Ensure reproducible test data
7. **Clear Cache Periodically**: Prevent memory buildup
8. **Customize Factories**: Extend factories for specific needs

## Future Enhancements

- **Streaming Generation**: Support for real-time context updates
- **Machine Learning**: ML-based context quality improvement
- **External Data**: Integration with external data sources
- **Context Relationships**: Support for related contexts across industries
- **Performance Metrics**: Detailed performance monitoring and optimization