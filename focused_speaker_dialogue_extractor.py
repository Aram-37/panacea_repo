#!/usr/bin/env python3
"""
Focused Speaker Dialogue Extractor
=================================

This tool extracts pure dialogues from panacea files with clear speaker transitions.
It breaks lines when speakers change and formats conversations for easy reading.

Requirements:
- Extract ONLY dialogues (no metadata or technical content)
- Break lines when speaker changes
- Format conversations for clear convenience
- Preserve chronological order
"""

import os
import re
import glob
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FocusedSpeakerDialogueExtractor:
    """Extractor for pure dialogues with clear speaker transitions"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.panacea_files = self._discover_panacea_files()
        
        # Speaker detection patterns
        self.speaker_patterns = {
            'teacher': [
                r'britkenko\s*[:：]\s*',
                r'성협\s*[:：]\s*',
                r'teacher\s*[:：]\s*',
                r'Cor\s*[:：]\s*',
                r'activate\s+',
                r'directive\s*[:：]\s*'
            ],
            'student': [
                r'github\s*copilot\s*[:：]\s*',
                r'copilot\s*[:：]\s*',
                r'assistant\s*[:：]\s*',
                r'ai\s*[:：]\s*',
                r'student\s*[:：]\s*',
                r'claude\s*[:：]\s*',
                r'chatgpt\s*[:：]\s*'
            ],
            'human': [
                r'user\s*[:：]\s*',
                r'human\s*[:：]\s*',
                r'you\s*[:：]\s*'
            ]
        }
        
        # Non-dialogue patterns to skip
        self.skip_patterns = [
            r'^\s*#',  # Headers
            r'^\s*\*\*[^*]+\*\*\s*$',  # Bold markers only
            r'^\s*-{3,}',  # Separators
            r'^\s*={3,}',  # Separators
            r'^\s*\d+\.\s*$',  # Numbers only
            r'^\s*\[\d{4}-\d{2}-\d{2}',  # Timestamps only
            r'^\s*```',  # Code blocks
            r'^\s*\*\s*$',  # Single asterisk
            r'^\s*\|\s*\|',  # Table formatting
            r'^\s*function\s*\(',  # Function definitions
            r'^\s*class\s+',  # Class definitions
            r'^\s*import\s+',  # Import statements
            r'^\s*from\s+',  # From imports
            r'^\s*def\s+',  # Function definitions
            r'^\s*\w+\s*=\s*[\[\{]',  # Variable assignments
            r'^\s*\d+\s*lines?\s*',  # Line count references
            r'^\s*source\s*:\s*',  # Source references
            r'^\s*file\s*:\s*',  # File references
            r'^\s*\w+\.(py|txt|md|json)\s*$',  # File names
            r'^\s*total\s+\w+\s*:\s*\d+',  # Statistics
            r'^\s*extracted\s+on\s*:',  # Extraction metadata
            r'^\s*generated\s*:',  # Generation metadata
        ]
        
        logger.info(f"Found {len(self.panacea_files)} panacea files for processing")
    
    def _discover_panacea_files(self) -> List[str]:
        """Discover all panacea files in the directory"""
        patterns = [
            'panacea*.txt',
            'panacea_*.txt',
            'panacea17_*.txt',
            'panacea_co_*.txt'
        ]
        
        files = []
        for pattern in patterns:
            files.extend(glob.glob(os.path.join(self.panacea_directory, pattern)))
        
        return sorted(files)
    
    def _detect_speaker(self, line: str) -> Optional[str]:
        """Detect speaker from line content"""
        line_lower = line.lower()
        
        # Check each speaker type
        for speaker_type, patterns in self.speaker_patterns.items():
            for pattern in patterns:
                if re.search(pattern, line_lower):
                    return speaker_type
        
        return None
    
    def _is_dialogue_line(self, line: str) -> bool:
        """Check if line contains actual dialogue content"""
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            return False
        
        # Skip lines matching skip patterns
        for pattern in self.skip_patterns:
            if re.match(pattern, stripped, re.IGNORECASE):
                return False
        
        # Must have reasonable length
        if len(stripped) < 10:
            return False
        
        # Check for dialogue indicators
        dialogue_indicators = [
            ':' in stripped,  # Speaker markers
            '?' in stripped,  # Questions
            '!' in stripped,  # Exclamations
            '"' in stripped,  # Quoted speech
            "'" in stripped and len(stripped) > 20,  # Quoted speech
            any(word in stripped.lower() for word in ['you', 'i', 'me', 'my', 'your', 'we', 'us']),  # Personal pronouns
            any(word in stripped.lower() for word in ['activate', 'cortex', 'panacea', 'rep', 'dialogue']),  # Key terms
            re.search(r'[가-힣]', stripped),  # Korean characters
        ]
        
        return any(dialogue_indicators)
    
    def _clean_dialogue_line(self, line: str) -> str:
        """Clean dialogue line for pure output"""
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', line.strip())
        
        # Remove metadata markers
        cleaned = re.sub(r'^\s*\[.*?\]\s*', '', cleaned)  # Remove [brackets]
        cleaned = re.sub(r'\*\*([^*]+)\*\*:', r'\1:', cleaned)  # **Label**: -> Label:
        cleaned = re.sub(r'^#+\s*', '', cleaned)  # Remove headers
        cleaned = re.sub(r'^-\s*', '', cleaned)  # Remove list markers
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)  # Remove numbered lists
        
        # Remove line references
        cleaned = re.sub(r'#\s*lines?\s*\d+-\d+.*?$', '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _extract_dialogues_from_file(self, filepath: str) -> List[Dict]:
        """Extract dialogues from a single file with speaker detection"""
        dialogues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return dialogues
        
        current_speaker = None
        current_dialogue = []
        line_number = 0
        
        for i, line in enumerate(lines):
            line_number = i + 1
            
            # Skip if not dialogue
            if not self._is_dialogue_line(line):
                continue
            
            # Clean the line
            cleaned_line = self._clean_dialogue_line(line)
            if not cleaned_line:
                continue
            
            # Detect speaker
            detected_speaker = self._detect_speaker(cleaned_line)
            
            # If speaker changed, save previous dialogue and start new one
            if detected_speaker and detected_speaker != current_speaker:
                # Save previous dialogue if exists
                if current_dialogue and current_speaker:
                    dialogue_text = '\n'.join(current_dialogue)
                    dialogues.append({
                        'speaker': current_speaker,
                        'content': dialogue_text,
                        'source_file': os.path.basename(filepath),
                        'line_start': line_number - len(current_dialogue),
                        'line_end': line_number - 1
                    })
                
                # Start new dialogue
                current_speaker = detected_speaker
                current_dialogue = [cleaned_line]
            else:
                # Continue current dialogue
                if current_speaker:
                    current_dialogue.append(cleaned_line)
                else:
                    # No speaker detected yet, treat as unknown
                    if not current_speaker:
                        current_speaker = 'unknown'
                        current_dialogue = [cleaned_line]
        
        # Save final dialogue
        if current_dialogue and current_speaker:
            dialogue_text = '\n'.join(current_dialogue)
            dialogues.append({
                'speaker': current_speaker,
                'content': dialogue_text,
                'source_file': os.path.basename(filepath),
                'line_start': line_number - len(current_dialogue) + 1,
                'line_end': line_number
            })
        
        return dialogues
    
    def _format_speaker_name(self, speaker: str) -> str:
        """Format speaker name for output"""
        speaker_names = {
            'teacher': '🎓 Teacher (britkenko/성협)',
            'student': '🤖 Student (AI/Copilot)',
            'human': '👤 Human (User)',
            'unknown': '❓ Unknown Speaker'
        }
        return speaker_names.get(speaker, f'❓ {speaker.title()}')
    
    def extract_all_dialogues(self) -> List[Dict]:
        """Extract all dialogues from all panacea files"""
        all_dialogues = []
        
        for filepath in self.panacea_files:
            logger.info(f"Processing: {os.path.basename(filepath)}")
            file_dialogues = self._extract_dialogues_from_file(filepath)
            all_dialogues.extend(file_dialogues)
            logger.info(f"  Extracted {len(file_dialogues)} dialogue segments")
        
        logger.info(f"Total dialogues extracted: {len(all_dialogues)}")
        return all_dialogues
    
    def generate_focused_output(self, dialogues: List[Dict], output_path: str) -> None:
        """Generate focused dialogue output with clear speaker transitions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"focused_speaker_dialogues_{timestamp}.txt"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Focused Speaker Dialogues - Clear Conversation Flow\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Dialogue Segments: {len(dialogues)}\n")
            f.write(f"Files Processed: {len(self.panacea_files)}\n\n")
            
            # Speaker distribution
            speaker_counts = {}
            for dialogue in dialogues:
                speaker = dialogue['speaker']
                speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
            
            f.write("## Speaker Distribution\n")
            for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {self._format_speaker_name(speaker)}: {count} segments\n")
            f.write("\n" + "=" * 60 + "\n\n")
            
            # Dialogue segments with clear speaker transitions
            current_speaker = None
            segment_number = 0
            
            for dialogue in dialogues:
                speaker = dialogue['speaker']
                content = dialogue['content']
                
                # Show speaker change clearly
                if speaker != current_speaker:
                    segment_number += 1
                    f.write(f"## Dialogue Segment {segment_number:03d}\n")
                    f.write(f"**{self._format_speaker_name(speaker)}**\n")
                    f.write(f"*Source: {dialogue['source_file']} (Lines {dialogue['line_start']}-{dialogue['line_end']})*\n\n")
                    current_speaker = speaker
                
                # Write dialogue content
                f.write(f"{content}\n\n")
                f.write("-" * 40 + "\n\n")
        
        logger.info(f"Focused dialogue output saved to: {filepath}")
    
    def generate_conversation_flow_output(self, dialogues: List[Dict], output_path: str) -> None:
        """Generate conversation flow output showing speaker transitions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_flow_{timestamp}.txt"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Conversation Flow - Speaker Transitions\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Dialogue Segments: {len(dialogues)}\n\n")
            
            # Group dialogues by source file for better organization
            files_dialogues = {}
            for dialogue in dialogues:
                source_file = dialogue['source_file']
                if source_file not in files_dialogues:
                    files_dialogues[source_file] = []
                files_dialogues[source_file].append(dialogue)
            
            # Process each file
            for source_file, file_dialogues in files_dialogues.items():
                f.write(f"## From File: {source_file}\n")
                f.write(f"Dialogue Segments: {len(file_dialogues)}\n\n")
                
                for i, dialogue in enumerate(file_dialogues, 1):
                    speaker = dialogue['speaker']
                    content = dialogue['content']
                    
                    # Show speaker and content
                    f.write(f"### {i:03d}. {self._format_speaker_name(speaker)}\n")
                    f.write(f"*Lines {dialogue['line_start']}-{dialogue['line_end']}*\n\n")
                    
                    # Format content with proper indentation
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip():
                            f.write(f"    {line}\n")
                    
                    f.write("\n" + "~" * 30 + "\n\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        logger.info(f"Conversation flow output saved to: {filepath}")

def main():
    """Main execution function"""
    print("🎯 Starting Focused Speaker Dialogue Extraction")
    print("=" * 50)
    
    # Initialize extractor
    extractor = FocusedSpeakerDialogueExtractor()
    
    # Extract dialogues
    print("🗣️  Extracting dialogues with speaker detection...")
    dialogues = extractor.extract_all_dialogues()
    
    # Generate outputs
    output_path = os.getcwd()
    print("📄 Generating focused dialogue output...")
    extractor.generate_focused_output(dialogues, output_path)
    
    print("🔄 Generating conversation flow output...")
    extractor.generate_conversation_flow_output(dialogues, output_path)
    
    print("\n✅ Focused speaker dialogue extraction completed!")
    print(f"Total dialogue segments: {len(dialogues)}")
    
    # Show speaker distribution
    speaker_counts = {}
    for dialogue in dialogues:
        speaker = dialogue['speaker']
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    
    print("\n📊 Speaker Distribution:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {speaker}: {count} segments")

if __name__ == "__main__":
    main()