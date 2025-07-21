#!/usr/bin/env python3
"""
Validation script for Anthropic provider implementation.
This script tests the Anthropic provider with a real API call if an API key is available.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.anthropic_provider import AnthropicProvider, ANTHROPIC_AVAILABLE
from services.ai_service import PromptRequest
from config.ai_config import AIConfig, load_ai_config
from config.settings import AIProvider


def test_anthropic_provider():
    """Test Anthropic provider with real API call if possible."""
    print("🔍 Testing Anthropic Provider Implementation")
    print("=" * 50)
    
    # Check if Anthropic library is available
    if not ANTHROPIC_AVAILABLE:
        print("❌ Anthropic library not available. Install with: pip install anthropic>=0.7.0")
        return False
    
    print("✅ Anthropic library is available")
    
    # Try to load configuration from environment
    config = load_ai_config(AIProvider.ANTHROPIC)
    
    if not config:
        print("⚠️  No Anthropic API key found in environment variables")
        print("   Set ANTHROPIC_API_KEY to test with real API calls")
        
        # Create a test configuration for validation
        try:
            config = AIConfig(
                provider=AIProvider.ANTHROPIC,
                api_key="test-key-for-validation",
                model="claude-3-haiku-20240307",
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
            print("✅ Configuration validation passed")
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    else:
        print(f"✅ Anthropic configuration loaded: model={config.model}")
    
    # Test provider initialization
    try:
        provider = AnthropicProvider(config)
        print("✅ Anthropic provider initialized successfully")
    except Exception as e:
        print(f"❌ Provider initialization failed: {e}")
        return False
    
    # Test model info
    try:
        model_info = provider.get_model_info()
        print(f"✅ Model info retrieved: {model_info['model_type']} model")
        print(f"   - Supports system messages: {model_info['supports_system_messages']}")
        print(f"   - Supports context: {model_info['supports_context']}")
    except Exception as e:
        print(f"❌ Model info retrieval failed: {e}")
        return False
    
    # Test with real API call if API key is available
    if os.getenv('ANTHROPIC_API_KEY'):
        print("\n🌐 Testing with real API call...")
        
        try:
            # Create a simple test request
            request = PromptRequest(
                prompt="Say 'Hello, World!' in exactly those words.",
                temperature=0.1,
                max_tokens=10
            )
            
            response = provider.generate_response(request)
            
            if response.success:
                print("✅ Real API call successful!")
                print(f"   Response: {response.content}")
                print(f"   Tokens used: {response.tokens_used}")
                print(f"   Response time: {response.response_time:.2f}s")
            else:
                print(f"❌ API call failed: {response.error_message}")
                return False
                
        except Exception as e:
            print(f"❌ API call exception: {e}")
            return False
    else:
        print("\n⚠️  Skipping real API call (no API key)")
    
    # Test connection validation
    try:
        if os.getenv('ANTHROPIC_API_KEY'):
            is_valid = provider.validate_connection()
            if is_valid:
                print("✅ Connection validation passed")
            else:
                print("❌ Connection validation failed")
                return False
        else:
            print("⚠️  Skipping connection validation (no API key)")
    except Exception as e:
        print(f"❌ Connection validation exception: {e}")
        return False
    
    print("\n🎉 All Anthropic provider tests passed!")
    return True


def main():
    """Main function."""
    success = test_anthropic_provider()
    
    if success:
        print("\n✅ Anthropic provider implementation is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Anthropic provider implementation has issues!")
        sys.exit(1)


if __name__ == "__main__":
    main()