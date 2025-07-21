"""
Demo Factory for Context Engineering Demo

Factory class to create and manage industry demonstration instances.
"""
from typing import Dict, Optional, Type
from .base_demo import BaseDemo
from .restaurant_demo import RestaurantDemo
from .healthcare_demo import HealthcareDemo
from .ecommerce_demo import EcommerceDemo
from .financial_demo import FinancialDemo
from .education_demo import EducationDemo
from .real_estate_demo import RealEstateDemo


class DemoFactory:
    """Factory for creating industry demonstration instances."""
    
    # Registry of available demo classes
    _demo_classes: Dict[str, Type[BaseDemo]] = {
        "Restaurant Reservations": RestaurantDemo,
        "Healthcare": HealthcareDemo,
        "E-commerce": EcommerceDemo,
        "Financial Services": FinancialDemo,
        "Education": EducationDemo,
        "Real Estate": RealEstateDemo
    }
    
    @classmethod
    def create_demo(cls, industry: str, ai_service=None, context_service=None) -> Optional[BaseDemo]:
        """
        Create a demo instance for the specified industry.
        
        Args:
            industry: Industry name (must match available demos)
            ai_service: AI service instance (optional)
            context_service: Context service instance (optional)
            
        Returns:
            Demo instance or None if industry not found
        """
        demo_class = cls._demo_classes.get(industry)
        if demo_class:
            return demo_class(ai_service=ai_service, context_service=context_service)
        return None
    
    @classmethod
    def get_available_industries(cls) -> list[str]:
        """
        Get list of available industry names.
        
        Returns:
            List of industry names
        """
        return list(cls._demo_classes.keys())
    
    @classmethod
    def register_demo(cls, industry: str, demo_class: Type[BaseDemo]) -> None:
        """
        Register a new demo class.
        
        Args:
            industry: Industry name
            demo_class: Demo class that extends BaseDemo
        """
        cls._demo_classes[industry] = demo_class
    
    @classmethod
    def is_industry_supported(cls, industry: str) -> bool:
        """
        Check if an industry is supported.
        
        Args:
            industry: Industry name to check
            
        Returns:
            True if industry is supported, False otherwise
        """
        return industry in cls._demo_classes