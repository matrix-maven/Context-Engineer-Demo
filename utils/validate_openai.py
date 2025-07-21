#!/usr/bin/env python3
"""
Validation script for OpenAI provider implementation.
This script tests the OpenAI provider with a real API call if an API key is available.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.openai_provider import OpenAIProvider, OPENAI_AVAILABLE
from services.ai_service import PromptRequest
from config.ai_config import AIConfig, load_ai_config
from config.settings import AIProvider


def test_openai_provider():
    """Test OpenAI provider with real API call if possible."""
    print("🔍 Testing OpenAI Provider Implementation")
    print("=" * 50)
    
    # Check if OpenAI library is available
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI library not available. Install with: pip install openai>=1.0.0")
        return False
    
    print("✅ OpenAI library is available")
    
    # Try to load configuration from environment
    config = load_ai_config(AIProvider.OPENAI)
    
    if not config:
        print("⚠️  No OpenAI API key found in environment variables")
        print("   Set OPENAI_API_KEY to test with real API calls")
        
        # Create a test configuration for validation
        try:
            config = AIConfig(
                provider=AIProvider.OPENAI,
                api_key="test-key-for-validation",
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
            print("✅ Configuration validation passed")
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    else:
        print(f"✅ OpenAI configuration loaded: model={config.model}")
    
    # Test provider initialization
    try:
        provider = OpenAIProvider(config)
        print("✅ OpenAI provider initialized successfully")
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
    if os.getenv('OPENAI_API_KEY'):
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
        if os.getenv('OPENAI_API_KEY'):
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
    
    print("\n🎉 All OpenAI provider tests passed!")
    return True


def main():
    """Main function."""
    success = test_openai_provider()
    
    if success:
        print("\n✅ OpenAI provider implementation is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ OpenAI provider implementation has issues!")
        sys.exit(1)


if __name__ == "__main__":
    main()