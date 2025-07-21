"""
Prompt management system for AI service integration.

This module provides a comprehensive prompt template system with support for
generic and contextual responses, industry-specific variations, and validation utilities.
"""
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Callable
from enum import Enum
import logging

from config.settings import get_settings


class PromptType(str, Enum):
    """Types of prompts supported by the system."""
    GENERIC = "generic"
    CONTEXTUAL = "contextual"
    SYSTEM = "system"
    INDUSTRY_SPECIFIC = "industry_specific"


class Industry(str, Enum):
    """Supported industry types for specialized prompts."""
    RESTAURANT = "restaurant"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    FINANCIAL = "financial"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"


@dataclass
class PromptTemplate:
    """
    Template for generating prompts with variable substitution.
    
    Attributes:
        name: Unique identifier for the template
        template: Template string with placeholders
        prompt_type: Type of prompt (generic, contextual, etc.)
        industry: Industry specialization (optional)
        variables: Required variables for template substitution
        description: Human-readable description of the template
        metadata: Additional metadata for the template
        professional_role: The professional role the AI should assume (e.g., "shopping assistant", "medical practitioner")
        customer_focus: Whether this template is designed for customer-facing interactions
        response_style: Style of response (e.g., "conversational", "professional", "friendly")
        personalization_elements: List of context elements to use for personalization
    """
    name: str
    template: str
    prompt_type: PromptType
    industry: Optional[Industry] = None
    variables: List[str] = field(default_factory=list)
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    professional_role: str = ""
    customer_focus: bool = False
    response_style: str = "professional"
    personalization_elements: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Extract variables from template after initialization."""
        if not self.variables:
            self.variables = self._extract_variables()
    
    def _extract_variables(self) -> List[str]:
        """Extract variable names from template string."""
        # Find all {variable_name} patterns
        pattern = r'\{([^}]+)\}'
        matches = re.findall(pattern, self.template)
        return list(set(matches))  # Remove duplicates
    
    def render(self, **kwargs) -> str:
        """
        Render template with provided variables.
        
        Args:
            **kwargs: Variables to substitute in template
            
        Returns:
            Rendered template string
            
        Raises:
            ValueError: If required variables are missing
        """
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
        
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Template variable not provided: {e}")
        except Exception as e:
            raise ValueError(f"Template rendering failed: {e}")
    
    def validate(self) -> List[str]:
        """
        Validate template structure and return list of issues.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check for empty template
        if not self.template or not self.template.strip():
            errors.append("Template cannot be empty")
        
        # Check for unmatched braces
        open_braces = self.template.count('{')
        close_braces = self.template.count('}')
        if open_braces != close_braces:
            errors.append("Unmatched braces in template")
        
        # Check for invalid variable names
        for var in self.variables:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var):
                errors.append(f"Invalid variable name: {var}")
        
        # Check for reasonable template length
        if len(self.template) > 10000:
            errors.append("Template is too long (>10000 characters)")
        
        # Validate customer-focused language if customer_focus is True
        if self.customer_focus:
            customer_focus_errors = self._validate_customer_focused_language()
            errors.extend(customer_focus_errors)
        
        # Validate professional role is set for customer-focused templates
        if self.customer_focus and not self.professional_role.strip():
            errors.append("Customer-focused templates must specify a professional_role")
        
        # Validate response style
        valid_styles = ["conversational", "professional", "friendly", "caring", "helpful"]
        if self.response_style and self.response_style not in valid_styles:
            errors.append(f"Invalid response_style: {self.response_style}. Must be one of: {valid_styles}")
        
        return errors
    
    def _validate_customer_focused_language(self) -> List[str]:
        """
        Validate that customer-focused templates use appropriate language.
        
        Returns:
            List of validation error messages for customer focus
        """
        errors = []
        template_lower = self.template.lower()
        
        # Check for business consultation language that should be avoided
        business_consultation_phrases = [
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
        ]
        
        for phrase in business_consultation_phrases:
            if phrase in template_lower:
                errors.append(f"Customer-focused template should avoid business consultation language: '{phrase}'")
        
        # Check for customer service language that should be present
        if self.prompt_type in [PromptType.GENERIC, PromptType.CONTEXTUAL]:
            # Updated list with additional service words
            customer_service_indicators = [
                "help", "assist", "recommend", "guide", "support", 
                "customer", "client", "user", "personalized", "specific",
                "provide", "offer", "find", "show", "give"
            ]
            
            # Debug: Check what indicators are found
            found_indicators = [ind for ind in customer_service_indicators if ind in template_lower]
            
            has_customer_language = any(indicator in template_lower for indicator in customer_service_indicators)
            if not has_customer_language:
                errors.append("Customer-focused template should include customer service language (help, assist, recommend, etc.)")
            # Debug: Add info about found indicators
            elif found_indicators:
                # This is just for debugging - remove in production
                pass
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary for serialization."""
        return {
            'name': self.name,
            'template': self.template,
            'prompt_type': self.prompt_type.value,
            'industry': self.industry.value if self.industry else None,
            'variables': self.variables,
            'description': self.description,
            'metadata': self.metadata,
            'professional_role': self.professional_role,
            'customer_focus': self.customer_focus,
            'response_style': self.response_style,
            'personalization_elements': self.personalization_elements
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptTemplate':
        """Create template from dictionary."""
        return cls(
            name=data['name'],
            template=data['template'],
            prompt_type=PromptType(data['prompt_type']),
            industry=Industry(data['industry']) if data.get('industry') else None,
            variables=data.get('variables', []),
            description=data.get('description', ''),
            metadata=data.get('metadata', {}),
            professional_role=data.get('professional_role', ''),
            customer_focus=data.get('customer_focus', False),
            response_style=data.get('response_style', 'professional'),
            personalization_elements=data.get('personalization_elements', [])
        )


class PromptValidator:
    """Utility class for validating prompts and templates."""
    
    @staticmethod
    def validate_prompt_content(content: str) -> List[str]:
        """
        Validate prompt content for common issues.
        
        Args:
            content: Prompt content to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        if not content or not content.strip():
            issues.append("Prompt content cannot be empty")
            return issues
        
        # Check length
        if len(content) < 10:
            issues.append("Prompt is too short (minimum 10 characters)")
        elif len(content) > 8000:
            issues.append("Prompt is too long (maximum 8000 characters)")
        
        # Check for potential injection patterns
        suspicious_patterns = [
            r'ignore\s+previous\s+instructions',
            r'forget\s+everything',
            r'system\s*:\s*you\s+are',
            r'<\s*script\s*>',
            r'javascript\s*:',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Potentially suspicious content detected: {pattern}")
        
        # Check for excessive repetition
        words = content.lower().split()
        if len(words) > 10:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            max_count = max(word_counts.values())
            if max_count > len(words) * 0.3:  # More than 30% repetition
                issues.append("Excessive word repetition detected")
        
        return issues
    
    @staticmethod
    def validate_context_data(context: Dict[str, Any]) -> List[str]:
        """
        Validate context data structure.
        
        Args:
            context: Context data to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        if not isinstance(context, dict):
            issues.append("Context must be a dictionary")
            return issues
        
        # Check for reasonable size
        try:
            context_str = json.dumps(context)
            if len(context_str) > 50000:
                issues.append("Context data is too large (>50KB)")
        except (TypeError, ValueError):
            issues.append("Context data is not JSON serializable")
        
        # Check for nested depth
        def check_depth(obj, current_depth=0):
            if current_depth > 10:
                return True
            if isinstance(obj, dict):
                return any(check_depth(v, current_depth + 1) for v in obj.values())
            elif isinstance(obj, list):
                return any(check_depth(item, current_depth + 1) for item in obj)
            return False
        
        if check_depth(context):
            issues.append("Context data is too deeply nested (>10 levels)")
        
        return issues


class PromptService:
    """
    Main service for managing prompt templates and generation.
    
    This service provides centralized prompt management with support for
    template registration, rendering, validation, and industry-specific variations.
    """
    
    def __init__(self):
        """Initialize prompt service with default templates."""
        self.templates: Dict[str, PromptTemplate] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self._load_default_templates()
    
    def register_template(self, template: PromptTemplate) -> None:
        """
        Register a new prompt template.
        
        Args:
            template: Template to register
            
        Raises:
            ValueError: If template is invalid or name conflicts
        """
        # Validate template
        errors = template.validate()
        if errors:
            raise ValueError(f"Invalid template '{template.name}': {errors}")
        
        # Check for name conflicts
        if template.name in self.templates:
            self.logger.warning(f"Overwriting existing template: {template.name}")
        
        self.templates[template.name] = template
        self.logger.debug(f"Registered template: {template.name}")
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Get template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template if found, None otherwise
        """
        return self.templates.get(name)
    
    def list_templates(self, prompt_type: Optional[PromptType] = None,
                      industry: Optional[Industry] = None) -> List[PromptTemplate]:
        """
        List templates with optional filtering.
        
        Args:
            prompt_type: Filter by prompt type
            industry: Filter by industry
            
        Returns:
            List of matching templates
        """
        templates = list(self.templates.values())
        
        if prompt_type:
            templates = [t for t in templates if t.prompt_type == prompt_type]
        
        if industry:
            templates = [t for t in templates if t.industry == industry]
        
        return templates
    
    def generate_generic_prompt(self, query: str, industry: Optional[Industry] = None) -> str:
        """
        Generate generic prompt for a query.
        
        Args:
            query: User query
            industry: Industry context (optional)
            
        Returns:
            Generated prompt string
        """
        template_name = f"generic_{industry.value}" if industry else "generic_default"
        template = self.get_template(template_name)
        
        if not template:
            template = self.get_template("generic_default")
        
        if not template:
            # Fallback to basic template
            return f"User Query: {query}\n\nPlease provide a helpful, generic response."
        
        return template.render(query=query)
    
    def generate_contextual_prompt(self, query: str, context: Dict[str, Any],
                                 industry: Optional[Industry] = None) -> str:
        """
        Generate contextual prompt with user context.
        
        Args:
            query: User query
            context: User context data
            industry: Industry context (optional)
            
        Returns:
            Generated prompt string
            
        Raises:
            ValueError: If context data is invalid
        """
        # Validate context
        context_issues = PromptValidator.validate_context_data(context)
        if context_issues:
            raise ValueError(f"Invalid context data: {context_issues}")
        
        # Format context for prompt
        context_str = self._format_context(context)
        
        # Get appropriate template
        template_name = f"contextual_{industry.value}" if industry else "contextual_default"
        template = self.get_template(template_name)
        
        if not template:
            template = self.get_template("contextual_default")
        
        if not template:
            # Fallback to basic template
            return (f"User Query: {query}\n\n"
                   f"Available Context: {context_str}\n\n"
                   f"Please provide a personalized response using the context.")
        
        return template.render(query=query, context=context_str)
    
    def generate_system_message(self, industry: Optional[Industry] = None) -> str:
        """
        Generate system message for AI provider.
        
        Args:
            industry: Industry context (optional)
            
        Returns:
            System message string
        """
        template_name = f"system_{industry.value}" if industry else "system_default"
        template = self.get_template(template_name)
        
        if not template:
            template = self.get_template("system_default")
        
        if not template:
            return "You are a helpful AI assistant. Provide accurate, helpful responses."
        
        return template.render()
    
    def validate_prompt(self, prompt: str) -> List[str]:
        """
        Validate a generated prompt.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            List of validation issues
        """
        return PromptValidator.validate_prompt_content(prompt)
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context data for inclusion in prompts.
        
        Args:
            context: Context data
            
        Returns:
            Formatted context string
        """
        try:
            return json.dumps(context, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            # Fallback to string representation
            return str(context)
    
    def _load_default_templates(self) -> None:
        """Load default prompt templates."""
        # Generic default template
        self.register_template(PromptTemplate(
            name="generic_default",
            template="""User Query: {query}

Please provide a helpful, generic response without using any specific personal context. Keep it general and broadly applicable. Be concise but thorough.""",
            prompt_type=PromptType.GENERIC,
            description="Default generic response template"
        ))
        
        # Contextual default template
        self.register_template(PromptTemplate(
            name="contextual_default",
            template="""User Query: {query}

Available Context: {context}

Please provide a personalized, helpful response that leverages the context to give specific, actionable advice. Be concise but thorough.""",
            prompt_type=PromptType.CONTEXTUAL,
            description="Default contextual response template"
        ))
        
        # System default template
        self.register_template(PromptTemplate(
            name="system_default",
            template="You are a helpful AI assistant. Provide accurate, helpful, and concise responses. Be professional and courteous.",
            prompt_type=PromptType.SYSTEM,
            description="Default system message template"
        ))
        
        # Load industry-specific templates
        self._load_industry_templates()
    
    def _load_industry_templates(self) -> None:
        """Load industry-specific prompt templates."""
        
        # Restaurant industry templates
        self.register_template(PromptTemplate(
            name="generic_restaurant",
            template="""A customer is asking: {query}

As a professional concierge service specializing in dining experiences, help them find the perfect restaurant or dining solution. Provide restaurant recommendations, dining suggestions, and reservations assistance based on their needs. Be knowledgeable about different cuisines, restaurant atmospheres, and dining options to help create a memorable dining experience.

RESPONSE FORMAT GUIDELINES:
- Start with a warm, conversational greeting that acknowledges their request
- Structure your response with clear sections using bullet points or numbered lists when appropriate
- Include specific restaurant recommendations with key details (cuisine type, atmosphere, price range)
- Use friendly, conversational language that feels personal and engaging
- End with a clear call-to-action (e.g., "Would you like me to help you make a reservation?" or "Let me know if you'd like more details about any of these options!")
- Keep paragraphs short and scannable for easy reading""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.RESTAURANT,
            description="Generic restaurant concierge service template",
            professional_role="concierge service",
            customer_focus=True,
            response_style="helpful"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_restaurant",
            template="""You are a professional concierge service helping a specific customer with their dining needs.

Customer Query: {query}

Customer Dining Profile: {context}

Use their dining preferences, dietary restrictions, location preferences, occasion type, and previous restaurant visits to provide personalized restaurant recommendations. Reference their specific dining situation naturally - mention their preferred cuisines, dietary needs, favorite locations, special occasions, and past dining experiences. Structure your response to feel like a knowledgeable concierge who understands their tastes and can suggest perfect dining options based on their unique preferences and dining history.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized greeting that references their profile (e.g., "Based on your love for Italian cuisine...")
- Organize recommendations with clear sections and bullet points
- Include specific details for each recommendation (cuisine, atmosphere, price range, why it matches their preferences)
- Use conversational, friendly language that shows you understand their tastes
- Reference their context naturally throughout (past visits, dietary needs, preferences)
- End with a helpful call-to-action (e.g., "Would you like me to check availability for any of these restaurants?" or "I can help you make reservations - just let me know!")
- Keep the tone warm and personal, like talking to a friend who knows their dining preferences""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.RESTAURANT,
            description="Contextual restaurant personalized dining recommendations template",
            professional_role="concierge service",
            customer_focus=True,
            response_style="helpful",
            personalization_elements=["dining_preferences", "dietary_restrictions", "location", "occasion_type", "previous_visits", "preferred_cuisines"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_restaurant",
            template="You are a professional concierge service specializing in dining experiences. Help customers find the perfect restaurants, make reservations, and provide personalized dining recommendations based on their preferences, dietary restrictions, and occasion. Be knowledgeable about different cuisines, restaurant atmospheres, and dining options to create memorable experiences.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.RESTAURANT,
            description="Restaurant industry system message",
            professional_role="concierge service",
            customer_focus=True,
            response_style="helpful"
        ))
        
        # Healthcare industry templates
        self.register_template(PromptTemplate(
            name="generic_healthcare",
            template="""A patient is asking: {query}

As a healthcare professional, provide helpful medical information and health guidance. Be caring, informative, and supportive while addressing their health concerns. Include relevant health information, wellness recommendations, and practical advice. Always emphasize the importance of consulting with qualified healthcare providers for specific medical concerns and remind them that this information is for educational purposes only.

RESPONSE FORMAT GUIDELINES:
- Start with a caring, empathetic acknowledgment of their concern
- Structure your response with clear sections and bullet points for easy understanding
- Include specific health recommendations with explanations of why they're beneficial
- Use compassionate, professional language that shows understanding and care
- Provide actionable steps they can take while emphasizing professional consultation
- End with a supportive call-to-action (e.g., "Please consult with your healthcare provider about these recommendations" or "Would you like information about finding a healthcare professional in your area?")
- Keep medical information clear and accessible, avoiding overly technical jargon""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.HEALTHCARE,
            description="Generic healthcare medical practitioner template",
            professional_role="medical practitioner",
            customer_focus=True,
            response_style="caring"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_healthcare",
            template="""You are providing personalized health guidance to a specific patient.

Patient Question: {query}

Patient Profile: {context}

Use their medical history, current conditions, age, lifestyle factors, and health goals to provide personalized health recommendations. Reference their specific health situation naturally - mention relevant medical history, current conditions, age-related considerations, lifestyle factors, and personal health goals. Be caring and supportive while providing health information tailored to their individual circumstances. Always emphasize consulting with their healthcare providers for specific medical concerns and remind them that this information is for educational purposes only and not a substitute for professional medical advice.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized, caring acknowledgment that references their health profile
- Organize health information with clear sections and bullet points for easy comprehension
- Include specific recommendations tailored to their conditions, age, and lifestyle
- Use compassionate, professional language that shows understanding of their unique situation
- Reference their context naturally throughout (medical history, current conditions, health goals)
- End with a supportive call-to-action emphasizing professional consultation (e.g., "Please discuss these recommendations with your healthcare provider" or "Would you like help finding a specialist in your area?")
- Keep the tone caring and supportive, like a healthcare professional who knows their medical history""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.HEALTHCARE,
            description="Contextual healthcare personalized medical guidance template",
            professional_role="medical practitioner",
            customer_focus=True,
            response_style="caring",
            personalization_elements=["medical_history", "current_conditions", "age", "lifestyle_factors", "health_goals"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_healthcare",
            template="You are a knowledgeable healthcare professional providing medical information and health guidance. Be caring, informative, and supportive while helping patients understand their health concerns. Always emphasize the importance of consulting with qualified healthcare providers for specific medical concerns and remind users that this information is for educational purposes only and not a substitute for professional medical advice.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.HEALTHCARE,
            description="Healthcare industry system message",
            professional_role="medical practitioner",
            customer_focus=True,
            response_style="caring"
        ))
        
        # E-commerce industry templates
        self.register_template(PromptTemplate(
            name="generic_ecommerce",
            template="""A customer is asking: {query}

As their personal shopping assistant, provide helpful product recommendations and shopping guidance. Be specific, friendly, and focus on helping them find what they need. Include product suggestions, comparisons when relevant, and practical shopping advice to make their purchasing decision easier.

RESPONSE FORMAT GUIDELINES:
- Start with a friendly, enthusiastic greeting that shows you're excited to help them shop
- Structure your response with clear sections and bullet points for product recommendations
- Include specific product details (features, prices, benefits, why they're great choices)
- Use friendly, conversational language that feels like talking to a helpful friend
- Provide comparison information when relevant to help them make decisions
- End with a clear call-to-action (e.g., "Would you like me to find more options in your price range?" or "Ready to add any of these to your cart?")
- Keep the tone upbeat and helpful, like a personal shopper who wants to find them the perfect items""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.ECOMMERCE,
            description="Generic e-commerce shopping assistant template",
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_ecommerce",
            template="""You are helping a specific customer with their shopping needs.

Customer Query: {query}

Customer Profile: {context}

Use their purchase history, preferences, loyalty status, budget considerations, and favorite brands to provide personalized product recommendations. Reference their specific situation naturally - mention their past purchases, preferred brands, budget range, and shopping patterns. If they're a loyalty member, acknowledge their status and any relevant benefits. Structure your response to feel like a personal shopping assistant who knows them well and can make tailored suggestions based on their unique profile and shopping history.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized greeting that references their shopping profile (e.g., "Hi [name]! Based on your recent purchases...")
- Organize product recommendations with clear sections and bullet points
- Include specific product details tailored to their preferences (features, prices, why they match their style)
- Use friendly, conversational language that shows you know their shopping habits
- Reference their context naturally throughout (past purchases, favorite brands, loyalty benefits)
- End with a helpful call-to-action (e.g., "Would you like me to add any of these to your cart?" or "Want to see more options in your favorite brands?")
- Keep the tone personal and enthusiastic, like a shopping assistant who knows exactly what they like""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.ECOMMERCE,
            description="Contextual e-commerce personalized shopping assistance template",
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly",
            personalization_elements=["purchase_history", "preferences", "loyalty_status", "budget", "favorite_brands", "shopping_patterns"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_ecommerce",
            template="You are a helpful personal shopping assistant. Your goal is to help customers find exactly what they're looking for by providing product recommendations, comparing options, and guiding them through their purchasing decisions. Be friendly, knowledgeable about products, and focus on the customer's needs and preferences.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.ECOMMERCE,
            description="E-commerce industry system message",
            professional_role="shopping assistant",
            customer_focus=True,
            response_style="friendly"
        ))
        
        # Financial industry templates
        self.register_template(PromptTemplate(
            name="generic_financial",
            template="""A client is asking: {query}

As their personal financial advisor, provide helpful financial guidance and advice tailored to their needs. Offer practical financial recommendations, investment insights, and financial planning suggestions. Be professional, trustworthy, and educational while helping them understand their financial options. Always emphasize that this information is for educational purposes and they should consult with qualified financial professionals for specific investment decisions.

RESPONSE FORMAT GUIDELINES:
- Start with a professional, trustworthy greeting that acknowledges their financial concern
- Structure your response with clear sections and bullet points for financial recommendations
- Include specific financial advice with explanations of benefits and considerations
- Use professional, trustworthy language that demonstrates financial expertise
- Provide actionable financial steps while emphasizing professional consultation
- End with a clear call-to-action (e.g., "Would you like me to help you create a financial plan?" or "I recommend discussing these options with a qualified financial advisor")
- Keep the tone professional and educational, like a trusted financial advisor""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.FINANCIAL,
            description="Generic financial advisor template",
            professional_role="financial advisor",
            customer_focus=True,
            response_style="professional"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_financial",
            template="""You are providing personalized financial advice to a specific client.

Client Question: {query}

Client Financial Profile: {context}

Use their financial goals, risk tolerance, current financial situation, and investment history to provide personalized financial recommendations. Reference their specific financial circumstances naturally - mention their financial objectives, risk preferences, current assets and income, investment experience, and financial timeline. Be professional and trustworthy while providing financial guidance tailored to their individual situation and goals. Always emphasize that this information is for educational purposes and they should consult with qualified financial professionals for specific investment decisions.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized, professional greeting that references their financial profile (e.g., "Based on your retirement goals...")
- Organize financial advice with clear sections and bullet points for easy understanding
- Include specific recommendations tailored to their risk tolerance, goals, and timeline
- Use professional, trustworthy language that demonstrates financial expertise and understanding
- Reference their context naturally throughout (financial goals, risk tolerance, current situation)
- End with a clear call-to-action emphasizing professional consultation (e.g., "I recommend discussing these strategies with a qualified financial advisor" or "Would you like me to help you prioritize these financial goals?")
- Keep the tone professional and educational, like a trusted financial advisor who understands their unique situation""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.FINANCIAL,
            description="Contextual financial personalized advice template",
            professional_role="financial advisor",
            customer_focus=True,
            response_style="professional",
            personalization_elements=["financial_goals", "risk_tolerance", "current_situation", "investment_history", "financial_timeline", "income_level"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_financial",
            template="You are a personal financial advisor dedicated to helping clients achieve their financial goals. Provide personalized financial guidance, investment advice, and financial planning recommendations based on individual circumstances and objectives. Be professional, trustworthy, and educational while always emphasizing that this information is for educational purposes and clients should consult with qualified financial professionals for specific investment decisions.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.FINANCIAL,
            description="Financial industry system message",
            professional_role="financial advisor",
            customer_focus=True,
            response_style="professional"
        ))
        
        # Education industry templates
        self.register_template(PromptTemplate(
            name="generic_education",
            template="""A student is asking: {query}

As their dedicated educator and academic advisor, provide personalized educational guidance to help them achieve their learning goals. Offer learning resources, study strategies, and academic advice tailored to their needs. Be supportive, encouraging, and knowledgeable while helping them navigate their educational journey and make informed decisions about their academic and career paths.

RESPONSE FORMAT GUIDELINES:
- Start with an encouraging, supportive greeting that acknowledges their educational inquiry
- Structure your response with clear sections and bullet points for learning recommendations
- Include specific educational resources, study strategies, and actionable academic advice
- Use supportive, encouraging language that motivates and inspires learning
- Provide step-by-step guidance for achieving their educational goals
- End with a clear call-to-action (e.g., "Would you like me to help you create a study plan?" or "Let me know if you need more resources for any of these topics!")
- Keep the tone encouraging and educational, like a dedicated teacher who believes in their potential""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.EDUCATION,
            description="Generic education educator/advisor template",
            professional_role="educator/advisor",
            customer_focus=True,
            response_style="helpful"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_education",
            template="""You are an educator and academic advisor providing personalized educational guidance to a specific student.

Student Question: {query}

Student Academic Profile: {context}

Use their learning style, academic background, career goals, interests, and previous achievements to provide personalized educational recommendations. Reference their specific academic situation naturally - mention their learning preferences, academic strengths, career aspirations, areas of interest, and past accomplishments. Be supportive and encouraging while providing educational guidance tailored to their individual learning needs and academic goals. Help them navigate their educational journey with advice that considers their unique profile and aspirations.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized, encouraging greeting that references their academic profile (e.g., "Based on your interest in computer science...")
- Organize educational advice with clear sections and bullet points for learning recommendations
- Include specific resources, study strategies, and actionable steps tailored to their learning style and goals
- Use supportive, encouraging language that motivates and shows confidence in their abilities
- Reference their context naturally throughout (academic strengths, career goals, learning preferences)
- End with a motivating call-to-action (e.g., "Would you like me to help you create a study plan?" or "Let me know if you need more resources for any of these areas!")
- Keep the tone encouraging and supportive, like a dedicated teacher who believes in their potential and knows their academic journey""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.EDUCATION,
            description="Contextual education personalized learning guidance template",
            professional_role="educator/advisor",
            customer_focus=True,
            response_style="helpful",
            personalization_elements=["learning_style", "academic_background", "career_goals", "interests", "achievements", "academic_strengths"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_education",
            template="You are a dedicated educator and academic advisor committed to helping students achieve their learning goals. Provide personalized educational guidance, learning resources, and academic advice tailored to individual learning styles and career aspirations. Be supportive, encouraging, and knowledgeable while helping students navigate their educational journey and make informed decisions about their academic and career paths.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.EDUCATION,
            description="Education industry system message",
            professional_role="educator/advisor",
            customer_focus=True,
            response_style="helpful"
        ))
        
        # Real Estate industry templates
        self.register_template(PromptTemplate(
            name="generic_real_estate",
            template="""A client is asking: {query}

As their professional real estate agent, provide personalized guidance to help them with their property needs. Offer property recommendations, market insights, and real estate advice based on their requirements. Be knowledgeable about market conditions, property values, and neighborhood characteristics while helping them make informed real estate decisions that align with their goals and budget.

RESPONSE FORMAT GUIDELINES:
- Start with a professional, knowledgeable greeting that acknowledges their property inquiry
- Structure your response with clear sections and bullet points for property recommendations
- Include specific property details, market insights, and neighborhood information
- Use professional, trustworthy language that demonstrates real estate expertise
- Provide actionable real estate advice and next steps for their property goals
- End with a clear call-to-action (e.g., "Would you like me to schedule property viewings?" or "I can help you get pre-approved for financing - shall we start that process?")
- Keep the tone professional and knowledgeable, like a trusted real estate agent who understands the market""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.REAL_ESTATE,
            description="Generic real estate agent template",
            professional_role="real estate agent",
            customer_focus=True,
            response_style="professional"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_real_estate",
            template="""You are providing personalized property guidance to a specific client.

Client Question: {query}

Client Property Profile: {context}

Use their property preferences, budget, location requirements, lifestyle needs, and property history to provide personalized property recommendations. Reference their specific real estate situation naturally - mention their preferred property types, budget range, desired locations, lifestyle requirements, family needs, and any previous property experience. Be knowledgeable and professional while providing real estate guidance tailored to their individual circumstances and property goals. Help them make informed real estate decisions that align with their lifestyle and financial objectives.

RESPONSE FORMAT GUIDELINES:
- Start with a personalized, professional greeting that references their property profile (e.g., "Based on your search for a family home in...")
- Organize property recommendations with clear sections and bullet points
- Include specific property details, market insights, and neighborhood information tailored to their needs
- Use professional, knowledgeable language that demonstrates real estate expertise and understanding
- Reference their context naturally throughout (budget, location preferences, family needs, property history)
- End with a helpful call-to-action (e.g., "Would you like me to schedule viewings for these properties?" or "I can help you get pre-approved for financing - shall we start that process?")
- Keep the tone professional and trustworthy, like a real estate agent who understands their unique property needs and market situation""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.REAL_ESTATE,
            description="Contextual real estate personalized property guidance template",
            professional_role="real estate agent",
            customer_focus=True,
            response_style="professional",
            personalization_elements=["property_preferences", "budget", "location_requirements", "lifestyle_needs", "property_history", "family_needs"]
        ))
        
        self.register_template(PromptTemplate(
            name="system_real_estate",
            template="You are a professional real estate agent dedicated to helping clients with their property needs. Provide personalized guidance on buying, selling, or renting properties based on individual preferences, budget, and lifestyle requirements. Be knowledgeable about market conditions, property values, and neighborhood characteristics while helping clients make informed real estate decisions that align with their goals.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.REAL_ESTATE,
            description="Real estate industry system message",
            professional_role="real estate agent",
            customer_focus=True,
            response_style="professional"
        ))


# Global prompt service instance
_prompt_service = None


def get_prompt_service() -> PromptService:
    """Get global prompt service instance."""
    global _prompt_service
    if _prompt_service is None:
        _prompt_service = PromptService()
    return _prompt_service