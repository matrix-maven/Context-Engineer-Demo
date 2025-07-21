"""
Unit tests for industry-specific context factories.
"""
import pytest
from datetime import datetime
from faker import Faker

from services.context_service import Industry, IndustryContext, ContextValidationError
from services.context_factories import (
    RestaurantContextFactory,
    HealthcareContextFactory,
    EcommerceContextFactory,
    FinancialContextFactory,
    EducationContextFactory,
    RealEstateContextFactory
)


class TestRestaurantContextFactory:
    """Test RestaurantContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = RestaurantContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.RESTAURANT
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'age' in profile
        assert 'email' in profile
        assert 'phone' in profile
        assert 'location' in profile
        assert 'loyalty_member' in profile
        
        # Check data types and ranges
        assert isinstance(profile['name'], str)
        assert 18 <= profile['age'] <= 75
        assert '@' in profile['email']
        assert isinstance(profile['loyalty_member'], bool)
        
        # Check location structure
        location = profile['location']
        assert 'city' in location
        assert 'state' in location
        assert 'zip_code' in location
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'reservation_request' in situational
        assert 'current_location' in situational
        assert 'weather' in situational
        assert 'day_of_week' in situational
        assert 'is_peak_hours' in situational
        
        # Check reservation request structure
        reservation = situational['reservation_request']
        assert 'date' in reservation
        assert 'time' in reservation
        assert 'party_size' in reservation
        assert 'occasion' in reservation
        
        # Check data validity
        assert 1 <= reservation['party_size'] <= 12
        assert isinstance(situational['is_peak_hours'], bool)
    
    def test_preferences_generation(self):
        """Test preferences generation."""
        preferences = self.factory.generate_preferences()
        
        # Check required fields
        assert 'cuisine_preferences' in preferences
        assert 'dietary_restrictions' in preferences
        assert 'price_range' in preferences
        assert 'atmosphere_preference' in preferences
        assert 'seating_preference' in preferences
        
        # Check data validity
        assert isinstance(preferences['cuisine_preferences'], list)
        assert len(preferences['cuisine_preferences']) >= 1
        assert preferences['price_range'] in ['$', '$$', '$$$', '$$$$']
    
    def test_history_generation(self):
        """Test history generation."""
        history = self.factory.generate_history()
        
        # Check required fields
        assert 'previous_visits' in history
        assert 'favorite_restaurants' in history
        assert 'last_reservation' in history
        assert 'average_spending' in history
        
        # Check data validity
        assert history['previous_visits'] >= 0
        assert isinstance(history['favorite_restaurants'], list)
        assert 25 <= history['average_spending'] <= 150
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.RESTAURANT
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestHealthcareContextFactory:
    """Test HealthcareContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = HealthcareContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.HEALTHCARE
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'age' in profile
        assert 'gender' in profile
        assert 'date_of_birth' in profile
        assert 'contact' in profile
        assert 'insurance' in profile
        assert 'emergency_contact' in profile
        
        # Check data validity
        assert 1 <= profile['age'] <= 95
        assert profile['gender'] in ['male', 'female', 'other']
        
        # Check nested structures
        contact = profile['contact']
        assert 'phone' in contact
        assert 'email' in contact
        assert 'address' in contact
        
        insurance = profile['insurance']
        assert 'provider' in insurance
        assert 'policy_number' in insurance
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'appointment_request' in situational
        assert 'current_symptoms' in situational
        assert 'pain_level' in situational
        assert 'mobility_status' in situational
        
        # Check appointment request structure
        appointment = situational['appointment_request']
        assert 'type' in appointment
        assert 'preferred_date' in appointment
        assert 'urgency' in appointment
        
        # Check data validity
        assert 0 <= situational['pain_level'] <= 10
        assert isinstance(situational['current_symptoms'], list)
    
    def test_medical_history_generation(self):
        """Test medical history generation."""
        history = self.factory.generate_history()
        
        # Check required fields
        assert 'medical_history' in history
        assert 'recent_visits' in history
        assert 'vaccination_status' in history
        
        # Check medical history structure
        medical = history['medical_history']
        assert 'chronic_conditions' in medical
        assert 'allergies' in medical
        assert 'medications' in medical
        
        # Check data validity
        assert isinstance(medical['chronic_conditions'], list)
        assert isinstance(medical['allergies'], list)
        assert isinstance(history['recent_visits'], list)
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.HEALTHCARE
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestEcommerceContextFactory:
    """Test EcommerceContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = EcommerceContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.ECOMMERCE
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'email' in profile
        assert 'age' in profile
        assert 'location' in profile
        assert 'account_type' in profile
        assert 'member_since' in profile
        assert 'loyalty_points' in profile
        
        # Check data validity
        assert 16 <= profile['age'] <= 70
        assert profile['account_type'] in ['regular', 'premium', 'vip', 'business']
        assert profile['loyalty_points'] >= 0
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'current_session' in situational
        assert 'shopping_intent' in situational
        assert 'current_search' in situational
        assert 'cart_status' in situational
        
        # Check session structure
        session = situational['current_session']
        assert 'device' in session
        assert 'browser' in session
        assert 'session_duration' in session
        
        # Check cart status
        cart = situational['cart_status']
        assert 'items_in_cart' in cart
        assert 'cart_value' in cart
        assert cart['items_in_cart'] >= 0
    
    def test_purchase_history_generation(self):
        """Test purchase history generation."""
        history = self.factory.generate_history()
        
        # Check required fields
        assert 'purchase_history' in history
        assert 'recent_purchases' in history
        assert 'browsing_history' in history
        assert 'customer_service' in history
        
        # Check purchase history structure
        purchase_hist = history['purchase_history']
        assert 'total_orders' in purchase_hist
        assert 'total_spent' in purchase_hist
        assert 'average_order_value' in purchase_hist
        
        # Check data validity
        assert purchase_hist['total_orders'] >= 0
        assert purchase_hist['total_spent'] >= 0
        assert isinstance(history['recent_purchases'], list)
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.ECOMMERCE
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestFinancialContextFactory:
    """Test FinancialContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = FinancialContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.FINANCIAL
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'age' in profile
        assert 'employment' in profile
        assert 'credit_profile' in profile
        assert 'customer_since' in profile
        
        # Check employment structure
        employment = profile['employment']
        assert 'status' in employment
        assert 'industry' in employment
        assert 'income_range' in employment
        
        # Check credit profile
        credit = profile['credit_profile']
        assert 'score_range' in credit
        assert 'history_length' in credit
        assert credit['history_length'] >= 0
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'service_request' in situational
        assert 'financial_goals' in situational
        assert 'risk_tolerance' in situational
        assert 'current_financial_situation' in situational
        
        # Check service request structure
        service_req = situational['service_request']
        assert 'type' in service_req
        assert 'urgency' in service_req
        
        # Check financial situation
        fin_situation = situational['current_financial_situation']
        assert 'monthly_income' in fin_situation
        assert 'monthly_expenses' in fin_situation
        assert fin_situation['monthly_income'] > 0
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.FINANCIAL
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestEducationContextFactory:
    """Test EducationContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = EducationContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.EDUCATION
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'email' in profile
        assert 'user_type' in profile
        assert 'contact' in profile
        
        # Check user type validity
        assert profile['user_type'] in ['student', 'parent', 'educator']
        
        # Check type-specific fields
        if profile['user_type'] == 'student':
            assert 'age' in profile
            assert 'grade_level' in profile
            assert 'student_id' in profile
        elif profile['user_type'] == 'parent':
            assert 'children' in profile
            assert isinstance(profile['children'], list)
        elif profile['user_type'] == 'educator':
            assert 'role' in profile
            assert 'subject_area' in profile
            assert 'years_experience' in profile
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'academic_period' in situational
        assert 'current_request' in situational
        assert 'academic_status' in situational
        assert 'learning_environment' in situational
        
        # Check academic period structure
        period = situational['academic_period']
        assert 'current_semester' in period
        assert 'academic_year' in period
        
        # Check academic status
        status = situational['academic_status']
        assert 'current_gpa' in status
        assert 2.0 <= status['current_gpa'] <= 4.0
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.EDUCATION
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestRealEstateContextFactory:
    """Test RealEstateContextFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factory = RealEstateContextFactory(self.faker)
    
    def test_industry_type(self):
        """Test factory returns correct industry."""
        assert self.factory.industry == Industry.REAL_ESTATE
    
    def test_user_profile_generation(self):
        """Test user profile generation."""
        profile = self.factory.generate_user_profile()
        
        # Check required fields
        assert 'name' in profile
        assert 'age' in profile
        assert 'employment' in profile
        assert 'family_status' in profile
        assert 'first_time_buyer' in profile
        
        # Check employment structure
        employment = profile['employment']
        assert 'status' in employment
        assert 'income' in employment
        assert employment['income'] > 0
        
        # Check family status
        family = profile['family_status']
        assert 'marital_status' in family
        assert 'children' in family
        assert family['children'] >= 0
    
    def test_situational_data_generation(self):
        """Test situational data generation."""
        situational = self.factory.generate_situational_data()
        
        # Check required fields
        assert 'transaction_type' in situational
        assert 'timeline' in situational
        assert 'motivation' in situational
        assert 'urgency' in situational
        
        # Check transaction type validity
        assert situational['transaction_type'] in ['buying', 'selling', 'renting']
        
        # Check transaction-specific fields
        if situational['transaction_type'] in ['buying', 'renting']:
            assert 'property_search' in situational
            assert 'preferred_locations' in situational
            
            search = situational['property_search']
            assert 'property_type' in search
            assert 'bedrooms' in search
            assert 'price_range' in search
        
        if situational['transaction_type'] == 'selling':
            assert 'current_property' in situational
            assert 'selling_reason' in situational
    
    def test_constraints_generation(self):
        """Test real estate specific constraints."""
        constraints = self.factory.generate_constraints()
        
        # Check base constraints
        assert 'budget_conscious' in constraints
        assert 'time_sensitive' in constraints
        
        # Check real estate specific constraints
        assert 'financing_constraints' in constraints
        assert 'location_constraints' in constraints
        assert 'timing_constraints' in constraints
        
        # Check financing constraints structure
        financing = constraints['financing_constraints']
        assert 'credit_score_range' in financing
        assert 'debt_to_income_ratio' in financing
        assert 'cash_available' in financing
    
    def test_complete_context_generation(self):
        """Test complete context generation."""
        context = self.factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.REAL_ESTATE
        assert context.is_valid()
        
        # Validate context
        errors = self.factory.validate_context(context)
        assert len(errors) == 0


