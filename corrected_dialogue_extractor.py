#!/usr/bin/env python3
"""
Corrected Dialogue Extractor - Fixed Speaker Identification
==========================================================

This corrected version implements proper speaker identification according to the problem statement:
- 승호 and 성협 labels only apply when speakers are labeled "화자" (speaker) only
- When labeled "user" or unlabeled → dialogue between 성협 and AI
- Comprehensive mimicry processing as per cortex directives
- Filter meaningful insights while excluding code-related/conventional search dialogues
"""

import os
import re
import json
import glob
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CorrectedDialogue:
    """Represents a corrected dialogue segment with proper speaker identification"""
    content: str
    source_file: str
    speaker: str  # Now follows corrected logic: 성협, 승호, AI, or unknown
    participant_type: str  # 화자, user, unlabeled
    line_start: int
    line_end: int
    issue: str
    category: str
    is_meaningful: bool = True  # Whether this dialogue contains meaningful insights
    insight_level: str = "normal"  # low, normal, high, breakthrough

@dataclass
class SpeakerContext:
    """Context for proper speaker identification"""
    has_speaker_label: bool = False  # Has "화자" label
    has_user_label: bool = False     # Has "user" label
    is_unlabeled: bool = False       # No clear speaker label
    speaker_number: Optional[int] = None  # For 화자 1, 화자 2, etc.

