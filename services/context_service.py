"""
Context generation service with Faker integration for industry-specific data.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Type
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
import random
from faker import Faker
from faker.providers import BaseProvider

from config.settings import get_settings


class Industry(str, Enum):
    """Supported industries for context generation."""
    RESTAURANT = "restaurant"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "e-commerce"
    FINANCIAL = "financial"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"


@dataclass
class IndustryContext:
    """
    Standardized industry context data model.
    
    This class represents context data for a specific industry with consistent
    structure for validation and quality checks.
    """
    industry: Industry
    user_profile: Dict[str, Any] = field(default_factory=dict)
    situational_data: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    history: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set generation timestamp if not provided."""
        if self.generated_at is None:
            self.generated_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            'industry': self.industry.value,
            'user_profile': self.user_profile,
            'situational_data': self.situational_data,
            'preferences': self.preferences,
            'history': self.history,
            'constraints': self.constraints,
            'metadata': self.metadata,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None
        }
    
    def is_valid(self) -> bool:
        """Check if context data is valid."""
        return (
            bool(self.user_profile) and
            bool(self.situational_data) and
            self.generated_at is not None
        )
    
    def get_context_summary(self) -> str:
        """Get a human-readable summary of the context."""
        summary_parts = []
        
        if self.user_profile:
            summary_parts.append(f"User: {self.user_profile.get('name', 'Unknown')}")
        
        if self.situational_data:
            situation = list(self.situational_data.keys())[0] if self.situational_data else "General"
            summary_parts.append(f"Situation: {situation}")
        
        if self.preferences:
            pref_count = len(self.preferences)
            summary_parts.append(f"Preferences: {pref_count} items")
        
        return " | ".join(summary_parts) if summary_parts else f"{self.industry.value} context"


class ContextValidationError(Exception):
    """Exception raised when context validation fails."""
    
    def __init__(self, message: str, industry: Optional[Industry] = None, 
                 validation_errors: Optional[List[str]] = None):
        super().__init__(message)
        self.industry = industry
        self.validation_errors = validation_errors or []


