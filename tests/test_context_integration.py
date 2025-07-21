"""
Integration tests for complete context service with all factories.
"""
import pytest
from services.context_service import ContextService, Industry


class TestContextServiceIntegration:
    """Test complete context service integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ContextService()
    
    def test_all_industries_registered(self):
        """Test that all expected industries are registered."""
        available = self.service.get_available_industries()
        
        expected_industries = [
            Industry.RESTAURANT,
            Industry.HEALTHCARE,
            Industry.ECOMMERCE,
            Industry.FINANCIAL,
            Industry.EDUCATION,
            Industry.REAL_ESTATE
        ]
        
        assert len(available) == len(expected_industries)
        for industry in expected_industries:
            assert industry in available
    
    def test_generate_context_for_all_industries(self):
        """Test context generation for all industries."""
        available = self.service.get_available_industries()
        
        for industry in available:
            context = self.service.generate_context(industry)
            
            # Basic validation
            assert context.industry == industry
            assert context.is_valid()
            
            # Quality check
            quality_score = self.service.get_context_quality_score(context)
            assert quality_score > 0.5, f"Low quality score for {industry.value}: {quality_score}"
    
    def test_context_refresh_functionality(self):
        """Test context refresh functionality."""
        # Generate initial contexts
        initial_contexts = {}
        for industry in self.service.get_available_industries():
            initial_contexts[industry] = self.service.generate_context(industry)
        
        # Refresh all contexts
        refreshed_contexts = self.service.refresh_all_contexts()
        
        # Check that we got refreshed contexts for all industries
        assert len(refreshed_contexts) == len(initial_contexts)
        
        # Check that refreshed contexts are different objects
        for industry in initial_contexts:
            assert refreshed_contexts[industry] is not initial_contexts[industry]
            assert refreshed_contexts[industry].generated_at != initial_contexts[industry].generated_at
    
    def test_cache_functionality(self):
        """Test caching functionality across industries."""
        # Generate contexts (should be cached)
        contexts1 = {}
        for industry in self.service.get_available_industries():
            contexts1[industry] = self.service.generate_context(industry)
        
        # Generate again (should use cache)
        contexts2 = {}
        for industry in self.service.get_available_industries():
            contexts2[industry] = self.service.generate_context(industry)
        
        # Should be same objects (from cache)
        for industry in contexts1:
            assert contexts1[industry] is contexts2[industry]
        
        # Check cache status
        cache_status = self.service.get_cache_status()
        assert len(cache_status['cached_industries']) == len(self.service.get_available_industries())
    
    def test_context_validation_across_industries(self):
        """Test context validation across all industries."""
        for industry in self.service.get_available_industries():
            context = self.service.generate_context(industry)
            
            # Validate using service
            errors = self.service.validate_context(context)
            assert len(errors) == 0, f"Validation errors for {industry.value}: {errors}"
    
    def test_context_quality_scoring(self):
        """Test quality scoring across all industries."""
        quality_scores = {}
        
        for industry in self.service.get_available_industries():
            context = self.service.generate_context(industry)
            score = self.service.get_context_quality_score(context)
            quality_scores[industry] = score
            
            # All contexts should have reasonable quality
            assert 0.5 <= score <= 1.0, f"Quality score for {industry.value} is {score}"
        
        # Log quality scores for reference
        print("\nContext Quality Scores:")
        for industry, score in quality_scores.items():
            print(f"  {industry.value}: {score:.2f}")
    
    def test_faker_seed_consistency(self):
        """Test that Faker seed produces consistent results."""
        # Set seed and generate contexts
        self.service.set_faker_seed(12345)
        contexts1 = {}
        for industry in [Industry.RESTAURANT, Industry.HEALTHCARE]:  # Test subset for speed
            contexts1[industry] = self.service.generate_context(industry, force_refresh=True)
        
        # Reset seed and generate again
        self.service.set_faker_seed(12345)
        contexts2 = {}
        for industry in [Industry.RESTAURANT, Industry.HEALTHCARE]:
            contexts2[industry] = self.service.generate_context(industry, force_refresh=True)
        
        # Should have same user names (high probability with same seed)
        for industry in contexts1:
            name1 = contexts1[industry].user_profile.get('name')
            name2 = contexts2[industry].user_profile.get('name')
            assert name1 == name2, f"Names differ for {industry.value}: {name1} vs {name2}"
    
    def test_context_serialization_all_industries(self):
        """Test context serialization for all industries."""
        for industry in self.service.get_available_industries():
            context = self.service.generate_context(industry)
            context_dict = context.to_dict()
            
            # Check serialization completeness
            assert isinstance(context_dict, dict)
            assert context_dict['industry'] == industry.value
            assert 'user_profile' in context_dict
            assert 'situational_data' in context_dict
            assert 'preferences' in context_dict
            assert 'history' in context_dict
            assert 'constraints' in context_dict
            assert 'metadata' in context_dict
            assert 'generated_at' in context_dict
    
    def test_service_string_representations(self):
        """Test string representations of service."""
        # Generate some contexts to populate cache
        for industry in list(self.service.get_available_industries())[:2]:
            self.service.generate_context(industry)
        
        # Test string representations
        str_repr = str(self.service)
        assert 'ContextService' in str_repr
        assert 'industries=' in str_repr
        assert 'cached=' in str_repr
        
        repr_str = repr(self.service)
        assert 'ContextService' in repr_str
        assert 'locale=' in repr_str
        assert 'industries=' in repr_str


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])