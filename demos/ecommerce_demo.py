"""
E-commerce Demo Module

Implements the e-commerce industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo

fake = Faker()


class EcommerceDemo(BaseDemo):
    """E-commerce shopping assistant demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        from services.prompt_service import Industry
        super().__init__("E-commerce", Industry.ECOMMERCE, ai_service, context_service)
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic e-commerce context using Faker."""
        return {
            "customer_profile": {
                "name": fake.name(),
                "email": fake.email(),
                "member_since": fake.date_between(start_date='-3y', end_date='-1m').strftime('%Y-%m-%d'),
                "loyalty_tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
                "location": f"{fake.city()}, {fake.state()}"
            },
            "shopping_behavior": {
                "preferred_categories": random.sample([
                    "Electronics", "Clothing", "Home & Garden", "Sports", 
                    "Books", "Beauty", "Automotive", "Toys"
                ], 3),
                "price_sensitivity": random.choice(["Budget-conscious", "Value-seeker", "Premium buyer"]),
                "shopping_frequency": random.choice(["Weekly", "Bi-weekly", "Monthly", "Occasional"]),
                "device_preference": random.choice(["Mobile", "Desktop", "Tablet"])
            },
            "current_session": {
                "cart_items": random.randint(0, 5),
                "cart_value": random.randint(0, 300),
                "browsing_time": f"{random.randint(5, 45)} minutes",
                "pages_viewed": random.randint(3, 15),
                "search_history": random.sample([
                    "wireless headphones", "running shoes", "coffee maker",
                    "laptop stand", "winter jacket", "smartphone case"
                ], 2)
            },
            "purchase_history": {
                "total_orders": random.randint(5, 50),
                "average_order_value": random.randint(50, 200),
                "last_purchase": fake.date_between(start_date='-2m', end_date='-1d').strftime('%Y-%m-%d'),
                "favorite_brands": random.sample([
                    "Apple", "Nike", "Samsung", "Sony", "Adidas", "Amazon Basics"
                ], 2),
                "return_rate": f"{random.randint(5, 15)}%"
            },
            "preferences": {
                "shipping_speed": random.choice(["Standard", "Express", "Same-day"]),
                "payment_method": random.choice(["Credit card", "PayPal", "Apple Pay", "Google Pay"]),
                "communication": random.choice(["Email", "SMS", "Push notifications"]),
                "reviews": random.choice(["Always reads", "Sometimes reads", "Rarely reads"])
            }
        }
    
    def generate_smart_context(self, query: str) -> Dict[str, Any]:
        """Generate context that intelligently enhances the user's query."""
        
        # Base realistic customer profile
        base_context = {
            "customer_profile": {
                "name": fake.name(),
                "email": fake.email(),
                "member_since": fake.date_between(start_date='-2y', end_date='-3m').strftime('%Y-%m-%d'),
                "loyalty_tier": random.choice(["Silver", "Gold", "Platinum"]),
                "location": f"{fake.city()}, {fake.state()}"
            }
        }
        
        # Query-aware enhancements
        query_lower = query.lower()
        
        # Electronics/Tech intelligence
        if any(word in query_lower for word in ['laptop', 'computer', 'macbook', 'pc', 'gaming', 'tech']):
            base_context.update({
                "shopping_behavior": {
                    "preferred_categories": ["Electronics", "Computers", "Gaming"],
                    "price_sensitivity": random.choice(["Value-seeker", "Premium buyer"]),
                    "device_preference": "Desktop",
                    "shopping_frequency": "Occasional"
                },
                "purchase_history": {
                    "total_orders": random.randint(15, 35),
                    "average_order_value": random.randint(300, 800),
                    "last_purchase": fake.date_between(start_date='-6m', end_date='-1m').strftime('%Y-%m-%d'),
                    "favorite_brands": random.sample(["Apple", "Dell", "HP", "ASUS", "Lenovo"], 2),
                    "return_rate": f"{random.randint(3, 8)}%"
                },
                "current_session": {
                    "cart_items": random.randint(0, 2),
                    "cart_value": random.randint(0, 1200),
                    "browsing_time": f"{random.randint(15, 60)} minutes",
                    "search_history": ["gaming laptop", "productivity software", "external monitor"]
                }
            })
        
        # Audio/Headphones intelligence
        elif any(word in query_lower for word in ['headphones', 'earbuds', 'audio', 'speakers', 'music']):
            base_context.update({
                "shopping_behavior": {
                    "preferred_categories": ["Electronics", "Audio", "Music"],
                    "price_sensitivity": random.choice(["Value-seeker", "Premium buyer"]),
                    "device_preference": random.choice(["Mobile", "Desktop"]),
                    "shopping_frequency": "Monthly"
                },
                "purchase_history": {
                    "total_orders": random.randint(20, 40),
                    "average_order_value": random.randint(80, 250),
                    "last_purchase": fake.date_between(start_date='-3m', end_date='-1d').strftime('%Y-%m-%d'),
                    "favorite_brands": random.sample(["Sony", "Bose", "Apple", "Sennheiser", "JBL"], 2),
                    "return_rate": f"{random.randint(5, 12)}%"
                },
                "current_session": {
                    "cart_items": random.randint(0, 3),
                    "cart_value": random.randint(0, 400),
                    "browsing_time": f"{random.randint(10, 30)} minutes",
                    "search_history": ["wireless headphones", "noise canceling", "bluetooth speakers"]
                }
            })
        
        # Shoes/Footwear intelligence
        elif any(word in query_lower for word in ['shoes', 'sneakers', 'running', 'boots', 'footwear']):
            base_context.update({
                "shopping_behavior": {
                    "preferred_categories": ["Shoes", "Sports", "Fashion"],
                    "price_sensitivity": random.choice(["Budget-conscious", "Value-seeker"]),
                    "device_preference": "Mobile",
                    "shopping_frequency": "Bi-weekly"
                },
                "purchase_history": {
                    "total_orders": random.randint(25, 50),
                    "average_order_value": random.randint(60, 180),
                    "last_purchase": fake.date_between(start_date='-2m', end_date='-1w').strftime('%Y-%m-%d'),
                    "favorite_brands": random.sample(["Nike", "Adidas", "New Balance", "Puma", "Allbirds"], 2),
                    "return_rate": f"{random.randint(8, 15)}%"
                },
                "current_session": {
                    "cart_items": random.randint(1, 4),
                    "cart_value": random.randint(50, 300),
                    "browsing_time": f"{random.randint(8, 25)} minutes",
                    "search_history": ["running shoes", "size 9", "athletic wear"]
                }
            })
        
        # Gift/Present intelligence
        elif any(word in query_lower for word in ['gift', 'present', 'birthday', 'anniversary', 'holiday']):
            base_context.update({
                "shopping_behavior": {
                    "preferred_categories": ["Gifts", "Electronics", "Home & Garden"],
                    "price_sensitivity": "Value-seeker",
                    "device_preference": random.choice(["Mobile", "Desktop"]),
                    "shopping_frequency": "Occasional"
                },
                "purchase_history": {
                    "total_orders": random.randint(12, 30),
                    "average_order_value": random.randint(40, 120),
                    "last_purchase": fake.date_between(start_date='-4m', end_date='-1m').strftime('%Y-%m-%d'),
                    "favorite_brands": random.sample(["Amazon Basics", "Apple", "Yankee Candle", "LEGO", "Nintendo"], 2),
                    "return_rate": f"{random.randint(3, 10)}%"
                },
                "current_session": {
                    "cart_items": random.randint(0, 2),
                    "cart_value": random.randint(0, 200),
                    "browsing_time": f"{random.randint(12, 40)} minutes",
                    "search_history": ["gift ideas", "under $50", "popular items"]
                },
                "gift_context": {
                    "occasion": random.choice(["Birthday", "Anniversary", "Holiday", "Graduation"]),
                    "recipient": random.choice(["Partner", "Friend", "Family member", "Colleague"]),
                    "budget_range": "$25-75"
                }
            })
        
        # Default shopping context
        else:
            base_context.update({
                "shopping_behavior": {
                    "preferred_categories": random.sample(["Electronics", "Clothing", "Home & Garden", "Books"], 2),
                    "price_sensitivity": random.choice(["Budget-conscious", "Value-seeker"]),
                    "device_preference": random.choice(["Mobile", "Desktop"]),
                    "shopping_frequency": random.choice(["Weekly", "Monthly"])
                },
                "purchase_history": {
                    "total_orders": random.randint(15, 40),
                    "average_order_value": random.randint(50, 150),
                    "last_purchase": fake.date_between(start_date='-2m', end_date='-1w').strftime('%Y-%m-%d'),
                    "favorite_brands": random.sample(["Amazon Basics", "Nike", "Apple", "Samsung"], 2),
                    "return_rate": f"{random.randint(5, 12)}%"
                },
                "current_session": {
                    "cart_items": random.randint(0, 3),
                    "cart_value": random.randint(0, 250),
                    "browsing_time": f"{random.randint(5, 30)} minutes",
                    "search_history": random.sample(["bestsellers", "deals", "new arrivals"], 2)
                }
            })
        
        # Add common preferences
        base_context["preferences"] = {
            "shipping_speed": random.choice(["Standard", "Express", "Prime"]),
            "payment_method": random.choice(["Credit card", "PayPal", "Apple Pay"]),
            "communication": random.choice(["Email", "SMS", "App notifications"]),
            "reviews": random.choice(["Always reads", "Sometimes reads"])
        }
        
        return base_context
    
    def get_sample_queries(self) -> List[str]:
        """Get sample e-commerce queries."""
        return [
            "Find wireless headphones under $100",
            "Show me running shoes for women",
            "I need a laptop for work",
            "Looking for birthday gift ideas",
            "Track my recent order"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for e-commerce queries."""
        return "e.g., Find wireless headphones, Show me running shoes, I need a laptop for work"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic e-commerce responses."""
        return "You are a helpful e-commerce assistant. Provide general product recommendations and shopping advice without using specific customer context."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual e-commerce responses."""
        return """You are a personalized e-commerce assistant. Use the provided customer context to give specific, tailored recommendations. Include:
- Product suggestions that match their preferences and purchase history
- Consider their budget and price sensitivity
- Reference their loyalty status and past purchases
- Provide personalized shopping advice
Be helpful, specific, and sales-oriented while being genuine."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for e-commerce queries."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['headphones', 'earbuds', 'audio']):
            return """🎧 **Great headphone recommendations for you:**

**Top Picks I'd Suggest:**
- **Sony WH-1000XM4** - Amazing noise canceling, perfect for travel
- **Apple AirPods Pro** - Seamless if you have an iPhone
- **Bose QuietComfort 45** - Super comfortable for long listening
- **JBL Tune 760NC** - Excellent value with good sound quality
- **Sennheiser HD 450BT** - Audiophile quality at a reasonable price

**What's your main use?** Music, calls, or gaming? I can narrow down the perfect match for you!

Would you like me to help you compare features or find the best deals?"""
        
        elif any(word in query_lower for word in ['shoes', 'sneakers', 'footwear']):
            return """👟 **Perfect shoe recommendations coming up:**

**What I'd recommend based on your needs:**
- **Running shoes** - Nike Air Zoom, Adidas Ultraboost for performance
- **Casual sneakers** - Allbirds Tree Runners, Vans Old Skool for everyday
- **Dress shoes** - Cole Haan, Clarks for professional occasions
- **Boots** - Timberland, Dr. Martens for durability and style
- **Sandals** - Birkenstock, Teva for comfort and support

**Tell me more about what you need them for** - running, work, casual wear? I can help you find the perfect fit and style!

Want to see current deals or specific size availability?"""
        
        elif any(word in query_lower for word in ['laptop', 'computer', 'pc']):
            return """💻 **Let me help you find the perfect laptop:**

**Based on what most customers need:**
- **For work/productivity** - MacBook Air M2, Dell XPS 13, ThinkPad X1
- **For gaming** - ASUS ROG, MSI Gaming, Alienware series
- **For students** - Acer Aspire, HP Pavilion, Lenovo IdeaPad
- **For creative work** - MacBook Pro, Surface Studio, HP Spectre
- **Budget-friendly** - Chromebooks, refurbished business laptops

**What will you mainly use it for?** Work, school, gaming, or creative projects? This helps me recommend the best specs and value for your needs.

I can also help you compare prices and find current promotions!"""
        
        elif any(word in query_lower for word in ['gift', 'present', 'birthday']):
            return """🎁 **I'd love to help you find the perfect gift:**

**Popular gift ideas I recommend:**
- **Tech gifts** - AirPods, smart watches, tablets, portable chargers
- **Fashion & accessories** - jewelry, handbags, scarves, sunglasses  
- **Home & lifestyle** - candles, coffee makers, cozy blankets, plants
- **Books & hobbies** - bestsellers, art supplies, puzzles, games
- **Experience gifts** - subscription boxes, gift cards, online courses

**Tell me about the recipient** - age, interests, relationship to you? I can suggest something they'll absolutely love!

What's your budget range? I'll find options that are perfect and thoughtful."""
        
        elif any(word in query_lower for word in ['track', 'order', 'shipping']):
            return """📦 **Let me help you track your order:**

**Here's how to check your order status:**
1. **Quick option:** Check your email for the tracking number I sent
2. **Account login:** Sign in and go to "My Orders" 
3. **Order lookup:** Use your order number and email
4. **Direct tracking:** Use the carrier's website with your tracking number

**Need immediate help?** I can look up your order right now if you have:
- Your order number, or
- The email address you used

**Shipping updates:** Most orders arrive within 2-5 business days, and I'll send you notifications at each step!

Is there a specific order you're concerned about? I'm here to help!"""
        
        else:
            return """🛒 **Welcome! I'm here to help you find exactly what you need:**

**How I can assist you today:**
- **Product recommendations** - Tell me what you're looking for
- **Compare options** - I'll help you find the best value
- **Check availability** - Size, color, stock status
- **Find deals** - Current sales and promotions
- **Answer questions** - Specs, shipping, returns, anything!

**Popular right now:**
- Electronics and tech accessories
- Fashion and seasonal items  
- Home essentials and decor
- Health and wellness products

**Just tell me what you're shopping for** and I'll help you find the perfect match! Whether it's a specific item or you're just browsing, I'm here to make your shopping experience great.

What can I help you discover today? 😊"""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for e-commerce queries."""
        query_lower = query.lower()
        customer = context['customer_profile']
        behavior = context['shopping_behavior']
        session = context['current_session']
        history = context['purchase_history']
        prefs = context['preferences']
        
        if any(word in query_lower for word in ['headphones', 'earbuds', 'audio']):
            return f"""🎯 **Perfect Headphones for {customer['name']}:**

