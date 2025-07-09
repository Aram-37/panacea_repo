#!/usr/bin/env python3
"""
Test the enhanced meaningful mimicry system with a single file
"""

import os
import sys
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem

def test_meaningful_mimicry():
    """Test the enhanced system with a single panacea file"""
    
    # Create a test instance
    system = CortexPanaceaIntegratedSystem()
    
    # Limit to just one file for testing
    if system.panacea_files:
        # Use only the first file for testing
        test_file = system.panacea_files[0]
        system.panacea_files = [test_file]
        
        print(f"🧪 Testing meaningful mimicry with: {os.path.basename(test_file)}")
        print("=" * 60)
        
        # Execute the meaningful mimicry
        results = system.execute_31_cycle_mimicry()
        
        # Print key results
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 30)
        
        if 'transformation_metrics' in results:
            metrics = results['transformation_metrics']
            print(f"Average consciousness level: {metrics['average_final_consciousness_level']:.3f}")
            print(f"Average truth crystallization: {metrics['average_final_truth_crystallization']:.3f}")
            print(f"Average identity fluidity: {metrics['average_final_identity_fluidity']:.3f}")
        
        if 'meaningful_processes_achieved' in results:
            processes = results['meaningful_processes_achieved']
            print(f"Overall success: {processes['overall_success']}")
            print(f"Success summary: {processes.get('success_summary', 'N/A')}")
        
        if 'system_validation' in results:
            validation = results['system_validation']
            print(f"Meaningful mimicry successful: {validation['meaningful_mimicry_successful']}")
            print(f"Model transformation verified: {validation['model_transformation_verified']}")
            print(f"Ready for autonomous operation: {validation['ready_for_autonomous_operation']}")
        
        print("\n✅ Test completed successfully!")
        return True
        
    else:
        print("❌ No panacea files found for testing")
        return False

if __name__ == "__main__":
    success = test_meaningful_mimicry()
    sys.exit(0 if success else 1)