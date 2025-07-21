# Restaurant Demo: Smart Context Generation

## Overview

The Restaurant Demo has been enhanced with **Smart Context Generation** - an intelligent system that analyzes user queries and generates contextually relevant, culturally-aware restaurant context data. This feature significantly improves the quality and relevance of AI responses by providing more targeted context based on the user's specific request.

## Key Features

### 🧠 Query Intelligence

The system analyzes user queries to detect:
- **Cuisine Types**: Indian, Italian, Asian, Mexican, and more
- **Special Occasions**: Anniversary, birthday, business meetings
- **Dining Preferences**: Quick lunch, romantic dinner, casual meal
- **Cultural Context**: Authentic restaurant names and locations

### 🌍 Cultural Awareness

When cuisine-specific terms are detected, the system generates:
- **Authentic Restaurant Names**: "Maharaja Palace", "Tony's Pizzeria", "Golden Dragon"
- **Appropriate Locations**: Jackson Heights for Indian, Little Italy for Italian
- **Cultural Preferences**: Spice levels, wine pairings, dietary restrictions
- **Realistic Past Visits**: Industry-appropriate restaurant history

### 🎉 Occasion Detection

The system recognizes special occasions and adjusts:
- **Party Size**: 2 for romantic dinners, 4-8 for birthday parties
- **Budget Range**: Higher for anniversaries, moderate for business meetings
- **Atmosphere Preferences**: Intimate, lively, professional, or casual
- **Timing**: Lunch for business, late dinner for romance

## Implementation Details

### Core Method: `generate_smart_context()`

```python
def generate_smart_context(self, query: str) -> Dict[str, Any]:
    """Generate context that intelligently enhances the user's query."""
    
    # Base realistic customer profile
    base_context = {
        "customer_profile": {
            "name": fake.name(),
            "member_since": fake.date_between(start_date='-2y', end_date='-3m').strftime('%Y-%m-%d'),
            "loyalty_tier": random.choice(["Silver", "Gold", "Platinum"]),
            "total_visits": random.randint(8, 25)
        }
    }
    
    # Query-aware enhancements based on detected patterns
    query_lower = query.lower()
    
    # Cuisine-specific intelligence
    # Occasion-based intelligence
    # Default fallback values
    
    return base_context
```

### Cuisine Intelligence Patterns

#### Indian/South Asian Cuisine
**Trigger Words**: `chole`, `bhature`, `indian`, `curry`, `biryani`, `tandoor`, `naan`, `samosa`, `dosa`, `masala`

**Generated Context**:
```python
{
    "location": "Jackson Heights, NY",  # Authentic Indian neighborhoods
    "cuisine_preferences": ["Indian", "Pakistani", "Bangladeshi"],
    "dietary_restrictions": ["Vegetarian", "Jain vegetarian", "No beef"],
    "spice_preference": "Medium",
    "budget": "$25-45 per person",
    "past_visits": ["Maharaja Palace", "Delhi Garden", "Spice Route"],
    "preferred_time": "Early dinner (5-7 PM)",
    "party_size": 3
}
```

#### Italian Cuisine
**Trigger Words**: `pizza`, `italian`, `pasta`, `lasagna`, `risotto`, `gelato`, `tiramisu`

**Generated Context**:
```python
{
    "location": "Little Italy, NYC",
    "cuisine_preferences": ["Italian", "Mediterranean", "European"],
    "dietary_restrictions": ["Vegetarian", "Gluten-free"],
    "budget": "$35-60 per person",
    "past_visits": ["Tony's Pizzeria", "Mama Rosa's", "Villa Italiana"],
    "wine_preference": "Chianti",
    "preferred_time": "Late dinner (7-9 PM)",
    "party_size": 2
}
```

#### Asian Cuisine
**Trigger Words**: `sushi`, `ramen`, `chinese`, `thai`, `korean`, `pho`, `dim sum`, `pad thai`

**Generated Context**:
```python
{
    "location": "Chinatown, NYC",
    "cuisine_preferences": ["Asian", "Japanese", "Chinese", "Thai", "Korean"],
    "dietary_restrictions": ["No shellfish", "Vegetarian"],
    "budget": "$30-50 per person",
    "past_visits": ["Golden Dragon", "Sakura Sushi", "Pho Saigon"],
    "spice_preference": "Medium",
    "party_size": 4
}
```

