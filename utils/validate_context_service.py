#!/usr/bin/env python3
"""
Validation script for Context Service implementation.
This script tests the Context Service with realistic data generation and validation.
"""
import os
import sys
from typing import Dict, Any

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_context_service():
    """Test Context Service implementation comprehensively."""
    print("🔍 Testing Context Service Implementation")
    print("=" * 50)
    
    try:
        from services.context_service import ContextService, Industry, IndustryContext, ContextValidationError
        print("✅ Context Service imports successful")
    except ImportError as e:
        print(f"❌ Failed to import Context Service: {e}")
        return False
    
    # Test basic service initialization
    try:
        service = ContextService()
        print("✅ Context Service initialized successfully")
    except Exception as e:
        print(f"❌ Context Service initialization failed: {e}")
        return False
    
    # Test service with custom configuration
    try:
        service_custom = ContextService(locale='en_US', seed=42)
        print("✅ Context Service with custom config initialized")
    except Exception as e:
        print(f"❌ Custom configuration failed: {e}")
        return False
    
    # Test available industries
    try:
        industries = list(Industry)
        print(f"✅ Available industries: {[i.value for i in industries]}")
        
        if len(industries) < 6:
            print(f"⚠️  Expected at least 6 industries, found {len(industries)}")
    except Exception as e:
        print(f"❌ Failed to get industries: {e}")
        return False
    
    # Test IndustryContext data model
    try:
        from datetime import datetime, timezone
        
        # Create a test context
        test_context = IndustryContext(
            industry=Industry.RESTAURANT,
            user_profile={"name": "Test User", "age": 30},
            situational_data={"party_size": 4, "occasion": "dinner"},
            preferences={"cuisine": "Italian"},
            history={"visits": ["Restaurant A", "Restaurant B"]},
            constraints={"budget": "$50-80"},
            metadata={"test": True}
        )
        
        # Test context methods
        assert test_context.is_valid()
        assert test_context.industry == Industry.RESTAURANT
        
        context_dict = test_context.to_dict()
        assert isinstance(context_dict, dict)
        assert context_dict['industry'] == 'restaurant'
        
        summary = test_context.get_context_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        print("✅ IndustryContext data model working correctly")
        
    except Exception as e:
        print(f"❌ IndustryContext testing failed: {e}")
        return False
    
    # Test Faker integration
    try:
        from faker import Faker
        faker = Faker('en_US')
        
        # Test basic Faker functionality
        name = faker.name()
        city = faker.city()
        
        assert isinstance(name, str) and len(name) > 0
        assert isinstance(city, str) and len(city) > 0
        
        print("✅ Faker integration working")
        
    except ImportError:
        print("❌ Faker library not available. Install with: pip install faker>=19.0.0")
        return False
    except Exception as e:
        print(f"❌ Faker integration failed: {e}")
        return False
    
    # Test service methods without factories (since they're not implemented yet)
    try:
        # Test cache status
        cache_status = service.get_cache_status()
        assert isinstance(cache_status, dict)
        assert 'cached_industries' in cache_status
        assert 'registered_factories' in cache_status
        
        print("✅ Cache status method working")
        
        # Test available industries method
        available = service.get_available_industries()
        assert isinstance(available, list)
        
        print("✅ Available industries method working")
        
        # Test Faker seed setting
        service.set_faker_seed(12345)
        print("✅ Faker seed setting working")
        
        # Test cache clearing
        service.clear_cache()
        print("✅ Cache clearing working")
        
    except Exception as e:
        print(f"❌ Service methods testing failed: {e}")
        return False
    
    # Test error handling
    try:
        # Test ContextValidationError
        error = ContextValidationError(
            "Test error",
            industry=Industry.RESTAURANT,
            validation_errors=["Error 1", "Error 2"]
        )
        
        assert str(error) == "Test error"
        assert error.industry == Industry.RESTAURANT
        assert len(error.validation_errors) == 2
        
        print("✅ Error handling working correctly")
        
    except Exception as e:
        print(f"❌ Error handling testing failed: {e}")
        return False
    
    # Test string representations
    try:
        service_str = str(service)
        service_repr = repr(service)
        
        assert "ContextService" in service_str
        assert "ContextService" in service_repr
        
        print("✅ String representations working")
        
    except Exception as e:
        print(f"❌ String representation testing failed: {e}")
        return False
    
    # Test configuration integration
    try:
        from config.settings import get_settings
        
        settings = get_settings()
        
        # Check if context-related settings are available
        if hasattr(settings, 'context_refresh_interval'):
            print(f"✅ Context refresh interval: {settings.context_refresh_interval}s")
        
        if hasattr(settings, 'max_context_size'):
            print(f"✅ Max context size: {settings.max_context_size}")
        
    except Exception as e:
        print(f"⚠️  Configuration integration test failed: {e}")
        # This is not critical for basic functionality
    
    print("\n🎉 All Context Service core tests passed!")
    print("\n📝 Note: Context factories are not yet implemented.")
    print("   The service infrastructure is ready for factory registration.")
    
    return True


