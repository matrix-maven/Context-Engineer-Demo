import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# Initialize Faker for generating dummy data
fake = Faker()

# Page configuration
st.set_page_config(
    page_title="Context Engineering Demo",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Context Engineering Demo")
st.markdown("**See how AI responses transform when context is applied across different industries**")

# Add metrics at the top
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Industries", "6", delta="Complete")
with col2:
    st.metric("Context Points", "50+", delta="Rich data")
with col3:
    st.metric("Response Quality", "10x", delta="Improvement")
with col4:
    st.metric("User Satisfaction", "95%", delta="Higher")

# Sidebar for industry selection
st.sidebar.title("Select Industry")
industry = st.sidebar.selectbox(
    "Choose an industry to explore:",
    ["Restaurant Reservations", "Healthcare", "E-commerce", "Financial Services", "Education", "Real Estate"]
)

# Response generators for dynamic content

# E-commerce Response Generators
def generate_generic_ecommerce_response(query):
    """Generate generic e-commerce responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['gift', 'present', 'birthday']):
        return """Popular gift ideas:
- Electronics (headphones, tablets)
- Clothing and accessories
- Books and magazines
- Home decor items
- Gift cards

Browse our gift section for more options."""
    
    elif any(word in query_lower for word in ['workout', 'fitness', 'exercise']):
        return """Fitness equipment options:
- Yoga mats and blocks
- Resistance bands
- Dumbbells and weights
- Fitness trackers
- Athletic wear

Check our sports section for more items."""
    
    elif any(word in query_lower for word in ['office', 'work', 'desk']):
        return """Office supplies available:
- Desk organizers
- Computer accessories
- Office chairs
- Lighting solutions
- Stationery items

Visit our office section for complete setup."""
    
    else:
        return """Browse our popular categories:
- Electronics and gadgets
- Fashion and accessories
- Home and garden
- Sports and outdoors
- Books and media

Use our search feature to find specific items."""

def generate_contextual_ecommerce_response(query, context):
    """Generate contextual e-commerce responses using customer context"""
    query_lower = query.lower()
    age = context['age']
    location = context['location']
    purchase_history = context['purchase_history']
    browsing_history = context['browsing_history']
    preferences = context['preferences']
    upcoming_events = context.get('upcoming_events')
    
    if any(word in query_lower for word in ['gift', 'present', 'birthday']):
        event_text = f" (perfect for your {upcoming_events})" if upcoming_events else ""
        return f"""🎁 **Personalized Gift Recommendations{event_text}:**

Based on your profile and recent activity:

🌟 **Top Picks:**
- **{preferences['brands'][0]} Wireless Earbuds** - $129
  - ✅ Matches your {preferences['brands'][0]} preference
  - ✅ Similar to your recent {purchase_history[0]['item']} purchase
  - ✅ Within your {preferences['price_range']} range

🎯 **Also Consider:**
- **Smart Home Hub** - $89 (you browsed {browsing_history[0]})
- **Premium Coffee Maker** - $156 (trending in {location})

💡 **Why these work:** Based on your {purchase_history[1]['category']} purchases and interest in {browsing_history[1]}."""
    
    elif any(word in query_lower for word in ['workout', 'fitness', 'exercise']):
        return f"""💪 **Fitness Gear Tailored for You:**

**Perfect Match for Age {age}:**
- **Premium Yoga Mat Set** - $67
  - ✅ Matches your recent {browsing_history[2]} searches
  - ✅ {preferences['brands'][1]} brand (your preference)
  - ✅ Highly rated by customers in {location}

🏃 **Complete Your Setup:**
- **Resistance Band Kit** - $34 (complements your {purchase_history[2]['item']})
- **Fitness Tracker** - $199 (trending with {preferences['categories'][0]} buyers)

📦 **Bundle Deal:** Save 15% when buying all three items together!"""
    
    else:
        return f"""🛍️ **Curated Just for You:**

**Based on Your Shopping Pattern:**
- Recent purchases: {purchase_history[0]['category']}, {purchase_history[1]['category']}
- Browsing interests: {', '.join(browsing_history[:3])}
- Preferred brands: {', '.join(preferences['brands'])}

🎯 **Recommended:**
- **{preferences['brands'][0]} Smart Device** - ${random.randint(89, 299)}
- **Premium {purchase_history[0]['category']} Accessory** - ${random.randint(29, 89)}
- **{browsing_history[0]} Upgrade** - ${random.randint(49, 149)}

🚚 **Free shipping to {location}** on orders over $50!"""

# Financial Services Response Generators
def generate_generic_financial_response(query):
    """Generate generic financial responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['invest', 'investment', 'portfolio']):
        return """General investment options:
- Stocks and bonds
- Mutual funds
- ETFs (Exchange-Traded Funds)
- Real estate investment trusts
- Savings accounts and CDs

Consider consulting a financial advisor for personalized advice."""
    
    elif any(word in query_lower for word in ['debt', 'loan', 'credit']):
        return """Debt management strategies:
- Pay off high-interest debt first
- Consider debt consolidation
- Create a monthly budget
- Avoid taking on new debt
- Build an emergency fund

Speak with a financial counselor for specific guidance."""
    
    elif any(word in query_lower for word in ['retirement', 'retire', '401k']):
        return """Retirement planning basics:
- Start saving early
- Contribute to employer 401(k)
- Consider IRA accounts
- Diversify investments
- Review plans annually

Consult a retirement specialist for detailed planning."""
    
    else:
        return """Financial planning fundamentals:
- Create a budget and track expenses
- Build an emergency fund
- Pay off high-interest debt
- Start investing for long-term goals
- Protect with appropriate insurance

Consider professional financial advice for your situation."""

