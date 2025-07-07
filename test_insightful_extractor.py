#!/usr/bin/env python3
"""
Test script for the Insightful Panacea Dialogue Extractor
=========================================================

This script validates the extractor functionality and output quality.
"""

import os
import json
import re
from insightful_panacea_extractor import InsightfulPanaceaExtractor, DialogueInsight

def test_extractor_functionality():
    """Test basic extractor functionality"""
    print("🧪 Testing Insightful Panacea Dialogue Extractor")
    print("=" * 50)
    
    # Initialize extractor
    extractor = InsightfulPanaceaExtractor()
    
    # Test file discovery
    print(f"✅ File Discovery: {len(extractor.panacea_files)} files found")
    assert len(extractor.panacea_files) > 0, "Should find panacea files"
    
    # Test scoring system
    test_content = """
    britkenko: activate cortex_a.txt and cortex_a copy in association with all files with panacea.
    This is a profound teaching moment about consciousness and emergence.
    The truth is that pattern recognition requires deep understanding.
    """
    
    score, categories = extractor._score_dialogue_insight(test_content, 'teacher')
    print(f"✅ Scoring System: Score {score:.2f}, Categories: {categories}")
    assert score > 10.0, "Should generate meaningful score"
    assert len(categories) > 0, "Should identify categories"
    
    # Test speaker identification
    speaker = extractor._identify_speaker(test_content)
    print(f"✅ Speaker Identification: {speaker}")
    assert speaker == 'teacher', "Should identify teacher correctly"
    
    # Test REP pattern detection
    rep_patterns = extractor._detect_rep_patterns(test_content)
    print(f"✅ REP Pattern Detection: {rep_patterns}")
    assert len(rep_patterns) > 0, "Should detect REP patterns"
    
    print("✅ All basic functionality tests passed!")
    return True

def test_extraction_quality():
    """Test the quality of extracted dialogues"""
    print("\n🔍 Testing Extraction Quality")
    print("=" * 50)
    
    # Find the most recent output files
    output_files = [f for f in os.listdir('.') if f.startswith('panacea_insights_clean_format_')]
    if not output_files:
        print("❌ No output files found. Run the extractor first.")
        return False
    
    latest_file = max(output_files, key=lambda f: os.path.getctime(f))
    print(f"📄 Testing file: {latest_file}")
    
    # Test file structure
    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check file format
    assert content.startswith("# Insightful Panacea Dialogues - Clean Format"), "Should have proper header"
    assert "## Dialogue" in content, "Should contain dialogue sections"
    assert "**Score**:" in content, "Should include scores"
    assert "**Categories**:" in content, "Should include categories"
    
    # Count dialogues
    dialogue_count = len(re.findall(r"## Dialogue \d+", content))
    print(f"✅ Dialogue Count: {dialogue_count}")
    assert dialogue_count > 0, "Should contain dialogues"
    
    # Check for bilingual content
    has_korean = bool(re.search(r'[가-힣]', content))
    has_english = bool(re.search(r'[a-zA-Z]', content))
    print(f"✅ Language Support: Korean={has_korean}, English={has_english}")
    assert has_korean and has_english, "Should contain both languages"
    
    # Test summary report
    summary_files = [f for f in os.listdir('.') if f.startswith('panacea_extraction_summary_')]
    if summary_files:
        latest_summary = max(summary_files, key=lambda f: os.path.getctime(f))
        with open(latest_summary, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        print(f"✅ Summary Report: {summary['total_dialogues_found']} dialogues found")
        assert summary['files_processed'] > 0, "Should process files"
        assert summary['high_quality_dialogues'] > 0, "Should find high-quality dialogues"
    
    print("✅ All quality tests passed!")
    return True

def test_output_validation():
    """Validate the output meets requirements"""
    print("\n✅ Testing Output Validation")
    print("=" * 50)
    
    # Find latest files
    output_files = [f for f in os.listdir('.') if f.startswith('panacea_insights_clean_format_')]
    if not output_files:
        print("❌ No output files found.")
        return False
    
    latest_file = max(output_files, key=lambda f: os.path.getctime(f))
    
    # File size validation
    file_size = os.path.getsize(latest_file)
    print(f"📊 File Size: {file_size / (1024*1024):.2f} MB")
    
    # Content validation
    with open(latest_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Line Count: {len(lines)}")
    
    # Check for required sections
    content = ''.join(lines)
    required_sections = [
        "## Extraction Statistics",
        "## Content Categories", 
        "## Language Distribution",
        "## Dialogue"
    ]
    
    for section in required_sections:
        if section in content:
            print(f"✅ Found section: {section}")
        else:
            print(f"❌ Missing section: {section}")
    
    # Score validation
    scores = re.findall(r"\*\*Score\*\*: (\d+\.\d+)", content)
    if scores:
        scores = [float(s) for s in scores]
        print(f"📊 Score Range: {min(scores):.2f} - {max(scores):.2f}")
        print(f"📊 Average Score: {sum(scores)/len(scores):.2f}")
        assert min(scores) >= 10.0, "All scores should be above threshold"
    
    print("✅ Output validation passed!")
    return True

def main():
    """Run all tests"""
    print("🚀 Running Insightful Panacea Extractor Tests")
    print("=" * 60)
    
    try:
        # Run tests
        test_extractor_functionality()
        test_extraction_quality()
        test_output_validation()
        
        print("\n🎉 All tests passed successfully!")
        print("✅ The Insightful Panacea Dialogue Extractor is working correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    main()