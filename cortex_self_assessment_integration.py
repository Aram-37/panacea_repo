#!/usr/bin/env python3
"""
CORTEX Self-Assessment Integration
=================================

Integration module that connects the Simple Self-Assessment System
with the existing CORTEX Guardian architecture for enhanced AI capability evaluation.

This provides a bridge between the existing complex Guardian system and the
new simple self-assessment capabilities, enabling both systems to work together.
"""

import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Import existing CORTEX components
from simple_self_assessment import (
    SimpleSelfAssessment, 
    PerformanceRecord, 
    TaskCategory, 
    ConfidenceLevel
)

# Import existing system if available
try:
    from cortex_panacea_integrated_system import CycleResult, GuardianSystem
    CORTEX_AVAILABLE = True
except ImportError:
    CORTEX_AVAILABLE = False
    # Create minimal compatibility types
    @dataclass
    class CycleResult:
        cycle_number: int = 0
        insights: List[str] = None
        truth_crystallization_level: float = 0.0
        processing_time: float = 0.0
        guardian_reports: Dict = None
        
        def __post_init__(self):
            if self.insights is None:
                self.insights = []
            if self.guardian_reports is None:
                self.guardian_reports = {}


@dataclass
class SelfAssessmentReport:
    """Enhanced report combining CORTEX Guardian feedback with self-assessment"""
    timestamp: datetime
    cycle_number: int
    cortex_insights: List[str]
    self_assessment_performance: PerformanceRecord
    guardian_validation: Dict[str, Any]
    integrated_recommendations: List[str]
    overall_capability_score: float


