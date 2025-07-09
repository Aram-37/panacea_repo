#!/usr/bin/env python3
"""
Continuous Monitoring and Optimization System
=============================================
Real-time monitoring and adaptive optimization for the Maximum Efficiency System.
Provides continuous performance tracking, adaptive configuration adjustment,
and real-time efficiency optimization.
"""

import time
import json
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
import statistics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Individual performance metric measurement"""
    timestamp: datetime
    metric_name: str
    value: float
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemSnapshot:
    """System performance snapshot at a point in time"""
    timestamp: datetime
    processing_efficiency: float
    truth_crystallization_rate: float
    obstacle_resolution_effectiveness: float
    external_mimicry_success_rate: float
    automation_manual_balance: float
    active_sessions: int
    memory_usage_mb: float
    cpu_usage_percent: float

@dataclass
class AdaptiveAdjustment:
    """Adaptive system adjustment"""
    timestamp: datetime
    adjustment_type: str  # "config_change", "threshold_adjustment", "mode_switch"
    previous_value: Any
    new_value: Any
    reason: str
    expected_impact: str

class ContinuousMonitor:
    """Continuous monitoring system for performance tracking"""
    
    def __init__(self, monitoring_interval: float = 5.0, history_size: int = 1000):
        self.monitoring_interval = monitoring_interval
        self.history_size = history_size
        
        # Performance history
        self.performance_history: deque = deque(maxlen=history_size)
        self.metrics_history: Dict[str, deque] = {}
        self.system_snapshots: deque = deque(maxlen=history_size)
        
        # Monitoring control
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Performance thresholds
        self.thresholds = {
            "efficiency_warning": 0.6,
            "efficiency_critical": 0.4,
            "truth_crystallization_warning": 0.5,
            "truth_crystallization_critical": 0.3,
            "response_time_warning": 30.0,  # seconds
            "response_time_critical": 60.0,
            "memory_warning": 500.0,  # MB
            "memory_critical": 1000.0
        }
        
        # Alert callbacks
        self.alert_callbacks: List[Callable] = []
        
        logger.info("🔍 Continuous Monitor initialized")
    
    def add_alert_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add callback for performance alerts"""
        self.alert_callbacks.append(callback)
    
    def record_metric(self, metric_name: str, value: float, context: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            context=context or {}
        )
        
        if metric_name not in self.metrics_history:
            self.metrics_history[metric_name] = deque(maxlen=self.history_size)
        
        self.metrics_history[metric_name].append(metric)
        
        # Check thresholds
        self._check_metric_thresholds(metric)
    
    def record_system_snapshot(self, snapshot: SystemSnapshot):
        """Record complete system snapshot"""
        self.system_snapshots.append(snapshot)
        
        # Record individual metrics
        self.record_metric("processing_efficiency", snapshot.processing_efficiency)
        self.record_metric("truth_crystallization_rate", snapshot.truth_crystallization_rate)
        self.record_metric("automation_manual_balance", snapshot.automation_manual_balance)
        self.record_metric("memory_usage_mb", snapshot.memory_usage_mb)
    
    def _check_metric_thresholds(self, metric: PerformanceMetric):
        """Check if metric violates thresholds and trigger alerts"""
        metric_name = metric.metric_name
        value = metric.value
        
        # Check efficiency thresholds
        if metric_name == "processing_efficiency":
            if value < self.thresholds["efficiency_critical"]:
                self._trigger_alert("CRITICAL", f"Processing efficiency critical: {value:.2f}")
            elif value < self.thresholds["efficiency_warning"]:
                self._trigger_alert("WARNING", f"Processing efficiency warning: {value:.2f}")
        
        # Check truth crystallization thresholds
        elif metric_name == "truth_crystallization_rate":
            if value < self.thresholds["truth_crystallization_critical"]:
                self._trigger_alert("CRITICAL", f"Truth crystallization critical: {value:.2f}")
            elif value < self.thresholds["truth_crystallization_warning"]:
                self._trigger_alert("WARNING", f"Truth crystallization warning: {value:.2f}")
        
        # Check memory thresholds
        elif metric_name == "memory_usage_mb":
            if value > self.thresholds["memory_critical"]:
                self._trigger_alert("CRITICAL", f"Memory usage critical: {value:.1f}MB")
            elif value > self.thresholds["memory_warning"]:
                self._trigger_alert("WARNING", f"Memory usage warning: {value:.1f}MB")
    
    def _trigger_alert(self, severity: str, message: str):
        """Trigger performance alert"""
        alert_data = {
            "severity": severity,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "system_state": self.get_current_performance_summary()
        }
        
        logger.warning(f"🚨 {severity}: {message}")
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(severity, alert_data)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("🔄 Continuous monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        logger.info("⏹️ Continuous monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                snapshot = self._collect_system_snapshot()
                self.record_system_snapshot(snapshot)
                
                # Sleep until next monitoring interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_snapshot(self) -> SystemSnapshot:
        """Collect current system performance snapshot"""
        import psutil
        
        # Get system resource usage
        memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # MB
        cpu_usage = psutil.cpu_percent()
        
        # Calculate performance metrics from recent history
        recent_efficiency = self._get_recent_average("processing_efficiency", minutes=5)
        recent_truth_rate = self._get_recent_average("truth_crystallization_rate", minutes=5)
        recent_balance = self._get_recent_average("automation_manual_balance", minutes=5)
        
        return SystemSnapshot(
            timestamp=datetime.now(),
            processing_efficiency=recent_efficiency or 0.0,
            truth_crystallization_rate=recent_truth_rate or 0.0,
            obstacle_resolution_effectiveness=0.8,  # Placeholder
            external_mimicry_success_rate=0.7,  # Placeholder
            automation_manual_balance=recent_balance or 0.5,
            active_sessions=1,  # Placeholder
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    def _get_recent_average(self, metric_name: str, minutes: int = 5) -> Optional[float]:
        """Get average of metric over recent time period"""
        if metric_name not in self.metrics_history:
            return None
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_values = [
            metric.value for metric in self.metrics_history[metric_name]
            if metric.timestamp >= cutoff_time
        ]
        
        if not recent_values:
            return None
        
        return statistics.mean(recent_values)
    
    def get_current_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "monitoring_active": self.monitoring_active,
            "total_snapshots": len(self.system_snapshots),
        }
        
        # Add recent averages for key metrics
        for metric_name in ["processing_efficiency", "truth_crystallization_rate", "automation_manual_balance"]:
            recent_avg = self._get_recent_average(metric_name, minutes=10)
            if recent_avg is not None:
                summary[f"recent_{metric_name}"] = recent_avg
        
        # Add latest system snapshot if available
        if self.system_snapshots:
            latest = self.system_snapshots[-1]
            summary["latest_snapshot"] = {
                "memory_usage_mb": latest.memory_usage_mb,
                "cpu_usage_percent": latest.cpu_usage_percent,
                "active_sessions": latest.active_sessions
            }
        
        return summary

class AdaptiveOptimizer:
    """Adaptive optimization system for continuous improvement"""
    
    def __init__(self, monitor: ContinuousMonitor):
        self.monitor = monitor
        self.adjustment_history: deque = deque(maxlen=500)
        
        # Optimization parameters
        self.optimization_interval = 30.0  # seconds
        self.optimization_active = False
        self.optimizer_thread: Optional[threading.Thread] = None
        
        # Performance targets
        self.targets = {
            "efficiency_target": 0.85,
            "truth_crystallization_target": 0.8,
            "response_time_target": 20.0,
            "balance_tolerance": 0.1
        }
        
        # Adjustment strategies
        self.adjustment_strategies = {
            "low_efficiency": self._adjust_for_low_efficiency,
            "low_truth_crystallization": self._adjust_for_low_truth_crystallization,
            "high_response_time": self._adjust_for_high_response_time,
            "imbalanced_automation": self._adjust_automation_balance
        }
        
        logger.info("🎯 Adaptive Optimizer initialized")
    
    def start_optimization(self):
        """Start adaptive optimization"""
        if self.optimization_active:
            return
        
        self.optimization_active = True
        self.optimizer_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimizer_thread.start()
        
        logger.info("🔄 Adaptive optimization started")
    
    def stop_optimization(self):
        """Stop adaptive optimization"""
        self.optimization_active = False
        if self.optimizer_thread:
            self.optimizer_thread.join(timeout=5.0)
        
        logger.info("⏹️ Adaptive optimization stopped")
    
    def _optimization_loop(self):
        """Main optimization loop"""
        while self.optimization_active:
            try:
                # Analyze current performance
                performance_summary = self.monitor.get_current_performance_summary()
                
                # Identify optimization opportunities
                adjustments = self._identify_optimization_opportunities(performance_summary)
                
                # Apply adjustments
                for adjustment in adjustments:
                    self._apply_adjustment(adjustment)
                
                # Sleep until next optimization cycle
                time.sleep(self.optimization_interval)
                
            except Exception as e:
                logger.error(f"Optimization loop error: {e}")
                time.sleep(self.optimization_interval)
    
    def _identify_optimization_opportunities(self, performance_summary: Dict[str, Any]) -> List[str]:
        """Identify optimization opportunities based on performance"""
        opportunities = []
        
        # Check efficiency
        recent_efficiency = performance_summary.get("recent_processing_efficiency")
        if recent_efficiency and recent_efficiency < self.targets["efficiency_target"]:
            opportunities.append("low_efficiency")
        
        # Check truth crystallization
        recent_truth = performance_summary.get("recent_truth_crystallization_rate")
        if recent_truth and recent_truth < self.targets["truth_crystallization_target"]:
            opportunities.append("low_truth_crystallization")
        
        # Check automation balance
        recent_balance = performance_summary.get("recent_automation_manual_balance")
        if recent_balance:
            if abs(recent_balance - 0.5) > self.targets["balance_tolerance"]:
                opportunities.append("imbalanced_automation")
        
        return opportunities
    
    def _apply_adjustment(self, adjustment_type: str):
        """Apply specific adjustment strategy"""
        if adjustment_type in self.adjustment_strategies:
            try:
                adjustment = self.adjustment_strategies[adjustment_type]()
                if adjustment:
                    self.adjustment_history.append(adjustment)
                    logger.info(f"🔧 Applied adjustment: {adjustment.adjustment_type} - {adjustment.reason}")
            except Exception as e:
                logger.error(f"Adjustment application error: {e}")
    
    def _adjust_for_low_efficiency(self) -> Optional[AdaptiveAdjustment]:
        """Adjust system for low efficiency"""
        # Strategy: Increase automation assistance slightly
        current_balance = self.monitor._get_recent_average("automation_manual_balance", minutes=10)
        if current_balance is None:
            return None
        
        new_balance = min(0.9, current_balance + 0.1)
        
        return AdaptiveAdjustment(
            timestamp=datetime.now(),
            adjustment_type="automation_increase",
            previous_value=current_balance,
            new_value=new_balance,
            reason="Low processing efficiency detected",
            expected_impact="Increase processing speed through automation"
        )
    
    def _adjust_for_low_truth_crystallization(self) -> Optional[AdaptiveAdjustment]:
        """Adjust system for low truth crystallization"""
        # Strategy: Increase manual insight requirement
        current_balance = self.monitor._get_recent_average("automation_manual_balance", minutes=10)
        if current_balance is None:
            return None
        
        new_balance = max(0.1, current_balance - 0.1)
        
        return AdaptiveAdjustment(
            timestamp=datetime.now(),
            adjustment_type="manual_increase",
            previous_value=current_balance,
            new_value=new_balance,
            reason="Low truth crystallization rate detected",
            expected_impact="Increase depth through manual insight"
        )
    
    def _adjust_for_high_response_time(self) -> Optional[AdaptiveAdjustment]:
        """Adjust system for high response time"""
        # Strategy: Reduce processing cycles or increase parallelization
        return AdaptiveAdjustment(
            timestamp=datetime.now(),
            adjustment_type="performance_optimization",
            previous_value="standard_cycles",
            new_value="reduced_cycles",
            reason="High response time detected",
            expected_impact="Reduce processing time while maintaining quality"
        )
    
    def _adjust_automation_balance(self) -> Optional[AdaptiveAdjustment]:
        """Adjust automation-manual balance"""
        current_balance = self.monitor._get_recent_average("automation_manual_balance", minutes=10)
        if current_balance is None:
            return None
        
        # Move balance toward target (0.5)
        target_balance = 0.5
        adjustment_factor = 0.05
        
        if current_balance > target_balance:
            new_balance = current_balance - adjustment_factor
        else:
            new_balance = current_balance + adjustment_factor
        
        return AdaptiveAdjustment(
            timestamp=datetime.now(),
            adjustment_type="balance_adjustment",
            previous_value=current_balance,
            new_value=new_balance,
            reason="Automation-manual balance optimization",
            expected_impact="Optimize balance between efficiency and authenticity"
        )
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        return {
            "optimization_active": self.optimization_active,
            "total_adjustments": len(self.adjustment_history),
            "recent_adjustments": [
                {
                    "timestamp": adj.timestamp.isoformat(),
                    "type": adj.adjustment_type,
                    "reason": adj.reason,
                    "impact": adj.expected_impact
                }
                for adj in list(self.adjustment_history)[-5:]  # Last 5 adjustments
            ],
            "current_targets": self.targets,
            "performance_trends": self._calculate_performance_trends()
        }
    
    def _calculate_performance_trends(self) -> Dict[str, str]:
        """Calculate performance trends over time"""
        trends = {}
        
        # Analyze trends for key metrics
        for metric_name in ["processing_efficiency", "truth_crystallization_rate"]:
            recent_values = []
            if metric_name in self.monitor.metrics_history:
                recent_time = datetime.now() - timedelta(minutes=30)
                recent_values = [
                    metric.value for metric in self.monitor.metrics_history[metric_name]
                    if metric.timestamp >= recent_time
                ]
            
            if len(recent_values) >= 3:
                # Simple trend calculation
                first_half = statistics.mean(recent_values[:len(recent_values)//2])
                second_half = statistics.mean(recent_values[len(recent_values)//2:])
                
                if second_half > first_half * 1.05:
                    trends[metric_name] = "improving"
                elif second_half < first_half * 0.95:
                    trends[metric_name] = "declining"
                else:
                    trends[metric_name] = "stable"
            else:
                trends[metric_name] = "insufficient_data"
        
        return trends

class ContinuousOptimizationSystem:
    """Complete continuous monitoring and optimization system"""
    
    def __init__(self, monitoring_interval: float = 5.0, optimization_interval: float = 30.0):
        self.monitor = ContinuousMonitor(monitoring_interval)
        self.optimizer = AdaptiveOptimizer(self.monitor)
        
        # System control
        self.system_active = False
        
        # Setup alert handling
        self.monitor.add_alert_callback(self._handle_performance_alert)
        
        logger.info("🚀 Continuous Optimization System initialized")
    
    def start_system(self):
        """Start complete monitoring and optimization system"""
        self.system_active = True
        self.monitor.start_monitoring()
        self.optimizer.start_optimization()
        
        logger.info("🔄 Continuous Optimization System started")
    
    def stop_system(self):
        """Stop complete monitoring and optimization system"""
        self.system_active = False
        self.optimizer.stop_optimization()
        self.monitor.stop_monitoring()
        
        logger.info("⏹️ Continuous Optimization System stopped")
    
    def _handle_performance_alert(self, severity: str, alert_data: Dict[str, Any]):
        """Handle performance alerts"""
        if severity == "CRITICAL":
            # Trigger immediate optimization
            logger.warning("🚨 CRITICAL alert received - triggering immediate optimization")
            
            # Force optimization cycle
            if self.optimizer.optimization_active:
                performance_summary = self.monitor.get_current_performance_summary()
                opportunities = self.optimizer._identify_optimization_opportunities(performance_summary)
                
                for opportunity in opportunities:
                    self.optimizer._apply_adjustment(opportunity)
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Get comprehensive system report"""
        return {
            "system_status": {
                "active": self.system_active,
                "monitoring_active": self.monitor.monitoring_active,
                "optimization_active": self.optimizer.optimization_active
            },
            "performance_summary": self.monitor.get_current_performance_summary(),
            "optimization_report": self.optimizer.get_optimization_report(),
            "system_health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health"""
        health = {
            "overall_status": "healthy",
            "issues": [],
            "recommendations": []
        }
        
        # Check recent performance
        performance = self.monitor.get_current_performance_summary()
        
        recent_efficiency = performance.get("recent_processing_efficiency")
        if recent_efficiency and recent_efficiency < 0.6:
            health["overall_status"] = "degraded"
            health["issues"].append("Low processing efficiency")
            health["recommendations"].append("Consider increasing automation assistance")
        
        recent_truth = performance.get("recent_truth_crystallization_rate")
        if recent_truth and recent_truth < 0.5:
            health["overall_status"] = "degraded"
            health["issues"].append("Low truth crystallization rate")
            health["recommendations"].append("Increase manual insight requirements")
        
        # Check system resources
        if "latest_snapshot" in performance:
            snapshot = performance["latest_snapshot"]
            if snapshot["memory_usage_mb"] > 800:
                health["issues"].append("High memory usage")
                health["recommendations"].append("Consider reducing parallel processing")
        
        return health

def run_continuous_optimization_demo():
    """Demonstrate continuous optimization system"""
    import psutil
    
    print("🚀 Starting Continuous Optimization System Demo")
    print("=" * 50)
    
    # Create and start system
    system = ContinuousOptimizationSystem(monitoring_interval=2.0, optimization_interval=10.0)
    system.start_system()
    
    try:
        # Simulate system usage with metrics
        for i in range(20):
            # Simulate varying performance metrics
            efficiency = 0.7 + (i % 5) * 0.05  # Varies from 0.7 to 0.9
            truth_rate = 0.6 + (i % 3) * 0.1   # Varies from 0.6 to 0.8
            balance = 0.4 + (i % 4) * 0.05     # Varies from 0.4 to 0.55
            
            # Record metrics
            system.monitor.record_metric("processing_efficiency", efficiency)
            system.monitor.record_metric("truth_crystallization_rate", truth_rate)
            system.monitor.record_metric("automation_manual_balance", balance)
            
            print(f"📊 Iteration {i+1}: Efficiency={efficiency:.2f}, Truth={truth_rate:.2f}, Balance={balance:.2f}")
            
            time.sleep(1)
        
        # Get final report
        print("\n📋 Final System Report:")
        print("=" * 30)
        
        report = system.get_comprehensive_report()
        
        print(f"System Status: {report['system_status']['active']}")
        print(f"Total Snapshots: {report['performance_summary']['total_snapshots']}")
        print(f"Total Adjustments: {report['optimization_report']['total_adjustments']}")
        print(f"System Health: {report['system_health']['overall_status']}")
        
        if report['optimization_report']['recent_adjustments']:
            print("\nRecent Adjustments:")
            for adj in report['optimization_report']['recent_adjustments']:
                print(f"  - {adj['type']}: {adj['reason']}")
        
        if report['system_health']['recommendations']:
            print("\nRecommendations:")
            for rec in report['system_health']['recommendations']:
                print(f"  - {rec}")
        
    finally:
        system.stop_system()
        print("\n✅ Continuous Optimization System Demo completed")

if __name__ == "__main__":
    # Check if psutil is available, if not use mock
    try:
        import psutil
    except ImportError:
        print("⚠️ psutil not available, using mock system metrics")
        
        # Mock psutil for demo
        class MockPsutil:
            class VirtualMemory:
                def __init__(self):
                    self.used = 400 * 1024 * 1024  # 400 MB
                    
            @staticmethod
            def virtual_memory():
                return MockPsutil.VirtualMemory()
            
            @staticmethod
            def cpu_percent():
                return 25.0
        
        import sys
        sys.modules['psutil'] = MockPsutil()
    
    run_continuous_optimization_demo()