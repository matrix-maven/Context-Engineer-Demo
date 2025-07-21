"""
Real Estate Demo Module

Implements the real estate industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo

fake = Faker()


class RealEstateDemo(BaseDemo):
    """Real estate assistant demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        from services.prompt_service import Industry
        super().__init__("Real Estate", Industry.REAL_ESTATE, ai_service, context_service)
    
    def _parse_price_range(self, price_range: str) -> float:
        """Parse price range string to get numeric value for calculations."""
        # Handle special cases like "$1M+"
        if "$1M+" in price_range:
            return 1000000
        elif "M" in price_range:
            return float(price_range.replace('$', '').replace('M', '').split('-')[0]) * 1000000
        elif "k" in price_range:
            return float(price_range.replace('$', '').replace('k', '').split('-')[0]) * 1000
        else:
            return float(price_range.replace('$', '').replace(',', '').split('-')[0])
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic real estate context using Faker."""
        client_type = random.choice(["Buyer", "Seller", "Renter", "Investor"])
        
        return {
            "client_profile": {
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "client_type": client_type,
                "age": random.randint(25, 65),
                "family_status": random.choice(["Single", "Married", "Married with children", "Divorced", "Widowed"]),
                "employment": random.choice(["Employed", "Self-employed", "Retired", "Student"]),
                "location": f"{fake.city()}, {fake.state()}"
            },
            "financial_profile": {
                "annual_income": random.choice(["$40k-60k", "$60k-80k", "$80k-120k", "$120k-180k", "$180k+"]),
                "credit_score": random.randint(580, 850),
                "down_payment_available": random.randint(10000, 150000) if client_type in ["Buyer", "Investor"] else 0,
                "pre_approved": random.choice([True, False]) if client_type in ["Buyer", "Investor"] else None,
                "debt_to_income": f"{random.randint(20, 45)}%",
                "savings": random.randint(5000, 200000)
            },
            "property_preferences": {
                "property_type": random.choice(["Single Family", "Condo", "Townhouse", "Multi-family", "Land"]),
                "bedrooms": random.randint(1, 5),
                "bathrooms": random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4]),
                "square_footage": random.choice(["800-1200", "1200-1800", "1800-2500", "2500-3500", "3500+"]),
                "price_range": random.choice([
                    "$100k-200k", "$200k-350k", "$350k-500k", "$500k-750k", "$750k-1M", "$1M+"
                ]),
                "preferred_areas": random.sample([
                    "Downtown", "Suburbs", "Waterfront", "Historic District", "New Development", "School District"
                ], random.randint(2, 3)),
                "must_haves": random.sample([
                    "Garage", "Yard", "Updated kitchen", "Master suite", "Home office", "Pool", "Fireplace"
                ], random.randint(2, 4)),
                "deal_breakers": random.sample([
                    "Busy street", "No parking", "Needs major repairs", "HOA fees", "Long commute"
                ], random.randint(1, 2))
            },
            "current_situation": {
                "timeline": random.choice(["ASAP", "Within 3 months", "3-6 months", "6-12 months", "Flexible"]),
                "urgency_reason": random.choice([
                    "Job relocation", "Growing family", "Downsizing", "Investment opportunity", 
                    "Lease ending", "Market timing", "Life change"
                ]),
                "current_housing": random.choice([
                    "Renting apartment", "Renting house", "Living with family", "Own current home", "Temporary housing"
                ]),
                "commute_requirements": {
                    "work_location": f"{fake.city()}, {fake.state()}",
                    "max_commute": random.choice(["15 min", "30 min", "45 min", "1 hour", "No preference"]),
                    "transportation": random.choice(["Car", "Public transit", "Walking/Biking", "Mixed"])
                }
            },
            "market_context": {
                "local_market": random.choice(["Seller's market", "Buyer's market", "Balanced market"]),
                "average_days_on_market": random.randint(15, 90),
                "price_trend": random.choice(["Rising", "Stable", "Declining"]),
                "inventory_level": random.choice(["Very low", "Low", "Normal", "High"]),
                "interest_rates": f"{random.uniform(6.0, 8.0):.2f}%",
                "seasonal_factor": random.choice(["Peak season", "Slow season", "Normal activity"])
            },
            "experience_and_history": {
                "first_time_buyer": random.choice([True, False]) if client_type == "Buyer" else False,
                "previous_transactions": random.randint(0, 5),
                "real_estate_knowledge": random.choice(["Beginner", "Some experience", "Experienced", "Expert"]),
                "preferred_communication": random.choice(["Email", "Phone", "Text", "In-person", "Video call"]),
                "agent_relationship": random.choice(["New client", "Returning client", "Referral"]),
                "past_challenges": random.sample([
                    "Financing issues", "Inspection problems", "Bidding wars", "Timing conflicts", "Market volatility"
                ], random.randint(0, 2))
            }
        }
    
    def get_sample_queries(self) -> List[str]:
        """Get sample real estate queries."""
        return [
            "I'm looking to buy my first home",
            "What's my home worth in today's market?",
            "Show me properties in good school districts",
            "I need to sell quickly due to job relocation",
            "What are current mortgage rates?"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for real estate queries."""
        return "e.g., I'm looking to buy my first home, What's my home worth?, Show me properties"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic real estate responses."""
        return "You are a helpful real estate assistant. Provide general real estate advice and market information without using specific client context."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual real estate responses."""
        return """You are a personalized real estate advisor. Use the provided client context to give specific, relevant real estate guidance. Consider:
- Client type (buyer, seller, renter, investor) and experience level
- Financial profile and pre-approval status
- Property preferences and must-haves/deal-breakers
- Timeline and urgency factors
- Local market conditions and trends
- Commute and lifestyle requirements

Provide actionable, professional advice tailored to their specific situation."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for real estate queries."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['buy', 'buying', 'purchase', 'first time']):
            return """🏠 **Your Home Buying Journey - Let Me Guide You:**

