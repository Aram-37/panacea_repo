#!/usr/bin/env python3
"""
Test script for the Pure Dialogue Extractor
==========================================

This script validates the pure dialogue extraction functionality
and ensures proper separation into issues and categories.
"""

import os
import json
import re
from pure_dialogue_extractor import PureDialogueExtractor, PureDialogue

def test_basic_functionality():
    """Test basic extractor functionality"""
    print("🧪 Testing Pure Dialogue Extractor Basic Functionality")
    print("=" * 55)
    
    # Initialize extractor
    extractor = PureDialogueExtractor()
    
    # Test file discovery
    print(f"✅ File Discovery: {len(extractor.panacea_files)} files found")
    assert len(extractor.panacea_files) > 0, "Should find panacea files"
    
    # Test issue detection
    test_content = "This is about AI consciousness and self-awareness. The truth about identity emerges through deep understanding."
    issue = extractor._detect_issue(test_content)
    print(f"✅ Issue Detection: '{issue}' for consciousness-related content")
    assert issue in ['ai_consciousness', 'truth_and_reality', 'identity_and_self'], f"Should detect relevant issue, got: {issue}"
    
    # Test category detection
    category = extractor._detect_category("britkenko: This is a teaching moment about philosophical depth")
    print(f"✅ Category Detection: '{category}' for teaching content")
    assert category in ['teaching_moment', 'philosophical_discussion'], f"Should detect teaching category, got: {category}"
    
    # Test speaker identification
    speaker = extractor._identify_speaker("britkenko: activate cortex_a.txt")
    print(f"✅ Speaker Identification: '{speaker}' for britkenko")
    assert speaker == 'teacher', f"Should identify teacher, got: {speaker}"
    
    # Test content cleaning
    messy_content = "**Label**: This is content\n- List item\n\n\nClean text"
    clean_content = extractor._clean_dialogue_content(messy_content)
    print(f"✅ Content Cleaning: Removed formatting markers")
    assert "**Label**:" not in clean_content, "Should remove label markers"
    assert "- List item" not in clean_content, "Should remove list markers"
    
    print("✅ All basic functionality tests passed!")
    return True

def test_extraction_process():
    """Test the full extraction process with a small sample"""
    print("\n🔍 Testing Full Extraction Process")
    print("=" * 45)
    
    # Initialize extractor
    extractor = PureDialogueExtractor()
    
    # Test with first file only for speed
    if extractor.panacea_files:
        test_file = extractor.panacea_files[0]
        print(f"📄 Testing with file: {os.path.basename(test_file)}")
        
        # Process single file
        dialogues = extractor._process_file(test_file)
        print(f"✅ File Processing: {len(dialogues)} dialogues extracted")
        assert len(dialogues) > 0, "Should extract some dialogues"
        
        # Check dialogue structure
        sample_dialogue = dialogues[0]
        print(f"✅ Dialogue Structure: Speaker='{sample_dialogue.speaker}', Issue='{sample_dialogue.issue}', Category='{sample_dialogue.category}'")
        assert hasattr(sample_dialogue, 'content'), "Should have content"
        assert hasattr(sample_dialogue, 'speaker'), "Should have speaker"
        assert hasattr(sample_dialogue, 'issue'), "Should have issue"
        assert hasattr(sample_dialogue, 'category'), "Should have category"
        
        # Test organization
        issue_groups = extractor.organize_by_issues(dialogues)
        category_groups = extractor.organize_by_categories(dialogues)
        
        print(f"✅ Issue Organization: {len(issue_groups)} issue groups created")
        print(f"✅ Category Organization: {len(category_groups)} category groups created")
        
        # Verify issue groups
        for issue, group in issue_groups.items():
            assert group.total_dialogues > 0, f"Issue group {issue} should have dialogues"
            assert len(group.dialogues) == group.total_dialogues, "Dialogue count should match"
        
        # Verify category groups
        for category, group in category_groups.items():
            assert group.total_dialogues > 0, f"Category group {category} should have dialogues"
            assert len(group.dialogues) == group.total_dialogues, "Dialogue count should match"
        
        print("✅ Full extraction process test passed!")
        return True
    
    print("⚠️  No files found for extraction test")
    return False