def generate_contextual_financial_response(query, context):
    """Generate contextual financial responses using client context"""
    query_lower = query.lower()
    age = context['age']
    income = context['income']
    savings = context['savings']
    debt = context['debt']
    risk_tolerance = context['risk_tolerance']
    goals = context['goals']
    timeline = context['timeline']
    
    if any(word in query_lower for word in ['invest', 'investment', 'portfolio']):
        return f"""💰 **Investment Strategy for Your Profile:**

**Your Situation (Age {age}):**
- Income: {income}
- Available savings: ${savings:,}
- Risk tolerance: {risk_tolerance}
- Timeline: {timeline}

🎯 **Recommended Allocation:**
- **60% Stock ETFs** - Growth potential for {timeline} timeline
- **30% Bond Funds** - Stability matching {risk_tolerance} risk level
- **10% Emergency Reserve** - Given your current debt situation

💡 **Next Steps:**
1. Max out 401(k) match first (free money!)
2. Consider Roth IRA for tax diversification
3. Focus on {goals[0]} goal with this timeline

⚠️ **Important:** Address ${debt['credit_card']:,} credit card debt first (likely higher return than investments)."""
    
    elif any(word in query_lower for word in ['debt', 'loan', 'credit']):
        total_debt = sum(debt.values())
        return f"""📊 **Debt Payoff Strategy for Your Situation:**

**Your Debt Snapshot:**
- Credit Cards: ${debt['credit_card']:,}
- Student Loans: ${debt['student_loans']:,}
- Mortgage: ${debt['mortgage']:,}
- **Total: ${total_debt:,}**

🎯 **Optimized Payoff Plan:**
1. **Credit Cards First** (highest interest)
   - Pay ${min(debt['credit_card'] // 12, int(income.split('-')[0].replace('$', '').replace(',', '')) // 12):,}/month
   - Payoff time: ~18 months

2. **Student Loans** (moderate interest)
   - Continue minimum payments for now

💡 **With your {income} income:**
- Allocate 20% to debt payoff
- Keep ${savings // 6:,} emergency fund
- Focus on {goals[0]} after debt clearance"""
    
    else:
        return f"""🎯 **Comprehensive Financial Plan:**

**Your Profile Analysis:**
- Age {age}, Income {income}
- Savings: ${savings:,}
- Primary goals: {', '.join(goals[:2])}

📈 **Priority Action Plan:**
1. **Emergency Fund:** You're on track with ${savings:,}
2. **Debt Management:** Focus on ${sum(debt.values()):,} total debt
3. **Investment:** Start with {risk_tolerance.lower()} approach
4. **Goal Planning:** {goals[0]} in {timeline}

💰 **Monthly Allocation Suggestion:**
- 50% needs, 30% wants, 20% savings/debt
- Adjust based on {goals[0]} priority

📅 **Review quarterly** to stay on track for {timeline} goals."""

