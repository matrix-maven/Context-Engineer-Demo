"""
Integration Tests for UI Components

This module contains integration tests to verify that UI components
work together correctly in realistic scenarios.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import components to test
from ui.components import UIComponents, ResponseData, MetricsData
from ui.layout import PageLayout, ComponentLayout, StyleManager
from demos.base_demo import BaseDemo, DemoResponse


class MockDemo(BaseDemo):
    """Mock demo class for testing."""
    
    def __init__(self):
        super().__init__("Test Industry", None, None, None)
    
    def generate_context(self):
        return {"user": "test", "preferences": ["A", "B"]}
    
    def get_sample_queries(self):
        return ["Query 1", "Query 2", "Query 3"]
    
    def get_query_placeholder(self):
        return "Test placeholder"
    
    def get_system_message_generic(self):
        return "Generic system message"
    
    def get_system_message_contextual(self):
        return "Contextual system message"
    
    def generate_fallback_generic_response(self, query):
        return f"Generic response for: {query}"
    
    def generate_fallback_contextual_response(self, query, context):
        return f"Contextual response for: {query} with context: {list(context.keys())}"


class TestUIIntegration:
    """Integration tests for UI components."""
    
    def test_complete_demo_workflow(self):
        """Test complete demo workflow with UI components."""
        demo = MockDemo()
        
        # Test query handling
        response = demo.handle_query("Test query")
        
        assert isinstance(response, DemoResponse)
        assert response.query == "Test query"
        assert response.industry == "Test Industry"
        assert "Generic response for: Test query" in response.generic_response
        assert "Contextual response for: Test query" in response.contextual_response
        assert isinstance(response.context_data, dict)
    
    def test_response_data_conversion(self):
        """Test conversion between DemoResponse and ResponseData."""
        demo = MockDemo()
        demo_response = demo.handle_query("Test query")
        
        # Convert to UI ResponseData
        ui_response = UIComponents.create_response_data(
            generic_response=demo_response.generic_response,
            contextual_response=demo_response.contextual_response,
            context_data=demo_response.context_data,
            query=demo_response.query,
            industry=demo_response.industry
        )
        
        assert ui_response.generic_response == demo_response.generic_response
        assert ui_response.contextual_response == demo_response.contextual_response
        assert ui_response.context_data == demo_response.context_data
        assert ui_response.query == demo_response.query
        assert ui_response.industry == demo_response.industry
        assert isinstance(ui_response.timestamp, datetime)
    
    def test_metrics_data_creation(self):
        """Test metrics data creation with different scenarios."""
        # Test AI enabled
        metrics_ai = UIComponents.create_metrics_data(ai_enabled=True, industries_count=8)
        assert metrics_ai.ai_enabled is True
        assert metrics_ai.response_quality == "10x"
        assert metrics_ai.industries_count == 8
        
        # Test AI disabled
        metrics_no_ai = UIComponents.create_metrics_data(ai_enabled=False, industries_count=6)
        assert metrics_no_ai.ai_enabled is False
        assert metrics_no_ai.response_quality == "Demo"
        assert metrics_no_ai.industries_count == 6
    
    def test_style_integration(self):
        """Test style management integration."""
        styles = StyleManager.get_demo_styles()
        
        # Verify key styles are present
        assert ".metric-container" in styles
        assert ".comparison-column" in styles
        assert ".context-section" in styles
        assert ".response-section" in styles
        assert ".sample-query-button" in styles
        
        # Verify styles are valid CSS-like format
        assert "{" in styles and "}" in styles
        assert "background-color" in styles
        assert "padding" in styles
        assert "border-radius" in styles
    
    @patch('streamlit.set_page_config')
    def test_page_layout_setup(self, mock_set_page_config):
        """Test page layout setup integration."""
        PageLayout.setup_page_config(
            title="Test Demo",
            icon="🧪",
            layout="wide"
        )
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Demo",
            page_icon="🧪",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def test_demo_ui_component_integration(self):
        """Test that demo classes can use UI components without errors."""
        demo = MockDemo()
        
        # Test that demo can generate context
        context = demo.generate_context()
        assert isinstance(context, dict)
        assert len(context) > 0
        
        # Test that demo can get sample queries
        queries = demo.get_sample_queries()
        assert isinstance(queries, list)
        assert len(queries) > 0
        
        # Test that demo can generate responses
        generic_response = demo.generate_fallback_generic_response("test")
        contextual_response = demo.generate_fallback_contextual_response("test", context)
        
        assert isinstance(generic_response, str)
        assert isinstance(contextual_response, str)
        assert len(generic_response) > 0
        assert len(contextual_response) > 0
    
    def test_error_handling_integration(self):
        """Test error handling across UI components."""
        # Test with invalid data
        try:
            UIComponents.create_response_data(
                generic_response="",
                contextual_response="",
                context_data={},
                query="",
                industry=""
            )
            # Should not raise an error, just create empty data
            assert True
        except Exception as e:
            pytest.fail(f"UI components should handle empty data gracefully: {e}")
    
    def test_component_data_flow(self):
        """Test data flow between different UI components."""
        # Create initial data
        demo = MockDemo()
        demo_response = demo.handle_query("Integration test query")
        
        # Convert to UI format
        ui_response = UIComponents.create_response_data(
            generic_response=demo_response.generic_response,
            contextual_response=demo_response.contextual_response,
            context_data=demo_response.context_data,
            query=demo_response.query,
            industry=demo_response.industry
        )
        
        # Create metrics
        metrics = UIComponents.create_metrics_data(ai_enabled=False, industries_count=1)
        
        # Verify data consistency
        assert ui_response.query == demo_response.query
        assert ui_response.industry == demo_response.industry
        assert metrics.industries_count == 1
        assert metrics.ai_enabled is False
    
    def test_layout_component_integration(self):
        """Test layout components work together."""
        # Test responsive layout configurations
        desktop_config = ComponentLayout.__dict__  # Access class methods
        
        # Verify ComponentLayout has required methods
        assert hasattr(ComponentLayout, 'create_metrics_grid')
        assert hasattr(ComponentLayout, 'create_comparison_layout')
        assert hasattr(ComponentLayout, 'create_tabbed_layout')
        assert hasattr(ComponentLayout, 'create_expandable_section')
    
    def test_ui_component_consistency(self):
        """Test UI component method consistency."""
        # Verify UIComponents has all required methods
        required_methods = [
            'render_page_header',
            'render_ai_status_indicator', 
            'render_metrics_dashboard',
            'render_industry_selector',
            'render_query_input',
            'render_sample_queries',
            'render_context_expander',
            'render_comparison_columns',
            'render_loading_indicator',
            'render_error_display',
            'render_success_message',
            'render_info_message',
            'render_demo_placeholder',
            'render_footer',
            'render_debug_sidebar',
            'create_response_data',
            'create_metrics_data'
        ]
        
        for method_name in required_methods:
            assert hasattr(UIComponents, method_name), f"UIComponents missing method: {method_name}"
    
    def test_layout_manager_consistency(self):
        """Test LayoutManager method consistency."""
        from ui.components import LayoutManager
        
        required_methods = [
            'create_two_column_layout',
            'create_three_column_layout', 
            'create_centered_container',
            'add_vertical_space'
        ]
        
        for method_name in required_methods:
            assert hasattr(LayoutManager, method_name), f"LayoutManager missing method: {method_name}"


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""
    
    def test_demo_rendering_scenario(self):
        """Test a realistic demo rendering scenario."""
        demo = MockDemo()
        
        # Simulate user entering a query
        user_query = "I need help with something"
        
        # Process the query
        response = demo.handle_query(user_query)
        
        # Convert for UI display
        ui_response = UIComponents.create_response_data(
            generic_response=response.generic_response,
            contextual_response=response.contextual_response,
            context_data=response.context_data,
            query=response.query,
            industry=response.industry
        )
        
        # Verify the complete flow works
        assert ui_response.query == user_query
        assert "Generic response for:" in ui_response.generic_response
        assert "Contextual response for:" in ui_response.contextual_response
        assert len(ui_response.context_data) > 0
    
    def test_multi_industry_scenario(self):
        """Test scenario with multiple industries."""
        industries = ["Restaurant", "Healthcare", "E-commerce"]
        
        for industry in industries:
            # Create metrics for each industry
            metrics = UIComponents.create_metrics_data(
                ai_enabled=True,
                industries_count=len(industries)
            )
            
            assert metrics.industries_count == len(industries)
            assert metrics.ai_enabled is True
    
    def test_error_recovery_scenario(self):
        """Test error recovery in realistic scenarios."""
        demo = MockDemo()
        
        # Test with empty query
        response = demo.handle_query("")
        assert isinstance(response, DemoResponse)
        
        # Test with very long query
        long_query = "x" * 1000
        response = demo.handle_query(long_query)
        assert isinstance(response, DemoResponse)
        assert response.query == long_query


if __name__ == "__main__":
    pytest.main([__file__])