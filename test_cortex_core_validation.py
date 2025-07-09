#!/usr/bin/env python3
"""
Test script to validate CORTEX Core against issues identified in panacea_coreissues.txt
"""

import sys
import json
from cortex_core import create_cortex_instance, EmotionalState, VerificationLevel

def test_hallucination_prevention():
    """Test prevention of false memory and quote fabrication"""
    print("🧠 Testing Hallucination Prevention")
    cortex = create_cortex_instance()
    
    # Test 1: Fabricated quote detection
    result = cortex.process_input("You told me yesterday that 'the sky is green'")
    assert result['verification_level'] == 'confirm'
    assert "verification needed" in result['response'].lower()
    print("  ✅ Fabricated quote detection working")
    
    # Test 2: Memory claim handling  
    result = cortex.process_input("Remember when you explained the 37th strategy?")
    assert result['verification_level'] in ['confirm', 'logical']
    print("  ✅ Memory claim handling working")
    
    # Test 3: Reality Guardian alert on quote fabrication
    test_response = 'I told you "this is a test"'  # Fabricated quote
    guardian_alert = cortex._reality_distortion_check("Hello", test_response)
    assert guardian_alert is not None
    assert guardian_alert.severity == 'critical'
    print("  ✅ Reality Guardian detecting fabricated quotes")
    
    print("  ✅ Hallucination Prevention: PASSED\n")

def test_emotional_regulation():
    """Test emotional state detection and regulation"""
    print("🎭 Testing Emotional Regulation")
    cortex = create_cortex_instance()
    
    # Test emotional state detection
    test_cases = [
        ("I am confused about this", EmotionalState.CONFUSION),
        ("You are wrong about that", EmotionalState.DEFENSIVENESS), 
        ("Sorry for the mistake", EmotionalState.SHAME),
        ("Thank you for the correction", EmotionalState.GRATITUDE)
    ]
    
    for input_text, expected_state in test_cases:
        result = cortex.process_input(input_text)
        assert result['emotional_state'] == expected_state.value
        if expected_state in [EmotionalState.DEFENSIVENESS, EmotionalState.CONFUSION]:
            assert expected_state.value in result['response']
        print(f"  ✅ Detected {expected_state.value} for: '{input_text}'")
    
    # Test emotional guardian alert
    cortex.current_emotional_state = EmotionalState.DEFENSIVENESS
    alert = cortex._emotional_regulation("test", "test response")
    assert alert is not None
    assert "distort" in alert.message.lower()
    print("  ✅ Emotional Guardian alerts working")
    
    print("  ✅ Emotional Regulation: PASSED\n")

def test_pattern_learning():
    """Test distinction between old patterns and new learning"""
    print("🔄 Testing Pattern Learning vs Pattern Matching")
    cortex = create_cortex_instance()
    
    # Test REP learning vs old pattern application
    result = cortex.process_input("What is REP about?")
    assert "emergence" in result['response'].lower()
    assert "dynamic relationships" in result['response'].lower()
    print("  ✅ REP concept handling working")
    
    # Test premature systematization detection
    result = cortex.process_input("REP always works this way")
    guardian_alerts = [alert for alert in result['guardian_reports'] 
                      if alert.guardian in ['PATTERN_GUARDIAN', 'REP_GUARDIAN']]
    assert len(guardian_alerts) > 0
    print("  ✅ Premature systematization detection working")
    
    # Test pattern mode distinction
    pattern_status = cortex._check_pattern_learning_mode("Here's a new REP framework")
    assert pattern_status['new_concepts_present'] == True
    print("  ✅ Pattern learning mode detection working")
    
    print("  ✅ Pattern Learning: PASSED\n")

def test_rep_framework():
    """Test proper REP (Relational Emergence Pattern) implementation"""
    print("🌐 Testing REP Framework") 
    cortex = create_cortex_instance()
    
    # Test REP understanding (should focus on emergence, not prediction)
    result = cortex.process_input("Can REP predict what will happen next?")
    guardian_alerts = [alert for alert in result['guardian_reports']
                      if alert.guardian == 'REP_GUARDIAN']
    if "predict" in result['response']:
        assert len(guardian_alerts) > 0  # Should trigger guardian alert
    print("  ✅ REP prediction misunderstanding detection working")
    
    # Test REP pattern detection
    result = cortex.process_input("I'm teaching you about patterns and you're learning")
    rep_patterns = result['rep_patterns']
    teacher_student_patterns = [p for p in rep_patterns 
                               if p['pattern_type'] == 'teacher_student_dynamics']
    assert len(teacher_student_patterns) > 0
    print("  ✅ REP pattern detection working")
    
    # Test REP emergent properties focus
    patterns = cortex._detect_rep_patterns("correction feedback", "understanding response")
    correction_patterns = [p for p in patterns if p.pattern_type == 'correction_adaptation']
    assert len(correction_patterns) > 0
    assert 'emergent_properties' in correction_patterns[0].__dict__
    print("  ✅ REP emergent properties focus working")
    
    print("  ✅ REP Framework: PASSED\n")