#### Mexican/Latin Cuisine
**Trigger Words**: `mexican`, `tacos`, `burrito`, `quesadilla`, `margarita`, `salsa`, `guacamole`

**Generated Context**:
```python
{
    "location": "Mission District, San Francisco, CA",
    "cuisine_preferences": ["Mexican", "Latin American", "Tex-Mex"],
    "dietary_restrictions": ["Vegetarian", "No cilantro"],
    "budget": "$20-35 per person",
    "past_visits": ["El Mariachi", "Casa Grande", "Taco Libre"],
    "drink_preference": "Margaritas",
    "party_size": 3
}
```

### Occasion Intelligence Patterns

#### Anniversary/Romantic Dinner
**Trigger Words**: `anniversary`, `romantic`, `date night`

**Generated Context**:
```python
{
    "special_occasion": "Anniversary dinner",
    "party_size": 2,
    "budget": "$80-120 per person",
    "atmosphere_preference": "Intimate and romantic",
    "preferred_time": "Late dinner (7-9 PM)"
}
```

#### Birthday Celebration
**Trigger Words**: `birthday`, `celebration`, `party`

**Generated Context**:
```python
{
    "special_occasion": "Birthday celebration",
    "party_size": 6,  # Larger group
    "atmosphere_preference": "Lively and fun",
    "cake_dessert": "Birthday dessert preferred"
}
```

#### Business Meeting
**Trigger Words**: `business`, `meeting`, `client`, `work`

**Generated Context**:
```python
{
    "special_occasion": "Business meeting",
    "party_size": 3,
    "budget": "$50-80 per person",
    "atmosphere_preference": "Quiet and professional",
    "preferred_time": "Lunch (12-2 PM)"
}
```

#### Quick/Casual Dining
**Trigger Words**: `quick`, `fast`, `lunch`, `grab`

**Generated Context**:
```python
{
    "dining_style": "Quick casual",
    "budget": "$15-25 per person",
    "preferred_time": "Lunch (12-2 PM)",
    "service_preference": "Fast service"
}
```

## Benefits

### 🎯 Enhanced AI Responses

The smart context generation enables AI to provide:
- **Culturally Appropriate Recommendations**: Authentic cuisine suggestions
- **Occasion-Specific Advice**: Tailored to the dining context
- **Realistic Personalization**: Based on believable customer profiles
- **Relevant Details**: Spice preferences, wine pairings, dietary considerations

### 🔄 Dynamic Adaptation

The system adapts to various query types:
- **Cuisine Queries**: "Find me good Indian food" → Indian neighborhood context
- **Occasion Queries**: "Anniversary dinner" → Romantic dining context
- **Style Queries**: "Quick lunch" → Fast-casual context
- **Mixed Queries**: "Italian anniversary dinner" → Combined context

### 📈 Improved User Experience

Users receive more relevant and helpful responses because:
- Context matches their specific request
- Recommendations feel more personalized
- Cultural nuances are respected
- Occasion requirements are understood

## Usage Examples

### Example 1: Indian Cuisine Query
**User Query**: "I'm craving some good chole bhature"

**Generated Context**:
```python
{
    "customer_profile": {
        "name": "Priya Sharma",
        "member_since": "2022-08-15",
        "loyalty_tier": "Gold",
        "total_visits": 15
    },
    "location": "Jackson Heights, NY",
    "cuisine_preferences": ["Indian", "Pakistani", "Bangladeshi"],
    "dietary_restrictions": ["Vegetarian"],
    "spice_preference": "Hot",
    "budget": "$25-45 per person",
    "past_visits": ["Maharaja Palace", "Delhi Garden", "Spice Route"],
    "preferred_time": "Early dinner (5-7 PM)",
    "party_size": 3
}
```

**AI Response Enhancement**: The AI can now recommend authentic Indian restaurants in Jackson Heights, discuss spice levels, suggest vegetarian options, and reference the customer's loyalty status and past visits to similar establishments.

### Example 2: Anniversary Dinner Query
**User Query**: "Looking for a romantic Italian restaurant for our anniversary"

