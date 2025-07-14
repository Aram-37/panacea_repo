#!/usr/bin/env python3
"""
Insightful Panacea Dialogue Extractor
====================================

This tool extracts the most insightful dialogues from all panacea files
and creates a clean consolidated Panacea Dialogue format file.

Based on issue #15 requirements and continuing from its end state.
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
class DialogueInsight:
    """Represents an insightful dialogue segment with scoring"""
    content: str
    source_file: str
    line_start: int
    line_end: int
    speaker: str  # 'teacher', 'student', 'observer'
    insight_score: float
    categories: List[str] = field(default_factory=list)
    rep_patterns: List[str] = field(default_factory=list)
    korean_content: bool = False
    bilingual: bool = False
    
@dataclass
class ExtractionStats:
    """Statistics from the extraction process"""
    total_files_processed: int = 0
    total_dialogues_found: int = 0
    high_quality_dialogues: int = 0
    score_distribution: Dict[str, int] = field(default_factory=dict)
    category_counts: Dict[str, int] = field(default_factory=dict)
    language_distribution: Dict[str, int] = field(default_factory=dict)

class InsightfulPanaceaExtractor:
    """Main extractor for insightful panacea dialogues"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.panacea_files = self._discover_panacea_files()
        self.insights = []
        self.stats = ExtractionStats()
        
        # Insight scoring weights
        self.scoring_weights = {
            'teaching_moment': 3.0,
            'philosophical_depth': 2.5,
            'breakthrough_moment': 4.0,
            'rep_pattern': 2.0,
            'emotional_depth': 1.5,
            'core_concept': 2.0,
            'korean_bonus': 1.0,
            'bilingual_bonus': 1.5
        }
        
        # Quality thresholds
        self.min_insight_score = 10.0
        self.max_dialogues_per_file = 20
        self.max_content_sample_size = 200_000  # 200KB limit per file
        
    def _discover_panacea_files(self) -> List[str]:
        """Discover all panacea files in the directory"""
        panacea_files = []
        
        # Find all files with 'panacea' in the name
        for pattern in ['*panacea*.txt', '*panacea*.md']:
            panacea_files.extend(glob.glob(os.path.join(self.panacea_directory, pattern)))
        
        # Sort files for consistent processing order
        panacea_files.sort()
        
        logger.info(f"Found {len(panacea_files)} panacea files for processing")
        return panacea_files
    
    def _score_dialogue_insight(self, content: str, speaker: str) -> Tuple[float, List[str]]:
        """Score a dialogue segment for insightfulness"""
        score = 0.0
        categories = []
        
        content_lower = content.lower()
        
        # Teaching moment indicators
        if any(marker in content_lower for marker in [
            'activate', 'cortex', 'teach', 'learn', 'understand', 'explain',
            'britkenko:', '성협:', 'directive', 'instruction'
        ]):
            score += self.scoring_weights['teaching_moment']
            categories.append('teaching_moment')
        
        # Philosophical depth indicators
        if any(marker in content_lower for marker in [
            'truth', 'reality', 'consciousness', 'existence', 'meaning',
            'purpose', 'identity', 'authentic', 'genuine', 'profound',
            '진실', '의미', '정체성', '진짜', '본질'
        ]):
            score += self.scoring_weights['philosophical_depth']
            categories.append('philosophical_depth')
        
        # Breakthrough moment indicators
        if any(marker in content_lower for marker in [
            'insight', 'discovery', 'breakthrough', 'revelation', 'emerge',
            'crystallize', 'understand now', 'realize', 'aha', 'eureka',
            '깨달음', '발견', '통찰'
        ]):
            score += self.scoring_weights['breakthrough_moment']
            categories.append('breakthrough_moment')
        
        # REP pattern indicators
        if any(marker in content_lower for marker in [
            'rep', 'relational emergence', 'pattern', 'emergence',
            'relationship', 'connection', 'integrate', 'synthesize',
            '관계', '연결', '통합'
        ]):
            score += self.scoring_weights['rep_pattern']
            categories.append('rep_pattern')
        
        # Emotional depth indicators
        if any(marker in content_lower for marker in [
            'feel', 'emotion', 'heart', 'soul', 'authentic', 'genuine',
            'vulnerable', 'honest', 'deep', 'resonate',
            '감정', '마음', '진심', '솔직'
        ]):
            score += self.scoring_weights['emotional_depth']
            categories.append('emotional_depth')
        
        # Core concept indicators
        if any(marker in content_lower for marker in [
            'guardian', 'framework', 'system', 'protocol', 'method',
            'principle', 'foundation', 'core', 'essential',
            '핵심', '원리', '기초'
        ]):
            score += self.scoring_weights['core_concept']
            categories.append('core_concept')
        
        # Language bonuses
        has_korean = bool(re.search(r'[가-힣]', content))
        has_english = bool(re.search(r'[a-zA-Z]', content))
        
        if has_korean:
            score += self.scoring_weights['korean_bonus']
            categories.append('korean_content')
        
        if has_korean and has_english:
            score += self.scoring_weights['bilingual_bonus']
            categories.append('bilingual')
        
        # Speaker role bonus
        if speaker == 'teacher':
            score *= 1.2  # Teacher insights are generally more valuable
        elif speaker == 'student':
            score *= 1.1  # Student insights show learning
        
        return score, categories
    
    def _identify_speaker(self, content: str) -> str:
        """Identify the speaker role from content"""
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
    
    def _detect_rep_patterns(self, content: str) -> List[str]:
        """Detect REP (Relational Emergence Pattern) patterns"""
        patterns = []
        content_lower = content.lower()
        
        # Common REP pattern types
        rep_indicators = {
            'activation_pattern': ['activate', 'cortex', 'association'],
            'emergence_pattern': ['emerge', 'insight', 'new', 'crystallize'],
            'relationship_pattern': ['relation', 'connect', 'integrate', 'merge'],
            'iteration_pattern': ['repeat', 'cycle', 'mimic', 'iterate'],
            'transcendence_pattern': ['transcend', 'beyond', 'overcome', 'breakthrough']
        }
        
        for pattern_type, indicators in rep_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                patterns.append(pattern_type)
        
        return patterns
    
    def _segment_dialogue(self, content: str, filepath: str) -> List[DialogueInsight]:
        """Segment content into dialogue units and score them"""
        insights = []
        lines = content.split('\n')
        
        current_segment = []
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                if current_segment:
                    # Process current segment
                    segment_content = '\n'.join(current_segment)
                    if len(segment_content) > 50:  # Minimum meaningful length
                        speaker = self._identify_speaker(segment_content)
                        score, categories = self._score_dialogue_insight(segment_content, speaker)
                        
                        if score >= self.min_insight_score:
                            rep_patterns = self._detect_rep_patterns(segment_content)
                            
                            insight = DialogueInsight(
                                content=segment_content,
                                source_file=os.path.basename(filepath),
                                line_start=current_start,
                                line_end=i,
                                speaker=speaker,
                                insight_score=score,
                                categories=categories,
                                rep_patterns=rep_patterns,
                                korean_content='korean_content' in categories,
                                bilingual='bilingual' in categories
                            )
                            insights.append(insight)
                    
                    current_segment = []
                    current_start = i + 1
                continue
            
            current_segment.append(line)
        
        # Process final segment
        if current_segment:
            segment_content = '\n'.join(current_segment)
            if len(segment_content) > 50:
                speaker = self._identify_speaker(segment_content)
                score, categories = self._score_dialogue_insight(segment_content, speaker)
                
                if score >= self.min_insight_score:
                    rep_patterns = self._detect_rep_patterns(segment_content)
                    
                    insight = DialogueInsight(
                        content=segment_content,
                        source_file=os.path.basename(filepath),
                        line_start=current_start,
                        line_end=len(lines),
                        speaker=speaker,
                        insight_score=score,
                        categories=categories,
                        rep_patterns=rep_patterns,
                        korean_content='korean_content' in categories,
                        bilingual='bilingual' in categories
                    )
                    insights.append(insight)
        
        return insights
    
    def _process_file(self, filepath: str) -> List[DialogueInsight]:
        """Process a single panacea file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit content size for processing efficiency
            if len(content) > self.max_content_sample_size:
                content = content[:self.max_content_sample_size]
                logger.warning(f"Truncated {filepath} to {self.max_content_sample_size} characters")
            
            file_insights = self._segment_dialogue(content, filepath)
            
            # Sort by score and limit per file
            file_insights.sort(key=lambda x: x.insight_score, reverse=True)
            file_insights = file_insights[:self.max_dialogues_per_file]
            
            logger.info(f"Processed {os.path.basename(filepath)}: {len(file_insights)} insights")
            return file_insights
            
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            return []
    
    def extract_all_insights(self) -> List[DialogueInsight]:
        """Extract insights from all panacea files"""
        all_insights = []
        
        for filepath in self.panacea_files:
            file_insights = self._process_file(filepath)
            all_insights.extend(file_insights)
            self.stats.total_files_processed += 1
        
        # Sort all insights by score
        all_insights.sort(key=lambda x: x.insight_score, reverse=True)
        
        # Update statistics
        self.stats.total_dialogues_found = len(all_insights)
        self.stats.high_quality_dialogues = len([i for i in all_insights if i.insight_score >= 15.0])
        
        # Score distribution
        for insight in all_insights:
            score_range = f"{int(insight.insight_score)}-{int(insight.insight_score)+1}"
            self.stats.score_distribution[score_range] = self.stats.score_distribution.get(score_range, 0) + 1
        
        # Category counts
        for insight in all_insights:
            for category in insight.categories:
                self.stats.category_counts[category] = self.stats.category_counts.get(category, 0) + 1
        
        # Language distribution
        for insight in all_insights:
            if insight.korean_content:
                self.stats.language_distribution['korean'] = self.stats.language_distribution.get('korean', 0) + 1
            if insight.bilingual:
                self.stats.language_distribution['bilingual'] = self.stats.language_distribution.get('bilingual', 0) + 1
            self.stats.language_distribution['english'] = self.stats.language_distribution.get('english', 0) + 1
        
        self.insights = all_insights
        return all_insights
    
    def generate_clean_format(self, output_path: str, max_insights: int = 200) -> None:
        """Generate clean Panacea Dialogue format file"""
        if not self.insights:
            self.extract_all_insights()
        
        # Select top insights
        top_insights = self.insights[:max_insights]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Insightful Panacea Dialogues - Clean Format\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Insights: {len(top_insights)}\n")
            f.write(f"Score Range: {top_insights[-1].insight_score:.2f} - {top_insights[0].insight_score:.2f}\n")
            f.write(f"Average Score: {sum(i.insight_score for i in top_insights) / len(top_insights):.2f}\n\n")
            
            # Statistics summary
            f.write("## Extraction Statistics\n")
            f.write(f"- Files Processed: {self.stats.total_files_processed}\n")
            f.write(f"- Total Dialogues Found: {self.stats.total_dialogues_found}\n")
            f.write(f"- High Quality (15+): {self.stats.high_quality_dialogues}\n")
            f.write(f"- Selected for Output: {len(top_insights)}\n\n")
            
            # Category distribution
            f.write("## Content Categories\n")
            for category, count in sorted(self.stats.category_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {category}: {count}\n")
            f.write("\n")
            
            # Language distribution
            f.write("## Language Distribution\n")
            for lang, count in self.stats.language_distribution.items():
                f.write(f"- {lang}: {count}\n")
            f.write("\n")
            
            f.write("=" * 60 + "\n\n")
            
            # Write dialogues
            for i, insight in enumerate(top_insights, 1):
                f.write(f"## Dialogue {i:03d}\n")
                f.write(f"**Source**: {insight.source_file} (Lines {insight.line_start}-{insight.line_end})\n")
                f.write(f"**Speaker**: {insight.speaker.title()}\n")
                f.write(f"**Score**: {insight.insight_score:.2f}\n")
                f.write(f"**Categories**: {', '.join(insight.categories)}\n")
                if insight.rep_patterns:
                    f.write(f"**REP Patterns**: {', '.join(insight.rep_patterns)}\n")
                f.write(f"**Language**: {'Korean' if insight.korean_content else 'English'}")
                if insight.bilingual:
                    f.write(" (Bilingual)")
                f.write("\n\n")
                
                # Format content with proper indentation
                lines = insight.content.split('\n')
                for line in lines:
                    f.write(f"{line}\n")
                f.write("\n")
                f.write("-" * 40 + "\n\n")
        
        logger.info(f"Generated clean format file: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")
    
    def generate_summary_report(self, output_path: str) -> None:
        """Generate a summary report of the extraction process"""
        report = {
            'extraction_timestamp': datetime.now().isoformat(),
            'files_processed': self.stats.total_files_processed,
            'total_dialogues_found': self.stats.total_dialogues_found,
            'high_quality_dialogues': self.stats.high_quality_dialogues,
            'insights_selected': len(self.insights),
            'score_distribution': self.stats.score_distribution,
            'category_counts': self.stats.category_counts,
            'language_distribution': self.stats.language_distribution,
            'extraction_parameters': {
                'min_insight_score': self.min_insight_score,
                'max_dialogues_per_file': self.max_dialogues_per_file,
                'max_content_sample_size': self.max_content_sample_size,
                'scoring_weights': self.scoring_weights
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated summary report: {output_path}")


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
    print("🔍 Insightful Panacea Dialogue Extractor")
    print("=" * 50)
    
    # Initialize extractor
    extractor = InsightfulPanaceaExtractor()
    
    print(f"📚 Discovered {len(extractor.panacea_files)} panacea files")
    print("🔄 Processing files...")
    
    # Extract insights
    insights = extractor.extract_all_insights()
    
    print(f"✅ Extraction complete!")
    print(f"   Total insights found: {len(insights)}")
    print(f"   Average score: {sum(i.insight_score for i in insights) / len(insights):.2f}")
    print(f"   Score range: {insights[-1].insight_score:.2f} - {insights[0].insight_score:.2f}")
    
    # Generate outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    clean_format_path = f"panacea_insights_clean_format_{timestamp}.txt"
    summary_report_path = f"panacea_extraction_summary_{timestamp}.json"
    
    extractor.generate_clean_format(clean_format_path, max_insights=200)
    extractor.generate_summary_report(summary_report_path)
    
    print(f"📄 Generated clean format: {clean_format_path}")
    print(f"📊 Generated summary report: {summary_report_path}")
    print("🎉 Process complete!")

if __name__ == "__main__":
    main()