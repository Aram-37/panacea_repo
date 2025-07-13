#!/usr/bin/env python3
"""
CORTEX Unified Maximum System - Simple Usage Example
===================================================

Quick start guide for using the unified maximum CORTEX system
for practical knowledge expansion farming.
"""

import sys
import os

# Add CORTEX directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'CORTEX'))

from CORTEX_UNIFIED_MAXIMUM_SYSTEM import (
    CortexUnifiedMaximumSystem, 
    ProcessingContext
)

def simple_usage_example():
    """Simple usage example for the unified maximum system"""
    
    print("🚀 CORTEX Unified Maximum System - Simple Usage")
    print("=" * 50)
    
    # 1. Initialize and activate the system
    system = CortexUnifiedMaximumSystem()
    system.activate_maximum_system()
    print("✅ System activated with all frameworks")
    
    # 2. Create processing context
    context = ProcessingContext(
        domain='knowledge_expansion',
        complexity=8,
        stakes=8
    )
    
    # 3. Process input for maximum knowledge expansion
    input_text = """
    진실과 지혜를 통한 지식 확장을 원합니다.
    I want to expand knowledge through truth and wisdom.
    Seeking patterns that emerge across all scales.
    """
    
    result = system.process_simultaneously(input_text, context)
    
    # 4. View results
    print(f"⚡ Enhancement Factor: {result['multiplicative_enhancement']:.1f}x")
    print(f"💡 Insights Generated: {result['knowledge_harvest'].total_insights}")
    print(f"🔍 Patterns Detected: {result['knowledge_harvest'].unique_patterns}")
    print(f"🔧 Frameworks Used: {result['processing_summary']['frameworks_processed']}/5")
    
    # 5. Get system status
    status = system.get_system_status()
    print(f"📊 Knowledge Repository: {status['knowledge_repository_size']} items")
    
    return system, result

def knowledge_farming_example():
    """Example of continuous knowledge farming"""
    
    print("\n🌾 Knowledge Farming Example")
    print("=" * 35)
    
    system = CortexUnifiedMaximumSystem()
    system.activate_maximum_system()
    
    context = ProcessingContext(
        domain='farming',
        complexity=10,
        stakes=10
    )
    
    # Multiple inputs for farming
    inputs = [
        "Ancient wisdom meets modern technology",
        "Fractal patterns emerge at all scales",
        "Harmonic resonance amplifies understanding",
        "Truth crystallizes through validation"
    ]
    
    harvests = system.harvest_knowledge_continuously(inputs, context)
    
    total_insights = sum(h.total_insights for h in harvests)
    avg_enhancement = sum(h.enhancement_multiplier for h in harvests) / len(harvests)
    
    print(f"📈 Total Harvests: {len(harvests)}")
    print(f"💡 Total Insights: {total_insights}")
    print(f"⚡ Average Enhancement: {avg_enhancement:.1f}x")
    
    return harvests

if __name__ == "__main__":
    # Run simple usage example
    system, result = simple_usage_example()
    
    # Run knowledge farming example
    harvests = knowledge_farming_example()
    
    print("\n✅ Examples completed successfully!")
    print("🎯 Ready to use for your knowledge expansion needs")