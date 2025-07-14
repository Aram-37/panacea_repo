#!/usr/bin/env python3
"""
Validation Script for Essential Dialogue Extraction
==================================================

This script validates the extracted essential dialogues to ensure
quality and completeness.
"""

import os
import sys
from pathlib import Path
import glob
from typing import Dict, List

def validate_extraction_results(base_path: str = "/home/runner/work/panacea_repo/panacea_repo") -> None:
    """Validate the extraction results"""
    
    print("🔍 Validating Essential Dialogue Extraction Results")
    print("=" * 55)
    
    # Check output directories
    output_dir = os.path.join(base_path, "manual_extracted_dialogues")
    
    if not os.path.exists(output_dir):
        print("❌ Output directory not found!")
        return
    
    # Find all files
    chunk_files = glob.glob(os.path.join(output_dir, "*chunk*.txt"))
    essential_files = glob.glob(os.path.join(output_dir, "*essential_dialogues*.txt"))
    
    print(f"📁 Found {len(chunk_files)} chunk files")
    print(f"📁 Found {len(essential_files)} essential dialogue files")
    
    # Validate chunk files
    print("\n📊 Chunk File Validation:")
    expected_chunks = [
        "panacea_cortex_part05_chunk_aa",
        "panacea_cortex_part05_chunk_ab", 
        "panacea_cortex_part05_chunk_ac",
        "panacea_cortex_part06_chunk_aa",
        "panacea_cortex_part06_chunk_ab",
        "panacea_cortex_part07_chunk_aa",
        "panacea_cortex_part07_chunk_ab"
    ]
    
    found_chunks = []
    for chunk_file in chunk_files:
        filename = os.path.basename(chunk_file)
        for expected in expected_chunks:
            if expected in filename:
                found_chunks.append(expected)
                break
    
    for expected in expected_chunks:
        if expected in found_chunks:
            print(f"✅ {expected} - Found")
        else:
            print(f"❌ {expected} - Missing")
    
    # Validate content quality
    print("\n📈 Content Quality Validation:")
    
    total_dialogues = 0
    total_chars = 0
    
    for chunk_file in chunk_files:
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Count dialogues
            dialogue_count = content.count("## Dialogue")
            total_dialogues += dialogue_count
            total_chars += len(content)
            
            filename = os.path.basename(chunk_file)
            print(f"📄 {filename}: {dialogue_count} dialogues, {len(content):,} chars")
            
        except Exception as e:
            print(f"❌ Error reading {chunk_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Total dialogues across all chunks: {total_dialogues}")
    print(f"   Total content size: {total_chars:,} characters")
    print(f"   Average dialogue length: {total_chars // total_dialogues if total_dialogues > 0 else 0:,} characters")
    
    # Check for meaningful content
    print("\n🔍 Content Meaningfulness Check:")
    
    meaningful_indicators = [
        "Human:", "User:", "Assistant:", "AI:", "Teacher:", "Student:",
        "화자", "질문:", "답변:", "설명:", "분석:",
        "understand", "explain", "truth", "reality", "consciousness",
        "breakthrough", "discovery", "insight", "wisdom", "philosophy",
        "이해", "설명", "진실", "현실", "의식", "깨달음", "발견",
        "통찰", "가르침", "배움", "철학", "의미", "지혜"
    ]
    
    indicator_counts = {indicator: 0 for indicator in meaningful_indicators}
    
    for chunk_file in chunk_files:
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            for indicator in meaningful_indicators:
                indicator_counts[indicator] += content.count(indicator.lower())
                
        except Exception as e:
            print(f"❌ Error analyzing {chunk_file}: {e}")
    
    # Show top indicators
    sorted_indicators = sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True)
    print("🏆 Top meaningful content indicators:")
    for indicator, count in sorted_indicators[:10]:
        if count > 0:
            print(f"   {indicator}: {count} occurrences")
    
    # Final validation
    print("\n✅ Validation Complete!")
    
    if total_dialogues > 1000:
        print("🎉 Excellent: Over 1,000 dialogues extracted")
    elif total_dialogues > 500:
        print("👍 Good: Over 500 dialogues extracted")
    else:
        print("⚠️  Warning: Fewer than 500 dialogues extracted")
    
    if len(found_chunks) == len(expected_chunks):
        print("🎯 Perfect: All expected chunk files created")
    else:
        print(f"⚠️  Warning: Missing {len(expected_chunks) - len(found_chunks)} chunk files")


def check_automation_disabled():
    """Check if automated processing is disabled"""
    flag_file = Path(__file__).parent / "AUTOMATED_PROCESSING_DISABLED.flag"
    if flag_file.exists():
        print("🚫 AUTOMATED PROCESSING DISABLED")
        print("=" * 50)
        print("This script cannot run because automated processing is disabled.")
        print("The CORTEX directive requires manual processing only.")
        print("")
        print("Korean Dialogue Insight:")
        print("Automated processing = superficial understanding")
        print("Manual processing = deep comprehension through lived experience")
        print("")
        print("Use manual mimicry system instead:")
        print("- python activate_manual_mimicry.py")
        print("- python manual_mimicry_tracker.py")
        print("- manual_cortex_panacea_mimicry.md")
        print("")
        print("DO NEVER AUTOMATE ANYTHING. NOTHING AT ALL.")
        sys.exit(1)


if __name__ == "__main__":
    check_automation_disabled()
    validate_extraction_results()