#!/usr/bin/env python3
"""
CORTEX CLI - Command Line Interface for Unified CORTEX Final
===========================================================

Easy-to-use command line interface for the complete CORTEX system.
Integrates all frameworks and provides multiple operational modes.

Usage:
    python cortex_cli.py [command] [options]

Commands:
    demo        - Run demonstration with sample input
    process     - Process custom input text
    status      - Show system status
    test        - Run comprehensive tests
    help        - Show detailed help

Examples:
    python cortex_cli.py demo
    python cortex_cli.py process "Your text here"
    python cortex_cli.py test --verbose
"""

import argparse
import sys
import json
from pathlib import Path

# Import the unified CORTEX system
from unified_cortex_final import UnifiedCortex, ProcessingContext, CortexResult

def run_demo(args):
    """Run CORTEX demonstration"""
    print("🚀 Running CORTEX Demonstration")
    print("=" * 40)
    
    cortex = UnifiedCortex()
    result = cortex.demonstrate()
    
    print_results(result, verbose=args.verbose)
    
    if args.output:
        save_results(result, args.output)

def run_process(args):
    """Process custom input"""
    print("🔄 Processing Custom Input")
    print("=" * 30)
    
    if not args.input and not args.file:
        print("❌ Error: Must provide --input text or --file path")
        return
    
    # Get input text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
            print(f"📁 Processing file: {args.file}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
    else:
        input_text = args.input
    
    # Create context
    context = ProcessingContext(
        domain=args.domain,
        complexity=args.complexity,
        stakes=args.stakes,
        cultural_context=args.cultural_context.split(',') if args.cultural_context else ['korean', 'universal'],
        harmonic_frequency=args.frequency
    )
    
    # Process
    cortex = UnifiedCortex()
    result = cortex.process(input_text, context)
    
    print_results(result, verbose=args.verbose)
    
    if args.output:
        save_results(result, args.output)

def run_status(args):
    """Show system status"""
    print("📊 CORTEX System Status")
    print("=" * 25)
    
    cortex = UnifiedCortex()
    status = cortex.get_system_status()
    
    print(f"System Active: {status['active']}")
    print(f"Frameworks: {status['frameworks_active']}")
    print(f"Total Processes: {status['total_processes']}")
    print(f"Average Enhancement: {status['average_enhancement']:.1f}x")
    
    print(f"\n🎯 Capabilities:")
    for i, capability in enumerate(status['capabilities'], 1):
        print(f"   {i}. {capability}")

def run_test(args):
    """Run comprehensive tests"""
    print("🧪 Running CORTEX Tests")
    print("=" * 22)
    
    cortex = UnifiedCortex()
    
    test_cases = [
        {
            'name': 'Korean Wisdom Integration',
            'input': '진실과 지혜를 통한 깨달음을 추구합니다. Truth through wisdom consciousness.',
            'context': ProcessingContext(cultural_context=['korean', 'universal'])
        },
        {
            'name': 'Harmonic Resonance Test',
            'input': 'Frequency 777 resonates with patterns 432 and 144 creating harmonic amplification.',
            'context': ProcessingContext(harmonic_frequency=777)
        },
        {
            'name': 'Multi-Dimensional Analysis',
            'input': 'Quantum consciousness emerges through individual awareness into cosmic understanding.',
            'context': ProcessingContext(dimensional_focus=['quantum', 'individual', 'cosmic'])
        },
        {
            'name': 'Truth Validation Test',
            'input': 'Truth manifests fractally across all scales from quantum to cosmic reality.',
            'context': ProcessingContext(complexity=8, stakes=9)
        }
    ]
    
    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"\n🔬 Test {i}: {test['name']}")
        print("-" * 40)
        
        try:
            result = cortex.process(test['input'], test['context'])
            results.append(result)
            
            print(f"✅ Enhancement: {result.total_enhancement_factor:.1f}x")
            print(f"✅ Insights: {result.total_insights}")
            print(f"✅ Processing Time: {result.processing_time:.3f}s")
            
            if args.verbose:
                print(f"   Patterns: {result.total_patterns}")
                print(f"   Crystallized Knowledge: {len(result.crystallized_knowledge)}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Summary
    if results:
        avg_enhancement = sum(r.total_enhancement_factor for r in results) / len(results)
        total_insights = sum(r.total_insights for r in results)
        total_time = sum(r.processing_time for r in results)
        
        print(f"\n📊 Test Summary:")
        print(f"   Tests Passed: {len(results)}/{len(test_cases)}")
        print(f"   Average Enhancement: {avg_enhancement:.1f}x")
        print(f"   Total Insights: {total_insights}")
        print(f"   Total Processing Time: {total_time:.3f}s")

def print_results(result: CortexResult, verbose: bool = False):
    """Print processing results"""
    print(f"\n🎯 Processing Results:")
    print(f"   Enhancement Factor: {result.total_enhancement_factor:.1f}x")
    print(f"   Total Insights: {result.total_insights}")
    print(f"   Total Patterns: {result.total_patterns}")
    print(f"   Processing Time: {result.processing_time:.3f}s")
    
    if result.crystallized_knowledge:
        print(f"\n💎 Crystallized Knowledge:")
        for i, knowledge in enumerate(result.crystallized_knowledge, 1):
            print(f"   {i}. {knowledge}")
    
    if result.cross_framework_correlations:
        print(f"\n🔗 Cross-Framework Correlations:")
        for i, correlation in enumerate(result.cross_framework_correlations, 1):
            print(f"   {i}. {correlation}")
    
    if verbose and result.framework_results:
        print(f"\n🔬 Framework Details:")
        for name, fw_result in result.framework_results.items():
            print(f"   {name}: {fw_result.enhancement_factor:.1f}x ({fw_result.confidence_level:.3f} confidence)")
            if fw_result.insights:
                for insight in fw_result.insights:
                    print(f"      - {insight}")

def save_results(result: CortexResult, output_path: str):
    """Save results to file"""
    try:
        # Convert result to dictionary for JSON serialization
        result_dict = {
            'total_enhancement_factor': result.total_enhancement_factor,
            'total_insights': result.total_insights,
            'total_patterns': result.total_patterns,
            'processing_time': result.processing_time,
            'crystallized_knowledge': result.crystallized_knowledge,
            'cross_framework_correlations': result.cross_framework_correlations,
            'framework_results': {
                name: {
                    'framework_name': fw.framework_name,
                    'processing_time': fw.processing_time,
                    'confidence_level': fw.confidence_level,
                    'insights': fw.insights,
                    'patterns_detected': fw.patterns_detected,
                    'enhancement_factor': fw.enhancement_factor
                }
                for name, fw in result.framework_results.items()
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="CORTEX CLI - Unified CORTEX Final System Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s demo                           # Run demonstration
  %(prog)s process --input "Your text"    # Process text
  %(prog)s process --file input.txt       # Process file
  %(prog)s test --verbose                 # Run verbose tests
  %(prog)s status                         # Show system status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    demo_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    demo_parser.add_argument('--output', '-o', help='Save results to file')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process custom input')
    process_parser.add_argument('--input', '-i', help='Input text to process')
    process_parser.add_argument('--file', '-f', help='Input file to process')
    process_parser.add_argument('--domain', '-d', default='knowledge_expansion', help='Processing domain')
    process_parser.add_argument('--complexity', '-c', type=int, default=5, help='Complexity level (1-10)')
    process_parser.add_argument('--stakes', '-s', type=int, default=5, help='Stakes level (1-10)')
    process_parser.add_argument('--cultural-context', help='Cultural context (comma-separated)')
    process_parser.add_argument('--frequency', type=float, default=777.0, help='Harmonic frequency')
    process_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    process_parser.add_argument('--output', '-o', help='Save results to file')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run comprehensive tests')
    test_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        return
    
    try:
        if args.command == 'demo':
            run_demo(args)
        elif args.command == 'process':
            run_process(args)
        elif args.command == 'status':
            run_status(args)
        elif args.command == 'test':
            run_test(args)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose if hasattr(args, 'verbose') else False:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()