Based on your {customer['loyalty_tier']} status and {behavior['price_sensitivity'].lower()} shopping style:

🌟 **Top Recommendation:**
- **Sony WH-1000XM4** - $280 (20% loyalty discount = $224)
  - ✅ Matches your {behavior['preferred_categories'][0]} preference
  - ✅ Similar to your recent {history['favorite_brands'][0]} purchases
  - ✅ {prefs['shipping_speed']} shipping available

🎵 **Alternative Options:**
- **Bose QuietComfort 45** - $250 (fits your ~${history['average_order_value']} average)
- **Apple AirPods Pro** - $180 (popular with {history['favorite_brands'][0]} users)

💡 **Special for you:** Free shipping + 30-day returns (as {customer['loyalty_tier']} member)

Add to cart now? Your {prefs['payment_method']} is ready!"""
        
        elif any(word in query_lower for word in ['shoes', 'sneakers', 'footwear']):
            return f"""👟 **Personalized Shoe Recommendations:**

Hey {customer['name']}! Based on your shopping history:

🏃 **Perfect Match:**
- **{history['favorite_brands'][0]} Running Shoes** - $120
  - ✅ Your favorite brand (5 previous purchases)
  - ✅ Fits your ${history['average_order_value']} typical spend
  - ✅ {behavior['price_sensitivity']} pricing tier