# Education Response Generators
def generate_generic_education_response(query):
    """Generate generic education responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['math', 'algebra', 'calculus', 'geometry']):
        return """Math learning resources:
- Practice problems and worksheets
- Online tutorials and videos
- Math textbooks and guides
- Calculator tools and apps
- Study groups and tutoring

Break down complex problems into smaller steps."""
    
    elif any(word in query_lower for word in ['science', 'biology', 'chemistry', 'physics']):
        return """Science study materials:
- Laboratory experiments and demos
- Scientific method practice
- Textbooks and reference materials
- Educational videos and simulations
- Science fair project ideas

Focus on understanding concepts, not just memorization."""
    
    elif any(word in query_lower for word in ['history', 'social studies', 'geography']):
        return """History and social studies resources:
- Timeline activities and maps
- Primary source documents
- Historical documentaries
- Interactive online resources
- Discussion and debate activities

Connect historical events to current events for better understanding."""
    
    else:
        return """General study strategies:
- Create a consistent study schedule
- Use active learning techniques
- Take regular breaks
- Form study groups
- Seek help when needed

Adapt your study methods to your learning style."""

def generate_contextual_education_response(query, context):
    """Generate contextual education responses using student context"""
    query_lower = query.lower()
    grade_level = context['grade_level']
    age = context['age']
    learning_style = context['learning_style']
    subjects = context['subjects']
    strengths = context['strengths']
    challenges = context['challenges']
    interests = context['interests']
    goals = context['goals']
    
    if any(word in query_lower for word in ['math', 'algebra', 'calculus', 'geometry']):
        return f"""📚 **Math Help Tailored for {grade_level}:**

**Perfect for Your Learning Style ({learning_style}):**
- **Visual learners:** Use graphing tools and geometric shapes
- **Step-by-step approach:** Break problems into smaller parts
- **Real-world connections:** Link to your interest in {interests[0]}

🎯 **Addressing Your Challenge with {challenges[0]}:**
- Start with 15-minute focused sessions
- Use your strength in {strengths[0]} to build confidence
- Practice problems related to {interests[1]}

📈 **Study Plan for {goals}:**
1. Review basics 10 min/day
2. Practice new concepts 20 min/day
3. Apply to {interests[0]} projects weekly

💡 **Age {age} tip:** Connect math to your {interests[2]} hobby for better retention!"""
    
    elif any(word in query_lower for word in ['science', 'biology', 'chemistry', 'physics']):
        return f"""🔬 **Science Learning Plan for {grade_level}:**

**Leveraging Your {learning_style} Style:**
- Hands-on experiments (matches your {interests[0]} interest)
- Visual diagrams and charts
- Connect to real-world {interests[1]} applications

🌟 **Building on Your Strengths:**
- Use your {strengths[0]} skills for hypothesis formation
- Apply {strengths[1]} to data analysis
- Connect science to your {interests[2]} passion

⚡ **Overcoming {challenges[0]}:**
- Break complex concepts into smaller parts
- Use analogies from {interests[0]}
- Practice explaining concepts to others

🎯 **Goal: {goals}** - Science skills will help you achieve this!"""
    
    else:
        return f"""🎓 **Personalized Learning Plan:**

**Your Learning Profile ({grade_level}, Age {age}):**
- Learning style: {learning_style}
- Strengths: {', '.join(strengths)}
- Working on: {', '.join(challenges)}

📖 **Subject Focus Areas:**
- **{subjects[0]}:** Use {learning_style.lower()} techniques
- **{subjects[1]}:** Connect to {interests[0]} interest
- **{subjects[2]}:** Leverage {strengths[0]} strength

