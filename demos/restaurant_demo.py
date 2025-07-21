"""
Restaurant Reservations Demo Module

Implements the restaurant industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo, Industry

fake = Faker()


class RestaurantDemo(BaseDemo):
    """Restaurant reservations demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        super().__init__("Restaurant Reservations", Industry.RESTAURANT, ai_service, context_service)
    
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
        
        # Query-aware enhancements
        query_lower = query.lower()
        
        # Indian/South Asian cuisine intelligence
        if any(word in query_lower for word in ['chole', 'bhature', 'indian', 'curry', 'biryani', 'tandoor', 'naan', 'samosa', 'dosa', 'masala']):
            base_context.update({
                "location": random.choice([
                    "Jackson Heights, NY", "Devon Avenue, Chicago, IL", "Fremont, CA", 
                    "Artesia, CA", "Hillcroft, Houston, TX", "Oak Tree Road, Edison, NJ"
                ]),
                "cuisine_preferences": ["Indian", "Pakistani", "Bangladeshi"],
                "dietary_restrictions": random.choice([[], ["Vegetarian"], ["Jain vegetarian"], ["No beef"]]),
                "spice_preference": random.choice(["Mild", "Medium", "Hot", "Extra hot"]),
                "budget": "$25-45 per person",
                "past_visits": ["Maharaja Palace", "Delhi Garden", "Spice Route", "Bombay Palace", "Curry House"],
                "preferred_time": random.choice(["Lunch (12-2 PM)", "Early dinner (5-7 PM)"]),
                "party_size": random.randint(2, 5)
            })
        
        # Italian cuisine intelligence
        elif any(word in query_lower for word in ['pizza', 'italian', 'pasta', 'lasagna', 'risotto', 'gelato', 'tiramisu']):
            base_context.update({
                "location": random.choice([
                    "Little Italy, NYC", "North End, Boston, MA", "Federal Hill, Providence, RI",
                    "Little Italy, San Diego, CA", "The Hill, St. Louis, MO"
                ]),
                "cuisine_preferences": ["Italian", "Mediterranean", "European"],
                "dietary_restrictions": random.choice([[], ["Vegetarian"], ["Gluten-free"], ["No seafood"]]),
                "budget": "$35-60 per person",
                "past_visits": ["Tony's Pizzeria", "Mama Rosa's", "Villa Italiana", "Carmine's", "Little Italy Bistro"],
                "wine_preference": random.choice(["Chianti", "Pinot Grigio", "Prosecco", "House wine"]),
                "preferred_time": random.choice(["Early dinner (5-7 PM)", "Late dinner (7-9 PM)"]),
                "party_size": random.randint(2, 4)
            })
        
        # Asian cuisine intelligence
        elif any(word in query_lower for word in ['sushi', 'ramen', 'chinese', 'thai', 'korean', 'pho', 'dim sum', 'pad thai']):
            base_context.update({
                "location": random.choice([
                    "Chinatown, NYC", "Koreatown, Los Angeles, CA", "International District, Seattle, WA",
                    "Chinatown, San Francisco, CA", "Asia Town, Cleveland, OH"
                ]),
                "cuisine_preferences": ["Asian", "Japanese", "Chinese", "Thai", "Korean"],
                "dietary_restrictions": random.choice([[], ["No shellfish"], ["Vegetarian"], ["Gluten-free"]]),
                "budget": "$30-50 per person",
                "past_visits": ["Golden Dragon", "Sakura Sushi", "Pho Saigon", "Seoul Kitchen", "Bangkok Garden"],
                "spice_preference": random.choice(["Mild", "Medium", "Spicy"]),
                "preferred_time": random.choice(["Lunch (12-2 PM)", "Early dinner (5-7 PM)", "Late dinner (7-9 PM)"]),
                "party_size": random.randint(2, 6)
            })
        
        # Mexican/Latin cuisine intelligence
        elif any(word in query_lower for word in ['mexican', 'tacos', 'burrito', 'quesadilla', 'margarita', 'salsa', 'guacamole']):
            base_context.update({
                "location": random.choice([
                    "Mission District, San Francisco, CA", "East LA, Los Angeles, CA", "Pilsen, Chicago, IL",
                    "South Austin, TX", "Westside, San Antonio, TX"
                ]),
                "cuisine_preferences": ["Mexican", "Latin American", "Tex-Mex"],
                "dietary_restrictions": random.choice([[], ["Vegetarian"], ["No cilantro"], ["Mild spice only"]]),
                "budget": "$20-35 per person",
                "past_visits": ["El Mariachi", "Casa Grande", "Taco Libre", "La Cocina", "Azteca Restaurant"],
                "drink_preference": random.choice(["Margaritas", "Mexican beer", "Horchata", "Fresh lime agua fresca"]),
                "preferred_time": random.choice(["Lunch (12-2 PM)", "Early dinner (5-7 PM)", "Late dinner (7-9 PM)"]),
                "party_size": random.randint(2, 5)
            })
        
        # Occasion-based intelligence
        if any(word in query_lower for word in ['anniversary', 'romantic', 'date night']):
            base_context.update({
                "special_occasion": "Anniversary dinner",
                "party_size": 2,
                "budget": "$80-120 per person",
                "atmosphere_preference": "Intimate and romantic",
                "preferred_time": "Late dinner (7-9 PM)"
            })
        elif any(word in query_lower for word in ['birthday', 'celebration', 'party']):
            base_context.update({
                "special_occasion": "Birthday celebration",
                "party_size": random.randint(4, 8),
                "atmosphere_preference": "Lively and fun",
                "cake_dessert": "Birthday dessert preferred"
            })
        elif any(word in query_lower for word in ['business', 'meeting', 'client', 'work']):
            base_context.update({
                "special_occasion": "Business meeting",
                "party_size": random.randint(2, 4),
                "budget": "$50-80 per person",
                "atmosphere_preference": "Quiet and professional",
                "preferred_time": "Lunch (12-2 PM)"
            })
        elif any(word in query_lower for word in ['quick', 'fast', 'lunch', 'grab']):
            base_context.update({
                "dining_style": "Quick casual",
                "budget": "$15-25 per person",
                "preferred_time": "Lunch (12-2 PM)",
                "service_preference": "Fast service"
            })
        
        # Default values for missing keys
        if "special_occasion" not in base_context:
            base_context["special_occasion"] = random.choice([None, "Casual dinner", "Weekend meal"])
        if "party_size" not in base_context:
            base_context["party_size"] = random.randint(2, 4)
        if "budget" not in base_context:
            base_context["budget"] = "$35-55 per person"
        if "preferred_time" not in base_context:
            base_context["preferred_time"] = random.choice(["Lunch (12-2 PM)", "Early dinner (5-7 PM)", "Late dinner (7-9 PM)"])
        
        return base_context
    
    def get_sample_queries(self) -> List[str]:
        """Get sample restaurant queries."""
        return [
            "Book a table for two tonight",
            "Find a romantic dinner spot",
            "I need lunch recommendations",
            "Looking for vegetarian restaurants",
            "Best Italian places nearby"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for restaurant queries."""
        return "e.g., Book a table for two, Find a romantic dinner spot, I need lunch recommendations"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic restaurant responses."""
        return "You are a helpful restaurant assistant. Provide general restaurant recommendations without using specific personal context."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual restaurant responses."""
        return """You are a personalized restaurant assistant. Use the provided context to give specific, actionable recommendations. Include:
- Specific restaurant suggestions that match their preferences
- Consider dietary restrictions and budget
- Reference their location and past visits
- Provide actionable next steps
Be helpful, specific, and personalized."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for restaurant queries."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['book', 'table', 'reservation']):
            return """🍽️ **I'd be delighted to help you with reservations:**

**Excellent dining options I recommend:**
- **Bella Vista** - Upscale Italian with city views, perfect for special occasions
- **The Garden Bistro** - Farm-to-table American cuisine, cozy atmosphere  
- **Sakura Sushi** - Fresh sushi and Japanese specialties, modern setting
- **Coastal Catch** - Seafood restaurant with daily fresh selections
- **Rustic Table** - Comfort food with a gourmet twist, family-friendly

**What I need to secure your reservation:**
- **Party size** and **preferred date/time**
- **Cuisine preference** or **occasion type**
- **Any dietary restrictions** I should mention
- **Special requests** (window table, quiet section, celebration)

**I can also help with:**
- Checking availability across multiple restaurants
- Suggesting alternatives if your first choice is booked
- Making special arrangements for celebrations

**What type of dining experience are you looking for?** I'll find the perfect spot and handle all the details! 🎯"""
        
        elif any(word in query_lower for word in ['romantic', 'date', 'special']):
            return """💕 **Perfect romantic dining recommendations:**

**Intimate restaurants I highly recommend:**
- **Moonlight Terrace** - Rooftop dining with stunning sunset views, live piano
- **Le Petit Jardin** - French bistro with candlelit tables and garden seating
- **Waterfront Grill** - Lakeside dining with private booths and soft lighting
- **The Wine Cellar** - Cozy underground restaurant with extensive wine selection
- **Starlight Steakhouse** - Classic elegance with tableside service

**What makes these special:**
- **Ambiance** - Dim lighting, quiet atmosphere, beautiful settings
- **Service** - Attentive but discreet, perfect for conversation
- **Menu** - Shareable appetizers, premium entrees, decadent desserts
- **Extras** - Wine pairings, special occasion amenities

**For your romantic evening, I can arrange:**
- **Prime seating** - Window tables, private corners, patio spots
- **Special touches** - Flowers, champagne, dessert with candles
- **Timing coordination** - Perfect reservation times for sunset/ambiance

**Tell me about your special occasion** - anniversary, proposal, first date? I'll ensure everything is absolutely perfect! ✨"""
        
        elif any(word in query_lower for word in ['lunch', 'quick', 'fast']):
            return """⚡ **Quick lunch spots I recommend:**

**Fast & delicious options:**
- **Fresh Bowl Co.** - Build-your-own salads and grain bowls, 5-minute service
- **Artisan Sandwich Shop** - Gourmet sandwiches made to order, 10-minute pickup
- **Noodle Express** - Asian noodle bowls and stir-fries, quick counter service
- **Mediterranean Wrap** - Fresh wraps, hummus bowls, healthy and fast
- **Soup & Salad Station** - Daily soups, fresh salads, grab-and-go options

**Perfect for busy schedules:**
- **Order ahead** - Most offer mobile ordering for pickup
- **Healthy options** - Fresh ingredients, customizable meals
- **Quick service** - 5-15 minute wait times
- **Convenient locations** - Near business districts and offices

**What I can help with:**
- **Pre-ordering** your meal for pickup time
- **Dietary accommodations** - vegetarian, gluten-free, etc.
- **Group orders** - coordinating lunch for your team
- **Location recommendations** - closest to your office/meeting

**What type of cuisine sounds good?** I'll find the perfect quick lunch spot and can even place your order ahead of time! 🥗"""
        
        else:
            return """🍴 **Welcome! I'm your personal dining concierge:**

**How I can enhance your dining experience:**
- **Restaurant recommendations** - Based on your taste, budget, occasion
- **Reservation management** - Securing tables at the best spots
- **Special arrangements** - Celebrations, dietary needs, group dining
- **Local expertise** - Hidden gems, new openings, seasonal favorites
- **Event coordination** - Business dinners, family gatherings, date nights

**Popular dining categories:**
- **Fine dining** - Special occasions, business entertainment
- **Casual favorites** - Family meals, weekend dining
- **Quick bites** - Lunch meetings, grab-and-go options
- **International cuisine** - Italian, Asian, Mexican, Mediterranean
- **Local specialties** - Regional favorites and chef-driven restaurants

**Special services I provide:**
- **Waitlist management** - Getting you into fully booked restaurants
- **Menu previews** - Helping you choose before you arrive
- **Dietary coordination** - Ensuring restaurants can accommodate your needs
- **Transportation tips** - Parking, valet, public transit options

**What brings you here today?** A special celebration, business meal, or just looking for something delicious? Tell me what you're craving and I'll make it happen! 🌟"""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for restaurant queries."""
        query_lower = query.lower()
        location = context['location']
        dietary = context['dietary_restrictions']
        cuisines = context['cuisine_preferences']
        budget = context['budget']
        
        if any(word in query_lower for word in ['book', 'table', 'reservation']):
            return f"""🎯 **Perfect Matches in {location}:**

