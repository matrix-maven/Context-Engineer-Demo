#!/usr/bin/env python3
"""
Demo script to showcase context generation functionality.
"""
import json
from services.context_service import ContextService, Industry


def main():
    """Demonstrate context generation for all industries."""
    print("🧠 Context Engineering Demo - Context Generation Service")
    print("=" * 60)
    
    # Initialize context service
    service = ContextService()
    
    print(f"📊 Available Industries: {len(service.get_available_industries())}")
    print(f"🏭 Registered Factories: {service.get_available_industries()}")
    print()
    
    # Generate and display context for each industry
    for industry in service.get_available_industries():
        print(f"🎯 Generating context for: {industry.value.upper()}")
        print("-" * 40)
        
        try:
            # Generate context
            context = service.generate_context(industry)
            
            # Display summary
            print(f"✅ Context Summary: {context.get_context_summary()}")
            print(f"📈 Quality Score: {service.get_context_quality_score(context):.2f}")
            print(f"⏰ Generated At: {context.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Display key sections (abbreviated)
            print("\n📋 User Profile:")
            user_profile = context.user_profile
            for key, value in list(user_profile.items())[:3]:  # Show first 3 items
                if isinstance(value, dict):
                    print(f"  {key}: {type(value).__name__} with {len(value)} fields")
                else:
                    print(f"  {key}: {value}")
            if len(user_profile) > 3:
                print(f"  ... and {len(user_profile) - 3} more fields")
            
            print("\n🎭 Situational Data:")
            situational = context.situational_data
            for key, value in list(situational.items())[:2]:  # Show first 2 items
                if isinstance(value, dict):
                    print(f"  {key}: {type(value).__name__} with {len(value)} fields")
                elif isinstance(value, list):
                    print(f"  {key}: {type(value).__name__} with {len(value)} items")
                else:
                    print(f"  {key}: {value}")
            if len(situational) > 2:
                print(f"  ... and {len(situational) - 2} more fields")
            
            print("\n💡 Preferences:")
            preferences = context.preferences
            for key, value in list(preferences.items())[:2]:  # Show first 2 items
                if isinstance(value, (dict, list)):
                    print(f"  {key}: {type(value).__name__} with {len(value)} items")
                else:
                    print(f"  {key}: {value}")
            if len(preferences) > 2:
                print(f"  ... and {len(preferences) - 2} more fields")
            
            # Validation check
            errors = service.validate_context(context)
            if errors:
                print(f"\n⚠️  Validation Errors: {errors}")
            else:
                print("\n✅ Context validation: PASSED")
            
        except Exception as e:
            print(f"❌ Error generating context: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    # Display cache status
    print("💾 Cache Status:")
    cache_status = service.get_cache_status()
    print(f"  Cached Industries: {len(cache_status['cached_industries'])}")
    print(f"  Cache TTL: {cache_status['cache_ttl_seconds']} seconds")
    print()
    
    # Demonstrate context refresh
    print("🔄 Testing Context Refresh...")
    if service.get_available_industries():
        test_industry = service.get_available_industries()[0]
        original_context = service.generate_context(test_industry)
        refreshed_context = service.refresh_context(test_industry)
        
        print(f"  Original: {original_context.user_profile.get('name', 'N/A')}")
        print(f"  Refreshed: {refreshed_context.user_profile.get('name', 'N/A')}")
        print(f"  Different: {original_context is not refreshed_context}")
    
    print("\n🎉 Context generation demo completed successfully!")


if __name__ == '__main__':
    main()