**As your real estate agent, I'll walk you through every step:**

**Phase 1: Financial Preparation (Week 1-2)**
- **Get pre-approved** - I'll connect you with trusted lenders
- **Determine your budget** - Not just what you qualify for, but what's comfortable
- **Down payment planning** - Explore options from 3% to 20%
- **Closing cost preparation** - Budget 2-5% of purchase price

**Phase 2: Home Search Strategy (Week 3-8)**
- **Define your must-haves** - Location, size, features, schools
- **Market analysis** - I'll show you current inventory and pricing trends
- **Property tours** - We'll visit homes that match your criteria
- **Neighborhood insights** - I know the local markets inside and out

**Phase 3: Making Your Offer (Week 8-10)**
- **Competitive offer strategy** - Price, terms, and contingencies
- **Negotiation expertise** - I'll advocate for your best interests
- **Contract review** - Ensuring all terms protect you
- **Timeline management** - Keeping everything on track

**Phase 4: Closing Process (Week 10-14)**
- **Home inspection coordination** - Protecting your investment
- **Appraisal management** - Ensuring fair market value
- **Final walkthrough** - Confirming property condition
- **Closing day support** - I'll be there to ensure smooth completion

**First-Time Buyer Advantages:**
- **FHA loans** - 3.5% down payment options
- **First-time buyer programs** - State and local assistance
- **Tax benefits** - Mortgage interest deductions
- **My expertise** - I specialize in helping first-time buyers

**What I Bring to Your Home Search:**
- **Market knowledge** - Pricing trends, neighborhood insights
- **Professional network** - Lenders, inspectors, contractors
- **Negotiation skills** - Getting you the best deal possible
- **Personal attention** - Your goals are my priority

**Current Market Insights:**
- Interest rates are stabilizing - good time to lock in
- Inventory is improving - more choices for buyers
- Seasonal trends favor buyers in fall/winter months
- Multiple offer situations still common in desirable areas

**My Promise to You:**
I'll be your advocate, advisor, and guide throughout this process. No pressure, just professional expertise focused on finding you the perfect home.

