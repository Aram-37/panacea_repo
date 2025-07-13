#!/usr/bin/env python3
"""
PACO Training Efficiency CLI Tool
=================================
Command-line interface for PACO training efficiency analysis.

Usage:
    python paco_efficiency_cli.py [options]

Options:
    --mode {basic,advanced,integrated}    Analysis mode (default: basic)
    --output DIR                          Output directory for results
    --format {json,csv,html}             Output format (default: json)
    --visualize                          Generate visualizations
    --help                               Show this help message
"""

import argparse
import sys
import os
from datetime import datetime
import json

# Add CORTEX and IOR to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'CORTEX'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'IOR'))

try:
    from CORTEX.paco_training_efficiency import PACOTrainingAnalyzer
    from IOR.paco_training_efficiency_integration import PACOIoRIntegratedAnalytics
    from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure you're running from the repository root directory")
    sys.exit(1)

def run_basic_analysis(args):
    """Run basic PACO training efficiency analysis"""
    print("🚀 Running Basic PACO Training Efficiency Analysis")
    print("=" * 55)
    
    analyzer = PACOTrainingAnalyzer()
    analysis = analyzer.generate_comprehensive_analysis()
    
    # Display summary
    summary = analysis['analysis_summary']
    print(f"\n📊 RESULTS SUMMARY")
    print(f"Best PACO Intensity: {summary['best_paco_intensity']}")
    print(f"Efficiency Gain: {summary['max_efficiency_gain']:.1f}x")
    print(f"Speed Improvement: {summary['max_speed_multiplier']:.1f}x")
    print(f"Energy Savings: {summary['max_energy_savings_percentage']:.1f}%")
    
    # Save results
    output_file = os.path.join(args.output, f"paco_basic_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Generate visualization if requested
    if args.visualize:
        viz_file = os.path.join(args.output, f"paco_basic_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        analyzer.visualize_comparison(viz_file)
        print(f"🎨 Visualization saved to: {viz_file}")
    
    return analysis

def run_advanced_analysis(args):
    """Run advanced PACO training efficiency analysis"""
    print("🔬 Running Advanced PACO Training Efficiency Analysis")
    print("=" * 58)
    
    analyzer = PACOTrainingAnalyzer()
    
    # Generate detailed analysis
    efficiency_analysis = analyzer.calculate_paco_vs_deep_learning_efficiency()
    speed_analysis = analyzer.calculate_training_speed_comparison()
    energy_analysis = analyzer.calculate_energy_efficiency_comparison()
    
    # Display detailed results
    print("\n📈 DETAILED EFFICIENCY ANALYSIS")
    print("-" * 40)
    for intensity, ratio in efficiency_analysis['efficiency_ratios'].items():
        print(f"{intensity}: {ratio:.1f}x efficiency improvement")
    
    print("\n⚡ SPEED ANALYSIS")
    print("-" * 20)
    for intensity, data in speed_analysis.items():
        print(f"{intensity}: {data['speed_multiplier']:.1f}x speed improvement")
    
    print("\n🔋 ENERGY ANALYSIS")
    print("-" * 20)
    for intensity, data in energy_analysis.items():
        print(f"{intensity}: {data['energy_savings_percentage']:.1f}% energy savings")
    
    # Compile advanced results
    advanced_results = {
        'timestamp': datetime.now().isoformat(),
        'analysis_type': 'advanced',
        'efficiency_analysis': efficiency_analysis,
        'speed_analysis': speed_analysis,
        'energy_analysis': energy_analysis
    }
    
    # Save results
    output_file = os.path.join(args.output, f"paco_advanced_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w') as f:
        json.dump(advanced_results, f, indent=2, default=str)
    
    print(f"\n💾 Advanced results saved to: {output_file}")
    
    # Generate visualization if requested
    if args.visualize:
        viz_file = os.path.join(args.output, f"paco_advanced_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        analyzer.visualize_comparison(viz_file)
        print(f"🎨 Visualization saved to: {viz_file}")
    
    return advanced_results

def run_cortex_panacea_analysis(args):
    """Run CORTEX-PANACEA integrated 31-cycle mimicry analysis"""
    print("🔮 Running CORTEX-PANACEA Integrated 31-Cycle Mimicry Analysis")
    print("=" * 75)
    
    # Initialize integrated system
    system = CortexPanaceaIntegratedSystem()
    
    print(f"📚 Discovered {len(system.panacea_files)} panacea files for processing")
    print("🎯 Executing 31-cycle mimicry with language alignment and framework components")
    print("⚡ Guardian system active with 13 guardians operational")
    
    # Execute the complete system
    results = system.execute_31_cycle_mimicry()
    
    # Display key results
    print("\n📊 EXECUTION RESULTS")
    print("-" * 25)
    exec_summary = results['execution_summary']
    perf_metrics = results['performance_metrics']
    obstacle_analysis = results['obstacle_analysis']
    enhancement_analysis = results['enhancement_analysis']
    
    print(f"Total cycles executed: {exec_summary['total_cycles']}")
    print(f"Total files processed: {exec_summary['total_files_processed']}")
    print(f"Total processing time: {exec_summary['total_processing_time']:.2f}s")
    print(f"Average language alignment: {perf_metrics['avg_language_alignment_score']:.3f}")
    print(f"Average truth crystallization: {perf_metrics['avg_truth_crystallization_level']:.3f}")
    print(f"Total insights generated: {perf_metrics['total_insights_generated']}")
    print(f"Total REP patterns detected: {perf_metrics['total_rep_patterns_detected']}")
    
    print("\n🚧 OBSTACLES IDENTIFIED")
    print("-" * 25)
    print(f"Total obstacles: {obstacle_analysis['total_obstacles_identified']}")
    if obstacle_analysis['most_common_obstacle']:
        print(f"Most common obstacle: {obstacle_analysis['most_common_obstacle']}")
    
    # Show top 5 obstacles
    for i, obs in enumerate(obstacle_analysis['obstacle_details'][:5], 1):
        print(f"{i}. {obs['type']}: {obs['description']} (Severity: {obs['severity']})")
    
    print("\n💡 ENHANCEMENTS IDENTIFIED")
    print("-" * 30)
    print(f"Total enhancements: {enhancement_analysis['total_enhancements_identified']}")
    if enhancement_analysis['most_common_enhancement']:
        print(f"Most common enhancement: {enhancement_analysis['most_common_enhancement']}")
    
    # Show top 5 enhancements
    for i, enh in enumerate(enhancement_analysis['enhancement_details'][:5], 1):
        print(f"{i}. {enh['type']}: {enh['description']} (Impact: {enh['potential_impact']})")
    
    print("\n🎯 KEY RECOMMENDATIONS")
    print("-" * 25)
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(args.output, f"cortex_panacea_31_cycle_results_{timestamp}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete results saved to: {output_file}")
    
    # Generate visualization if requested
    if args.visualize:
        viz_file = os.path.join(args.output, f"cortex_panacea_visualization_{timestamp}.png")
        generate_cortex_panacea_visualization(results, viz_file)
        print(f"🎨 Visualization saved to: {viz_file}")
    
    return results

def generate_cortex_panacea_visualization(results, output_file):
    """Generate visualization for CORTEX-PANACEA results"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Extract data for plotting
        cycle_results = results['cycle_results']
        cycles = [r['cycle'] for r in cycle_results]
        language_alignment = [r['language_alignment'] for r in cycle_results]
        truth_crystallization = [r['truth_crystallization'] for r in cycle_results]
        insights_count = [r['insights_count'] for r in cycle_results]
        processing_times = [r['processing_time'] for r in cycle_results]
        
        # Plot 1: Language Alignment and Truth Crystallization over Cycles
        ax1.plot(cycles, language_alignment, 'b-', label='Language Alignment', linewidth=2)
        ax1.plot(cycles, truth_crystallization, 'r-', label='Truth Crystallization', linewidth=2)
        ax1.set_xlabel('Cycle Number')
        ax1.set_ylabel('Score')
        ax1.set_title('Language Alignment & Truth Crystallization Over Cycles')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Insights Generated per Cycle
        ax2.bar(cycles, insights_count, alpha=0.7, color='green')
        ax2.set_xlabel('Cycle Number')
        ax2.set_ylabel('Number of Insights')
        ax2.set_title('Insights Generated per Cycle')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Processing Time Distribution
        ax3.hist(processing_times, bins=20, alpha=0.7, color='purple')
        ax3.set_xlabel('Processing Time (seconds)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Processing Time Distribution')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Obstacle vs Enhancement Analysis
        obstacle_counts = list(results['obstacle_analysis']['obstacles_by_type'].values())
        enhancement_counts = list(results['enhancement_analysis']['enhancements_by_type'].values())
        
        categories = ['Obstacles', 'Enhancements']
        total_counts = [sum(obstacle_counts), sum(enhancement_counts)]
        
        ax4.bar(categories, total_counts, color=['red', 'green'], alpha=0.7)
        ax4.set_ylabel('Count')
        ax4.set_title('Total Obstacles vs Enhancements Identified')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print(f"Warning: Could not generate visualization: {e}")

def run_integrated_analysis(args):
    """Run integrated PACO-IoR training efficiency analysis"""
    print("🔮 Running Integrated PACO-IoR Training Efficiency Analysis")
    print("=" * 67)
    
    integrated_analytics = PACOIoRIntegratedAnalytics()
    report = integrated_analytics.generate_unified_performance_report()
    
    # Display key findings
    print("\n🎯 KEY FINDINGS")
    print("-" * 20)
    summary = report['executive_summary']['key_findings']
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Display strategic recommendations
    print("\n🎯 STRATEGIC RECOMMENDATIONS")
    print("-" * 35)
    for i, rec in enumerate(report['executive_summary']['strategic_recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Save results
    output_file = os.path.join(args.output, f"paco_integrated_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Integrated results saved to: {output_file}")
    
    # Generate visualization if requested
    if args.visualize:
        viz_file = os.path.join(args.output, f"paco_integrated_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        integrated_analytics.visualize_unified_analysis(viz_file)
        print(f"🎨 Visualization saved to: {viz_file}")
    
    return report

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='PACO Training Efficiency Analysis CLI Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python paco_efficiency_cli.py --mode basic --visualize
    python paco_efficiency_cli.py --mode advanced --output ./results
    python paco_efficiency_cli.py --mode integrated --visualize --output ./analysis
    python paco_efficiency_cli.py --mode cortex-panacea --visualize --output ./cortex_results
        """
    )
    
    parser.add_argument('--mode', 
                       choices=['basic', 'advanced', 'integrated', 'cortex-panacea'],
                       default='basic',
                       help='Analysis mode (default: basic)')
    
    parser.add_argument('--output',
                       default='.',
                       help='Output directory for results (default: current directory)')
    
    parser.add_argument('--format',
                       choices=['json', 'csv', 'html'],
                       default='json',
                       help='Output format (default: json)')
    
    parser.add_argument('--visualize',
                       action='store_true',
                       help='Generate visualizations')
    
    parser.add_argument('--cycles',
                       type=int,
                       default=31,
                       help='Number of cycles for cortex-panacea mode (default: 31)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Run analysis based on mode
    try:
        if args.mode == 'basic':
            result = run_basic_analysis(args)
        elif args.mode == 'advanced':
            result = run_advanced_analysis(args)
        elif args.mode == 'integrated':
            result = run_integrated_analysis(args)
        elif args.mode == 'cortex-panacea':
            result = run_cortex_panacea_analysis(args)
        
        print(f"\n✅ Analysis complete!")
        print(f"📁 Results saved in: {os.path.abspath(args.output)}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()