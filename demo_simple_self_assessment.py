#!/usr/bin/env python3
"""
CORTEX Simple Self-Assessment Demo
=================================

Practical demonstration of how to use the simple self-assessment system
with the existing CORTEX architecture for improved AI capability evaluation.

This demonstrates the simplest approach to replicate Copilot-like self-assessment
capabilities without complexity or policy violations.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

from simple_self_assessment import SimpleSelfAssessment, TaskCategory
from cortex_self_assessment_integration import CortexSelfAssessmentIntegration
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem


class SimpleCortexSelfAssessment:
    """
    Simple wrapper that adds self-assessment to existing CORTEX operations.
    
    This is the minimal integration approach - just add self-assessment
    capabilities to existing CORTEX cycles without changing the core system.
    """
    
    def __init__(self):
        # Initialize existing CORTEX system
        try:
            self.cortex_system = CortexPanaceaIntegratedSystem()
            self.cortex_available = True
            print("✅ CORTEX system initialized")
        except Exception as e:
            print(f"⚠️  CORTEX system not available: {e}")
            self.cortex_system = None
            self.cortex_available = False
        
        # Initialize self-assessment
        self.self_assessment = SimpleSelfAssessment()
        self.integration = CortexSelfAssessmentIntegration()
        
        print("✅ Simple self-assessment system ready")
    
    def run_self_assessed_cortex_cycle(self, 
                                     expected_insights: List[str],
                                     confidence_prediction: float,
                                     file_path: str = None) -> Dict[str, Any]:
        """
        Run a CORTEX cycle with self-assessment capabilities.
        
        Args:
            expected_insights: What insights we expect to discover
            confidence_prediction: Our confidence level (0.0-1.0) before processing
            file_path: Optional specific file to process
            
        Returns:
            Results including both CORTEX output and self-assessment
        """
        print(f"\n🧠 Running Self-Assessed CORTEX Cycle")
        print(f"   Expected insights: {len(expected_insights)}")
        print(f"   Predicted confidence: {confidence_prediction:.1%}")
        
        start_time = time.time()
        
        if self.cortex_available and file_path:
            # Run actual CORTEX cycle
            cycle_result = self.cortex_system._execute_single_cycle(1, file_path)
            processing_time = cycle_result.processing_time
            actual_insights = cycle_result.insights
            
            # Perform integrated assessment
            assessment_report = self.integration.assess_cortex_cycle(
                cycle_result=cycle_result,
                expected_insights=expected_insights,
                predicted_confidence=confidence_prediction
            )
            
            print(f"✅ CORTEX cycle completed in {processing_time:.1f}s")
            print(f"   Insights generated: {len(actual_insights)}")
            print(f"   Self-assessment accuracy: {assessment_report.self_assessment_performance.accuracy_score:.1%}")
            print(f"   Overall capability score: {assessment_report.overall_capability_score:.1%}")
            
        else:
            # Simulate CORTEX cycle for demonstration
            processing_time = time.time() - start_time + 2.0
            actual_insights = [
                "pattern recognition enhanced through iterative analysis",
                "truth verification improved via cross-validation",
                "knowledge synthesis optimized using multi-dimensional frameworks"
            ]
            
            # Create simulated result and assess
            from cortex_panacea_integrated_system import CycleResult
            simulated_result = CycleResult(
                cycle_number=1,
                file_processed=file_path or "simulated_input.txt",
                insights=actual_insights,
                truth_crystallization_level=0.7,
                processing_time=processing_time
            )
            
            assessment_report = self.integration.assess_cortex_cycle(
                cycle_result=simulated_result,
                expected_insights=expected_insights,
                predicted_confidence=confidence_prediction
            )
            
            print(f"✅ Simulated cycle completed in {processing_time:.1f}s")
            print(f"   Insights generated: {len(actual_insights)}")
            print(f"   Self-assessment accuracy: {assessment_report.self_assessment_performance.accuracy_score:.1%}")
        
        # Extract key self-assessment insights
        performance = assessment_report.self_assessment_performance
        
        # Show self-assessment results
        print(f"\n📊 Self-Assessment Results:")
        print(f"   Performance accuracy: {performance.accuracy_score:.1%}")
        print(f"   Confidence before: {performance.confidence_predicted:.1%}")
        print(f"   Confidence after: {performance.confidence_actual:.1%}")
        
        if performance.errors_detected:
            print(f"   ⚠️  Errors: {', '.join(performance.errors_detected)}")
        
        if performance.lessons_learned:
            print(f"   💡 Lessons: {', '.join(performance.lessons_learned)}")
        
        if assessment_report.integrated_recommendations:
            print(f"   🎯 Recommendations: {', '.join(assessment_report.integrated_recommendations[:3])}")
        
        return {
            "cortex_results": {
                "insights": actual_insights,
                "processing_time": processing_time,
                "truth_crystallization": getattr(assessment_report, 'cycle_result', {}).get('truth_crystallization_level', 0.7)
            },
            "self_assessment": {
                "accuracy": performance.accuracy_score,
                "confidence_predicted": performance.confidence_predicted,
                "confidence_actual": performance.confidence_actual,
                "errors": performance.errors_detected,
                "lessons": performance.lessons_learned,
                "recommendations": assessment_report.integrated_recommendations
            },
            "overall_capability_score": assessment_report.overall_capability_score
        }
    
    def get_learning_progress_report(self) -> Dict[str, Any]:
        """Get a comprehensive learning progress report"""
        print(f"\n📈 Generating Learning Progress Report")
        
        # Get self-assessment summary
        self_summary = self.self_assessment.get_self_assessment_summary()
        
        # Get integrated assessment
        comprehensive = self.integration.get_comprehensive_assessment()
        
        print(f"✅ Report generated")
        print(f"   Total tasks completed: {self_summary.get('total_tasks_completed', 0)}")
        print(f"   Current performance level: {self_summary.get('overall_performance', {}).get('performance_level', 'unknown')}")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "self_assessment_summary": self_summary,
            "comprehensive_assessment": comprehensive,
            "key_metrics": {
                "tasks_completed": self_summary.get('total_tasks_completed', 0),
                "current_accuracy": self_summary.get('overall_performance', {}).get('accuracy', 0),
                "performance_level": self_summary.get('overall_performance', {}).get('performance_level', 'unknown'),
                "active_recommendations": len(self_summary.get('recommendations', []))
            }
        }
    
    def suggest_cortex_reforms(self, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Suggest CORTEX system reforms based on self-assessment insights"""
        print(f"\n🔧 Analyzing System for Reform Opportunities")
        
        # Define reform parameters based on self-assessment
        reform_params = {}
        
        # Analyze current performance to suggest reforms
        summary = self.self_assessment.get_self_assessment_summary()
        current_accuracy = summary.get('overall_performance', {}).get('accuracy', 0.5)
        
        # Suggest specific reforms based on performance gaps
        if current_accuracy < 0.6:
            reform_params['truth_detection_enhancement'] = 0.4
            print("   📊 Truth detection enhancement recommended")
        
        calibration = self.self_assessment.calibrate_confidence()
        if calibration.get('status') == 'calibrated':
            recommendations = calibration.get('recommendations', [])
            if 'reduce_overconfidence_for_high_predictions' in recommendations:
                reform_params['confidence_calibration_reform'] = 0.3
                print("   ⚖️  Confidence calibration reform recommended")
        
        # Learning rate optimization
        progress = self.self_assessment.get_learning_progress()
        if progress.get('accuracy_trend') == 'declining':
            reform_params['learning_rate_optimization'] = 0.5
            print("   📈 Learning rate optimization recommended")
        elif progress.get('improvement_rate', 0) < 0.1:
            reform_params['learning_rate_optimization'] = 0.2
            print("   📈 Minor learning rate optimization recommended")
        
        if not reform_params:
            reform_params['maintenance_optimization'] = 0.1
            print("   🔧 Maintenance optimization recommended")
        
        # Simulate the reforms
        simulation = self.integration.simulate_cortex_reform(reform_params)
        
        print(f"✅ Reform analysis completed")
        print(f"   Proposed reforms: {len(reform_params)}")
        print(f"   Implementation feasibility: {simulation['simulation_results']['reform_feasibility']}")
        print(f"   Implementation complexity: {simulation['simulation_results']['implementation_complexity']}")
        
        return {
            "proposed_reforms": reform_params,
            "simulation_results": simulation,
            "implementation_priority": "high" if current_accuracy < 0.5 else "medium" if current_accuracy < 0.7 else "low"
        }