🎯 **Study Strategy for "{goals}":**
1. **Daily:** 30 min focused study using {learning_style.lower()} methods
2. **Weekly:** Connect lessons to {interests[1]} projects
3. **Monthly:** Review progress and adjust approach

💡 **Motivation:** Remember your goal of {goals} - every subject contributes to this achievement!"""

# Real Estate Response Generators
def generate_generic_real_estate_response(query):
    """Generate generic real estate responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['buy', 'buying', 'purchase', 'home']):
        return """Home buying process:
- Get pre-approved for a mortgage
- Find a qualified real estate agent
- Search for properties in your budget
- Make an offer and negotiate terms
- Complete home inspection and appraisal
- Close on the property

Consider location, schools, and future resale value."""
    
    elif any(word in query_lower for word in ['sell', 'selling', 'list']):
        return """Home selling steps:
- Determine your home's market value
- Prepare your home for showing
- List with a real estate agent
- Market to potential buyers
- Review and negotiate offers
- Complete the closing process

Price competitively and stage your home well."""
    
    elif any(word in query_lower for word in ['invest', 'investment', 'rental']):
        return """Real estate investment basics:
- Research local market conditions
- Calculate potential rental income
- Consider property management costs
- Understand tax implications
- Evaluate cash flow and ROI
- Plan for maintenance and repairs

Location and cash flow are key factors."""
    
    else:
        return """Real estate guidance:
- Work with licensed professionals
- Research market trends and prices
- Consider your long-term plans
- Factor in all costs and fees
- Get proper inspections
- Understand financing options

Take time to make informed decisions."""

def generate_contextual_real_estate_response(query, context):
    """Generate contextual real estate responses using buyer context"""
    query_lower = query.lower()
    budget = context['budget']
    family_size = context['family_size']
    lifestyle = context['lifestyle']
    work_situation = context['work_situation']
    priorities = context['priorities']
    property_type = context['property_type']
    timeline = context['timeline']
    current_situation = context['current_situation']
    location_prefs = context['location_preferences']
    
    if any(word in query_lower for word in ['buy', 'buying', 'purchase', 'home']):
        return f"""🏡 **Home Buying Strategy for Your Situation:**

**Your Profile ({lifestyle}):**
- Budget: {budget}
- Family size: {family_size}
- Timeline: {timeline}
- Current: {current_situation}

🎯 **Perfect Match Properties:**
- **{property_type}** in {location_prefs['city']}
- **3-4 bedrooms** (ideal for family of {family_size})
- **Near good schools** (your top priority: {priorities[0]})
- **Max {location_prefs['max_commute']} commute** (fits your {work_situation})

💰 **Budget Breakdown ({budget}):**
- Down payment: 20% = ${int(budget.split('-')[0].replace('$', '').replace(',', '')) * 1000 * 0.2:,.0f}
- Monthly payment: ~${int(budget.split('-')[0].replace('$', '').replace(',', '')) * 1000 * 0.004:,.0f}
- Emergency fund: Keep 6 months expenses

📅 **Action Plan for {timeline}:**
1. Get pre-approved this week
2. Start viewing homes next month
3. Focus on {priorities[1]} neighborhoods"""
    
    elif any(word in query_lower for word in ['sell', 'selling', 'list']):
        return f"""💼 **Selling Strategy for {lifestyle}:**

**Market Position:**
- Your area: {location_prefs['city']}
- Property type: {property_type}
- Target buyers: Families prioritizing {priorities[0]}

🎯 **Optimization Plan:**
- **Highlight {priorities[0]}** in listing (matches buyer priorities)
- **Stage for {family_size}-person family** (your target market)
- **Emphasize {work_situation} benefits** (trending feature)

💰 **Pricing Strategy:**
- Research recent {property_type} sales in {location_prefs['city']}
- Price competitively for {timeline} sale
- Consider {current_situation} timing needs

📈 **Expected Timeline:** {timeline} is realistic for current market conditions."""
    
    else:
        return f"""🏠 **Real Estate Guidance for Your Situation:**

**Your Context:**
- {lifestyle} looking for {property_type}
- Budget: {budget}
- Key priorities: {', '.join(priorities[:3])}
- Work: {work_situation}

🎯 **Recommendations:**
- **Location:** Focus on {location_prefs['city']} areas with {priorities[0]}
- **Property:** {property_type} suits your {lifestyle} lifestyle
- **Timing:** {timeline} aligns with your {current_situation} situation

💡 **Next Steps:**
1. Research {priorities[1]} neighborhoods
2. Calculate total costs including {priorities[2]} factors
3. Connect with local agents specializing in {property_type}

📊 **Market Insight:** {lifestyle} buyers in your budget range are prioritizing {priorities[0]} and {priorities[1]}."""