def test_context_quality_scoring():
    """Test context quality scoring functionality."""
    print("\n🔍 Testing Context Quality Scoring")
    print("-" * 30)
    
    try:
        from services.context_service import ContextService, Industry, IndustryContext
        
        service = ContextService()
        
        # Test with minimal context (low quality)
        minimal_context = IndustryContext(
            industry=Industry.RESTAURANT,
            user_profile={},
            situational_data={},
            preferences={},
            history={},
            constraints={}
        )
        
        minimal_score = service.get_context_quality_score(minimal_context)
        print(f"✅ Minimal context score: {minimal_score:.2f}")
        
        # Test with rich context (high quality)
        rich_context = IndustryContext(
            industry=Industry.RESTAURANT,
            user_profile={
                "name": "John Doe",
                "age": 35,
                "location": "New York, NY",
                "dietary_restrictions": ["vegetarian"]
            },
            situational_data={
                "party_size": 4,
                "occasion": "anniversary",
                "time_preference": "evening",
                "budget": "$100-150"
            },
            preferences={
                "cuisine": ["Italian", "French"],
                "ambiance": "romantic",
                "service_style": "fine_dining"
            },
            history={
                "past_visits": ["Restaurant A", "Restaurant B"],
                "favorite_dishes": ["pasta", "wine"],
                "reviews_written": 5
            },
            constraints={
                "budget_limit": 150,
                "time_limit": "2 hours",
                "accessibility": "wheelchair_accessible"
            }
        )
        
        rich_score = service.get_context_quality_score(rich_context)
        print(f"✅ Rich context score: {rich_score:.2f}")
        
        # Verify rich context scores higher than minimal
        assert rich_score > minimal_score, f"Rich context should score higher: {rich_score} vs {minimal_score}"
        
        print("✅ Quality scoring working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Quality scoring test failed: {e}")
        return False


def test_reproducible_generation():
    """Test reproducible generation with seeds."""
    print("\n🔍 Testing Reproducible Generation")
    print("-" * 30)
    
    try:
        from services.context_service import ContextService
        
        # Create two services with same seed
        service1 = ContextService(seed=42)
        service2 = ContextService(seed=42)
        
        # Generate some data with Faker
        name1 = service1.faker.name()
        name2 = service2.faker.name()
        
        city1 = service1.faker.city()
        city2 = service2.faker.city()
        
        # Should be identical with same seed
        assert name1 == name2, f"Names should be identical: {name1} vs {name2}"
        assert city1 == city2, f"Cities should be identical: {city1} vs {city2}"
        
        print(f"✅ Reproducible generation working: {name1}, {city1}")
        
        # Test seed changing
        service1.set_faker_seed(123)
        service2.set_faker_seed(123)
        
        name3 = service1.faker.name()
        name4 = service2.faker.name()
        
        assert name3 == name4, f"Names should be identical after seed change: {name3} vs {name4}"
        assert name3 != name1, f"Names should be different with different seed: {name3} vs {name1}"
        
        print("✅ Seed changing working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Reproducible generation test failed: {e}")
        return False


def main():
    """Main validation function."""
    print("Context Service Validation")
    print("=" * 60)
    
    success = True
    
    # Run core tests
    if not test_context_service():
        success = False
    
    # Run quality scoring tests
    if not test_context_quality_scoring():
        success = False
    
    # Run reproducible generation tests
    if not test_reproducible_generation():
        success = False
    
    print("\n" + "=" * 60)
    
    if success:
        print("✅ All Context Service tests passed!")
        print("\n🚀 Context Service is ready for use!")
        print("\nNext steps:")
        print("   1. Implement context factories in services/context_factories.py")
        print("   2. Register factories with the service")
        print("   3. Test with real context generation")
        print("   4. Integrate with AI providers")
        sys.exit(0)
    else:
        print("❌ Some Context Service tests failed!")
        print("\nPlease fix the issues above before using the Context Service.")
        sys.exit(1)


if __name__ == "__main__":
    main()