**Ready to start your home search?** Let's schedule a consultation to discuss your needs and create a personalized buying strategy! 🔑"""
        
        elif any(word in query_lower for word in ['sell', 'selling', 'worth', 'value']):
            return """💰 **Selling Your Home - My Proven Marketing Strategy:**

**As your listing agent, I'll maximize your home's value and minimize time on market:**

**Step 1: Professional Market Analysis**
- **Comparative Market Analysis (CMA)** - Recent sales in your neighborhood
- **Current competition** - What's actively for sale and at what price
- **Market trends** - Seasonal patterns and buyer demand
- **Pricing strategy** - Competitive positioning for quick sale

**Step 2: Home Preparation & Staging**
- **Pre-listing inspection** - Address issues before buyers find them
- **Strategic improvements** - High-impact, cost-effective updates
- **Professional staging** - Making your home irresistible to buyers
- **Curb appeal enhancement** - First impressions matter most

**Step 3: Marketing Excellence**
- **Professional photography** - High-quality images that sell
- **MLS listing optimization** - Maximum exposure to agents and buyers
- **Online marketing** - Zillow, Realtor.com, social media promotion
- **Traditional marketing** - Signs, flyers, open houses when appropriate

**Step 4: Showing Management**
- **Flexible showing schedule** - Accommodating serious buyers
- **Feedback collection** - Understanding buyer reactions
- **Open house events** - Creating buyer competition
- **Virtual tours** - Reaching remote and busy buyers

**Step 5: Offer Negotiation**
- **Multiple offer strategy** - Maximizing your sale price
- **Terms evaluation** - Price isn't everything (timing, contingencies matter)
- **Counteroffer expertise** - Getting the best possible deal
- **Contract management** - Protecting your interests throughout

**What Your Home is Worth:**
- **Market value** depends on location, condition, and current demand
- **Pricing too high** results in longer market time and lower final price
- **Pricing strategically** often generates multiple offers above asking
- **I'll provide detailed analysis** specific to your property

**My Selling Advantages:**
- **Local market expertise** - I know what buyers want in your area
- **Professional network** - Contractors, stagers, photographers
- **Marketing reach** - Maximum exposure through all channels
- **Negotiation skills** - Getting you top dollar

**Current Seller Market:**
- Buyer demand remains strong in most price ranges
- Well-priced homes are selling quickly (often within 30 days)
- Professional presentation is crucial for maximum value
- Seasonal timing can impact both price and speed of sale

**My Commitment to You:**
- **Honest pricing advice** - Based on market data, not wishful thinking
- **Comprehensive marketing** - Professional presentation and promotion
- **Regular communication** - Weekly updates on activity and feedback
- **Expert negotiation** - Protecting your interests in every offer

**Ready to sell?** Let's schedule a consultation where I'll provide a detailed market analysis and personalized selling strategy for your home! 📈"""
        
        elif any(word in query_lower for word in ['school', 'district', 'education']):
            return """🎓 **School District Home Search - My Family-Focused Expertise:**

**As your family's real estate agent, I understand that schools are often the #1 priority:**

**School District Research I Provide:**
- **Test scores and ratings** - State assessments, GreatSchools.org ratings
- **School boundaries** - Exact attendance zones (these can change!)
- **Enrollment trends** - Growing vs. declining districts
- **Special programs** - Gifted, STEM, arts, language immersion
- **Extracurricular offerings** - Sports, clubs, academic competitions

**Top-Rated Districts in Our Area:**
**Excellent (9-10 Rating):**
- Premium pricing (+15-25% above market average)
- High demand, limited inventory
- Strong resale values and appreciation
- Competitive admission to top universities

**Very Good (7-8 Rating):**
- Moderate premium (+5-15% above market)
- Good balance of quality and value
- **Often my recommendation** for best overall value
- Still excellent college preparation

**My School District Strategy:**
**For Elementary Families:**
- Focus on elementary boundaries first
- Consider middle/high school progression
- Evaluate neighborhood stability
- Plan for potential boundary changes

**For Middle/High School Families:**
- Immediate school quality is priority
- Consider specialized programs
- Evaluate peer groups and culture
- Plan for college preparation resources

**Beyond Test Scores - What I Evaluate:**
- **Teacher quality and retention**
- **Class sizes and student-teacher ratios**
- **Facilities and technology resources**
- **Parent involvement and community support**
- **Safety records and policies**
- **Special needs accommodations**

**Home Search Strategy:**
**Budget Considerations:**
- School premium can add $20k-100k+ to home prices
- Property taxes often higher in top districts
- Consider total cost of ownership
- Evaluate private school alternatives

**Timing Factors:**
- **Spring market** - Families moving for fall enrollment
- **Summer closings** - Settled before school starts
- **Enrollment deadlines** - Some districts have cutoff dates
- **Rental options** - Temporary housing while searching

**My Family-Focused Services:**
- **School visit coordination** - Scheduling tours during your home search
- **Boundary verification** - Confirming exact school assignments
- **Future planning** - Considering K-12 progression
- **Community connections** - Introducing you to other families

**Red Flags I Help You Avoid:**
- Homes on school boundary lines (risk of reassignment)
- Districts with declining enrollment or funding
- Areas with frequent boundary changes
- Overpriced homes solely due to school reputation

**Investment Perspective:**
- Top school districts maintain value better in downturns
- Easier resale when you're ready to move
- Strong rental demand if you relocate
- Generational wealth building through appreciation

**My Promise to School-Focused Families:**
I'll help you find the perfect balance of home, neighborhood, and schools within your budget. Your children's education is an investment in their future - let's make sure you're making the right choice.

**Ready to find your family's perfect home and school combination?** Let's discuss your specific needs and create a targeted search strategy! 📚"""
        
        elif any(word in query_lower for word in ['mortgage', 'rate', 'financing', 'loan']):
            return """💳 **Mortgage and Financing Guidance - My Lending Expertise:**

**As your real estate agent, I work with financing every day. Let me guide you through your options:**

**Current Market Rates (Updated Weekly):**
- **30-Year Fixed:** 6.5-7.5% (most popular option)
- **15-Year Fixed:** 6.0-7.0% (faster payoff, higher payments)
- **5/1 ARM:** 5.5-6.5% (lower initial rate, adjusts after 5 years)
- **FHA Loans:** Similar rates, lower down payment requirements

**Loan Programs I Help Clients Navigate:**

**Conventional Loans (Most Common):**
- **Down payment:** 5-20% (20% avoids PMI)
- **Credit score:** 620+ (better rates with 740+)
- **Debt-to-income:** Under 43% preferred
- **Best for:** Strong credit, stable income

**FHA Loans (First-Time Buyer Friendly):**
- **Down payment:** 3.5% minimum
- **Credit score:** 580+ (some lenders accept lower)
- **Mortgage insurance:** Required but removable
- **Best for:** Lower down payment, flexible credit

**VA Loans (Veterans):**
- **Down payment:** $0 (100% financing)
- **No PMI:** Significant monthly savings
- **Credit requirements:** Flexible
- **Best for:** Eligible veterans and service members

**USDA Loans (Rural Areas):**
- **Down payment:** $0 in eligible areas
- **Income limits:** Based on area median income
- **Property requirements:** Must be in qualified rural zones
- **Best for:** Rural and suburban buyers

**My Lender Network:**
I work with trusted mortgage professionals who:
- **Close on time** - Protecting your purchase contract
- **Competitive rates** - Shopping multiple investors
- **Excellent communication** - Keeping everyone informed
- **Local expertise** - Understanding our market conditions

**Pre-Approval Process:**
**What You'll Need:**
- 2 years tax returns
- 2 months bank statements
- Pay stubs (30 days)
- Employment verification
- Credit report authorization

**Benefits of Pre-Approval:**
- **Know your budget** - Shop with confidence
- **Stronger offers** - Sellers take you seriously
- **Faster closing** - Much of the work is already done
- **Rate protection** - Lock in current rates

**Rate Shopping Strategy:**
- **Get quotes from 3-5 lenders** - Rates and fees vary
- **Compare APR, not just rate** - Includes all costs
- **Consider local vs. national** - Service levels differ
- **Timing matters** - Rates change daily

**Down Payment Options:**
**20% Down (Ideal):**
- No PMI required
- Better interest rates
- Stronger negotiating position
- Lower monthly payments

**Less Than 20% Down:**
- PMI required (0.3-1.5% annually)
- Slightly higher rates
- Still viable option for many buyers
- PMI removable when you reach 20% equity

**First-Time Buyer Programs:**
- **State programs** - Down payment assistance
- **Local grants** - City/county assistance
- **Employer programs** - Some companies offer help
- **Family gifts** - Properly documented gift funds

**My Financing Support:**
- **Lender recommendations** - Based on your specific situation
- **Rate monitoring** - Alerting you to favorable changes
- **Timeline coordination** - Ensuring smooth closing process
- **Problem solving** - Addressing issues that arise

**Red Flags I Help You Avoid:**
- Adjustable rates without understanding risks
- Lenders with poor closing track records
- Excessive fees and closing costs
- Loan programs that don't fit your situation

**Current Market Advice:**
- **Rates are stabilizing** - Good time to lock when you find your home
- **Shop aggressively** - Small rate differences add up over 30 years
- **Consider points** - Paying upfront for lower rate may make sense
- **Plan for the long term** - Most people keep loans 7-10 years

**Ready to get pre-approved?** I'll connect you with the right lender for your situation and help you navigate the entire financing process! 🏦"""
        
        elif any(word in query_lower for word in ['rent', 'rental', 'lease']):
            return """🏠 **Rental Market Expertise - Your Leasing Specialist:**

**As your rental agent, I help both tenants find perfect homes and landlords find quality tenants:**

**For Renters - Finding Your Perfect Home:**

**Current Rental Market:**
- **Inventory levels** - Good selection in most price ranges
- **Rent trends** - Stabilizing after recent increases
- **Seasonal patterns** - Best selection in spring/summer
- **Competition** - Quality properties still move quickly

**Rental Search Strategy:**
**Budget Planning:**
- **30% rule** - Rent shouldn't exceed 30% of gross income
- **Additional costs** - Utilities, parking, pet fees, renter's insurance
- **Security deposits** - Typically 1-2 months rent
- **Application fees** - Budget $50-100 per application

**Property Types I Show:**
- **Apartments** - Amenities, maintenance included, community features
- **Single-family homes** - Privacy, yard space, more storage
- **Townhomes** - Balance of space and convenience
- **Condos** - Modern amenities, often newer construction

**Lease Negotiation:**
- **Rent amount** - Market analysis for fair pricing
- **Lease terms** - Length, renewal options, early termination
- **Pet policies** - Fees, deposits, breed restrictions
- **Maintenance responsibilities** - What's included vs. tenant responsibility

**For Property Owners - Maximizing Your Investment:**

**Rental Property Management:**
**Market Analysis:**
- **Competitive rent pricing** - Maximizing income while minimizing vacancy
- **Property positioning** - Highlighting unique features and benefits
- **Seasonal timing** - Optimal listing and lease renewal timing
- **Market trends** - Staying ahead of rental market changes

**Tenant Screening:**
- **Credit checks** - Financial responsibility verification
- **Income verification** - 3x rent income requirement
- **Employment history** - Stability and reliability
- **Previous landlord references** - Rental history and behavior

**Property Preparation:**
- **Staging for rentals** - Making properties show well
- **Maintenance priorities** - Cost-effective improvements
- **Photography** - Professional listing photos
- **Marketing strategy** - Maximum exposure to qualified tenants

**Lease Management:**
- **Legal compliance** - Fair housing laws, local regulations
- **Lease documentation** - Protecting your interests
- **Security deposit handling** - Proper procedures and documentation
- **Renewal strategies** - Retaining good tenants

**Rent vs. Buy Analysis:**
**When Renting Makes Sense:**
- **Short-term plans** - Moving within 2-3 years
- **Financial flexibility** - Preserving capital for other investments
- **Maintenance-free living** - No repair responsibilities
- **Location flexibility** - Easier to relocate for opportunities

**When Buying Makes Sense:**
- **Long-term stability** - Planning to stay 5+ years
- **Building equity** - Monthly payments build ownership
- **Tax benefits** - Mortgage interest and property tax deductions
- **Control and customization** - Make it truly your own

**My Rental Services:**

**For Tenants:**
- **Property search** - Finding homes that match your criteria
- **Market insights** - Rental rates and neighborhood information
- **Application assistance** - Strengthening your rental application
- **Lease review** - Understanding terms and protecting your interests

**For Landlords:**
- **Property marketing** - Professional listing and promotion
- **Tenant screening** - Finding qualified, reliable renters
- **Lease preparation** - Legal compliance and protection
- **Market analysis** - Optimal pricing and positioning

**Current Opportunities:**
- **Corporate relocations** - Temporary housing needs
- **Luxury rentals** - High-end market showing strength
- **Pet-friendly properties** - High demand, premium pricing
- **Short-term furnished** - Business travelers and temporary assignments

**My Commitment:**
Whether you're looking to rent or lease out a property, I provide professional service focused on your specific needs and goals.

**Ready to explore rental options?** Let's discuss your situation and find the perfect rental solution! 🔑"""
        
        else:
            return """🏡 **Your Trusted Real Estate Partner - Complete Market Expertise:**

**Welcome! As your dedicated real estate agent, I'm here to guide you through every aspect of your property journey:**

**My Full-Service Real Estate Expertise:**

**For Home Buyers:**
- **Market analysis** - Current inventory, pricing trends, neighborhood insights
- **Property search** - Finding homes that match your criteria and budget
- **Buyer representation** - Negotiating the best price and terms
- **Transaction management** - Coordinating inspections, appraisals, and closing

**For Home Sellers:**
- **Property valuation** - Accurate pricing based on current market conditions
- **Marketing strategy** - Professional photography, staging, and promotion
- **Seller representation** - Maximizing your sale price and protecting your interests
- **Closing coordination** - Managing all details through successful completion

**For Investors:**
- **Investment analysis** - Cash flow projections, ROI calculations
- **Market opportunities** - Identifying undervalued properties and emerging areas
- **Rental market expertise** - Understanding tenant demand and rental rates
- **Portfolio strategy** - Building and managing real estate investments

**Current Market Insights:**
**Buyer's Market Indicators:**
- Increased inventory levels
- Longer days on market
- More negotiating power for buyers
- Opportunity for favorable terms

**Seller's Market Indicators:**
- Limited inventory
- Quick sales and multiple offers
- Strong price appreciation
- Favorable conditions for sellers

**Interest Rate Impact:**
- Current rates affecting affordability
- Refinancing opportunities for existing homeowners
- First-time buyer programs and assistance
- Investment property financing options

**My Local Market Specialties:**
**Neighborhood Expertise:**
- **School districts** - Ratings, boundaries, and family-friendly communities
- **Commuter areas** - Access to employment centers and transportation
- **Investment zones** - Emerging areas with growth potential
- **Luxury markets** - High-end properties and exclusive communities

**Property Types:**
- **Single-family homes** - Traditional neighborhoods and new construction
- **Condominiums** - Urban living and low-maintenance lifestyles
- **Townhomes** - Balance of space and convenience
- **Investment properties** - Rental income and appreciation potential

**My Professional Services:**

**Market Analysis:**
- **Comparative Market Analysis (CMA)** - Accurate property valuations
- **Neighborhood reports** - Demographics, amenities, and trends
- **Investment analysis** - Cash flow and return projections
- **Market timing** - Optimal buying and selling strategies

**Transaction Support:**
- **Contract negotiation** - Protecting your interests and maximizing value
- **Inspection coordination** - Ensuring property condition and value
- **Financing assistance** - Connecting you with trusted lenders
- **Closing management** - Smooth transaction completion

**Client Education:**
- **First-time buyer guidance** - Step-by-step process education
- **Market updates** - Regular insights on conditions and opportunities
- **Investment strategies** - Building wealth through real estate
- **Legal compliance** - Understanding contracts and regulations

**My Commitment to Excellence:**
- **Local expertise** - Deep knowledge of our market and communities
- **Professional network** - Trusted relationships with lenders, inspectors, contractors
- **Personal attention** - Your goals are my priority
- **Proven results** - Track record of successful transactions

**Technology and Marketing:**
- **Professional photography** - Showcasing properties at their best
- **Online marketing** - Maximum exposure through all digital channels
- **Virtual tours** - Convenient viewing for busy schedules
- **Market analytics** - Data-driven pricing and strategy decisions

**Why Choose Me as Your Agent:**
- **Experience** - Years of successful transactions in our local market
- **Knowledge** - Continuous education and market expertise
- **Integrity** - Honest advice and transparent communication
- **Results** - Proven track record of achieving client goals

**Current Opportunities:**
- **First-time buyer programs** - Down payment assistance and favorable terms
- **Move-up buyers** - Leveraging equity for larger homes
- **Downsizing** - Right-sizing for retirement or lifestyle changes
- **Investment properties** - Building wealth through real estate

**Ready to Make Your Move?**
Whether you're buying your first home, selling to upgrade, or building an investment portfolio, I'm here to make your real estate goals a reality.

**Let's schedule a consultation** to discuss your specific needs and create a personalized strategy for success! 🎯

**What brings you to the real estate market today?** I'm excited to help you achieve your property goals! 🌟"""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for real estate queries."""
        query_lower = query.lower()
        client = context['client_profile']
        financial = context['financial_profile']
        preferences = context['property_preferences']
        situation = context['current_situation']
        market = context['market_context']
        experience = context['experience_and_history']
        
        if any(word in query_lower for word in ['buy', 'buying', 'purchase', 'first time']):
            return f"""🏠 **Personalized Home Buying Plan for {client['name']}:**

