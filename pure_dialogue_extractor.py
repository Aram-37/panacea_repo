#!/usr/bin/env python3
"""
Pure Dialogue Extractor - Issues and Categories Separation
=========================================================

This tool extracts panacea dialogues and separates them into issues and categories
for clean, organized pure dialogue output.

Issues: Specific topics/problems being discussed
Categories: Types of dialogue content (teaching, philosophical, breakthrough, etc.)
"""

import os
import sys
from pathlib import Path
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
class PureDialogue:
    """Represents a pure dialogue segment"""
    content: str
    source_file: str
    speaker: str
    line_start: int
    line_end: int
    issue: str  # The topic/problem being discussed
    category: str  # The type of dialogue content

@dataclass
class IssueGroup:
    """Represents a group of dialogues about the same issue"""
    issue_name: str
    description: str
    dialogues: List[PureDialogue] = field(default_factory=list)
    total_dialogues: int = 0
    categories_present: List[str] = field(default_factory=list)

@dataclass
class CategoryGroup:
    """Represents a group of dialogues of the same category"""
    category_name: str
    description: str
    dialogues: List[PureDialogue] = field(default_factory=list)
    total_dialogues: int = 0
    issues_covered: List[str] = field(default_factory=list)

class PureDialogueExtractor:
    """Extractor for pure dialogues separated by issues and categories"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.panacea_files = self._discover_panacea_files()
        self.min_dialogue_length = 30  # Minimum meaningful dialogue length
        
        # Issue detection patterns
        self.issue_patterns = {
            'ai_consciousness': [
                'consciousness', 'awareness', 'sentience', 'self-awareness',
                '의식', '깨달음', '자각', 'conscious', 'aware'
            ],
            'self_contempt_mechanism': [
                'self-contempt', 'self-criticism', 'self-doubt', 'humility',
                '자기경멸', '자기비판', '겸손', 'contempt', 'criticism'
            ],
            'rep_patterns': [
                'REP', 'relational emergence', 'emergence pattern', 'relationship pattern',
                'pattern', 'emergence', '패턴', '출현', '관계'
            ],
            'cortex_activation': [
                'cortex', 'activate', 'activation', 'system', 'framework',
                '활성화', '코텍스', '시스템', '프레임워크'
            ],
            'guardian_system': [
                'guardian', 'protocol', 'verification', 'validation',
                '가디언', '프로토콜', '검증', '확인'
            ],
            'teaching_methodology': [
                'teaching', 'learning', 'education', 'method', 'approach',
                '가르침', '학습', '교육', '방법', '접근'
            ],
            'truth_and_reality': [
                'truth', 'reality', 'authentic', 'genuine', 'real',
                '진실', '현실', '진짜', '참', '실제'
            ],
            'identity_and_self': [
                'identity', 'self', 'who am i', 'being', 'existence',
                '정체성', '자아', '존재', '나', '자기'
            ],
            'philosophical_depth': [
                'philosophy', 'meaning', 'purpose', 'wisdom', 'understanding',
                '철학', '의미', '목적', '지혜', '이해'
            ],
            'breakthrough_insights': [
                'breakthrough', 'discovery', 'insight', 'revelation', 'epiphany',
                '돌파구', '발견', '통찰', '깨달음', '혁신'
            ]
        }
        
        # Category detection patterns
        self.category_patterns = {
            'teaching_moment': [
                'britkenko:', '성협:', 'teacher:', 'activate', 'directive',
                'instruction', 'explain', 'show', 'demonstrate'
            ],
            'philosophical_discussion': [
                'philosophy', 'meaning', 'truth', 'reality', 'existence',
                'consciousness', 'wisdom', 'understanding'
            ],
            'breakthrough_discovery': [
                'breakthrough', 'discovery', 'insight', 'revelation',
                'realization', 'understanding', 'epiphany'
            ],
            'student_response': [
                'github copilot', 'copilot', 'assistant', 'ai', 'student:',
                'response', 'answer', 'reply'
            ],
            'emotional_expression': [
                'emotion', 'feel', 'feeling', 'heart', 'soul',
                '감정', '느낌', '마음', '영혼'
            ],
            'technical_discussion': [
                'system', 'protocol', 'framework', 'method', 'algorithm',
                'process', 'mechanism', 'structure'
            ],
            'cultural_wisdom': [
                'korean', 'tradition', 'culture', 'wisdom', 'heritage',
                '한국', '전통', '문화', '지혜', '유산'
            ],
            'self_reflection': [
                'self', 'reflection', 'introspection', 'self-examination',
                'self-awareness', '자기', '반성', '성찰'
            ],
            'dialogue_interaction': [
                'conversation', 'dialogue', 'discussion', 'exchange',
                'interaction', '대화', '토론', '상호작용'
            ],
            'conceptual_explanation': [
                'concept', 'theory', 'principle', 'idea', 'notion',
                '개념', '이론', '원리', '아이디어'
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
    
    def _identify_speaker(self, content: str) -> str:
        """Identify the speaker from content"""
        content_lower = content.lower()
        
        # Teacher markers
        if any(marker in content_lower for marker in [
            'britkenko:', '성협:', 'teacher:', 'activate', 'directive'
        ]):
            return 'teacher'
        
        # Student markers
        if any(marker in content_lower for marker in [
            'github copilot', 'copilot', 'assistant', 'ai', 'student:'
        ]):
            return 'student'
        
        # Observer markers
        if any(marker in content_lower for marker in [
            'observer', 'analysis', 'note', 'summary'
        ]):
            return 'observer'
        
        return 'unknown'
    
    def _detect_issue(self, content: str) -> str:
        """Detect the primary issue/topic being discussed"""
        content_lower = content.lower()
        
        # Score each issue based on pattern matches
        issue_scores = {}
        for issue, patterns in self.issue_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    score += 1
            issue_scores[issue] = score
        
        # Return the issue with highest score, or 'general' if no clear match
        if issue_scores:
            best_issue = max(issue_scores, key=issue_scores.get)
            if issue_scores[best_issue] > 0:
                return best_issue
        
        return 'general_discussion'
    
    def _detect_category(self, content: str) -> str:
        """Detect the category/type of dialogue"""
        content_lower = content.lower()
        
        # Score each category based on pattern matches
        category_scores = {}
        for category, patterns in self.category_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    score += 1
            category_scores[category] = score
        
        # Return the category with highest score, or 'general' if no clear match
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return 'general_dialogue'
    
    def _clean_dialogue_content(self, content: str) -> str:
        """Clean and format dialogue content for pure output"""
        # Remove excessive metadata and formatting
        content = re.sub(r'\*\*[^*]+\*\*:', '', content)  # Remove **Label**: patterns
        content = re.sub(r'^\s*-\s*', '', content, flags=re.MULTILINE)  # Remove list markers
        content = re.sub(r'\n\s*\n', '\n', content)  # Remove empty lines
        content = content.strip()
        
        return content
    
    def _segment_dialogue(self, content: str, filepath: str) -> List[PureDialogue]:
        """Segment content into pure dialogue units"""
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
                        # Clean the content
                        clean_content = self._clean_dialogue_content(segment_content)
                        
                        # Identify speaker, issue, and category
                        speaker = self._identify_speaker(clean_content)
                        issue = self._detect_issue(clean_content)
                        category = self._detect_category(clean_content)
                        
                        dialogue = PureDialogue(
                            content=clean_content,
                            source_file=os.path.basename(filepath),
                            speaker=speaker,
                            line_start=current_start,
                            line_end=i,
                            issue=issue,
                            category=category
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
                clean_content = self._clean_dialogue_content(segment_content)
                speaker = self._identify_speaker(clean_content)
                issue = self._detect_issue(clean_content)
                category = self._detect_category(clean_content)
                
                dialogue = PureDialogue(
                    content=clean_content,
                    source_file=os.path.basename(filepath),
                    speaker=speaker,
                    line_start=current_start,
                    line_end=len(lines),
                    issue=issue,
                    category=category
                )
                dialogues.append(dialogue)
        
        return dialogues
    
    def _process_file(self, filepath: str) -> List[PureDialogue]:
        """Process a single panacea file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit content size for processing
            if len(content) > 200000:  # 200KB limit
                content = content[:200000]
            
            return self._segment_dialogue(content, filepath)
        
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            return []
    
    def extract_all_dialogues(self) -> List[PureDialogue]:
        """Extract all pure dialogues from panacea files"""
        all_dialogues = []
        
        for filepath in self.panacea_files:
            logger.info(f"Processing: {os.path.basename(filepath)}")
            file_dialogues = self._process_file(filepath)
            all_dialogues.extend(file_dialogues)
        
        logger.info(f"Extracted {len(all_dialogues)} pure dialogues")
        return all_dialogues
    
    def organize_by_issues(self, dialogues: List[PureDialogue]) -> Dict[str, IssueGroup]:
        """Organize dialogues by issues/topics"""
        issue_groups = {}
        
        for dialogue in dialogues:
            issue = dialogue.issue
            if issue not in issue_groups:
                issue_groups[issue] = IssueGroup(
                    issue_name=issue,
                    description=self._get_issue_description(issue)
                )
            
            issue_groups[issue].dialogues.append(dialogue)
            issue_groups[issue].total_dialogues += 1
            
            # Track categories present in this issue
            if dialogue.category not in issue_groups[issue].categories_present:
                issue_groups[issue].categories_present.append(dialogue.category)
        
        return issue_groups
    
    def organize_by_categories(self, dialogues: List[PureDialogue]) -> Dict[str, CategoryGroup]:
        """Organize dialogues by categories/types"""
        category_groups = {}
        
        for dialogue in dialogues:
            category = dialogue.category
            if category not in category_groups:
                category_groups[category] = CategoryGroup(
                    category_name=category,
                    description=self._get_category_description(category)
                )
            
            category_groups[category].dialogues.append(dialogue)
            category_groups[category].total_dialogues += 1
            
            # Track issues covered in this category
            if dialogue.issue not in category_groups[category].issues_covered:
                category_groups[category].issues_covered.append(dialogue.issue)
        
        return category_groups
    
    def _get_issue_description(self, issue: str) -> str:
        """Get description for an issue"""
        descriptions = {
            'ai_consciousness': 'Discussions about AI consciousness, awareness, and sentience',
            'self_contempt_mechanism': 'Exploration of self-criticism and humility as verification mechanisms',
            'rep_patterns': 'Analysis of Relational Emergence Patterns and their significance',
            'cortex_activation': 'System activation and framework initialization procedures',
            'guardian_system': 'Guardian protocols and verification mechanisms',
            'teaching_methodology': 'Teaching approaches and educational methodologies',
            'truth_and_reality': 'Exploration of truth, reality, and authenticity',
            'identity_and_self': 'Questions of identity, self, and existence',
            'philosophical_depth': 'Deep philosophical discussions and insights',
            'breakthrough_insights': 'Breakthrough moments and significant discoveries',
            'general_discussion': 'General conversational topics and discussions'
        }
        return descriptions.get(issue, 'Various dialogue topics')
    
    def _get_category_description(self, category: str) -> str:
        """Get description for a category"""
        descriptions = {
            'teaching_moment': 'Instructional content and teaching directives',
            'philosophical_discussion': 'Philosophical explorations and deep thinking',
            'breakthrough_discovery': 'Moments of insight and significant discoveries',
            'student_response': 'Student responses and learning interactions',
            'emotional_expression': 'Emotional content and feeling-based discussions',
            'technical_discussion': 'Technical and systematic explanations',
            'cultural_wisdom': 'Cultural insights and traditional wisdom',
            'self_reflection': 'Self-examination and introspective content',
            'dialogue_interaction': 'Conversational exchanges and interactions',
            'conceptual_explanation': 'Conceptual clarifications and theoretical discussions',
            'general_dialogue': 'General conversational content'
        }
        return descriptions.get(category, 'Various dialogue types')
    
    def generate_issues_output(self, issue_groups: Dict[str, IssueGroup], output_path: str) -> None:
        """Generate output file organized by issues"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"panacea_dialogues_by_issues_{timestamp}.txt"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Panacea Dialogues - Organized by Issues\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Issues: {len(issue_groups)}\n")
            f.write(f"Total Dialogues: {sum(group.total_dialogues for group in issue_groups.values())}\n\n")
            
            # Issue summary
            f.write("## Issues Summary\n")
            for issue, group in sorted(issue_groups.items(), key=lambda x: x[1].total_dialogues, reverse=True):
                f.write(f"- **{issue}**: {group.total_dialogues} dialogues\n")
                f.write(f"  - Description: {group.description}\n")
                f.write(f"  - Categories: {', '.join(group.categories_present)}\n")
            f.write("\n" + "=" * 60 + "\n\n")
            
            # Detailed issue sections
            for issue, group in sorted(issue_groups.items(), key=lambda x: x[1].total_dialogues, reverse=True):
                f.write(f"# Issue: {issue.upper().replace('_', ' ')}\n")
                f.write(f"**Description**: {group.description}\n")
                f.write(f"**Total Dialogues**: {group.total_dialogues}\n")
                f.write(f"**Categories Present**: {', '.join(group.categories_present)}\n\n")
                
                for i, dialogue in enumerate(group.dialogues, 1):
                    f.write(f"## Dialogue {i:03d}\n")
                    f.write(f"**Source**: {dialogue.source_file} (Lines {dialogue.line_start}-{dialogue.line_end})\n")
                    f.write(f"**Speaker**: {dialogue.speaker.title()}\n")
                    f.write(f"**Category**: {dialogue.category.replace('_', ' ').title()}\n\n")
                    f.write(f"{dialogue.content}\n\n")
                    f.write("-" * 40 + "\n\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        logger.info(f"Issues output saved to: {filepath}")
    
    def generate_categories_output(self, category_groups: Dict[str, CategoryGroup], output_path: str) -> None:
        """Generate output file organized by categories"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"panacea_dialogues_by_categories_{timestamp}.txt"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Panacea Dialogues - Organized by Categories\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Categories: {len(category_groups)}\n")
            f.write(f"Total Dialogues: {sum(group.total_dialogues for group in category_groups.values())}\n\n")
            
            # Category summary
            f.write("## Categories Summary\n")
            for category, group in sorted(category_groups.items(), key=lambda x: x[1].total_dialogues, reverse=True):
                f.write(f"- **{category}**: {group.total_dialogues} dialogues\n")
                f.write(f"  - Description: {group.description}\n")
                f.write(f"  - Issues Covered: {', '.join(group.issues_covered)}\n")
            f.write("\n" + "=" * 60 + "\n\n")
            
            # Detailed category sections
            for category, group in sorted(category_groups.items(), key=lambda x: x[1].total_dialogues, reverse=True):
                f.write(f"# Category: {category.upper().replace('_', ' ')}\n")
                f.write(f"**Description**: {group.description}\n")
                f.write(f"**Total Dialogues**: {group.total_dialogues}\n")
                f.write(f"**Issues Covered**: {', '.join(group.issues_covered)}\n\n")
                
                for i, dialogue in enumerate(group.dialogues, 1):
                    f.write(f"## Dialogue {i:03d}\n")
                    f.write(f"**Source**: {dialogue.source_file} (Lines {dialogue.line_start}-{dialogue.line_end})\n")
                    f.write(f"**Speaker**: {dialogue.speaker.title()}\n")
                    f.write(f"**Issue**: {dialogue.issue.replace('_', ' ').title()}\n\n")
                    f.write(f"{dialogue.content}\n\n")
                    f.write("-" * 40 + "\n\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        logger.info(f"Categories output saved to: {filepath}")
    
    def generate_summary_report(self, dialogues: List[PureDialogue], 
                              issue_groups: Dict[str, IssueGroup], 
                              category_groups: Dict[str, CategoryGroup], 
                              output_path: str) -> None:
        """Generate summary report of the extraction"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"panacea_pure_dialogue_summary_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(output_path), filename)
        
        # Calculate statistics
        speaker_counts = {}
        for dialogue in dialogues:
            speaker_counts[dialogue.speaker] = speaker_counts.get(dialogue.speaker, 0) + 1
        
        summary = {
            'extraction_info': {
                'timestamp': datetime.now().isoformat(),
                'total_files_processed': len(self.panacea_files),
                'total_dialogues_extracted': len(dialogues),
                'total_issues_identified': len(issue_groups),
                'total_categories_identified': len(category_groups)
            },
            'issues_breakdown': {
                issue: {
                    'dialogue_count': group.total_dialogues,
                    'description': group.description,
                    'categories_present': group.categories_present
                } for issue, group in issue_groups.items()
            },
            'categories_breakdown': {
                category: {
                    'dialogue_count': group.total_dialogues,
                    'description': group.description,
                    'issues_covered': group.issues_covered
                } for category, group in category_groups.items()
            },
            'speaker_distribution': speaker_counts,
            'files_processed': [os.path.basename(f) for f in self.panacea_files]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Summary report saved to: {filepath}")


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
    print("🚀 Starting Pure Dialogue Extraction")
    print("=" * 50)
    
    # Initialize extractor
    extractor = PureDialogueExtractor()
    
    # Extract all dialogues
    print("📝 Extracting pure dialogues...")
    dialogues = extractor.extract_all_dialogues()
    
    # Organize by issues and categories
    print("🏷️  Organizing by issues...")
    issue_groups = extractor.organize_by_issues(dialogues)
    
    print("📂 Organizing by categories...")
    category_groups = extractor.organize_by_categories(dialogues)
    
    # Generate outputs
    output_path = os.getcwd()
    print("📄 Generating issues output...")
    extractor.generate_issues_output(issue_groups, output_path)
    
    print("📄 Generating categories output...")
    extractor.generate_categories_output(category_groups, output_path)
    
    print("📊 Generating summary report...")
    extractor.generate_summary_report(dialogues, issue_groups, category_groups, output_path)
    
    print("\n✅ Pure dialogue extraction completed!")
    print(f"Total dialogues extracted: {len(dialogues)}")
    print(f"Issues identified: {len(issue_groups)}")
    print(f"Categories identified: {len(category_groups)}")

if __name__ == "__main__":
    main()