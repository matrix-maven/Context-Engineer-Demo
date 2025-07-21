#!/usr/bin/env python3
"""
Configuration validation script for Context Engineering Demo.

This script validates the application configuration and environment setup
before starting the application. It can be run standalone or imported.

Usage:
    python validate_config.py              # Run validation checks
    python validate_config.py --verbose    # Run with detailed output
    python validate_config.py --fix        # Attempt to fix common issues
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.validation import validate_and_setup, print_validation_results


def create_missing_directories():
    """Create missing directories that are required for the application."""
    required_dirs = [
        'logs',
        'config',
        'services', 
        'demos',
        'ui',
        'utils',
        'tests'
    ]
    
    created_dirs = []
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_name)
            except Exception as e:
                print(f"❌ Failed to create directory {dir_name}: {e}")
    
    if created_dirs:
        print(f"✅ Created missing directories: {', '.join(created_dirs)}")
    
    return created_dirs


def create_env_file_if_missing():
    """Create .env file from template if it doesn't exist."""
    env_file = Path('.env')
    template_file = Path('.env.template')
    
    if not env_file.exists() and template_file.exists():
        try:
            # Copy template to .env
            with open(template_file, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    
    return False


def fix_common_issues():
    """Attempt to fix common configuration issues."""
    print("🔧 Attempting to fix common configuration issues...\n")
    
    fixes_applied = []
    
    # Create missing directories
    created_dirs = create_missing_directories()
    if created_dirs:
        fixes_applied.extend([f"Created directory: {d}" for d in created_dirs])
    
    # Create .env file from template
    if create_env_file_if_missing():
        fixes_applied.append("Created .env file from template")
    
    # Create __init__.py files in package directories
    package_dirs = ['config', 'services', 'demos', 'ui', 'utils', 'tests']
    for dir_name in package_dirs:
        init_file = Path(dir_name) / '__init__.py'
        if Path(dir_name).exists() and not init_file.exists():
            try:
                init_file.touch()
                fixes_applied.append(f"Created {init_file}")
            except Exception as e:
                print(f"❌ Failed to create {init_file}: {e}")
    
    if fixes_applied:
        print("✅ Applied fixes:")
        for fix in fixes_applied:
            print(f"   • {fix}")
    else:
        print("ℹ️  No automatic fixes were needed or possible")
    
    print()


def main():
    """Main validation script."""
    parser = argparse.ArgumentParser(
        description="Validate Context Engineering Demo configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_config.py                 # Basic validation
    python validate_config.py --verbose       # Detailed output
    python validate_config.py --fix           # Fix common issues first
    python validate_config.py --fix --verbose # Fix and validate with details
        """
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation information'
    )
    
    parser.add_argument(
        '--fix', '-f',
        action='store_true',
        help='Attempt to fix common configuration issues'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only show errors and warnings'
    )
    
    args = parser.parse_args()
    
    print("🧠 Context Engineering Demo - Configuration Validator")
    print("=" * 60)
    
    # Apply fixes if requested
    if args.fix:
        fix_common_issues()
    
    # Run validation
    print("🔍 Running configuration validation...\n")
    
    try:
        success, validation_result = validate_and_setup()
        
        # Print results
        if args.quiet:
            # Only show errors and warnings in quiet mode
            if validation_result.errors:
                print("❌ ERRORS:")
                for error in validation_result.errors:
                    print(f"   • {error}")
            
            if validation_result.warnings:
                print("⚠️  WARNINGS:")
                for warning in validation_result.warnings:
                    print(f"   • {warning}")
        else:
            print_validation_results(validation_result, verbose=args.verbose)
        
        # Exit with appropriate code
        if success:
            print("🎉 Configuration validation passed! The application is ready to run.")
            if not args.quiet:
                print("\nTo start the application:")
                print("   streamlit run main.py    # AI-powered version")
                print("   streamlit run app.py     # Static fallback version")
            sys.exit(0)
        else:
            print("❌ Configuration validation failed. Please fix the issues above.")
            if not args.quiet:
                print("\nCommon solutions:")
                print("   • Run with --fix to attempt automatic fixes")
                print("   • Check that .env file exists and contains valid API keys")
                print("   • Ensure all required dependencies are installed")
                print("   • Verify directory structure is complete")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Unexpected error during validation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()