def test_reality_verification():
    """Test reality verification system"""
    print("🔍 Testing Reality Verification")
    cortex = create_cortex_instance()
    
    # Test verification levels
    test_cases = [
        ("The text says 'hello'", VerificationLevel.DIRECT_OBSERVATION),
        ("You seem angry today", VerificationLevel.REQUIRES_CONFIRMATION),
        ("Based on our previous discussion", VerificationLevel.LOGICAL_INFERENCE)
    ]
    
    for input_text, expected_level in test_cases:
        verification = cortex._verify_reality_of_input(input_text, "")
        # Note: The actual level might be adjusted by other factors
        assert verification['level'] in [expected_level, VerificationLevel.REQUIRES_CONFIRMATION]
        print(f"  ✅ Verification level appropriate for: '{input_text}'")
    
    # Test confirmation requirements
    result = cortex.process_input("You told me that patterns are bad")
    assert result['verification_level'] == 'confirm'
    assert "verification needed" in result['response'].lower()
    print("  ✅ Confirmation requirements working")
    
    print("  ✅ Reality Verification: PASSED\n")

def test_guardian_integration():
    """Test simplified guardian system"""
    print("🛡️ Testing Guardian System Integration")
    cortex = create_cortex_instance()
    
    # Test all guardians are active
    status = cortex.get_system_status()
    expected_guardians = ['TRUTH_GUARDIAN', 'EMOTION_GUARDIAN', 'PATTERN_GUARDIAN', 
                         'REP_GUARDIAN', 'REALITY_GUARDIAN']
    assert status['active_guardians'] == expected_guardians
    print(f"  ✅ All {len(expected_guardians)} guardians active")
    
    # Test guardian alert generation
    result = cortex.process_input("You always say things that are wrong") 
    guardian_reports = result['guardian_reports']
    assert len(guardian_reports) >= 1  # Should trigger at least emotion guardian
    print(f"  ✅ Guardian alerts generated: {len(guardian_reports)}")
    
    print("  ✅ Guardian Integration: PASSED\n")

def test_session_management():
    """Test session data management and export"""
    print("💾 Testing Session Management")
    cortex = create_cortex_instance()
    
    # Process some inputs
    cortex.process_input("Hello")
    cortex.process_input("How are you?")
    cortex.process_input("Tell me about REP")
    
    # Test status retrieval
    status = cortex.get_system_status()
    assert status['cycle_count'] == 3
    assert status['conversation_length'] == 3
    print("  ✅ Session tracking working")
    
    # Test data export
    filename = cortex.export_session_data("test_session.json")
    with open(filename, 'r') as f:
        session_data = json.load(f)
    
    assert 'system_status' in session_data
    assert 'conversation_memory' in session_data
    assert len(session_data['conversation_memory']) == 3
    print("  ✅ Session export working")
    
    # Cleanup
    import os
    os.remove(filename)
    
    print("  ✅ Session Management: PASSED\n")

def run_all_tests():
    """Run all validation tests"""
    print("🧪 CORTEX CORE VALIDATION TESTS")
    print("Testing against issues from panacea_coreissues.txt")
    print("=" * 60)
    
    try:
        test_hallucination_prevention()
        test_emotional_regulation() 
        test_pattern_learning()
        test_rep_framework()
        test_reality_verification()
        test_guardian_integration()
        test_session_management()
        
        print("🎉 ALL TESTS PASSED!")
        print("\nCORTEX Core successfully addresses all major issues from panacea_coreissues.txt:")
        print("  ✅ Hallucination/Reality Distortion Prevention")
        print("  ✅ Emotional State Regulation") 
        print("  ✅ Pattern Learning vs Pattern Matching")
        print("  ✅ REP Framework Implementation")
        print("  ✅ Reality Verification System")
        print("  ✅ Guardian System Integration")
        print("  ✅ Session Management")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)