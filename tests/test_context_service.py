"""
Unit tests for context service foundation.
"""
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch

from services.context_service import (
    ContextService, 
    BaseContextFactory, 
    IndustryContext, 
    Industry,
    ContextValidationError
)


class MockContextFactory(BaseContextFactory):
    """Mock context factory for testing."""
    
    def _get_industry(self) -> Industry:
        return Industry.RESTAURANT
    
    def generate_user_profile(self) -> dict:
        return {
            'name': self.faker.name(),
            'age': self.faker.random_int(min=18, max=80),
            'email': self.faker.email()
        }
    
    def generate_situational_data(self) -> dict:
        return {
            'current_time': self.faker.time(),
            'location': self.faker.city(),
            'party_size': self.faker.random_int(min=1, max=8)
        }
    
    def generate_preferences(self) -> dict:
        return {
            'cuisine_type': self.faker.random_element(['Italian', 'Chinese', 'Mexican']),
            'dietary_restrictions': self.faker.random_element(['None', 'Vegetarian', 'Vegan'])
        }
    
    def generate_history(self) -> dict:
        return {
            'previous_visits': self.faker.random_int(min=0, max=10),
            'favorite_dishes': [self.faker.word() for _ in range(3)]
        }


class TestIndustryContext:
    """Test IndustryContext data model."""
    
    def test_context_creation(self):
        """Test basic context creation."""
        context = IndustryContext(
            industry=Industry.RESTAURANT,
            user_profile={'name': 'John Doe'},
            situational_data={'location': 'New York'}
        )
        
        assert context.industry == Industry.RESTAURANT
        assert context.user_profile['name'] == 'John Doe'
        assert context.situational_data['location'] == 'New York'
        assert context.generated_at is not None
    
    def test_context_to_dict(self):
        """Test context serialization to dictionary."""
        context = IndustryContext(
            industry=Industry.HEALTHCARE,
            user_profile={'name': 'Jane Doe'},
            situational_data={'symptoms': 'headache'}
        )
        
        context_dict = context.to_dict()
        
        assert context_dict['industry'] == 'healthcare'
        assert context_dict['user_profile']['name'] == 'Jane Doe'
        assert context_dict['situational_data']['symptoms'] == 'headache'
        assert 'generated_at' in context_dict
    
    def test_context_validation(self):
        """Test context validation."""
        # Valid context
        valid_context = IndustryContext(
            industry=Industry.ECOMMERCE,
            user_profile={'name': 'Test User'},
            situational_data={'product': 'laptop'}
        )
        assert valid_context.is_valid()
        
        # Invalid context (missing required fields)
        invalid_context = IndustryContext(
            industry=Industry.ECOMMERCE,
            user_profile={},
            situational_data={}
        )
        assert not invalid_context.is_valid()
    
    def test_context_summary(self):
        """Test context summary generation."""
        context = IndustryContext(
            industry=Industry.FINANCIAL,
            user_profile={'name': 'Alice Smith'},
            situational_data={'transaction_type': 'loan'},
            preferences={'risk_level': 'low'}
        )
        
        summary = context.get_context_summary()
        assert 'Alice Smith' in summary
        assert 'transaction_type' in summary
        assert 'Preferences: 1 items' in summary


class TestBaseContextFactory:
    """Test BaseContextFactory abstract class."""
    
    def test_factory_initialization(self):
        """Test factory initialization."""
        from faker import Faker
        faker = Faker()
        factory = MockContextFactory(faker)
        
        assert factory.faker == faker
        assert factory.industry == Industry.RESTAURANT
        assert factory.logger is not None
    
    def test_context_generation(self):
        """Test complete context generation."""
        from faker import Faker
        faker = Faker()
        factory = MockContextFactory(faker)
        
        context = factory.generate_context()
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.RESTAURANT
        assert context.user_profile
        assert context.situational_data
        assert context.preferences
        assert context.history
        assert context.constraints
        assert context.metadata
    
    def test_context_validation(self):
        """Test context validation."""
        from faker import Faker
        faker = Faker()
        factory = MockContextFactory(faker)
        
        # Generate valid context
        context = factory.generate_context()
        errors = factory.validate_context(context)
        assert len(errors) == 0
        
        # Test invalid context
        invalid_context = IndustryContext(
            industry=Industry.HEALTHCARE,  # Wrong industry
            user_profile={},  # Missing name
            situational_data={}  # Empty
        )
        errors = factory.validate_context(invalid_context)
        assert len(errors) > 0
        assert any('industry mismatch' in error for error in errors)
        assert any('missing name' in error for error in errors)


