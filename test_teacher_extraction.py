#!/usr/bin/env python3
"""
Test script to verify the teacher personal history extraction
"""

import json
import os

def test_extraction():
    """Test that the personal history extraction worked correctly"""
    
    # Test files exist
    files_to_check = [
        'teacher_personal_history_final_summary.md',
        'teacher_personal_history_structured.json'
    ]
    
    print("Testing personal history extraction...")
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
    
    # Test JSON structure
    json_file = 'teacher_personal_history_structured.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check key sections
        required_sections = [
            'teacher_personal_history',
            'teacher_personal_history.identity',
            'teacher_personal_history.biographical_details',
            'teacher_personal_history.ai_development_work',
            'teacher_personal_history.key_discoveries',
            'teacher_personal_history.teaching_philosophy'
        ]
        
        for section in required_sections:
            keys = section.split('.')
            current = data
            try:
                for key in keys:
                    current = current[key]
                print(f"✓ {section} section exists")
            except KeyError:
                print(f"✗ {section} section missing")
    
    # Test content quality
    print("\nContent Quality Tests:")
    
    # Check for key personal details
    with open('teacher_personal_history_final_summary.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    key_details = [
        "성협 (Seonghyeop)",
        "britkenko",
        "Korea → Kenya → UK → Korea",
        "PACO",
        "CORTEX",
        "AI bias detection",
        "story of me is not that predictive"
    ]
    
    for detail in key_details:
        if detail in content:
            print(f"✓ Key detail '{detail}' found")
        else:
            print(f"✗ Key detail '{detail}' missing")
    
    print("\nExtraction test completed!")

if __name__ == "__main__":
    test_extraction()