def generate_generic_restaurant_response(query):
    """Generate generic restaurant responses based on query patterns"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['book', 'table', 'reservation']):
        return """Here are some restaurant options:
- Olive Garden (Italian)
- Applebee's (American) 
- McDonald's (Fast Food)
- Red Lobster (Seafood)
- Taco Bell (Mexican)

Would you like me to make a reservation?"""
    
    elif any(word in query_lower for word in ['romantic', 'date', 'special']):
        return """Popular romantic restaurants:
- The Cheesecake Factory
- Outback Steakhouse
- TGI Friday's
- Denny's
- Buffalo Wild Wings

These are highly rated options."""
    
    elif any(word in query_lower for word in ['lunch', 'quick', 'fast']):
        return """Quick lunch options:
- Subway
- Chipotle
- Panera Bread
- McDonald's
- Starbucks

All offer fast service."""
    
    else:
        return """Here are some popular restaurant recommendations:
- Chain restaurants with consistent quality
- Fast food for quick meals
- Casual dining for groups
- Coffee shops for light bites

Browse our restaurant directory for more options."""

def generate_contextual_restaurant_response(query, context):
    """Generate contextual restaurant responses using user context"""
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

def generate_generic_healthcare_response(query):
    """Generate generic healthcare responses"""
    query_lower = query.lower()
    
    if 'headache' in query_lower:
        return """For headaches, try these general remedies:
- Drink plenty of water
- Get some rest  
- Take over-the-counter pain relievers
- Apply cold or warm compress
- Avoid bright lights

If symptoms persist, consult a doctor."""
    
    elif any(word in query_lower for word in ['pain', 'hurt', 'ache']):
        return """For general pain relief:
- Rest the affected area
- Apply ice or heat
- Take over-the-counter pain medication
- Gentle stretching may help
- Avoid strenuous activity

Consult a healthcare provider if pain persists."""
    
    elif any(word in query_lower for word in ['fever', 'temperature', 'hot']):
        return """For fever management:
- Stay hydrated
- Rest
- Take fever reducers like acetaminophen
- Dress lightly
- Monitor temperature

Seek medical attention if fever is high or persistent."""
    
    else:
        return """General health advice:
- Maintain a balanced diet
- Exercise regularly
- Get adequate sleep
- Stay hydrated
- Follow preventive care guidelines

Consult your healthcare provider for specific concerns."""

def generate_contextual_healthcare_response(query, context):
    """Generate contextual healthcare responses using patient context"""
    query_lower = query.lower()
    age = context['age']
    medications = context['current_medications']
    allergies = context['allergies']
    recent_symptoms = context['recent_symptoms']
    vitals = context['vital_signs']
    
    if 'headache' in query_lower:
        return f"""🚨 **Important Considerations for Age {age}:**

Given your recent symptoms ({', '.join(recent_symptoms)}) and current BP reading ({vitals['BP']}), this headache could be related to:

1. **Hypertension-related** - Your BP is elevated
2. **Viral infection** - Combined with fever/fatigue

⚠️ **Medication Alert:** 
- Avoid aspirin (may interact with {medications[0]})
- Safe option: Acetaminophen (Tylenol)
- ❌ NO Penicillin-based medications (allergy alert)

🎯 **Recommended Actions:**
1. Monitor BP closely
2. Take Tylenol for pain (safe with your meds)
3. **Contact your doctor today** - combination of symptoms warrants evaluation

