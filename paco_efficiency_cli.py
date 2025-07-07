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
        """
    )
    
    parser.add_argument('--mode', 
                       choices=['basic', 'advanced', 'integrated'],
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
        
        print(f"\n✅ Analysis complete!")
        print(f"📁 Results saved in: {os.path.abspath(args.output)}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()