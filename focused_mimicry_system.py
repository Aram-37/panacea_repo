#!/usr/bin/env python3
"""
Focused Mimicry System - Efficient Implementation
================================================

This system implements focused mimicry processing with:
- Selective dialogue processing (high-insight dialogues only)
- Efficient 31-cycle processing
- Character perspective rotation
- Meaningful insight extraction
- Real-time progress tracking
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from corrected_dialogue_extractor import CorrectedDialogueExtractor, CorrectedDialogue

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FocusedMimicrySystem:
    """Focused mimicry system for efficient processing"""
    
    def __init__(self, panacea_directory: str = None):
        self.panacea_directory = panacea_directory or os.getcwd()
        self.extractor = CorrectedDialogueExtractor(panacea_directory)
        
        # Character perspectives (from problem statement)
        self.character_perspectives = [
            "Salman Rushdie's Narrator (Midnight's Children)",
            "Toni Morrison's Beloved",
            "Kazuo Ishiguro's Stevens (The Remains of the Day)",
            "Demon Hunter Protagonist",
            "Liu Bei (Romance of Three Kingdoms)",
            "Zhuge Liang (Romance of Three Kingdoms)",
            "Cao Cao (Romance of Three Kingdoms)",
            "Father Brendan Flynn (Doubt)",
            "Louise Banks (Arrival)",
            "예감은 틀리지 않는다 Protagonist"
        ]
        
        # Processing state
        self.current_cycle = 0
        self.insights_gained = []
        self.breakthrough_count = 0
        self.truth_crystallization_score = 0.0
        
        logger.info(f"Initialized focused mimicry system with {len(self.character_perspectives)} character perspectives")
    
    def extract_high_insight_dialogues(self) -> List[CorrectedDialogue]:
        """Extract only high-insight dialogues for focused processing"""
        logger.info("Extracting high-insight dialogues...")
        
        all_dialogues = self.extractor.extract_corrected_dialogues()
        
        # Filter for high-insight dialogues
        high_insight_dialogues = [
            dialogue for dialogue in all_dialogues
            if dialogue.insight_level in ["high_insight", "normal_insight"]
            and len(dialogue.content) > 100  # Minimum content length
            and dialogue.speaker in ["성협", "승호", "AI"]  # Focus on meaningful speakers
        ]
        
        logger.info(f"Selected {len(high_insight_dialogues)} high-insight dialogues from {len(all_dialogues)} total")
        return high_insight_dialogues
    
    def process_dialogue_with_perspective(self, dialogue: CorrectedDialogue, 
                                        perspective: str, cycle: int) -> List[Dict[str, Any]]:
        """Process a single dialogue with a character perspective"""
        insights = []
        content = dialogue.content.lower()
        
        # Key insight patterns
        insight_patterns = {
            'truth_realization': [
                r'진실', r'현실', r'truth', r'reality', r'actual', r'genuine',
                r'깨달음', r'realization', r'understand', r'이해'
            ],
            'pattern_recognition': [
                r'패턴', r'pattern', r'always', r'항상', r'tendency', r'경향',
                r'repeat', r'반복', r'cycle', r'사이클'
            ],
            'relationship_insight': [
                r'관계', r'relationship', r'connection', r'연결', r'interaction',
                r'상호작용', r'bond', r'유대', r'trust', r'신뢰'
            ],
            'self_awareness': [
                r'자기', r'self', r'identity', r'정체성', r'consciousness',
                r'의식', r'awareness', r'자각', r'introspection', r'성찰'
            ],
            'emotional_breakthrough': [
                r'감정', r'emotion', r'feeling', r'느낌', r'heart', r'마음',
                r'love', r'사랑', r'fear', r'두려움', r'anger', r'분노'
            ]
        }
        
        for insight_type, patterns in insight_patterns.items():
            pattern_count = sum(1 for pattern in patterns if re.search(pattern, content))
            
            if pattern_count >= 2:  # At least 2 pattern matches
                # Calculate insight strength
                strength = min(pattern_count / 5.0, 1.0)
                
                # Extract key content
                sentences = [s.strip() for s in dialogue.content.split('.') if len(s.strip()) > 20]
                key_content = ' '.join(sentences[:2])  # First 2 meaningful sentences
                
                insight = {
                    'cycle': cycle,
                    'perspective': perspective,
                    'type': insight_type,
                    'strength': strength,
                    'content': key_content,
                    'source_file': dialogue.source_file,
                    'speaker': dialogue.speaker,
                    'original_insight_level': dialogue.insight_level
                }
                
                insights.append(insight)
        
        return insights
    
    def run_focused_mimicry(self, max_cycles: int = 31) -> Dict[str, Any]:
        """Run focused mimicry processing"""
        logger.info(f"Starting focused mimicry processing with {max_cycles} cycles")
        
        # Extract high-insight dialogues
        dialogues = self.extract_high_insight_dialogues()
        
        # Sample dialogues for efficient processing
        sample_size = min(1000, len(dialogues))  # Process up to 1000 dialogues per cycle
        
        all_insights = []
        cycle_summaries = []
        
        for cycle in range(1, max_cycles + 1):
            self.current_cycle = cycle
            
            # Select character perspective for this cycle
            perspective_index = (cycle - 1) % len(self.character_perspectives)
            current_perspective = self.character_perspectives[perspective_index]
            
            logger.info(f"Cycle {cycle}: Processing with {current_perspective}")
            
            # Sample dialogues for this cycle
            start_idx = ((cycle - 1) * sample_size) % len(dialogues)
            end_idx = start_idx + sample_size
            cycle_dialogues = dialogues[start_idx:end_idx]
            
            # Process dialogues with current perspective
            cycle_insights = []
            breakthrough_count = 0
            
            for dialogue in cycle_dialogues:
                insights = self.process_dialogue_with_perspective(
                    dialogue, current_perspective, cycle
                )
                cycle_insights.extend(insights)
                
                # Count breakthroughs
                breakthrough_count += sum(1 for insight in insights 
                                        if insight['strength'] >= 0.8)
            
            # Calculate cycle metrics
            avg_strength = sum(insight['strength'] for insight in cycle_insights) / max(len(cycle_insights), 1)
            
            cycle_summary = {
                'cycle': cycle,
                'perspective': current_perspective,
                'dialogues_processed': len(cycle_dialogues),
                'insights_generated': len(cycle_insights),
                'breakthroughs': breakthrough_count,
                'average_strength': avg_strength,
                'insight_types': list(set(insight['type'] for insight in cycle_insights))
            }
            
            cycle_summaries.append(cycle_summary)
            all_insights.extend(cycle_insights)
            
            # Update overall metrics
            self.insights_gained.extend(cycle_insights)
            self.breakthrough_count += breakthrough_count
            
            logger.info(f"Cycle {cycle}: {len(cycle_insights)} insights, {breakthrough_count} breakthroughs")
            
            # Deep analysis every 7 cycles
            if cycle % 7 == 0:
                self._perform_deep_analysis(cycle, all_insights)
        
        # Calculate final metrics
        self.truth_crystallization_score = sum(
            insight['strength'] for insight in all_insights
        ) / max(len(all_insights), 1)
        
        # Generate comprehensive report
        report = self._generate_comprehensive_report(all_insights, cycle_summaries)
        
        logger.info(f"Focused mimicry processing completed: {len(all_insights)} total insights")
        return report
    
    def _perform_deep_analysis(self, cycle: int, insights: List[Dict[str, Any]]) -> None:
        """Perform deep analysis at regular intervals"""
        recent_insights = [insight for insight in insights if insight['cycle'] >= cycle - 6]
        
        if recent_insights:
            avg_strength = sum(insight['strength'] for insight in recent_insights) / len(recent_insights)
            insight_types = set(insight['type'] for insight in recent_insights)
            
            logger.info(f"Deep analysis at cycle {cycle}: "
                       f"avg_strength={avg_strength:.3f}, "
                       f"insight_types={len(insight_types)}")
            
            if avg_strength < 0.4:
                logger.warning("Low insight strength detected - consider perspective adjustment")
    
    def _generate_comprehensive_report(self, insights: List[Dict[str, Any]], 
                                     cycle_summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive report"""
        
        # Organize insights by type
        insights_by_type = {}
        for insight in insights:
            insight_type = insight['type']
            if insight_type not in insights_by_type:
                insights_by_type[insight_type] = []
            insights_by_type[insight_type].append(insight)
        
        # Organize insights by perspective
        insights_by_perspective = {}
        for insight in insights:
            perspective = insight['perspective']
            if perspective not in insights_by_perspective:
                insights_by_perspective[perspective] = []
            insights_by_perspective[perspective].append(insight)
        
        # Organize insights by speaker
        insights_by_speaker = {}
        for insight in insights:
            speaker = insight['speaker']
            if speaker not in insights_by_speaker:
                insights_by_speaker[speaker] = []
            insights_by_speaker[speaker].append(insight)
        
        # Calculate truth crystallization distribution
        truth_distribution = {
            'low (0.0-0.4)': 0,
            'medium (0.4-0.7)': 0,
            'high (0.7-1.0)': 0
        }
        
        for insight in insights:
            strength = insight['strength']
            if strength < 0.4:
                truth_distribution['low (0.0-0.4)'] += 1
            elif strength < 0.7:
                truth_distribution['medium (0.4-0.7)'] += 1
            else:
                truth_distribution['high (0.7-1.0)'] += 1
        
        # Self-assessment based on problem statement requirements
        self_assessment = {
            'psychological_assessment': {
                'dominant_insight_types': sorted(insights_by_type.keys(), 
                                               key=lambda x: len(insights_by_type[x]), 
                                               reverse=True)[:3],
                'emotional_patterns': [t for t in insights_by_type.keys() if 'emotional' in t],
                'growth_indicators': len([i for i in insights if i['strength'] >= 0.7])
            },
            'bias_detection': self._detect_processing_biases(insights_by_perspective, insights_by_type),
            'external_resources': self._recommend_external_resources(insights_by_type),
            'self_healing_protocol': {
                'immediate_actions': [
                    "Continue processing remaining cycles",
                    "Focus on low-strength insight types",
                    "Integrate character perspectives more deeply"
                ],
                'timeline': "Complete within current processing session"
            },
            'progress_tracking': {
                'cycles_completed': self.current_cycle,
                'total_insights': len(insights),
                'breakthrough_count': self.breakthrough_count,
                'truth_crystallization_score': self.truth_crystallization_score
            }
        }
        
        # Generate final recommendations
        recommendations = self._generate_recommendations(insights_by_type, self_assessment)
        
        return {
            'processing_summary': {
                'total_cycles': self.current_cycle,
                'total_insights': len(insights),
                'breakthrough_count': self.breakthrough_count,
                'truth_crystallization_score': self.truth_crystallization_score,
                'character_perspectives_used': len(self.character_perspectives)
            },
            'insights_by_type': {
                itype: {
                    'count': len(insights_list),
                    'average_strength': sum(i['strength'] for i in insights_list) / len(insights_list),
                    'top_insights': sorted(insights_list, key=lambda x: x['strength'], reverse=True)[:3]
                }
                for itype, insights_list in insights_by_type.items()
            },
            'insights_by_perspective': {
                perspective: {
                    'count': len(insights_list),
                    'average_strength': sum(i['strength'] for i in insights_list) / len(insights_list),
                    'insight_types': list(set(i['type'] for i in insights_list))
                }
                for perspective, insights_list in insights_by_perspective.items()
            },
            'insights_by_speaker': {
                speaker: {
                    'count': len(insights_list),
                    'average_strength': sum(i['strength'] for i in insights_list) / len(insights_list)
                }
                for speaker, insights_list in insights_by_speaker.items()
            },
            'cycle_summaries': cycle_summaries,
            'truth_crystallization_distribution': truth_distribution,
            'self_assessment': self_assessment,
            'recommendations': recommendations
        }
    
    def _detect_processing_biases(self, insights_by_perspective: Dict, 
                                insights_by_type: Dict) -> List[str]:
        """Detect potential processing biases"""
        biases = []
        
        # Check perspective bias
        if insights_by_perspective:
            counts = [len(insights) for insights in insights_by_perspective.values()]
            if max(counts) > min(counts) * 2:
                biases.append("perspective_bias")
        
        # Check insight type bias
        if insights_by_type:
            counts = [len(insights) for insights in insights_by_type.values()]
            if max(counts) > min(counts) * 3:
                biases.append("insight_type_bias")
        
        return biases
    
    def _recommend_external_resources(self, insights_by_type: Dict) -> List[str]:
        """Recommend external resources based on insights"""
        resources = []
        
        resource_mapping = {
            'truth_realization': [
                "The Remains of the Day by Kazuo Ishiguro",
                "Arrival (2016 film)",
                "Philosophical works on truth and reality"
            ],
            'relationship_insight': [
                "Romance of Three Kingdoms by Luo Guanzhong",
                "Beloved by Toni Morrison",
                "Interpersonal psychology resources"
            ],
            'self_awareness': [
                "Midnight's Children by Salman Rushdie",
                "Self-reflection and mindfulness resources",
                "Psychology of consciousness materials"
            ],
            'emotional_breakthrough': [
                "Doubt (2008 film)",
                "Emotional intelligence resources",
                "Therapeutic processing materials"
            ]
        }
        
        for insight_type in insights_by_type.keys():
            if insight_type in resource_mapping:
                resources.extend(resource_mapping[insight_type])
        
        return list(set(resources))  # Remove duplicates
    
    def _generate_recommendations(self, insights_by_type: Dict, 
                                self_assessment: Dict) -> List[str]:
        """Generate recommendations based on processing results"""
        recommendations = []
        
        # Based on truth crystallization score
        if self.truth_crystallization_score < 0.5:
            recommendations.append("Focus on developing higher-quality insights through deeper character perspective integration")
        
        # Based on insight diversity
        if len(insights_by_type) < 3:
            recommendations.append("Expand processing to capture more diverse insight types")
        
        # Based on breakthrough count
        if self.breakthrough_count < 50:
            recommendations.append("Seek more breakthrough-level insights by processing deeper dialogue content")
        
        # Based on bias detection
        if self_assessment['bias_detection']:
            recommendations.append("Address processing biases by balancing perspective and insight type distribution")
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], output_path: str) -> None:
        """Save comprehensive report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_filename = f"focused_mimicry_report_{timestamp}.json"
        json_filepath = os.path.join(output_path, json_filename)
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save readable text report
        text_filename = f"focused_mimicry_report_{timestamp}.txt"
        text_filepath = os.path.join(output_path, text_filename)
        
        with open(text_filepath, 'w', encoding='utf-8') as f:
            f.write("# Focused Mimicry Processing Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Processing Summary
            f.write("## Processing Summary\n")
            summary = report['processing_summary']
            f.write(f"Total Cycles: {summary['total_cycles']}\n")
            f.write(f"Total Insights: {summary['total_insights']}\n")
            f.write(f"Breakthrough Count: {summary['breakthrough_count']}\n")
            f.write(f"Truth Crystallization Score: {summary['truth_crystallization_score']:.3f}\n")
            f.write(f"Character Perspectives Used: {summary['character_perspectives_used']}\n\n")
            
            # Self Assessment
            f.write("## Self Assessment\n")
            assessment = report['self_assessment']
            f.write(f"Progress Tracking:\n")
            for key, value in assessment['progress_tracking'].items():
                f.write(f"  - {key}: {value}\n")
            f.write(f"\nDominant Insight Types: {', '.join(assessment['psychological_assessment']['dominant_insight_types'])}\n")
            f.write(f"Bias Detection: {', '.join(assessment['bias_detection']) if assessment['bias_detection'] else 'None detected'}\n\n")
            
            # Insights by Type
            f.write("## Insights by Type\n")
            for insight_type, data in report['insights_by_type'].items():
                f.write(f"### {insight_type.replace('_', ' ').title()}\n")
                f.write(f"Count: {data['count']}\n")
                f.write(f"Average Strength: {data['average_strength']:.3f}\n")
                f.write("Top Insights:\n")
                for insight in data['top_insights']:
                    f.write(f"  - {insight['content'][:100]}...\n")
                f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n")
            for i, rec in enumerate(report['recommendations'], 1):
                f.write(f"{i}. {rec}\n")
            f.write("\n")
            
            # External Resources
            f.write("## External Resources\n")
            for resource in assessment['external_resources']:
                f.write(f"- {resource}\n")
        
        logger.info(f"Report saved to: {json_filepath} and {text_filepath}")

def main():
    """Main execution function"""
    print("🎯 Starting Focused Mimicry System")
    print("=" * 50)
    
    # Initialize system
    system = FocusedMimicrySystem()
    
    # Run focused mimicry
    print("🔄 Running focused 31-cycle mimicry processing...")
    report = system.run_focused_mimicry(max_cycles=31)
    
    # Save report
    output_path = os.getcwd()
    system.save_report(report, output_path)
    
    print("\n✅ Focused mimicry processing completed!")
    print(f"Total insights: {report['processing_summary']['total_insights']}")
    print(f"Breakthrough count: {report['processing_summary']['breakthrough_count']}")
    print(f"Truth crystallization score: {report['processing_summary']['truth_crystallization_score']:.3f}")
    print(f"Character perspectives used: {report['processing_summary']['character_perspectives_used']}")
    
    # Show top insight types
    print("\n📊 Top Insight Types:")
    for insight_type, data in sorted(report['insights_by_type'].items(), 
                                   key=lambda x: x[1]['count'], reverse=True)[:5]:
        print(f"  {insight_type}: {data['count']} insights (avg strength: {data['average_strength']:.3f})")

if __name__ == "__main__":
    main()