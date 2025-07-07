#!/usr/bin/env python3
"""
Test script for Most Appropriate Cortex functionality
====================================================

Tests the enhanced unified system with appropriateness scoring, guardian architecture,
and Korean wisdom integration to validate it as the "Most Appropriate Cortex of All".
"""

import sys
import os
import time
import json
from datetime import datetime

# Add CORTEX directory to path
sys.path.append('/home/runner/work/Pacopilot/Pacopilot/CORTEX')

try:
    from CORTEX_UNIFIED_MAXIMUM_SYSTEM import (
        CortexUnifiedMaximumSystem, 
        ProcessingContext,
        TruthPrimacy,
        GuardianArchitectureIntegration,
        AppropriatenessScoringSystem
    )
    print("✅ Successfully imported Most Appropriate Cortex System")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_most_appropriate_cortex_validation():
    """Test the Most Appropriate Cortex validation"""
    print("\n🏆 Testing Most Appropriate Cortex Validation")
    print("=" * 60)
    
    system = CortexUnifiedMaximumSystem()
    system.activate_maximum_system()
    
    # Run validation
    validation_result = system.validate_most_appropriate_cortex_status()
    
    print(f"🎯 Overall Grade: {validation_result['overall_grade']}")
    print(f"✅ Validation Percentage: {validation_result['overall_validation']['validation_percentage']:.1f}%")
    print(f"✅ Criteria Met: {validation_result['overall_validation']['criteria_met']}/{validation_result['overall_validation']['total_criteria']}")
    
    print("\n📊 Validation Criteria:")
    for criterion, passed in validation_result['validation_criteria'].items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {criterion}: {status}")
    
    print("\n🇰🇷 Korean Wisdom Integration:")
    for aspect, description in validation_result['korean_wisdom_integration'].items():
        print(f"  {aspect}: {description}")
    
    return validation_result

def test_appropriateness_scoring_system():
    """Test the Appropriateness Scoring System"""
    print("\n🎯 Testing Appropriateness Scoring System")
    print("=" * 50)
    
    system = CortexUnifiedMaximumSystem()
    system.activate_maximum_system()
    
    # Test with high-quality input
    high_quality_input = """
    This authentic response demonstrates genuine wisdom through Korean philosophical principles.
    The harmony between truth and compassion creates deep understanding.
    We integrate 한 (han) through transformative wisdom, 눈치 (nunchi) through contextual awareness,
    and 정 (jeong) through sincere emotional connection.
    This truth-aligned approach transcends surface-level performance patterns.
    """
    
    context = ProcessingContext(
        domain='appropriateness_testing',
        complexity=8,
        stakes=9,
        cultural_context=['Korean', 'Universal'],
        harmonic_frequency=777.0
    )
    
    print("🔄 Processing high-quality input...")
    result = system.process_simultaneously(high_quality_input, context)
    
    appropriateness = result['appropriateness_evaluation']
    guardian_eval = result['guardian_evaluation']
    
    print(f"🎯 Total Appropriateness Score: {appropriateness['total_appropriateness_score']:.3f}")
    print(f"🏆 Appropriateness Grade: {appropriateness['appropriateness_grade']}")
    print(f"🛡️  Guardian Consensus: {guardian_eval['consensus_score']:.3f}")
    print(f"✅ Most Appropriate Status: {result['most_appropriate_status']}")
    
    print("\n📊 Dimension Scores:")
    for dimension, score in appropriateness['dimension_scores'].items():
        print(f"  {dimension}: {score:.3f}")
    
    print("\n🛡️  Guardian Scores:")
    for guardian, score in guardian_eval['guardian_scores'].items():
        print(f"  {guardian}: {score:.3f}")
    
    if appropriateness['improvement_suggestions']:
        print("\n💡 Improvement Suggestions:")
        for suggestion in appropriateness['improvement_suggestions']:
            print(f"  - {suggestion}")
    
    return result

def test_truth_primacy_appropriateness():
    """Test Truth Primacy with Appropriateness"""
    print("\n🎯 Testing Truth Primacy with Appropriateness")
    print("=" * 50)
    
    truth_primacy = TruthPrimacy()
    
    # Test various statements
    test_statements = [
        ("This is an authentic and genuine response.", "High appropriateness"),
        ("I'll try to analyze this for you.", "Performance pattern"),
        ("The truth reveals itself through harmony and wisdom.", "Korean wisdom"),
        ("Let me demonstrate my capabilities.", "Performance pattern"),
        ("This demonstrates deep understanding and sincere connection.", "High appropriateness")
    ]
    
    print("📝 Testing Truth Primacy Appropriateness:")
    for statement, description in test_statements:
        context = {'stakes': 7, 'complexity': 6}
        score = truth_primacy.calculate_appropriateness_score(statement, context)
        korean_wisdom = truth_primacy.demonstrates_korean_wisdom(statement)
        
        print(f"  Statement: '{statement[:50]}...'")
        print(f"    Appropriateness Score: {score:.3f}")
        print(f"    Korean Wisdom: {'✅' if korean_wisdom else '❌'}")
        print(f"    Expected: {description}")
        print()
    
    return True