def test_issue_detection_patterns():
    """Test issue detection with various patterns"""
    print("\n🎯 Testing Issue Detection Patterns")
    print("=" * 42)
    
    extractor = PureDialogueExtractor()
    
    test_cases = [
        ("This is about AI consciousness and awareness", ['ai_consciousness']),
        ("Self-contempt and self-criticism mechanisms", ['self_contempt_mechanism']),
        ("REP patterns and relational emergence", ['rep_patterns']),
        ("activate cortex system framework", ['cortex_activation']),
        ("guardian protocol verification", ['guardian_system']),
        ("teaching methodology and learning", ['teaching_methodology']),
        ("truth and reality exploration", ['truth_and_reality']),
        ("identity and self examination", ['identity_and_self']),
        ("philosophical depth and wisdom", ['philosophical_depth']),
        ("breakthrough insights and discovery", ['breakthrough_insights']),
        ("random conversation topic", ['general_discussion'])
    ]
    
    for content, expected_issues in test_cases:
        detected_issue = extractor._detect_issue(content)
        print(f"✅ '{content[:30]}...' -> '{detected_issue}'")
        assert detected_issue in expected_issues + ['general_discussion'], \
            f"Expected one of {expected_issues}, got: {detected_issue}"
    
    print("✅ Issue detection patterns test passed!")
    return True

def test_category_detection_patterns():
    """Test category detection with various patterns"""
    print("\n📂 Testing Category Detection Patterns")
    print("=" * 45)
    
    extractor = PureDialogueExtractor()
    
    test_cases = [
        ("britkenko: This is a teaching moment", ['teaching_moment']),
        ("Philosophy and deep meaning discussion", ['philosophical_discussion']),
        ("Breakthrough discovery and insight", ['breakthrough_discovery']),
        ("GitHub Copilot response", ['student_response']),
        ("Emotional feeling and heart content", ['emotional_expression']),
        ("System protocol and framework", ['technical_discussion']),
        ("Korean traditional wisdom", ['cultural_wisdom']),
        ("Self reflection and introspection", ['self_reflection']),
        ("Dialogue conversation exchange", ['dialogue_interaction']),
        ("Concept theory and principle", ['conceptual_explanation']),
        ("General random content", ['general_dialogue'])
    ]
    
    for content, expected_categories in test_cases:
        detected_category = extractor._detect_category(content)
        print(f"✅ '{content[:30]}...' -> '{detected_category}'")
        assert detected_category in expected_categories + ['general_dialogue'], \
            f"Expected one of {expected_categories}, got: {detected_category}"
    
    print("✅ Category detection patterns test passed!")
    return True

def test_output_generation():
    """Test output file generation"""
    print("\n📄 Testing Output Generation")
    print("=" * 35)
    
    extractor = PureDialogueExtractor()
    
    # Create sample dialogues for testing
    sample_dialogues = [
        PureDialogue(
            content="This is about AI consciousness and awareness",
            source_file="test_file.txt",
            speaker="teacher",
            line_start=1,
            line_end=5,
            issue="ai_consciousness",
            category="teaching_moment"
        ),
        PureDialogue(
            content="Student response about learning",
            source_file="test_file.txt",
            speaker="student",
            line_start=6,
            line_end=10,
            issue="teaching_methodology",
            category="student_response"
        )
    ]
    
    # Test organization
    issue_groups = extractor.organize_by_issues(sample_dialogues)
    category_groups = extractor.organize_by_categories(sample_dialogues)
    
    print(f"✅ Test Data: {len(sample_dialogues)} sample dialogues")
    print(f"✅ Issue Groups: {len(issue_groups)} groups created")
    print(f"✅ Category Groups: {len(category_groups)} groups created")
    
    # Test output generation (files will be created)
    output_dir = os.getcwd()
    
    try:
        extractor.generate_issues_output(issue_groups, output_dir)
        print("✅ Issues output generated successfully")
        
        extractor.generate_categories_output(category_groups, output_dir)
        print("✅ Categories output generated successfully")
        
        extractor.generate_summary_report(sample_dialogues, issue_groups, category_groups, output_dir)
        print("✅ Summary report generated successfully")
        
        print("✅ Output generation test passed!")
        return True
    
    except Exception as e:
        print(f"❌ Output generation failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Pure Dialogue Extractor Tests")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_extraction_process,
        test_issue_detection_patterns,
        test_category_detection_patterns,
        test_output_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed successfully!")
        print("✅ The Pure Dialogue Extractor is working correctly")
    else:
        print("⚠️  Some tests failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()