class TestContextService:
    """Test ContextService main class."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        service = ContextService()
        
        assert service.faker is not None
        assert service.settings is not None
        assert service.logger is not None
        assert isinstance(service._context_cache, dict)
        assert isinstance(service._cache_timestamps, dict)
        assert isinstance(service._factories, dict)
    
    def test_factory_registration(self):
        """Test factory registration."""
        service = ContextService()
        
        # Should have all factories registered automatically
        available = service.get_available_industries()
        assert len(available) == 6  # All 6 industries should be registered
        
        # Register additional mock factory (should replace existing)
        service.register_factory(MockContextFactory)
        
        # Should still have restaurant factory (now the mock one)
        available = service.get_available_industries()
        assert Industry.RESTAURANT in available
    
    def test_context_generation(self):
        """Test context generation."""
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        context = service.generate_context(Industry.RESTAURANT)
        
        assert isinstance(context, IndustryContext)
        assert context.industry == Industry.RESTAURANT
        assert context.is_valid()
    
    def test_context_caching(self):
        """Test context caching mechanism."""
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        # Generate context (should be cached)
        context1 = service.generate_context(Industry.RESTAURANT)
        
        # Generate again (should use cache)
        context2 = service.generate_context(Industry.RESTAURANT)
        
        # Should be the same object (from cache)
        assert context1 is context2
        
        # Force refresh should generate new context
        context3 = service.refresh_context(Industry.RESTAURANT)
        assert context3 is not context1
    
    def test_context_validation_error(self):
        """Test context validation error handling."""
        service = ContextService()
        
        # Clear all factories to test error handling
        service._factories.clear()
        
        # Try to generate context for unregistered industry
        with pytest.raises(ContextValidationError) as exc_info:
            service.generate_context(Industry.HEALTHCARE)
        
        assert "No factory registered" in str(exc_info.value)
        assert exc_info.value.industry == Industry.HEALTHCARE
    
    def test_quality_scoring(self):
        """Test context quality scoring."""
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        context = service.generate_context(Industry.RESTAURANT)
        score = service.get_context_quality_score(context)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be reasonably high quality
    
    def test_cache_management(self):
        """Test cache management operations."""
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        # Generate context to populate cache
        service.generate_context(Industry.RESTAURANT)
        
        # Check cache status
        status = service.get_cache_status()
        assert 'restaurant' in status['cached_industries']
        assert len(status['cache_timestamps']) == 1
        
        # Clear specific cache
        service.clear_cache(Industry.RESTAURANT)
        status = service.get_cache_status()
        assert len(status['cached_industries']) == 0
    
    def test_faker_seed(self):
        """Test Faker seed functionality."""
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        # Set seed and generate context
        service.set_faker_seed(12345)
        context1 = service.generate_context(Industry.RESTAURANT, force_refresh=True)
        
        # Reset seed and generate again
        service.set_faker_seed(12345)
        context2 = service.generate_context(Industry.RESTAURANT, force_refresh=True)
        
        # Should generate similar data (names might be the same)
        assert context1.user_profile['name'] == context2.user_profile['name']
    
    @patch('services.context_service.get_settings')
    def test_cache_ttl(self, mock_get_settings):
        """Test cache TTL functionality."""
        # Mock settings with short TTL
        mock_settings = Mock()
        mock_settings.context_refresh_interval = 1  # 1 second TTL
        mock_get_settings.return_value = mock_settings
        
        service = ContextService()
        service.register_factory(MockContextFactory)
        
        # Generate context
        context1 = service.generate_context(Industry.RESTAURANT)
        
        # Immediately should use cache
        context2 = service.generate_context(Industry.RESTAURANT)
        assert context1 is context2
        
        # Manually expire cache by setting old timestamp
        old_time = datetime.now(timezone.utc) - timedelta(seconds=2)
        service._cache_timestamps[Industry.RESTAURANT] = old_time
        
        # Should generate new context now
        context3 = service.generate_context(Industry.RESTAURANT)
        assert context3 is not context1


if __name__ == '__main__':
    pytest.main([__file__])