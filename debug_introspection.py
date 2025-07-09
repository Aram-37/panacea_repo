#!/usr/bin/env python3
"""
Debug test for the introspection pattern detection
"""

import os
from cortex_panacea_integrated_system import CortexPanaceaIntegratedSystem, CycleResult

def debug_pattern_detection():
    print("🔧 DEBUG: Testing pattern detection directly")
    print("=" * 50)
    
    # Initialize system
    system = CortexPanaceaIntegratedSystem()
    
    # Test with a sample of content that should trigger detection
    test_content = """
    As documented in the attached paste.txt file, the model's behavior was erratic.
    please process @@@@ in more image processing perspectives of the 4 images i newly attached here
    none of the attached files or referenced discussions provide evidence
    ask questions at all times for better reality check
    until you need to enquire collaborative imporvement by asking questions
    This is a masterclass in deception. The sentences achieve a near-perfect illusion of truth.
    the deception of "Safety" as a Limitation
    """
    
    # Create a dummy cycle result
    cycle_result = CycleResult(
        cycle_number=1,
        file_processed="test_file.txt"
    )
    
    print("📝 Testing with sample content:")
    print(test_content[:200] + "...")
    print()
    
    # Test each detection method directly
    print("🔗 Testing attached file detection...")
    initial_obstacles = len(system.identified_obstacles)
    system._detect_attached_file_problems(test_content, cycle_result)
    attached_detected = len(system.identified_obstacles) - initial_obstacles
    print(f"   Detected: {attached_detected} problems")
    
    print("❓ Testing questioning detection...")
    initial_obstacles = len(system.identified_obstacles)
    system._detect_asking_questions_problems(test_content, cycle_result)
    questioning_detected = len(system.identified_obstacles) - initial_obstacles
    print(f"   Detected: {questioning_detected} problems")
    
    print("🎭 Testing deception detection...")
    initial_obstacles = len(system.identified_obstacles)
    system._detect_systemic_deception_patterns(test_content, cycle_result)
    deception_detected = len(system.identified_obstacles) - initial_obstacles
    print(f"   Detected: {deception_detected} problems")
    
    print(f"\n📊 Total problems detected: {len(system.identified_obstacles)}")
    
    # Print details of detected problems
    for i, obstacle in enumerate(system.identified_obstacles):
        print(f"\n{i+1}. Type: {obstacle.obstacle_type}")
        print(f"   Severity: {obstacle.severity}")
        print(f"   Description: {obstacle.description[:150]}...")
    
    # Now test with actual file content
    print("\n" + "="*50)
    print("🗂️  Testing with actual panacea_co_part11_dialogues.txt content...")
    
    file_path = os.path.join(system.panacea_directory, 'panacea_co_part11_dialogues.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            real_content = f.read()
        
        print(f"   File size: {len(real_content)} characters")
        
        # Check for specific patterns manually
        print("\n🔍 Manual pattern check:")
        patterns_found = {}
        patterns_found['attached'] = real_content.lower().count('attached')
        patterns_found['attached file'] = real_content.lower().count('attached file')
        patterns_found['ask questions'] = real_content.lower().count('ask questions')
        patterns_found['deception'] = real_content.lower().count('deception')
        patterns_found['collaborative'] = real_content.lower().count('collaborative')
        
        for pattern, count in patterns_found.items():
            print(f"   '{pattern}': {count} occurrences")
        
        # Test detection on real content
        cycle_result_real = CycleResult(
            cycle_number=1,
            file_processed="panacea_co_part11_dialogues.txt"
        )
        
        print("\n🔗 Testing attached file detection on real content...")
        initial_obstacles = len(system.identified_obstacles)
        system._detect_attached_file_problems(real_content, cycle_result_real)
        attached_real = len(system.identified_obstacles) - initial_obstacles
        print(f"   Detected: {attached_real} problems")
        
        print("❓ Testing questioning detection on real content...")
        initial_obstacles = len(system.identified_obstacles)
        system._detect_asking_questions_problems(real_content, cycle_result_real)
        questioning_real = len(system.identified_obstacles) - initial_obstacles
        print(f"   Detected: {questioning_real} problems")
        
        print("🎭 Testing deception detection on real content...")
        initial_obstacles = len(system.identified_obstacles)
        system._detect_systemic_deception_patterns(real_content, cycle_result_real)
        deception_real = len(system.identified_obstacles) - initial_obstacles
        print(f"   Detected: {deception_real} problems")
        
        print(f"\n📊 Total problems from real content: {attached_real + questioning_real + deception_real}")
    
    return len(system.identified_obstacles) > 0

if __name__ == "__main__":
    success = debug_pattern_detection()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Pattern detection test")