def demo_simple_self_assessment():
    """Demonstrate the simple self-assessment approach"""
    print("🚀 CORTEX Simple Self-Assessment Demo")
    print("=" * 45)
    print("This demonstrates the simplest approach to AI self-assessment")
    print("similar to Copilot agents, without policy violations or complexity.")
    
    # Initialize the system
    cortex_sa = SimpleCortexSelfAssessment()
    
    # Demo 1: Self-assessed CORTEX cycle
    print(f"\n" + "=" * 50)
    print("📋 Demo 1: Self-Assessed Processing Cycle")
    print("=" * 50)
    
    expected_insights = [
        "improve pattern recognition accuracy",
        "enhance truth verification protocols", 
        "optimize knowledge synthesis methods"
    ]
    
    result1 = cortex_sa.run_self_assessed_cortex_cycle(
        expected_insights=expected_insights,
        confidence_prediction=0.75
    )
    
    # Demo 2: Multiple cycles to show learning
    print(f"\n" + "=" * 50)
    print("📋 Demo 2: Learning Through Multiple Cycles")
    print("=" * 50)
    
    learning_scenarios = [
        {
            "expected": ["detect temporal patterns", "identify causal relationships"],
            "confidence": 0.6,
            "description": "Pattern analysis task"
        },
        {
            "expected": ["verify source credibility", "cross-check facts"],
            "confidence": 0.8,
            "description": "Truth verification task"
        },
        {
            "expected": ["synthesize multiple perspectives", "create unified framework"],
            "confidence": 0.7,
            "description": "Knowledge synthesis task"
        }
    ]
    
    for i, scenario in enumerate(learning_scenarios, 1):
        print(f"\n🔄 Cycle {i}: {scenario['description']}")
        result = cortex_sa.run_self_assessed_cortex_cycle(
            expected_insights=scenario["expected"],
            confidence_prediction=scenario["confidence"]
        )
    
    # Demo 3: Learning progress analysis
    print(f"\n" + "=" * 50)
    print("📋 Demo 3: Learning Progress Analysis")
    print("=" * 50)
    
    progress_report = cortex_sa.get_learning_progress_report()
    
    # Demo 4: System reform suggestions
    print(f"\n" + "=" * 50)
    print("📋 Demo 4: System Reform Suggestions")
    print("=" * 50)
    
    reform_suggestions = cortex_sa.suggest_cortex_reforms()
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📋 Demo Summary: Key Capabilities Demonstrated")
    print("=" * 50)
    
    print("✅ Core Self-Assessment Features:")
    print("   • Real-time performance measurement and accuracy tracking")
    print("   • Confidence calibration and prediction accuracy")
    print("   • Learning progress monitoring across multiple tasks")
    print("   • Error detection and lesson extraction")
    print("   • Capability boundary identification")
    
    print("\n✅ CORTEX Integration Features:")
    print("   • Seamless integration with existing Guardian system")
    print("   • Enhanced cycle assessment with multi-dimensional scoring")
    print("   • Reform simulation and recommendation generation")
    print("   • Comprehensive progress tracking and reporting")
    
    print("\n✅ Practical Benefits:")
    print("   • Simple to implement and understand")
    print("   • No policy violations or complexity overhead")
    print("   • Immediate actionable insights for improvement")
    print("   • Compatible with existing CORTEX architecture")
    print("   • Provides Copilot-like self-assessment capabilities")
    
    return cortex_sa, progress_report, reform_suggestions


if __name__ == "__main__":
    # Run the complete demonstration
    system, progress, reforms = demo_simple_self_assessment()
    
    print(f"\n🎯 Ready for practical use!")
    print("Use SimpleCortexSelfAssessment for your CORTEX operations with built-in self-assessment.")