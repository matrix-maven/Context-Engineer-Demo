"""
Layout Management Utilities for Context Engineering Demo

This module provides utilities for managing page layouts, responsive design,
and consistent styling across the application.
"""
import streamlit as st
from typing import List, Optional, Dict, Any, Callable, Tuple
from contextlib import contextmanager


class ResponsiveLayout:
    """Handles responsive layout management for different screen sizes."""
    
    @staticmethod
    def get_column_config(screen_size: str = "desktop") -> Dict[str, List[float]]:
        """
        Get column configurations for different screen sizes.
        
        Args:
            screen_size: Target screen size (desktop, tablet, mobile)
            
        Returns:
            Dictionary with column ratio configurations
        """
        configs = {
            "desktop": {
                "two_column": [1, 1],
                "three_column": [1, 1, 1],
                "sidebar_main": [1, 3],
                "main_sidebar": [3, 1],
                "metrics": [1, 1, 1, 1]
            },
            "tablet": {
                "two_column": [1, 1],
                "three_column": [1, 2, 1],
                "sidebar_main": [1, 2],
                "main_sidebar": [2, 1],
                "metrics": [1, 1, 1, 1]
            },
            "mobile": {
                "two_column": [1],  # Stack vertically
                "three_column": [1],  # Stack vertically
                "sidebar_main": [1],  # Stack vertically
                "main_sidebar": [1],  # Stack vertically
                "metrics": [1, 1]  # Two rows of two
            }
        }
        return configs.get(screen_size, configs["desktop"])
    
    @staticmethod
    def create_responsive_columns(layout_type: str, screen_size: str = "desktop"):
        """
        Create responsive columns based on layout type and screen size.
        
        Args:
            layout_type: Type of layout (two_column, three_column, etc.)
            screen_size: Target screen size
            
        Returns:
            Streamlit columns
        """
        config = ResponsiveLayout.get_column_config(screen_size)
        ratios = config.get(layout_type, [1, 1])
        return st.columns(ratios)


class PageLayout:
    """Manages overall page layout structure."""
    
    @staticmethod
    def setup_page_config(title: str = "Context Engineering Demo", 
                         icon: str = "🧠", layout: str = "wide"):
        """
        Setup page configuration with consistent settings.
        
        Args:
            title: Page title
            icon: Page icon
            layout: Page layout (wide, centered)
        """
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    @contextmanager
    def main_container():
        """Context manager for main content container."""
        with st.container():
            yield
    
    @staticmethod
    @contextmanager
    def sidebar_container():
        """Context manager for sidebar content."""
        with st.sidebar:
            yield
    
    @staticmethod
    def create_header_section(title: str, subtitle: str = "", 
                            show_divider: bool = True):
        """
        Create standardized header section.
        
        Args:
            title: Main title
            subtitle: Optional subtitle
            show_divider: Whether to show divider after header
        """
        st.title(title)
        if subtitle:
            st.markdown(subtitle)
        if show_divider:
            st.markdown("---")
    
    @staticmethod
    def create_footer_section(content: str, show_divider: bool = True):
        """
        Create standardized footer section.
        
        Args:
            content: Footer content
            show_divider: Whether to show divider before footer
        """
        if show_divider:
            st.markdown("---")
        st.markdown(content)


class ComponentLayout:
    """Manages layout for specific UI components."""
    
    @staticmethod
    def create_metrics_grid(metrics_data: List[Dict[str, Any]], 
                          columns: int = 4) -> None:
        """
        Create a grid layout for metrics display.
        
        Args:
            metrics_data: List of metric dictionaries
            columns: Number of columns in the grid
        """
        cols = st.columns(columns)
        for i, metric in enumerate(metrics_data):
            with cols[i % columns]:
                st.metric(
                    label=metric.get("label", ""),
                    value=metric.get("value", ""),
                    delta=metric.get("delta", None)
                )
    
    @staticmethod
    def create_comparison_layout(left_content: Callable, right_content: Callable,
                               left_title: str = "", right_title: str = "",
                               ratio: List[float] = [1, 1]):
        """
        Create side-by-side comparison layout.
        
        Args:
            left_content: Function to render left content
            right_content: Function to render right content
            left_title: Title for left column
            right_title: Title for right column
            ratio: Column width ratios
        """
        col1, col2 = st.columns(ratio)
        
        with col1:
            if left_title:
                st.subheader(left_title)
            left_content()
        
        with col2:
            if right_title:
                st.subheader(right_title)
            right_content()
    
    @staticmethod
    def create_tabbed_layout(tabs: Dict[str, Callable]) -> str:
        """
        Create tabbed layout with content functions.
        
        Args:
            tabs: Dictionary mapping tab names to content functions
            
        Returns:
            Name of the selected tab
        """
        tab_names = list(tabs.keys())
        selected_tabs = st.tabs(tab_names)
        
        for i, (tab_name, content_func) in enumerate(tabs.items()):
            with selected_tabs[i]:
                content_func()
        
        return tab_names[0]  # Return first tab as default
    
    @staticmethod
    def create_expandable_section(title: str, content_func: Callable, 
                                expanded: bool = False) -> bool:
        """
        Create expandable section with content.
        
        Args:
            title: Section title
            content_func: Function to render content
            expanded: Whether section is expanded by default
            
        Returns:
            Whether section is currently expanded
        """
        with st.expander(title, expanded=expanded):
            content_func()
            return True
        return False
    
    @staticmethod
    def create_card_layout(title: str, content: str, 
                          actions: Optional[List[Dict[str, Any]]] = None):
        """
        Create card-style layout for content.
        
        Args:
            title: Card title
            content: Card content
            actions: Optional list of action buttons
        """
        with st.container():
            st.markdown(f"### {title}")
            st.markdown(content)
            
            if actions:
                cols = st.columns(len(actions))
                for i, action in enumerate(actions):
                    with cols[i]:
                        if st.button(action.get("label", "Action"), 
                                   key=action.get("key", f"action_{i}")):
                            if "callback" in action:
                                action["callback"]()


