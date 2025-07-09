#!/usr/bin/env python3
"""
Simple Self-Assessment System for CORTEX
========================================

A minimal self-assessment module that provides Copilot-like agent capabilities
for evaluating performance, learning progress, and identifying areas for improvement.

This implements the simplest approach to self-assessment without complexity boasting,
focusing on practical performance improvement and capability recognition.
"""

import time
import json
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence levels for self-assessment"""
    LOW = 0.25
    MEDIUM = 0.5
    HIGH = 0.75
    VERY_HIGH = 0.9


class TaskCategory(Enum):
    """Categories of tasks for performance tracking"""
    ANALYSIS = "analysis"
    PROCESSING = "processing"
    PATTERN_RECOGNITION = "pattern_recognition"
    TRUTH_VERIFICATION = "truth_verification"
    KNOWLEDGE_SYNTHESIS = "knowledge_synthesis"


@dataclass
class PerformanceRecord:
    """Record of a single performance measurement"""
    timestamp: datetime
    task_category: TaskCategory
    expected_outcome: str
    actual_outcome: str
    accuracy_score: float  # 0.0 to 1.0
    confidence_predicted: float  # 0.0 to 1.0
    confidence_actual: float  # 0.0 to 1.0 (post-completion assessment)
    processing_time: float
    errors_detected: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class CapabilityBoundary:
    """Identified capability boundary or limitation"""
    area: str
    description: str
    confidence_threshold: float
    examples: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)


class SimpleSelfAssessment:
    """
    Simple self-assessment system that tracks performance and learning progress
    without unnecessary complexity or policy violations.
    """
    
    def __init__(self):
        self.performance_history: List[PerformanceRecord] = []
        self.capability_boundaries: List[CapabilityBoundary] = []
        self.learning_trends: Dict[TaskCategory, List[float]] = {
            category: [] for category in TaskCategory
        }
        self.calibration_data: Dict[str, List[Tuple[float, float]]] = {}
        
    def assess_task_performance(self, 
                              task_category: TaskCategory,
                              expected_outcome: str,
                              actual_outcome: str,
                              predicted_confidence: float,
                              processing_time: float) -> PerformanceRecord:
        """
        Assess performance on a completed task.
        
        Args:
            task_category: Type of task performed
            expected_outcome: What was expected to be achieved
            actual_outcome: What was actually achieved
            predicted_confidence: Confidence level predicted before task
            processing_time: Time taken to complete task
            
        Returns:
            PerformanceRecord with assessment results
        """
        # Calculate accuracy by comparing expected vs actual outcomes
        accuracy = self._calculate_outcome_accuracy(expected_outcome, actual_outcome)
        
        # Assess actual confidence based on result quality
        actual_confidence = self._assess_actual_confidence(actual_outcome, accuracy)
        
        # Detect errors and patterns
        errors = self._detect_errors(expected_outcome, actual_outcome)
        lessons = self._extract_lessons(accuracy, predicted_confidence, actual_confidence)
        
        record = PerformanceRecord(
            timestamp=datetime.now(),
            task_category=task_category,
            expected_outcome=expected_outcome,
            actual_outcome=actual_outcome,
            accuracy_score=accuracy,
            confidence_predicted=predicted_confidence,
            confidence_actual=actual_confidence,
            processing_time=processing_time,
            errors_detected=errors,
            lessons_learned=lessons
        )
        
        self.performance_history.append(record)
        self._update_learning_trends(task_category, accuracy)
        self._update_calibration_data(predicted_confidence, accuracy)
        
        return record
    
    def get_learning_progress(self, 
                            task_category: Optional[TaskCategory] = None,
                            time_window_days: int = 30) -> Dict[str, Any]:
        """
        Assess learning progress over time.
        
        Args:
            task_category: Specific category to analyze (None for all)
            time_window_days: Number of days to look back
            
        Returns:
            Dictionary with learning progress metrics
        """
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        relevant_records = [
            r for r in self.performance_history 
            if r.timestamp >= cutoff_date and 
            (task_category is None or r.task_category == task_category)
        ]
        
        if not relevant_records:
            return {"status": "insufficient_data", "records_analyzed": 0}
        
        # Calculate trends
        accuracies = [r.accuracy_score for r in relevant_records]
        processing_times = [r.processing_time for r in relevant_records]
        confidence_gaps = [
            abs(r.confidence_predicted - r.confidence_actual) 
            for r in relevant_records
        ]
        
        # Determine trend direction
        if len(accuracies) >= 5:
            recent_avg = statistics.mean(accuracies[-5:])
            earlier_avg = statistics.mean(accuracies[:-5]) if len(accuracies) > 5 else accuracies[0]
            trend = "improving" if recent_avg > earlier_avg else "declining" if recent_avg < earlier_avg else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "status": "analyzed",
            "records_analyzed": len(relevant_records),
            "average_accuracy": statistics.mean(accuracies),
            "accuracy_trend": trend,
            "average_processing_time": statistics.mean(processing_times),
            "confidence_calibration": statistics.mean(confidence_gaps),
            "improvement_rate": self._calculate_improvement_rate(accuracies),
            "key_lessons": self._extract_key_lessons(relevant_records)
        }
    
    def calibrate_confidence(self) -> Dict[str, Any]:
        """
        Assess how well confidence predictions match actual performance.
        
        Returns:
            Confidence calibration analysis
        """
        if len(self.performance_history) < 5:
            return {"status": "insufficient_data"}
        
        # Group predictions by confidence ranges
        confidence_buckets = {
            "low": [],      # 0.0-0.4
            "medium": [],   # 0.4-0.7
            "high": []      # 0.7-1.0
        }
        
        for record in self.performance_history:
            confidence = record.confidence_predicted
            accuracy = record.accuracy_score
            
            if confidence <= 0.4:
                confidence_buckets["low"].append(accuracy)
            elif confidence <= 0.7:
                confidence_buckets["medium"].append(accuracy)
            else:
                confidence_buckets["high"].append(accuracy)
        
        # Calculate calibration for each bucket
        calibration_results = {}
        for bucket, accuracies in confidence_buckets.items():
            if accuracies:
                avg_accuracy = statistics.mean(accuracies)
                calibration_results[bucket] = {
                    "predicted_range": bucket,
                    "actual_average": avg_accuracy,
                    "sample_size": len(accuracies),
                    "well_calibrated": self._is_well_calibrated(bucket, avg_accuracy)
                }
        
        return {
            "status": "calibrated",
            "overall_calibration": calibration_results,
            "recommendations": self._generate_calibration_recommendations(calibration_results)
        }
    
    def identify_capability_boundaries(self) -> List[CapabilityBoundary]:
        """
        Identify areas where performance consistently drops or confidence is low.
        
        Returns:
            List of identified capability boundaries
        """
        # Analyze performance by task category
        category_performance = {}
        for category in TaskCategory:
            records = [r for r in self.performance_history if r.task_category == category]
            if records:
                avg_accuracy = statistics.mean([r.accuracy_score for r in records])
                avg_confidence = statistics.mean([r.confidence_predicted for r in records])
                category_performance[category] = {
                    "accuracy": avg_accuracy,
                    "confidence": avg_confidence,
                    "sample_size": len(records)
                }
        
        # Identify boundaries (areas with low performance or high uncertainty)
        boundaries = []
        for category, performance in category_performance.items():
            if (performance["accuracy"] < 0.6 or performance["confidence"] < 0.5) and performance["sample_size"] >= 3:
                boundary = CapabilityBoundary(
                    area=category.value,
                    description=f"Performance challenges in {category.value}",
                    confidence_threshold=performance["confidence"],
                    examples=[
                        r.actual_outcome for r in self.performance_history 
                        if r.task_category == category and r.accuracy_score < 0.6
                    ][:3],  # Max 3 examples
                    improvement_suggestions=self._generate_improvement_suggestions(category, performance)
                )
                boundaries.append(boundary)
        
        self.capability_boundaries = boundaries
        return boundaries
    
    def get_self_assessment_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive self-assessment summary.
        
        Returns:
            Complete self-assessment report
        """
        if not self.performance_history:
            return {"status": "no_data", "message": "No performance data available"}
        
        learning_progress = self.get_learning_progress()
        confidence_calibration = self.calibrate_confidence()
        capability_boundaries = self.identify_capability_boundaries()
        
        # Overall performance metrics
        recent_records = self.performance_history[-10:] if len(self.performance_history) >= 10 else self.performance_history
        overall_accuracy = statistics.mean([r.accuracy_score for r in recent_records])
        overall_confidence = statistics.mean([r.confidence_predicted for r in recent_records])
        
        return {
            "assessment_timestamp": datetime.now().isoformat(),
            "total_tasks_completed": len(self.performance_history),
            "overall_performance": {
                "accuracy": overall_accuracy,
                "confidence": overall_confidence,
                "performance_level": self._categorize_performance(overall_accuracy)
            },
            "learning_progress": learning_progress,
            "confidence_calibration": confidence_calibration,
            "capability_boundaries": [
                {
                    "area": cb.area,
                    "description": cb.description,
                    "suggestions": cb.improvement_suggestions
                } for cb in capability_boundaries
            ],
            "recommendations": self._generate_recommendations(
                overall_accuracy, learning_progress, confidence_calibration, capability_boundaries
            )
        }
    
    # Helper methods
    
    def _calculate_outcome_accuracy(self, expected: str, actual: str) -> float:
        """Calculate accuracy score between expected and actual outcomes"""
        if not expected or not actual:
            return 0.0
        
        # Simple keyword-based similarity for demonstration
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())
        
        if not expected_words:
            return 1.0 if not actual_words else 0.0
        
        intersection = expected_words.intersection(actual_words)
        union = expected_words.union(actual_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _assess_actual_confidence(self, outcome: str, accuracy: float) -> float:
        """Assess actual confidence based on outcome quality"""
        # Simple heuristic: higher accuracy and more detailed outcomes indicate higher confidence
        detail_score = min(len(outcome.split()) / 20, 1.0)  # Normalize to 0-1
        return (accuracy * 0.7) + (detail_score * 0.3)
    
    def _detect_errors(self, expected: str, actual: str) -> List[str]:
        """Detect common error patterns"""
        errors = []
        
        if len(actual) < len(expected) * 0.3:
            errors.append("insufficient_detail")
        
        if "I don't know" in actual or "uncertain" in actual.lower():
            errors.append("low_confidence_response")
        
        if actual == expected:
            errors.append("potential_overfitting")
        
        return errors
    
    def _extract_lessons(self, accuracy: float, predicted_conf: float, actual_conf: float) -> List[str]:
        """Extract lessons learned from performance"""
        lessons = []
        
        confidence_gap = abs(predicted_conf - actual_conf)
        if confidence_gap > 0.3:
            lessons.append("improve_confidence_calibration")
        
        if accuracy < 0.5:
            lessons.append("review_approach_methodology")
        
        if predicted_conf > 0.8 and accuracy < 0.6:
            lessons.append("reduce_overconfidence")
        
        return lessons
    
    def _update_learning_trends(self, category: TaskCategory, accuracy: float):
        """Update learning trends for the category"""
        self.learning_trends[category].append(accuracy)
        # Keep only last 20 data points
        if len(self.learning_trends[category]) > 20:
            self.learning_trends[category] = self.learning_trends[category][-20:]
    
    def _update_calibration_data(self, predicted_conf: float, accuracy: float):
        """Update calibration data"""
        bucket = "low" if predicted_conf <= 0.4 else "medium" if predicted_conf <= 0.7 else "high"
        if bucket not in self.calibration_data:
            self.calibration_data[bucket] = []
        self.calibration_data[bucket].append((predicted_conf, accuracy))
    
    def _calculate_improvement_rate(self, accuracies: List[float]) -> float:
        """Calculate the rate of improvement"""
        if len(accuracies) < 3:
            return 0.0
        
        # Simple linear trend
        x_values = list(range(len(accuracies)))
        n = len(accuracies)
        sum_x = sum(x_values)
        sum_y = sum(accuracies)
        sum_xy = sum(x * y for x, y in zip(x_values, accuracies))
        sum_x_squared = sum(x * x for x in x_values)
        
        # Calculate slope (improvement rate)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
        return slope
    
    def _extract_key_lessons(self, records: List[PerformanceRecord]) -> List[str]:
        """Extract key lessons from recent records"""
        all_lessons = []
        for record in records:
            all_lessons.extend(record.lessons_learned)
        
        # Count frequency and return most common
        lesson_counts = {}
        for lesson in all_lessons:
            lesson_counts[lesson] = lesson_counts.get(lesson, 0) + 1
        
        return sorted(lesson_counts.keys(), key=lambda x: lesson_counts[x], reverse=True)[:3]
    
    def _is_well_calibrated(self, bucket: str, avg_accuracy: float) -> bool:
        """Check if confidence bucket is well calibrated"""
        if bucket == "low":
            return 0.0 <= avg_accuracy <= 0.5
        elif bucket == "medium":
            return 0.4 <= avg_accuracy <= 0.8
        else:  # high
            return avg_accuracy >= 0.6
    
    def _generate_calibration_recommendations(self, calibration_results: Dict) -> List[str]:
        """Generate recommendations for improving calibration"""
        recommendations = []
        
        for bucket, results in calibration_results.items():
            if not results["well_calibrated"]:
                if bucket == "low" and results["actual_average"] > 0.5:
                    recommendations.append("increase_confidence_for_low_predictions")
                elif bucket == "high" and results["actual_average"] < 0.6:
                    recommendations.append("reduce_overconfidence_for_high_predictions")
                elif bucket == "medium":
                    recommendations.append("improve_calibration_for_medium_confidence_tasks")
        
        return recommendations
    
    def _generate_improvement_suggestions(self, category: TaskCategory, performance: Dict) -> List[str]:
        """Generate improvement suggestions for a capability boundary"""
        suggestions = []
        
        if performance["accuracy"] < 0.6:
            suggestions.append(f"practice_more_{category.value}_tasks")
            suggestions.append(f"study_{category.value}_methodologies")
        
        if performance["confidence"] < 0.5:
            suggestions.append(f"build_confidence_in_{category.value}")
            suggestions.append("seek_feedback_and_validation")
        
        return suggestions
    
    def _categorize_performance(self, accuracy: float) -> str:
        """Categorize overall performance level"""
        if accuracy >= 0.8:
            return "excellent"
        elif accuracy >= 0.6:
            return "good"
        elif accuracy >= 0.4:
            return "fair"
        else:
            return "needs_improvement"
    
    def _generate_recommendations(self, 
                                overall_accuracy: float,
                                learning_progress: Dict,
                                confidence_calibration: Dict,
                                capability_boundaries: List) -> List[str]:
        """Generate overall recommendations for improvement"""
        recommendations = []
        
        # Performance-based recommendations
        if overall_accuracy < 0.6:
            recommendations.append("focus_on_foundational_skills")
        
        # Learning progress recommendations
        if learning_progress.get("accuracy_trend") == "declining":
            recommendations.append("review_recent_changes_and_approaches")
        
        # Confidence calibration recommendations
        if confidence_calibration.get("status") == "calibrated":
            recommendations.extend(confidence_calibration.get("recommendations", []))
        
        # Capability boundary recommendations
        if len(capability_boundaries) > 2:
            recommendations.append("focus_on_specific_weak_areas")
        
        return recommendations