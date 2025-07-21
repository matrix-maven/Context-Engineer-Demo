"""
Demo modules for Context Engineering Demo

This package contains all industry-specific demonstration modules
that implement the BaseDemo interface.
"""

from .base_demo import BaseDemo, DemoResponse
from .restaurant_demo import RestaurantDemo
from .healthcare_demo import HealthcareDemo
from .ecommerce_demo import EcommerceDemo
from .financial_demo import FinancialDemo
from .education_demo import EducationDemo
from .real_estate_demo import RealEstateDemo
from .demo_factory import DemoFactory

__all__ = [
    'BaseDemo',
    'DemoResponse',
    'RestaurantDemo',
    'HealthcareDemo',
    'EcommerceDemo',
    'FinancialDemo',
    'EducationDemo',
    'RealEstateDemo',
    'DemoFactory'
]