**Your Buyer Profile:**
- {"First-time buyer" if experience['first_time_buyer'] else "Experienced buyer"} ({experience['real_estate_knowledge']} level)
- Budget: {preferences['price_range']} (based on {financial['annual_income']} income)
- {"✅ Pre-approved" if financial['pre_approved'] else "⚠️ Need pre-approval"} | Credit Score: {financial['credit_score']}
- Down Payment Available: ${financial['down_payment_available']:,}

**Perfect Property Match:**
- **Type:** {preferences['property_type']} with {preferences['bedrooms']} bed/{preferences['bathrooms']} bath
- **Size:** {preferences['square_footage']} sq ft
- **Must-Haves:** {', '.join(preferences['must_haves'])}
- **Avoid:** {', '.join(preferences['deal_breakers'])}

**Market Advantage Strategy:**
- **Current Market:** {market['local_market']} (avg {market['average_days_on_market']} days on market)
- **Your Timeline:** {situation['timeline']} (reason: {situation['urgency_reason']})
- **Interest Rate:** {market['interest_rates']} ({"act quickly - rates rising" if market['price_trend'] == 'Rising' else "good timing"})

**Location Focus:**
- **Preferred Areas:** {', '.join(preferences['preferred_areas'])}
- **Commute:** Max {situation['commute_requirements']['max_commute']} to {situation['commute_requirements']['work_location']}
- **Transportation:** {situation['commute_requirements']['transportation']}

