#!/usr/bin/env python3
"""
AI-Powered Context Engineering Demo
This is the enhanced version with real AI integration.
Fallback to app.py for static demo if needed.
"""
import streamlit as st
import os
import logging
from typing import Optional, Dict, Any

# Import configuration and settings
from config.settings import get_settings, AppSettings
from config.ai_config import AIConfig, load_ai_config, get_available_providers, get_default_provider
from config.settings import AIProvider

# Import AI services
from services.ai_orchestrator import AIServiceOrchestrator
from services.ai_service import PromptRequest, AIResponse
from services.prompt_service import get_prompt_service, Industry
from services.context_service import ContextService

# Import demo framework
from demos.demo_factory import DemoFactory

# Import UI components
from ui.components import UIComponents
from ui.layout import PageLayout

# Import error handling
from utils.error_handler import ErrorHandler
from utils.logger import setup_logging

# Import configuration validation
from config.validation import validate_and_setup, ValidationResult

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Configuration validation and startup checks
@st.cache_resource
def validate_configuration() -> tuple[bool, ValidationResult]:
    """Validate application configuration on startup."""
    try:
        logger.info("Starting configuration validation...")
        success, result = validate_and_setup()
        
        if success:
            logger.info("Configuration validation passed")
        else:
            logger.error(f"Configuration validation failed: {len(result.errors)} errors")
            for error in result.errors:
                logger.error(f"Config error: {error}")
        
        return success, result
    except Exception as e:
        logger.error(f"Configuration validation failed with exception: {e}")
        # Create a basic validation result for the error
        result = ValidationResult()
        result.add_error(f"Configuration validation failed: {str(e)}")
        return False, result

