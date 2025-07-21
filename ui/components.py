"""
Reusable UI Components for Context Engineering Demo

This module provides modular Streamlit components for consistent UI across
all industry demonstrations.
"""
import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import json
import time
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResponseData:
    """Container for response display data"""
    generic_response: str
    contextual_response: str
    context_data: Dict[str, Any]
    query: str
    industry: str
    timestamp: Optional[datetime] = None


@dataclass
class MetricsData:
    """Container for metrics display data"""
    industries_count: int = 6
    context_points: str = "50+"
    response_quality: str = "10x"
    user_satisfaction: str = "95%"
    ai_enabled: bool = False


class UIComponents:
    """Collection of reusable UI components for the demo application."""
    
    @staticmethod
    def render_page_header(title: str = "🧠 Context Engineering Demo", 
                          subtitle: str = "**See how AI responses transform when context is applied across different industries**"):
        """
        Render the main page header with title and subtitle.
        
        Args:
            title: Main page title
            subtitle: Subtitle/description text
        """
        st.title(title)
        st.markdown(subtitle)
    
    @staticmethod
    def render_ai_status_indicator(ai_enabled: bool, provider_name: str = "AI"):
        """
        Render AI status indicator showing current mode.
        
        Args:
            ai_enabled: Whether AI is currently enabled
            provider_name: Name of the AI provider
        """
        if ai_enabled:
            st.success(f"🤖 **AI Mode**: Real {provider_name} responses enabled")
        else:
            st.warning("📝 **Fallback Mode**: Using static responses (set API key for AI)")
    
    @staticmethod
    def render_metrics_dashboard(metrics: MetricsData):
        """
        Render the top-level metrics dashboard.
        
        Args:
            metrics: MetricsData containing metric values
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Industries", str(metrics.industries_count), delta="Complete")
        
        with col2:
            st.metric("Context Points", metrics.context_points, delta="Rich data")
        
        with col3:
            quality_delta = "AI-Powered" if metrics.ai_enabled else "Static"
            st.metric("Response Quality", metrics.response_quality, delta=quality_delta)
        
        with col4:
            st.metric("User Satisfaction", metrics.user_satisfaction, delta="Higher")
    
    @staticmethod
    def render_industry_selector(industries: List[str], key: str = "industry_selector") -> str:
        """
        Render industry selection sidebar.
        
        Args:
            industries: List of available industries
            key: Unique key for the selectbox
            
        Returns:
            Selected industry name
        """
        st.sidebar.title("Select Industry")
        return st.sidebar.selectbox(
            "Choose an industry to explore:",
            industries,
            key=key
        )
    
    @staticmethod
    def render_query_input(industry_name: str, placeholder: str, 
                          key: Optional[str] = None) -> Optional[str]:
        """
        Render query input field with industry-specific styling.
        
        Args:
            industry_name: Name of the industry for labeling
            placeholder: Placeholder text for the input
            key: Optional unique key for the input
            
        Returns:
            User query string or None
        """
        if key is None:
            key = f"{industry_name.lower().replace(' ', '_')}_query"
        
        return st.text_input(
            f"🎤 Enter your {industry_name.lower()} request:",
            placeholder=placeholder,
            key=key
        )
    
    @staticmethod
    def render_sample_queries(queries: List[str], industry_name: str, 
                            input_key: str, max_columns: int = 3):
        """
        Render sample queries as clickable buttons.
        
        Args:
            queries: List of sample query strings
            industry_name: Name of the industry
            input_key: Key for the input field to update
            max_columns: Maximum number of columns for button layout
        """
        st.markdown("**💡 Try these sample queries:**")
        
        # Create columns for button layout
        num_cols = min(len(queries), max_columns)
        cols = st.columns(num_cols)
        
        for i, query in enumerate(queries[:max_columns]):
            with cols[i % num_cols]:
                # Truncate long queries for button display
                button_text = query[:30] + "..." if len(query) > 30 else query
                
                if st.button(
                    button_text,
                    key=f"sample_{industry_name}_{i}",
                    help=query,
                    use_container_width=True
                ):
                    st.session_state[input_key] = query
                    st.rerun()
    
    @staticmethod
    def render_context_expander(context_data: Dict[str, Any], 
                              title: str = "📊 Available Context") -> bool:
        """
        Render expandable context display section.
        
        Args:
            context_data: Dictionary containing context information
            title: Title for the expander section
            
        Returns:
            True if expander is expanded, False otherwise
        """
        with st.expander(title):
            # Format context data for better readability
            UIComponents._render_formatted_context(context_data)
            return True
        return False
    
    @staticmethod
    def _render_formatted_context(context_data: Dict[str, Any]):
        """
        Render formatted context data with improved readability.
        
        Args:
            context_data: Dictionary containing context information
        """
        # Try to render in a more readable format first
        try:
            # Group related context items
            for key, value in context_data.items():
                if isinstance(value, dict):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    for sub_key, sub_value in value.items():
                        st.markdown(f"  • {sub_key}: {sub_value}")
                elif isinstance(value, list):
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {', '.join(map(str, value))}")
                else:
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        except Exception:
            # Fallback to JSON display
            st.json(context_data)
    
    @staticmethod
    def render_comparison_columns(response_data: ResponseData):
        """
        Render side-by-side comparison of generic vs contextual responses.
        
        Args:
            response_data: ResponseData containing both responses and context
        """
        col1, col2 = st.columns(2)
        
        with col1:
            UIComponents._render_generic_response_column(response_data)
        
        with col2:
            UIComponents._render_contextual_response_column(response_data)
    
    @staticmethod
    def _render_generic_response_column(response_data: ResponseData):
        """Render the generic response column."""
        st.subheader("❌ Context OFF")
        st.info(f"Query: {response_data.query}")
        
        # Add response quality indicator
        st.caption("🤖 Generic AI Response")
        
        st.markdown(f"**Response:**\n\n{response_data.generic_response}")
        
        # Add context summary for comparison
        context_count = len(response_data.context_data.keys())
        st.caption(f"💭 No context used (ignoring {context_count} available data points)")
    
    @staticmethod
    def _render_contextual_response_column(response_data: ResponseData):
        """Render the contextual response column."""
        st.subheader("✅ Context ON")
        st.info(f"Query: {response_data.query}")
        
        # Display context in expandable section
        UIComponents.render_context_expander(response_data.context_data)
        
        # Add response quality indicator
        context_count = len(response_data.context_data.keys())
        st.caption(f"🎯 Personalized AI Response (using {context_count} context points)")
        
        st.markdown(f"**Response:**\n\n{response_data.contextual_response}")
    
    @staticmethod
    def render_loading_indicator(message: str = "🤖 AI is thinking...", 
                               show_spinner: bool = True):
        """
        Render loading indicator for AI processing.
        
        Args:
            message: Loading message to display
            show_spinner: Whether to show spinner animation
        """
        if show_spinner:
            return st.spinner(message)
        else:
            st.info(message)
            return None
    
    @staticmethod
    def render_error_display(error_message: str, error_type: str = "Error", 
                           show_details: bool = False, details: Optional[str] = None):
        """
        Render error message with optional details.
        
        Args:
            error_message: Main error message to display
            error_type: Type of error (Error, Warning, etc.)
            show_details: Whether to show detailed error information
            details: Detailed error information
        """
        if error_type.lower() == "warning":
            st.warning(f"⚠️ {error_message}")
        else:
            st.error(f"❌ {error_message}")
        
        if show_details and details:
            with st.expander("🔍 Error Details"):
                st.code(details)
    
    @staticmethod
    def render_success_message(message: str, details: Optional[str] = None):
        """
        Render success message with optional details.
        
        Args:
            message: Success message to display
            details: Optional additional details
        """
        st.success(f"✅ {message}")
        if details:
            st.caption(details)
    
    @staticmethod
    def render_info_message(message: str, icon: str = "ℹ️"):
        """
        Render informational message.
        
        Args:
            message: Information message to display
            icon: Icon to display with the message
        """
        st.info(f"{icon} {message}")
    
    @staticmethod
    def render_demo_placeholder(industry_name: str):
        """
        Render placeholder message when no query is entered.
        
        Args:
            industry_name: Name of the current industry
        """
        st.info(f"👆 Enter a {industry_name.lower()}-related query above to see the context difference!")
    
    @staticmethod
    def render_footer(ai_enabled: bool):
        """
        Render application footer with mode information.
        
        Args:
            ai_enabled: Whether AI mode is currently enabled
        """
        st.markdown("---")
        if ai_enabled:
            st.markdown("**🤖 AI-Powered Demo:** Real AI responses show how context transforms generic answers into personalized, actionable insights.")
        else:
            st.markdown("**📝 Demo Mode:** Set API key environment variable to enable real AI responses and see the full power of context engineering.")
    
    @staticmethod
    def render_debug_sidebar(debug_info: Dict[str, Any]):
        """
        Render debug information in sidebar.
        
        Args:
            debug_info: Dictionary containing debug information
        """
        if st.sidebar.checkbox("Show Debug Info"):
            st.sidebar.markdown("### Debug Information")
            for key, value in debug_info.items():
                st.sidebar.markdown(f"**{key}:** {value}")
    
    @staticmethod
    def create_response_data(generic_response: str, contextual_response: str,
                           context_data: Dict[str, Any], query: str, 
                           industry: str) -> ResponseData:
        """
        Create ResponseData object with timestamp.
        
        Args:
            generic_response: Generic AI response
            contextual_response: Contextual AI response
            context_data: Context information used
            query: Original user query
            industry: Industry name
            
        Returns:
            ResponseData object
        """
        return ResponseData(
            generic_response=generic_response,
            contextual_response=contextual_response,
            context_data=context_data,
            query=query,
            industry=industry,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def create_metrics_data(ai_enabled: bool, industries_count: int = 6) -> MetricsData:
        """
        Create MetricsData object with current application state.
        
        Args:
            ai_enabled: Whether AI is currently enabled
            industries_count: Number of available industries
            
        Returns:
            MetricsData object
        """
        return MetricsData(
            industries_count=industries_count,
            context_points="50+",
            response_quality="10x" if ai_enabled else "Demo",
            user_satisfaction="95%",
            ai_enabled=ai_enabled
        )


class LayoutManager:
    """Utility class for managing page layouts and responsive design."""
    
    @staticmethod
    def create_two_column_layout(left_ratio: float = 0.5) -> Tuple[Any, Any]:
        """
        Create a two-column layout with specified ratio.
        
        Args:
            left_ratio: Ratio for left column (0.0 to 1.0)
            
        Returns:
            Tuple of (left_column, right_column)
        """
        right_ratio = 1.0 - left_ratio
        return st.columns([left_ratio, right_ratio])
    
    @staticmethod
    def create_three_column_layout(ratios: Optional[List[float]] = None) -> Tuple[Any, Any, Any]:
        """
        Create a three-column layout with specified ratios.
        
        Args:
            ratios: List of ratios for columns, defaults to equal
            
        Returns:
            Tuple of (left_column, center_column, right_column)
        """
        if ratios is None:
            ratios = [1, 1, 1]
        return st.columns(ratios)
    
    @staticmethod
    def create_centered_container(width: str = "80%"):
        """
        Create a centered container with specified width.
        
        Args:
            width: CSS width value for the container
            
        Returns:
            Streamlit container
        """
        col1, col2, col3 = st.columns([1, 2, 1])
        return col2
    
    @staticmethod
    def add_vertical_space(lines: int = 1):
        """
        Add vertical spacing between elements.
        
        Args:
            lines: Number of empty lines to add
        """
        for _ in range(lines):
            st.write("")
    
    @staticmethod
    def create_sidebar_section(title: str, content_func):
        """
        Create a sidebar section with title and content.
        
        Args:
            title: Section title
            content_func: Function to render section content
        """
        st.sidebar.markdown(f"### {title}")
        content_func()
        st.sidebar.markdown("---")


# Convenience functions for common UI patterns
def render_demo_header(industry_name: str, icon: str = "🏢"):
    """Convenience function to render demo header."""
    st.header(f"{icon} {industry_name}")


def render_query_section(industry_name: str, placeholder: str, 
                        sample_queries: List[str]) -> Optional[str]:
    """Convenience function to render complete query input section."""
    # Render sample queries
    input_key = f"{industry_name.lower().replace(' ', '_')}_query"
    UIComponents.render_sample_queries(sample_queries, industry_name, input_key)
    
    # Render query input
    return UIComponents.render_query_input(industry_name, placeholder, input_key)


def render_response_comparison(generic_response: str, contextual_response: str,
                             context_data: Dict[str, Any], query: str, 
                             industry: str):
    """Convenience function to render complete response comparison."""
    response_data = UIComponents.create_response_data(
        generic_response, contextual_response, context_data, query, industry
    )
    UIComponents.render_comparison_columns(response_data)