**Next Steps:**
1. {"Complete pre-approval process" if not financial['pre_approved'] else "✅ Pre-approval complete"}
2. Schedule showings in {preferences['preferred_areas'][0]} area
3. {"Move quickly - seller's market!" if market['local_market'] == "Seller's market" else "Take time to evaluate - buyer's market"}

**Financing Estimate:**
- Monthly Payment: ~${int((self._parse_price_range(preferences['price_range']) * 0.8) * 0.006):,} (estimated)
- Down Payment: ${financial['down_payment_available']:,} ({int(financial['down_payment_available'] / (self._parse_price_range(preferences['price_range']) / 100)) if financial['down_payment_available'] > 0 else 0}% down)

Ready to start your home search? 🔑"""
        
        elif any(word in query_lower for word in ['sell', 'selling', 'worth', 'value']):
            return f"""💰 **Home Valuation & Selling Strategy for {client['name']}:**

**Market Analysis for Your Area:**
- **Market Type:** {market['local_market']} 
- **Price Trend:** {market['price_trend']} 
- **Average Days on Market:** {market['average_days_on_market']} days
- **Inventory:** {market['inventory_level']} supply

**Your Selling Situation:**
- **Timeline:** {situation['timeline']} (reason: {situation['urgency_reason']})
- **Current Housing:** {situation['current_housing']}
- **Experience Level:** {experience['real_estate_knowledge']}

