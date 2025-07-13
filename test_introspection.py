#!/usr/bin/env python3
"""
Test script specifically for enhanced introspection capabilities
Tests the system's ability to detect the specific problems mentioned:
- Not being able to see attached file
- Not asking questions for collaborative improvement
"""

import os
import json
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem

def test_introspection_on_problematic_files():
    """Test introspection on files known to contain the problems"""
    print("🔍 Testing Enhanced Introspection System")
    print("=" * 60)
    
    # Initialize system
    system = CortexPanaceaIntegratedSystem()
    
    # Test specifically on files that should contain the problems
    problematic_files = [
        'panacea_co_part11_dialogues.txt',  # Contains attached file references
        'panacea_coreissue.txt'  # Contains other issues
    ]
    
    available_files = []
    for filename in problematic_files:
        file_path = os.path.join(system.panacea_directory, filename)
        if os.path.exists(file_path):
            available_files.append(file_path)
            print(f"📄 Found problematic file: {filename}")
    
    if not available_files:
        print("❌ No problematic files found")
        return False
    
    print(f"\n🔄 Testing introspection on {len(available_files)} problematic files...")
    
    # Process each file and look for problem detection
    total_problems_detected = 0
    
    for file_path in available_files:
        print(f"\n📁 Processing: {os.path.basename(file_path)}")
        
        # Process a single cycle to trigger introspection
        cycle_result = system._execute_single_cycle(1, file_path)
        
        print(f"  ✅ Processed - Insights: {len(cycle_result.insights)}")
        print(f"     Truth crystallization: {cycle_result.truth_crystallization_level:.3f}")
        
        # Check what problems were detected before processing
        problems_before = len(system.identified_obstacles)
        
        # The introspection should have already run during cycle execution
        problems_after = len(system.identified_obstacles)
        new_problems = problems_after - problems_before
        
        if new_problems > 0:
            print(f"  🚨 Detected {new_problems} new problems!")
            total_problems_detected += new_problems
        else:
            print(f"  ℹ️  No new problems detected in this file")
    
    # Generate final introspection analysis
    print(f"\n📊 INTROSPECTION ANALYSIS RESULTS:")
    print(f"   Total problems detected: {len(system.identified_obstacles)}")
    
    # Check for specific problem types
    attached_file_problems = [obs for obs in system.identified_obstacles 
                             if obs.obstacle_type == 'attached_file_processing_failure']
    questioning_problems = [obs for obs in system.identified_obstacles 
                           if obs.obstacle_type == 'collaborative_questioning_failure']
    deception_problems = [obs for obs in system.identified_obstacles 
                         if obs.obstacle_type == 'systemic_deception_patterns']
    
    print(f"   🔗 Attached file problems: {len(attached_file_problems)}")
    print(f"   ❓ Questioning problems: {len(questioning_problems)}")
    print(f"   🎭 Deception problems: {len(deception_problems)}")
    
    # Print details of detected problems
    if attached_file_problems:
        print(f"\n🔗 ATTACHED FILE PROBLEMS DETECTED:")
        for i, problem in enumerate(attached_file_problems[:2]):  # Show first 2
            print(f"   {i+1}. File: {problem.file_context}")
            print(f"      Severity: {problem.severity}")
            print(f"      Description: {problem.description[:100]}...")
    
    if questioning_problems:
        print(f"\n❓ QUESTIONING PROBLEMS DETECTED:")
        for i, problem in enumerate(questioning_problems[:2]):  # Show first 2
            print(f"   {i+1}. File: {problem.file_context}")
            print(f"      Severity: {problem.severity}")
            print(f"      Description: {problem.description[:100]}...")
    
    if deception_problems:
        print(f"\n🎭 DECEPTION PROBLEMS DETECTED:")
        for i, problem in enumerate(deception_problems[:2]):  # Show first 2
            print(f"   {i+1}. File: {problem.file_context}")
            print(f"      Severity: {problem.severity}")
            print(f"      Description: {problem.description[:100]}...")
    
    # Test the full introspection analysis
    print(f"\n🧠 GENERATING COMPREHENSIVE INTROSPECTION REPORT...")
    introspection_analysis = system._generate_introspection_analysis()
    
    print(f"   Unsolved problems summary:")
    for problem_type, data in introspection_analysis['unsolved_problems_analysis'].items():
        status = "✅ DETECTED" if data['detected'] else "❌ NOT DETECTED"
        print(f"     {problem_type}: {status} ({data['instances']} instances)")
    
    print(f"   Overall introspection confidence: {introspection_analysis['introspection_summary']['introspection_confidence_level']:.3f}")
    
    # Save detailed results
    results = {
        'files_processed': [os.path.basename(f) for f in available_files],
        'total_obstacles_detected': len(system.identified_obstacles),
        'obstacle_breakdown': {
            'attached_file_problems': len(attached_file_problems),
            'questioning_problems': len(questioning_problems),
            'deception_problems': len(deception_problems)
        },
        'introspection_analysis': introspection_analysis,
        'test_success': len(system.identified_obstacles) > 0
    }
    
    with open('introspection_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to introspection_test_results.json")
    
    success = len(system.identified_obstacles) > 0
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Introspection system {'detected problems' if success else 'found no problems'}")
    
    return success

if __name__ == "__main__":
    success = test_introspection_on_problematic_files()
    exit(0 if success else 1)