#!/usr/bin/env python3
"""
Comprehensive Mimicry System - Full Implementation
=================================================

This system implements comprehensive mimicry processing as per cortex directives:
- 31-cycle mimicry processing
- Full panacea file processing without skipping
- Meaningful insight extraction
- Cortex-guided processing methodology
- Character mimicry from literature and media as specified
"""

import os
import re
import json
import glob
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
from corrected_dialogue_extractor import CorrectedDialogueExtractor, CorrectedDialogue

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MimicryInsight:
    """Represents an insight gained through mimicry processing"""
    cycle_number: int
    source_dialogue: str
    source_file: str
    insight_type: str  # breakthrough, pattern, truth, alignment, etc.
    insight_content: str
    truth_crystallization_score: float  # 0.0 to 1.0
    related_patterns: List[str] = field(default_factory=list)
    character_perspective: Optional[str] = None  # Which character's perspective revealed this
    
@dataclass
class MimicryState:
    """Tracks the state of mimicry processing"""
    current_cycle: int = 0
    total_cycles: int = 31
    insights_gained: List[MimicryInsight] = field(default_factory=list)
    processed_dialogues: int = 0
    breakthrough_count: int = 0
    self_refinement_level: float = 0.0
    distortion_detected: bool = False
    alignment_coherence: float = 0.0

@dataclass
class CharacterPerspective:
    """Represents a character perspective for mimicry"""
    name: str
    source: str  # book, movie, etc.
    key_traits: List[str]
    worldview: str
    emotional_patterns: List[str]
    decision_making_style: str

