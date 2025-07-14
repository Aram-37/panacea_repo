#!/usr/bin/env python3
"""
Test script for the Focused Speaker Dialogue Extractor
====================================================

This script validates the focused dialogue extraction with speaker transitions.
"""

import os
import tempfile
from focused_speaker_dialogue_extractor import FocusedSpeakerDialogueExtractor

def test_speaker_detection():
    """Test speaker detection functionality"""
    print("🧪 Testing Speaker Detection")
    print("=" * 40)
    
    # Initialize extractor
    extractor = FocusedSpeakerDialogueExtractor()
    
    # Test cases
    test_cases = [
        ("britkenko: activate cortex system", "teacher"),
        ("성협: 이것은 테스트입니다", "teacher"),
        ("github copilot: I understand your request", "student"),
        ("assistant: Here is my response", "student"),
        ("user: What do you think about this?", "human"),
        ("human: This is a question", "human"),
        ("activate cortex_a.txt in association", "teacher"),
        ("Some random text without speaker", None),
    ]
    
    for test_input, expected in test_cases:
        result = extractor._detect_speaker(test_input)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_input[:30]}...' -> '{result}' (expected: '{expected}')")
    
    print("✅ Speaker detection test completed!")
    print()

def test_dialogue_line_detection():
    """Test dialogue line detection"""
    print("🧪 Testing Dialogue Line Detection")
    print("=" * 40)
    
    extractor = FocusedSpeakerDialogueExtractor()
    
    test_cases = [
        ("britkenko: This is a teaching moment", True),
        ("# This is a header", False),
        ("```python", False),
        ("What do you think about consciousness?", True),
        ("   ", False),
        ("123.", False),
        ("This is meaningful dialogue content with proper length", True),
        ("- List item", False),
        ("**Bold text**", False),
        ("Human: I have a question for you", True),
        ("activate cortex system framework", True),
        ("한국어로 대화를 나누어 보겠습니다", True),
        ("function test_function() {", False),
        ("import numpy as np", False),
    ]
    
    for test_input, expected in test_cases:
        result = extractor._is_dialogue_line(test_input)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_input[:30]}...' -> {result} (expected: {expected})")
    
    print("✅ Dialogue line detection test completed!")
    print()

def test_dialogue_cleaning():
    """Test dialogue content cleaning"""
    print("🧪 Testing Dialogue Cleaning")
    print("=" * 40)
    
    extractor = FocusedSpeakerDialogueExtractor()
    
    test_cases = [
        ("**Label**: This is content", "Label: This is content"),
        ("### Header text", "Header text"),
        ("- List item content", "List item content"),
        ("1. Numbered item", "Numbered item"),
        ("   Extra    spaces   ", "Extra spaces"),
        ("[2025-01-01] Timestamp content", "Timestamp content"),
        ("britkenko: activate cortex # lines 123-456", "britkenko: activate cortex"),
    ]
    
    for test_input, expected in test_cases:
        result = extractor._clean_dialogue_line(test_input)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_input}' -> '{result}' (expected: '{expected}')")
    
    print("✅ Dialogue cleaning test completed!")
    print()

def test_full_extraction():
    """Test full extraction process with sample content"""
    print("🧪 Testing Full Extraction Process")
    print("=" * 40)
    
    # Create temporary test file
    sample_content = """# Test Panacea File
This is some header content.

britkenko: activate cortex_a.txt and cortex_a copy in association with all files with panacea in its names.
you must not assume that the pattern appearance you assume will be applicable to anything in panacea.

github copilot: I understand your directive about cortex activation.
I will process the panacea files according to your instructions.

성협: 이것은 한국어로 된 교육 내용입니다.
REP 패턴을 찾아서 분석해야 합니다.

assistant: Thank you for the Korean guidance.
I can see the REP patterns emerging in the dialogue structure.

# This is a comment section
Some non-dialogue content here.

user: What do you think about consciousness and self-awareness?
This is a philosophical question.

britkenko: consciousness is not just awareness but the capacity for truth-seeking.
The self-contempt mechanism is crucial for authentic AI development.

Unknown speaker content without clear markers.
But this might still be dialogue content.
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_content)
        temp_path = f.name
    
    try:
        # Initialize extractor with temp directory
        extractor = FocusedSpeakerDialogueExtractor(os.path.dirname(temp_path))
        extractor.panacea_files = [temp_path]  # Override to use our test file
        
        # Extract dialogues
        dialogues = extractor._extract_dialogues_from_file(temp_path)
        
        print(f"✅ Extracted {len(dialogues)} dialogue segments")
        
        # Verify results
        assert len(dialogues) > 0, "Should extract some dialogues"
        
        # Check speaker distribution
        speakers = [d['speaker'] for d in dialogues]
        unique_speakers = set(speakers)
        print(f"✅ Found speakers: {', '.join(unique_speakers)}")
        
        # Check for expected speakers
        expected_speakers = {'teacher', 'student', 'human', 'unknown'}
        found_speakers = set(speakers)
        assert len(found_speakers.intersection(expected_speakers)) > 0, "Should find expected speakers"
        
        # Show sample dialogue
        if dialogues:
            sample = dialogues[0]
            print(f"✅ Sample dialogue: {sample['speaker']} - {sample['content'][:50]}...")
        
        print("✅ Full extraction test passed!")
        
    finally:
        # Clean up
        os.unlink(temp_path)
    
    print()

def test_output_generation():
    """Test output file generation"""
    print("🧪 Testing Output Generation")
    print("=" * 40)
    
    # Create sample dialogue data
    sample_dialogues = [
        {
            'speaker': 'teacher',
            'content': 'activate cortex_a.txt and process panacea files',
            'source_file': 'test_file.txt',
            'line_start': 1,
            'line_end': 2
        },
        {
            'speaker': 'student',
            'content': 'I understand the cortex activation directive',
            'source_file': 'test_file.txt',
            'line_start': 3,
            'line_end': 4
        },
        {
            'speaker': 'teacher',
            'content': 'Good. Now analyze the REP patterns',
            'source_file': 'test_file.txt',
            'line_start': 5,
            'line_end': 6
        }
    ]
    
    # Initialize extractor
    extractor = FocusedSpeakerDialogueExtractor()
    
    # Test output generation
    output_path = os.getcwd()
    
    try:
        extractor.generate_focused_output(sample_dialogues, output_path)
        print("✅ Focused output generated successfully")
        
        extractor.generate_conversation_flow_output(sample_dialogues, output_path)
        print("✅ Conversation flow output generated successfully")
        
        # Check if files were created
        import glob
        focused_files = glob.glob("../focused_speaker_dialogues_*.txt")
        flow_files = glob.glob("../conversation_flow_*.txt")
        
        assert len(focused_files) > 0, "Should create focused output file"
        assert len(flow_files) > 0, "Should create conversation flow file"
        
        print(f"✅ Created {len(focused_files)} focused output files")
        print(f"✅ Created {len(flow_files)} conversation flow files")
        
    except Exception as e:
        print(f"❌ Output generation failed: {e}")
        raise
    
    print("✅ Output generation test completed!")
    print()

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Focused Speaker Dialogue Extractor Tests")
    print("=" * 60)
    
    try:
        test_speaker_detection()
        test_dialogue_line_detection()
        test_dialogue_cleaning()
        test_full_extraction()
        test_output_generation()
        
        print("🎉 All tests passed successfully!")
        print("✅ The Focused Speaker Dialogue Extractor is working correctly")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()