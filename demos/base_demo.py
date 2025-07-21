"""
Base Demo Class for Context Engineering Demo

This module provides the abstract base class for all industry demonstrations,
establishing a consistent interface and common functionality.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
import streamlit as st
from dataclasses import dataclass

# Import Industry enum from prompt service
try:
    from services.prompt_service import Industry
except ImportError:
    # Fallback if prompt service not available
    from enum import Enum
    class Industry(str, Enum):
        RESTAURANT = "restaurant"
        HEALTHCARE = "healthcare"
        ECOMMERCE = "ecommerce"
        FINANCIAL = "financial"
        EDUCATION = "education"
        REAL_ESTATE = "real_estate"


@dataclass
class DemoResponse:
    """Container for demo response data"""
    generic_response: str
    contextual_response: str
    context_data: Dict[str, Any]
    query: str
    industry: str


class BaseDemo(ABC):
    """
    Abstract base class for industry demonstrations.
    
    Provides common functionality for query handling, response display,
    and context management while allowing industry-specific customization.
    """
    
    def __init__(self, industry_name: str, industry_enum: Optional[Industry] = None, 
                 ai_service=None, context_service=None):
        """
        Initialize the base demo.
        
        Args:
            industry_name: Display name for the industry
            industry_enum: Industry enum value for prompt service integration
            ai_service: AI service for generating responses (optional)
            context_service: Context generation service (optional)
        """
        self.industry_name = industry_name
        self.industry_enum = industry_enum
        self.ai_service = ai_service
        self.context_service = context_service
        self.use_ai = ai_service is not None
    
    @abstractmethod
    def generate_context(self) -> Dict[str, Any]:
        """
        Generate industry-specific context data.
        
        Returns:
            Dictionary containing relevant context for the industry
        """
        pass
    
    @abstractmethod
    def get_sample_queries(self) -> List[str]:
        """
        Get sample queries relevant to the industry.
        
        Returns:
            List of sample query strings
        """
        pass
    
    @abstractmethod
    def get_query_placeholder(self) -> str:
        """
        Get placeholder text for the query input field.
        
        Returns:
            Placeholder text string
        """
        pass
    
    @abstractmethod
    def get_system_message_generic(self) -> str:
        """
        Get system message for generic AI responses.
        
        Returns:
            System message string for generic responses
        """
        pass
    
    @abstractmethod
    def get_system_message_contextual(self) -> str:
        """
        Get system message for contextual AI responses.
        
        Returns:
            System message string for contextual responses
        """
        pass
    
    @abstractmethod
    def generate_fallback_generic_response(self, query: str) -> str:
        """
        Generate fallback generic response when AI is unavailable.
        
        Args:
            query: User query string
            
        Returns:
            Generic response string
        """
        pass
    
    @abstractmethod
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """
        Generate fallback contextual response when AI is unavailable.
        
        Args:
            query: User query string
            context: Context data dictionary
            
        Returns:
            Contextual response string
        """
        pass
    
    def generate_generic_response(self, query: str) -> str:
        """
        Generate generic response using AI or fallback.
        
        Args:
            query: User query string
            
        Returns:
            Generic response string
        """
        if self.use_ai and self.ai_service:
            try:
                return self.ai_service.generate_response(
                    query=query,
                    context={},
                    is_contextual=False,
                    industry=self.industry_enum
                )
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
                return self.generate_fallback_generic_response(query)
        else:
            return self.generate_fallback_generic_response(query)
    
    def generate_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """
        Generate contextual response using AI or fallback.
        
        Args:
            query: User query string
            context: Context data dictionary
            
        Returns:
            Contextual response string
        """
        if self.use_ai and self.ai_service:
            try:
                return self.ai_service.generate_response(
                    query=query,
                    context=context,
                    is_contextual=True,
                    industry=self.industry_enum
                )
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
                return self.generate_fallback_contextual_response(query, context)
        else:
            return self.generate_fallback_contextual_response(query, context)
    
    def handle_query(self, query: str) -> DemoResponse:
        """
        Process a user query and generate both generic and contextual responses.
        
        Args:
            query: User query string
            
        Returns:
            DemoResponse containing both responses and context
        """
        # Generate fresh context for each query - use smart context if available
        if hasattr(self, 'generate_smart_context'):
            context = self.generate_smart_context(query)
        else:
            context = self.generate_context()
        
        # Generate both response types
        generic_response = self.generate_generic_response(query)
        contextual_response = self.generate_contextual_response(query, context)
        
        return DemoResponse(
            generic_response=generic_response,
            contextual_response=contextual_response,
            context_data=context,
            query=query,
            industry=self.industry_name
        )
    
    def render_query_input(self) -> Optional[str]:
        """
        Render the query input field using UI components.
        
        Returns:
            User query string or None if no query entered
        """
        # Import here to avoid circular imports
        from ui.components import UIComponents
        
        key = f"{self.industry_name.lower().replace(' ', '_')}_query"
        return UIComponents.render_query_input(
            self.industry_name, 
            self.get_query_placeholder(), 
            key
        )
    
    def render_sample_queries(self):
        """Render sample queries as clickable buttons using UI components."""
        # Import here to avoid circular imports
        from ui.components import UIComponents
        
        sample_queries = self.get_sample_queries()
        input_key = f"{self.industry_name.lower().replace(' ', '_')}_query"
        
        UIComponents.render_sample_queries(
            sample_queries, 
            self.industry_name, 
            input_key
        )
    
    def render_comparison_columns(self, response: DemoResponse):
        """
        Render the side-by-side comparison columns using UI components.
        
        Args:
            response: DemoResponse containing the responses and context
        """
        # Import here to avoid circular imports
        from ui.components import UIComponents
        
        # Convert DemoResponse to ResponseData
        response_data = UIComponents.create_response_data(
            generic_response=response.generic_response,
            contextual_response=response.contextual_response,
            context_data=response.context_data,
            query=response.query,
            industry=response.industry
        )
        
        UIComponents.render_comparison_columns(response_data)
    
    def render_demo_header(self):
        """Render the demo header with industry-specific icon and title using UI components."""
        # Import here to avoid circular imports
        from ui.layout import create_industry_demo_layout
        
        icon = self.get_industry_icon()
        create_industry_demo_layout(self.industry_name, icon)
    
    def get_industry_icon(self) -> str:
        """
        Get the emoji icon for the industry.
        Can be overridden by subclasses for custom icons.
        
        Returns:
            Emoji string
        """
        # Default icons for common industries
        icons = {
            "Restaurant Reservations": "🍽️",
            "Healthcare": "🏥",
            "E-commerce": "🛒",
            "Financial Services": "💰",
            "Education": "📚",
            "Real Estate": "🏠"
        }
        return icons.get(self.industry_name, "🏢")
    
    def render(self):
        """
        Main render method for the demo.
        Handles the complete demo flow including input, processing, and display.
        """
        # Render header
        self.render_demo_header()
        
        # Render sample queries
        self.render_sample_queries()
        
        # Render query input
        user_query = self.render_query_input()
        
        if user_query:
            # Process query and generate responses
            response = self.handle_query(user_query)
            
            # Render comparison columns
            self.render_comparison_columns(response)
        else:
            st.info(f"👆 Enter a {self.industry_name.lower()}-related query above to see the context difference!")
    
    def get_context_summary(self, context: Dict[str, Any]) -> str:
        """
        Generate a brief summary of the context for display purposes.
        
        Args:
            context: Context data dictionary
            
        Returns:
            Summary string
        """
        key_count = len(context.keys())
        return f"Using {key_count} context points: {', '.join(list(context.keys())[:3])}{'...' if key_count > 3 else ''}"