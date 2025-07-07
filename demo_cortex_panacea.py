#!/usr/bin/env python3
"""
Demonstration of CORTEX-PANACEA Integrated System
=================================================

This script demonstrates the full system with a realistic small-scale run
to show all components working together while being efficient for testing.
"""

import os
import json
import time
from datetime import datetime
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem

def demonstrate_cortex_panacea_system():
    """Demonstrate the system with a 5-cycle run across 3 files"""
    
    print("🎯 CORTEX-PANACEA Integrated System Demonstration")
    print("=" * 60)
    print("This demonstrates the full 31-cycle capability with a smaller test run")
    print()
    
    # Initialize system
    system = CortexPanaceaIntegratedSystem()
    
    print(f"📚 System Status:")
    print(f"  - Total panacea files discovered: {len(system.panacea_files)}")
    print(f"  - Guardian system: {len(system.guardian_system.guardians)} guardians active")
    print(f"  - ULAF framework: {len(system.ulaf_framework.layers)} language layers")
    print(f"  - RDSF framework: {len(system.rdsf_framework.scales)} dimensional scales")
    print()
    
    # Show discovered files
    print("📄 Discovered Panacea Files:")
    for i, file_path in enumerate(system.panacea_files[:10], 1):
        print(f"  {i:2d}. {os.path.basename(file_path)}")
    if len(system.panacea_files) > 10:
        print(f"  ... and {len(system.panacea_files) - 10} more files")
    print()
    
    # For demonstration, run with first 3 files and 5 cycles
    demo_files = system.panacea_files[:3]
    demo_cycles = 5
    
    print(f"🔄 Running demonstration with {len(demo_files)} files × {demo_cycles} cycles = {len(demo_files) * demo_cycles} total processing cycles")
    print()
    
    start_time = time.time()
    
    # Execute cycles
    for cycle_num in range(1, demo_cycles + 1):
        print(f"🔄 CYCLE {cycle_num}/{demo_cycles}")
        
        for file_path in demo_files:
            file_name = os.path.basename(file_path)
            
            # Execute single cycle
            cycle_result = system._execute_single_cycle(cycle_num, file_path)
            system.cycle_results.append(cycle_result)
            
            # Identify obstacles and enhancements
            system._identify_obstacles_and_enhancements(cycle_result)
            
            # Show progress
            print(f"  ✅ {file_name}")
            print(f"     Insights: {len(cycle_result.insights)}, "
                  f"Language: {cycle_result.language_alignment_score:.3f}, "
                  f"Truth: {cycle_result.truth_crystallization_level:.3f}")
        
        print()
    
    # Generate final analysis
    total_time = time.time() - start_time
    results = system._generate_final_analysis(total_time)
    
    # Display results
    print("📊 DEMONSTRATION RESULTS")
    print("=" * 30)
    
    exec_summary = results['execution_summary']
    perf_metrics = results['performance_metrics']
    obstacle_analysis = results['obstacle_analysis']
    enhancement_analysis = results['enhancement_analysis']
    
    print(f"🎯 Execution Summary:")
    print(f"  Total cycles executed: {exec_summary['total_cycles']}")
    print(f"  Files processed: {exec_summary['total_files_processed']}")
    print(f"  Total processing time: {exec_summary['total_processing_time']:.2f} seconds")
    print(f"  Average time per cycle: {exec_summary['avg_processing_time_per_cycle']:.2f} seconds")
    print()
    
    print(f"⚡ Performance Metrics:")
    print(f"  Average language alignment: {perf_metrics['avg_language_alignment_score']:.3f}")
    print(f"  Average truth crystallization: {perf_metrics['avg_truth_crystallization_level']:.3f}")
    print(f"  Total insights generated: {perf_metrics['total_insights_generated']}")
    print(f"  Total REP patterns detected: {perf_metrics['total_rep_patterns_detected']}")
    print(f"  Insights per cycle: {perf_metrics['insights_per_cycle']:.1f}")
    print()
    
    print(f"🚧 Obstacle Analysis:")
    print(f"  Total obstacles identified: {obstacle_analysis['total_obstacles_identified']}")
    if obstacle_analysis['obstacles_by_type']:
        print(f"  Obstacle types: {list(obstacle_analysis['obstacles_by_type'].keys())}")
        if obstacle_analysis['most_common_obstacle']:
            print(f"  Most common: {obstacle_analysis['most_common_obstacle']}")
    print()
    
    print(f"💡 Enhancement Analysis:")
    print(f"  Total enhancements identified: {enhancement_analysis['total_enhancements_identified']}")
    if enhancement_analysis['enhancements_by_type']:
        print(f"  Enhancement types: {list(enhancement_analysis['enhancements_by_type'].keys())}")
        if enhancement_analysis['most_common_enhancement']:
            print(f"  Most common: {enhancement_analysis['most_common_enhancement']}")
    print()
    
    print(f"🛡️ Guardian System Summary:")
    guardian_summary = results['guardian_system_summary']
    active_guardians = [name for name, data in guardian_summary.items() if data['total_reports'] > 0]
    print(f"  Active guardians: {len(active_guardians)}")
    print(f"  Guardian names: {', '.join(active_guardians[:5])}")
    if len(active_guardians) > 5:
        print(f"  ... and {len(active_guardians) - 5} more")
    print()
    
    print(f"🎯 Key Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")
    print()
    
    # Save demonstration results
    demo_results_file = f"demo_cortex_panacea_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(demo_results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Demonstration results saved to: {demo_results_file}")
    print()
    
    # Show scalability projection
    print("🚀 SCALABILITY PROJECTION FOR FULL 31-CYCLE RUN")
    print("=" * 55)
    
    cycles_per_file = 31
    total_files = len(system.panacea_files)
    total_cycles_full = cycles_per_file * total_files
    
    avg_time_per_cycle = total_time / len(system.cycle_results)
    projected_time = total_cycles_full * avg_time_per_cycle
    
    print(f"📊 Full System Projection:")
    print(f"  Total files: {total_files}")
    print(f"  Cycles per file: {cycles_per_file}")
    print(f"  Total cycles: {total_cycles_full}")
    print(f"  Estimated total time: {projected_time:.1f} seconds ({projected_time/60:.1f} minutes)")
    print(f"  Estimated insights: {int(perf_metrics['insights_per_cycle'] * total_cycles_full)}")
    print(f"  Estimated REP patterns: {int(perf_metrics['rep_patterns_per_cycle'] * total_cycles_full)}")
    print()
    
    print("✅ DEMONSTRATION COMPLETE")
    print("This system is ready for full 31-cycle educational dialogue training!")
    print("Use the CLI with: python paco_efficiency_cli.py --mode cortex-panacea --visualize")
    
    return results

if __name__ == "__main__":
    demonstrate_cortex_panacea_system()