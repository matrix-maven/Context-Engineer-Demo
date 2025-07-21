"""
Financial Services Demo Module

Implements the financial services industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo

fake = Faker()


class FinancialDemo(BaseDemo):
    """Financial services assistant demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        from services.prompt_service import Industry
        super().__init__("Financial Services", Industry.FINANCIAL, ai_service, context_service)
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic financial services context using Faker."""
        return {
            "customer_profile": {
                "name": fake.name(),
                "age": random.randint(25, 65),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "customer_since": fake.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d'),
                "relationship_tier": random.choice(["Basic", "Preferred", "Premier", "Private"])
            },
            "financial_status": {
                "employment": random.choice(["Employed", "Self-employed", "Retired", "Student"]),
                "annual_income": random.choice(["$30k-50k", "$50k-75k", "$75k-100k", "$100k-150k", "$150k+"]),
                "credit_score": random.randint(650, 850),
                "debt_to_income": f"{random.randint(15, 45)}%",
                "homeowner": random.choice([True, False])
            },
            "current_accounts": {
                "checking_balance": random.randint(500, 15000),
                "savings_balance": random.randint(1000, 50000),
                "credit_cards": random.randint(1, 4),
                "total_credit_limit": random.randint(5000, 50000),
                "investment_accounts": random.randint(0, 3),
                "loans": random.sample(["Auto loan", "Mortgage", "Personal loan", "Student loan"], random.randint(0, 2))
            },
            "financial_goals": {
                "primary_goals": random.sample([
                    "Retirement planning", "Home purchase", "Emergency fund", 
                    "Debt consolidation", "Investment growth", "Education funding"
                ], random.randint(2, 3)),
                "time_horizon": random.choice(["Short-term (1-2 years)", "Medium-term (3-7 years)", "Long-term (8+ years)"]),
                "risk_tolerance": random.choice(["Conservative", "Moderate", "Aggressive"]),
                "monthly_savings_capacity": random.randint(200, 2000)
            },
            "recent_activity": {
                "last_login": fake.date_between(start_date='-7d', end_date='today').strftime('%Y-%m-%d'),
                "recent_transactions": random.randint(15, 45),
                "monthly_spending": random.randint(2000, 8000),
                "top_spending_categories": random.sample([
                    "Groceries", "Gas", "Restaurants", "Utilities", "Shopping", "Healthcare"
                ], 3),
                "alerts_enabled": random.choice([True, False])
            },
            "service_preferences": {
                "preferred_contact": random.choice(["Email", "Phone", "Text", "In-person"]),
                "digital_adoption": random.choice(["High", "Medium", "Low"]),
                "advisor_relationship": random.choice(["Self-directed", "Occasional guidance", "Regular advisor"]),
                "communication_frequency": random.choice(["Weekly", "Monthly", "Quarterly", "As needed"])
            }
        }
    
    def get_sample_queries(self) -> List[str]:
        """Get sample financial services queries."""
        return [
            "How can I improve my credit score?",
            "I want to invest for retirement",
            "Should I refinance my mortgage?",
            "Help me create a budget",
            "What's the best savings account?"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for financial queries."""
        return "e.g., How can I improve my credit score?, I want to invest for retirement"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic financial responses."""
        return "You are a helpful financial advisor. Provide general financial advice and information without using specific customer context. Always recommend consulting with financial professionals for personalized advice."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual financial responses."""
        return """You are a personalized financial advisor. Use the provided customer context to give specific, relevant financial guidance. Consider:
- Current financial status and account balances
- Credit score and debt situation
- Financial goals and risk tolerance
- Age and time horizon for investments
- Existing accounts and relationship history

Provide actionable, personalized advice while emphasizing the importance of professional financial planning."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for financial queries."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['credit', 'score', 'improve']):
            return """💳 **Credit Score Improvement Strategy:**

**Your credit score is crucial for your financial future. Here's my professional guidance:**

**The 5 Pillars of Credit Health:**
1. **Payment History (35%)** - Never miss a payment, even minimums
2. **Credit Utilization (30%)** - Keep balances below 30% of limits, ideally under 10%
3. **Credit Age (15%)** - Keep old accounts open to maintain history length
4. **Credit Mix (10%)** - Have a healthy mix of credit cards, loans, etc.
5. **New Credit (10%)** - Limit hard inquiries, space out new applications

