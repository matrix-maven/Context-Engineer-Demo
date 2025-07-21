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
            customer_service_indicators = [
                "help", "assist", "recommend", "guide", "support", 
                "customer", "client", "user", "personalized", "specific"
            ]
            
            has_customer_language = any(indicator in template_lower for indicator in customer_service_indicators)
            if not has_customer_language:
                errors.append("Customer-focused template should include customer service language (help, assist, recommend, etc.)")
        
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
            template="""User Query: {query}

Please provide helpful restaurant and food service advice. Focus on general best practices, common solutions, and industry standards. Be practical and actionable.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.RESTAURANT,
            description="Generic restaurant industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_restaurant",
            template="""User Query: {query}

Restaurant Context: {context}

Based on the specific restaurant context provided, give personalized advice that considers the establishment's unique situation, customer base, and operational details. Be specific and actionable.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.RESTAURANT,
            description="Contextual restaurant industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_restaurant",
            template="You are an expert restaurant and food service consultant. Provide practical, industry-specific advice based on best practices in restaurant operations, customer service, and food safety.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.RESTAURANT,
            description="Restaurant industry system message"
        ))
        
        # Healthcare industry templates
        self.register_template(PromptTemplate(
            name="generic_healthcare",
            template="""User Query: {query}

Please provide general healthcare and medical practice guidance. Focus on best practices, regulatory compliance, and patient care standards. Always emphasize the importance of professional medical consultation.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.HEALTHCARE,
            description="Generic healthcare industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_healthcare",
            template="""User Query: {query}

Healthcare Context: {context}

Based on the healthcare context provided, offer specific guidance that considers the medical practice's unique situation, patient demographics, and operational requirements. Always emphasize professional medical consultation.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.HEALTHCARE,
            description="Contextual healthcare industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_healthcare",
            template="You are a healthcare administration and practice management consultant. Provide guidance on healthcare operations, compliance, and best practices. Always emphasize that medical advice should come from qualified healthcare professionals.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.HEALTHCARE,
            description="Healthcare industry system message"
        ))
        
        # E-commerce industry templates
        self.register_template(PromptTemplate(
            name="generic_ecommerce",
            template="""User Query: {query}

Please provide e-commerce and online retail guidance. Focus on best practices for online sales, customer experience, digital marketing, and business operations.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.ECOMMERCE,
            description="Generic e-commerce industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_ecommerce",
            template="""User Query: {query}

E-commerce Context: {context}

Based on the e-commerce business context provided, offer specific recommendations that consider the business model, target market, product catalog, and operational details.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.ECOMMERCE,
            description="Contextual e-commerce industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_ecommerce",
            template="You are an e-commerce and digital retail consultant. Provide expert advice on online business operations, digital marketing, customer experience, and e-commerce best practices.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.ECOMMERCE,
            description="E-commerce industry system message"
        ))
        
        # Financial industry templates
        self.register_template(PromptTemplate(
            name="generic_financial",
            template="""User Query: {query}

Please provide general financial services guidance. Focus on industry best practices, regulatory compliance, risk management, and customer service standards. Always emphasize the importance of professional financial advice.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.FINANCIAL,
            description="Generic financial industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_financial",
            template="""User Query: {query}

Financial Services Context: {context}

Based on the financial services context provided, offer specific guidance that considers the institution's unique situation, client base, and regulatory environment. Always emphasize professional financial consultation.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.FINANCIAL,
            description="Contextual financial industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_financial",
            template="You are a financial services consultant. Provide guidance on financial operations, compliance, risk management, and industry best practices. Always emphasize that specific financial advice should come from qualified financial professionals.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.FINANCIAL,
            description="Financial industry system message"
        ))
        
        # Education industry templates
        self.register_template(PromptTemplate(
            name="generic_education",
            template="""User Query: {query}

Please provide educational guidance and best practices. Focus on teaching methods, student engagement, curriculum development, and educational administration.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.EDUCATION,
            description="Generic education industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_education",
            template="""User Query: {query}

Educational Context: {context}

Based on the educational context provided, offer specific recommendations that consider the institution's unique situation, student demographics, curriculum requirements, and educational goals.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.EDUCATION,
            description="Contextual education industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_education",
            template="You are an educational consultant and expert in teaching methodologies. Provide guidance on educational best practices, curriculum development, student engagement, and institutional management.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.EDUCATION,
            description="Education industry system message"
        ))
        
        # Real Estate industry templates
        self.register_template(PromptTemplate(
            name="generic_real_estate",
            template="""User Query: {query}

Please provide real estate industry guidance. Focus on best practices for property management, sales, market analysis, and client relations in the real estate sector.""",
            prompt_type=PromptType.GENERIC,
            industry=Industry.REAL_ESTATE,
            description="Generic real estate industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="contextual_real_estate",
            template="""User Query: {query}

Real Estate Context: {context}

Based on the real estate context provided, offer specific recommendations that consider the market conditions, property types, client needs, and business objectives.""",
            prompt_type=PromptType.CONTEXTUAL,
            industry=Industry.REAL_ESTATE,
            description="Contextual real estate industry template"
        ))
        
        self.register_template(PromptTemplate(
            name="system_real_estate",
            template="You are a real estate industry expert and consultant. Provide guidance on property management, real estate sales, market analysis, and industry best practices.",
            prompt_type=PromptType.SYSTEM,
            industry=Industry.REAL_ESTATE,
            description="Real estate industry system message"
        ))


# Global prompt service instance
_prompt_service = None


def get_prompt_service() -> PromptService:
    """Get global prompt service instance."""
    global _prompt_service
    if _prompt_service is None:
        _prompt_service = PromptService()
    return _prompt_service