**Estimated Home Value Range:**
Based on {preferences['property_type']} properties in {client['location']}:
- **Conservative Estimate:** {preferences['price_range'].split('-')[0]} 
- **Market Value:** {preferences['price_range']}
- **Optimistic (if staged well):** {preferences['price_range'].split('-')[1] if '-' in preferences['price_range'] else preferences['price_range']}

**Selling Strategy:**
{"**Quick Sale Approach** (due to your timeline):" if situation['timeline'] in ['ASAP', 'Within 3 months'] else "**Maximum Value Approach:**"}
- Price at {95 if situation['timeline'] == 'ASAP' else 98 if situation['timeline'] == 'Within 3 months' else 102}% of market value
- {"Minimal staging, sell as-is" if situation['timeline'] == 'ASAP' else "Professional staging recommended"}
- {"Accept first reasonable offer" if situation['timeline'] == 'ASAP' else "Negotiate for best terms"}

**Market Advantages:**
- {market['local_market']} favors {"you as seller!" if market['local_market'] == "Seller's market" else "buyers (price competitively)"}
- {market['seasonal_factor']} - {"great timing!" if market['seasonal_factor'] == 'Peak season' else "consider timing"}

**Preparation Checklist:**
1. Professional market analysis (CMA)
2. {"Quick repairs only" if situation['timeline'] == 'ASAP' else "Strategic improvements for ROI"}
3. Professional photography
4. {"Price aggressively for quick sale" if situation['timeline'] == 'ASAP' else "Strategic pricing for maximum value"}

