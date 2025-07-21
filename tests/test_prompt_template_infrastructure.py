"""
Test cases for the updated PromptTemplate infrastructure with customer-focused features.
"""
import pytest
from services.prompt_service import PromptTemplate, PromptType, Industry, get_prompt_service


class TestPromptTemplateInfrastructure:
    """Test the new infrastructure features for customer-focused prompts."""
    
    def test_new_fields_initialization(self):
        """Test that new fields are properly initialized."""
        template = PromptTemplate(
            name="test_template",
            template="Test template with {query}",
            prompt_type=PromptType.GENERIC,
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly",
            personalization_elements=["history", "preferences"]
        )
        
        assert template.professional_role == "shopping assistant"
        assert template.customer_focus is True
        assert template.response_style == "friendly"
        assert template.personalization_elements == ["history", "preferences"]
    
    def test_default_field_values(self):
        """Test that new fields have appropriate default values."""
        template = PromptTemplate(
            name="test_template",
            template="Test template",
            prompt_type=PromptType.GENERIC
        )
        
        assert template.professional_role == ""
        assert template.customer_focus is False
        assert template.response_style == "professional"
        assert template.personalization_elements == []
    
    def test_customer_focused_validation_success(self):
        """Test validation passes for properly customer-focused templates."""
        template = PromptTemplate(
            name="good_customer_template",
            template="I'm here to help you find the perfect product. What can I assist you with today?",
            prompt_type=PromptType.GENERIC,
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly"
        )
        
        errors = template.validate()
        assert len(errors) == 0
    
    def test_customer_focused_validation_missing_role(self):
        """Test validation fails when customer_focus is True but professional_role is empty."""
        template = PromptTemplate(
            name="missing_role_template",
            template="I can help you with your needs",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role=""  # Empty role should trigger error
        )
        
        errors = template.validate()
        assert any("must specify a professional_role" in error for error in errors)
    
    def test_customer_focused_validation_business_language(self):
        """Test validation detects business consultation language."""
        template = PromptTemplate(
            name="business_template",
            template="I provide business consultation and best practices for your operations",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role="consultant"
        )
        
        errors = template.validate()
        business_errors = [e for e in errors if "business consultation language" in e]
        assert len(business_errors) >= 2  # Should detect both "business consultation" and "best practices for"
    
    def test_customer_focused_validation_missing_service_language(self):
        """Test validation detects missing customer service language."""
        # Test with a template that has clear service language
        good_template = PromptTemplate(
            name="good_service_template",
            template="I can help you find the perfect product for your needs",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role="advisor"
        )
        
        errors = good_template.validate()
        service_errors = [e for e in errors if "customer service language" in e]
        assert len(service_errors) == 0
        
        # Test with truly missing service language
        bad_template = PromptTemplate(
            name="truly_bad_template",
            template="This is just some text without any service words",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role="advisor"
        )
        
        bad_errors = bad_template.validate()
        service_errors = [e for e in bad_errors if "customer service language" in e]
        assert len(service_errors) > 0
    
    def test_response_style_validation(self):
        """Test validation of response_style field."""
        # Valid style
        template = PromptTemplate(
            name="valid_style_template",
            template="Test template",
            prompt_type=PromptType.GENERIC,
            response_style="conversational"
        )
        errors = template.validate()
        style_errors = [e for e in errors if "Invalid response_style" in e]
        assert len(style_errors) == 0
        
        # Invalid style
        template = PromptTemplate(
            name="invalid_style_template",
            template="Test template",
            prompt_type=PromptType.GENERIC,
            response_style="invalid_style"
        )
        errors = template.validate()
        style_errors = [e for e in errors if "Invalid response_style" in e]
        assert len(style_errors) == 1
    
    def test_serialization_with_new_fields(self):
        """Test that serialization includes all new fields."""
        template = PromptTemplate(
            name="serialization_test",
            template="Test template with {query}",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.ECOMMERCE,
            professional_role="personal shopper",
            customer_focus=True,
            response_style="caring",
            personalization_elements=["purchase_history", "preferences", "budget"]
        )
        
        data = template.to_dict()
        
        assert data["professional_role"] == "personal shopper"
        assert data["customer_focus"] is True
        assert data["response_style"] == "caring"
        assert data["personalization_elements"] == ["purchase_history", "preferences", "budget"]
    
    def test_deserialization_with_new_fields(self):
        """Test that deserialization properly handles new fields."""
        data = {
            "name": "deserialization_test",
            "template": "Test template",
            "prompt_type": "generic",
            "industry": "healthcare",
            "professional_role": "medical practitioner",
            "customer_focus": True,
            "response_style": "caring",
            "personalization_elements": ["medical_history", "conditions"]
        }
        
        template = PromptTemplate.from_dict(data)
        
        assert template.professional_role == "medical practitioner"
        assert template.customer_focus is True
        assert template.response_style == "caring"
        assert template.personalization_elements == ["medical_history", "conditions"]
    
    def test_deserialization_with_missing_new_fields(self):
        """Test that deserialization handles missing new fields with defaults."""
        data = {
            "name": "legacy_template",
            "template": "Legacy template",
            "prompt_type": "generic"
        }
        
        template = PromptTemplate.from_dict(data)
        
        assert template.professional_role == ""
        assert template.customer_focus is False
        assert template.response_style == "professional"
        assert template.personalization_elements == []
    
    def test_prompt_service_compatibility(self):
        """Test that PromptService still works with updated templates."""
        service = get_prompt_service()
        
        # Register a customer-focused template
        customer_template = PromptTemplate(
            name="test_customer_service",
            template="As a {professional_role}, I'm here to help with: {query}",
            prompt_type=PromptType.GENERIC,
            industry=Industry.ECOMMERCE,
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly"
        )
        
        service.register_template(customer_template)
        
        # Verify it was registered
        retrieved = service.get_template("test_customer_service")
        assert retrieved is not None
        assert retrieved.professional_role == "shopping assistant"
        assert retrieved.customer_focus is True
    
    def test_existing_templates_still_work(self):
        """Test that existing templates without new fields still function."""
        service = get_prompt_service()
        
        # Get an existing template
        template = service.get_template("generic_default")
        assert template is not None
        
        # Verify it has default values for new fields
        assert template.professional_role == ""
        assert template.customer_focus is False
        assert template.response_style == "professional"
        assert template.personalization_elements == []
        
        # Verify it still renders correctly
        prompt = service.generate_generic_prompt("test query")
        assert "test query" in prompt