class FormLayout:
    """Manages form layouts and input grouping."""
    
    @staticmethod
    def create_input_group(title: str, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create grouped input fields with title.
        
        Args:
            title: Group title
            inputs: List of input field configurations
            
        Returns:
            Dictionary of input values
        """
        st.markdown(f"#### {title}")
        values = {}
        
        for input_config in inputs:
            input_type = input_config.get("type", "text")
            key = input_config.get("key", "")
            label = input_config.get("label", "")
            
            if input_type == "text":
                values[key] = st.text_input(
                    label, 
                    value=input_config.get("default", ""),
                    placeholder=input_config.get("placeholder", "")
                )
            elif input_type == "select":
                values[key] = st.selectbox(
                    label,
                    options=input_config.get("options", []),
                    index=input_config.get("default_index", 0)
                )
            elif input_type == "multiselect":
                values[key] = st.multiselect(
                    label,
                    options=input_config.get("options", []),
                    default=input_config.get("default", [])
                )
            elif input_type == "slider":
                values[key] = st.slider(
                    label,
                    min_value=input_config.get("min", 0),
                    max_value=input_config.get("max", 100),
                    value=input_config.get("default", 50)
                )
        
        return values
    
    @staticmethod
    def create_button_group(buttons: List[Dict[str, Any]], 
                          layout: str = "horizontal") -> Optional[str]:
        """
        Create group of buttons with specified layout.
        
        Args:
            buttons: List of button configurations
            layout: Layout type (horizontal, vertical)
            
        Returns:
            Key of clicked button or None
        """
        if layout == "horizontal":
            cols = st.columns(len(buttons))
            for i, button in enumerate(buttons):
                with cols[i]:
                    if st.button(
                        button.get("label", "Button"),
                        key=button.get("key", f"btn_{i}"),
                        help=button.get("help", ""),
                        use_container_width=True
                    ):
                        return button.get("key", f"btn_{i}")
        else:  # vertical
            for button in buttons:
                if st.button(
                    button.get("label", "Button"),
                    key=button.get("key", f"btn_{button.get('label', 'btn')}"),
                    help=button.get("help", ""),
                    use_container_width=True
                ):
                    return button.get("key", f"btn_{button.get('label', 'btn')}")
        
        return None


class StyleManager:
    """Manages custom styling and CSS."""
    
    @staticmethod
    def apply_custom_css(css: str):
        """
        Apply custom CSS to the application.
        
        Args:
            css: CSS string to apply
        """
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def get_demo_styles() -> str:
        """
        Get CSS styles for the demo application.
        
        Returns:
            CSS string with demo-specific styles
        """
        return """
        .metric-container {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .comparison-column {
            border: 1px solid #e0e0e0;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .context-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #007bff;
        }
        
        .response-section {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .sample-query-button {
            margin: 0.25rem;
            width: 100%;
        }
        
        .status-indicator {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
        }
        
        .status-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .status-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        """
    
    @staticmethod
    def apply_demo_styles():
        """Apply demo-specific styles to the application."""
        StyleManager.apply_custom_css(StyleManager.get_demo_styles())


# Utility functions for common layout patterns
def create_demo_page_layout(title: str, subtitle: str = "", 
                          apply_styles: bool = True):
    """
    Create standard demo page layout with header and styling.
    
    Args:
        title: Page title
        subtitle: Optional subtitle
        apply_styles: Whether to apply custom styles
    """
    if apply_styles:
        StyleManager.apply_demo_styles()
    
    PageLayout.create_header_section(title, subtitle)


def create_industry_demo_layout(industry_name: str, icon: str = "🏢"):
    """
    Create standard layout for industry demo pages.
    
    Args:
        industry_name: Name of the industry
        icon: Industry icon
    """
    st.header(f"{icon} {industry_name}")


def create_two_column_comparison(left_title: str = "❌ Context OFF",
                               right_title: str = "✅ Context ON"):
    """
    Create two-column layout for response comparison.
    
    Args:
        left_title: Title for left column
        right_title: Title for right column
        
    Returns:
        Tuple of (left_column, right_column)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(left_title)
    
    with col2:
        st.subheader(right_title)
    
    return col1, col2