class BaseContextFactory(ABC):
    """
    Abstract base class for industry-specific context factories.
    
    This class defines the standard interface that all context factories must
    implement to ensure consistent context generation across industries.
    """
    
    def __init__(self, faker: Faker):
        """
        Initialize context factory with Faker instance.
        
        Args:
            faker: Faker instance for data generation
        """
        self.faker = faker
        self.industry = self._get_industry()
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    @abstractmethod
    def _get_industry(self) -> Industry:
        """Get the industry this factory generates context for."""
        pass
    
    @abstractmethod
    def generate_user_profile(self) -> Dict[str, Any]:
        """Generate realistic user profile data."""
        pass
    
    @abstractmethod
    def generate_situational_data(self) -> Dict[str, Any]:
        """Generate industry-specific situational data."""
        pass
    
    @abstractmethod
    def generate_preferences(self) -> Dict[str, Any]:
        """Generate user preferences relevant to the industry."""
        pass
    
    @abstractmethod
    def generate_history(self) -> Dict[str, Any]:
        """Generate user history data relevant to the industry."""
        pass
    
    def generate_constraints(self) -> Dict[str, Any]:
        """Generate constraints (can be overridden by subclasses)."""
        return {
            "budget_conscious": self.faker.boolean(chance_of_getting_true=30),
            "time_sensitive": self.faker.boolean(chance_of_getting_true=40),
            "accessibility_needs": self.faker.boolean(chance_of_getting_true=15)
        }
    
    def generate_context(self) -> IndustryContext:
        """
        Generate complete industry context.
        
        Returns:
            IndustryContext: Complete context data for the industry
        """
        try:
            context = IndustryContext(
                industry=self.industry,
                user_profile=self.generate_user_profile(),
                situational_data=self.generate_situational_data(),
                preferences=self.generate_preferences(),
                history=self.generate_history(),
                constraints=self.generate_constraints(),
                metadata={
                    'factory': self.__class__.__name__,
                    'faker_seed': self.faker.seed_instance,
                    'generation_method': 'faker'
                }
            )
            
            self.logger.debug(f"Generated context for {self.industry.value}: {context.get_context_summary()}")
            return context
            
        except Exception as e:
            self.logger.error(f"Failed to generate context for {self.industry.value}: {str(e)}")
            raise ContextValidationError(
                f"Context generation failed for {self.industry.value}",
                industry=self.industry,
                validation_errors=[str(e)]
            )
    
    def validate_context(self, context: IndustryContext) -> List[str]:
        """
        Validate generated context data.
        
        Args:
            context: Context to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Basic validation
        if not context.is_valid():
            errors.append("Context missing required fields")
        
        if context.industry != self.industry:
            errors.append(f"Context industry mismatch: expected {self.industry.value}, got {context.industry.value}")
        
        # Validate user profile
        if not context.user_profile.get('name'):
            errors.append("User profile missing name")
        
        # Validate situational data is not empty
        if not context.situational_data:
            errors.append("Situational data is empty")
        
        # Industry-specific validation (can be overridden)
        errors.extend(self._validate_industry_specific(context))
        
        return errors
    
    def _validate_industry_specific(self, context: IndustryContext) -> List[str]:
        """
        Perform industry-specific validation (override in subclasses).
        
        Args:
            context: Context to validate
            
        Returns:
            List of validation error messages
        """
        return []


class ContextService:
    """
    Main context generation service with Faker integration.
    
    This service manages context generation across multiple industries using
    industry-specific factories and provides caching and validation.
    """
    
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        """
        Initialize context service.
        
        Args:
            locale: Faker locale for data generation
            seed: Random seed for reproducible generation (optional)
        """
        self.faker = Faker(locale)
        if seed is not None:
            self.faker.seed_instance(seed)
        
        self.settings = get_settings()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Context cache with TTL
        self._context_cache: Dict[Industry, IndustryContext] = {}
        self._cache_timestamps: Dict[Industry, datetime] = {}
        
        # Factory registry
        self._factories: Dict[Industry, BaseContextFactory] = {}
        self._register_factories()
    
    def _register_factories(self) -> None:
        """Register all available context factories."""
        # Import and register factories here to avoid circular imports
        from services.context_factories import (
            RestaurantContextFactory,
            HealthcareContextFactory,
            EcommerceContextFactory,
            FinancialContextFactory,
            EducationContextFactory,
            RealEstateContextFactory
        )
        
        # Register all available factories
        factories = [
            RestaurantContextFactory,
            HealthcareContextFactory,
            EcommerceContextFactory,
            FinancialContextFactory,
            EducationContextFactory,
            RealEstateContextFactory
        ]
        
        for factory_class in factories:
            self.register_factory(factory_class)
    
    def register_factory(self, factory_class: Type[BaseContextFactory]) -> None:
        """
        Register a context factory for an industry.
        
        Args:
            factory_class: Factory class to register
        """
        factory = factory_class(self.faker)
        self._factories[factory.industry] = factory
        self.logger.debug(f"Registered factory for {factory.industry.value}")
    
    def get_available_industries(self) -> List[Industry]:
        """Get list of industries with registered factories."""
        return list(self._factories.keys())
    
    def generate_context(self, industry: Industry, force_refresh: bool = False) -> IndustryContext:
        """
        Generate context for a specific industry.
        
        Args:
            industry: Industry to generate context for
            force_refresh: Force generation of new context (ignore cache)
            
        Returns:
            IndustryContext: Generated context data
            
        Raises:
            ContextValidationError: If context generation or validation fails
        """
        # Check cache first (unless force refresh)
        if not force_refresh and self._is_cached_context_valid(industry):
            cached_context = self._context_cache[industry]
            self.logger.debug(f"Using cached context for {industry.value}")
            return cached_context
        
        # Get factory for industry
        factory = self._factories.get(industry)
        if not factory:
            raise ContextValidationError(
                f"No factory registered for industry: {industry.value}",
                industry=industry
            )
        
        # Generate new context
        context = factory.generate_context()
        
        # Validate context
        validation_errors = factory.validate_context(context)
        if validation_errors:
            raise ContextValidationError(
                f"Context validation failed for {industry.value}",
                industry=industry,
                validation_errors=validation_errors
            )
        
        # Cache the context
        self._context_cache[industry] = context
        self._cache_timestamps[industry] = datetime.now(timezone.utc)
        
        self.logger.info(f"Generated new context for {industry.value}: {context.get_context_summary()}")
        return context
    
    def refresh_context(self, industry: Industry) -> IndustryContext:
        """
        Force refresh context for a specific industry.
        
        Args:
            industry: Industry to refresh context for
            
        Returns:
            IndustryContext: Newly generated context data
        """
        return self.generate_context(industry, force_refresh=True)
    
    def refresh_all_contexts(self) -> Dict[Industry, IndustryContext]:
        """
        Refresh contexts for all registered industries.
        
        Returns:
            Dict mapping industries to their new contexts
        """
        refreshed_contexts = {}
        
        for industry in self.get_available_industries():
            try:
                refreshed_contexts[industry] = self.refresh_context(industry)
            except ContextValidationError as e:
                self.logger.error(f"Failed to refresh context for {industry.value}: {str(e)}")
                # Continue with other industries
        
        return refreshed_contexts
    
    def validate_context(self, context: IndustryContext) -> List[str]:
        """
        Validate context using appropriate factory.
        
        Args:
            context: Context to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        factory = self._factories.get(context.industry)
        if not factory:
            return [f"No factory available for industry: {context.industry.value}"]
        
        return factory.validate_context(context)
    
    def get_context_quality_score(self, context: IndustryContext) -> float:
        """
        Calculate quality score for context data (0.0 to 1.0).
        
        Args:
            context: Context to score
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 6.0  # Maximum possible score
        
        # Basic completeness checks
        if context.user_profile:
            score += 1.0
        if context.situational_data:
            score += 1.0
        if context.preferences:
            score += 1.0
        if context.history:
            score += 1.0
        if context.constraints:
            score += 0.5
        
        # Data richness checks
        total_fields = (
            len(context.user_profile) +
            len(context.situational_data) +
            len(context.preferences) +
            len(context.history)
        )
        
        if total_fields >= 10:
            score += 1.0
        elif total_fields >= 5:
            score += 0.5
        
        # Validation check
        validation_errors = self.validate_context(context)
        if not validation_errors:
            score += 0.5
        
        return min(score / max_score, 1.0)
    
    def _is_cached_context_valid(self, industry: Industry) -> bool:
        """Check if cached context is still valid based on TTL."""
        if industry not in self._context_cache:
            return False
        
        cache_time = self._cache_timestamps.get(industry)
        if not cache_time:
            return False
        
        ttl = timedelta(seconds=self.settings.context_refresh_interval)
        return datetime.now(timezone.utc) - cache_time < ttl
    
    def clear_cache(self, industry: Optional[Industry] = None) -> None:
        """
        Clear context cache.
        
        Args:
            industry: Specific industry to clear (None for all)
        """
        if industry:
            self._context_cache.pop(industry, None)
            self._cache_timestamps.pop(industry, None)
            self.logger.debug(f"Cleared cache for {industry.value}")
        else:
            self._context_cache.clear()
            self._cache_timestamps.clear()
            self.logger.debug("Cleared all context cache")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get current cache status for debugging."""
        return {
            'cached_industries': [industry.value for industry in self._context_cache.keys()],
            'cache_timestamps': {
                industry.value: timestamp.isoformat()
                for industry, timestamp in self._cache_timestamps.items()
            },
            'registered_factories': [industry.value for industry in self._factories.keys()],
            'cache_ttl_seconds': self.settings.context_refresh_interval
        }
    
    def set_faker_seed(self, seed: int) -> None:
        """
        Set Faker seed for reproducible generation.
        
        Args:
            seed: Random seed value
        """
        self.faker.seed_instance(seed)
        self.logger.debug(f"Set Faker seed to {seed}")
    
    def __str__(self) -> str:
        """String representation of context service."""
        return f"ContextService(industries={len(self._factories)}, cached={len(self._context_cache)})"
    
    def __repr__(self) -> str:
        """Detailed string representation of context service."""
        return (
            f"ContextService("
            f"locale={self.faker.locales}, "
            f"industries={list(self._factories.keys())}, "
            f"cached_contexts={list(self._context_cache.keys())}, "
            f"cache_ttl={self.settings.context_refresh_interval}s)"
        )