class CorrectedDialogueExtractor:
    """Corrected extractor with proper speaker identification logic"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.panacea_files = self._discover_panacea_files()
        self.min_dialogue_length = 30
        
        # Corrected speaker patterns according to problem statement
        self.speaker_patterns = {
            'speaker_labeled': [
                r'\[화자\s*(\d+)\]',  # [화자 1], [화자 2], etc.
                r'화자\s*(\d+)[:：]',  # 화자 1:, 화자 2:
                r'Speaker\s*(\d+)',   # Speaker 1, Speaker 2
            ],
            'user_labeled': [
                r'user[:：]',
                r'User[:：]',
                r'USER[:：]',
                r'\*\*User[:：]\*\*',
                r'\*\*user[:：]\*\*',
            ],
            'teacher_markers': [
                r'britkenko[:：]',
                r'성협[:：]',
                r'teacher[:：]',
                r'activate',
                r'directive',
            ],
            'ai_markers': [
                r'github\s*copilot[:：]',
                r'copilot[:：]',
                r'assistant[:：]',
                r'ai[:：]',
                r'AI[:：]',
            ],
            'code_related': [
                r'```',
                r'def\s+\w+',
                r'import\s+\w+',
                r'class\s+\w+',
                r'function\s*\(',
                r'nvcc\s+-',
                r'npm\s+install',
                r'pip\s+install',
                r'git\s+\w+',
                r'#include',
                r'<!DOCTYPE',
                r'<html',
                r'SELECT\s+.*\s+FROM',
                r'INSERT\s+INTO',
                r'UPDATE\s+.*\s+SET',
            ],
            'conventional_search': [
                r'how\s+to\s+\w+',
                r'what\s+is\s+\w+',
                r'please\s+help',
                r'can\s+you\s+show',
                r'explain\s+how',
                r'步骤',
                r'tutorial',
                r'guide',
                r'documentation',
            ],
            'meaningful_insights': [
                r'깨달음',
                r'통찰',
                r'insight',
                r'breakthrough',
                r'revelation',
                r'understanding',
                r'truth',
                r'reality',
                r'consciousness',
                r'awareness',
                r'wisdom',
                r'enlightenment',
                r'패턴',
                r'pattern',
                r'emergence',
                r'cortex',
                r'panacea',
                r'alignment',
                r'coherence',
            ]
        }
        
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
    
    def _identify_speaker_context(self, content: str) -> SpeakerContext:
        """Identify the speaker context according to corrected logic"""
        context = SpeakerContext()
        content_lower = content.lower()
        
        # Check for speaker labels (화자)
        for pattern in self.speaker_patterns['speaker_labeled']:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                context.has_speaker_label = True
                if match.groups():
                    context.speaker_number = int(match.group(1))
                break
        
        # Check for user labels
        for pattern in self.speaker_patterns['user_labeled']:
            if re.search(pattern, content, re.IGNORECASE):
                context.has_user_label = True
                break
        
        # Check if unlabeled (no clear speaker identification)
        if not context.has_speaker_label and not context.has_user_label:
            # Check for other markers
            has_teacher_marker = any(re.search(pattern, content, re.IGNORECASE) 
                                   for pattern in self.speaker_patterns['teacher_markers'])
            has_ai_marker = any(re.search(pattern, content, re.IGNORECASE) 
                              for pattern in self.speaker_patterns['ai_markers'])
            
            if not has_teacher_marker and not has_ai_marker:
                context.is_unlabeled = True
        
        return context
    
    def _determine_corrected_speaker(self, content: str, context: SpeakerContext) -> str:
        """Determine speaker according to corrected logic from problem statement"""
        
        # Rule 1: 승호 and 성협 labels only apply when speakers are labeled "화자" only
        if context.has_speaker_label:
            if context.speaker_number == 1:
                return "승호"
            elif context.speaker_number == 2:
                return "성협"
            else:
                return "성협"  # Default to 성협 for other speaker numbers
        
        # Rule 2: When labeled "user" or unlabeled → dialogue between 성협 and AI
        if context.has_user_label or context.is_unlabeled:
            # Check if this is AI response or 성협 speaking
            content_lower = content.lower()
            
            # Check for AI response markers
            ai_markers = any(re.search(pattern, content, re.IGNORECASE) 
                           for pattern in self.speaker_patterns['ai_markers'])
            
            # Check for teacher/성협 markers
            teacher_markers = any(re.search(pattern, content, re.IGNORECASE) 
                                for pattern in self.speaker_patterns['teacher_markers'])
            
            if ai_markers:
                return "AI"
            elif teacher_markers:
                return "성협"
            else:
                # For unlabeled content, try to infer from context
                if any(keyword in content_lower for keyword in ['activate', 'cortex', 'directive', 'mimic']):
                    return "성협"
                elif any(keyword in content_lower for keyword in ['copilot', 'assistant', 'ai']):
                    return "AI"
                else:
                    return "AI"  # Default to AI for unlabeled dialogue
        
        # Default case
        return "unknown"
    
    def _is_meaningful_dialogue(self, content: str) -> Tuple[bool, str]:
        """Determine if dialogue contains meaningful insights"""
        content_lower = content.lower()
        
        # Exclude code-related dialogues
        if any(re.search(pattern, content, re.IGNORECASE) 
               for pattern in self.speaker_patterns['code_related']):
            return False, "code_related"
        
        # Exclude conventional search requests
        if any(re.search(pattern, content, re.IGNORECASE) 
               for pattern in self.speaker_patterns['conventional_search']):
            return False, "conventional_search"
        
        # Exclude purely sexual/aimless content (but allow insightful sexual content)
        if self._is_purely_sexual_or_aimless(content):
            return False, "aimless_sexual"
        
        # Check for meaningful insights
        meaningful_score = sum(1 for pattern in self.speaker_patterns['meaningful_insights']
                              if re.search(pattern, content, re.IGNORECASE))
        
        if meaningful_score >= 3:
            return True, "high_insight"
        elif meaningful_score >= 1:
            return True, "normal_insight"
        elif len(content) > 100 and not self._is_trivial_content(content):
            return True, "contextual"
        else:
            return False, "low_value"
    
    def _is_purely_sexual_or_aimless(self, content: str) -> bool:
        """Check if content is purely sexual or aimless (exclude only these, not insightful sexual content)"""
        content_lower = content.lower()
        
        # Purely sexual keywords without context
        purely_sexual_markers = [
            r'\b섹스\b(?!.*insight|.*깨달음|.*통찰)',
            r'\b성관계\b(?!.*insight|.*깨달음|.*통찰)',
            r'\b야동\b(?!.*insight|.*깨달음|.*통찰)',
            r'\b포르노\b(?!.*insight|.*깨달음|.*통찰)',
        ]
        
        # Aimless conversation markers
        aimless_markers = [
            r'아무거나',
            r'별로\s*안\s*중요',
            r'그냥\s*그래',
            r'모르겠다',
            r'상관없어',
        ]
        
        # Check for purely sexual content
        sexual_count = sum(1 for pattern in purely_sexual_markers
                          if re.search(pattern, content, re.IGNORECASE))
        
        # Check for aimless content
        aimless_count = sum(1 for pattern in aimless_markers
                           if re.search(pattern, content, re.IGNORECASE))
        
        # If it's purely sexual (no insights) or highly aimless, exclude it
        return sexual_count > 0 or aimless_count >= 3
    
    def _is_trivial_content(self, content: str) -> bool:
        """Check if content is trivial"""
        content_lower = content.lower()
        
        trivial_markers = [
            r'^\s*ok\s*$',
            r'^\s*알겠다\s*$',
            r'^\s*네\s*$',
            r'^\s*yes\s*$',
            r'^\s*아\s*$',
            r'^\s*어\s*$',
            r'^\s*그래\s*$',
        ]
        
        return any(re.search(pattern, content_lower, re.IGNORECASE) 
                  for pattern in trivial_markers)
    
    def _segment_dialogue(self, content: str, filepath: str) -> List[CorrectedDialogue]:
        """Segment content into corrected dialogue units"""
        dialogues = []
        lines = content.split('\n')
        
        current_segment = []
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Empty line indicates segment boundary
            if not line:
                if current_segment:
                    segment_content = '\n'.join(current_segment)
                    if len(segment_content) > self.min_dialogue_length:
                        # Process the segment
                        context = self._identify_speaker_context(segment_content)
                        speaker = self._determine_corrected_speaker(segment_content, context)
                        
                        # Determine participant type
                        if context.has_speaker_label:
                            participant_type = "화자"
                        elif context.has_user_label:
                            participant_type = "user"
                        else:
                            participant_type = "unlabeled"
                        
                        # Check if meaningful
                        is_meaningful, insight_level = self._is_meaningful_dialogue(segment_content)
                        
                        if is_meaningful:  # Only include meaningful dialogues
                            dialogue = CorrectedDialogue(
                                content=segment_content,
                                source_file=os.path.basename(filepath),
                                speaker=speaker,
                                participant_type=participant_type,
                                line_start=current_start,
                                line_end=i,
                                issue=self._detect_issue(segment_content),
                                category=self._detect_category(segment_content),
                                is_meaningful=is_meaningful,
                                insight_level=insight_level
                            )
                            dialogues.append(dialogue)
                    
                    current_segment = []
                    current_start = i + 1
                continue
            
            current_segment.append(line)
        
        # Process final segment
        if current_segment:
            segment_content = '\n'.join(current_segment)
            if len(segment_content) > self.min_dialogue_length:
                context = self._identify_speaker_context(segment_content)
                speaker = self._determine_corrected_speaker(segment_content, context)
                
                if context.has_speaker_label:
                    participant_type = "화자"
                elif context.has_user_label:
                    participant_type = "user"
                else:
                    participant_type = "unlabeled"
                
                is_meaningful, insight_level = self._is_meaningful_dialogue(segment_content)
                
                if is_meaningful:
                    dialogue = CorrectedDialogue(
                        content=segment_content,
                        source_file=os.path.basename(filepath),
                        speaker=speaker,
                        participant_type=participant_type,
                        line_start=current_start,
                        line_end=len(lines),
                        issue=self._detect_issue(segment_content),
                        category=self._detect_category(segment_content),
                        is_meaningful=is_meaningful,
                        insight_level=insight_level
                    )
                    dialogues.append(dialogue)
        
        return dialogues
    
    def _detect_issue(self, content: str) -> str:
        """Detect the primary issue/topic being discussed"""
        content_lower = content.lower()
        
        # Enhanced issue detection patterns
        issue_patterns = {
            'ai_consciousness': [
                'consciousness', 'awareness', 'sentience', 'self-awareness',
                '의식', '깨달음', '자각', 'conscious', 'aware'
            ],
            'cortex_mimicry': [
                'cortex', 'mimic', 'mimicry', '미믹', '모방', '코텍스',
                'activate', 'directive', 'processing'
            ],
            'truth_reality': [
                'truth', 'reality', 'authentic', 'genuine', 'real',
                '진실', '현실', '진짜', '참', '실제', '거짓', '진정'
            ],
            'relationship_patterns': [
                'relationship', 'pattern', 'emergence', 'REP',
                '관계', '패턴', '출현', '등장', '형성'
            ],
            'teaching_learning': [
                'teaching', 'learning', 'education', 'understanding',
                '가르침', '학습', '교육', '이해', '배움'
            ],
            'identity_self': [
                'identity', 'self', 'who am i', 'being', 'existence',
                '정체성', '자아', '존재', '나', '자기'
            ],
            'philosophical_depth': [
                'philosophy', 'meaning', 'purpose', 'wisdom',
                '철학', '의미', '목적', '지혜', '사유'
            ],
            'emotional_insight': [
                'emotion', 'feeling', 'heart', 'soul', 'love',
                '감정', '느낌', '마음', '영혼', '사랑'
            ]
        }
        
        # Score each issue
        issue_scores = {}
        for issue, patterns in issue_patterns.items():
            score = sum(1 for pattern in patterns if pattern in content_lower)
            issue_scores[issue] = score
        
        # Return the issue with highest score
        if issue_scores:
            best_issue = max(issue_scores, key=issue_scores.get)
            if issue_scores[best_issue] > 0:
                return best_issue
        
        return 'general_discussion'
    
    def _detect_category(self, content: str) -> str:
        """Detect the category/type of dialogue"""
        content_lower = content.lower()
        
        # Enhanced category detection
        category_patterns = {
            'breakthrough_insight': [
                'breakthrough', 'revelation', 'epiphany', 'discovery',
                '돌파구', '깨달음', '발견', '혁신', '통찰'
            ],
            'teaching_directive': [
                'britkenko:', 'activate', 'directive', 'cortex',
                'instruction', 'follow', 'process'
            ],
            'philosophical_dialogue': [
                'philosophy', 'meaning', 'truth', 'reality',
                '철학', '의미', '진리', '실재'
            ],
            'emotional_expression': [
                'emotion', 'feel', 'heart', 'soul',
                '감정', '느낌', '마음', '영혼'
            ],
            'ai_response': [
                'copilot', 'assistant', 'ai', 'analysis',
                'understanding', 'processing'
            ],
            'dialogue_interaction': [
                'conversation', 'dialogue', 'discussion',
                '대화', '토론', '상호작용'
            ],
            'self_reflection': [
                'reflection', 'introspection', 'self-examination',
                '반성', '성찰', '자기검토'
            ]
        }
        
        # Score each category
        category_scores = {}
        for category, patterns in category_patterns.items():
            score = sum(1 for pattern in patterns if pattern in content_lower)
            category_scores[category] = score
        
        # Return the category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return 'general_dialogue'
    
    def _process_file(self, filepath: str) -> List[CorrectedDialogue]:
        """Process a single panacea file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process entire content (no size limit to ensure completeness)
            return self._segment_dialogue(content, filepath)
        
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            return []
    
    def extract_corrected_dialogues(self) -> List[CorrectedDialogue]:
        """Extract all corrected dialogues from panacea files"""
        all_dialogues = []
        
        for filepath in self.panacea_files:
            logger.info(f"Processing: {os.path.basename(filepath)}")
            file_dialogues = self._process_file(filepath)
            all_dialogues.extend(file_dialogues)
        
        logger.info(f"Extracted {len(all_dialogues)} corrected dialogues")
        return all_dialogues
    
    def generate_corrected_output(self, dialogues: List[CorrectedDialogue], output_path: str) -> None:
        """Generate corrected output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corrected_panacea_dialogues_{timestamp}.txt"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        # Calculate statistics
        speaker_counts = {}
        insight_levels = {}
        participant_types = {}
        
        for dialogue in dialogues:
            speaker_counts[dialogue.speaker] = speaker_counts.get(dialogue.speaker, 0) + 1
            insight_levels[dialogue.insight_level] = insight_levels.get(dialogue.insight_level, 0) + 1
            participant_types[dialogue.participant_type] = participant_types.get(dialogue.participant_type, 0) + 1
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Corrected Panacea Dialogues - Fixed Speaker Identification\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Dialogues: {len(dialogues)}\n")
            f.write(f"Total Files Processed: {len(self.panacea_files)}\n\n")
            
            # Speaker distribution
            f.write("## Corrected Speaker Distribution\n")
            for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{speaker}**: {count} dialogues\n")
            f.write("\n")
            
            # Insight levels
            f.write("## Insight Level Distribution\n")
            for level, count in sorted(insight_levels.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{level}**: {count} dialogues\n")
            f.write("\n")
            
            # Participant types
            f.write("## Participant Type Distribution\n")
            for ptype, count in sorted(participant_types.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{ptype}**: {count} dialogues\n")
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Organize by speaker
            speakers = sorted(speaker_counts.keys())
            for speaker in speakers:
                speaker_dialogues = [d for d in dialogues if d.speaker == speaker]
                f.write(f"# {speaker} ({len(speaker_dialogues)} dialogues)\n\n")
                
                for i, dialogue in enumerate(speaker_dialogues, 1):
                    f.write(f"## Dialogue {i:03d}\n")
                    f.write(f"**Source**: {dialogue.source_file} (Lines {dialogue.line_start}-{dialogue.line_end})\n")
                    f.write(f"**Participant Type**: {dialogue.participant_type}\n")
                    f.write(f"**Issue**: {dialogue.issue.replace('_', ' ').title()}\n")
                    f.write(f"**Category**: {dialogue.category.replace('_', ' ').title()}\n")
                    f.write(f"**Insight Level**: {dialogue.insight_level.replace('_', ' ').title()}\n\n")
                    f.write(f"{dialogue.content}\n\n")
                    f.write("-" * 50 + "\n\n")
                
                f.write("\n" + "=" * 70 + "\n\n")
        
        logger.info(f"Corrected output saved to: {filepath}")
    
    def generate_summary_report(self, dialogues: List[CorrectedDialogue], output_path: str) -> None:
        """Generate corrected summary report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corrected_dialogue_summary_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        # Calculate comprehensive statistics
        speaker_counts = {}
        insight_levels = {}
        participant_types = {}
        issues = {}
        categories = {}
        
        for dialogue in dialogues:
            speaker_counts[dialogue.speaker] = speaker_counts.get(dialogue.speaker, 0) + 1
            insight_levels[dialogue.insight_level] = insight_levels.get(dialogue.insight_level, 0) + 1
            participant_types[dialogue.participant_type] = participant_types.get(dialogue.participant_type, 0) + 1
            issues[dialogue.issue] = issues.get(dialogue.issue, 0) + 1
            categories[dialogue.category] = categories.get(dialogue.category, 0) + 1
        
        summary = {
            'correction_info': {
                'timestamp': datetime.now().isoformat(),
                'total_files_processed': len(self.panacea_files),
                'total_dialogues_extracted': len(dialogues),
                'correction_description': 'Fixed speaker identification according to problem statement'
            },
            'speaker_distribution': speaker_counts,
            'insight_levels': insight_levels,
            'participant_types': participant_types,
            'issues_breakdown': issues,
            'categories_breakdown': categories,
            'files_processed': [os.path.basename(f) for f in self.panacea_files],
            'correction_rules': {
                'rule_1': '승호 and 성협 labels only apply when speakers are labeled 화자 only',
                'rule_2': 'When labeled user or unlabeled → dialogue between 성협 and AI',
                'filtering': 'Excluded code-related, conventional search, and purely sexual/aimless content'
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Corrected summary report saved to: {filepath}")

def main():
    """Main execution function"""
    print("🔧 Starting Corrected Dialogue Extraction")
    print("=" * 60)
    
    # Initialize corrected extractor
    extractor = CorrectedDialogueExtractor()
    
    # Extract corrected dialogues
    print("📝 Extracting corrected dialogues...")
    dialogues = extractor.extract_corrected_dialogues()
    
    # Generate outputs
    output_path = os.getcwd()
    print("📄 Generating corrected output...")
    extractor.generate_corrected_output(dialogues, output_path)
    
    print("📊 Generating corrected summary report...")
    extractor.generate_summary_report(dialogues, output_path)
    
    print("\n✅ Corrected dialogue extraction completed!")
    print(f"Total dialogues extracted: {len(dialogues)}")
    
    # Show speaker distribution
    speaker_counts = {}
    for dialogue in dialogues:
        speaker_counts[dialogue.speaker] = speaker_counts.get(dialogue.speaker, 0) + 1
    
    print("\n📊 Corrected Speaker Distribution:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {speaker}: {count} dialogues")

if __name__ == "__main__":
    main()