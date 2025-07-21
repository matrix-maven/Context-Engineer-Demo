#!/usr/bin/env python3
"""
Validation script for main.py integration
Tests all modular components work together correctly
"""
import os
import sys
from typing import Dict, Any

def test_configuration_loading():
    """Test configuration loading and validation."""
    print("🔧 Testing configuration loading...")
    
    try:
        from config.settings import get_settings, AppSettings
        from config.ai_config import get_available_providers, get_default_provider
        
        # Test settings loading
        settings = get_settings()
        assert settings.app_title, "App title should be set"
        assert settings.industries, "Industries list should not be empty"
        print(f"✅ Settings loaded: {settings.app_title}")
        
        # Test AI provider configuration
        available_providers = get_available_providers()
        print(f"✅ Available AI providers: {len(available_providers)}")
        
        default_provider = get_default_provider()
        if default_provider:
            print(f"✅ Default provider: {default_provider.value}")
        else:
            print("ℹ️  No default provider available (no API keys set)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_service_initialization():
    """Test service initialization."""
    print("\n🔧 Testing service initialization...")
    
    try:
        from services.ai_orchestrator import AIServiceOrchestrator
        from services.context_service import ContextService
        from services.prompt_service import get_prompt_service
        
        # Test context service
        context_service = ContextService()
        print("✅ Context service initialized")
        
        # Test prompt service
        prompt_service = get_prompt_service()
        templates = prompt_service.list_templates()
        print(f"✅ Prompt service initialized with {len(templates)} templates")
        
        # Test AI orchestrator (may not have providers)
        orchestrator = AIServiceOrchestrator()
        available_providers = orchestrator.get_available_providers()
        print(f"✅ AI orchestrator initialized with {len(available_providers)} providers")
        
        return True
        
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False

def test_demo_factory():
    """Test demo factory functionality."""
    print("\n🔧 Testing demo factory...")
    
    try:
        from demos.demo_factory import DemoFactory
        
        # Test available industries
        industries = DemoFactory.get_available_industries()
        assert len(industries) > 0, "Should have available industries"
        print(f"✅ Available industries: {industries}")
        
        # Test demo creation (without AI service for now)
        for industry in industries[:2]:  # Test first 2 industries
            demo = DemoFactory.create_demo(industry)
            assert demo is not None, f"Demo should be created for {industry}"
            print(f"✅ Demo created for {industry}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo factory test failed: {e}")
        return False

def test_ui_components():
    """Test UI components."""
    print("\n🔧 Testing UI components...")
    
    try:
        from ui.components import UIComponents, MetricsData
        from ui.layout import PageLayout
        
        # Test metrics data creation
        metrics = UIComponents.create_metrics_data(ai_enabled=False, industries_count=6)
        assert isinstance(metrics, MetricsData), "Should create MetricsData object"
        print("✅ UI components working")
        
        # Test page layout utilities
        # Note: Can't test Streamlit components without Streamlit context
        print("✅ Page layout utilities available")
        
        return True
        
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False

def test_error_handling():
    """Test error handling utilities."""
    print("\n🔧 Testing error handling...")
    
    try:
        from utils.error_handler import ErrorHandler
        from utils.logger import setup_logging
        
        # Test logger setup
        setup_logging()
        print("✅ Logging setup successful")
        
        # Test error handler
        fallback_response = ErrorHandler.get_fallback_response("test query", "restaurant")
        assert fallback_response, "Should get fallback response"
        print("✅ Error handler working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_ai_integration():
    """Test AI integration (if API keys available)."""
    print("\n🔧 Testing AI integration...")
    
    try:
        from services.ai_orchestrator import AIServiceOrchestrator
        from services.ai_service import PromptRequest
        from services.prompt_service import get_prompt_service, Industry
        
        # Initialize orchestrator
        orchestrator = AIServiceOrchestrator()
        available_providers = orchestrator.get_available_providers()
        
        if not available_providers:
            print("ℹ️  No AI providers available (no API keys set)")
            return True
        
        # Test prompt generation
        prompt_service = get_prompt_service()
        generic_prompt = prompt_service.generate_generic_prompt("test query", Industry.RESTAURANT)
        assert generic_prompt, "Should generate generic prompt"
        print("✅ Prompt generation working")
        
        # Test request creation
        request = PromptRequest(
            prompt=generic_prompt,
            system_message="Test system message",
            temperature=0.7,
            max_tokens=100
        )
        print("✅ AI request creation working")
        
        print(f"✅ AI integration ready with {len(available_providers)} providers")
        return True
        
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🧠 Context Engineering Demo - Main.py Integration Validation")
    print("=" * 60)
    
    tests = [
        test_configuration_loading,
        test_service_initialization,
        test_demo_factory,
        test_ui_components,
        test_error_handling,
        test_ai_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Main.py integration is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())