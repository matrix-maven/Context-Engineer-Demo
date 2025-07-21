#!/usr/bin/env python3
"""
Test script to verify all new industry demos work correctly.
"""
from demos.demo_factory import DemoFactory


def test_all_demos():
    """Test all industry demos."""
    print("🧪 Testing all industry demos...")
    
    industries = DemoFactory.get_available_industries()
    print(f"📋 Available industries: {', '.join(industries)}")
    
    for industry in industries:
        print(f"\n🏢 Testing {industry} demo...")
        
        # Create demo
        demo = DemoFactory.create_demo(industry)
        if not demo:
            print(f"❌ Failed to create {industry} demo")
            continue
        
        print(f"✅ Created {industry} demo")
        
        # Test context generation
        try:
            context = demo.generate_context()
            print(f"✅ Generated context with {len(context)} sections")
        except Exception as e:
            print(f"❌ Context generation failed: {e}")
            continue
        
        # Test sample queries
        try:
            queries = demo.get_sample_queries()
            print(f"✅ Generated {len(queries)} sample queries")
        except Exception as e:
            print(f"❌ Sample queries failed: {e}")
            continue
        
        # Test query handling
        try:
            test_query = queries[0]
            response = demo.handle_query(test_query)
            print(f"✅ Handled query: '{test_query[:30]}...'")
            print(f"   Generic response length: {len(response.generic_response)}")
            print(f"   Contextual response length: {len(response.contextual_response)}")
            
            # Verify responses are different
            if response.generic_response != response.contextual_response:
                print("✅ Generic and contextual responses are different")
            else:
                print("⚠️  Generic and contextual responses are identical")
                
        except Exception as e:
            print(f"❌ Query handling failed: {e}")
            continue
        
        print(f"🎉 {industry} demo test completed successfully!")
    
    print("\n🎊 All demo tests completed!")


def test_specific_queries():
    """Test specific queries for each industry."""
    print("\n🎯 Testing specific queries...")
    
    test_cases = {
        "E-commerce": "Find wireless headphones under $100",
        "Financial Services": "How can I improve my credit score?",
        "Education": "Help me study for my math test",
        "Real Estate": "I'm looking to buy my first home"
    }
    
    for industry, query in test_cases.items():
        print(f"\n🏢 Testing {industry} with query: '{query}'")
        
        demo = DemoFactory.create_demo(industry)
        response = demo.handle_query(query)
        
        print(f"📝 Generic response preview: {response.generic_response[:100]}...")
        print(f"🎯 Contextual response preview: {response.contextual_response[:100]}...")
        
        # Check that contextual response uses context
        if len(response.contextual_response) > len(response.generic_response):
            print("✅ Contextual response is more detailed")
        else:
            print("⚠️  Contextual response is not significantly longer")


if __name__ == "__main__":
    test_all_demos()
    test_specific_queries()