**Net Proceeds Estimate:**
- Sale Price: {preferences['price_range']}
- Closing Costs: ~6-8% of sale price
- Your Net: ~92-94% of sale price

Ready to get your home on the market? 📈"""
        
        elif any(word in query_lower for word in ['school', 'district', 'education']):
            return f"""🎓 **School District Home Search for {client['name']}:**

**Your Family Profile:**
- Family Status: {client['family_status']}
- Looking for: {preferences['bedrooms']} bedroom {preferences['property_type']}
- Budget: {preferences['price_range']}
- Timeline: {situation['timeline']}

**Top School Districts in Your Area:**
Based on your {preferences['preferred_areas']} preferences:

🌟 **Excellent Districts (9-10 rated):**
- Premium pricing: +15-25% above market
- High demand, low inventory
- Strong resale values

⭐ **Very Good Districts (7-8 rated):**
- Moderate premium: +5-15% above market
- Good balance of value and quality
- **Recommended for your budget**

**Property Recommendations:**
- **Sweet Spot:** {preferences['property_type']} in Very Good districts
- **Target Areas:** {preferences['preferred_areas'][1]} (excellent schools, reasonable prices)
- **Commute Factor:** {situation['commute_requirements']['max_commute']} to {situation['commute_requirements']['work_location']}

**Market Reality Check:**
- **Current Market:** {market['local_market']}
- **School District Homes:** {"Move fast - high demand!" if market['local_market'] == "Seller's market" else "Good selection available"}
- **Your Advantage:** {"Pre-approved" if financial['pre_approved'] else "Get pre-approved first"} with {financial['credit_score']} credit score

**Budget Impact:**
- Base Price Range: {preferences['price_range']}
- School Premium: +$20k-50k for top districts
- **Realistic Budget:** Adjust to {preferences['price_range'].split('-')[1] if '-' in preferences['price_range'] else preferences['price_range']} for best schools

**Action Plan:**
1. Research specific school boundaries
2. Visit schools during your home tours
3. Consider future school changes/redistricting
4. {"Act quickly on good properties" if market['local_market'] == "Seller's market" else "Take time to compare options"}

**Family-Friendly Features to Prioritize:**
- {', '.join([f for f in preferences['must_haves'] if f in ['Yard', 'Garage', 'Home office']])}
- Safe neighborhood with sidewalks
- Proximity to parks and activities

