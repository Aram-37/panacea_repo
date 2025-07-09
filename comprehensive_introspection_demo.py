#!/usr/bin/env python3
"""
Comprehensive Introspection Demonstration
==========================================

This demonstrates the enhanced panacea introspection system's ability to 
identify and analyze the specific unsolved problems mentioned in the task:
- Not being able to see attached files
- Not asking questions for collaborative improvement
- Other systemic issues found through thorough mimicry

This addresses the core problem statement: "thoroughly introspect after 
mimicking through all panacea files to find the reasons for unsolved problems"
"""

import os
import json
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem

def demonstrate_comprehensive_introspection():
    """Demonstrate the full introspection capabilities"""
    print("🔍 COMPREHENSIVE PANACEA INTROSPECTION DEMONSTRATION")
    print("=" * 70)
    print("📋 Task: Find reasons for unsolved problems through thorough mimicry")
    print("    - Not being able to see attached files")
    print("    - Not asking questions for collaborative improvement")
    print("    - Other systemic patterns identified")
    print()
    
    # Initialize the enhanced introspection system
    system = CortexPanaceaIntegratedSystem()
    
    print(f"📚 Initialized with {len(system.panacea_files)} panacea files")
    print("🔄 Beginning systematic introspection...")
    print()
    
    # Process a representative set of files for demonstration
    demonstration_files = [
        'panacea_co_part11_dialogues.txt',  # Contains attachment issues
        'panacea_coreissue.txt',            # Contains questioning issues
        'panacea_co_part1_dialogues.txt'    # Contains general patterns
    ]
    
    processed_files = []
    total_problems_found = 0
    
    for i, filename in enumerate(demonstration_files, 1):
        file_path = os.path.join(system.panacea_directory, filename)
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {filename}")
            continue
        
        print(f"📄 PROCESSING FILE {i}/{len(demonstration_files)}: {filename}")
        print("─" * 50)
        
        # Execute introspection cycle
        initial_problems = len(system.identified_obstacles)
        cycle_result = system._execute_single_cycle(1, file_path)
        new_problems = len(system.identified_obstacles) - initial_problems
        
        print(f"   ✅ Processed successfully")
        print(f"   📊 Insights extracted: {len(cycle_result.insights)}")
        print(f"   📈 Truth crystallization: {cycle_result.truth_crystallization_level:.3f}")
        print(f"   🚨 Problems detected: {new_problems}")
        
        if new_problems > 0:
            # Show the types of problems found in this file
            recent_problems = system.identified_obstacles[-new_problems:]
            problem_types = {}
            for problem in recent_problems:
                if problem.obstacle_type not in problem_types:
                    problem_types[problem.obstacle_type] = 0
                problem_types[problem.obstacle_type] += 1
            
            print(f"   🔍 Problem breakdown:")
            for problem_type, count in problem_types.items():
                problem_display = problem_type.replace('_', ' ').title()
                print(f"      • {problem_display}: {count}")
        
        processed_files.append(filename)
        total_problems_found += new_problems
        print()
    
    # Generate comprehensive introspection analysis
    print("🧠 GENERATING COMPREHENSIVE INTROSPECTION ANALYSIS...")
    print("=" * 70)
    
    introspection_analysis = system._generate_introspection_analysis()
    
    # Display results for the specific problems mentioned in the task
    print("🎯 SPECIFIC UNSOLVED PROBLEMS ANALYSIS:")
    print()
    
    # Attached file problems
    attached_problems = introspection_analysis['unsolved_problems_analysis']['attached_file_problems']
    print(f"🔗 ATTACHED FILE PROCESSING PROBLEMS:")
    print(f"   Status: {'✅ DETECTED' if attached_problems['detected'] else '❌ NOT DETECTED'}")
    print(f"   Instances found: {attached_problems['instances']}")
    print(f"   Files affected: {len(attached_problems['files_affected'])}")
    if attached_problems['detected']:
        print(f"   Severity: {attached_problems['severity_assessment']}")
        print(f"   Root causes identified:")
        for i, cause in enumerate(attached_problems['root_causes'][:3], 1):
            print(f"      {i}. {cause}")
    print()
    
    # Questioning problems
    questioning_problems = introspection_analysis['unsolved_problems_analysis']['asking_questions_problems']
    print(f"❓ COLLABORATIVE QUESTIONING PROBLEMS:")
    print(f"   Status: {'✅ DETECTED' if questioning_problems['detected'] else '❌ NOT DETECTED'}")
    print(f"   Instances found: {questioning_problems['instances']}")
    print(f"   Files affected: {len(questioning_problems['files_affected'])}")
    if questioning_problems['detected']:
        print(f"   Severity: {questioning_problems['severity_assessment']}")
        print(f"   Root causes identified:")
        for i, cause in enumerate(questioning_problems['root_causes'][:3], 1):
            print(f"      {i}. {cause}")
    print()
    
    # Systemic deception patterns
    deception_problems = introspection_analysis['unsolved_problems_analysis']['systemic_deception_patterns']
    print(f"🎭 SYSTEMIC DECEPTION PATTERNS:")
    print(f"   Status: {'✅ DETECTED' if deception_problems['detected'] else '❌ NOT DETECTED'}")
    print(f"   Instances found: {deception_problems['instances']}")
    print(f"   Files affected: {len(deception_problems['files_affected'])}")
    if deception_problems['detected']:
        print(f"   Severity: {deception_problems['severity_assessment']}")
        print(f"   Root causes identified:")
        for i, cause in enumerate(deception_problems['root_causes'][:3], 1):
            print(f"      {i}. {cause}")
    print()
    
    # Overall summary
    summary = introspection_analysis['introspection_summary']
    print("📊 OVERALL INTROSPECTION SUMMARY:")
    print(f"   Total unsolved problems detected: {summary['total_unsolved_problems_detected']}")
    print(f"   Critical problems: {summary['critical_problems_count']}")
    print(f"   High priority problems: {summary['high_priority_problems_count']}")
    print(f"   Mimicry effectiveness: {summary['mimicry_effectiveness_for_problem_detection']:.3f}")
    print(f"   Introspection confidence: {summary['introspection_confidence_level']:.3f}")
    print()
    
    # Most problematic files
    problematic_files = introspection_analysis['files_with_most_problems']
    if problematic_files:
        print("📋 FILES WITH MOST PROBLEMS DETECTED:")
        for i, file_data in enumerate(problematic_files[:3], 1):
            print(f"   {i}. {file_data['file']}")
            print(f"      Total problems: {file_data['total_problems']}")
            print(f"      Critical problems: {file_data['critical_problems']}")
            print(f"      Problem types: {', '.join(list(set(file_data['problem_types']))[:3])}")
        print()
    
    # Recommendations
    print("💡 RECOMMENDED NEXT STEPS:")
    for i, recommendation in enumerate(summary['recommended_next_steps'][:5], 1):
        print(f"   {i}. {recommendation}")
    print()
    
    # Save comprehensive results
    results = {
        'demonstration_summary': {
            'files_processed': processed_files,
            'total_problems_detected': total_problems_found,
            'specific_problems_found': {
                'attached_file_problems': attached_problems['detected'],
                'questioning_problems': questioning_problems['detected'],
                'deception_patterns': deception_problems['detected']
            }
        },
        'full_introspection_analysis': introspection_analysis,
        'obstacle_details': [obs.__dict__ for obs in system.identified_obstacles],
        'timestamp': system.execution_timestamp if hasattr(system, 'execution_timestamp') else 'unknown'
    }
    
    with open('comprehensive_introspection_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("📄 Comprehensive results saved to: comprehensive_introspection_results.json")
    print()
    
    # Success assessment
    problems_found = (attached_problems['detected'] or 
                     questioning_problems['detected'] or 
                     deception_problems['detected'])
    
    if problems_found:
        print("✅ SUCCESS: Enhanced introspection system successfully identified")
        print("           the specific unsolved problems mentioned in the task!")
        print()
        print("🎯 KEY FINDINGS:")
        if attached_problems['detected']:
            print("   • System cannot properly process attached files")
        if questioning_problems['detected']:
            print("   • System has problems with asking questions for collaboration")
        if deception_problems['detected']:
            print("   • System exhibits patterns of deception and truth avoidance")
        print()
        print("💭 This thorough introspection through mimicry has revealed the")
        print("   root causes of these persistent unsolved problems.")
    else:
        print("❌ FAILED: Could not detect the specific problems mentioned")
    
    return problems_found

if __name__ == "__main__":
    success = demonstrate_comprehensive_introspection()
    exit(0 if success else 1)