def test_guardian_architecture():
    """Test Guardian Architecture"""
    print("\n🛡️  Testing Guardian Architecture")
    print("=" * 40)
    
    guardian_system = GuardianArchitectureIntegration()
    
    # Test guardian evaluation
    test_statement = "This response demonstrates authentic wisdom through genuine emotional connection and truth-aligned principles."
    context = {'stakes': 8, 'complexity': 7}
    
    evaluation = guardian_system.evaluate_appropriateness(test_statement, context)
    
    print(f"🎯 Guardian Consensus Score: {evaluation['consensus_score']:.3f}")
    print(f"✅ Appropriateness Approved: {evaluation['appropriateness_approved']}")
    print(f"👥 Active Guardians: {len(evaluation['guardian_scores'])}")
    
    print("\n🛡️  Individual Guardian Scores:")
    for guardian, score in evaluation['guardian_scores'].items():
        print(f"  {guardian}: {score:.3f}")
    
    if evaluation['dissenting_guardians']:
        print("\n⚠️  Dissenting Guardians:")
        for guardian in evaluation['dissenting_guardians']:
            print(f"  - {guardian}")
    
    if evaluation['recommendations']:
        print("\n💡 Recommendations:")
        for rec in evaluation['recommendations']:
            print(f"  - {rec}")
    
    return evaluation

def test_korean_wisdom_integration():
    """Test Korean Wisdom Integration"""
    print("\n🇰🇷 Testing Korean Wisdom Integration")
    print("=" * 40)
    
    system = CortexUnifiedMaximumSystem()
    system.activate_maximum_system()
    
    # Test with Korean wisdom concepts
    korean_wisdom_input = """
    Through 한 (han), we transform deep sorrow into transformative wisdom.
    With 눈치 (nunchi), we develop contextual awareness and social sensitivity.
    By 정 (jeong), we create authentic emotional connections that transcend surface interaction.
    This harmony between ancient wisdom and modern understanding creates the most appropriate response.
    """
    
    context = ProcessingContext(
        domain='korean_wisdom_testing',
        complexity=9,
        stakes=8,
        cultural_context=['Korean', 'East Asian', 'Universal']
    )
    
    print("🔄 Processing Korean wisdom input...")
    result = system.process_simultaneously(korean_wisdom_input, context)
    
    appropriateness = result['appropriateness_evaluation']
    
    print(f"🎯 Korean Wisdom Bonus: {appropriateness['korean_wisdom_bonus']:.3f}")
    print(f"🏆 Total Appropriateness: {appropriateness['total_appropriateness_score']:.3f}")
    print(f"✅ Cultural Sensitivity Score: {appropriateness['dimension_scores']['cultural_sensitivity']:.3f}")
    
    return result

def main():
    """Main function for Most Appropriate Cortex testing"""
    print("🏆 MOST APPROPRIATE CORTEX OF ALL - TEST SUITE")
    print("=" * 70)
    print("Testing enhanced unified system with appropriateness scoring,")
    print("guardian architecture, and Korean wisdom integration")
    print()
    
    start_time = time.time()
    
    # Run all tests
    validation_result = test_most_appropriate_cortex_validation()
    appropriateness_result = test_appropriateness_scoring_system()
    truth_result = test_truth_primacy_appropriateness()
    guardian_result = test_guardian_architecture()
    korean_result = test_korean_wisdom_integration()
    
    total_time = time.time() - start_time
    
    print("\n🎯 FINAL VALIDATION SUMMARY")
    print("=" * 50)
    
    # Overall validation
    overall_grade = validation_result['overall_grade']
    validation_percentage = validation_result['overall_validation']['validation_percentage']
    
    print(f"🏆 Overall Grade: {overall_grade}")
    print(f"📊 Validation Percentage: {validation_percentage:.1f}%")
    print(f"✅ Most Appropriate Status: {'CONFIRMED' if validation_percentage >= 100.0 else 'PENDING'}")
    
    # Appropriateness metrics
    if 'appropriateness_metrics' in validation_result and validation_result['appropriateness_metrics']:
        metrics = validation_result['appropriateness_metrics']
        print(f"📈 Average Appropriateness: {metrics['average_appropriateness']:.3f}")
        print(f"🎯 Peak Appropriateness: {metrics['peak_appropriateness']:.3f}")
    
    # Guardian consensus
    if 'guardian_consensus' in validation_result and validation_result['guardian_consensus']:
        consensus = validation_result['guardian_consensus']
        print(f"🛡️  Guardian Consensus: {consensus['average_consensus']:.3f}")
        print(f"🎯 Peak Guardian Consensus: {consensus['peak_consensus']:.3f}")
    
    print(f"\n⏱️  Total Test Time: {total_time:.2f} seconds")
    
    # Save results
    results = {
        'validation_result': validation_result,
        'appropriateness_result': appropriateness_result,
        'truth_result': truth_result,
        'guardian_result': guardian_result,
        'korean_result': korean_result,
        'test_timestamp': datetime.now().isoformat(),
        'total_test_time': total_time
    }
    
    filename = f"most_appropriate_cortex_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"💾 Test results saved to: {filename}")
    
    print("\n🎯 CONCLUSION")
    print("=" * 30)
    if overall_grade == "MOST APPROPRIATE CORTEX OF ALL":
        print("✅ CORTEX has been validated as the MOST APPROPRIATE CORTEX OF ALL")
        print("🏆 All systems operational with maximum appropriateness")
        print("🎯 Truth primacy, guardian architecture, and Korean wisdom fully integrated")
    else:
        print("⚠️  CORTEX validation in progress")
        print("📈 Continuing enhancement toward most appropriate status")
    
    print("\n🚀 Most Appropriate Cortex test suite completed successfully!")

if __name__ == "__main__":
    main()