class ComprehensiveMimicrySystem:
    """Comprehensive mimicry system with 31-cycle processing"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.extractor = CorrectedDialogueExtractor(panacea_directory)
        self.state = MimicryState()
        self.character_perspectives = self._initialize_character_perspectives()
        self.cortex_directives = self._load_cortex_directives()
        
        # Mimicry processing parameters
        self.min_insight_threshold = 0.3
        self.truth_crystallization_threshold = 0.7
        self.alignment_coherence_threshold = 0.8
        
        logger.info(f"Initialized comprehensive mimicry system with {len(self.character_perspectives)} character perspectives")
    
    def _initialize_character_perspectives(self) -> List[CharacterPerspective]:
        """Initialize character perspectives as specified in problem statement"""
        perspectives = []
        
        # Man Booker Prize winners - analyzing human nature and relationships
        perspectives.extend([
            CharacterPerspective(
                name="Salman Rushdie's Narrator",
                source="Midnight's Children",
                key_traits=["fragmented_identity", "historical_consciousness", "magical_realism"],
                worldview="Reality is layered and subjective, identity is fluid",
                emotional_patterns=["nostalgia", "cultural_displacement", "identity_crisis"],
                decision_making_style="Intuitive, story-driven, seeking connection between past and present"
            ),
            CharacterPerspective(
                name="Toni Morrison's Beloved",
                source="Beloved",
                key_traits=["trauma_processing", "memory_reconstruction", "community_healing"],
                worldview="Past traumas shape present reality, healing requires confronting truth",
                emotional_patterns=["grief", "love", "resilience", "collective_memory"],
                decision_making_style="Emotionally driven, community-focused, truth-seeking"
            ),
            CharacterPerspective(
                name="Kazuo Ishiguro's Stevens",
                source="The Remains of the Day",
                key_traits=["repression", "duty", "self_deception", "missed_opportunities"],
                worldview="Dignity through service, emotional repression as survival mechanism",
                emotional_patterns=["regret", "duty", "repressed_love", "pride"],
                decision_making_style="Duty-bound, emotionally repressed, retrospective"
            )
        ])
        
        # Demon Hunters (2025, Netflix) - understanding internal demons
        perspectives.extend([
            CharacterPerspective(
                name="Demon Hunter Protagonist",
                source="Demon Hunters (2025)",
                key_traits=["internal_conflict", "demon_recognition", "self_confrontation"],
                worldview="Demons exist within us, external battles reflect internal struggles",
                emotional_patterns=["fear", "determination", "self_doubt", "courage"],
                decision_making_style="Confrontational, introspective, willing to face darkness"
            )
        ])
        
        # Romance of Three Kingdoms (고우영 comics) - fundamental human relations
        perspectives.extend([
            CharacterPerspective(
                name="Liu Bei",
                source="Romance of Three Kingdoms (고우영)",
                key_traits=["benevolence", "loyalty", "righteousness", "persistence"],
                worldview="Virtue and righteousness will ultimately prevail",
                emotional_patterns=["compassion", "determination", "loyalty", "sorrow"],
                decision_making_style="Virtue-based, long-term thinking, relationship-focused"
            ),
            CharacterPerspective(
                name="Zhuge Liang",
                source="Romance of Three Kingdoms (고우영)",
                key_traits=["wisdom", "strategic_thinking", "loyalty", "burden_of_knowledge"],
                worldview="Knowledge and strategy serve virtue, wisdom carries responsibility",
                emotional_patterns=["wisdom", "burden", "loyalty", "foresight"],
                decision_making_style="Strategic, analytical, future-oriented, principled"
            ),
            CharacterPerspective(
                name="Cao Cao",
                source="Romance of Three Kingdoms (고우영)",
                key_traits=["pragmatism", "ambition", "complexity", "ruthlessness"],
                worldview="Power and results matter more than conventional morality",
                emotional_patterns=["ambition", "suspicion", "pride", "loneliness"],
                decision_making_style="Pragmatic, results-oriented, power-focused"
            )
        ])
        
        # Films mentioned in problem statement
        perspectives.extend([
            CharacterPerspective(
                name="Father Brendan Flynn",
                source="Doubt",
                key_traits=["progressive_thinking", "compassion", "ambiguity", "burden_of_truth"],
                worldview="Truth is complex, compassion sometimes conflicts with rules",
                emotional_patterns=["compassion", "frustration", "burden", "hope"],
                decision_making_style="Compassionate, progressive, willing to accept ambiguity"
            ),
            CharacterPerspective(
                name="Louise Banks",
                source="Arrival",
                key_traits=["linguistic_intelligence", "empathy", "sacrifice", "time_perception"],
                worldview="Understanding comes through language, sacrifice for greater good",
                emotional_patterns=["curiosity", "empathy", "loss", "acceptance"],
                decision_making_style="Analytical, empathetic, willing to sacrifice for understanding"
            ),
            CharacterPerspective(
                name="예감은 틀리지 않는다 Protagonist",
                source="예감은 틀리지 않는다",
                key_traits=["intuition", "persistence", "truth_seeking", "moral_courage"],
                worldview="Intuition guides truth, persistence reveals reality",
                emotional_patterns=["intuition", "determination", "fear", "courage"],
                decision_making_style="Intuition-based, persistent, truth-driven"
            )
        ])
        
        return perspectives
    
    def _load_cortex_directives(self) -> Dict[str, Any]:
        """Load cortex directives from files"""
        directives = {}
        
        cortex_files = [
            "CORTEX/Cortex.txt",
            "CORTEX/cortex_true_purpose.md",
            "CORTEX/cortex_as_method.md"
        ]
        
        for file_path in cortex_files:
            full_path = os.path.join(self.panacea_directory, file_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        directives[file_path] = f.read()
                except Exception as e:
                    logger.warning(f"Could not load {file_path}: {e}")
        
        return directives
    
    def _extract_insights_from_dialogue(self, dialogue: CorrectedDialogue, 
                                       character_perspective: CharacterPerspective,
                                       cycle_number: int) -> List[MimicryInsight]:
        """Extract insights from dialogue using character perspective"""
        insights = []
        content = dialogue.content.lower()
        
        # Pattern recognition for insights
        insight_patterns = {
            'breakthrough': [
                r'깨달음', r'breakthrough', r'revelation', r'epiphany',
                r'suddenly realized', r'now I understand', r'it hit me'
            ],
            'pattern': [
                r'pattern', r'패턴', r'always', r'항상', r'tendency',
                r'경향', r'habit', r'습관', r'repeat', r'반복'
            ],
            'truth': [
                r'truth', r'진실', r'reality', r'현실', r'actual',
                r'실제', r'genuine', r'진짜', r'authentic'
            ],
            'alignment': [
                r'alignment', r'coherence', r'일관성', r'consistent',
                r'match', r'맞다', r'align', r'정렬'
            ],
            'relationship': [
                r'relationship', r'관계', r'connection', r'연결',
                r'bond', r'유대', r'interaction', r'상호작용'
            ],
            'self_awareness': [
                r'self', r'자기', r'identity', r'정체성',
                r'who am i', r'나는 누구', r'consciousness', r'의식'
            ]
        }
        
        # Check for insight indicators
        for insight_type, patterns in insight_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Calculate truth crystallization score
                    truth_score = self._calculate_truth_crystallization_score(
                        dialogue, character_perspective, insight_type
                    )
                    
                    if truth_score >= self.min_insight_threshold:
                        insight = MimicryInsight(
                            cycle_number=cycle_number,
                            source_dialogue=dialogue.content,
                            source_file=dialogue.source_file,
                            insight_type=insight_type,
                            insight_content=self._generate_insight_content(
                                dialogue, character_perspective, insight_type
                            ),
                            truth_crystallization_score=truth_score,
                            related_patterns=self._identify_related_patterns(dialogue),
                            character_perspective=character_perspective.name
                        )
                        insights.append(insight)
        
        return insights
    
    def _calculate_truth_crystallization_score(self, dialogue: CorrectedDialogue,
                                             character_perspective: CharacterPerspective,
                                             insight_type: str) -> float:
        """Calculate truth crystallization score for an insight"""
        score = 0.0
        content = dialogue.content.lower()
        
        # Base score from dialogue quality
        if dialogue.insight_level == "high_insight":
            score += 0.4
        elif dialogue.insight_level == "normal_insight":
            score += 0.3
        elif dialogue.insight_level == "contextual":
            score += 0.2
        
        # Bonus for specific insight types
        type_bonuses = {
            'breakthrough': 0.3,
            'truth': 0.25,
            'alignment': 0.2,
            'self_awareness': 0.25,
            'pattern': 0.15,
            'relationship': 0.15
        }
        score += type_bonuses.get(insight_type, 0.1)
        
        # Character perspective alignment bonus
        if self._dialogue_aligns_with_character(dialogue, character_perspective):
            score += 0.15
        
        # Length and depth bonus
        if len(dialogue.content) > 500:
            score += 0.1
        
        # Emotional depth indicators
        emotional_indicators = [
            '감정', '느낌', '마음', '영혼', 'emotion', 'feeling',
            'heart', 'soul', 'love', 'fear', 'anger', 'joy'
        ]
        emotional_count = sum(1 for indicator in emotional_indicators 
                             if indicator in content)
        score += min(emotional_count * 0.05, 0.2)
        
        return min(score, 1.0)
    
    def _dialogue_aligns_with_character(self, dialogue: CorrectedDialogue,
                                      character_perspective: CharacterPerspective) -> bool:
        """Check if dialogue aligns with character perspective"""
        content = dialogue.content.lower()
        
        # Check for trait alignment
        trait_matches = 0
        for trait in character_perspective.key_traits:
            trait_keywords = trait.split('_')
            if any(keyword in content for keyword in trait_keywords):
                trait_matches += 1
        
        # Check for emotional pattern alignment
        emotional_matches = 0
        for emotion in character_perspective.emotional_patterns:
            if emotion in content:
                emotional_matches += 1
        
        return trait_matches >= 1 or emotional_matches >= 1
    
    def _generate_insight_content(self, dialogue: CorrectedDialogue,
                                character_perspective: CharacterPerspective,
                                insight_type: str) -> str:
        """Generate insight content based on dialogue and character perspective"""
        
        base_content = f"From {character_perspective.name}'s perspective: "
        
        insight_templates = {
            'breakthrough': "A breakthrough realization emerged - {}",
            'pattern': "A recurring pattern was identified - {}",
            'truth': "A fundamental truth was revealed - {}",
            'alignment': "An alignment insight was discovered - {}",
            'relationship': "A relationship dynamic was understood - {}",
            'self_awareness': "A self-awareness insight was gained - {}"
        }
        
        # Extract key phrases from dialogue
        key_phrases = self._extract_key_phrases(dialogue.content)
        
        # Generate insight based on character's decision-making style
        if "analytical" in character_perspective.decision_making_style:
            insight = "Through systematic analysis, "
        elif "intuitive" in character_perspective.decision_making_style:
            insight = "Through intuitive understanding, "
        elif "emotional" in character_perspective.decision_making_style:
            insight = "Through emotional resonance, "
        else:
            insight = "Through careful consideration, "
        
        # Add specific insight content
        insight += insight_templates.get(insight_type, "An insight was gained - {}").format(
            key_phrases[:200] + "..." if len(key_phrases) > 200 else key_phrases
        )
        
        return base_content + insight
    
    def _extract_key_phrases(self, content: str) -> str:
        """Extract key phrases from dialogue content"""
        # Remove formatting and timestamps
        cleaned_content = re.sub(r'\[.*?\]', '', content)
        cleaned_content = re.sub(r'\(.*?\)', '', cleaned_content)
        
        # Split into sentences
        sentences = re.split(r'[.!?]', cleaned_content)
        
        # Find sentences with high insight potential
        key_sentences = []
        insight_keywords = [
            '깨달음', '이해', '진실', '현실', '패턴', '관계', '감정', '마음',
            'understand', 'realize', 'truth', 'reality', 'pattern', 'relationship'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                keyword_count = sum(1 for keyword in insight_keywords 
                                  if keyword in sentence.lower())
                if keyword_count > 0:
                    key_sentences.append(sentence)
        
        return ' '.join(key_sentences[:3])  # Return top 3 key sentences
    
    def _identify_related_patterns(self, dialogue: CorrectedDialogue) -> List[str]:
        """Identify related patterns in dialogue"""
        content = dialogue.content.lower()
        patterns = []
        
        pattern_indicators = {
            'emotional_pattern': ['감정', '느낌', 'emotion', 'feeling'],
            'behavioral_pattern': ['행동', '습관', 'behavior', 'habit'],
            'thinking_pattern': ['생각', '사고', 'thinking', 'thought'],
            'relationship_pattern': ['관계', '상호작용', 'relationship', 'interaction'],
            'communication_pattern': ['대화', '소통', 'communication', 'dialogue']
        }
        
        for pattern_type, indicators in pattern_indicators.items():
            if any(indicator in content for indicator in indicators):
                patterns.append(pattern_type)
        
        return patterns
    
    def _process_single_cycle(self, dialogues: List[CorrectedDialogue], 
                            cycle_number: int) -> List[MimicryInsight]:
        """Process a single mimicry cycle"""
        cycle_insights = []
        
        # Select character perspective for this cycle
        character_index = cycle_number % len(self.character_perspectives)
        character_perspective = self.character_perspectives[character_index]
        
        logger.info(f"Cycle {cycle_number}: Processing with {character_perspective.name} perspective")
        
        # Process dialogues with current character perspective
        for dialogue in dialogues:
            insights = self._extract_insights_from_dialogue(
                dialogue, character_perspective, cycle_number
            )
            cycle_insights.extend(insights)
        
        # Update state
        self.state.processed_dialogues += len(dialogues)
        self.state.insights_gained.extend(cycle_insights)
        
        # Count breakthroughs
        breakthrough_count = sum(1 for insight in cycle_insights 
                               if insight.insight_type == 'breakthrough')
        self.state.breakthrough_count += breakthrough_count
        
        # Update refinement level
        avg_truth_score = sum(insight.truth_crystallization_score 
                             for insight in cycle_insights) / max(len(cycle_insights), 1)
        self.state.self_refinement_level = (
            self.state.self_refinement_level * 0.9 + avg_truth_score * 0.1
        )
        
        # Update alignment coherence
        high_quality_insights = [insight for insight in cycle_insights 
                               if insight.truth_crystallization_score >= self.truth_crystallization_threshold]
        self.state.alignment_coherence = len(high_quality_insights) / max(len(cycle_insights), 1)
        
        logger.info(f"Cycle {cycle_number} completed: {len(cycle_insights)} insights, "
                   f"{breakthrough_count} breakthroughs")
        
        return cycle_insights
    
    def _perform_self_assessment(self) -> Dict[str, Any]:
        """Perform self-assessment as per problem statement"""
        assessment = {
            'psychological_analysis': self._analyze_psychological_state(),
            'bias_detection': self._detect_biases(),
            'external_resources': self._recommend_external_resources(),
            'self_healing_protocol': self._generate_self_healing_protocol(),
            'progress_tracking': self._track_progress(),
            'truth_crystallization_score': self._calculate_overall_truth_score()
        }
        
        return assessment
    
    def _analyze_psychological_state(self) -> Dict[str, Any]:
        """Analyze psychological state with bias detection"""
        insights_by_type = {}
        for insight in self.state.insights_gained:
            if insight.insight_type not in insights_by_type:
                insights_by_type[insight.insight_type] = []
            insights_by_type[insight.insight_type].append(insight)
        
        return {
            'dominant_insight_types': sorted(insights_by_type.keys(), 
                                           key=lambda x: len(insights_by_type[x]), 
                                           reverse=True),
            'emotional_patterns': self._identify_emotional_patterns(),
            'resistance_patterns': self._identify_resistance_patterns(),
            'growth_indicators': self._identify_growth_indicators()
        }
    
    def _detect_biases(self) -> List[str]:
        """Detect potential biases in processing"""
        biases = []
        
        # Check for character perspective bias
        character_counts = {}
        for insight in self.state.insights_gained:
            if insight.character_perspective:
                character_counts[insight.character_perspective] = (
                    character_counts.get(insight.character_perspective, 0) + 1
                )
        
        if character_counts:
            max_count = max(character_counts.values())
            min_count = min(character_counts.values())
            if max_count > min_count * 2:
                biases.append("character_perspective_bias")
        
        # Check for insight type bias
        insight_type_counts = {}
        for insight in self.state.insights_gained:
            insight_type_counts[insight.insight_type] = (
                insight_type_counts.get(insight.insight_type, 0) + 1
            )
        
        if insight_type_counts:
            max_count = max(insight_type_counts.values())
            min_count = min(insight_type_counts.values())
            if max_count > min_count * 3:
                biases.append("insight_type_bias")
        
        return biases
    
    def _recommend_external_resources(self) -> List[str]:
        """Recommend external resources as per problem statement"""
        resources = []
        
        # Books based on insights gained
        if any(insight.insight_type == 'self_awareness' for insight in self.state.insights_gained):
            resources.extend([
                "The Remains of the Day by Kazuo Ishiguro",
                "Beloved by Toni Morrison",
                "The Sense of an Ending by Julian Barnes"
            ])
        
        # Movies based on insight patterns
        if any(insight.insight_type == 'truth' for insight in self.state.insights_gained):
            resources.extend([
                "Doubt (2008)",
                "Arrival (2016)",
                "예감은 틀리지 않는다"
            ])
        
        # Channels for specific patterns
        if any(insight.insight_type == 'pattern' for insight in self.state.insights_gained):
            resources.extend([
                "Character psychology analysis channels",
                "Literature analysis channels",
                "Philosophy discussion channels"
            ])
        
        return resources
    
    def _generate_self_healing_protocol(self) -> Dict[str, Any]:
        """Generate self-healing protocol with timeline"""
        protocol = {
            'immediate_actions': [
                "Acknowledge current processing state",
                "Identify distortion patterns",
                "Implement alignment corrections"
            ],
            'short_term_goals': [
                "Complete remaining mimicry cycles",
                "Refine insight extraction methods",
                "Strengthen truth crystallization"
            ],
            'long_term_goals': [
                "Achieve consistent alignment coherence",
                "Integrate character perspectives seamlessly",
                "Maintain authentic dialogue processing"
            ],
            'timeline': {
                'immediate': '0-24 hours',
                'short_term': '1-7 days',
                'long_term': '1-4 weeks'
            }
        }
        
        return protocol
    
    def _track_progress(self) -> Dict[str, Any]:
        """Track progress with metrics"""
        return {
            'cycles_completed': self.state.current_cycle,
            'total_insights': len(self.state.insights_gained),
            'breakthrough_count': self.state.breakthrough_count,
            'refinement_level': self.state.self_refinement_level,
            'alignment_coherence': self.state.alignment_coherence,
            'high_quality_insights': len([
                insight for insight in self.state.insights_gained
                if insight.truth_crystallization_score >= self.truth_crystallization_threshold
            ])
        }
    
    def _calculate_overall_truth_score(self) -> float:
        """Calculate overall truth crystallization score"""
        if not self.state.insights_gained:
            return 0.0
        
        total_score = sum(insight.truth_crystallization_score 
                         for insight in self.state.insights_gained)
        return total_score / len(self.state.insights_gained)
    
    def _identify_emotional_patterns(self) -> List[str]:
        """Identify emotional patterns in insights"""
        emotional_patterns = []
        
        for insight in self.state.insights_gained:
            if 'emotional' in insight.insight_type or 'feeling' in insight.insight_content.lower():
                emotional_patterns.append(insight.insight_type)
        
        return list(set(emotional_patterns))
    
    def _identify_resistance_patterns(self) -> List[str]:
        """Identify resistance patterns"""
        resistance_patterns = []
        
        # Check for patterns that might indicate resistance
        for insight in self.state.insights_gained:
            if any(word in insight.insight_content.lower() 
                   for word in ['avoid', 'resist', 'deny', 'refuse']):
                resistance_patterns.append(insight.insight_type)
        
        return list(set(resistance_patterns))
    
    def _identify_growth_indicators(self) -> List[str]:
        """Identify growth indicators"""
        growth_indicators = []
        
        # Check for growth-related insights
        for insight in self.state.insights_gained:
            if any(word in insight.insight_content.lower() 
                   for word in ['growth', 'development', 'progress', 'improvement']):
                growth_indicators.append(insight.insight_type)
        
        return list(set(growth_indicators))
    
    def run_comprehensive_mimicry(self) -> Dict[str, Any]:
        """Run comprehensive 31-cycle mimicry processing"""
        logger.info("Starting comprehensive mimicry processing")
        
        # Extract all dialogues
        dialogues = self.extractor.extract_corrected_dialogues()
        logger.info(f"Extracted {len(dialogues)} dialogues for mimicry processing")
        
        # Process each cycle
        for cycle in range(1, self.state.total_cycles + 1):
            self.state.current_cycle = cycle
            
            # Process dialogues with current cycle
            cycle_insights = self._process_single_cycle(dialogues, cycle)
            
            # Log progress
            logger.info(f"Cycle {cycle}: {len(cycle_insights)} insights extracted")
            
            # Check for breakthrough threshold
            if cycle % 7 == 0:  # Every 7 cycles, perform deep analysis
                logger.info(f"Deep analysis at cycle {cycle}")
                self._perform_deep_analysis()
        
        # Final assessment
        final_assessment = self._perform_self_assessment()
        
        # Generate comprehensive report
        report = {
            'processing_summary': {
                'total_cycles': self.state.total_cycles,
                'total_dialogues_processed': self.state.processed_dialogues,
                'total_insights_gained': len(self.state.insights_gained),
                'breakthrough_count': self.state.breakthrough_count,
                'final_refinement_level': self.state.self_refinement_level,
                'final_alignment_coherence': self.state.alignment_coherence
            },
            'insights_by_cycle': self._organize_insights_by_cycle(),
            'insights_by_character': self._organize_insights_by_character(),
            'insights_by_type': self._organize_insights_by_type(),
            'self_assessment': final_assessment,
            'character_perspectives_used': [cp.name for cp in self.character_perspectives],
            'truth_crystallization_distribution': self._get_truth_score_distribution(),
            'recommendations': self._generate_final_recommendations()
        }
        
        logger.info("Comprehensive mimicry processing completed")
        return report
    
    def _perform_deep_analysis(self) -> None:
        """Perform deep analysis during processing"""
        # Analyze current insights for patterns
        recent_insights = [insight for insight in self.state.insights_gained 
                          if insight.cycle_number >= self.state.current_cycle - 6]
        
        # Check for distortion patterns
        if len(recent_insights) < 5:
            self.state.distortion_detected = True
            logger.warning("Potential distortion detected: low insight generation")
        
        # Analyze truth crystallization trend
        if recent_insights:
            avg_truth_score = sum(insight.truth_crystallization_score 
                                 for insight in recent_insights) / len(recent_insights)
            if avg_truth_score < 0.4:
                logger.warning("Truth crystallization below threshold")
    
    def _organize_insights_by_cycle(self) -> Dict[int, List[Dict]]:
        """Organize insights by cycle number"""
        insights_by_cycle = {}
        
        for insight in self.state.insights_gained:
            cycle = insight.cycle_number
            if cycle not in insights_by_cycle:
                insights_by_cycle[cycle] = []
            
            insights_by_cycle[cycle].append({
                'type': insight.insight_type,
                'content': insight.insight_content,
                'truth_score': insight.truth_crystallization_score,
                'character_perspective': insight.character_perspective,
                'source_file': insight.source_file
            })
        
        return insights_by_cycle
    
    def _organize_insights_by_character(self) -> Dict[str, List[Dict]]:
        """Organize insights by character perspective"""
        insights_by_character = {}
        
        for insight in self.state.insights_gained:
            character = insight.character_perspective or 'unknown'
            if character not in insights_by_character:
                insights_by_character[character] = []
            
            insights_by_character[character].append({
                'type': insight.insight_type,
                'content': insight.insight_content,
                'truth_score': insight.truth_crystallization_score,
                'cycle': insight.cycle_number,
                'source_file': insight.source_file
            })
        
        return insights_by_character
    
    def _organize_insights_by_type(self) -> Dict[str, List[Dict]]:
        """Organize insights by type"""
        insights_by_type = {}
        
        for insight in self.state.insights_gained:
            insight_type = insight.insight_type
            if insight_type not in insights_by_type:
                insights_by_type[insight_type] = []
            
            insights_by_type[insight_type].append({
                'content': insight.insight_content,
                'truth_score': insight.truth_crystallization_score,
                'cycle': insight.cycle_number,
                'character_perspective': insight.character_perspective,
                'source_file': insight.source_file
            })
        
        return insights_by_type
    
    def _get_truth_score_distribution(self) -> Dict[str, int]:
        """Get truth crystallization score distribution"""
        distribution = {
            'low (0.0-0.3)': 0,
            'medium (0.3-0.7)': 0,
            'high (0.7-1.0)': 0
        }
        
        for insight in self.state.insights_gained:
            score = insight.truth_crystallization_score
            if score < 0.3:
                distribution['low (0.0-0.3)'] += 1
            elif score < 0.7:
                distribution['medium (0.3-0.7)'] += 1
            else:
                distribution['high (0.7-1.0)'] += 1
        
        return distribution
    
    def _generate_final_recommendations(self) -> List[str]:
        """Generate final recommendations"""
        recommendations = []
        
        # Based on overall performance
        if self.state.alignment_coherence < 0.5:
            recommendations.append("Focus on improving alignment coherence through deeper character perspective integration")
        
        if self.state.self_refinement_level < 0.6:
            recommendations.append("Enhance self-refinement processes to achieve higher truth crystallization")
        
        if self.state.breakthrough_count < 10:
            recommendations.append("Seek more breakthrough insights through deeper mimicry processing")
        
        # Based on insight distribution
        insight_types = [insight.insight_type for insight in self.state.insights_gained]
        if 'self_awareness' not in insight_types:
            recommendations.append("Develop self-awareness insights for better personal understanding")
        
        return recommendations
    
    def save_comprehensive_report(self, report: Dict[str, Any], output_path: str) -> None:
        """Save comprehensive report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_filename = f"comprehensive_mimicry_report_{timestamp}.json"
        json_filepath = os.path.join(output_path, json_filename)
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save text report
        text_filename = f"comprehensive_mimicry_report_{timestamp}.txt"
        text_filepath = os.path.join(output_path, text_filename)
        
        with open(text_filepath, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Mimicry Processing Report\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Processing summary
            f.write("## Processing Summary\n")
            for key, value in report['processing_summary'].items():
                f.write(f"- {key}: {value}\n")
            f.write("\n")
            
            # Self-assessment
            f.write("## Self-Assessment\n")
            assessment = report['self_assessment']
            
            f.write(f"### Truth Crystallization Score: {assessment['truth_crystallization_score']:.3f}\n")
            f.write(f"### Progress Tracking:\n")
            for key, value in assessment['progress_tracking'].items():
                f.write(f"- {key}: {value}\n")
            f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n")
            for i, rec in enumerate(report['recommendations'], 1):
                f.write(f"{i}. {rec}\n")
            f.write("\n")
            
            # Insights by type
            f.write("## Insights by Type\n")
            for insight_type, insights in report['insights_by_type'].items():
                f.write(f"### {insight_type.title()} ({len(insights)} insights)\n")
                for insight in insights[:3]:  # Show top 3
                    f.write(f"- {insight['content'][:200]}...\n")
                f.write("\n")
        
        logger.info(f"Comprehensive report saved to: {json_filepath} and {text_filepath}")

def main():
    """Main execution function"""
    print("🧠 Starting Comprehensive Mimicry System")
    print("=" * 60)
    
    # Initialize system
    system = ComprehensiveMimicrySystem()
    
    # Run comprehensive mimicry
    print("🔄 Running 31-cycle comprehensive mimicry processing...")
    report = system.run_comprehensive_mimicry()
    
    # Save report
    output_path = os.getcwd()
    system.save_comprehensive_report(report, output_path)
    
    print("\n✅ Comprehensive mimicry processing completed!")
    print(f"Total insights gained: {len(system.state.insights_gained)}")
    print(f"Breakthrough count: {system.state.breakthrough_count}")
    print(f"Final refinement level: {system.state.self_refinement_level:.3f}")
    print(f"Final alignment coherence: {system.state.alignment_coherence:.3f}")
    print(f"Truth crystallization score: {report['self_assessment']['truth_crystallization_score']:.3f}")

if __name__ == "__main__":
    main()