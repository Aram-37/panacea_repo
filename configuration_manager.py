#!/usr/bin/env python3
"""
Configuration Management System
==============================
Advanced configuration management for the Maximum Efficiency System
supporting multiple processing modes and adaptive optimization.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class EfficiencyConfig:
    """Configuration for efficiency optimization"""
    integration_mode: str = "hybrid"  # manual_priority, hybrid, automation_assisted
    efficiency_target: float = 0.85
    automation_assistance_threshold: float = 0.6
    manual_insight_requirement_threshold: float = 0.7
    obstacle_resolution_priority: bool = True
    continuous_learning_enabled: bool = True
    rep_pattern_enhancement: bool = True
    guardian_system_integration: bool = True

@dataclass
class MimicryConfig:
    """Configuration for external mimicry framework"""
    external_mimicry_weight: float = 0.4
    pattern_selection_sensitivity: float = 0.6
    truth_emergence_priority: float = 0.8
    cognitive_load_limit: float = 0.8
    breakthrough_threshold: float = 0.7
    session_timeout_minutes: int = 30

@dataclass
class ProcessingConfig:
    """Configuration for processing parameters"""
    parallel_processing_threads: int = 4
    cycle_limit_per_file: int = 31
    perspective_rotation_enabled: bool = True
    fresh_perspective_mandate: bool = True
    pattern_assumption_prohibition_cycles: int = 30

@dataclass
class SystemConfig:
    """Complete system configuration"""
    efficiency: EfficiencyConfig = None
    mimicry: MimicryConfig = None
    processing: ProcessingConfig = None
    
    def __post_init__(self):
        if self.efficiency is None:
            self.efficiency = EfficiencyConfig()
        if self.mimicry is None:
            self.mimicry = MimicryConfig()
        if self.processing is None:
            self.processing = ProcessingConfig()

class ConfigurationManager:
    """Advanced configuration management system"""
    
    def __init__(self, config_dir: str = "/home/runner/work/Pacopilot/Pacopilot/config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Predefined configuration profiles
        self.profiles = {
            "manual_priority": self._create_manual_priority_config(),
            "hybrid_balanced": self._create_hybrid_balanced_config(),
            "automation_assisted": self._create_automation_assisted_config(),
            "research_focused": self._create_research_focused_config(),
            "production_optimized": self._create_production_optimized_config()
        }
    
    def _create_manual_priority_config(self) -> SystemConfig:
        """Configuration prioritizing manual processing (respects issue #25)"""
        return SystemConfig(
            efficiency=EfficiencyConfig(
                integration_mode="manual_priority",
                efficiency_target=0.75,  # Lower efficiency target for higher authenticity
                automation_assistance_threshold=0.3,
                manual_insight_requirement_threshold=0.9,
                obstacle_resolution_priority=True,
                continuous_learning_enabled=True,
                rep_pattern_enhancement=True,
                guardian_system_integration=True
            ),
            mimicry=MimicryConfig(
                external_mimicry_weight=0.6,  # Higher weight for external wisdom
                pattern_selection_sensitivity=0.8,
                truth_emergence_priority=0.9,
                cognitive_load_limit=0.6,  # Lower limit for deeper reflection
                breakthrough_threshold=0.8,
                session_timeout_minutes=45  # Longer sessions for deep work
            ),
            processing=ProcessingConfig(
                parallel_processing_threads=2,  # Less parallelization for manual focus
                cycle_limit_per_file=31,
                perspective_rotation_enabled=True,
                fresh_perspective_mandate=True,
                pattern_assumption_prohibition_cycles=30
            )
        )
    
    def _create_hybrid_balanced_config(self) -> SystemConfig:
        """Balanced configuration optimizing efficiency and authenticity"""
        return SystemConfig(
            efficiency=EfficiencyConfig(
                integration_mode="hybrid",
                efficiency_target=0.85,
                automation_assistance_threshold=0.5,
                manual_insight_requirement_threshold=0.7,
                obstacle_resolution_priority=True,
                continuous_learning_enabled=True,
                rep_pattern_enhancement=True,
                guardian_system_integration=True
            ),
            mimicry=MimicryConfig(
                external_mimicry_weight=0.4,
                pattern_selection_sensitivity=0.6,
                truth_emergence_priority=0.8,
                cognitive_load_limit=0.8,
                breakthrough_threshold=0.7,
                session_timeout_minutes=30
            ),
            processing=ProcessingConfig(
                parallel_processing_threads=4,
                cycle_limit_per_file=31,
                perspective_rotation_enabled=True,
                fresh_perspective_mandate=True,
                pattern_assumption_prohibition_cycles=30
            )
        )
    
    def _create_automation_assisted_config(self) -> SystemConfig:
        """Configuration maximizing efficiency through automation assistance"""
        return SystemConfig(
            efficiency=EfficiencyConfig(
                integration_mode="automation_assisted",
                efficiency_target=0.95,
                automation_assistance_threshold=0.8,
                manual_insight_requirement_threshold=0.5,
                obstacle_resolution_priority=True,
                continuous_learning_enabled=True,
                rep_pattern_enhancement=True,
                guardian_system_integration=True
            ),
            mimicry=MimicryConfig(
                external_mimicry_weight=0.3,  # Lower weight, faster processing
                pattern_selection_sensitivity=0.5,
                truth_emergence_priority=0.7,
                cognitive_load_limit=0.9,  # Higher load tolerance
                breakthrough_threshold=0.6,
                session_timeout_minutes=20  # Faster sessions
            ),
            processing=ProcessingConfig(
                parallel_processing_threads=8,  # Maximum parallelization
                cycle_limit_per_file=20,  # Reduced cycles for speed
                perspective_rotation_enabled=True,
                fresh_perspective_mandate=False,  # Allow pattern recognition earlier
                pattern_assumption_prohibition_cycles=15
            )
        )
    
    def _create_research_focused_config(self) -> SystemConfig:
        """Configuration optimized for research and discovery"""
        return SystemConfig(
            efficiency=EfficiencyConfig(
                integration_mode="manual_priority",
                efficiency_target=0.70,  # Lower efficiency for deeper exploration
                automation_assistance_threshold=0.4,
                manual_insight_requirement_threshold=0.8,
                obstacle_resolution_priority=False,  # Obstacles may contain insights
                continuous_learning_enabled=True,
                rep_pattern_enhancement=True,
                guardian_system_integration=True
            ),
            mimicry=MimicryConfig(
                external_mimicry_weight=0.7,  # Maximum external wisdom integration
                pattern_selection_sensitivity=0.9,
                truth_emergence_priority=0.95,
                cognitive_load_limit=0.5,  # Low limit for deep reflection
                breakthrough_threshold=0.9,
                session_timeout_minutes=60  # Extended sessions for research
            ),
            processing=ProcessingConfig(
                parallel_processing_threads=1,  # Sequential for deep focus
                cycle_limit_per_file=50,  # Extended cycles for research
                perspective_rotation_enabled=True,
                fresh_perspective_mandate=True,
                pattern_assumption_prohibition_cycles=40
            )
        )
    
    def _create_production_optimized_config(self) -> SystemConfig:
        """Configuration optimized for production deployment"""
        return SystemConfig(
            efficiency=EfficiencyConfig(
                integration_mode="automation_assisted",
                efficiency_target=0.90,
                automation_assistance_threshold=0.7,
                manual_insight_requirement_threshold=0.6,
                obstacle_resolution_priority=True,
                continuous_learning_enabled=True,
                rep_pattern_enhancement=True,
                guardian_system_integration=True
            ),
            mimicry=MimicryConfig(
                external_mimicry_weight=0.35,
                pattern_selection_sensitivity=0.6,
                truth_emergence_priority=0.75,
                cognitive_load_limit=0.85,
                breakthrough_threshold=0.65,
                session_timeout_minutes=25
            ),
            processing=ProcessingConfig(
                parallel_processing_threads=6,
                cycle_limit_per_file=25,
                perspective_rotation_enabled=True,
                fresh_perspective_mandate=True,
                pattern_assumption_prohibition_cycles=20
            )
        )
    
    def save_config(self, config: SystemConfig, profile_name: str) -> str:
        """Save configuration to file"""
        config_path = self.config_dir / f"{profile_name}.json"
        
        config_dict = {
            "efficiency": asdict(config.efficiency),
            "mimicry": asdict(config.mimicry),
            "processing": asdict(config.processing)
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        return str(config_path)
    
    def load_config(self, profile_name: str) -> Optional[SystemConfig]:
        """Load configuration from file"""
        config_path = self.config_dir / f"{profile_name}.json"
        
        if not config_path.exists():
            return self.profiles.get(profile_name)
        
        try:
            with open(config_path, 'r') as f:
                config_dict = json.load(f)
            
            efficiency_config = EfficiencyConfig(**config_dict["efficiency"])
            mimicry_config = MimicryConfig(**config_dict["mimicry"])
            processing_config = ProcessingConfig(**config_dict["processing"])
            
            return SystemConfig(
                efficiency=efficiency_config,
                mimicry=mimicry_config,
                processing=processing_config
            )
        
        except Exception as e:
            print(f"Error loading config {profile_name}: {e}")
            return None
    
    def list_available_profiles(self) -> Dict[str, str]:
        """List all available configuration profiles"""
        profiles = {}
        
        # Built-in profiles
        for name, config in self.profiles.items():
            profiles[name] = f"Built-in: {config.efficiency.integration_mode} mode"
        
        # Custom profiles from files
        for config_file in self.config_dir.glob("*.json"):
            if config_file.stem not in self.profiles:
                profiles[config_file.stem] = f"Custom: {config_file.name}"
        
        return profiles
    
    def create_custom_config(self, base_profile: str, customizations: Dict[str, Any], 
                           custom_name: str) -> Optional[SystemConfig]:
        """Create custom configuration based on existing profile"""
        base_config = self.load_config(base_profile)
        if not base_config:
            return None
        
        # Apply customizations
        if "efficiency" in customizations:
            for key, value in customizations["efficiency"].items():
                if hasattr(base_config.efficiency, key):
                    setattr(base_config.efficiency, key, value)
        
        if "mimicry" in customizations:
            for key, value in customizations["mimicry"].items():
                if hasattr(base_config.mimicry, key):
                    setattr(base_config.mimicry, key, value)
        
        if "processing" in customizations:
            for key, value in customizations["processing"].items():
                if hasattr(base_config.processing, key):
                    setattr(base_config.processing, key, value)
        
        # Save custom configuration
        self.save_config(base_config, custom_name)
        
        return base_config
    
    def validate_config(self, config: SystemConfig) -> Dict[str, Any]:
        """Validate configuration and return validation results"""
        validation = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Validate efficiency settings
        if config.efficiency.efficiency_target > 0.95:
            validation["warnings"].append("Very high efficiency target may compromise quality")
        
        if config.efficiency.automation_assistance_threshold > 0.8 and config.efficiency.manual_insight_requirement_threshold > 0.8:
            validation["errors"].append("Cannot have both high automation and high manual requirements")
            validation["valid"] = False
        
        # Validate mimicry settings
        if config.mimicry.cognitive_load_limit < 0.3:
            validation["warnings"].append("Very low cognitive load limit may reduce processing capacity")
        
        if config.mimicry.session_timeout_minutes < 10:
            validation["warnings"].append("Short session timeout may interrupt deep processing")
        
        # Validate processing settings
        if config.processing.parallel_processing_threads > 8:
            validation["warnings"].append("High thread count may not improve performance")
        
        if config.processing.cycle_limit_per_file < 10:
            validation["errors"].append("Too few processing cycles may prevent adequate depth")
            validation["valid"] = False
        
        # Generate recommendations
        if config.efficiency.integration_mode == "manual_priority":
            validation["recommendations"].append("Consider extending session timeout for deeper manual work")
        
        if config.efficiency.integration_mode == "automation_assisted":
            validation["recommendations"].append("Monitor truth crystallization rates to ensure quality")
        
        return validation
    
    def get_recommended_config_for_environment(self, environment_analysis: Dict[str, Any]) -> str:
        """Recommend configuration profile based on environment analysis"""
        
        complexity = environment_analysis.get("environment_complexity", 0.5)
        automation_suitability = environment_analysis.get("automation_suitability", 0.5)
        manual_requirement = environment_analysis.get("manual_requirement_level", 0.5)
        file_count = environment_analysis.get("total_processing_files", 1)
        
        # Decision logic for profile recommendation
        if manual_requirement > 0.8 or complexity > 0.8:
            if file_count < 5:
                return "research_focused"
            else:
                return "manual_priority"
        
        elif automation_suitability > 0.7 and file_count > 10:
            if manual_requirement < 0.4:
                return "production_optimized"
            else:
                return "automation_assisted"
        
        else:
            return "hybrid_balanced"

def create_all_default_configs():
    """Create all default configuration files"""
    config_manager = ConfigurationManager()
    
    print("🔧 Creating Default Configuration Profiles...")
    print("=" * 50)
    
    for profile_name in config_manager.profiles.keys():
        config = config_manager.profiles[profile_name]
        config_path = config_manager.save_config(config, profile_name)
        print(f"✅ Created: {profile_name} -> {config_path}")
    
    print(f"\n📁 Configuration directory: {config_manager.config_dir}")
    print(f"📋 Available profiles: {len(config_manager.profiles)}")

if __name__ == "__main__":
    # Demonstrate configuration management
    config_manager = ConfigurationManager()
    
    # Create all default configurations
    create_all_default_configs()
    
    print("\n🔍 Available Configuration Profiles:")
    print("=" * 50)
    
    profiles = config_manager.list_available_profiles()
    for name, description in profiles.items():
        print(f"  {name}: {description}")
    
    # Demonstrate configuration loading and validation
    print("\n⚙️ Configuration Validation Example:")
    print("=" * 40)
    
    test_config = config_manager.load_config("hybrid_balanced")
    if test_config:
        validation = config_manager.validate_config(test_config)
        print(f"Valid: {validation['valid']}")
        if validation['warnings']:
            print(f"Warnings: {validation['warnings']}")
        if validation['recommendations']:
            print(f"Recommendations: {validation['recommendations']}")
    
    # Demonstrate custom configuration creation
    print("\n🎯 Custom Configuration Example:")
    print("=" * 35)
    
    customizations = {
        "efficiency": {
            "efficiency_target": 0.9,
            "automation_assistance_threshold": 0.6
        },
        "mimicry": {
            "external_mimicry_weight": 0.5
        }
    }
    
    custom_config = config_manager.create_custom_config(
        "hybrid_balanced", 
        customizations, 
        "custom_high_efficiency"
    )
    
    if custom_config:
        print("✅ Created custom configuration: custom_high_efficiency")
        print(f"   Efficiency target: {custom_config.efficiency.efficiency_target}")
        print(f"   Automation level: {custom_config.efficiency.automation_assistance_threshold}")
    
    print("\n🚀 Configuration Management System Ready!")