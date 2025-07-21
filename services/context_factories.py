"""
Industry-specific context factories for generating realistic context data.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from services.context_service import BaseContextFactory, Industry


class RestaurantContextFactory(BaseContextFactory):
    """Context factory for restaurant industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.RESTAURANT
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate restaurant customer profile."""
        return {
            'name': self.faker.name(),
            'age': self.faker.random_int(min=18, max=75),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'location': {
                'city': self.faker.city(),
                'state': self.faker.state(),
                'zip_code': self.faker.zipcode()
            },
            'loyalty_member': self.faker.boolean(chance_of_getting_true=40),
            'preferred_contact': self.faker.random_element(['email', 'phone', 'text'])
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate restaurant-specific situational data."""
        reservation_time = self.faker.date_time_between(
            start_date='+1h', end_date='+7d'
        )
        
        return {
            'reservation_request': {
                'date': reservation_time.strftime('%Y-%m-%d'),
                'time': reservation_time.strftime('%H:%M'),
                'party_size': self.faker.random_int(min=1, max=12),
                'occasion': self.faker.random_element([
                    'casual dining', 'business meeting', 'date night', 
                    'birthday celebration', 'anniversary', 'family gathering'
                ])
            },
            'current_location': self.faker.city(),
            'weather': self.faker.random_element([
                'sunny', 'rainy', 'cloudy', 'snowy', 'windy'
            ]),
            'day_of_week': reservation_time.strftime('%A'),
            'is_peak_hours': reservation_time.hour in [12, 13, 18, 19, 20],
            'special_requests': self.faker.random_element([
                None, 'wheelchair accessible', 'quiet table', 
                'window seat', 'private dining', 'high chair needed'
            ])
        }
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate restaurant preferences."""
        cuisines = [
            'Italian', 'Chinese', 'Mexican', 'Indian', 'Japanese', 
            'French', 'Thai', 'Mediterranean', 'American', 'Korean'
        ]
        
        return {
            'cuisine_preferences': self.faker.random_elements(
                cuisines, length=self.faker.random_int(min=1, max=3), unique=True
            ),
            'dietary_restrictions': self.faker.random_element([
                'none', 'vegetarian', 'vegan', 'gluten-free', 
                'dairy-free', 'nut allergy', 'shellfish allergy'
            ]),
            'price_range': self.faker.random_element([
                '$', '$$', '$$$', '$$$$'
            ]),
            'atmosphere_preference': self.faker.random_element([
                'casual', 'upscale', 'family-friendly', 'romantic', 'trendy'
            ]),
            'seating_preference': self.faker.random_element([
                'booth', 'table', 'bar seating', 'outdoor patio', 'no preference'
            ])
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate restaurant history."""
        return {
            'previous_visits': self.faker.random_int(min=0, max=25),
            'favorite_restaurants': [
                self.faker.company() + ' Restaurant' 
                for _ in range(self.faker.random_int(min=1, max=4))
            ],
            'last_reservation': {
                'date': self.faker.date_between(start_date='-6m', end_date='-1d').isoformat(),
                'restaurant': self.faker.company() + ' Bistro',
                'rating': self.faker.random_int(min=3, max=5)
            },
            'average_spending': self.faker.random_int(min=25, max=150),
            'cancellation_history': self.faker.random_int(min=0, max=3),
            'no_show_history': self.faker.random_int(min=0, max=2)
        }


