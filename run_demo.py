#!/usr/bin/env python3
"""
Demo runner script for Context Engineering Demo
Allows easy switching between static and AI-powered versions
"""
import os
import sys
import subprocess
import argparse

def run_static_demo():
    """Run the static version (app.py)"""
    print("🔧 Starting Static Context Engineering Demo...")
    print("📝 Using hardcoded responses (safe fallback)")
    print("🌐 Open your browser to: http://localhost:8501")
    print("-" * 50)
    
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running static demo: {e}")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")

def run_ai_demo():
    """Run the AI-powered version (main.py)"""
    print("🤖 Starting AI-Powered Context Engineering Demo...")
    
    # Check for available API keys
    api_keys_found = []
    if os.getenv('OPENAI_API_KEY'):
        api_keys_found.append("OpenAI")
    if os.getenv('ANTHROPIC_API_KEY'):
        api_keys_found.append("Anthropic")
    if os.getenv('GEMINI_API_KEY'):
        api_keys_found.append("Gemini")
    if os.getenv('OPENROUTER_API_KEY'):
        api_keys_found.append("OpenRouter")
    
    if api_keys_found:
        print(f"✅ AI providers found: {', '.join(api_keys_found)} - Real AI responses enabled")
    else:
        print("⚠️  No AI provider API keys found - Will use fallback mode")
        print("   Set one of these environment variables for full AI experience:")
        print("   - OPENAI_API_KEY for OpenAI GPT models")
        print("   - ANTHROPIC_API_KEY for Claude models")
        print("   - GEMINI_API_KEY for Google Gemini")
        print("   - OPENROUTER_API_KEY for OpenRouter")
    
    print("🌐 Open your browser to: http://localhost:8501")
    print("-" * 50)
    
    try:
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running AI demo: {e}")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description="Context Engineering Demo Runner")
    parser.add_argument(
        "version", 
        choices=["static", "ai"], 
        help="Version to run: 'static' for safe fallback, 'ai' for AI-powered"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501, 
        help="Port to run on (default: 8501)"
    )
    
    args = parser.parse_args()
    
    # Set port if specified
    if args.port != 8501:
        os.environ['STREAMLIT_SERVER_PORT'] = str(args.port)
    
    print("🧠 Context Engineering Demo Runner")
    print("=" * 40)
    
    if args.version == "static":
        run_static_demo()
    elif args.version == "ai":
        run_ai_demo()

if __name__ == "__main__":
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print("🧠 Context Engineering Demo Runner")
        print("=" * 40)
        print()
        print("Available versions:")
        print("  📝 static  - Safe fallback with hardcoded responses")
        print("  🤖 ai     - AI-powered with real AI provider integration")
        print()
        print("Usage:")
        print("  python run_demo.py static    # Run static version")
        print("  python run_demo.py ai        # Run AI-powered version")
        print()
        print("For AI version, set one of these API key environment variables:")
        print("  export OPENAI_API_KEY='your-openai-key'")
        print("  export ANTHROPIC_API_KEY='your-anthropic-key'")
        print("  export GEMINI_API_KEY='your-gemini-key'")
        print("  export OPENROUTER_API_KEY='your-openrouter-key'")
        print()
        print("Multiple providers can be configured - the app will use the best available.")
        sys.exit(0)
    
    main()