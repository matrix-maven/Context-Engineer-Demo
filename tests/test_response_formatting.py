"""
Test response formatting and structure improvements for customer-focused prompts.

This module tests that all industry templates include proper response formatting
guidelines and that the generated prompts instruct the AI to provide well-structured,
conversational responses with clear call-to-action elements.
"""
import pytest
from services.prompt_service import get_prompt_service, Industry, PromptType


class TestResponseFormatting:
    """Test response formatting improvements across all industries."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.prompt_service = get_prompt_service()
        self.industries = [
            Industry.RESTAURANT,
            Industry.HEALTHCARE,
            Industry.ECOMMERCE,
            Industry.FINANCIAL,
            Industry.EDUCATION,
            Industry.REAL_ESTATE
        ]
    
    def test_generic_templates_include_formatting_guidelines(self):
        """Test that all generic templates include response formatting guidelines."""
        for industry in self.industries:
            template_name = f"generic_{industry.value}"
            template = self.prompt_service.get_template(template_name)
            
            assert template is not None, f"Template {template_name} not found"
            
            # Check for formatting guidelines section
            assert "RESPONSE FORMAT GUIDELINES:" in template.template, \
                f"Template {template_name} missing formatting guidelines"
            
            # Check for specific formatting instructions
            formatting_keywords = [
                "Start with",
                "Structure your response",
                "Include specific",
                "Use",
                "End with",
                "Keep"
            ]
            
            for keyword in formatting_keywords:
                assert keyword in template.template, \
                    f"Template {template_name} missing formatting instruction: {keyword}"
    
    def test_contextual_templates_include_formatting_guidelines(self):
        """Test that all contextual templates include response formatting guidelines."""
        for industry in self.industries:
            template_name = f"contextual_{industry.value}"
            template = self.prompt_service.get_template(template_name)
            
            assert template is not None, f"Template {template_name} not found"
            
            # Check for formatting guidelines section
            assert "RESPONSE FORMAT GUIDELINES:" in template.template, \
                f"Template {template_name} missing formatting guidelines"
            
            # Check for personalization instructions
            personalization_keywords = [
                "personalized",
                "references their",
                "context naturally",
                "profile"
            ]
            
            for keyword in personalization_keywords:
                assert keyword in template.template.lower(), \
                    f"Template {template_name} missing personalization instruction: {keyword}"
    
    def test_conversational_language_patterns(self):
        """Test that templates include conversational language patterns."""
        conversational_indicators = [
            "friendly",
            "conversational",
            "warm",
            "personal",
            "engaging",
            "caring",
            "supportive",
            "helpful"
        ]
        
        for industry in self.industries:
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                
                # Check that at least one conversational indicator is present
                template_lower = template.template.lower()
                has_conversational_language = any(
                    indicator in template_lower for indicator in conversational_indicators
                )
                
                assert has_conversational_language, \
                    f"Template {template_name} lacks conversational language patterns"
    
    def test_call_to_action_elements(self):
        """Test that templates include clear call-to-action elements."""
        cta_indicators = [
            "call-to-action",
            "Would you like",
            "Let me know",
            "I can help",
            "Ready to",
            "Shall we",
            "Please",
            "Would you"
        ]
        
        for industry in self.industries:
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                
                # Check that call-to-action guidance is present
                has_cta_guidance = any(
                    indicator in template.template for indicator in cta_indicators
                )
                
                assert has_cta_guidance, \
                    f"Template {template_name} lacks call-to-action guidance"
    
    def test_structured_response_instructions(self):
        """Test that templates include instructions for structured responses."""
        structure_keywords = [
            "bullet points",
            "sections",
            "organized",
            "clear sections",
            "numbered lists",
            "structure"
        ]
        
        for industry in self.industries:
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                
                # Check that structure guidance is present
                template_lower = template.template.lower()
                has_structure_guidance = any(
                    keyword in template_lower for keyword in structure_keywords
                )
                
                assert has_structure_guidance, \
                    f"Template {template_name} lacks structured response instructions"
    
    def test_industry_specific_formatting_requirements(self):
        """Test industry-specific formatting requirements."""
        industry_requirements = {
            Industry.RESTAURANT: ["cuisine", "atmosphere", "price range", "reservations"],
            Industry.HEALTHCARE: ["medical", "health", "healthcare provider", "educational purposes"],
            Industry.ECOMMERCE: ["product", "shopping", "cart", "recommendations"],
            Industry.FINANCIAL: ["financial", "advisor", "investment", "qualified financial professionals"],
            Industry.EDUCATION: ["learning", "academic", "educational", "study"],
            Industry.REAL_ESTATE: ["property", "real estate", "market", "neighborhood"]
        }
        
        for industry, requirements in industry_requirements.items():
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                
                template_lower = template.template.lower()
                for requirement in requirements:
                    assert requirement.lower() in template_lower, \
                        f"Template {template_name} missing industry requirement: {requirement}"
    
    def test_professional_tone_consistency(self):
        """Test that professional tone is consistent across templates."""
        professional_indicators = {
            Industry.RESTAURANT: ["concierge", "dining experience", "knowledgeable"],
            Industry.HEALTHCARE: ["healthcare professional", "caring", "medical"],
            Industry.ECOMMERCE: ["shopping assistant", "personal", "helpful"],
            Industry.FINANCIAL: ["financial advisor", "professional", "trustworthy"],
            Industry.EDUCATION: ["educator", "academic advisor", "supportive"],
            Industry.REAL_ESTATE: ["real estate agent", "professional", "knowledgeable"]
        }
        
        for industry, indicators in professional_indicators.items():
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                
                template_lower = template.template.lower()
                for indicator in indicators:
                    assert indicator.lower() in template_lower, \
                        f"Template {template_name} missing professional indicator: {indicator}"
    
    def test_response_style_metadata(self):
        """Test that templates have appropriate response_style metadata."""
        expected_styles = {
            Industry.RESTAURANT: "helpful",
            Industry.HEALTHCARE: "caring",
            Industry.ECOMMERCE: "friendly",
            Industry.FINANCIAL: "professional",
            Industry.EDUCATION: "helpful",
            Industry.REAL_ESTATE: "professional"
        }
        
        for industry, expected_style in expected_styles.items():
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                assert template.response_style == expected_style, \
                    f"Template {template_name} has incorrect response_style: {template.response_style}, expected: {expected_style}"
    
    def test_customer_focus_flag(self):
        """Test that all industry templates have customer_focus set to True."""
        for industry in self.industries:
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                assert template.customer_focus is True, \
                    f"Template {template_name} should have customer_focus=True"
    
    def test_professional_role_defined(self):
        """Test that all industry templates have professional_role defined."""
        expected_roles = {
            Industry.RESTAURANT: "concierge service",
            Industry.HEALTHCARE: "medical practitioner",
            Industry.ECOMMERCE: "shopping assistant",
            Industry.FINANCIAL: "financial advisor",
            Industry.EDUCATION: "educator/advisor",
            Industry.REAL_ESTATE: "real estate agent"
        }
        
        for industry, expected_role in expected_roles.items():
            for prompt_type in ["generic", "contextual"]:
                template_name = f"{prompt_type}_{industry.value}"
                template = self.prompt_service.get_template(template_name)
                
                assert template is not None, f"Template {template_name} not found"
                assert template.professional_role == expected_role, \
                    f"Template {template_name} has incorrect professional_role: {template.professional_role}, expected: {expected_role}"


class TestFormattingIntegration:
    """Test integration of formatting improvements with prompt generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.prompt_service = get_prompt_service()
    
    def test_generic_prompt_generation_includes_formatting(self):
        """Test that generated generic prompts include formatting guidelines."""
        test_query = "I need help with my shopping"
        
        for industry in [Industry.ECOMMERCE, Industry.RESTAURANT, Industry.HEALTHCARE]:
            prompt = self.prompt_service.generate_generic_prompt(test_query, industry)
            
            # Check that formatting guidelines are included
            assert "RESPONSE FORMAT GUIDELINES:" in prompt, \
                f"Generated prompt for {industry} missing formatting guidelines"
            
            # Check that the query is included
            assert test_query in prompt, \
                f"Generated prompt for {industry} missing original query"
    
    def test_contextual_prompt_generation_includes_formatting(self):
        """Test that generated contextual prompts include formatting guidelines."""
        test_query = "What should I buy?"
        test_context = {
            "user_id": "test123",
            "preferences": ["electronics", "books"],
            "budget": "$500"
        }
        
        for industry in [Industry.ECOMMERCE, Industry.FINANCIAL]:
            prompt = self.prompt_service.generate_contextual_prompt(
                test_query, test_context, industry
            )
            
            # Check that formatting guidelines are included
            assert "RESPONSE FORMAT GUIDELINES:" in prompt, \
                f"Generated contextual prompt for {industry} missing formatting guidelines"
            
            # Check that personalization instructions are included
            assert "personalized" in prompt.lower(), \
                f"Generated contextual prompt for {industry} missing personalization instructions"
    
    def test_system_messages_maintain_professional_roles(self):
        """Test that system messages maintain professional role definitions."""
        professional_roles = {
            Industry.RESTAURANT: "concierge service",
            Industry.HEALTHCARE: "healthcare professional",
            Industry.ECOMMERCE: "shopping assistant",
            Industry.FINANCIAL: "financial advisor",
            Industry.EDUCATION: "educator",
            Industry.REAL_ESTATE: "real estate agent"
        }
        
        for industry, expected_role in professional_roles.items():
            system_message = self.prompt_service.generate_system_message(industry)
            
            assert expected_role.lower() in system_message.lower(), \
                f"System message for {industry} missing professional role: {expected_role}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])