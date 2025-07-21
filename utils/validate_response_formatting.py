#!/usr/bin/env python3
"""
Validation script for Response Format Guidelines enhancement.
This script tests the new response format guidelines in all industry prompt templates.
"""
import os
import sys
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.prompt_service import get_prompt_service, Industry, PromptType
from config.settings import get_settings


def test_response_format_guidelines():
    """Test that all industry templates have proper response format guidelines."""
    print("🔍 Testing Response Format Guidelines Enhancement")
    print("=" * 60)
    
    prompt_service = get_prompt_service()
    
    # Test all industries
    industries = [
        Industry.RESTAURANT,
        Industry.HEALTHCARE,
        Industry.ECOMMERCE,
        Industry.FINANCIAL,
        Industry.EDUCATION,
        Industry.REAL_ESTATE
    ]
    
    results = {
        'total_templates': 0,
        'templates_with_guidelines': 0,
        'templates_without_guidelines': 0,
        'issues': []
    }
    
    print("📋 Checking Response Format Guidelines in Templates:")
    print("-" * 60)
    
    for industry in industries:
        print(f"\n🏢 {industry.value.upper()} INDUSTRY:")
        
        # Test generic template
        generic_template = prompt_service.get_template(f"generic_{industry.value}")
        if generic_template:
            results['total_templates'] += 1
            
            # Check for formatting guidelines
            has_guidelines = "RESPONSE FORMAT GUIDELINES:" in generic_template.template
            has_structure = "Structure your response" in generic_template.template or "Organize" in generic_template.template
            has_cta = "call-to-action" in generic_template.template.lower() or "would you like" in generic_template.template.lower()
            
            if has_guidelines:
                results['templates_with_guidelines'] += 1
                print(f"   ✅ Generic template has response format guidelines")
                
                # Show a snippet of the formatting guidelines
                guidelines_start = generic_template.template.find("RESPONSE FORMAT GUIDELINES:")
                guidelines_snippet = generic_template.template[guidelines_start:guidelines_start + 200] + "..."
                print(f"   📝 Guidelines Preview: {guidelines_snippet}")
                
            else:
                results['templates_without_guidelines'] += 1
                results['issues'].append(f"{industry.value} generic template missing response format guidelines")
                print(f"   ❌ Generic template missing response format guidelines")
        
        # Test contextual template
        contextual_template = prompt_service.get_template(f"contextual_{industry.value}")
        if contextual_template:
            results['total_templates'] += 1
            
            # Check for formatting and personalization
            has_guidelines = "RESPONSE FORMAT GUIDELINES:" in contextual_template.template
            has_personalization = "personalized" in contextual_template.template.lower()
            has_context_ref = "profile" in contextual_template.template.lower() or "context" in contextual_template.template.lower()
            
            if has_guidelines:
                results['templates_with_guidelines'] += 1
                print(f"   ✅ Contextual template has response format guidelines")
                
                if has_personalization and has_context_ref:
                    print(f"   ✅ Contextual template includes personalization instructions")
                else:
                    results['issues'].append(f"{industry.value} contextual template lacks personalization guidance")
                    print(f"   ⚠️  Contextual template could use better personalization guidance")
            else:
                results['templates_without_guidelines'] += 1
                results['issues'].append(f"{industry.value} contextual template missing response format guidelines")
                print(f"   ❌ Contextual template missing response format guidelines")
    
    return results


def test_template_structure_consistency():
    """Test that all templates follow the enhanced structure."""
    print("\n🏗️ Testing Template Structure Consistency")
    print("-" * 60)
    
    prompt_service = get_prompt_service()
    industries = [Industry.RESTAURANT, Industry.HEALTHCARE, Industry.ECOMMERCE, 
                 Industry.FINANCIAL, Industry.EDUCATION, Industry.REAL_ESTATE]
    
    structure_results = {
        'templates_checked': 0,
        'well_structured': 0,
        'structure_issues': []
    }
    
    expected_elements = [
        "RESPONSE FORMAT GUIDELINES:",
        "Start with",
        "Structure your response" or "Organize",
        "End with",
        "call-to-action"
    ]
    
    for industry in industries:
        for template_type in ['generic', 'contextual']:
            template = prompt_service.get_template(f"{template_type}_{industry.value}")
            if template:
                structure_results['templates_checked'] += 1
                
                # Check for key structural elements
                template_text = template.template.lower()
                missing_elements = []
                
                if "response format guidelines:" not in template_text:
                    missing_elements.append("Response Format Guidelines section")
                
                if "start with" not in template_text:
                    missing_elements.append("Opening instruction")
                
                if not ("structure your response" in template_text or "organize" in template_text):
                    missing_elements.append("Structure guidance")
                
                if "end with" not in template_text:
                    missing_elements.append("Closing instruction")
                
                if "call-to-action" not in template_text:
                    missing_elements.append("Call-to-action guidance")
                
                if not missing_elements:
                    structure_results['well_structured'] += 1
                    print(f"   ✅ {industry.value} {template_type} template is well-structured")
                else:
                    structure_results['structure_issues'].append({
                        'template': f"{industry.value} {template_type}",
                        'missing': missing_elements
                    })
                    print(f"   ⚠️  {industry.value} {template_type} template missing: {', '.join(missing_elements)}")
    
    return structure_results