👕 **Complete the Look:**
- Matching athletic wear from your preferred {behavior['preferred_categories'][1]} category

🚚 **Delivery:** {prefs['shipping_speed']} shipping to {customer['location']}
💳 **Payment:** Use your saved {prefs['payment_method']}

Want to add to your cart with {session['cart_items']} current items?"""
        
        elif any(word in query_lower for word in ['laptop', 'computer', 'pc']):
            return f"""💻 **Laptop Recommendations for {customer['name']}:**

Based on your {customer['loyalty_tier']} member profile:

🎯 **Best Match:**
- **MacBook Air M2** - $999 (${history['average_order_value']} range)
  - ✅ Matches your {history['favorite_brands'][0]} brand loyalty
  - ✅ Perfect for {behavior['device_preference'].lower()} users like you
  - ✅ {customer['loyalty_tier']} member gets extended warranty

💼 **Alternative:**
- **Dell XPS 13** - $850 (great for {behavior['price_sensitivity'].lower()} shoppers)

🎁 **Member Perks:**
- Free setup service (${customer['loyalty_tier']} benefit)
- {prefs['shipping_speed']} shipping included
- 60-day return policy

Ready to upgrade your tech setup?"""
        
        elif any(word in query_lower for word in ['gift', 'present', 'birthday']):
            return f"""🎁 **Personalized Gift Ideas for {customer['name']}:**

