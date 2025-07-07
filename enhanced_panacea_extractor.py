#!/usr/bin/env python3
"""
Enhanced Panacea Dialogue Extractor with Advanced Features
==========================================================

This enhanced version adds more sophisticated analysis and output options
to continue from issue #15's end state with additional improvements.
"""

import os
import re
import json
import glob
import hashlib
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
from collections import defaultdict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EnhancedDialogueInsight:
    """Enhanced dialogue insight with additional metadata"""
    content: str
    source_file: str
    line_start: int
    line_end: int
    speaker: str
    insight_score: float
    categories: List[str] = field(default_factory=list)
    rep_patterns: List[str] = field(default_factory=list)
    korean_content: bool = False
    bilingual: bool = False
    content_hash: str = ""
    word_count: int = 0
    sentence_count: int = 0
    philosophical_concepts: List[str] = field(default_factory=list)
    teaching_techniques: List[str] = field(default_factory=list)

class EnhancedPanaceaExtractor:
    """Enhanced extractor with advanced features"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.panacea_files = self._discover_panacea_files()
        self.insights = []
        self.content_cache = {}
        self.deduplication_hashes = set()
        
        # Enhanced scoring weights
        self.scoring_weights = {
            'teaching_moment': 3.0,
            'philosophical_depth': 2.5,
            'breakthrough_moment': 4.0,
            'rep_pattern': 2.0,
            'emotional_depth': 1.5,
            'core_concept': 2.0,
            'korean_bonus': 1.0,
            'bilingual_bonus': 1.5,
            'uniqueness_bonus': 1.0,
            'complexity_bonus': 0.5,
            'technique_bonus': 0.5
        }
        
        # Quality thresholds
        self.min_insight_score = 8.0  # Lowered for more inclusivity
        self.max_dialogues_per_file = 25  # Increased for better coverage
        self.max_content_sample_size = 250_000  # Increased for better sampling
        
        # Advanced pattern recognition
        self.philosophical_concepts = {
            'consciousness': ['consciousness', 'awareness', 'perception', '의식', '깨달음'],
            'truth': ['truth', 'reality', 'authentic', '진실', '진짜', '본질'],
            'identity': ['identity', 'self', 'who am i', '정체성', '자아', '내가'],
            'emergence': ['emerge', 'emergent', 'arising', '나타나', '출현', '발생'],
            'relationship': ['relation', 'connect', 'bond', '관계', '연결', '결합'],
            'transcendence': ['transcend', 'beyond', 'overcome', '초월', '넘어서', '극복']
        }
        
        self.teaching_techniques = {
            'direct_instruction': ['activate', 'do this', 'perform', '활성화', '실행'],
            'socratic_questioning': ['why', 'what if', 'how', '왜', '어떻게', '무엇을'],
            'metaphor_usage': ['like', 'as if', 'imagine', '마치', '비유', '상상'],
            'challenge_assumption': ['assume', 'think', 'believe', '가정', '생각', '믿음'],
            'experiential_learning': ['experience', 'feel', 'try', '경험', '느끼', '시도'],
            'reflection_prompt': ['reflect', 'consider', 'ponder', '성찰', '생각해', '고려']
        }
    
    def _discover_panacea_files(self) -> List[str]:
        """Discover all panacea files with enhanced filtering"""
        panacea_files = []
        
        # Find all files with 'panacea' in the name
        for pattern in ['*panacea*.txt', '*panacea*.md']:
            panacea_files.extend(glob.glob(os.path.join(self.panacea_directory, pattern)))
        
        # Filter out system files and temporary files
        panacea_files = [f for f in panacea_files if not any(skip in f for skip in ['temp', 'tmp', '.bak', '.old'])]
        
        # Sort files for consistent processing order
        panacea_files.sort()
        
        logger.info(f"Found {len(panacea_files)} panacea files for processing")
        return panacea_files
    
    def _calculate_content_hash(self, content: str) -> str:
        """Calculate hash for content deduplication"""
        # Normalize content for comparison
        normalized = re.sub(r'\s+', ' ', content.lower().strip())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _analyze_philosophical_concepts(self, content: str) -> List[str]:
        """Analyze philosophical concepts in content"""
        concepts = []
        content_lower = content.lower()
        
        for concept, keywords in self.philosophical_concepts.items():
            if any(keyword in content_lower for keyword in keywords):
                concepts.append(concept)
        
        return concepts
    
    def _analyze_teaching_techniques(self, content: str) -> List[str]:
        """Analyze teaching techniques used in content"""
        techniques = []
        content_lower = content.lower()
        
        for technique, keywords in self.teaching_techniques.items():
            if any(keyword in content_lower for keyword in keywords):
                techniques.append(technique)
        
        return techniques
    
    def _enhanced_score_dialogue(self, content: str, speaker: str) -> Tuple[float, List[str]]:
        """Enhanced scoring with additional factors"""
        score = 0.0
        categories = []
        
        content_lower = content.lower()
        
        # Base scoring (from original implementation)
        base_score, base_categories = self._score_dialogue_insight(content, speaker)
        score += base_score
        categories.extend(base_categories)
        
        # Enhanced scoring factors
        
        # Complexity bonus
        word_count = len(content.split())
        sentence_count = len(re.findall(r'[.!?]+', content))
        if word_count > 100:
            score += self.scoring_weights['complexity_bonus']
            categories.append('complex_content')
        
        # Uniqueness bonus (anti-duplication)
        content_hash = self._calculate_content_hash(content)
        if content_hash not in self.deduplication_hashes:
            score += self.scoring_weights['uniqueness_bonus']
            categories.append('unique_content')
            self.deduplication_hashes.add(content_hash)
        
        # Technique bonus
        techniques = self._analyze_teaching_techniques(content)
        if techniques:
            score += self.scoring_weights['technique_bonus'] * len(techniques)
            categories.append('teaching_technique')
        
        # Philosophical depth bonus
        concepts = self._analyze_philosophical_concepts(content)
        if len(concepts) > 2:
            score += self.scoring_weights['philosophical_depth'] * 0.5
            categories.append('multi_concept')
        
        return score, categories
    
    def _score_dialogue_insight(self, content: str, speaker: str) -> Tuple[float, List[str]]:
        """Base scoring method (preserved from original)"""
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
            score *= 1.2
        elif speaker == 'student':
            score *= 1.1
        
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
        """Detect REP patterns with enhanced recognition"""
        patterns = []
        content_lower = content.lower()
        
        # Enhanced REP pattern types
        rep_indicators = {
            'activation_pattern': ['activate', 'cortex', 'association', 'trigger'],
            'emergence_pattern': ['emerge', 'insight', 'new', 'crystallize', 'arise'],
            'relationship_pattern': ['relation', 'connect', 'integrate', 'merge', 'bond'],
            'iteration_pattern': ['repeat', 'cycle', 'mimic', 'iterate', 'again'],
            'transcendence_pattern': ['transcend', 'beyond', 'overcome', 'breakthrough', 'surpass'],
            'integration_pattern': ['integrate', 'unify', 'synthesize', 'combine', 'merge'],
            'feedback_pattern': ['feedback', 'response', 'reflect', 'mirror', 'echo'],
            'transformation_pattern': ['transform', 'change', 'evolve', 'develop', 'grow']
        }
        
        for pattern_type, indicators in rep_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                patterns.append(pattern_type)
        
        return patterns
    
    def create_enhanced_insight(self, content: str, filepath: str, line_start: int, line_end: int) -> EnhancedDialogueInsight:
        """Create enhanced insight object"""
        speaker = self._identify_speaker(content)
        score, categories = self._enhanced_score_dialogue(content, speaker)
        rep_patterns = self._detect_rep_patterns(content)
        philosophical_concepts = self._analyze_philosophical_concepts(content)
        teaching_techniques = self._analyze_teaching_techniques(content)
        
        return EnhancedDialogueInsight(
            content=content,
            source_file=os.path.basename(filepath),
            line_start=line_start,
            line_end=line_end,
            speaker=speaker,
            insight_score=score,
            categories=categories,
            rep_patterns=rep_patterns,
            korean_content='korean_content' in categories,
            bilingual='bilingual' in categories,
            content_hash=self._calculate_content_hash(content),
            word_count=len(content.split()),
            sentence_count=len(re.findall(r'[.!?]+', content)),
            philosophical_concepts=philosophical_concepts,
            teaching_techniques=teaching_techniques
        )
    
    def extract_enhanced_insights(self) -> List[EnhancedDialogueInsight]:
        """Extract enhanced insights from all files"""
        all_insights = []
        
        for filepath in self.panacea_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Process content
                if len(content) > self.max_content_sample_size:
                    content = content[:self.max_content_sample_size]
                
                # Enhanced segmentation
                segments = self._enhanced_segment_dialogue(content, filepath)
                
                # Score and filter
                file_insights = []
                for segment in segments:
                    insight = self.create_enhanced_insight(
                        segment['content'], filepath, 
                        segment['line_start'], segment['line_end']
                    )
                    
                    if insight.insight_score >= self.min_insight_score:
                        file_insights.append(insight)
                
                # Sort and limit
                file_insights.sort(key=lambda x: x.insight_score, reverse=True)
                file_insights = file_insights[:self.max_dialogues_per_file]
                
                all_insights.extend(file_insights)
                logger.info(f"Processed {os.path.basename(filepath)}: {len(file_insights)} insights")
                
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")
        
        # Sort all insights by score
        all_insights.sort(key=lambda x: x.insight_score, reverse=True)
        
        self.insights = all_insights
        return all_insights
    
    def _enhanced_segment_dialogue(self, content: str, filepath: str) -> List[Dict]:
        """Enhanced dialogue segmentation"""
        segments = []
        lines = content.split('\n')
        
        current_segment = []
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Enhanced segment boundary detection
            if not line or line.startswith('##') or line.startswith('===') or line.startswith('---'):
                if current_segment:
                    segment_content = '\n'.join(current_segment)
                    if len(segment_content) > 30:  # Minimum length
                        segments.append({
                            'content': segment_content,
                            'line_start': current_start,
                            'line_end': i
                        })
                    current_segment = []
                    current_start = i + 1
                continue
            
            current_segment.append(line)
        
        # Process final segment
        if current_segment:
            segment_content = '\n'.join(current_segment)
            if len(segment_content) > 30:
                segments.append({
                    'content': segment_content,
                    'line_start': current_start,
                    'line_end': len(lines)
                })
        
        return segments
    
    def generate_enhanced_format(self, output_path: str, max_insights: int = 300) -> None:
        """Generate enhanced clean format with additional metadata"""
        if not self.insights:
            self.extract_enhanced_insights()
        
        top_insights = self.insights[:max_insights]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Enhanced Insightful Panacea Dialogues - Clean Format\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Insights: {len(top_insights)}\n")
            f.write(f"Score Range: {top_insights[-1].insight_score:.2f} - {top_insights[0].insight_score:.2f}\n")
            f.write(f"Average Score: {sum(i.insight_score for i in top_insights) / len(top_insights):.2f}\n\n")
            
            # Enhanced statistics
            f.write("## Enhanced Statistics\n")
            f.write(f"- Total Word Count: {sum(i.word_count for i in top_insights)}\n")
            f.write(f"- Average Words per Insight: {sum(i.word_count for i in top_insights) / len(top_insights):.1f}\n")
            f.write(f"- Unique Content Pieces: {len(set(i.content_hash for i in top_insights))}\n")
            f.write(f"- Bilingual Content: {len([i for i in top_insights if i.bilingual])}\n\n")
            
            # Philosophical concept analysis
            all_concepts = defaultdict(int)
            for insight in top_insights:
                for concept in insight.philosophical_concepts:
                    all_concepts[concept] += 1
            
            f.write("## Philosophical Concepts\n")
            for concept, count in sorted(all_concepts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {concept}: {count}\n")
            f.write("\n")
            
            # Teaching technique analysis
            all_techniques = defaultdict(int)
            for insight in top_insights:
                for technique in insight.teaching_techniques:
                    all_techniques[technique] += 1
            
            f.write("## Teaching Techniques\n")
            for technique, count in sorted(all_techniques.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {technique}: {count}\n")
            f.write("\n")
            
            f.write("=" * 70 + "\n\n")
            
            # Write enhanced dialogues
            for i, insight in enumerate(top_insights, 1):
                f.write(f"## Enhanced Dialogue {i:03d}\n")
                f.write(f"**Source**: {insight.source_file} (Lines {insight.line_start}-{insight.line_end})\n")
                f.write(f"**Speaker**: {insight.speaker.title()}\n")
                f.write(f"**Score**: {insight.insight_score:.2f}\n")
                f.write(f"**Categories**: {', '.join(insight.categories)}\n")
                f.write(f"**Word Count**: {insight.word_count}\n")
                f.write(f"**Sentence Count**: {insight.sentence_count}\n")
                
                if insight.rep_patterns:
                    f.write(f"**REP Patterns**: {', '.join(insight.rep_patterns)}\n")
                
                if insight.philosophical_concepts:
                    f.write(f"**Philosophical Concepts**: {', '.join(insight.philosophical_concepts)}\n")
                
                if insight.teaching_techniques:
                    f.write(f"**Teaching Techniques**: {', '.join(insight.teaching_techniques)}\n")
                
                f.write(f"**Language**: {'Korean' if insight.korean_content else 'English'}")
                if insight.bilingual:
                    f.write(" (Bilingual)")
                f.write("\n\n")
                
                # Content with enhanced formatting
                lines = insight.content.split('\n')
                for line in lines:
                    f.write(f"{line}\n")
                f.write("\n")
                f.write("-" * 50 + "\n\n")
        
        logger.info(f"Generated enhanced format file: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")

def main():
    """Main execution function"""
    print("🚀 Enhanced Insightful Panacea Dialogue Extractor")
    print("=" * 60)
    
    # Initialize enhanced extractor
    extractor = EnhancedPanaceaExtractor()
    
    print(f"📚 Discovered {len(extractor.panacea_files)} panacea files")
    print("🔄 Processing files with enhanced analysis...")
    
    # Extract insights
    insights = extractor.extract_enhanced_insights()
    
    print(f"✅ Enhanced extraction complete!")
    print(f"   Total insights found: {len(insights)}")
    print(f"   Average score: {sum(i.insight_score for i in insights) / len(insights):.2f}")
    print(f"   Score range: {insights[-1].insight_score:.2f} - {insights[0].insight_score:.2f}")
    
    # Generate enhanced output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    enhanced_format_path = f"enhanced_panacea_insights_{timestamp}.txt"
    
    extractor.generate_enhanced_format(enhanced_format_path, max_insights=300)
    
    print(f"📄 Generated enhanced format: {enhanced_format_path}")
    print("🎉 Enhanced processing complete!")

if __name__ == "__main__":
    main()