def test_industry_specific_formatting():
    """Test that each industry has appropriate formatting guidelines."""
    print("\n🎯 Testing Industry-Specific Formatting Guidelines")
    print("-" * 60)
    
    prompt_service = get_prompt_service()
    
    # Industry-specific expectations
    industry_expectations = {
        Industry.RESTAURANT: ["restaurant recommendations", "cuisine", "atmosphere", "reservation"],
        Industry.HEALTHCARE: ["health", "medical", "healthcare provider", "educational purposes"],
        Industry.ECOMMERCE: ["product recommendations", "shopping", "purchase", "products"],
        Industry.FINANCIAL: ["financial", "investment", "professional", "educational purposes"],
        Industry.EDUCATION: ["learning", "academic", "educational", "study"],
        Industry.REAL_ESTATE: ["property", "real estate", "market", "recommendations"]
    }
    
    formatting_results = {
        'industries_checked': 0,
        'appropriate_formatting': 0,
        'formatting_issues': []
    }
    
    for industry, expected_terms in industry_expectations.items():
        formatting_results['industries_checked'] += 1
        
        generic_template = prompt_service.get_template(f"generic_{industry.value}")
        if generic_template:
            template_text = generic_template.template.lower()
            
            # Check for industry-specific terms in formatting guidelines
            guidelines_section = ""
            if "response format guidelines:" in template_text:
                guidelines_start = template_text.find("response format guidelines:")
                guidelines_section = template_text[guidelines_start:guidelines_start + 500]
            
            found_terms = [term for term in expected_terms if term in template_text]
            
            if len(found_terms) >= 2:  # At least 2 industry-specific terms
                formatting_results['appropriate_formatting'] += 1
                print(f"   ✅ {industry.value} has appropriate industry-specific formatting")
                print(f"      Found terms: {', '.join(found_terms)}")
            else:
                formatting_results['formatting_issues'].append({
                    'industry': industry.value,
                    'found_terms': found_terms,
                    'expected_terms': expected_terms
                })
                print(f"   ⚠️  {industry.value} could use more industry-specific formatting guidance")
                print(f"      Found: {found_terms}, Expected: {expected_terms}")
    
    return formatting_results


def test_call_to_action_quality():
    """Test the quality and variety of call-to-action instructions."""
    print("\n📞 Testing Call-to-Action Quality")
    print("-" * 60)
    
    prompt_service = get_prompt_service()
    industries = [Industry.RESTAURANT, Industry.HEALTHCARE, Industry.ECOMMERCE, 
                 Industry.FINANCIAL, Industry.EDUCATION, Industry.REAL_ESTATE]
    
    cta_results = {
        'templates_checked': 0,
        'good_ctas': 0,
        'cta_issues': []
    }
    
    # Good call-to-action patterns
    good_cta_patterns = [
        "would you like me to",
        "let me know if",
        "i can help you",
        "would you like more",
        "shall i",
        "do you need"
    ]
    
    for industry in industries:
        for template_type in ['generic', 'contextual']:
            template = prompt_service.get_template(f"{template_type}_{industry.value}")
            if template:
                cta_results['templates_checked'] += 1
                
                template_text = template.template.lower()
                
                # Look for call-to-action examples in the guidelines
                found_cta_patterns = [pattern for pattern in good_cta_patterns if pattern in template_text]
                
                if found_cta_patterns:
                    cta_results['good_ctas'] += 1
                    print(f"   ✅ {industry.value} {template_type} has good call-to-action examples")
                    print(f"      Patterns: {', '.join(found_cta_patterns)}")
                else:
                    cta_results['cta_issues'].append(f"{industry.value} {template_type}")
                    print(f"   ⚠️  {industry.value} {template_type} could use better call-to-action examples")
    
    return cta_results