Based on your gifting history and preferences:

🌟 **Trending in Your Categories:**
- **{behavior['preferred_categories'][0]} Gifts** ($50-150 range)
  - Smart home devices (popular with {customer['loyalty_tier']} members)
  - Premium accessories from {history['favorite_brands'][0]}

🎯 **Perfect Price Range:**
- Around ${history['average_order_value']} (your typical spend)
- {behavior['price_sensitivity']} options available

📦 **Gift Services:**
- Gift wrapping (free for {customer['loyalty_tier']} members)
- {prefs['shipping_speed']} delivery to {customer['location']}
- Gift receipt included

Want me to show specific items in your favorite categories?"""
        
        elif any(word in query_lower for word in ['track', 'order', 'shipping']):
            return f"""📦 **Order Tracking for {customer['name']}:**

Your recent order status:

🚚 **Latest Order:** 
- Order placed: {history['last_purchase']}
- Status: In transit
- Expected delivery: Tomorrow via {prefs['shipping_speed']} shipping
- Tracking: Will be sent to {customer['email']}

📱 **Quick Access:**
- Check your {prefs['communication']} for updates
- Use our mobile app for real-time tracking
- {customer['loyalty_tier']} members get priority support

🎯 **While you wait:** Items in your cart (${session['cart_value']}) are still available!

Need help with anything else?"""
        
        else:
            return f"""🛒 **Welcome back, {customer['name']}!**

Your personalized shopping experience:

🎯 **Just for You:**
- New arrivals in {', '.join(behavior['preferred_categories'])}
- {customer['loyalty_tier']} member exclusive deals
- Items similar to your {history['favorite_brands'][0]} purchases

📊 **Your Session:**
- Cart: {session['cart_items']} items (${session['cart_value']})
- Browsing: {session['browsing_time']} today
- Recently viewed: {', '.join(session['search_history'])}

🚀 **Quick Actions:**
- Complete your cart checkout
- Browse your {behavior['preferred_categories'][0]} favorites
- Check new {history['favorite_brands'][0]} arrivals

What can I help you find today?"""