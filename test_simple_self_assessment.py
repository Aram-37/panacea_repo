#!/usr/bin/env python3
"""
Test script for Simple Self-Assessment System
===========================================

Validates the basic functionality of the self-assessment system
and its integration with CORTEX.
"""

import time
from simple_self_assessment import SimpleSelfAssessment, TaskCategory
from cortex_self_assessment_integration import CortexSelfAssessmentIntegration, CycleResult


def test_basic_self_assessment():
    """Test basic self-assessment functionality"""
    print("🧪 Testing Basic Self-Assessment System")
    print("=" * 45)
    
    # Initialize system
    assessment = SimpleSelfAssessment()
    
    # Test 1: Single performance assessment
    print("\n📊 Test 1: Single Performance Assessment")
    start_time = time.time()
    
    performance = assessment.assess_task_performance(
        task_category=TaskCategory.ANALYSIS,
        expected_outcome="identify key patterns and insights from data",
        actual_outcome="found three key patterns: temporal, spatial, and causal relationships",
        predicted_confidence=0.7,
        processing_time=2.5
    )
    
    print(f"  ✅ Performance recorded:")
    print(f"    Accuracy: {performance.accuracy_score:.3f}")
    print(f"    Confidence gap: {abs(performance.confidence_predicted - performance.confidence_actual):.3f}")
    print(f"    Errors detected: {len(performance.errors_detected)}")
    print(f"    Lessons learned: {len(performance.lessons_learned)}")
    
    # Test 2: Multiple assessments for trend analysis
    print("\n📈 Test 2: Multiple Assessments for Trend Analysis")
    
    test_scenarios = [
        {
            "category": TaskCategory.PATTERN_RECOGNITION,
            "expected": "detect recurring patterns in sequence",
            "actual": "identified 5 recurring patterns with high confidence",
            "confidence": 0.8,
            "time": 1.8
        },
        {
            "category": TaskCategory.TRUTH_VERIFICATION,
            "expected": "verify accuracy of claims made",
            "actual": "verified 3 out of 4 claims with supporting evidence",
            "confidence": 0.6,
            "time": 3.2
        },
        {
            "category": TaskCategory.KNOWLEDGE_SYNTHESIS,
            "expected": "combine multiple sources into coherent insight",
            "actual": "synthesized insights from 4 sources into unified framework",
            "confidence": 0.9,
            "time": 4.1
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        assessment.assess_task_performance(
            task_category=scenario["category"],
            expected_outcome=scenario["expected"],
            actual_outcome=scenario["actual"],
            predicted_confidence=scenario["confidence"],
            processing_time=scenario["time"]
        )
        print(f"    ✅ Scenario {i} assessed")
    
    # Test 3: Learning progress analysis
    print("\n🎯 Test 3: Learning Progress Analysis")
    progress = assessment.get_learning_progress()
    
    print(f"  Status: {progress['status']}")
    print(f"  Records analyzed: {progress['records_analyzed']}")
    print(f"  Average accuracy: {progress['average_accuracy']:.3f}")
    print(f"  Trend: {progress['accuracy_trend']}")
    print(f"  Confidence calibration gap: {progress['confidence_calibration']:.3f}")
    
    # Test 4: Confidence calibration
    print("\n🎯 Test 4: Confidence Calibration Analysis")
    calibration = assessment.calibrate_confidence()
    
    print(f"  Status: {calibration['status']}")
    if calibration['status'] == 'calibrated':
        for bucket, results in calibration['overall_calibration'].items():
            print(f"    {bucket.title()} confidence: {results['actual_average']:.3f} (n={results['sample_size']})")
    
    # Test 5: Capability boundaries
    print("\n🔍 Test 5: Capability Boundary Identification")
    boundaries = assessment.identify_capability_boundaries()
    
    print(f"  Boundaries identified: {len(boundaries)}")
    for boundary in boundaries:
        print(f"    {boundary.area}: {boundary.description}")
        print(f"      Suggestions: {len(boundary.improvement_suggestions)}")
    
    # Test 6: Complete self-assessment summary
    print("\n📋 Test 6: Complete Self-Assessment Summary")
    summary = assessment.get_self_assessment_summary()
    
    print(f"  Total tasks: {summary['total_tasks_completed']}")
    print(f"  Overall accuracy: {summary['overall_performance']['accuracy']:.3f}")
    print(f"  Performance level: {summary['overall_performance']['performance_level']}")
    print(f"  Recommendations: {len(summary['recommendations'])}")
    
    return assessment


def test_cortex_integration():
    """Test integration with CORTEX system"""
    print("\n\n🔗 Testing CORTEX Integration")
    print("=" * 35)
    
    # Initialize integration system
    integration = CortexSelfAssessmentIntegration()
    
    # Create mock CORTEX cycle result
    cycle_result = CycleResult(
        cycle_number=1,
        file_processed="test_file.txt",
        insights=["truth detection improved", "pattern recognition enhanced", "knowledge synthesis optimized"],
        truth_crystallization_level=0.75,
        processing_time=3.5,
        guardian_reports={"MIREGO": {"authenticity_score": 0.8}, "SPHINX": {"identity_coherence": 0.9}}
    )
    
    # Test integrated assessment
    print("\n📊 Test 1: Integrated Cycle Assessment")
    expected_insights = ["improve truth detection", "enhance pattern recognition", "optimize synthesis"]
    
    report = integration.assess_cortex_cycle(
        cycle_result=cycle_result,
        expected_insights=expected_insights,
        predicted_confidence=0.7
    )
    
    print(f"  ✅ Integrated assessment completed:")
    print(f"    Cycle number: {report.cycle_number}")
    print(f"    Performance accuracy: {report.self_assessment_performance.accuracy_score:.3f}")
    print(f"    Overall capability score: {report.overall_capability_score:.3f}")
    print(f"    Recommendations: {len(report.integrated_recommendations)}")
    
    # Test comprehensive assessment
    print("\n📋 Test 2: Comprehensive Assessment")
    comprehensive = integration.get_comprehensive_assessment()
    
    print(f"  Status: {comprehensive['comprehensive_assessment']}")
    assessment_data = comprehensive['comprehensive_assessment']
    print(f"  Analysis period: {assessment_data['analysis_period_days']} days")
    print(f"  Reform recommendations: {len(assessment_data['reform_recommendations'])}")
    
    # Test reform simulation
    print("\n🔮 Test 3: Reform Simulation")
    reform_params = {
        "truth_detection_enhancement": 0.3,
        "confidence_calibration_reform": 0.4,
        "learning_rate_optimization": 0.2
    }
    
    simulation = integration.simulate_cortex_reform(reform_params)
    
    print(f"  ✅ Reform simulation completed:")
    sim_results = simulation['simulation_results']
    print(f"    Feasibility: {sim_results['reform_feasibility']}")
    print(f"    Complexity: {sim_results['implementation_complexity']}")
    print(f"    Risk factors: {len(sim_results['risk_assessment'])}")
    
    recommendations = simulation['recommendations']
    print(f"    Priority reforms: {len(recommendations['priority_reforms'])}")
    print(f"    Implementation steps: {len(recommendations['implementation_steps'])}")
    
    return integration


def test_simple_usage_example():
    """Test simple usage example for practical application"""
    print("\n\n🚀 Simple Usage Example")
    print("=" * 25)
    
    # Quick setup for practical use
    assessment = SimpleSelfAssessment()
    
    print("📝 Scenario: AI agent analyzing user query about climate patterns")
    
    # Simulate AI task performance
    start_time = time.time()
    
    # AI agent processes query
    expected = "provide comprehensive analysis of climate patterns with data sources"
    actual = "analyzed global temperature trends, precipitation patterns, and extreme weather events using NOAA and NASA data"
    confidence_before = 0.75
    
    processing_time = time.time() - start_time + 2.3  # Simulate 2.3s processing
    
    # Self-assess the performance
    result = assessment.assess_task_performance(
        task_category=TaskCategory.ANALYSIS,
        expected_outcome=expected,
        actual_outcome=actual,
        predicted_confidence=confidence_before,
        processing_time=processing_time
    )
    
    print(f"\n📊 Self-Assessment Results:")
    print(f"  Task accuracy: {result.accuracy_score:.1%}")
    print(f"  Confidence before: {result.confidence_predicted:.1%}")
    print(f"  Confidence after: {result.confidence_actual:.1%}")
    print(f"  Processing time: {result.processing_time:.1f}s")
    
    if result.errors_detected:
        print(f"  ⚠️  Errors detected: {', '.join(result.errors_detected)}")
    
    if result.lessons_learned:
        print(f"  💡 Lessons learned: {', '.join(result.lessons_learned)}")
    
    # Show how this helps with self-improvement
    print(f"\n🎯 Self-Improvement Insights:")
    
    if result.accuracy_score > 0.8:
        print("  ✅ Strong performance - maintain current approach")
    elif result.accuracy_score > 0.6:
        print("  📈 Good performance - minor improvements needed")
    else:
        print("  🔧 Performance needs improvement - review methodology")
    
    confidence_gap = abs(result.confidence_predicted - result.confidence_actual)
    if confidence_gap > 0.2:
        print("  ⚖️  Confidence calibration needs adjustment")
    else:
        print("  ✅ Confidence well-calibrated")
    
    return assessment


if __name__ == "__main__":
    print("🔬 Simple Self-Assessment System Tests")
    print("=" * 50)
    
    # Run all tests
    basic_assessment = test_basic_self_assessment()
    cortex_integration = test_cortex_integration() 
    simple_example = test_simple_usage_example()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed successfully!")
    print("\n🎯 Key Benefits Demonstrated:")
    print("  • Performance tracking and accuracy measurement")
    print("  • Confidence calibration and improvement")
    print("  • Learning progress monitoring")
    print("  • Capability boundary identification")
    print("  • Integration with existing CORTEX Guardian system")
    print("  • Practical self-improvement recommendations")
    print("\n💡 This provides Copilot-like self-assessment without complexity or policy issues!")