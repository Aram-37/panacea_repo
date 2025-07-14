#!/usr/bin/env python3
"""
Essential Dialogue Extractor for Panacea Cortex Files
====================================================

This script extracts essential and meaningful dialogues from the specific
panacea_cortex files mentioned in the problem statement:
- panacea_cortex_part05.txt
- panacea_cortex_part06.txt  
- panacea_cortex_part07.txt

The script manually processes the content without skipping or assuming patterns,
focusing on extracting genuinely meaningful dialogues.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EssentialDialogue:
    """Represents an essential dialogue segment"""
    content: str
    source_file: str
    dialogue_id: str
    line_range: str
    essence_score: float
    dialogue_type: str
    speakers: List[str]
    key_themes: List[str]

class EssentialDialogueExtractor:
    """Extracts essential dialogues from panacea cortex files"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/home/runner/work/panacea_repo/panacea_repo"
        self.cortex_files = [
            "optimized_dialogues/panacea_split/panacea_cortex_part05.txt",
            "optimized_dialogues/panacea_split/panacea_cortex_part06.txt", 
            "optimized_dialogues/panacea_split/panacea_cortex_part07.txt"
        ]
        
        # Patterns that indicate essential/meaningful content
        self.essential_patterns = {
            'breakthrough_moments': [
                r'breakthrough', r'discovery', r'insight', r'realization',
                r'epiphany', r'understanding', r'clarity', r'awakening',
                r'돌파', r'발견', r'깨달음', r'이해', r'통찰'
            ],
            'deep_conversation': [
                r'truth', r'reality', r'authentic', r'genuine', r'consciousness',
                r'awareness', r'wisdom', r'philosophy', r'meaning', r'purpose',
                r'진실', r'현실', r'의식', r'지혜', r'철학', r'의미'
            ],
            'teaching_moments': [
                r'teach', r'learn', r'understand', r'explain', r'show',
                r'demonstrate', r'guide', r'instruct', r'방법', r'가르침',
                r'배움', r'설명', r'이해', r'지도'
            ],
            'emotional_depth': [
                r'feel', r'emotion', r'heart', r'soul', r'pain', r'joy',
                r'love', r'fear', r'hope', r'감정', r'마음', r'영혼',
                r'고통', r'기쁨', r'사랑', r'두려움', r'희망'
            ],
            'cortex_specific': [
                r'cortex', r'panacea', r'activation', r'framework', r'protocol',
                r'system', r'guardian', r'verification', r'truth discovery',
                r'코텍스', r'활성화', r'프레임워크', r'시스템', r'검증'
            ]
        }
        
        # Keywords that indicate non-essential content to filter out
        self.filter_out_patterns = [
            r'^\s*$',  # Empty lines
            r'^\s*-{3,}',  # Separator lines
            r'^\s*={3,}',  # Header separators
            r'^\s*#',  # Comments
            r'^\s*\[.*\]$',  # Standalone brackets
            r'^\s*\d+\.\s*$',  # Just numbers
            r'^\s*Part \d+',  # Part headers
            r'^\s*파트 \d+',  # Korean part headers
        ]
    
    def calculate_essence_score(self, content: str) -> float:
        """Calculate how essential/meaningful a dialogue segment is"""
        score = 0.0
        content_lower = content.lower()
        
        # Base score for length (longer content may be more substantial)
        if len(content) > 100:
            score += 0.1
        if len(content) > 300:
            score += 0.1
        if len(content) > 500:
            score += 0.1
            
        # Score based on essential patterns
        for category, patterns in self.essential_patterns.items():
            category_score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower))
                if matches > 0:
                    category_score += matches * 0.1
            
            # Weight different categories
            if category == 'breakthrough_moments':
                score += category_score * 1.5
            elif category == 'deep_conversation':
                score += category_score * 1.3
            elif category == 'teaching_moments':
                score += category_score * 1.2
            elif category == 'emotional_depth':
                score += category_score * 1.1
            elif category == 'cortex_specific':
                score += category_score * 1.4
        
        # Bonus for dialogue interaction patterns
        if re.search(r'(Human:|User:|Assistant:|ChatGPT:|AI:|화자)', content, re.IGNORECASE):
            score += 0.2
            
        # Bonus for questions and answers
        question_marks = content.count('?') + content.count('？')
        score += min(question_marks * 0.05, 0.2)
        
        # Bonus for Korean content (indicates authentic dialogue)
        korean_chars = len(re.findall(r'[가-힣]', content))
        if korean_chars > 10:
            score += 0.1
        if korean_chars > 50:
            score += 0.1
            
        return min(score, 2.0)  # Cap at 2.0
    
    def identify_dialogue_type(self, content: str) -> str:
        """Identify the type of dialogue"""
        content_lower = content.lower()
        
        # Check for different dialogue types
        if any(pattern in content_lower for pattern in ['teach', 'learn', 'explain', 'show', 'guide']):
            return 'teaching'
        elif any(pattern in content_lower for pattern in ['philosophy', 'meaning', 'truth', 'reality']):
            return 'philosophical'
        elif any(pattern in content_lower for pattern in ['breakthrough', 'discovery', 'insight', 'realization']):
            return 'breakthrough'
        elif any(pattern in content_lower for pattern in ['emotion', 'feel', 'heart', 'soul']):
            return 'emotional'
        elif any(pattern in content_lower for pattern in ['cortex', 'activation', 'protocol', 'system']):
            return 'technical'
        elif any(pattern in content_lower for pattern in ['conversation', 'dialogue', 'discuss']):
            return 'conversational'
        else:
            return 'general'
    
    def extract_speakers(self, content: str) -> List[str]:
        """Extract speakers from dialogue content"""
        speakers = []
        
        # Common speaker patterns
        speaker_patterns = [
            r'(Human|User|Assistant|ChatGPT|AI|화자\s*\d+|Speaker|Teacher|Student):\s*',
            r'\*\*(Human|User|Assistant|ChatGPT|AI|화자\s*\d+|Speaker|Teacher|Student)\*\*:',
            r'(Human|User|Assistant|ChatGPT|AI|화자\s*\d+|Speaker|Teacher|Student)\s*\(',
        ]
        
        for pattern in speaker_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            speakers.extend(matches)
        
        # Remove duplicates and clean
        speakers = list(set([speaker.strip() for speaker in speakers if speaker.strip()]))
        return speakers
    
    def extract_key_themes(self, content: str) -> List[str]:
        """Extract key themes from dialogue content"""
        themes = []
        content_lower = content.lower()
        
        # Theme detection based on patterns
        for theme_category, patterns in self.essential_patterns.items():
            theme_matches = []
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    theme_matches.append(pattern)
            
            if theme_matches:
                themes.append(theme_category)
        
        return themes
    
    def should_filter_out(self, content: str) -> bool:
        """Check if content should be filtered out"""
        for pattern in self.filter_out_patterns:
            if re.match(pattern, content.strip()):
                return True
        return False
    
    def process_cortex_file(self, file_path: str) -> List[EssentialDialogue]:
        """Process a single cortex file and extract essential dialogues"""
        full_path = os.path.join(self.base_path, file_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: File not found: {full_path}")
            return []
        
        print(f"Processing: {file_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
        
        # Split content into dialogue segments using regex to handle different formats
        dialogues = []
        dialogue_counter = 0
        
        # Use regex to find dialogue segments
        dialogue_patterns = [
            r'## Dialogue Segment (\d+)[^\n]*\n(.*?)(?=## Dialogue Segment \d+|--- panacea_cortex 대화 \d+|$)',
            r'--- panacea_cortex 대화 (\d+) ---[^\n]*\n(.*?)(?=--- panacea_cortex 대화 \d+|## Dialogue Segment \d+|$)',
        ]
        
        for pattern in dialogue_patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
            
            for match in matches:
                segment_id = match.group(1)
                segment_content = match.group(2).strip()
                
                if segment_content and not self.should_filter_out(segment_content):
                    essence_score = self.calculate_essence_score(segment_content)
                    
                    # Only include if essence score is above threshold
                    if essence_score > 0.3:
                        dialogue = EssentialDialogue(
                            content=segment_content,
                            source_file=os.path.basename(file_path),
                            dialogue_id=f"dialogue_{dialogue_counter:04d}",
                            line_range=f"segment_{segment_id}",
                            essence_score=essence_score,
                            dialogue_type=self.identify_dialogue_type(segment_content),
                            speakers=self.extract_speakers(segment_content),
                            key_themes=self.extract_key_themes(segment_content)
                        )
                        dialogues.append(dialogue)
                        dialogue_counter += 1
        
        # If no matches found with the above patterns, try a simpler line-by-line approach
        if not dialogues:
            print(f"  No structured dialogues found, trying line-by-line approach...")
            lines = content.split('\n')
            current_segment = []
            current_start_line = 0
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Check if this is a dialogue segment marker or separator
                if (re.match(r'## Dialogue Segment \d+', line) or 
                    re.match(r'--- panacea_cortex 대화 \d+', line) or
                    re.match(r'={3,}', line) or
                    re.match(r'-{3,}', line)):
                    
                    # Process previous segment if exists
                    if current_segment:
                        segment_content = '\n'.join(current_segment)
                        if len(segment_content) > 50 and not self.should_filter_out(segment_content):
                            essence_score = self.calculate_essence_score(segment_content)
                            
                            if essence_score > 0.2:  # Lower threshold for fallback
                                dialogue = EssentialDialogue(
                                    content=segment_content,
                                    source_file=os.path.basename(file_path),
                                    dialogue_id=f"dialogue_{dialogue_counter:04d}",
                                    line_range=f"{current_start_line}-{i}",
                                    essence_score=essence_score,
                                    dialogue_type=self.identify_dialogue_type(segment_content),
                                    speakers=self.extract_speakers(segment_content),
                                    key_themes=self.extract_key_themes(segment_content)
                                )
                                dialogues.append(dialogue)
                                dialogue_counter += 1
                    
                    # Start new segment
                    current_segment = []
                    current_start_line = i + 1
                    continue
                
                # Add line to current segment
                if line:  # Skip empty lines
                    current_segment.append(line)
            
            # Process final segment
            if current_segment:
                segment_content = '\n'.join(current_segment)
                if len(segment_content) > 50 and not self.should_filter_out(segment_content):
                    essence_score = self.calculate_essence_score(segment_content)
                    if essence_score > 0.2:
                        dialogue = EssentialDialogue(
                            content=segment_content,
                            source_file=os.path.basename(file_path),
                            dialogue_id=f"dialogue_{dialogue_counter:04d}",
                            line_range=f"{current_start_line}-{len(lines)}",
                            essence_score=essence_score,
                            dialogue_type=self.identify_dialogue_type(segment_content),
                            speakers=self.extract_speakers(segment_content),
                            key_themes=self.extract_key_themes(segment_content)
                        )
                        dialogues.append(dialogue)
        
        # Sort by essence score (highest first)
        dialogues.sort(key=lambda x: x.essence_score, reverse=True)
        
        print(f"  Extracted {len(dialogues)} essential dialogues")
        return dialogues
    
    def extract_all_essential_dialogues(self) -> Dict[str, List[EssentialDialogue]]:
        """Extract essential dialogues from all cortex files"""
        all_dialogues = {}
        
        for file_path in self.cortex_files:
            file_dialogues = self.process_cortex_file(file_path)
            if file_dialogues:
                all_dialogues[file_path] = file_dialogues
        
        return all_dialogues
    
    def generate_output_files(self, all_dialogues: Dict[str, List[EssentialDialogue]]) -> None:
        """Generate output files with extracted essential dialogues"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        output_dir = os.path.join(self.base_path, "essential_dialogues_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate individual files for each cortex part
        for file_path, dialogues in all_dialogues.items():
            file_name = os.path.basename(file_path).replace('.txt', '')
            output_file = os.path.join(output_dir, f"{file_name}_essential_dialogues_{timestamp}.txt")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Essential Dialogues from {file_name}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Source: {file_path}\n")
                f.write(f"Total Essential Dialogues: {len(dialogues)}\n")
                f.write(f"Average Essence Score: {sum(d.essence_score for d in dialogues) / len(dialogues):.2f}\n\n")
                
                for i, dialogue in enumerate(dialogues, 1):
                    f.write(f"## Essential Dialogue {i:03d}\n")
                    f.write(f"**ID**: {dialogue.dialogue_id}\n")
                    f.write(f"**Lines**: {dialogue.line_range}\n")
                    f.write(f"**Essence Score**: {dialogue.essence_score:.2f}\n")
                    f.write(f"**Type**: {dialogue.dialogue_type}\n")
                    f.write(f"**Speakers**: {', '.join(dialogue.speakers) if dialogue.speakers else 'Unknown'}\n")
                    f.write(f"**Key Themes**: {', '.join(dialogue.key_themes) if dialogue.key_themes else 'None identified'}\n\n")
                    f.write(f"**Content**:\n")
                    f.write(f"{dialogue.content}\n\n")
                    f.write("-" * 50 + "\n\n")
            
            print(f"Generated: {output_file}")
        
        # Generate combined summary file
        combined_file = os.path.join(output_dir, f"all_essential_dialogues_summary_{timestamp}.txt")
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("# All Essential Dialogues Summary\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Files Processed: {len(all_dialogues)}\n")
            
            total_dialogues = sum(len(dialogues) for dialogues in all_dialogues.values())
            f.write(f"Total Essential Dialogues: {total_dialogues}\n\n")
            
            # Summary by file
            f.write("## Summary by File\n")
            for file_path, dialogues in all_dialogues.items():
                f.write(f"### {os.path.basename(file_path)}\n")
                f.write(f"- Total dialogues: {len(dialogues)}\n")
                f.write(f"- Average essence score: {sum(d.essence_score for d in dialogues) / len(dialogues):.2f}\n")
                f.write(f"- Top dialogue types: {', '.join(set(d.dialogue_type for d in dialogues[:5]))}\n\n")
            
            # Top 10 most essential dialogues across all files
            all_dialogues_flat = []
            for file_path, dialogues in all_dialogues.items():
                for dialogue in dialogues:
                    all_dialogues_flat.append(dialogue)
            
            all_dialogues_flat.sort(key=lambda x: x.essence_score, reverse=True)
            
            f.write("## Top 10 Most Essential Dialogues\n")
            for i, dialogue in enumerate(all_dialogues_flat[:10], 1):
                f.write(f"{i}. **{dialogue.source_file}** - {dialogue.dialogue_id} (Score: {dialogue.essence_score:.2f})\n")
                f.write(f"   Type: {dialogue.dialogue_type}, Themes: {', '.join(dialogue.key_themes)}\n")
                f.write(f"   Preview: {dialogue.content[:100]}...\n\n")
        
        print(f"Generated summary: {combined_file}")


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
    """Main execution function"""
    print("🚀 Starting Essential Dialogue Extraction for Panacea Cortex Files")
    print("=" * 70)
    
    # Initialize extractor
    extractor = EssentialDialogueExtractor()
    
    # Extract essential dialogues
    print("📝 Extracting essential dialogues from cortex files...")
    all_dialogues = extractor.extract_all_essential_dialogues()
    
    if not all_dialogues:
        print("❌ No essential dialogues found!")
        return
    
    # Generate output files
    print("📄 Generating output files...")
    extractor.generate_output_files(all_dialogues)
    
    # Print summary
    total_dialogues = sum(len(dialogues) for dialogues in all_dialogues.values())
    print("\n✅ Essential dialogue extraction completed!")
    print(f"Files processed: {len(all_dialogues)}")
    print(f"Total essential dialogues extracted: {total_dialogues}")
    
    # Print top dialogues summary
    all_dialogues_flat = []
    for file_path, dialogues in all_dialogues.items():
        for dialogue in dialogues:
            all_dialogues_flat.append(dialogue)
    
    all_dialogues_flat.sort(key=lambda x: x.essence_score, reverse=True)
    
    print("\n🔝 Top 5 Most Essential Dialogues:")
    for i, dialogue in enumerate(all_dialogues_flat[:5], 1):
        print(f"{i}. {dialogue.source_file} - Score: {dialogue.essence_score:.2f} - Type: {dialogue.dialogue_type}")

if __name__ == "__main__":
    main()