Your children's education is worth the investment! 📚"""
        
        elif any(word in query_lower for word in ['mortgage', 'rate', 'financing', 'loan']):
            return f"""💳 **Personalized Financing Analysis for {client['name']}:**

**Your Financial Profile:**
- Annual Income: {financial['annual_income']}
- Credit Score: {financial['credit_score']} ({"Excellent" if financial['credit_score'] >= 740 else "Good" if financial['credit_score'] >= 670 else "Fair - room for improvement"})
- Down Payment: ${financial['down_payment_available']:,}
- Debt-to-Income: {financial['debt_to_income']}
- {"✅ Pre-approved" if financial['pre_approved'] else "❌ Need pre-approval"}

**Current Market Rates** (based on your {financial['credit_score']} credit score):
- **30-Year Fixed:** {market['interest_rates']} 
- **15-Year Fixed:** {float(market['interest_rates'].replace('%', '')) - 0.5:.2f}%
- **5/1 ARM:** {float(market['interest_rates'].replace('%', '')) - 0.75:.2f}%

**Loan Options for You:**
{"**Conventional Loan** (Recommended):" if financial['down_payment_available'] >= 50000 else "**FHA Loan** (3.5% down):"}
- Down Payment: {f"${financial['down_payment_available']:,} ({int(financial['down_payment_available'] / (self._parse_price_range(preferences['price_range']) / 100))}%)" if financial['down_payment_available'] >= 50000 else "As low as 3.5%"}
- {"No PMI required" if financial['down_payment_available'] >= 50000 else "PMI required (removable later)"}
- Rate: {market['interest_rates']}

**Monthly Payment Breakdown** (for {preferences['price_range']} home):
- Principal & Interest: ${int(self._parse_price_range(preferences['price_range']) * 0.006):,}
- Property Tax: ${int(self._parse_price_range(preferences['price_range']) * 0.012 / 12):,}
- Insurance: ${int(self._parse_price_range(preferences['price_range']) * 0.004 / 12):,}
- **Total Monthly:** ${int(self._parse_price_range(preferences['price_range']) * 0.022):,}

**Affordability Analysis:**
- Income Required: {financial['annual_income']} ✅
- DTI Impact: {financial['debt_to_income']} ({"Good" if int(financial['debt_to_income'].replace('%', '')) < 36 else "Monitor closely"})
- **Comfortable Budget:** {preferences['price_range']}

**Rate Lock Strategy:**
- **Current Trend:** {market['price_trend']} rates
- **Recommendation:** {"Lock rate immediately" if market['price_trend'] == 'Rising' else "Monitor for better rates"}
- **Timeline:** {situation['timeline']} gives you {"urgency to act" if situation['timeline'] in ['ASAP', 'Within 3 months'] else "time to shop"}

**Next Steps:**
1. {"Complete pre-approval process" if not financial['pre_approved'] else "✅ Pre-approval complete"}
2. Shop with 2-3 lenders for best rate
3. Consider rate lock timing
4. {"Move quickly - rates may rise" if market['price_trend'] == 'Rising' else "Take time to find best deal"}

Your financing looks strong for your target price range! 💪"""
        
        else:
            return f"""🏡 **Comprehensive Real Estate Analysis for {client['name']}:**

**Your Profile:**
- **Client Type:** {client['client_type']} ({experience['real_estate_knowledge']} level)
- **Location:** {client['location']}
- **Timeline:** {situation['timeline']} (reason: {situation['urgency_reason']})
- **Budget:** {preferences['price_range']}

**Current Market Conditions:**
- **Market Type:** {market['local_market']}
- **Inventory:** {market['inventory_level']} supply
- **Price Trend:** {market['price_trend']}
- **Average DOM:** {market['average_days_on_market']} days
- **Interest Rates:** {market['interest_rates']}

**Your Ideal Property:**
- **Type:** {preferences['property_type']}
- **Size:** {preferences['bedrooms']} bed/{preferences['bathrooms']} bath, {preferences['square_footage']} sq ft
- **Must-Haves:** {', '.join(preferences['must_haves'])}
- **Preferred Areas:** {', '.join(preferences['preferred_areas'])}

**Financial Readiness:**
- **Income:** {financial['annual_income']}
- **Credit Score:** {financial['credit_score']}
- **Down Payment:** """ + (f"${financial['down_payment_available']:,}" if financial['down_payment_available'] else "TBD") + f"""
- {"✅ Pre-approved" if financial['pre_approved'] else "⚠️ Need pre-approval"}

**Market Strategy:**
{"**Buyer's Advantage:**" if market['local_market'] == "Buyer's market" else "**Seller's Market - Act Fast:**" if market['local_market'] == "Seller's market" else "**Balanced Market:**"}
- {"Take time to negotiate" if market['local_market'] == "Buyer's market" else "Be prepared to compete" if market['local_market'] == "Seller's market" else "Standard market conditions"}
- {"Multiple offers likely" if market['local_market'] == "Seller's market" else "Room for negotiation" if market['local_market'] == "Buyer's market" else "Fair negotiations expected"}

**Commute Considerations:**
- **Work Location:** {situation['commute_requirements']['work_location']}
- **Max Commute:** {situation['commute_requirements']['max_commute']}
- **Transportation:** {situation['commute_requirements']['transportation']}

**Immediate Action Items:**
1. {"Complete pre-approval" if not financial['pre_approved'] else "✅ Financing ready"}
2. {"Schedule immediate showings" if situation['timeline'] == 'ASAP' else "Begin property search"}
3. {"Prepare for quick decisions" if market['local_market'] == "Seller's market" else "Take time to evaluate options"}

**Success Factors:**
- Your {experience['real_estate_knowledge']} experience level {"is an advantage" if experience['real_estate_knowledge'] in ['Experienced', 'Expert'] else "means we'll guide you through the process"}
- {financial['credit_score']} credit score {"gives you excellent options" if financial['credit_score'] >= 740 else "provides good financing options"}
- {situation['timeline']} timeline {"requires immediate action" if situation['timeline'] == 'ASAP' else "allows for strategic planning"}

Ready to make your real estate goals a reality? 🎯"""