def generate_summary_report(guidelines_results: Dict, structure_results: Dict, 
                          formatting_results: Dict, cta_results: Dict):
    """Generate a comprehensive summary report."""
    print("\n" + "=" * 60)
    print("📊 RESPONSE FORMAT GUIDELINES VALIDATION SUMMARY")
    print("=" * 60)
    
    # Overall statistics
    total_score = 0
    max_score = 0
    
    print(f"\n📋 Response Format Guidelines Coverage:")
    guidelines_coverage = (guidelines_results['templates_with_guidelines'] / 
                          guidelines_results['total_templates'] * 100) if guidelines_results['total_templates'] > 0 else 0
    print(f"   • Templates with guidelines: {guidelines_results['templates_with_guidelines']}/{guidelines_results['total_templates']} ({guidelines_coverage:.1f}%)")
    total_score += guidelines_results['templates_with_guidelines']
    max_score += guidelines_results['total_templates']
    
    print(f"\n🏗️ Template Structure Quality:")
    structure_coverage = (structure_results['well_structured'] / 
                         structure_results['templates_checked'] * 100) if structure_results['templates_checked'] > 0 else 0
    print(f"   • Well-structured templates: {structure_results['well_structured']}/{structure_results['templates_checked']} ({structure_coverage:.1f}%)")
    total_score += structure_results['well_structured']
    max_score += structure_results['templates_checked']
    
    print(f"\n🎯 Industry-Specific Formatting:")
    formatting_coverage = (formatting_results['appropriate_formatting'] / 
                          formatting_results['industries_checked'] * 100) if formatting_results['industries_checked'] > 0 else 0
    print(f"   • Industries with appropriate formatting: {formatting_results['appropriate_formatting']}/{formatting_results['industries_checked']} ({formatting_coverage:.1f}%)")
    total_score += formatting_results['appropriate_formatting']
    max_score += formatting_results['industries_checked']
    
    print(f"\n📞 Call-to-Action Quality:")
    cta_coverage = (cta_results['good_ctas'] / 
                   cta_results['templates_checked'] * 100) if cta_results['templates_checked'] > 0 else 0
    print(f"   • Templates with good CTAs: {cta_results['good_ctas']}/{cta_results['templates_checked']} ({cta_coverage:.1f}%)")
    total_score += cta_results['good_ctas']
    max_score += cta_results['templates_checked']
    
    # Overall score
    overall_score = (total_score / max_score * 100) if max_score > 0 else 0
    print(f"\n🎯 Overall Enhancement Score: {total_score}/{max_score} ({overall_score:.1f}%)")
    
    # Issues summary
    all_issues = (guidelines_results['issues'] + 
                 [f"Structure: {issue['template']} - {', '.join(issue['missing'])}" for issue in structure_results['structure_issues']] +
                 [f"Formatting: {issue['industry']} needs more specific terms" for issue in formatting_results['formatting_issues']] +
                 [f"CTA: {issue} needs better call-to-action examples" for issue in cta_results['cta_issues']])
    
    if all_issues:
        print(f"\n⚠️  Issues to Address ({len(all_issues)}):")
        for issue in all_issues[:10]:  # Show first 10 issues
            print(f"   • {issue}")
        if len(all_issues) > 10:
            print(f"   ... and {len(all_issues) - 10} more issues")
    else:
        print(f"\n✅ No issues found - all templates are properly enhanced!")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if overall_score >= 90:
        print("   🎉 Excellent! Response Format Guidelines are well implemented.")
    elif overall_score >= 75:
        print("   👍 Good implementation. Consider addressing the minor issues above.")
    elif overall_score >= 50:
        print("   ⚠️  Moderate implementation. Several templates need enhancement.")
    else:
        print("   ❌ Poor implementation. Most templates need response format guidelines.")
    
    return overall_score >= 75


def main():
    """Main validation function."""
    print("🧠 Context Engineering Demo - Response Format Guidelines Validator")
    print("=" * 70)
    
    try:
        # Run all validation tests
        guidelines_results = test_response_format_guidelines()
        structure_results = test_template_structure_consistency()
        formatting_results = test_industry_specific_formatting()
        cta_results = test_call_to_action_quality()
        
        # Generate summary report
        success = generate_summary_report(guidelines_results, structure_results, 
                                        formatting_results, cta_results)
        
        if success:
            print("\n🎉 Response Format Guidelines validation passed!")
            print("\nThe enhancement has been successfully implemented across all industry templates.")
            sys.exit(0)
        else:
            print("\n⚠️  Response Format Guidelines validation completed with issues.")
            print("Please review the issues above and enhance the templates as needed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error during validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()