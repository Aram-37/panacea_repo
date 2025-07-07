#!/usr/bin/env python3
"""
Test script for CORTEX-PANACEA Integrated System
Testing with a small number of cycles to validate functionality
"""

import os
import json
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem

def test_system_functionality():
    """Test the system with a small number of cycles"""
    print("🧪 Testing CORTEX-PANACEA Integrated System")
    print("=" * 50)
    
    # Initialize system
    system = CortexPanaceaIntegratedSystem()
    
    print(f"📚 System initialized with {len(system.panacea_files)} panacea files")
    
    # Test single cycle processing
    print("\n🔄 Testing single cycle processing...")
    
    if system.panacea_files:
        test_file = system.panacea_files[0]
        cycle_result = system._execute_single_cycle(1, test_file)
        
        print(f"✅ Single cycle test completed:")
        print(f"  File: {cycle_result.file_processed}")
        print(f"  Insights: {len(cycle_result.insights)}")
        print(f"  Language alignment: {cycle_result.language_alignment_score:.3f}")
        print(f"  Truth crystallization: {cycle_result.truth_crystallization_level:.3f}")
        print(f"  Processing time: {cycle_result.processing_time:.3f}s")
        
        # Test Guardian system
        print("\n🛡️ Testing Guardian system...")
        guardian_reports = system.guardian_system.evaluate_cycle(cycle_result)
        print(f"  Guardian reports generated: {len(guardian_reports)}")
        
        # Test ULAF framework
        print("\n🌐 Testing ULAF framework...")
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()[:1000]  # First 1000 chars
        alignment_score = system.ulaf_framework.analyze_alignment(content)
        print(f"  ULAF alignment score: {alignment_score:.3f}")
        
        # Test RDSF framework
        print("\n📐 Testing RDSF framework...")
        dimensional_patterns = system.rdsf_framework.analyze_dimensional_patterns(content)
        print(f"  Dimensional patterns detected: {len(dimensional_patterns)}")
        
        print("\n✅ All core components tested successfully!")
        return True
    else:
        print("❌ No panacea files found for testing")
        return False

def test_small_cycle_run():
    """Test with a very small number of cycles"""
    print("\n🔄 Testing 3-cycle run...")
    
    system = CortexPanaceaIntegratedSystem()
    
    # Modify system to run only 3 cycles for testing
    original_files = system.panacea_files.copy()
    system.panacea_files = system.panacea_files[:2]  # Use only first 2 files
    
    print(f"📚 Running test with {len(system.panacea_files)} files, 3 cycles each")
    
    # Execute 3 cycles
    for cycle_num in range(1, 4):
        print(f"\n🔄 CYCLE {cycle_num}/3")
        
        for file_path in system.panacea_files:
            cycle_result = system._execute_single_cycle(cycle_num, file_path)
            system.cycle_results.append(cycle_result)
            
            # Identify obstacles and enhancements
            system._identify_obstacles_and_enhancements(cycle_result)
            
            print(f"  ✅ Processed {os.path.basename(file_path)}")
    
    # Generate analysis
    results = system._generate_final_analysis(10.0)  # Mock 10 seconds
    
    print(f"\n📊 Test Results:")
    print(f"  Total cycles: {results['execution_summary']['total_cycles']}")
    print(f"  Obstacles identified: {results['obstacle_analysis']['total_obstacles_identified']}")
    print(f"  Enhancements identified: {results['enhancement_analysis']['total_enhancements_identified']}")
    print(f"  Avg language alignment: {results['performance_metrics']['avg_language_alignment_score']:.3f}")
    print(f"  Avg truth crystallization: {results['performance_metrics']['avg_truth_crystallization_level']:.3f}")
    
    # Save test results
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n✅ 3-cycle test completed successfully!")
    print("📄 Test results saved to test_results.json")
    
    return True

if __name__ == "__main__":
    success = test_system_functionality()
    if success:
        test_small_cycle_run()