class HealthcareContextFactory(BaseContextFactory):
    """Context factory for healthcare industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.HEALTHCARE
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate healthcare patient profile."""
        return {
            'name': self.faker.name(),
            'age': self.faker.random_int(min=1, max=95),
            'gender': self.faker.random_element(['male', 'female', 'other']),
            'date_of_birth': self.faker.date_of_birth().isoformat(),
            'contact': {
                'phone': self.faker.phone_number(),
                'email': self.faker.email(),
                'address': {
                    'street': self.faker.street_address(),
                    'city': self.faker.city(),
                    'state': self.faker.state(),
                    'zip_code': self.faker.zipcode()
                }
            },
            'insurance': {
                'provider': self.faker.random_element([
                    'Blue Cross Blue Shield', 'Aetna', 'Cigna', 
                    'UnitedHealth', 'Kaiser Permanente', 'Humana'
                ]),
                'policy_number': self.faker.bothify('###-##-####'),
                'group_number': self.faker.bothify('GRP-#####')
            },
            'emergency_contact': {
                'name': self.faker.name(),
                'relationship': self.faker.random_element([
                    'spouse', 'parent', 'child', 'sibling', 'friend'
                ]),
                'phone': self.faker.phone_number()
            }
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate healthcare-specific situational data."""
        return {
            'appointment_request': {
                'type': self.faker.random_element([
                    'routine checkup', 'follow-up', 'urgent care', 
                    'specialist consultation', 'preventive screening'
                ]),
                'preferred_date': self.faker.date_between(
                    start_date='+1d', end_date='+30d'
                ).isoformat(),
                'preferred_time': self.faker.random_element([
                    'morning', 'afternoon', 'evening', 'any time'
                ]),
                'urgency': self.faker.random_element([
                    'routine', 'urgent', 'emergency'
                ])
            },
            'current_symptoms': self.faker.random_elements([
                'headache', 'fever', 'cough', 'fatigue', 'nausea', 
                'dizziness', 'chest pain', 'shortness of breath'
            ], length=self.faker.random_int(min=0, max=3), unique=True),
            'symptom_duration': self.faker.random_element([
                '1 day', '2-3 days', '1 week', '2 weeks', '1 month', 'ongoing'
            ]),
            'pain_level': self.faker.random_int(min=0, max=10),
            'mobility_status': self.faker.random_element([
                'fully mobile', 'limited mobility', 'wheelchair', 'bedridden'
            ])
        }
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate healthcare preferences."""
        return {
            'preferred_provider': self.faker.random_element([
                'primary care physician', 'specialist', 'nurse practitioner'
            ]),
            'communication_preference': self.faker.random_element([
                'phone', 'email', 'patient portal', 'text message'
            ]),
            'appointment_preferences': {
                'time_of_day': self.faker.random_element([
                    'early morning', 'morning', 'afternoon', 'evening'
                ]),
                'day_of_week': self.faker.random_element([
                    'weekday', 'weekend', 'any day'
                ]),
                'reminder_preference': self.faker.random_element([
                    '24 hours', '2 hours', '1 hour', 'no reminder'
                ])
            },
            'language_preference': self.faker.random_element([
                'English', 'Spanish', 'French', 'Chinese', 'Other'
            ]),
            'accessibility_needs': self.faker.random_element([
                'none', 'wheelchair access', 'hearing assistance', 
                'vision assistance', 'interpreter needed'
            ])
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate healthcare history."""
        return {
            'medical_history': {
                'chronic_conditions': self.faker.random_elements([
                    'diabetes', 'hypertension', 'asthma', 'arthritis', 
                    'heart disease', 'depression', 'anxiety'
                ], length=self.faker.random_int(min=0, max=3), unique=True),
                'allergies': self.faker.random_elements([
                    'penicillin', 'peanuts', 'shellfish', 'latex', 'pollen'
                ], length=self.faker.random_int(min=0, max=2), unique=True),
                'medications': [
                    self.faker.word() + 'in' 
                    for _ in range(self.faker.random_int(min=0, max=4))
                ]
            },
            'recent_visits': [
                {
                    'date': self.faker.date_between(start_date='-1y', end_date='-1d').isoformat(),
                    'type': self.faker.random_element([
                        'checkup', 'urgent care', 'specialist', 'emergency'
                    ]),
                    'provider': f"Dr. {self.faker.last_name()}"
                }
                for _ in range(self.faker.random_int(min=0, max=5))
            ],
            'vaccination_status': {
                'covid_19': self.faker.boolean(chance_of_getting_true=85),
                'flu': self.faker.boolean(chance_of_getting_true=60),
                'up_to_date': self.faker.boolean(chance_of_getting_true=70)
            }
        }


class EcommerceContextFactory(BaseContextFactory):
    """Context factory for e-commerce industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.ECOMMERCE
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate e-commerce customer profile."""
        return {
            'name': self.faker.name(),
            'email': self.faker.email(),
            'age': self.faker.random_int(min=16, max=70),
            'location': {
                'city': self.faker.city(),
                'state': self.faker.state(),
                'country': self.faker.country(),
                'zip_code': self.faker.zipcode()
            },
            'account_type': self.faker.random_element([
                'regular', 'premium', 'vip', 'business'
            ]),
            'member_since': self.faker.date_between(start_date='-5y', end_date='-1m').isoformat(),
            'loyalty_points': self.faker.random_int(min=0, max=5000),
            'preferred_payment': self.faker.random_element([
                'credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay'
            ])
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate e-commerce situational data."""
        return {
            'current_session': {
                'device': self.faker.random_element([
                    'desktop', 'mobile', 'tablet'
                ]),
                'browser': self.faker.random_element([
                    'Chrome', 'Safari', 'Firefox', 'Edge'
                ]),
                'session_duration': self.faker.random_int(min=2, max=45),
                'pages_viewed': self.faker.random_int(min=1, max=20)
            },
            'shopping_intent': self.faker.random_element([
                'browsing', 'researching', 'ready_to_buy', 'comparing_prices'
            ]),
            'current_search': {
                'query': self.faker.random_element([
                    'wireless headphones', 'running shoes', 'laptop', 
                    'coffee maker', 'winter jacket', 'smartphone'
                ]),
                'category': self.faker.random_element([
                    'electronics', 'clothing', 'home', 'sports', 'books'
                ]),
                'price_range': self.faker.random_element([
                    'under_50', '50_100', '100_500', 'over_500'
                ])
            },
            'cart_status': {
                'items_in_cart': self.faker.random_int(min=0, max=8),
                'cart_value': self.faker.random_int(min=0, max=500),
                'abandoned_carts': self.faker.random_int(min=0, max=3)
            }
        }
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate e-commerce preferences."""
        return {
            'product_categories': self.faker.random_elements([
                'electronics', 'clothing', 'home_garden', 'sports', 
                'books', 'beauty', 'automotive', 'toys'
            ], length=self.faker.random_int(min=2, max=4), unique=True),
            'brands': self.faker.random_elements([
                'Apple', 'Samsung', 'Nike', 'Adidas', 'Sony', 
                'Amazon Basics', 'Target', 'IKEA'
            ], length=self.faker.random_int(min=1, max=3), unique=True),
            'price_sensitivity': self.faker.random_element([
                'budget_conscious', 'value_seeker', 'premium_buyer', 'price_insensitive'
            ]),
            'shipping_preferences': {
                'speed': self.faker.random_element([
                    'standard', 'expedited', 'overnight', 'same_day'
                ]),
                'cost': self.faker.random_element([
                    'free_shipping_only', 'low_cost_ok', 'speed_over_cost'
                ])
            },
            'communication_preferences': {
                'promotions': self.faker.boolean(chance_of_getting_true=60),
                'recommendations': self.faker.boolean(chance_of_getting_true=70),
                'order_updates': self.faker.boolean(chance_of_getting_true=90)
            }
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate e-commerce history."""
        return {
            'purchase_history': {
                'total_orders': self.faker.random_int(min=0, max=50),
                'total_spent': self.faker.random_int(min=0, max=5000),
                'average_order_value': self.faker.random_int(min=25, max=200),
                'last_purchase_date': self.faker.date_between(
                    start_date='-6m', end_date='-1d'
                ).isoformat()
            },
            'recent_purchases': [
                {
                    'product': self.faker.random_element([
                        'Wireless Earbuds', 'Running Shoes', 'Coffee Maker',
                        'Laptop Stand', 'Phone Case', 'Book'
                    ]),
                    'price': self.faker.random_int(min=15, max=300),
                    'date': self.faker.date_between(start_date='-3m', end_date='-1d').isoformat(),
                    'rating': self.faker.random_int(min=3, max=5)
                }
                for _ in range(self.faker.random_int(min=0, max=5))
            ],
            'browsing_history': {
                'frequently_viewed_categories': self.faker.random_elements([
                    'electronics', 'clothing', 'home', 'sports'
                ], length=self.faker.random_int(min=1, max=3), unique=True),
                'wishlist_items': self.faker.random_int(min=0, max=15),
                'saved_for_later': self.faker.random_int(min=0, max=8)
            },
            'customer_service': {
                'support_tickets': self.faker.random_int(min=0, max=5),
                'returns': self.faker.random_int(min=0, max=3),
                'satisfaction_score': self.faker.random_int(min=3, max=5)
            }
        }


class FinancialContextFactory(BaseContextFactory):
    """Context factory for financial services industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.FINANCIAL
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate financial services customer profile."""
        return {
            'name': self.faker.name(),
            'age': self.faker.random_int(min=18, max=75),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'employment': {
                'status': self.faker.random_element([
                    'employed', 'self_employed', 'unemployed', 'retired', 'student'
                ]),
                'industry': self.faker.random_element([
                    'technology', 'healthcare', 'education', 'finance', 
                    'retail', 'manufacturing', 'government'
                ]),
                'income_range': self.faker.random_element([
                    'under_30k', '30k_50k', '50k_75k', '75k_100k', 
                    '100k_150k', 'over_150k'
                ])
            },
            'credit_profile': {
                'score_range': self.faker.random_element([
                    'poor', 'fair', 'good', 'very_good', 'excellent'
                ]),
                'history_length': self.faker.random_int(min=0, max=30)
            },
            'customer_since': self.faker.date_between(start_date='-10y', end_date='-1m').isoformat()
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate financial services situational data."""
        return {
            'service_request': {
                'type': self.faker.random_element([
                    'account_opening', 'loan_application', 'investment_advice',
                    'insurance_quote', 'mortgage_inquiry', 'credit_card_application'
                ]),
                'urgency': self.faker.random_element([
                    'low', 'medium', 'high', 'urgent'
                ]),
                'amount': self.faker.random_int(min=1000, max=500000) if self.faker.boolean() else None
            },
            'financial_goals': self.faker.random_elements([
                'retirement_planning', 'home_purchase', 'debt_consolidation',
                'emergency_fund', 'investment_growth', 'education_funding'
            ], length=self.faker.random_int(min=1, max=3), unique=True),
            'risk_tolerance': self.faker.random_element([
                'very_conservative', 'conservative', 'moderate', 
                'aggressive', 'very_aggressive'
            ]),
            'time_horizon': self.faker.random_element([
                'short_term', 'medium_term', 'long_term'
            ]),
            'current_financial_situation': {
                'monthly_income': self.faker.random_int(min=2000, max=15000),
                'monthly_expenses': self.faker.random_int(min=1500, max=12000),
                'existing_debt': self.faker.random_int(min=0, max=100000),
                'savings': self.faker.random_int(min=0, max=50000)
            }
        }
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate financial preferences."""
        return {
            'communication_preferences': {
                'method': self.faker.random_element([
                    'email', 'phone', 'text', 'mail', 'in_person'
                ]),
                'frequency': self.faker.random_element([
                    'daily', 'weekly', 'monthly', 'quarterly', 'as_needed'
                ]),
                'time_of_day': self.faker.random_element([
                    'morning', 'afternoon', 'evening', 'any_time'
                ])
            },
            'service_preferences': {
                'digital_vs_branch': self.faker.random_element([
                    'digital_only', 'mostly_digital', 'mixed', 'mostly_branch', 'branch_only'
                ]),
                'advisor_relationship': self.faker.random_element([
                    'self_directed', 'occasional_advice', 'regular_guidance', 'full_service'
                ])
            },
            'investment_preferences': {
                'asset_classes': self.faker.random_elements([
                    'stocks', 'bonds', 'mutual_funds', 'etfs', 
                    'real_estate', 'commodities', 'crypto'
                ], length=self.faker.random_int(min=1, max=4), unique=True),
                'esg_investing': self.faker.boolean(chance_of_getting_true=30)
            }
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate financial history."""
        return {
            'account_history': {
                'checking_accounts': self.faker.random_int(min=0, max=3),
                'savings_accounts': self.faker.random_int(min=0, max=5),
                'credit_cards': self.faker.random_int(min=0, max=8),
                'loans': self.faker.random_int(min=0, max=4),
                'investment_accounts': self.faker.random_int(min=0, max=3)
            },
            'transaction_patterns': {
                'monthly_transactions': self.faker.random_int(min=10, max=100),
                'average_transaction_amount': self.faker.random_int(min=25, max=500),
                'primary_spending_categories': self.faker.random_elements([
                    'groceries', 'gas', 'restaurants', 'utilities', 
                    'entertainment', 'shopping', 'healthcare'
                ], length=self.faker.random_int(min=2, max=4), unique=True)
            },
            'service_usage': {
                'online_banking': self.faker.boolean(chance_of_getting_true=85),
                'mobile_app': self.faker.boolean(chance_of_getting_true=70),
                'atm_usage': self.faker.random_int(min=0, max=20),
                'branch_visits': self.faker.random_int(min=0, max=12)
            },
            'customer_satisfaction': {
                'overall_rating': self.faker.random_int(min=3, max=5),
                'likelihood_to_recommend': self.faker.random_int(min=6, max=10),
                'complaints': self.faker.random_int(min=0, max=2)
            }
        }


class EducationContextFactory(BaseContextFactory):
    """Context factory for education industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.EDUCATION
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate education user profile."""
        user_type = self.faker.random_element(['student', 'parent', 'educator'])
        
        profile = {
            'name': self.faker.name(),
            'email': self.faker.email(),
            'user_type': user_type,
            'contact': {
                'phone': self.faker.phone_number(),
                'address': {
                    'street': self.faker.street_address(),
                    'city': self.faker.city(),
                    'state': self.faker.state(),
                    'zip_code': self.faker.zipcode()
                }
            }
        }
        
        if user_type == 'student':
            profile.update({
                'age': self.faker.random_int(min=5, max=25),
                'grade_level': self.faker.random_element([
                    'kindergarten', '1st', '2nd', '3rd', '4th', '5th',
                    '6th', '7th', '8th', '9th', '10th', '11th', '12th',
                    'college_freshman', 'college_sophomore', 'college_junior', 'college_senior'
                ]),
                'student_id': self.faker.bothify('STU-#####')
            })
        elif user_type == 'parent':
            profile.update({
                'age': self.faker.random_int(min=25, max=55),
                'children': [
                    {
                        'name': self.faker.first_name(),
                        'age': self.faker.random_int(min=5, max=18),
                        'grade': self.faker.random_element([
                            'kindergarten', '1st', '2nd', '3rd', '4th', '5th',
                            '6th', '7th', '8th', '9th', '10th', '11th', '12th'
                        ])
                    }
                    for _ in range(self.faker.random_int(min=1, max=3))
                ]
            })
        else:  # educator
            profile.update({
                'age': self.faker.random_int(min=22, max=65),
                'role': self.faker.random_element([
                    'teacher', 'principal', 'counselor', 'administrator', 'tutor'
                ]),
                'subject_area': self.faker.random_element([
                    'mathematics', 'english', 'science', 'history', 
                    'art', 'music', 'physical_education', 'special_education'
                ]),
                'years_experience': self.faker.random_int(min=0, max=40)
            })
        
        return profile
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate education situational data."""
        return {
            'academic_period': {
                'current_semester': self.faker.random_element([
                    'fall', 'spring', 'summer'
                ]),
                'academic_year': f"{datetime.now().year}-{datetime.now().year + 1}",
                'week_of_semester': self.faker.random_int(min=1, max=16)
            },
            'current_request': {
                'type': self.faker.random_element([
                    'enrollment', 'course_registration', 'grade_inquiry',
                    'tutoring_request', 'academic_support', 'schedule_change'
                ]),
                'urgency': self.faker.random_element([
                    'low', 'medium', 'high', 'urgent'
                ]),
                'deadline': self.faker.date_between(
                    start_date='+1d', end_date='+30d'
                ).isoformat() if self.faker.boolean() else None
            },
            'academic_status': {
                'current_gpa': round(self.faker.random.uniform(2.0, 4.0), 2),
                'credit_hours': self.faker.random_int(min=12, max=18),
                'academic_standing': self.faker.random_element([
                    'good_standing', 'probation', 'honors', 'dean_list'
                ])
            },
            'learning_environment': {
                'format': self.faker.random_element([
                    'in_person', 'online', 'hybrid'
                ]),
                'class_size_preference': self.faker.random_element([
                    'small', 'medium', 'large', 'no_preference'
                ])
            }
        }
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate education preferences."""
        return {
            'learning_style': self.faker.random_element([
                'visual', 'auditory', 'kinesthetic', 'reading_writing'
            ]),
            'communication_preferences': {
                'method': self.faker.random_element([
                    'email', 'phone', 'text', 'in_person', 'video_call'
                ]),
                'frequency': self.faker.random_element([
                    'daily', 'weekly', 'bi_weekly', 'monthly', 'as_needed'
                ])
            },
            'subject_interests': self.faker.random_elements([
                'mathematics', 'science', 'english', 'history', 'art',
                'music', 'foreign_languages', 'computer_science', 'psychology'
            ], length=self.faker.random_int(min=2, max=5), unique=True),
            'extracurricular_interests': self.faker.random_elements([
                'sports', 'music', 'drama', 'debate', 'student_government',
                'volunteer_work', 'clubs', 'research'
            ], length=self.faker.random_int(min=1, max=4), unique=True),
            'technology_comfort': self.faker.random_element([
                'beginner', 'intermediate', 'advanced', 'expert'
            ])
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate education history."""
        return {
            'academic_history': {
                'previous_schools': [
                    {
                        'name': f"{self.faker.city()} {self.faker.random_element(['Elementary', 'Middle', 'High'])} School",
                        'years_attended': self.faker.random_int(min=1, max=4),
                        'gpa': round(self.faker.random.uniform(2.5, 4.0), 2)
                    }
                    for _ in range(self.faker.random_int(min=1, max=3))
                ],
                'standardized_test_scores': {
                    'sat': self.faker.random_int(min=800, max=1600) if self.faker.boolean() else None,
                    'act': self.faker.random_int(min=10, max=36) if self.faker.boolean() else None
                },
                'honors_awards': self.faker.random_elements([
                    'honor_roll', 'perfect_attendance', 'academic_excellence',
                    'leadership_award', 'community_service'
                ], length=self.faker.random_int(min=0, max=3), unique=True)
            },
            'course_history': {
                'completed_courses': self.faker.random_int(min=5, max=30),
                'favorite_subjects': self.faker.random_elements([
                    'mathematics', 'science', 'english', 'history', 'art'
                ], length=self.faker.random_int(min=1, max=3), unique=True),
                'challenging_subjects': self.faker.random_elements([
                    'mathematics', 'science', 'english', 'foreign_language'
                ], length=self.faker.random_int(min=0, max=2), unique=True)
            },
            'support_services': {
                'tutoring_used': self.faker.boolean(chance_of_getting_true=30),
                'counseling_services': self.faker.boolean(chance_of_getting_true=20),
                'special_accommodations': self.faker.boolean(chance_of_getting_true=15)
            }
        }


class RealEstateContextFactory(BaseContextFactory):
    """Context factory for real estate industry."""
    
    def _get_industry(self) -> Industry:
        return Industry.REAL_ESTATE
    
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate real estate client profile."""
        return {
            'name': self.faker.name(),
            'age': self.faker.random_int(min=22, max=70),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'current_address': {
                'street': self.faker.street_address(),
                'city': self.faker.city(),
                'state': self.faker.state(),
                'zip_code': self.faker.zipcode()
            },
            'employment': {
                'status': self.faker.random_element([
                    'employed', 'self_employed', 'retired', 'unemployed'
                ]),
                'income': self.faker.random_int(min=30000, max=200000),
                'employment_length': self.faker.random_int(min=0, max=20)
            },
            'family_status': {
                'marital_status': self.faker.random_element([
                    'single', 'married', 'divorced', 'widowed'
                ]),
                'children': self.faker.random_int(min=0, max=4),
                'pets': self.faker.random_int(min=0, max=3)
            },
            'first_time_buyer': self.faker.boolean(chance_of_getting_true=35)
        }
    
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate real estate situational data."""
        transaction_type = self.faker.random_element(['buying', 'selling', 'renting'])
        
        situational_data = {
            'transaction_type': transaction_type,
            'timeline': self.faker.random_element([
                'immediately', 'within_1_month', 'within_3_months', 
                'within_6_months', 'within_1_year', 'flexible'
            ]),
            'motivation': self.faker.random_element([
                'job_relocation', 'family_growth', 'downsizing', 
                'investment', 'lifestyle_change', 'retirement'
            ]),
            'urgency': self.faker.random_element([
                'low', 'medium', 'high', 'urgent'
            ])
        }
        
        if transaction_type in ['buying', 'renting']:
            situational_data.update({
                'property_search': {
                    'property_type': self.faker.random_element([
                        'single_family', 'condo', 'townhouse', 'apartment', 'duplex'
                    ]),
                    'bedrooms': self.faker.random_int(min=1, max=5),
                    'bathrooms': self.faker.random_element([1, 1.5, 2, 2.5, 3, 3.5, 4]),
                    'square_footage': self.faker.random_int(min=500, max=4000),
                    'price_range': {
                        'min': self.faker.random_int(min=100000, max=300000),
                        'max': self.faker.random_int(min=400000, max=800000)
                    }
                },
                'preferred_locations': [
                    self.faker.city() for _ in range(self.faker.random_int(min=1, max=3))
                ],
                'financing': {
                    'pre_approved': self.faker.boolean(chance_of_getting_true=60),
                    'down_payment': self.faker.random_int(min=5, max=25),
                    'loan_type': self.faker.random_element([
                        'conventional', 'fha', 'va', 'usda', 'cash'
                    ])
                }
            })
        
        if transaction_type == 'selling':
            situational_data.update({
                'current_property': {
                    'property_type': self.faker.random_element([
                        'single_family', 'condo', 'townhouse'
                    ]),
                    'bedrooms': self.faker.random_int(min=2, max=5),
                    'bathrooms': self.faker.random_element([1, 1.5, 2, 2.5, 3]),
                    'square_footage': self.faker.random_int(min=800, max=3500),
                    'year_built': self.faker.random_int(min=1950, max=2020),
                    'estimated_value': self.faker.random_int(min=200000, max=600000)
                },
                'selling_reason': self.faker.random_element([
                    'upgrading', 'downsizing', 'relocating', 'financial', 'lifestyle'
                ])
            })
        
        return situational_data
    
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate real estate preferences."""
        return {
            'property_features': {
                'must_haves': self.faker.random_elements([
                    'garage', 'yard', 'updated_kitchen', 'master_suite',
                    'hardwood_floors', 'fireplace', 'pool', 'basement'
                ], length=self.faker.random_int(min=2, max=4), unique=True),
                'nice_to_haves': self.faker.random_elements([
                    'walk_in_closet', 'home_office', 'deck_patio',
                    'stainless_appliances', 'granite_counters', 'cathedral_ceilings'
                ], length=self.faker.random_int(min=1, max=3), unique=True)
            },
            'neighborhood_preferences': {
                'school_quality': self.faker.random_element([
                    'not_important', 'somewhat_important', 'very_important', 'critical'
                ]),
                'commute_distance': self.faker.random_element([
                    'under_15_min', '15_30_min', '30_45_min', 'over_45_min'
                ]),
                'neighborhood_type': self.faker.random_element([
                    'urban', 'suburban', 'rural', 'mixed'
                ]),
                'amenities': self.faker.random_elements([
                    'parks', 'shopping', 'restaurants', 'public_transit',
                    'gyms', 'libraries', 'hospitals'
                ], length=self.faker.random_int(min=2, max=4), unique=True)
            },
            'communication_preferences': {
                'contact_method': self.faker.random_element([
                    'phone', 'email', 'text', 'any'
                ]),
                'contact_frequency': self.faker.random_element([
                    'daily', 'few_times_week', 'weekly', 'as_needed'
                ]),
                'showing_preferences': {
                    'days': self.faker.random_elements([
                        'monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday'
                    ], length=self.faker.random_int(min=2, max=5), unique=True),
                    'times': self.faker.random_element([
                        'morning', 'afternoon', 'evening', 'flexible'
                    ])
                }
            }
        }
    
    def generate_history(self) -> Dict[str, Any]:
        """Generate real estate history."""
        return {
            'property_history': {
                'properties_owned': self.faker.random_int(min=0, max=5),
                'years_in_current_home': self.faker.random_int(min=0, max=20),
                'previous_transactions': [
                    {
                        'type': self.faker.random_element(['bought', 'sold', 'rented']),
                        'year': self.faker.random_int(min=2010, max=2023),
                        'location': self.faker.city(),
                        'price': self.faker.random_int(min=150000, max=500000)
                    }
                    for _ in range(self.faker.random_int(min=0, max=3))
                ]
            },
            'agent_experience': {
                'worked_with_agent_before': self.faker.boolean(chance_of_getting_true=40),
                'referral_source': self.faker.random_element([
                    'friend_family', 'online_search', 'previous_agent',
                    'advertisement', 'walk_in'
                ]),
                'agent_preferences': self.faker.random_element([
                    'experienced', 'local_expert', 'full_service', 'tech_savvy'
                ])
            },
            'market_knowledge': {
                'market_research_done': self.faker.boolean(chance_of_getting_true=70),
                'price_awareness': self.faker.random_element([
                    'very_aware', 'somewhat_aware', 'limited_knowledge'
                ]),
                'market_conditions_concern': self.faker.random_element([
                    'not_concerned', 'somewhat_concerned', 'very_concerned'
                ])
            }
        }
    
    def generate_constraints(self) -> Dict[str, Any]:
        """Generate real estate specific constraints."""
        base_constraints = super().generate_constraints()
        
        base_constraints.update({
            'financing_constraints': {
                'credit_score_range': self.faker.random_element([
                    'excellent', 'good', 'fair', 'poor'
                ]),
                'debt_to_income_ratio': self.faker.random_int(min=10, max=45),
                'cash_available': self.faker.random_int(min=5000, max=100000)
            },
            'location_constraints': {
                'max_commute_time': self.faker.random_int(min=15, max=60),
                'school_district_required': self.faker.boolean(chance_of_getting_true=40),
                'proximity_to_family': self.faker.random_element([
                    'not_important', 'preferred', 'required'
                ])
            },
            'timing_constraints': {
                'lease_expiration': self.faker.date_between(
                    start_date='+1m', end_date='+12m'
                ).isoformat() if self.faker.boolean() else None,
                'job_start_date': self.faker.date_between(
                    start_date='+1m', end_date='+6m'
                ).isoformat() if self.faker.boolean() else None,
                'school_year_consideration': self.faker.boolean(chance_of_getting_true=30)
            }
        })
        
        return base_constraints