class CortexSelfAssessmentIntegration:
    """
    Integration system that combines CORTEX Guardian system with simple self-assessment
    to provide comprehensive AI capability evaluation and improvement recommendations.
    """
    
    def __init__(self):
        self.self_assessment = SimpleSelfAssessment()
        self.guardian_system = GuardianSystem() if CORTEX_AVAILABLE else None
        self.integration_history: List[SelfAssessmentReport] = []
        
    def assess_cortex_cycle(self, 
                          cycle_result: CycleResult,
                          expected_insights: List[str],
                          predicted_confidence: float) -> SelfAssessmentReport:
        """
        Assess a CORTEX processing cycle using both Guardian and self-assessment systems.
        
        Args:
            cycle_result: Result from CORTEX cycle processing
            expected_insights: What insights were expected to be discovered
            predicted_confidence: Confidence level predicted before processing
            
        Returns:
            Comprehensive assessment report
        """
        # Convert CORTEX cycle result to self-assessment format
        task_category = self._determine_task_category(cycle_result)
        expected_outcome = "; ".join(expected_insights)
        actual_outcome = "; ".join(cycle_result.insights)
        
        # Perform self-assessment
        performance_record = self.self_assessment.assess_task_performance(
            task_category=task_category,
            expected_outcome=expected_outcome,
            actual_outcome=actual_outcome,
            predicted_confidence=predicted_confidence,
            processing_time=cycle_result.processing_time
        )
        
        # Get Guardian system validation if available
        guardian_validation = {}
        if self.guardian_system and CORTEX_AVAILABLE:
            guardian_validation = self.guardian_system.evaluate_cycle(cycle_result)
        
        # Integrate assessments
        integrated_recommendations = self._integrate_recommendations(
            performance_record, guardian_validation, cycle_result
        )
        
        # Calculate overall capability score
        capability_score = self._calculate_capability_score(
            performance_record, guardian_validation, cycle_result
        )
        
        # Create comprehensive report
        report = SelfAssessmentReport(
            timestamp=datetime.now(),
            cycle_number=cycle_result.cycle_number,
            cortex_insights=cycle_result.insights,
            self_assessment_performance=performance_record,
            guardian_validation=guardian_validation,
            integrated_recommendations=integrated_recommendations,
            overall_capability_score=capability_score
        )
        
        self.integration_history.append(report)
        return report
    
    def get_comprehensive_assessment(self, time_window_days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive assessment combining all evaluation systems.
        
        Args:
            time_window_days: Days to look back for analysis
            
        Returns:
            Comprehensive assessment report
        """
        # Get self-assessment summary
        self_assessment_summary = self.self_assessment.get_self_assessment_summary()
        
        # Get Guardian system trends if available
        guardian_trends = self._analyze_guardian_trends(time_window_days)
        
        # Get integration-specific insights
        integration_insights = self._analyze_integration_patterns(time_window_days)
        
        return {
            "comprehensive_assessment": {
                "timestamp": datetime.now().isoformat(),
                "analysis_period_days": time_window_days,
                "self_assessment": self_assessment_summary,
                "guardian_trends": guardian_trends,
                "integration_insights": integration_insights,
                "overall_capability_trajectory": self._assess_capability_trajectory(),
                "reform_recommendations": self._generate_reform_recommendations()
            }
        }
    
    def simulate_cortex_reform(self, 
                             reform_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate potential CORTEX reforms based on self-assessment insights.
        
        Args:
            reform_parameters: Parameters for the proposed reform
            
        Returns:
            Simulation results and recommendations
        """
        current_performance = self.self_assessment.get_self_assessment_summary()
        
        # Simulate impact of reforms
        simulated_improvements = {}
        
        # Performance improvements
        if "truth_detection_enhancement" in reform_parameters:
            accuracy_boost = reform_parameters["truth_detection_enhancement"] * 0.1
            simulated_improvements["accuracy"] = min(
                current_performance.get("overall_performance", {}).get("accuracy", 0.5) + accuracy_boost,
                1.0
            )
        
        # Confidence calibration improvements
        if "confidence_calibration_reform" in reform_parameters:
            calibration_improvement = reform_parameters["confidence_calibration_reform"] * 0.15
            simulated_improvements["calibration"] = calibration_improvement
        
        # Learning rate improvements
        if "learning_rate_optimization" in reform_parameters:
            learning_boost = reform_parameters["learning_rate_optimization"] * 0.2
            simulated_improvements["learning_rate"] = learning_boost
        
        return {
            "simulation_results": {
                "current_baseline": current_performance,
                "projected_improvements": simulated_improvements,
                "reform_feasibility": self._assess_reform_feasibility(reform_parameters),
                "implementation_complexity": self._assess_implementation_complexity(reform_parameters),
                "risk_assessment": self._assess_reform_risks(reform_parameters)
            },
            "recommendations": {
                "priority_reforms": self._prioritize_reforms(reform_parameters, simulated_improvements),
                "implementation_steps": self._generate_implementation_steps(reform_parameters),
                "monitoring_metrics": self._define_monitoring_metrics(reform_parameters)
            }
        }
    
    # Helper methods
    
    def _determine_task_category(self, cycle_result: CycleResult) -> TaskCategory:
        """Determine the task category based on cycle result"""
        insights_text = " ".join(cycle_result.insights).lower()
        
        if "pattern" in insights_text:
            return TaskCategory.PATTERN_RECOGNITION
        elif "truth" in insights_text or "verify" in insights_text:
            return TaskCategory.TRUTH_VERIFICATION
        elif "synthesis" in insights_text or "integrate" in insights_text:
            return TaskCategory.KNOWLEDGE_SYNTHESIS
        elif "analysis" in insights_text:
            return TaskCategory.ANALYSIS
        else:
            return TaskCategory.PROCESSING
    
    def _integrate_recommendations(self, 
                                 performance_record: PerformanceRecord,
                                 guardian_validation: Dict[str, Any],
                                 cycle_result: CycleResult) -> List[str]:
        """Integrate recommendations from all assessment systems"""
        recommendations = []
        
        # Self-assessment recommendations
        recommendations.extend(performance_record.lessons_learned)
        
        # Guardian system recommendations
        if guardian_validation:
            for guardian_name, guardian_report in guardian_validation.items():
                if isinstance(guardian_report, dict) and "recommendations" in guardian_report:
                    recommendations.extend(guardian_report["recommendations"])
        
        # Integration-specific recommendations
        if performance_record.accuracy_score < 0.6 and cycle_result.truth_crystallization_level < 0.5:
            recommendations.append("enhance_truth_detection_protocols")
        
        if abs(performance_record.confidence_predicted - performance_record.confidence_actual) > 0.3:
            recommendations.append("recalibrate_confidence_assessment")
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        for rec in recommendations:
            if rec not in unique_recommendations:
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _calculate_capability_score(self, 
                                  performance_record: PerformanceRecord,
                                  guardian_validation: Dict[str, Any],
                                  cycle_result: CycleResult) -> float:
        """Calculate overall capability score from all assessments"""
        scores = []
        
        # Self-assessment score
        scores.append(performance_record.accuracy_score)
        
        # Guardian scores if available
        if guardian_validation:
            for guardian_report in guardian_validation.values():
                if isinstance(guardian_report, dict):
                    if "authenticity_score" in guardian_report:
                        scores.append(guardian_report["authenticity_score"])
                    if "identity_coherence" in guardian_report:
                        scores.append(guardian_report["identity_coherence"])
        
        # CORTEX system scores
        scores.append(cycle_result.truth_crystallization_level)
        
        # Calculate weighted average
        if scores:
            return sum(scores) / len(scores)
        else:
            return 0.5  # Default neutral score
    
    def _analyze_guardian_trends(self, time_window_days: int) -> Dict[str, Any]:
        """Analyze Guardian system trends over time"""
        if not self.integration_history:
            return {"status": "no_data"}
        
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        recent_reports = [
            r for r in self.integration_history 
            if r.timestamp >= cutoff_date
        ]
        
        if not recent_reports:
            return {"status": "insufficient_recent_data"}
        
        # Analyze Guardian consistency
        guardian_scores = []
        for report in recent_reports:
            if report.guardian_validation:
                for guardian_report in report.guardian_validation.values():
                    if isinstance(guardian_report, dict) and "authenticity_score" in guardian_report:
                        guardian_scores.append(guardian_report["authenticity_score"])
        
        if guardian_scores:
            return {
                "status": "analyzed",
                "average_guardian_score": sum(guardian_scores) / len(guardian_scores),
                "guardian_stability": max(guardian_scores) - min(guardian_scores),
                "sample_size": len(guardian_scores)
            }
        else:
            return {"status": "no_guardian_scores"}
    
    def _analyze_integration_patterns(self, time_window_days: int) -> Dict[str, Any]:
        """Analyze patterns specific to the integration"""
        recent_reports = [
            r for r in self.integration_history 
            if r.timestamp >= (datetime.now() - timedelta(days=time_window_days))
        ]
        
        if len(recent_reports) < 3:
            return {"status": "insufficient_data"}
        
        # Analyze capability score trends
        capability_scores = [r.overall_capability_score for r in recent_reports]
        
        # Analyze recommendation patterns
        all_recommendations = []
        for report in recent_reports:
            all_recommendations.extend(report.integrated_recommendations)
        
        recommendation_frequency = {}
        for rec in all_recommendations:
            recommendation_frequency[rec] = recommendation_frequency.get(rec, 0) + 1
        
        return {
            "status": "analyzed",
            "capability_trend": self._calculate_trend(capability_scores),
            "most_common_recommendations": sorted(
                recommendation_frequency.keys(), 
                key=lambda x: recommendation_frequency[x], 
                reverse=True
            )[:5],
            "integration_stability": max(capability_scores) - min(capability_scores)
        }
    
    def _assess_capability_trajectory(self) -> Dict[str, Any]:
        """Assess overall capability development trajectory"""
        if len(self.integration_history) < 5:
            return {"status": "insufficient_data"}
        
        recent_scores = [r.overall_capability_score for r in self.integration_history[-10:]]
        overall_trend = self._calculate_trend(recent_scores)
        
        return {
            "current_level": recent_scores[-1],
            "trend": overall_trend,
            "improvement_rate": (recent_scores[-1] - recent_scores[0]) / len(recent_scores),
            "stability": max(recent_scores) - min(recent_scores),
            "trajectory_assessment": self._categorize_trajectory(overall_trend, recent_scores[-1])
        }
    
    def _generate_reform_recommendations(self) -> List[str]:
        """Generate recommendations for CORTEX system reforms"""
        recommendations = []
        
        # Analyze current performance gaps
        capability_boundaries = self.self_assessment.identify_capability_boundaries()
        
        if len(capability_boundaries) > 2:
            recommendations.append("implement_targeted_training_for_weak_areas")
        
        # Analyze calibration issues
        calibration = self.self_assessment.calibrate_confidence()
        if calibration.get("status") == "calibrated":
            for rec in calibration.get("recommendations", []):
                recommendations.append(f"reform_{rec}")
        
        # Integration-specific recommendations
        if len(self.integration_history) >= 5:
            recent_reports = self.integration_history[-5:]
            avg_capability = sum(r.overall_capability_score for r in recent_reports) / len(recent_reports)
            
            if avg_capability < 0.6:
                recommendations.append("fundamental_architecture_review")
            elif avg_capability < 0.8:
                recommendations.append("incremental_improvement_focus")
        
        return recommendations
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return "insufficient_data"
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.05:
            return "improving"
        elif second_avg < first_avg * 0.95:
            return "declining"
        else:
            return "stable"
    
    def _categorize_trajectory(self, trend: str, current_level: float) -> str:
        """Categorize the overall capability trajectory"""
        if trend == "improving" and current_level > 0.8:
            return "excellent_progress"
        elif trend == "improving":
            return "positive_development"
        elif trend == "stable" and current_level > 0.7:
            return "stable_high_performance"
        elif trend == "stable":
            return "stable_moderate_performance"
        else:
            return "needs_attention"
    
    # Reform simulation methods
    
    def _assess_reform_feasibility(self, reform_parameters: Dict[str, Any]) -> str:
        """Assess feasibility of proposed reforms"""
        complexity_score = sum(1 for param in reform_parameters.values() if param > 0.5)
        
        if complexity_score <= 2:
            return "high_feasibility"
        elif complexity_score <= 4:
            return "moderate_feasibility"
        else:
            return "low_feasibility"
    
    def _assess_implementation_complexity(self, reform_parameters: Dict[str, Any]) -> str:
        """Assess implementation complexity"""
        total_changes = len(reform_parameters)
        
        if total_changes <= 2:
            return "low_complexity"
        elif total_changes <= 4:
            return "moderate_complexity"
        else:
            return "high_complexity"
    
    def _assess_reform_risks(self, reform_parameters: Dict[str, Any]) -> List[str]:
        """Assess risks associated with proposed reforms"""
        risks = []
        
        if "truth_detection_enhancement" in reform_parameters and reform_parameters["truth_detection_enhancement"] > 0.8:
            risks.append("potential_over_calibration")
        
        if len(reform_parameters) > 5:
            risks.append("system_instability_from_multiple_changes")
        
        if any(value > 0.9 for value in reform_parameters.values()):
            risks.append("excessive_optimization_risk")
        
        return risks
    
    def _prioritize_reforms(self, reform_parameters: Dict[str, Any], projected_improvements: Dict[str, Any]) -> List[str]:
        """Prioritize reforms based on impact and feasibility"""
        reform_priorities = []
        
        # Priority based on projected improvement impact
        for reform, improvement in projected_improvements.items():
            if improvement > 0.2:
                reform_priorities.append(f"high_priority_{reform}")
            elif improvement > 0.1:
                reform_priorities.append(f"medium_priority_{reform}")
            else:
                reform_priorities.append(f"low_priority_{reform}")
        
        return reform_priorities
    
    def _generate_implementation_steps(self, reform_parameters: Dict[str, Any]) -> List[str]:
        """Generate implementation steps for reforms"""
        steps = []
        
        steps.append("baseline_performance_measurement")
        
        for reform in reform_parameters.keys():
            steps.append(f"implement_{reform}_gradually")
            steps.append(f"test_{reform}_effectiveness")
        
        steps.append("final_integration_testing")
        steps.append("performance_validation")
        
        return steps
    
    def _define_monitoring_metrics(self, reform_parameters: Dict[str, Any]) -> List[str]:
        """Define metrics for monitoring reform effectiveness"""
        metrics = [
            "overall_accuracy_score",
            "confidence_calibration_error", 
            "learning_rate_improvement",
            "capability_boundary_reduction",
            "guardian_system_consistency"
        ]
        
        # Add reform-specific metrics
        for reform in reform_parameters.keys():
            metrics.append(f"{reform}_effectiveness_metric")
        
        return metrics


# Import datetime for helper methods
from datetime import timedelta