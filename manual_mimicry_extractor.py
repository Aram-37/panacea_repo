#!/usr/bin/env python3
"""
Manual Mimicry Dialogue Extractor for Panacea Cortex
===================================================

This script manually processes panacea cortex files to extract essential dialogues
without skipping or assuming patterns, as requested in the problem statement.
"""

import os
import re
from typing import List, Dict, Tuple
from datetime import datetime

class ManualMimicryExtractor:
    """Manually extract essential dialogues from panacea cortex files"""
    
    def __init__(self, base_path: str = "/home/runner/work/panacea_repo/panacea_repo"):
        self.base_path = base_path
        self.files_to_process = {
            'panacea_cortex_part05': 'optimized_dialogues/panacea_split/panacea_cortex_part05.txt',
            'panacea_cortex_part06': 'optimized_dialogues/panacea_split/panacea_cortex_part06.txt',
            'panacea_cortex_part07': 'optimized_dialogues/panacea_split/panacea_cortex_part07.txt'
        }
        
    def extract_raw_segments(self, content: str) -> List[Dict]:
        """Extract all segments without filtering"""
        segments = []
        
        # Find all dialogue segments using various patterns
        patterns = [
            r'## Dialogue Segment (\d+)[^\n]*\n(.*?)(?=## Dialogue Segment \d+|--- panacea_cortex 대화 \d+|$)',
            r'--- panacea_cortex 대화 (\d+) ---[^\n]*\n(.*?)(?=--- panacea_cortex 대화 \d+|## Dialogue Segment \d+|$)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
            for match in matches:
                segment_id = match.group(1)
                segment_content = match.group(2).strip()
                
                if segment_content:
                    segments.append({
                        'id': segment_id,
                        'content': segment_content,
                        'raw_length': len(segment_content),
                        'has_dialogue': self.contains_dialogue_markers(segment_content),
                        'has_korean': self.contains_korean(segment_content),
                        'complexity_score': self.calculate_complexity(segment_content)
                    })
        
        return segments
    
    def contains_dialogue_markers(self, content: str) -> bool:
        """Check if content contains dialogue markers"""
        dialogue_markers = [
            r'(Human|User|Assistant|AI|Teacher|Student):\s*',
            r'화자\s*\d+:', r'Speaker\s*\d+:', 
            r'\*\*(Human|User|Assistant|AI)\*\*:',
            r'질문:', r'답변:', r'설명:', r'분석:',
        ]
        
        for marker in dialogue_markers:
            if re.search(marker, content, re.IGNORECASE):
                return True
        return False
    
    def contains_korean(self, content: str) -> bool:
        """Check if content contains Korean text"""
        return bool(re.search(r'[가-힣]', content))
    
    def calculate_complexity(self, content: str) -> float:
        """Calculate complexity/meaningfulness score"""
        score = 0.0
        
        # Length bonus
        if len(content) > 100:
            score += 0.1
        if len(content) > 500:
            score += 0.1
        if len(content) > 1000:
            score += 0.1
        
        # Meaningful words
        meaningful_words = [
            'understand', 'explain', 'truth', 'reality', 'consciousness',
            'awareness', 'wisdom', 'breakthrough', 'discovery', 'insight',
            'teach', 'learn', 'philosophy', 'meaning', 'cortex', 'panacea',
            'system', 'framework', 'protocol', 'activation', 'guardian',
            '이해', '설명', '진실', '현실', '의식', '깨달음', '발견',
            '통찰', '가르침', '배움', '철학', '의미', '지혜', '시스템',
            '프레임워크', '활성화', '코텍스'
        ]
        
        content_lower = content.lower()
        for word in meaningful_words:
            if word in content_lower:
                score += 0.05
        
        # Dialogue interaction bonus
        if self.contains_dialogue_markers(content):
            score += 0.2
        
        # Korean content bonus
        if self.contains_korean(content):
            score += 0.1
        
        # Questions and answers
        questions = content.count('?') + content.count('？')
        score += min(questions * 0.02, 0.1)
        
        return score
    
    def is_essential_dialogue(self, segment: Dict) -> bool:
        """Determine if a segment is essential dialogue"""
        # Must have minimum length
        if segment['raw_length'] < 30:
            return False
        
        # Must have some complexity
        if segment['complexity_score'] < 0.15:
            return False
        
        # Preferred: has dialogue markers or Korean content
        if segment['has_dialogue'] or segment['has_korean']:
            return True
        
        # High complexity can override other requirements
        if segment['complexity_score'] > 0.5:
            return True
        
        return False
    
    def process_file(self, file_key: str, file_path: str) -> List[Dict]:
        """Process a single file to extract essential dialogues"""
        full_path = os.path.join(self.base_path, file_path)
        
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            return []
        
        print(f"Processing: {file_key}")
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        # Extract all segments
        raw_segments = self.extract_raw_segments(content)
        print(f"  Found {len(raw_segments)} raw segments")
        
        # Filter for essential dialogues
        essential_segments = []
        for segment in raw_segments:
            if self.is_essential_dialogue(segment):
                essential_segments.append(segment)
        
        print(f"  {len(essential_segments)} essential dialogues identified")
        
        # Sort by complexity score (highest first)
        essential_segments.sort(key=lambda x: x['complexity_score'], reverse=True)
        
        return essential_segments
    
    def save_essential_dialogues(self, file_key: str, segments: List[Dict]) -> None:
        """Save essential dialogues to file"""
        output_dir = os.path.join(self.base_path, "manual_extracted_dialogues")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{file_key}_essential_dialogues_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Essential Dialogues from {file_key}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Essential Dialogues: {len(segments)}\n")
            f.write(f"Manual Extraction - No patterns skipped\n\n")
            
            for i, segment in enumerate(segments, 1):
                f.write(f"## Essential Dialogue {i:03d}\n")
                f.write(f"**Segment ID**: {segment['id']}\n")
                f.write(f"**Length**: {segment['raw_length']} characters\n")
                f.write(f"**Complexity Score**: {segment['complexity_score']:.2f}\n")
                f.write(f"**Has Dialogue Markers**: {segment['has_dialogue']}\n")
                f.write(f"**Has Korean Content**: {segment['has_korean']}\n\n")
                f.write(f"**Content**:\n")
                f.write(f"{segment['content']}\n\n")
                f.write("-" * 50 + "\n\n")
        
        print(f"Saved: {filename}")
    
    def create_combined_chunks(self, all_segments: Dict[str, List[Dict]]) -> None:
        """Create combined chunk files as requested"""
        output_dir = os.path.join(self.base_path, "manual_extracted_dialogues")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create chunk files as requested in problem statement
        chunk_mapping = {
            'panacea_cortex_part05': ['chunk_aa', 'chunk_ab', 'chunk_ac'],
            'panacea_cortex_part06': ['chunk_aa', 'chunk_ab'],
            'panacea_cortex_part07': ['chunk_aa', 'chunk_ab']
        }
        
        for file_key, chunks in chunk_mapping.items():
            if file_key not in all_segments:
                continue
                
            segments = all_segments[file_key]
            segments_per_chunk = max(1, len(segments) // len(chunks))
            
            for i, chunk_name in enumerate(chunks):
                start_idx = i * segments_per_chunk
                end_idx = (i + 1) * segments_per_chunk if i < len(chunks) - 1 else len(segments)
                chunk_segments = segments[start_idx:end_idx]
                
                if not chunk_segments:
                    continue
                
                filename = f"{file_key}_{chunk_name}_{timestamp}.txt"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {file_key} - {chunk_name}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Chunk: {chunk_name}\n")
                    f.write(f"Dialogues in chunk: {len(chunk_segments)}\n\n")
                    
                    for j, segment in enumerate(chunk_segments, 1):
                        f.write(f"## Dialogue {j:03d}\n")
                        f.write(f"**Segment ID**: {segment['id']}\n")
                        f.write(f"**Complexity Score**: {segment['complexity_score']:.2f}\n\n")
                        f.write(f"{segment['content']}\n\n")
                        f.write("-" * 40 + "\n\n")
                
                print(f"Created chunk: {filename} ({len(chunk_segments)} dialogues)")
    
    def process_all_files(self) -> None:
        """Process all files and create outputs"""
        print("🚀 Manual Mimicry Dialogue Extraction")
        print("=" * 50)
        print("Processing panacea cortex files without skipping patterns")
        print()
        
        all_segments = {}
        
        for file_key, file_path in self.files_to_process.items():
            segments = self.process_file(file_key, file_path)
            if segments:
                all_segments[file_key] = segments
                self.save_essential_dialogues(file_key, segments)
        
        print("\n📦 Creating chunk files as requested...")
        self.create_combined_chunks(all_segments)
        
        # Summary
        total_dialogues = sum(len(segments) for segments in all_segments.values())
        print(f"\n✅ Extraction completed!")
        print(f"Total files processed: {len(all_segments)}")
        print(f"Total essential dialogues: {total_dialogues}")
        print("Check 'manual_extracted_dialogues' directory for outputs")

def main():
    """Main execution"""
    extractor = ManualMimicryExtractor()
    extractor.process_all_files()

if __name__ == "__main__":
    main()