**My Action Plan for You:**
- **Immediate (30 days):** Set up autopay for all accounts
- **Short-term (3-6 months):** Pay down high balances, dispute errors
- **Long-term (6+ months):** Build positive payment history, optimize utilization

**Pro Tips from My Experience:**
- Pay twice monthly to keep utilization low
- Request credit limit increases (don't use them)
- Consider becoming an authorized user on family member's account
- Use credit monitoring to track progress

**Expected Timeline:** Most clients see 50-100 point improvements within 6-12 months with consistent effort.

⚠️ **Important:** Avoid credit repair scams. Legitimate improvement takes time and discipline. I'm here to guide you through the process with proven strategies."""
        
        elif any(word in query_lower for word in ['invest', 'retirement', '401k', 'ira']):
            return """📈 **Retirement Investment Guidance:**

**Time is your greatest asset in retirement planning. Let me help you maximize it:**

**My Investment Philosophy:**
- **Start NOW** - Even $50/month beats waiting for the "perfect" amount
- **Employer match first** - It's free money, always take the full match
- **Tax-advantaged accounts** - 401(k), IRA, Roth IRA are your best friends
- **Diversification** - Don't put all eggs in one basket
- **Stay the course** - Market volatility is normal, consistency wins

**Your Retirement Roadmap:**
1. **Foundation:** Emergency fund (3-6 months expenses)
2. **Priority 1:** 401(k) up to employer match
3. **Priority 2:** Max out Roth IRA ($6,500/year, $7,500 if 50+)
4. **Priority 3:** Max out 401(k) ($22,500/year, $30,000 if 50+)
5. **Advanced:** Taxable investment accounts

**Asset Allocation by Age (Rule of Thumb):**
- **20s-30s:** 80-90% stocks, 10-20% bonds
- **40s:** 70-80% stocks, 20-30% bonds  
- **50s:** 60-70% stocks, 30-40% bonds
- **60s+:** 50-60% stocks, 40-50% bonds

**The Power of Compound Interest:**
- $300/month starting at 25 = $1.2M at 65
- $300/month starting at 35 = $600K at 65
- Starting 10 years earlier doubles your retirement wealth!

**My recommendation:** Start with target-date funds if you're unsure about allocation. They automatically adjust as you age.

💡 **Remember:** I'm here to help you create a personalized strategy based on your specific goals and timeline."""
        
        elif any(word in query_lower for word in ['mortgage', 'refinance', 'home', 'loan']):
            return """🏠 **Mortgage & Home Financing Guidance:**

**Buying a home is likely your largest financial decision. Let me guide you through it:**

**Current Market Reality:**
- **Interest rates:** Currently elevated but still historically reasonable
- **Home prices:** Vary significantly by location and market conditions
- **Competition:** Varies by market - be prepared to act quickly in hot markets

**My Mortgage Strategy for You:**
1. **Pre-approval first** - Know your budget before shopping
2. **20% down payment ideal** - Avoids PMI, better rates, stronger offers
3. **Debt-to-income under 36%** - Ensures comfortable payments
4. **Shop multiple lenders** - Rates and terms can vary significantly

**Refinancing Considerations:**
- **Rate improvement:** Generally need 0.75%+ improvement to justify costs
- **Break-even analysis:** Calculate months to recoup closing costs
- **Loan term decisions:** 15-year saves interest, 30-year provides flexibility
- **Cash-out refinancing:** Can be smart for home improvements or debt consolidation

**First-Time Buyer Programs:**
- **FHA loans:** 3.5% down, more flexible credit requirements
- **VA loans:** 0% down for eligible veterans
- **USDA loans:** 0% down in eligible rural areas
- **State/local programs:** Down payment assistance, tax credits

**My Professional Advice:**
- **Buy what you can afford long-term** - Don't stretch for the maximum
- **Factor in maintenance costs** - Budget 1-3% of home value annually
- **Consider total cost of ownership** - Taxes, insurance, HOA, utilities
- **Location matters most** - You can renovate a house, not a neighborhood

**Red Flags to Avoid:**
- Adjustable rates without understanding risks
- Interest-only loans
- Borrowing from retirement for down payment
- Skipping home inspection to win bidding wars

I'm here to help you navigate this complex process and make the best decision for your financial future."""
        
        elif any(word in query_lower for word in ['budget', 'budgeting', 'expenses']):
            return """💰 **Personal Budgeting Strategy:**

**A budget isn't about restriction - it's about giving every dollar a purpose. Let me show you how:**

**My Proven Budgeting Framework:**
**50/30/20 Rule (Starting Point):**
- **50% Needs:** Housing, utilities, groceries, minimum debt payments
- **30% Wants:** Dining out, entertainment, hobbies, shopping
- **20% Savings & Debt:** Emergency fund, retirement, extra debt payments

**Step-by-Step Budget Creation:**
1. **Track everything for 30 days** - Use apps like Mint, YNAB, or simple spreadsheet
2. **Categorize expenses** - Fixed vs. variable, needs vs. wants
3. **Identify spending leaks** - Small recurring charges add up quickly
4. **Set realistic targets** - Drastic cuts usually fail
5. **Automate savings** - Pay yourself first, before you can spend it

**My Budget Optimization Tips:**
- **Housing under 30%** - Biggest expense, biggest opportunity
- **Transportation under 15%** - Consider total cost of car ownership
- **Food budget reality check** - Groceries vs. dining out balance
- **Subscription audit** - Cancel unused services (average person has $273/month)

**Emergency Fund Priority:**
- **Start with $1,000** - Covers most small emergencies
- **Build to 3-6 months expenses** - Full financial security
- **Keep in high-yield savings** - Accessible but earning interest

**Debt Elimination Strategy:**
- **List all debts** - Balance, minimum payment, interest rate
- **Choose method:** Avalanche (highest rate first) or Snowball (smallest balance first)
- **Pay minimums on all, extra on target debt**
- **Celebrate milestones** - Debt freedom is worth celebrating!

**Budget Success Secrets:**
- **Review monthly** - Adjust as life changes
- **Use cash for problem categories** - Physical money creates awareness
- **Plan for irregular expenses** - Car maintenance, gifts, vacations
- **Include fun money** - Budgets need breathing room

**Technology Tools I Recommend:**
- **Mint:** Free, comprehensive tracking
- **YNAB:** Zero-based budgeting philosophy
- **Personal Capital:** Great for investment tracking
- **Bank apps:** Most have built-in budgeting features

Remember: The best budget is the one you'll actually follow. Start simple and refine over time."""
        
        elif any(word in query_lower for word in ['savings', 'account', 'interest']):
            return """💵 **Savings Strategy & Account Selection:**

**Your savings strategy should match your goals and timeline. Let me help you optimize:**

**Savings Account Hierarchy:**
1. **Emergency Fund** - High-yield savings, 3-6 months expenses
2. **Short-term goals** - CDs or high-yield savings (1-3 years)
3. **Medium-term goals** - Conservative investments (3-7 years)
4. **Long-term goals** - Growth investments (7+ years)

**Current High-Yield Savings Options:**
- **Online banks:** 4.0-5.0% APY (Marcus, Ally, Capital One 360)
- **Credit unions:** Often competitive rates with local service
- **Traditional banks:** Usually lower rates but convenient if you need branches
- **Money market accounts:** Slightly higher rates, limited transactions

**My Account Selection Criteria:**
- **FDIC insured** - Non-negotiable for safety
- **No monthly fees** - Your money should grow, not shrink
- **Easy access** - Online/mobile banking, ATM network
- **Competitive rates** - Shop around, rates change frequently
- **Minimum balance requirements** - Make sure you can maintain them

**Savings Strategies I Recommend:**
**The 1% Rule:** Increase your savings rate by 1% each year
**Pay Yourself First:** Automate transfers on payday
**Round-Up Programs:** Save spare change automatically
**Separate Goals:** Different accounts for different purposes

**Certificate of Deposit (CD) Strategy:**
- **CD Ladder:** Multiple CDs with staggered maturity dates
- **Current rates:** 4.5-5.5% for 1-5 year terms
- **Best for:** Money you won't need for specific timeframe
- **Consider:** Early withdrawal penalties vs. potential rate changes

**Money Market vs. Savings:**
- **Money Market:** Higher rates, limited transactions, check writing
- **Savings:** Lower rates, unlimited online transfers, simpler
- **My advice:** High-yield savings for most people, money market for larger balances

**Advanced Savings Tactics:**
- **I Bonds:** Government bonds, inflation-protected, 10.12% current rate
- **Treasury Bills:** Short-term government securities, competitive rates
- **Brokerage sweep accounts:** Higher rates, FDIC insured through program banks

**Savings Goals Framework:**
- **Emergency fund:** 3-6 months expenses (priority #1)
- **House down payment:** 20% of home price + closing costs
- **Car replacement:** Avoid financing by saving ahead
- **Vacation fund:** Enjoy guilt-free travel with dedicated savings
- **Holiday/gift fund:** Spread seasonal expenses throughout the year

**Red Flags to Avoid:**
- Accounts with monthly fees
- Teaser rates that drop after introductory period
- Complicated requirements to earn advertised rate
- Non-FDIC insured accounts (unless you understand the risks)

The key is matching your savings vehicle to your timeline and risk tolerance. I'm here to help you create a comprehensive savings strategy."""
        
        else:
            return """💼 **Comprehensive Financial Wellness Guidance:**

**Welcome! As your financial advisor, I'm here to help you build lasting financial security. Let's start with the fundamentals:**

**Your Financial Health Checkup:**
**Foundation Level:**
- ✅ **Emergency Fund:** 3-6 months of expenses in high-yield savings
- ✅ **Budget Control:** Know where every dollar goes, live below your means
- ✅ **Debt Management:** Pay minimums on all debts, attack highest interest first
- ✅ **Credit Health:** Score above 700, utilization below 30%

**Growth Level:**
- 📈 **Retirement Savings:** 10-15% of income, maximize employer match
- 🏠 **Homeownership:** If it makes sense for your situation and market
- 💰 **Investment Portfolio:** Diversified, age-appropriate allocation
- 🛡️ **Insurance Protection:** Health, disability, life insurance as needed

**Wealth Building Level:**
- 🎯 **Tax Optimization:** Max out tax-advantaged accounts
- 🏢 **Real Estate Investment:** Consider after mastering basics
- 📊 **Advanced Investing:** Individual stocks, bonds, alternative investments
- 🎓 **Estate Planning:** Wills, trusts, beneficiary designations

**My Core Financial Principles:**
1. **Pay Yourself First** - Automate savings before you can spend
2. **Time in Market > Timing the Market** - Consistency beats perfection
3. **Diversification is Protection** - Don't put all eggs in one basket
4. **Compound Interest is Magic** - Start early, be patient
5. **Knowledge is Power** - Understand before you invest

**Common Financial Mistakes I Help Clients Avoid:**
- Lifestyle inflation with every raise
- Emotional investing decisions
- Inadequate emergency funds
- Ignoring employer 401(k) match
- Paying only minimums on high-interest debt
- Procrastinating on retirement planning

**Your Next Steps:**
1. **Assessment:** Where are you now financially?
2. **Goals:** What do you want to achieve and when?
3. **Strategy:** Create a personalized plan to get there
4. **Implementation:** Take action with proper guidance
5. **Monitoring:** Regular check-ins and adjustments

**Areas I Can Help You With:**
- **Budgeting & Cash Flow Management**
- **Debt Elimination Strategies**
- **Retirement Planning & Investment Allocation**
- **Home Buying & Mortgage Guidance**
- **Tax Planning & Optimization**
- **Insurance Needs Analysis**
- **Estate Planning Basics**

**My Promise to You:**
I'll provide honest, straightforward advice focused on your best interests. No product sales, no hidden agendas - just professional guidance to help you achieve financial independence.

**What's your biggest financial concern or goal right now?** Let's create a plan to address it together. 🎯

Remember: Building wealth is a marathon, not a sprint. I'm here to guide you every step of the way."""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for financial queries."""
        query_lower = query.lower()
        customer = context['customer_profile']
        financial = context['financial_status']
        accounts = context['current_accounts']
        goals = context['financial_goals']
        activity = context['recent_activity']
        prefs = context['service_preferences']
        
        if any(word in query_lower for word in ['credit', 'score', 'improve']):
            return f"""🎯 **Credit Improvement Plan for {customer['name']}:**

**Your Current Situation:**
- Credit Score: {financial['credit_score']} ({"Excellent" if financial['credit_score'] >= 800 else "Good" if financial['credit_score'] >= 700 else "Fair"})
- Total Credit Limit: ${accounts['total_credit_limit']:,}
- Debt-to-Income: {financial['debt_to_income']}

**Personalized Action Plan:**
1. **Immediate (30 days):**
   - Pay down credit cards to under 30% utilization
   - Set up autopay for all accounts (prevent late payments)

2. **Short-term (3-6 months):**
   - Target utilization under 10% for score boost
   - Request credit limit increases on existing cards

3. **Long-term:**
   - Keep oldest accounts open (you've been with us since {customer['customer_since']})
   - Monitor monthly with free credit reports

**{customer['relationship_tier']} Member Benefits:**
- Free credit monitoring
- Personalized credit coaching sessions
- Priority customer service

Would you like to schedule a credit consultation?"""
        
        elif any(word in query_lower for word in ['invest', 'retirement', '401k', 'ira']):
            return f"""🎯 **Retirement Strategy for {customer['name']} (Age {customer['age']}):**

**Your Investment Profile:**
- Risk Tolerance: {goals['risk_tolerance']}
- Time Horizon: {goals['time_horizon']}
- Monthly Savings Capacity: ${goals['monthly_savings_capacity']}
- Current Investment Accounts: {accounts['investment_accounts']}

**Personalized Recommendations:**

1. **Immediate Priority:**
   - Maximize employer 401(k) match (free money!)
   - Consider Roth IRA (${6500 if customer['age'] < 50 else 7500} annual limit)

2. **Portfolio Allocation** ({goals['risk_tolerance']} approach):
   - Stocks: {70 if goals['risk_tolerance'] == 'Aggressive' else 60 if goals['risk_tolerance'] == 'Moderate' else 40}%
   - Bonds: {20 if goals['risk_tolerance'] == 'Aggressive' else 30 if goals['risk_tolerance'] == 'Moderate' else 50}%
   - International: {10 if goals['risk_tolerance'] == 'Aggressive' else 10 if goals['risk_tolerance'] == 'Moderate' else 10}%

3. **Monthly Action Plan:**
   - Invest ${goals['monthly_savings_capacity']} automatically
   - Review quarterly (as {customer['relationship_tier']} member)

**Projected Retirement Value:** ${goals['monthly_savings_capacity'] * 12 * 25:,} (assuming 7% growth over 25 years)

Ready to start your investment plan?"""
        
        elif any(word in query_lower for word in ['mortgage', 'refinance', 'home', 'loan']):
            return f"""🏠 **Mortgage Analysis for {customer['name']}:**

**Your Qualification Profile:**
- Credit Score: {financial['credit_score']} ({"Excellent rates available" if financial['credit_score'] >= 740 else "Good rates available"})
- Annual Income: {financial['annual_income']}
- Debt-to-Income: {financial['debt_to_income']}
- Current Homeowner: {"Yes" if financial['homeowner'] else "No"}

**Refinancing Analysis:**
{"**Current Mortgage:** Likely paying 4-6% (based on your customer history)" if financial['homeowner'] else "**Home Purchase:** First-time buyer programs available"}

**Today's Rates** ({customer['relationship_tier']} member pricing):
- 30-year fixed: 6.75% (0.25% relationship discount)
- 15-year fixed: 6.25% (0.25% relationship discount)
- ARM 5/1: 5.95% (0.25% relationship discount)

**Estimated Savings:**
{"- Monthly payment reduction: $200-400" if financial['homeowner'] else "- Pre-approval amount: $" + str(int(financial['annual_income'].replace('$', '').replace('k', '000').replace('-', '').replace('+', '')) * 4) + " (estimated)"}
- Closing costs: $3,000-5,000
- Break-even: 18-24 months

**Next Steps:**
1. Free rate lock (30 days)
2. {customer['relationship_tier']} member gets expedited processing
3. No application fee

Schedule your mortgage consultation today?"""
        
        elif any(word in query_lower for word in ['budget', 'budgeting', 'expenses']):
            return f"""💰 **Personalized Budget Plan for {customer['name']}:**

**Your Current Financial Picture:**
- Monthly Income: ~${int(financial['annual_income'].replace('$', '').replace('k', '000').replace('-', '').replace('+', '')) // 12:,} (estimated from {financial['annual_income']})
- Monthly Spending: ${activity['monthly_spending']:,}
- Top Categories: {', '.join(activity['top_spending_categories'])}

**Recommended Budget Allocation:**
- **Needs (50%):** ${int(activity['monthly_spending'] * 0.5):,}
  - Housing, utilities, groceries, minimum debt payments
- **Wants (30%):** ${int(activity['monthly_spending'] * 0.3):,}
  - Dining out, entertainment, shopping
- **Savings (20%):** ${int(activity['monthly_spending'] * 0.2):,}
  - Emergency fund, retirement, goals

**Your Savings Capacity:** ${goals['monthly_savings_capacity']} ({"Above recommended!" if goals['monthly_savings_capacity'] > activity['monthly_spending'] * 0.2 else "Room for improvement"})

**Action Plan:**
1. **This Week:** Set up automatic transfers
2. **This Month:** Track spending with our mobile app
3. **Ongoing:** Monthly budget reviews

**{customer['relationship_tier']} Member Tools:**
- Free budgeting app with spending alerts
- Quarterly financial check-ins
- Custom savings goals tracking

Want to set up automatic savings transfers?"""
        
        elif any(word in query_lower for word in ['savings', 'account', 'interest']):
            return f"""💰 **Savings Strategy for {customer['name']}:**

**Your Current Savings:**
- Savings Balance: ${accounts['savings_balance']:,}
- Checking Balance: ${accounts['checking_balance']:,}
- Monthly Savings Capacity: ${goals['monthly_savings_capacity']}

**Recommended Account Structure:**

1. **Emergency Fund** (Priority #1):
   - Target: ${activity['monthly_spending'] * 6:,} (6 months expenses)
   - Current: ${accounts['savings_balance']:,}
   - {"✅ Fully funded!" if accounts['savings_balance'] >= activity['monthly_spending'] * 6 else f"Need: ${activity['monthly_spending'] * 6 - accounts['savings_balance']:,} more"}

2. **High-Yield Savings** ({customer['relationship_tier']} rate):
   - Current APY: 4.25% (0.50% relationship bonus)
   - Monthly interest: ~${int(accounts['savings_balance'] * 0.0425 / 12):,}

3. **Goal-Based Savings:**
   - {goals['primary_goals'][0]}: ${goals['monthly_savings_capacity'] // 2}/month
   - {goals['primary_goals'][1]}: ${goals['monthly_savings_capacity'] // 2}/month

**Optimization Plan:**
- Move excess checking (>${accounts['checking_balance'] - 2000:,}) to high-yield savings
- Set up automatic transfers on payday
- Ladder CDs for {goals['time_horizon']} goals

**Projected Growth:** ${accounts['savings_balance'] + (goals['monthly_savings_capacity'] * 12):,} in one year

Ready to optimize your savings strategy?"""
        
        else:
            return f"""💼 **Financial Wellness Summary for {customer['name']}:**

**Your Financial Health Score:** {"Excellent" if financial['credit_score'] > 750 and accounts['savings_balance'] > 10000 else "Good" if financial['credit_score'] > 650 else "Needs Attention"}

**Current Status:**
- {customer['relationship_tier']} member since {customer['customer_since']}
- Credit Score: {financial['credit_score']}
- Total Savings: ${accounts['savings_balance']:,}
- Monthly Savings: ${goals['monthly_savings_capacity']}

**Priority Action Items:**
1. **{goals['primary_goals'][0]}** - Your top financial goal
2. **Emergency Fund** - {"✅ Adequate" if accounts['savings_balance'] >= activity['monthly_spending'] * 3 else "⚠️ Build to $" + str(activity['monthly_spending'] * 6) + " (6 months)"}
3. **Debt Management** - DTI at {financial['debt_to_income']} {"(Good)" if int(financial['debt_to_income'].replace('%', '')) < 36 else "(Consider reduction)"}

**Available Services:**
- Free financial planning consultation
- {customer['relationship_tier']} member investment advisory
- Automated savings and investment tools
- Credit monitoring and improvement

**Next Steps:**
- Schedule your annual financial review
- Optimize account structure for better returns
- Review insurance and estate planning needs

What financial goal would you like to tackle first?"""