🌟 **Top Recommendation:**
- **Verde Italiano** - Vegetarian Italian, $65/person, 0.3 miles
  - ✅ Accommodates {', '.join(dietary)} dietary needs
  - ✅ Matches your {cuisines[0]} preference
  - ✅ Within your {budget} budget
  - ✅ Available tonight 7-9 PM

🥗 **Alternative:**
- **Mediterranean Breeze** - Gluten-free options, $55/person, 0.5 miles

⚠️ **Avoid:** Chez Laurent (you visited recently)

Shall I book Verde Italiano for tonight?"""
        
        elif any(word in query_lower for word in ['romantic', 'date', 'special']):
            return f"""💕 **Romantic Options in {location}:**

🌹 **Perfect for Date Night:**
- **Bella Vista** - {cuisines[0]} with city views, $70/person
  - ✅ Intimate atmosphere, accommodates {dietary[0]}
  - ✅ Within {budget} range
  - ✅ Highly rated for special occasions

🕯️ **Cozy Alternative:**
- **Garden Terrace** - {cuisines[1]} with outdoor seating, $60/person

Both have availability this weekend and match your preferences!"""
        
        elif any(word in query_lower for word in ['lunch', 'quick', 'fast']):
            return f"""🚀 **Quick Lunch Near {location}:**

⚡ **Fast & Fits Your Needs:**
- **Green Bowl** - Vegetarian bowls, $15, 2 blocks away
  - ✅ Accommodates {dietary[0]} diet
  - ✅ Quick service (5-10 min)
  - ✅ Well under your {budget} budget

🥙 **Alternative:**
- **Med Express** - {cuisines[1]} wraps, $12, 3 blocks

Both are perfect for your dietary restrictions and time constraints!"""
        
        else:
            return f"""🎯 **Personalized Recommendations for {location}:**

Based on your profile:
- **Dietary needs:** {', '.join(dietary)}
- **Favorite cuisines:** {', '.join(cuisines)}
- **Budget:** {budget}

🌟 **Top Matches:**
- **Verde Italiano** - Vegetarian {cuisines[0]}, perfect fit
- **Spice Garden** - {cuisines[2]} with gluten-free options
- **Mediterranean Breeze** - Healthy {cuisines[1]} cuisine

All within your budget and dietary preferences!"""