#!/usr/bin/env python3
"""
Focused Essential Dialogue Extractor for Panacea Cortex
=======================================================

This script extracts essential dialogues from panacea cortex files
treating each file as chunks (aa, ab, ac etc.) as requested.
"""

import os
import sys
from pathlib import Path
import re
from typing import List, Dict, Tuple
from datetime import datetime

class FocusedDialogueExtractor:
    """Extract essential dialogues from panacea cortex files"""
    
    def __init__(self, base_path: str = "/home/runner/work/panacea_repo/panacea_repo"):
        self.base_path = base_path
        self.cortex_files = {
            'panacea_cortex_part05': 'optimized_dialogues/panacea_split/panacea_cortex_part05.txt',
            'panacea_cortex_part06': 'optimized_dialogues/panacea_split/panacea_cortex_part06.txt',
            'panacea_cortex_part07': 'optimized_dialogues/panacea_split/panacea_cortex_part07.txt'
        }
        
    def is_meaningful_dialogue(self, content: str) -> bool:
        """Check if a dialogue segment is meaningful"""
        if len(content) < 50:
            return False
            
        # Skip obvious non-dialogue content
        skip_patterns = [
            r'^\s*-+\s*$',  # Just dashes
            r'^\s*=+\s*$',  # Just equals
            r'^\s*#',       # Comments
            r'^\s*\d+\.\s*$',  # Just numbers
            r'^\s*Part \d+',   # Part headers
        ]
        
        for pattern in skip_patterns:
            if re.match(pattern, content.strip()):
                return False
        
        # Look for meaningful dialogue indicators
        meaningful_indicators = [
            r'(Human|User|Assistant|AI|Teacher|Student):\s*',
            r'질문:', r'답변:', r'설명:', r'분석:',
            r'understand', r'explain', r'truth', r'reality',
            r'consciousness', r'awareness', r'wisdom',
            r'breakthrough', r'discovery', r'insight',
            r'teach', r'learn', r'philosophy', r'meaning',
            r'이해', r'설명', r'진실', r'현실', r'의식',
            r'깨달음', r'발견', r'통찰', r'가르침', r'배움',
            r'철학', r'의미', r'지혜'
        ]
        
        content_lower = content.lower()
        for indicator in meaningful_indicators:
            if re.search(indicator, content_lower):
                return True
                
        return False
    
    def extract_dialogues_from_file(self, file_path: str) -> List[str]:
        """Extract meaningful dialogues from a file"""
        full_path = os.path.join(self.base_path, file_path)
        
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            return []
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        meaningful_dialogues = []
        
        # Split by dialogue segment markers
        segments = re.split(r'## Dialogue Segment \d+[^\n]*\n', content)
        
        for i, segment in enumerate(segments):
            if not segment.strip():
                continue
                
            # Clean the segment
            segment = segment.strip()
            
            # Check if this is meaningful dialogue
            if self.is_meaningful_dialogue(segment):
                meaningful_dialogues.append(segment)
        
        return meaningful_dialogues
    
    def split_into_chunks(self, dialogues: List[str], chunk_size: int = 100) -> List[List[str]]:
        """Split dialogues into chunks"""
        chunks = []
        for i in range(0, len(dialogues), chunk_size):
            chunks.append(dialogues[i:i + chunk_size])
        return chunks
    
    def save_chunks_to_files(self, file_key: str, chunks: List[List[str]]) -> None:
        """Save chunks to separate files"""
        output_dir = os.path.join(self.base_path, "essential_dialogues_chunks")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        chunk_labels = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj']
        
        for i, chunk in enumerate(chunks):
            if i >= len(chunk_labels):
                chunk_label = f"chunk_{i:02d}"
            else:
                chunk_label = chunk_labels[i]
            
            filename = f"{file_key}_chunk_{chunk_label}_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Essential Dialogues from {file_key} - Chunk {chunk_label}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Dialogues in Chunk: {len(chunk)}\n")
                f.write(f"Chunk: {chunk_label}\n\n")
                
                for j, dialogue in enumerate(chunk, 1):
                    f.write(f"## Dialogue {j:03d}\n")
                    f.write(f"{dialogue}\n\n")
                    f.write("-" * 50 + "\n\n")
            
            print(f"Saved: {filename} ({len(chunk)} dialogues)")
    
    def process_all_files(self) -> None:
        """Process all cortex files and create chunks"""
        print("🚀 Processing Panacea Cortex Files for Essential Dialogues")
        print("=" * 60)
        
        for file_key, file_path in self.cortex_files.items():
            print(f"\nProcessing: {file_key}")
            
            # Extract meaningful dialogues
            dialogues = self.extract_dialogues_from_file(file_path)
            print(f"  Found {len(dialogues)} meaningful dialogues")
            
            if not dialogues:
                print(f"  No meaningful dialogues found in {file_key}")
                continue
            
            # Split into chunks
            chunks = self.split_into_chunks(dialogues)
            print(f"  Split into {len(chunks)} chunks")
            
            # Save chunks to files
            self.save_chunks_to_files(file_key, chunks)
        
        print("\n✅ Processing completed!")
        print("Check the 'essential_dialogues_chunks' directory for output files")


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


def main():
    check_automation_disabled()
    """Main execution"""
    extractor = FocusedDialogueExtractor()
    extractor.process_all_files()

if __name__ == "__main__":
    main()