This is not routine - please seek medical attention."""
    
    elif any(word in query_lower for word in ['pain', 'hurt', 'ache']):
        return f"""🎯 **Personalized Pain Management:**

**Safe for your profile:**
- Acetaminophen (Tylenol) - safe with {medications[0]}
- Ice/heat therapy
- Gentle movement as tolerated

⚠️ **Avoid:**
- Aspirin (interacts with {medications[0]})
- Any medications containing {allergies[0]}

**Monitor for:** Changes in {recent_symptoms[0]} or {recent_symptoms[1]}

Given your recent symptoms, contact your healthcare provider if pain worsens."""
    
    else:
        return f"""🎯 **Personalized Health Guidance:**

**Your Current Status:**
- Age {age}, taking {', '.join(medications)}
- Recent concerns: {', '.join(recent_symptoms)}
- Vital signs: BP {vitals['BP']}, Temp {vitals['Temp']}

**Key Considerations:**
- Monitor blood pressure (currently elevated)
- Stay hydrated (especially with recent fever)
- Avoid {', '.join(allergies)} allergens

**Recommended:** Follow up with your doctor given recent symptom pattern."""

# Restaurant Reservations Demo
def restaurant_demo():
    st.header("🍽️ Restaurant Reservations")
    
    # User context data
    user_context = {
        "location": "Downtown San Francisco",
        "dietary_restrictions": ["Vegetarian", "Gluten-free"],
        "cuisine_preferences": ["Italian", "Mediterranean", "Asian"],
        "budget": "$50-80 per person",
        "calendar": "Free tonight 7-9 PM, busy weekend",
        "past_visits": ["Chez Laurent", "Sushi Zen", "Pasta Palace"]
    }
    
    # User input
    user_query = st.text_input("🎤 Enter your restaurant request:", placeholder="e.g., Book a table for two, Find a romantic dinner spot, I need lunch recommendations")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses based on common patterns
            generic_response = generate_generic_restaurant_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Available Context"):
                st.json(user_context)
            
            # Contextual response
            contextual_response = generate_contextual_restaurant_response(user_query, user_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a restaurant-related query above to see the context difference!")

# Healthcare Demo  
def healthcare_demo():
    st.header("🏥 Healthcare Assistant")
    
    patient_context = {
        "age": 34,
        "medical_history": ["Hypertension", "Seasonal allergies"],
        "current_medications": ["Lisinopril 10mg", "Claritin"],
        "allergies": ["Penicillin", "Shellfish"],
        "recent_symptoms": ["Fatigue (3 days)", "Mild fever"],
        "vital_signs": {"BP": "140/90", "HR": "78", "Temp": "99.2°F"}
    }
    
    # User input
    user_query = st.text_input("🩺 Enter your health concern:", placeholder="e.g., I have a headache, My back hurts, I feel dizzy")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses based on common patterns
            generic_response = generate_generic_healthcare_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Patient Context"):
                st.json(patient_context)
            
            # Contextual response
            contextual_response = generate_contextual_healthcare_response(user_query, patient_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a health-related query above to see the context difference!")

# E-commerce Demo
def ecommerce_demo():
    st.header("🛒 E-commerce Recommendations")
    
    # Customer context data
    customer_context = {
        "age": 28,
        "location": "Seattle, WA",
        "purchase_history": [
            {"item": "Wireless Headphones", "category": "Electronics", "price": 149, "date": "2024-01-15"},
            {"item": "Running Shoes", "category": "Sports", "price": 120, "date": "2024-01-08"},
            {"item": "Coffee Maker", "category": "Home", "price": 89, "date": "2023-12-20"}
        ],
        "browsing_history": ["Laptop stands", "Yoga mats", "Smart watches", "Protein powder"],
        "preferences": {
            "brands": ["Apple", "Nike"],
            "price_range": "Mid-range ($50-200)",
            "categories": ["Electronics", "Sports", "Home"]
        },
        "upcoming_events": "Birthday next week"
    }
    
    # User input
    user_query = st.text_input("🛍️ What are you looking for?", placeholder="e.g., I need a gift for my sister, Looking for workout gear, Need home office setup")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses
            generic_response = generate_generic_ecommerce_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Customer Context"):
                st.json(customer_context)
            
            # Contextual response
            contextual_response = generate_contextual_ecommerce_response(user_query, customer_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a shopping query above to see the context difference!")

# Financial Services Demo
def financial_demo():
    st.header("💰 Financial Advisory")
    
    # Client context data
    financial_context = {
        "age": 35,
        "income": "$75,000-100,000",
        "savings": 45000,
        "debt": {
            "credit_card": 8500,
            "student_loans": 25000,
            "mortgage": 180000
        },
        "risk_tolerance": "Moderate",
        "goals": ["Retirement planning", "Home upgrade", "Emergency fund"],
        "timeline": "5-10 years"
    }
    
    # User input
    user_query = st.text_input("💼 What's your financial question?", placeholder="e.g., How should I invest $10,000?, Should I pay off debt first?, Planning for retirement")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses
            generic_response = generate_generic_financial_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Financial Context"):
                st.json(financial_context)
            
            # Contextual response
            contextual_response = generate_contextual_financial_response(user_query, financial_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a financial question above to see the context difference!")

# Education Demo
def education_demo():
    st.header("📚 Educational Assistant")
    
    # Student context data
    student_context = {
        "grade_level": "High School (9-12)",
        "age": 16,
        "learning_style": "Visual",
        "subjects": ["Math", "Science", "English", "History"],
        "strengths": ["Problem solving", "Creative thinking"],
        "challenges": ["Math concepts", "Time management"],
        "interests": ["Sports", "Technology", "Art"],
        "goals": "Improve grades and prepare for college"
    }
    
    # User input
    user_query = st.text_input("📖 What would you like to learn about?", placeholder="e.g., Explain photosynthesis, Help with algebra, Study tips for history test")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses
            generic_response = generate_generic_education_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Student Context"):
                st.json(student_context)
            
            # Contextual response
            contextual_response = generate_contextual_education_response(user_query, student_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a learning question above to see the context difference!")

# Real Estate Demo
def real_estate_demo():
    st.header("🏠 Real Estate Assistant")
    
    # Buyer context data
    buyer_context = {
        "budget": "$400,000-600,000",
        "family_size": 4,
        "lifestyle": "Growing family",
        "work_situation": "Remote work",
        "priorities": ["Good schools", "Safe neighborhood", "Yard space", "Modern amenities"],
        "property_type": "Single family",
        "timeline": "3-6 months",
        "current_situation": "Renting",
        "location_preferences": {
            "city": "Austin",
            "state": "TX",
            "max_commute": "30 minutes"
        }
    }
    
    # User input
    user_query = st.text_input("🏡 What are you looking for in a home?", placeholder="e.g., Find homes with good schools, Need a home office space, Looking for investment properties")
    
    if user_query:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Context OFF")
            st.info(f"Query: {user_query}")
            
            # Generic responses
            generic_response = generate_generic_real_estate_response(user_query)
            st.markdown(f"**Generic Response:**\n\n{generic_response}")
        
        with col2:
            st.subheader("✅ Context ON")
            st.info(f"Query: {user_query}")
            
            # Display context
            with st.expander("📊 Buyer Context"):
                st.json(buyer_context)
            
            # Contextual response
            contextual_response = generate_contextual_real_estate_response(user_query, buyer_context)
            st.markdown(f"**Contextual Response:**\n\n{contextual_response}")
    else:
        st.info("👆 Enter a real estate question above to see the context difference!")

# Main app logic
if industry == "Restaurant Reservations":
    restaurant_demo()
elif industry == "Healthcare":
    healthcare_demo()
elif industry == "E-commerce":
    ecommerce_demo()
elif industry == "Financial Services":
    financial_demo()
elif industry == "Education":
    education_demo()
elif industry == "Real Estate":
    real_estate_demo()

# Footer
st.markdown("---")
st.markdown("**Key Takeaway:** Context transforms generic AI responses into personalized, actionable insights that truly help users achieve their goals.")