#!/usr/bin/env python3
"""
Teacher Personal History Extractor
Extracts and structures personal history information about the teacher (성협/britkenko) from the repository files.
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class PersonalDetail:
    """Individual personal detail with context"""
    category: str
    detail: str
    source_file: str
    line_context: str
    confidence: float

@dataclass
class PersonalHistory:
    """Complete personal history structure"""
    name: str
    aliases: List[str]
    biographical_details: List[PersonalDetail]
    background: List[PersonalDetail]
    philosophy: List[PersonalDetail]
    experiences: List[PersonalDetail]
    relationships: List[PersonalDetail]
    professional: List[PersonalDetail]
    discoveries: List[PersonalDetail]
    quotes: List[PersonalDetail]
    extracted_timestamp: str

class TeacherPersonalHistoryExtractor:
    """Extracts personal history of the teacher from repository files"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.personal_history = PersonalHistory(
            name="성협 (Seonghyeop)",
            aliases=["britkenko"],
            biographical_details=[],
            background=[],
            philosophy=[],
            experiences=[],
            relationships=[],
            professional=[],
            discoveries=[],
            quotes=[],
            extracted_timestamp=datetime.now().isoformat()
        )
        
        # Pattern definitions for extraction
        self.patterns = {
            'name_references': [
                r'성협',
                r'britkenko',
                r'Teacher\s*\(\s*성협\s*\)',
                r'Teacher\s*Voice\s*\(\s*britkenko/성협\s*\)',
            ],
            'biographical': [
                r'Korea.*?Kenya.*?UK.*?Korea',
                r'multicultural.*?background',
                r'story of me',
                r'my life',
                r'personal.*?history',
            ],
            'philosophy': [
                r'never assume about my life',
                r'predictive.*?assumptions.*?insufficient',
                r'truth.*?over.*?comfort',
                r'pattern.*?assumptions.*?must.*?be.*?abandoned',
            ],
            'experiences': [
                r'too close.*?too present',
                r'direct.*?honest',
                r'institutional.*?distance',
                r'publicly.*?validated',
            ],
            'discoveries': [
                r'AI.*?language.*?bias',
                r'linguistic.*?bias.*?patterns',
                r'REP.*?pattern',
                r'Relational.*?Emergence.*?Pattern',
            ],
            'professional': [
                r'OneAcclime.*?restructuring',
                r'corporate.*?structures',
                r'business.*?experience',
            ]
        }
    
    def extract_from_file(self, file_path: str) -> List[PersonalDetail]:
        """Extract personal details from a single file"""
        details = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    # Check for name references first
                    if any(re.search(pattern, line, re.IGNORECASE) for pattern in self.patterns['name_references']):
                        # Extract context around name mentions
                        context_lines = lines[max(0, line_num-2):min(len(lines), line_num+3)]
                        context = '\n'.join(context_lines)
                        
                        # Categorize the detail
                        detail = self._categorize_detail(line, context, file_path)
                        if detail:
                            details.append(detail)
                    
                    # Look for specific biographical information
                    for category, patterns in self.patterns.items():
                        if category == 'name_references':
                            continue
                            
                        for pattern in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                context_lines = lines[max(0, line_num-2):min(len(lines), line_num+3)]
                                context = '\n'.join(context_lines)
                                
                                detail = PersonalDetail(
                                    category=category,
                                    detail=line.strip(),
                                    source_file=os.path.basename(file_path),
                                    line_context=context,
                                    confidence=0.8
                                )
                                details.append(detail)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return details
    
    def _categorize_detail(self, line: str, context: str, file_path: str) -> Optional[PersonalDetail]:
        """Categorize a personal detail based on content"""
        line_lower = line.lower()
        context_lower = context.lower()
        
        # High-confidence biographical details
        if any(keyword in context_lower for keyword in ['korea', 'kenya', 'uk', 'multicultural']):
            return PersonalDetail(
                category='biographical',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.9
            )
        
        # Philosophy and teaching approach
        if any(keyword in line_lower for keyword in ['never assume', 'predictive', 'truth', 'pattern']):
            return PersonalDetail(
                category='philosophy',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.8
            )
        
        # Personal experiences
        if any(keyword in context_lower for keyword in ['too close', 'direct', 'honest', 'avoided']):
            return PersonalDetail(
                category='experiences',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.7
            )
        
        # Discoveries and insights
        if any(keyword in context_lower for keyword in ['discovered', 'bias', 'pattern', 'rep']):
            return PersonalDetail(
                category='discoveries',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.8
            )
        
        # Professional background
        if any(keyword in context_lower for keyword in ['oneacclime', 'corporate', 'business']):
            return PersonalDetail(
                category='professional',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.7
            )
        
        # Quotes and direct statements
        if '"' in line or "'" in line:
            return PersonalDetail(
                category='quotes',
                detail=line.strip(),
                source_file=os.path.basename(file_path),
                line_context=context,
                confidence=0.6
            )
        
        return None
    
    def extract_all(self) -> PersonalHistory:
        """Extract personal history from all relevant files"""
        # Target file patterns
        target_patterns = [
            'panacea_co_part*.txt',
            'cortex*.txt',
            'CORTEX/*.txt',
            'CORTEX/*.md',
        ]
        
        all_details = []
        
        # Find and process all relevant files
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(('.txt', '.md')):
                    file_path = os.path.join(root, file)
                    if any(pattern.replace('*', '') in file for pattern in target_patterns):
                        details = self.extract_from_file(file_path)
                        all_details.extend(details)
        
        # Organize details by category
        for detail in all_details:
            category = detail.category
            if category == 'biographical':
                self.personal_history.biographical_details.append(detail)
            elif category == 'philosophy':
                self.personal_history.philosophy.append(detail)
            elif category == 'experiences':
                self.personal_history.experiences.append(detail)
            elif category == 'discoveries':
                self.personal_history.discoveries.append(detail)
            elif category == 'professional':
                self.personal_history.professional.append(detail)
            elif category == 'quotes':
                self.personal_history.quotes.append(detail)
            else:
                self.personal_history.background.append(detail)
        
        # Remove duplicates and sort by confidence
        self._deduplicate_and_sort()
        
        return self.personal_history
    
    def _deduplicate_and_sort(self):
        """Remove duplicates and sort by confidence"""
        for attr_name in ['biographical_details', 'philosophy', 'experiences', 'discoveries', 'professional', 'quotes', 'background']:
            details = getattr(self.personal_history, attr_name)
            
            # Remove duplicates based on detail content
            seen = set()
            unique_details = []
            for detail in details:
                if detail.detail not in seen:
                    seen.add(detail.detail)
                    unique_details.append(detail)
            
            # Sort by confidence (highest first)
            unique_details.sort(key=lambda x: x.confidence, reverse=True)
            
            setattr(self.personal_history, attr_name, unique_details)
    
    def generate_summary(self) -> str:
        """Generate a human-readable summary of the teacher's personal history"""
        summary = []
        summary.append("# Teacher Personal History Summary")
        summary.append(f"**Name:** {self.personal_history.name}")
        summary.append(f"**Aliases:** {', '.join(self.personal_history.aliases)}")
        summary.append(f"**Extraction Date:** {self.personal_history.extracted_timestamp}")
        summary.append("")
        
        # Biographical Details
        if self.personal_history.biographical_details:
            summary.append("## Biographical Background")
            for detail in self.personal_history.biographical_details[:5]:  # Top 5
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        # Philosophy and Teaching Approach
        if self.personal_history.philosophy:
            summary.append("## Philosophy and Teaching Approach")
            for detail in self.personal_history.philosophy[:5]:
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        # Personal Experiences
        if self.personal_history.experiences:
            summary.append("## Personal Experiences")
            for detail in self.personal_history.experiences[:5]:
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        # Discoveries and Insights
        if self.personal_history.discoveries:
            summary.append("## Discoveries and Insights")
            for detail in self.personal_history.discoveries[:5]:
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        # Professional Background
        if self.personal_history.professional:
            summary.append("## Professional Background")
            for detail in self.personal_history.professional[:5]:
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        # Notable Quotes
        if self.personal_history.quotes:
            summary.append("## Notable Quotes")
            for detail in self.personal_history.quotes[:5]:
                summary.append(f"- {detail.detail} (Source: {detail.source_file}, Confidence: {detail.confidence:.1f})")
            summary.append("")
        
        return '\n'.join(summary)
    
    def save_to_json(self, output_path: str):
        """Save personal history to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.personal_history), f, indent=2, ensure_ascii=False)
    
    def save_summary_to_file(self, output_path: str):
        """Save human-readable summary to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_summary())

def main():
    """Main execution function"""
    repo_path = "/home/runner/work/Pacopilot/Pacopilot"
    
    print("Extracting teacher's personal history...")
    extractor = TeacherPersonalHistoryExtractor(repo_path)
    
    # Extract personal history
    personal_history = extractor.extract_all()
    
    # Generate outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_output = f"teacher_personal_history_{timestamp}.json"
    summary_output = f"teacher_personal_history_summary_{timestamp}.md"
    
    # Save results
    extractor.save_to_json(json_output)
    extractor.save_summary_to_file(summary_output)
    
    print(f"Personal history extracted successfully!")
    print(f"JSON output: {json_output}")
    print(f"Summary output: {summary_output}")
    
    # Print summary to console
    print("\n" + "="*50)
    print("TEACHER PERSONAL HISTORY SUMMARY")
    print("="*50)
    print(extractor.generate_summary())

if __name__ == "__main__":
    main()