# Load application settings
@st.cache_resource
def load_app_configuration():
    """Load and validate application configuration."""
    try:
        settings = get_settings()
        logger.info(f"Loaded application settings: {settings.app_title}")
        return settings
    except Exception as e:
        logger.error(f"Failed to load application settings: {e}")
        # Return default settings if loading fails
        return AppSettings()

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all application services with proper error handling."""
    services = {}
    
    try:
        # Load configuration
        settings = load_app_configuration()
        services['settings'] = settings
        
        # Initialize context service
        context_service = ContextService()
        services['context_service'] = context_service
        logger.info("✅ Context service initialized")
        
        # Initialize AI orchestrator
        orchestrator = AIServiceOrchestrator(
            enable_caching=settings.enable_caching,
            cache_ttl_seconds=settings.cache_ttl,
            fallback_enabled=True
        )
        services['ai_orchestrator'] = orchestrator
        
        # Get available providers
        available_providers = orchestrator.get_available_providers()
        services['available_providers'] = available_providers
        
        if not available_providers:
            logger.warning("No AI providers available")
            services['ai_provider'] = None
            services['ai_enabled'] = False
            return services
        
        # Select provider
        default_provider = get_default_provider()
        if default_provider and default_provider in available_providers:
            target_provider = default_provider
        else:
            target_provider = available_providers[0]
            if default_provider:
                logger.warning(f"Default provider {default_provider.value} not available, using {target_provider.value}")
        
        # Set and validate provider
        if orchestrator.set_provider(target_provider):
            if orchestrator.validate_provider_connection(target_provider):
                services['ai_provider'] = target_provider
                services['ai_enabled'] = True
                logger.info(f"✅ AI provider {target_provider.value} connected successfully")
            else:
                logger.error(f"Failed to validate connection to {target_provider.value}")
                services['ai_provider'] = None
                services['ai_enabled'] = False
        else:
            logger.error(f"Failed to set provider {target_provider.value}")
            services['ai_provider'] = None
            services['ai_enabled'] = False
        
        return services
        
    except Exception as e:
        logger.error(f"Service initialization failed: {e}")
        # Return minimal services for fallback mode
        return {
            'settings': AppSettings(),
            'context_service': ContextService(),
            'ai_orchestrator': None,
            'ai_provider': None,
            'ai_enabled': False,
            'available_providers': []
        }

# Page configuration using settings
services = initialize_services()
settings = services['settings']

st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.app_icon,
    layout=settings.layout
)

# Enhanced AI Response Generator using all modular components
class AIResponseGenerator:
    """Enhanced AI response generator that integrates all modular services."""
    
    def __init__(self, services: Dict[str, Any]):
        """Initialize with all required services."""
        self.services = services
        self.orchestrator = services.get('ai_orchestrator')
        self.provider = services.get('ai_provider')
        self.context_service = services.get('context_service')
        self.settings = services.get('settings')
        self.use_ai = services.get('ai_enabled', False)
        
        # Initialize prompt service
        self.prompt_service = get_prompt_service()
        
        logger.info(f"AIResponseGenerator initialized: AI enabled={self.use_ai}, Provider={self.provider}")
    
    def generate_response(self, query: str, context: Dict[str, Any], 
                         is_contextual: bool = True, 
                         industry: Optional[Industry] = None) -> str:
        """Generate AI response with comprehensive error handling and fallback."""
        if not self.use_ai or not self.orchestrator:
            return self._generate_fallback_response(query, context, is_contextual)
        
        try:
            # Generate appropriate prompt using prompt service
            if is_contextual:
                prompt = self.prompt_service.generate_contextual_prompt(query, context, industry)
            else:
                prompt = self.prompt_service.generate_generic_prompt(query, industry)
            
            # Generate system message
            system_message = self.prompt_service.generate_system_message(industry)
            
            # Validate prompt
            validation_issues = self.prompt_service.validate_prompt(prompt)
            if validation_issues:
                logger.warning(f"Prompt validation issues: {validation_issues}")
            
            # Create request with settings from configuration
            request = PromptRequest(
                prompt=prompt,
                system_message=system_message,
                temperature=self.settings.ai_temperature,
                max_tokens=self.settings.ai_max_tokens,
                context={'industry': industry.value if industry else 'general'}
            )
            
            # Generate response using orchestrator
            with st.spinner("🤖 AI is thinking..."):
                response = self.orchestrator.generate_response(request, self.provider)
            
            if response.success:
                return response.content
            else:
                # Use error handler for user-friendly error messages
                error_msg = ErrorHandler.handle_error(
                    Exception(response.error_message or "Unknown AI error"),
                    {'query': query, 'industry': industry.value if industry else 'general'}
                )
                st.error(f"AI Error: {error_msg}")
                return self._generate_fallback_response(query, context, is_contextual)
                
        except Exception as e:
            # Use error handler for comprehensive error handling
            error_msg = ErrorHandler.handle_error(e, {'query': query, 'industry': industry.value if industry else 'general'})
            st.error(f"Error generating AI response: {error_msg}")
            logger.error(f"AI response generation failed: {e}")
            return self._generate_fallback_response(query, context, is_contextual)
    
    def _generate_fallback_response(self, query: str, context: Dict[str, Any], 
                                  is_contextual: bool) -> str:
        """Generate fallback responses using error handler."""
        try:
            # Use error handler's fallback response system
            industry = context.get('industry', 'general') if context else 'general'
            return ErrorHandler.get_fallback_response(query, industry)
        except Exception:
            # Ultimate fallback
            if not is_contextual:
                return "This is a generic response. AI integration is currently unavailable, showing fallback content."
            else:
                context_keys = list(context.keys()) if context else []
                return f"This would be a contextual response using: {context_keys}. AI integration is currently unavailable, showing fallback content."

# Initialize enhanced AI generator with all services
ai_generator = AIResponseGenerator(services)

# Main Application UI
def main():
    """Main application entry point with full modular integration."""
    
    # Perform configuration validation on startup
    config_valid, validation_result = validate_configuration()
    
    # Setup page layout using settings
    PageLayout.setup_page_config(
        title=settings.app_title,
        icon=settings.app_icon,
        layout=settings.layout
    )
    
    # Show configuration issues if any
    if not config_valid:
        st.error("⚠️ Configuration Issues Detected")
        
        if validation_result.errors:
            st.error("**Errors:**")
            for error in validation_result.errors:
                st.error(f"• {error}")
        
        if validation_result.warnings:
            st.warning("**Warnings:**")
            for warning in validation_result.warnings:
                st.warning(f"• {warning}")
        
        st.info("""
        **To fix configuration issues:**
        1. Run `python validate_config.py --fix` to attempt automatic fixes
        2. Check that your `.env` file exists and contains valid API keys
        3. Ensure all required dependencies are installed: `pip install -r requirements.txt`
        4. Review the configuration guide in `docs/configuration.md`
        """)
        
        # Continue with limited functionality
        st.warning("⚠️ Running in limited mode due to configuration issues")
    
    # Render page header
    UIComponents.render_page_header(
        title=f"{settings.app_icon} {settings.app_title}",
        subtitle="**See how AI responses transform when context is applied across different industries**"
    )
    
    # Display service status
    if services['ai_enabled'] and services['ai_provider']:
        provider_name = services['ai_provider'].value.title()
        UIComponents.render_ai_status_indicator(True, provider_name)
    else:
        UIComponents.render_ai_status_indicator(False, "AI")
        
        # Show configuration help if no providers available
        if not services['available_providers']:
            st.info("""
            🔧 **Setup Required**: No AI providers are configured. 
            
            To enable AI responses, set one of these environment variables:
            - `OPENAI_API_KEY` for OpenAI
            - `ANTHROPIC_API_KEY` for Anthropic Claude
            - `GEMINI_API_KEY` for Google Gemini
            - `OPENROUTER_API_KEY` for OpenRouter
            
            Then restart the application.
            """)
    
    # Render metrics dashboard
    metrics_data = UIComponents.create_metrics_data(
        ai_enabled=services['ai_enabled'],
        industries_count=len(settings.industries)
    )
    UIComponents.render_metrics_dashboard(metrics_data)
    
    # Industry selection sidebar
    available_industries = DemoFactory.get_available_industries()
    selected_industry = UIComponents.render_industry_selector(available_industries)
    
    # Create and render demo
    try:
        demo = DemoFactory.create_demo(
            selected_industry, 
            ai_service=ai_generator,
            context_service=services['context_service']
        )
        
        if demo:
            demo.render()
        else:
            st.error(f"❌ Demo not available for {selected_industry}")
            st.info("Available demos: " + ", ".join(available_industries))
            
    except Exception as e:
        error_msg = ErrorHandler.handle_error(e, {'industry': selected_industry})
        st.error(f"❌ Error loading demo: {error_msg}")
        logger.error(f"Demo loading failed: {e}")
    
    # Render footer
    UIComponents.render_footer(services['ai_enabled'])
    
    # Debug information in sidebar
    render_debug_info()

def render_debug_info():
    """Render debug information in sidebar."""
    debug_info = {}
    
    # AI Provider information
    if services['ai_enabled'] and services['ai_provider']:
        provider = services['ai_provider']
        api_key_env_var = f"{provider.value.upper()}_API_KEY"
        debug_info.update({
            "AI Provider": f"{provider.value.title()} (Connected)",
            "Active Provider": provider.value,
            "API Key Set": "Yes" if os.getenv(api_key_env_var) else "No",
            "Available Providers": len(services['available_providers'])
        })
        
        # Add orchestrator stats if available
        if services['ai_orchestrator']:
            try:
                stats = services['ai_orchestrator'].get_provider_stats()
                if provider.value in stats:
                    provider_stats = stats[provider.value]
                    debug_info.update({
                        "Requests": provider_stats.get('requests', 0),
                        "Success Rate": f"{provider_stats.get('success_rate', 0):.1%}",
                        "Avg Response Time": f"{provider_stats.get('average_response_time', 0):.2f}s"
                    })
            except Exception as e:
                logger.debug(f"Could not get provider stats: {e}")
    else:
        # Fallback mode information
        default_provider = get_default_provider()
        if default_provider:
            api_key_env_var = f"{default_provider.value.upper()}_API_KEY"
            debug_info.update({
                "AI Provider": "Fallback Mode (Static responses)",
                "Configured Provider": default_provider.value,
                "API Key Set": "Yes" if os.getenv(api_key_env_var) else "No"
            })
        else:
            debug_info.update({
                "AI Provider": "No providers configured",
                "Available Providers": len(services['available_providers'])
            })
    
    # Application information
    debug_info.update({
        "App Version": "AI-Powered",
        "Caching Enabled": "Yes" if settings.enable_caching else "No",
        "Debug Mode": "Yes" if settings.debug else "No",
        "Industries": len(settings.industries)
    })
    
    UIComponents.render_debug_sidebar(debug_info)

# Run the main application
if __name__ == "__main__":
    main()
else:
    # When imported as module, still run main for Streamlit
    main()