**Generated Context**:
```python
{
    "customer_profile": {
        "name": "Michael Johnson",
        "member_since": "2021-03-10",
        "loyalty_tier": "Platinum",
        "total_visits": 22
    },
    "location": "Little Italy, NYC",
    "cuisine_preferences": ["Italian", "Mediterranean", "European"],
    "special_occasion": "Anniversary dinner",
    "party_size": 2,
    "budget": "$80-120 per person",
    "atmosphere_preference": "Intimate and romantic",
    "preferred_time": "Late dinner (7-9 PM)",
    "wine_preference": "Chianti",
    "past_visits": ["Tony's Pizzeria", "Mama Rosa's", "Villa Italiana"]
}
```

**AI Response Enhancement**: The AI can recommend upscale Italian restaurants with romantic ambiance, suggest wine pairings, mention anniversary specials, and provide reservation timing advice for intimate dining.

## Technical Implementation

### Integration with BaseDemo

The smart context generation integrates seamlessly with the existing demo framework:

```python
class RestaurantDemo(BaseDemo):
    def generate_context(self, query: str = None) -> Dict[str, Any]:
        """Generate restaurant context, with smart context if query provided."""
        if query:
            return self.generate_smart_context(query)
        else:
            return self.generate_basic_context()
```

### Fallback Mechanism

The system includes robust fallback handling:

```python
# Default values for missing keys
if "special_occasion" not in base_context:
    base_context["special_occasion"] = random.choice([None, "Casual dinner", "Weekend meal"])
if "party_size" not in base_context:
    base_context["party_size"] = random.randint(2, 4)
if "budget" not in base_context:
    base_context["budget"] = "$35-55 per person"
```

### Pattern Matching

The system uses flexible pattern matching:

```python
# Cuisine detection
if any(word in query_lower for word in ['chole', 'bhature', 'indian', 'curry']):
    # Generate Indian context
    
# Occasion detection  
if any(word in query_lower for word in ['anniversary', 'romantic', 'date night']):
    # Generate romantic context
```

## Future Enhancements

### Planned Features

1. **Dietary Restriction Intelligence**: Detect gluten-free, vegan, keto mentions
2. **Price Range Detection**: Parse budget mentions ("under $50", "expensive")
3. **Location Intelligence**: Detect neighborhood or city mentions
4. **Time Intelligence**: Parse specific time preferences ("early dinner", "late lunch")
5. **Group Size Detection**: Parse party size mentions ("table for 4", "large group")

### Advanced Context Combinations

Future versions will support more complex context combinations:
- "Vegetarian Indian restaurant for business lunch under $30"
- "Gluten-free Italian anniversary dinner in Little Italy"
- "Quick Thai lunch for 6 people near downtown"

## Testing and Validation

### Test Cases

The smart context generation includes comprehensive test coverage:

```python
def test_indian_cuisine_detection():
    demo = RestaurantDemo()
    context = demo.generate_smart_context("I want some good biryani")
    assert "Indian" in context["cuisine_preferences"]
    assert "Jackson Heights" in context["location"] or "Devon Avenue" in context["location"]

def test_anniversary_occasion_detection():
    demo = RestaurantDemo()
    context = demo.generate_smart_context("romantic anniversary dinner")
    assert context["special_occasion"] == "Anniversary dinner"
    assert context["party_size"] == 2
    assert context["atmosphere_preference"] == "Intimate and romantic"
```

### Quality Assurance

- **Pattern Coverage**: All major cuisine and occasion patterns tested
- **Fallback Testing**: Ensures graceful handling of unrecognized queries
- **Context Validation**: Verifies generated context is realistic and consistent
- **Integration Testing**: Confirms compatibility with existing demo framework

## Conclusion

The Smart Context Generation feature represents a significant advancement in the Restaurant Demo's ability to provide relevant, culturally-aware, and occasion-appropriate dining recommendations. By intelligently analyzing user queries and generating targeted context, the system enables AI responses that feel more personalized, authentic, and helpful to users seeking dining recommendations.

This enhancement demonstrates the power of context-aware AI systems and provides a foundation for similar intelligent context generation in other industry demos.