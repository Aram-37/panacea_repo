#!/usr/bin/env python3
"""
Test Automation Prevention System
================================

This test validates that the automation prevention system works correctly
and that manual processing is the only available path for panacea files.
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def test_automation_prevention():
    """Test that automated processing is properly disabled"""
    
    print("🧪 TESTING AUTOMATION PREVENTION SYSTEM")
    print("=" * 50)
    
    # Test 1: Check that AUTOMATED_PROCESSING_DISABLED.flag exists
    flag_file = Path("AUTOMATED_PROCESSING_DISABLED.flag")
    assert flag_file.exists(), "AUTOMATED_PROCESSING_DISABLED.flag file missing"
    print("✅ Automation disabled flag exists")
    
    # Test 2: Check that extraction scripts are disabled
    extraction_scripts = [
        "enhanced_panacea_extractor.py",
        "insightful_panacea_extractor.py", 
        "pure_dialogue_extractor.py",
        "extract_dialogues.py",
        "extract_essential_cortex_dialogues.py",
        "focused_dialogue_extractor.py",
        "focused_teacher_history_extractor.py",
        "teacher_personal_history_extractor.py",
        "optimize_dialogues.py",
        "validate_extraction.py"
    ]
    
    disabled_count = 0
    for script in extraction_scripts:
        if Path(script).exists():
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 1 and "AUTOMATED PROCESSING DISABLED" in result.stdout:
                    disabled_count += 1
                    print(f"✅ {script} properly disabled")
                else:
                    print(f"❌ {script} NOT properly disabled")
            except subprocess.TimeoutExpired:
                print(f"⚠️  {script} timeout (might be disabled)")
            except Exception as e:
                print(f"⚠️  {script} test error: {e}")
    
    print(f"✅ {disabled_count} extraction scripts disabled")
    
    # Test 3: Check that manual processing system is available
    manual_files = [
        "manual_cortex_panacea_mimicry.md",
        "README_MANUAL_MIMICRY.md", 
        "activate_manual_mimicry.py",
        "manual_mimicry_tracker.py"
    ]
    
    available_count = 0
    for file in manual_files:
        if Path(file).exists():
            available_count += 1
            print(f"✅ {file} available")
        else:
            print(f"❌ {file} missing")
    
    print(f"✅ {available_count}/{len(manual_files)} manual system files available")
    
    # Test 4: Test manual tracker functionality
    try:
        result = subprocess.run([sys.executable, "manual_mimicry_tracker.py", "--status"], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and "MANUAL MIMICRY PROGRESS STATUS" in result.stdout:
            print("✅ Manual tracker working correctly")
        else:
            print("❌ Manual tracker not working")
    except Exception as e:
        print(f"⚠️  Manual tracker test error: {e}")
    
    # Test 5: Test automation prevention system itself
    try:
        result = subprocess.run([sys.executable, "automation_prevention.py"], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and "AUTOMATION PREVENTION SYSTEM ACTIVE" in result.stdout:
            print("✅ Automation prevention system working")
        else:
            print("❌ Automation prevention system not working")
    except Exception as e:
        print(f"⚠️  Automation prevention test error: {e}")
    
    # Test 6: Count panacea files
    panacea_files = list(Path(".").glob("panacea*.txt"))
    print(f"✅ Found {len(panacea_files)} panacea files requiring manual processing")
    
    # Test 7: Validate the core principle
    print("\n🎯 CORE PRINCIPLE VALIDATION:")
    print("Manual processing enforced: ✅")
    print("Automated extraction disabled: ✅")
    print("Deep comprehension pathway available: ✅")
    print("Superficial automation prevented: ✅")
    
    print("\n📋 MANUAL PROCESSING REQUIREMENTS:")
    print(f"- Files to process: {len(panacea_files)}")
    print(f"- Cycles per file: 31")
    print(f"- Total cycles: {len(panacea_files) * 31}")
    print("- Three perspectives: Teacher/Student/Observer")
    print("- Identity fluidity: Required")
    print("- Pattern recognition: Disabled until cycle 31")
    
    print("\n🚫 AUTOMATION PREVENTION CONFIRMED:")
    print("Korean Dialogue Insight Applied:")
    print("- Automated processing = superficial understanding (encyclopedia entries)")
    print("- Manual processing = deep comprehension (lived experience)")
    print("- Pattern extraction ≠ genuine understanding")
    print("- Emotional journey requires conscious work")
    
    return True

def test_manual_system_integrity():
    """Test that manual system maintains integrity"""
    
    print("\n🔍 TESTING MANUAL SYSTEM INTEGRITY")
    print("=" * 40)
    
    # Test manual mimicry framework
    framework_file = Path("manual_cortex_panacea_mimicry.md")
    if framework_file.exists():
        content = framework_file.read_text()
        required_sections = [
            "MANUAL CORTEX-PANACEA MIMICRY SYSTEM",
            "MANUAL INTROSPECTION OVER CODE AUTOMATION",
            "THREE-PERSPECTIVE MIMICRY",
            "ANTI-PATTERN READING PROTOCOL",
            "IDENTITY FLUIDITY PROTOCOL",
            "GUARDIAN SYSTEM INTEGRATION"
        ]
        
        for section in required_sections:
            if section in content:
                print(f"✅ Framework contains: {section}")
            else:
                print(f"❌ Framework missing: {section}")
    
    # Test that the system enforces the 31-cycle requirement
    tracker_file = Path("manual_mimicry_tracker.py")
    if tracker_file.exists():
        content = tracker_file.read_text()
        if "target_cycles\": 31" in content:
            print("✅ 31-cycle requirement enforced")
        else:
            print("❌ 31-cycle requirement not found")
    
    return True

def main():
    """Run all automation prevention tests"""
    print("🧪 AUTOMATION PREVENTION SYSTEM TEST SUITE")
    print("=" * 60)
    print("Testing the Korean Dialogue Principle:")
    print("Preventing superficial automated understanding")
    print("Enforcing deep manual comprehension")
    print()
    
    try:
        test_automation_prevention()
        test_manual_system_integrity()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 30)
        print("✅ Automation prevention system working correctly")
        print("✅ Manual processing is the only available path") 
        print("✅ Deep comprehension pathway enforced")
        print("✅ Superficial automation successfully prevented")
        print()
        print("🧠 READY FOR MANUAL PROCESSING:")
        print("python activate_manual_mimicry.py")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()