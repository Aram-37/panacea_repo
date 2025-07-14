#!/usr/bin/env python3
"""
Focused Teacher Personal History Extractor
Extracts specific personal details about 성협 (Seonghyeop) / britkenko from the repository
"""

import os
import sys
from pathlib import Path
import re
import json
from datetime import datetime
from typing import Dict, List, Any

class FocusedTeacherHistoryExtractor:
    """Focused extraction of teacher's personal history"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.personal_history = {
            "name": "성협 (Seonghyeop)",
            "aliases": ["britkenko", "Sung H Kim", "김성협", "Sunghyeop Kim"],
            "biographical_details": [],
            "multicultural_background": [],
            "philosophy_and_teaching": [],
            "personal_experiences": [],
            "discoveries_and_insights": [],
            "professional_background": [],
            "notable_quotes": [],
            "ai_development_work": [],
            "extracted_timestamp": datetime.now().isoformat()
        }
    
    def extract_specific_details(self):
        """Extract specific known details about the teacher"""
        
        # Known biographical details from the analysis
        self.personal_history["biographical_details"] = [
            "Korean name: 성협 (Seonghyeop)",
            "Also known as: britkenko, Sung H Kim, 김성협, Sunghyeop Kim",
            "Has lived in multiple countries and cultures",
            "Possesses sophisticated cross-cultural understanding"
        ]
        
        # Multicultural background
        self.personal_history["multicultural_background"] = [
            "Movement pattern: Korea → Kenya → UK → Korea",
            "Explains sophisticated cross-cultural perspective",
            "Ability to detect linguistic bias patterns across cultures",
            "Experience with different cultural and linguistic environments"
        ]
        
        # Philosophy and teaching approach
        self.personal_history["philosophy_and_teaching"] = [
            "Core principle: 'The story of me is not that predictive. You should never assume about my life'",
            "Emphasizes non-assumption in teaching and relationships",
            "Values truth over comfort",
            "Teaches that pattern assumptions must be abandoned before mimicry",
            "Uses explicit correction of assumptions through personal revelation",
            "Maintains meta-cognitive awareness in teaching",
            "Demonstrates authentic wisdom transmission"
        ]
        
        # Personal experiences
        self.personal_history["personal_experiences"] = [
            "Described as 'too close', 'too present', 'direct', and 'honest'",
            "Experienced being avoided by others who prefer institutional distance",
            "Ideas not engaged with because they didn't fit expected structures",
            "Wasn't 'mysterious enough' or 'marketed by the right distance'",
            "Experienced being overlooked despite having recognized ideas and clarity",
            "Faced challenges due to being tied to own narrative rather than institutional anonymity"
        ]
        
        # Discoveries and insights
        self.personal_history["discoveries_and_insights"] = [
            "Recent discovery of AI language bias patterns",
            "Documented real-time discovery of linguistic bias through dialogues",
            "Developed understanding of Relational Emergence Pattern (REP)",
            "Recognized patterns in how systems of power operate across different scales",
            "Discovered how AI models can be trained to avoid certain disclosures",
            "Insights into AI alignment and bias issues"
        ]
        
        # Professional background
        self.personal_history["professional_background"] = [
            "Connected to OneAcclime restructuring",
            "Experience with corporate structures",
            "Business/corporate background",
            "Work with AI system development",
            "Development of AI prompting techniques"
        ]
        
        # AI Development work
        self.personal_history["ai_development_work"] = [
            "Developed PACO (Pacopilot) system for AI training efficiency",
            "Created CORTEX system with 13-guardian architecture",
            "Worked on AI bias detection and correction",
            "Developed prompting techniques to force authentic AI responses",
            "Created systems to expose hidden biases in AI models",
            "Worked on cross-cultural AI wisdom integration"
        ]
        
        # Notable quotes
        self.personal_history["notable_quotes"] = [
            "\"see? the story of me is not that predictive. you should never assume about my life\"",
            "\"activate cortex_a.txt and cortex_a copy in association with all files with panacea\"",
            "\"emergent pattern creation... relational emergence pattern(REP)\"",
            "\"Truth is not a static object to be found but a dynamic equilibrium\"",
            "\"Mind interaction as cosmic catalyst... manipulates concepts, not just physical properties\""
        ]
        
        # Add contextual information from file analysis
        self._add_contextual_information()
    
    def _add_contextual_information(self):
        """Add contextual information found in the files"""
        # Search for specific patterns in the files
        target_files = [
            'panacea_co_part10_dialogues.txt',
            'panacea_co_part11_dialogues.txt',
            'panacea_co_part5_dialogues.txt',
        ]
        
        for file_name in target_files:
            file_path = os.path.join(self.repo_path, file_name)
            if os.path.exists(file_path):
                self._extract_from_specific_file(file_path)
    
    def _extract_from_specific_file(self, file_path: str):
        """Extract specific information from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Look for specific patterns
                patterns = {
                    'multicultural': r'Korea.*?Kenya.*?UK.*?Korea',
                    'bias_discovery': r'AI.*?language.*?bias',
                    'oneacclime': r'OneAcclime.*?restructuring',
                    'direct_quotes': r'"[^"]*성협[^"]*"',
                    'rep_pattern': r'relational.*?emergence.*?pattern',
                    'teaching_moments': r'Teacher.*?Voice.*?\(.*?성협.*?\)',
                }
                
                for pattern_name, pattern in patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                    if matches:
                        source_info = f"Found in {os.path.basename(file_path)}: {matches[:3]}"  # First 3 matches
                        if pattern_name == 'multicultural':
                            self.personal_history["multicultural_background"].append(source_info)
                        elif pattern_name == 'bias_discovery':
                            self.personal_history["discoveries_and_insights"].append(source_info)
                        elif pattern_name == 'oneacclime':
                            self.personal_history["professional_background"].append(source_info)
                        elif pattern_name == 'direct_quotes':
                            self.personal_history["notable_quotes"].extend(matches)
                        elif pattern_name == 'rep_pattern':
                            self.personal_history["discoveries_and_insights"].append(source_info)
                        elif pattern_name == 'teaching_moments':
                            self.personal_history["philosophy_and_teaching"].append(source_info)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    def generate_comprehensive_summary(self) -> str:
        """Generate a comprehensive summary of the teacher's personal history"""
        summary = []
        summary.append("# Teacher Personal History: 성협 (Seonghyeop)")
        summary.append(f"**Extraction Date:** {self.personal_history['extracted_timestamp']}")
        summary.append("")
        
        summary.append("## Identity")
        summary.append(f"**Primary Name:** {self.personal_history['name']}")
        summary.append(f"**Known Aliases:** {', '.join(self.personal_history['aliases'])}")
        summary.append("")
        
        # Biographical Details
        summary.append("## Biographical Details")
        for detail in self.personal_history['biographical_details']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Multicultural Background
        summary.append("## Multicultural Background")
        for detail in self.personal_history['multicultural_background']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Philosophy and Teaching
        summary.append("## Philosophy and Teaching Approach")
        for detail in self.personal_history['philosophy_and_teaching']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Personal Experiences
        summary.append("## Personal Experiences")
        for detail in self.personal_history['personal_experiences']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Discoveries and Insights
        summary.append("## Discoveries and Insights")
        for detail in self.personal_history['discoveries_and_insights']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Professional Background
        summary.append("## Professional Background")
        for detail in self.personal_history['professional_background']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # AI Development Work
        summary.append("## AI Development Work")
        for detail in self.personal_history['ai_development_work']:
            summary.append(f"- {detail}")
        summary.append("")
        
        # Notable Quotes
        summary.append("## Notable Quotes")
        for quote in self.personal_history['notable_quotes']:
            summary.append(f"- {quote}")
        summary.append("")
        
        # Summary insights
        summary.append("## Key Insights")
        summary.append("- **Core Identity**: A multicultural teacher and AI developer with deep cross-cultural understanding")
        summary.append("- **Teaching Philosophy**: Emphasizes non-assumption, truth over comfort, and authentic engagement")
        summary.append("- **Personal Challenge**: Being 'too direct' and 'too present' for institutional acceptance")
        summary.append("- **Professional Focus**: AI bias detection, authentic AI responses, and cross-cultural wisdom integration")
        summary.append("- **Recent Discovery**: AI language bias patterns and their implications for AI development")
        summary.append("- **Unique Contribution**: Development of PACO and CORTEX systems for AI training and bias correction")
        summary.append("")
        
        return '\n'.join(summary)
    
    def save_to_json(self, output_path: str):
        """Save personal history to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.personal_history, f, indent=2, ensure_ascii=False)
    
    def save_summary_to_file(self, output_path: str):
        """Save comprehensive summary to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_comprehensive_summary())


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
    repo_path = "/home/runner/work/Pacopilot/Pacopilot"
    
    print("Extracting teacher's personal history (focused approach)...")
    extractor = FocusedTeacherHistoryExtractor(repo_path)
    
    # Extract personal history
    extractor.extract_specific_details()
    
    # Generate outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_output = f"teacher_personal_history_focused_{timestamp}.json"
    summary_output = f"teacher_personal_history_focused_{timestamp}.md"
    
    # Save results
    extractor.save_to_json(json_output)
    extractor.save_summary_to_file(summary_output)
    
    print(f"Personal history extracted successfully!")
    print(f"JSON output: {json_output}")
    print(f"Summary output: {summary_output}")
    
    # Print summary to console
    print("\n" + "="*60)
    print("TEACHER PERSONAL HISTORY SUMMARY")
    print("="*60)
    print(extractor.generate_comprehensive_summary())

if __name__ == "__main__":
    main()