class TestCustomerFocusedLanguageValidation:
    """Test the customer-focused language validation in detail."""
    
    @pytest.mark.parametrize("phrase", [
        "business consultant",
        "business consultation",
        "business advice",
        "best practices for",
        "industry guidance",
        "operational details",
        "business operations",
        "management consultant",
        "practice management",
        "business model",
        "operational requirements"
    ])
    def test_business_consultation_phrases_detected(self, phrase):
        """Test that specific business consultation phrases are detected."""
        template = PromptTemplate(
            name="test_template",
            template=f"I provide {phrase} to help your company",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role="consultant"
        )
        
        errors = template.validate()
        business_errors = [e for e in errors if phrase in e.lower()]
        assert len(business_errors) > 0
    
    @pytest.mark.parametrize("word", [
        "help", "assist", "recommend", "guide", "support",
        "customer", "client", "user", "personalized", "specific"
    ])
    def test_customer_service_words_accepted(self, word):
        """Test that customer service words are properly recognized."""
        template = PromptTemplate(
            name="test_template",
            template=f"I will {word} you with your needs",
            prompt_type=PromptType.GENERIC,
            customer_focus=True,
            professional_role="assistant"
        )
        
        errors = template.validate()
        service_errors = [e for e in errors if "customer service language" in e]
        assert len(service_errors) == 0