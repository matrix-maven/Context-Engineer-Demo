"""
Tests for UI Components

This module contains tests for the reusable UI components to ensure
they function correctly and maintain consistency.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import Dict, Any

# Import the components to test
from ui.components import UIComponents, ResponseData, MetricsData, LayoutManager
from ui.layout import ResponsiveLayout, PageLayout, ComponentLayout, FormLayout, StyleManager


class TestUIComponents:
    """Test cases for UIComponents class."""
    
    def test_create_response_data(self):
        """Test ResponseData creation."""
        response_data = UIComponents.create_response_data(
            generic_response="Generic response",
            contextual_response="Contextual response",
            context_data={"key": "value"},
            query="Test query",
            industry="Test Industry"
        )
        
        assert response_data.generic_response == "Generic response"
        assert response_data.contextual_response == "Contextual response"
        assert response_data.context_data == {"key": "value"}
        assert response_data.query == "Test query"
        assert response_data.industry == "Test Industry"
        assert isinstance(response_data.timestamp, datetime)
    
    def test_create_metrics_data(self):
        """Test MetricsData creation."""
        # Test with AI enabled
        metrics_ai = UIComponents.create_metrics_data(ai_enabled=True, industries_count=8)
        assert metrics_ai.industries_count == 8
        assert metrics_ai.response_quality == "10x"
        assert metrics_ai.ai_enabled is True
        
        # Test with AI disabled
        metrics_no_ai = UIComponents.create_metrics_data(ai_enabled=False)
        assert metrics_no_ai.industries_count == 6
        assert metrics_no_ai.response_quality == "Demo"
        assert metrics_no_ai.ai_enabled is False
    
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    def test_render_page_header(self, mock_markdown, mock_title):
        """Test page header rendering."""
        UIComponents.render_page_header("Test Title", "Test Subtitle")
        
        mock_title.assert_called_once_with("Test Title")
        mock_markdown.assert_called_once_with("Test Subtitle")
    
    @patch('streamlit.success')
    @patch('streamlit.warning')
    def test_render_ai_status_indicator(self, mock_warning, mock_success):
        """Test AI status indicator rendering."""
        # Test AI enabled
        UIComponents.render_ai_status_indicator(True, "OpenAI")
        mock_success.assert_called_once_with("🤖 **AI Mode**: Real OpenAI responses enabled")
        
        # Test AI disabled
        UIComponents.render_ai_status_indicator(False)
        mock_warning.assert_called_once_with("📝 **Fallback Mode**: Using static responses (set API key for AI)")
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_render_metrics_dashboard(self, mock_metric, mock_columns):
        """Test metrics dashboard rendering."""
        # Create mock columns that support context manager protocol
        mock_cols = []
        for _ in range(4):
            mock_col = Mock()
            mock_col.__enter__ = Mock(return_value=mock_col)
            mock_col.__exit__ = Mock(return_value=None)
            mock_cols.append(mock_col)
        
        mock_columns.return_value = mock_cols
        
        metrics = MetricsData(
            industries_count=6,
            context_points="50+",
            response_quality="10x",
            user_satisfaction="95%",
            ai_enabled=True
        )
        
        UIComponents.render_metrics_dashboard(metrics)
        
        mock_columns.assert_called_once_with(4)
        assert mock_metric.call_count == 4
    
    @patch('streamlit.sidebar')
    def test_render_industry_selector(self, mock_sidebar):
        """Test industry selector rendering."""
        mock_sidebar.title = Mock()
        mock_sidebar.selectbox = Mock(return_value="Test Industry")
        
        industries = ["Industry 1", "Industry 2", "Test Industry"]
        result = UIComponents.render_industry_selector(industries, "test_key")
        
        mock_sidebar.title.assert_called_once_with("Select Industry")
        mock_sidebar.selectbox.assert_called_once_with(
            "Choose an industry to explore:",
            industries,
            key="test_key"
        )
        assert result == "Test Industry"
    
    @patch('streamlit.text_input')
    def test_render_query_input(self, mock_text_input):
        """Test query input rendering."""
        mock_text_input.return_value = "Test query"
        
        result = UIComponents.render_query_input(
            "Test Industry", 
            "Test placeholder", 
            "test_key"
        )
        
        mock_text_input.assert_called_once_with(
            "🎤 Enter your test industry request:",
            placeholder="Test placeholder",
            key="test_key"
        )
        assert result == "Test query"
    
    @patch('streamlit.columns')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.session_state', {})
    @patch('streamlit.rerun')
    def test_render_sample_queries(self, mock_rerun, mock_markdown, mock_button, mock_columns):
        """Test sample queries rendering."""
        # Create mock columns that support context manager protocol
        mock_cols = []
        for _ in range(3):
            mock_col = Mock()
            mock_col.__enter__ = Mock(return_value=mock_col)
            mock_col.__exit__ = Mock(return_value=None)
            mock_cols.append(mock_col)
        
        mock_columns.return_value = mock_cols
        mock_button.return_value = True
        
        queries = ["Query 1", "Query 2", "Query 3"]
        UIComponents.render_sample_queries(queries, "Test Industry", "test_key")
        
        mock_markdown.assert_called_once_with("**💡 Try these sample queries:**")
        mock_columns.assert_called_once_with(3)
        assert mock_button.call_count == 3
    
    @patch('streamlit.expander')
    def test_render_context_expander(self, mock_expander):
        """Test context expander rendering."""
        mock_expander_obj = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_obj)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        context_data = {"key1": "value1", "key2": ["item1", "item2"]}
        result = UIComponents.render_context_expander(context_data, "Test Context")
        
        mock_expander.assert_called_once_with("Test Context")
        assert result is True
    
    @patch('streamlit.columns')
    def test_render_comparison_columns(self, mock_columns):
        """Test comparison columns rendering."""
        # Create mock columns that support context manager protocol
        mock_cols = []
        for _ in range(2):
            mock_col = Mock()
            mock_col.__enter__ = Mock(return_value=mock_col)
            mock_col.__exit__ = Mock(return_value=None)
            mock_cols.append(mock_col)
        
        mock_columns.return_value = mock_cols
        
        response_data = ResponseData(
            generic_response="Generic",
            contextual_response="Contextual",
            context_data={"key": "value"},
            query="Test query",
            industry="Test Industry"
        )
        
        with patch.object(UIComponents, '_render_generic_response_column') as mock_generic, \
             patch.object(UIComponents, '_render_contextual_response_column') as mock_contextual:
            
            UIComponents.render_comparison_columns(response_data)
            
            mock_columns.assert_called_once_with(2)
            mock_generic.assert_called_once_with(response_data)
            mock_contextual.assert_called_once_with(response_data)
    
    @patch('streamlit.spinner')
    @patch('streamlit.info')
    def test_render_loading_indicator(self, mock_info, mock_spinner):
        """Test loading indicator rendering."""
        # Test with spinner
        UIComponents.render_loading_indicator("Loading...", True)
        mock_spinner.assert_called_once_with("Loading...")
        
        # Test without spinner
        UIComponents.render_loading_indicator("Loading...", False)
        mock_info.assert_called_once_with("Loading...")
    
    @patch('streamlit.error')
    @patch('streamlit.warning')
    @patch('streamlit.expander')
    def test_render_error_display(self, mock_expander, mock_warning, mock_error):
        """Test error display rendering."""
        # Test error type
        UIComponents.render_error_display("Test error", "Error")
        mock_error.assert_called_once_with("❌ Test error")
        
        # Test warning type
        UIComponents.render_error_display("Test warning", "Warning")
        mock_warning.assert_called_once_with("⚠️ Test warning")
        
        # Test with details
        mock_expander_obj = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_obj)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        UIComponents.render_error_display("Test error", "Error", True, "Error details")
        mock_expander.assert_called_once_with("🔍 Error Details")
    
    @patch('streamlit.success')
    @patch('streamlit.caption')
    def test_render_success_message(self, mock_caption, mock_success):
        """Test success message rendering."""
        UIComponents.render_success_message("Success!", "Details")
        
        mock_success.assert_called_once_with("✅ Success!")
        mock_caption.assert_called_once_with("Details")
    
    @patch('streamlit.info')
    def test_render_info_message(self, mock_info):
        """Test info message rendering."""
        UIComponents.render_info_message("Info message", "🔔")
        mock_info.assert_called_once_with("🔔 Info message")
    
    @patch('streamlit.info')
    def test_render_demo_placeholder(self, mock_info):
        """Test demo placeholder rendering."""
        UIComponents.render_demo_placeholder("Test Industry")
        mock_info.assert_called_once_with("👆 Enter a test industry-related query above to see the context difference!")


class TestLayoutManager:
    """Test cases for LayoutManager class."""
    
    @patch('streamlit.columns')
    def test_create_two_column_layout(self, mock_columns):
        """Test two-column layout creation."""
        mock_columns.return_value = ("col1", "col2")
        
        result = LayoutManager.create_two_column_layout(0.6)
        
        mock_columns.assert_called_once_with([0.6, 0.4])
        assert result == ("col1", "col2")
    
    @patch('streamlit.columns')
    def test_create_three_column_layout(self, mock_columns):
        """Test three-column layout creation."""
        mock_columns.return_value = ("col1", "col2", "col3")
        
        # Test with custom ratios
        result = LayoutManager.create_three_column_layout([2, 1, 1])
        mock_columns.assert_called_once_with([2, 1, 1])
        assert result == ("col1", "col2", "col3")
        
        # Test with default ratios
        mock_columns.reset_mock()
        LayoutManager.create_three_column_layout()
        mock_columns.assert_called_once_with([1, 1, 1])
    
    @patch('streamlit.columns')
    def test_create_centered_container(self, mock_columns):
        """Test centered container creation."""
        mock_columns.return_value = ("col1", "col2", "col3")
        
        result = LayoutManager.create_centered_container()
        
        mock_columns.assert_called_once_with([1, 2, 1])
        assert result == "col2"
    
    @patch('streamlit.write')
    def test_add_vertical_space(self, mock_write):
        """Test vertical space addition."""
        LayoutManager.add_vertical_space(3)
        assert mock_write.call_count == 3


class TestResponsiveLayout:
    """Test cases for ResponsiveLayout class."""
    
    def test_get_column_config(self):
        """Test column configuration retrieval."""
        # Test desktop config
        desktop_config = ResponsiveLayout.get_column_config("desktop")
        assert "two_column" in desktop_config
        assert desktop_config["two_column"] == [1, 1]
        
        # Test mobile config
        mobile_config = ResponsiveLayout.get_column_config("mobile")
        assert mobile_config["two_column"] == [1]  # Stacked
        
        # Test invalid config (should return desktop)
        invalid_config = ResponsiveLayout.get_column_config("invalid")
        assert invalid_config == ResponsiveLayout.get_column_config("desktop")
    
    @patch('streamlit.columns')
    def test_create_responsive_columns(self, mock_columns):
        """Test responsive column creation."""
        mock_columns.return_value = ("col1", "col2")
        
        ResponsiveLayout.create_responsive_columns("two_column", "desktop")
        mock_columns.assert_called_once_with([1, 1])


class TestPageLayout:
    """Test cases for PageLayout class."""
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config(self, mock_set_page_config):
        """Test page configuration setup."""
        PageLayout.setup_page_config("Test Title", "🧪", "centered")
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Title",
            page_icon="🧪",
            layout="centered",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    def test_create_header_section(self, mock_markdown, mock_title):
        """Test header section creation."""
        PageLayout.create_header_section("Test Title", "Test Subtitle", True)
        
        mock_title.assert_called_once_with("Test Title")
        assert mock_markdown.call_count == 2  # subtitle + divider
    
    @patch('streamlit.markdown')
    def test_create_footer_section(self, mock_markdown):
        """Test footer section creation."""
        PageLayout.create_footer_section("Footer content", True)
        
        assert mock_markdown.call_count == 2  # divider + content


class TestComponentLayout:
    """Test cases for ComponentLayout class."""
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_create_metrics_grid(self, mock_metric, mock_columns):
        """Test metrics grid creation."""
        # Create mock columns that support context manager protocol
        mock_cols = []
        for _ in range(4):
            mock_col = Mock()
            mock_col.__enter__ = Mock(return_value=mock_col)
            mock_col.__exit__ = Mock(return_value=None)
            mock_cols.append(mock_col)
        
        mock_columns.return_value = mock_cols
        
        metrics_data = [
            {"label": "Metric 1", "value": "100", "delta": "+10"},
            {"label": "Metric 2", "value": "200", "delta": "+20"}
        ]
        
        ComponentLayout.create_metrics_grid(metrics_data, 4)
        
        mock_columns.assert_called_once_with(4)
        assert mock_metric.call_count == 2
    
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    def test_create_comparison_layout(self, mock_subheader, mock_columns):
        """Test comparison layout creation."""
        # Create mock columns that support context manager protocol
        mock_cols = []
        for _ in range(2):
            mock_col = Mock()
            mock_col.__enter__ = Mock(return_value=mock_col)
            mock_col.__exit__ = Mock(return_value=None)
            mock_cols.append(mock_col)
        
        mock_columns.return_value = mock_cols
        
        left_func = Mock()
        right_func = Mock()
        
        ComponentLayout.create_comparison_layout(
            left_func, right_func, "Left Title", "Right Title", [2, 1]
        )
        
        mock_columns.assert_called_once_with([2, 1])
        assert mock_subheader.call_count == 2
        left_func.assert_called_once()
        right_func.assert_called_once()
    
    @patch('streamlit.tabs')
    def test_create_tabbed_layout(self, mock_tabs):
        """Test tabbed layout creation."""
        # Create mock tab objects that support context manager protocol
        mock_tab_objects = []
        for _ in range(2):
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tab_objects.append(mock_tab)
        
        mock_tabs.return_value = mock_tab_objects
        
        content_func1 = Mock()
        content_func2 = Mock()
        tabs = {"Tab 1": content_func1, "Tab 2": content_func2}
        
        result = ComponentLayout.create_tabbed_layout(tabs)
        
        mock_tabs.assert_called_once_with(["Tab 1", "Tab 2"])
        content_func1.assert_called_once()
        content_func2.assert_called_once()
        assert result == "Tab 1"
    
    @patch('streamlit.expander')
    def test_create_expandable_section(self, mock_expander):
        """Test expandable section creation."""
        mock_expander_obj = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_obj)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        content_func = Mock()
        result = ComponentLayout.create_expandable_section("Test Title", content_func, True)
        
        mock_expander.assert_called_once_with("Test Title", expanded=True)
        content_func.assert_called_once()
        assert result is True


class TestStyleManager:
    """Test cases for StyleManager class."""
    
    @patch('streamlit.markdown')
    def test_apply_custom_css(self, mock_markdown):
        """Test custom CSS application."""
        css = "body { color: red; }"
        StyleManager.apply_custom_css(css)
        
        mock_markdown.assert_called_once_with(
            f"<style>{css}</style>", 
            unsafe_allow_html=True
        )
    
    def test_get_demo_styles(self):
        """Test demo styles retrieval."""
        styles = StyleManager.get_demo_styles()
        
        assert isinstance(styles, str)
        assert ".metric-container" in styles
        assert ".comparison-column" in styles
        assert ".context-section" in styles
    
    @patch.object(StyleManager, 'apply_custom_css')
    @patch.object(StyleManager, 'get_demo_styles')
    def test_apply_demo_styles(self, mock_get_styles, mock_apply_css):
        """Test demo styles application."""
        mock_get_styles.return_value = "test styles"
        
        StyleManager.apply_demo_styles()
        
        mock_get_styles.assert_called_once()
        mock_apply_css.assert_called_once_with("test styles")


# Integration tests
class TestUIIntegration:
    """Integration tests for UI components working together."""
    
    def test_response_data_integration(self):
        """Test ResponseData integration with UI components."""
        response_data = UIComponents.create_response_data(
            generic_response="Generic response",
            contextual_response="Contextual response",
            context_data={"user": "test", "preferences": ["A", "B"]},
            query="Test query",
            industry="Test Industry"
        )
        
        # Verify data structure
        assert hasattr(response_data, 'generic_response')
        assert hasattr(response_data, 'contextual_response')
        assert hasattr(response_data, 'context_data')
        assert hasattr(response_data, 'query')
        assert hasattr(response_data, 'industry')
        assert hasattr(response_data, 'timestamp')
        
        # Verify data types
        assert isinstance(response_data.context_data, dict)
        assert isinstance(response_data.timestamp, datetime)
    
    def test_metrics_data_integration(self):
        """Test MetricsData integration with UI components."""
        metrics = UIComponents.create_metrics_data(ai_enabled=True, industries_count=8)
        
        # Verify all required fields are present
        assert hasattr(metrics, 'industries_count')
        assert hasattr(metrics, 'context_points')
        assert hasattr(metrics, 'response_quality')
        assert hasattr(metrics, 'user_satisfaction')
        assert hasattr(metrics, 'ai_enabled')
        
        # Verify AI-specific values
        assert metrics.response_quality == "10x"
        assert metrics.ai_enabled is True


if __name__ == "__main__":
    pytest.main([__file__])