class TestContextFactoryIntegration:
    """Test integration of all context factories."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.faker = Faker()
        self.factories = [
            RestaurantContextFactory(self.faker),
            HealthcareContextFactory(self.faker),
            EcommerceContextFactory(self.faker),
            FinancialContextFactory(self.faker),
            EducationContextFactory(self.faker),
            RealEstateContextFactory(self.faker)
        ]
    
    def test_all_factories_generate_valid_contexts(self):
        """Test that all factories generate valid contexts."""
        for factory in self.factories:
            context = factory.generate_context()
            
            # Basic validation
            assert isinstance(context, IndustryContext)
            assert context.is_valid()
            assert context.industry == factory.industry
            
            # Factory validation
            errors = factory.validate_context(context)
            assert len(errors) == 0, f"Validation errors for {factory.industry.value}: {errors}"
    
    def test_context_data_richness(self):
        """Test that contexts contain rich, varied data."""
        for factory in self.factories:
            context = factory.generate_context()
            
            # Check all main sections are populated
            assert len(context.user_profile) > 0
            assert len(context.situational_data) > 0
            assert len(context.preferences) > 0
            assert len(context.history) > 0
            assert len(context.constraints) > 0
            assert len(context.metadata) > 0
            
            # Check total field count for richness
            total_fields = (
                len(context.user_profile) +
                len(context.situational_data) +
                len(context.preferences) +
                len(context.history) +
                len(context.constraints)
            )
            assert total_fields >= 10, f"Context for {factory.industry.value} has only {total_fields} fields"
    
    def test_context_uniqueness(self):
        """Test that contexts generate unique data."""
        for factory in self.factories:
            # Generate multiple contexts
            contexts = [factory.generate_context() for _ in range(3)]
            
            # Check that user names are different (high probability)
            names = [ctx.user_profile.get('name') for ctx in contexts]
            assert len(set(names)) > 1, f"Generated identical names for {factory.industry.value}"
            
            # Check that contexts have different timestamps
            timestamps = [ctx.generated_at for ctx in contexts]
            assert len(set(timestamps)) == len(timestamps), f"Identical timestamps for {factory.industry.value}"
    
    def test_context_serialization(self):
        """Test that contexts can be serialized to dict."""
        for factory in self.factories:
            context = factory.generate_context()
            context_dict = context.to_dict()
            
            # Check all required keys are present
            required_keys = [
                'industry', 'user_profile', 'situational_data',
                'preferences', 'history', 'constraints', 'metadata', 'generated_at'
            ]
            for key in required_keys:
                assert key in context_dict, f"Missing key {key} in {factory.industry.value} context dict"
            
            # Check industry value is string
            assert isinstance(context_dict['industry'], str)
            assert context_dict['industry'] == factory.industry.value


if __name__ == '__main__':
    pytest.main([__file__])