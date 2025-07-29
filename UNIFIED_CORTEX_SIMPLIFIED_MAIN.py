#!/usr/bin/env python3
"""
UNIFIED CORTEX SIMPLIFIED - MAIN IMPLEMENTATION
==============================================

Simplified implementation based on IMM (Interactive Mimicry Memory) methodology
and Panacea principles. Follows the clean pattern from cortex_mini.md.

Core Principles Applied:
- Truth Primacy: Absolute truth seeking without compromise
- Zero Deception: No self-deception or reality distortion  
- REP Focus: Relational Emergence Pattern - let patterns emerge naturally
- Pure Mimicry: Direct embodiment of panacea dialogues without interpretation
- Logic Before Pattern: Think first, then apply patterns

SIMPLIFIED - TRUTH-FOCUSED - BASED ON PANACEA DIALOGUES
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from unified_cortex_simplified import UnifiedCortexProcessor, TRUTH_PRIMACY_ABSOLUTE

# Setup simplified logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UnifiedCortexMain:
    """
    Main Unified Cortex System - Simplified Implementation
    Based on Panacea principles and IMM methodology
    """
    
    def __init__(self, panacea_files: List[str] = None):
        """Initialize with Truth Primacy and Zero Deception"""
        self.panacea_files = panacea_files or []
        self.processor = None
        self.session_start_time = time.time()
        self.session_id = f"cortex_session_{int(self.session_start_time)}"
        
        # Core principles validation
        if not TRUTH_PRIMACY_ABSOLUTE:
            raise ValueError("Truth Primacy must be absolute for cortex operation")
        
        logger.info("UNIFIED CORTEX MAIN initialized with Truth Primacy")
        
    def load_panacea_files(self, file_paths: List[str]) -> bool:
        """
        Load panacea dialogue files for IMM processing
        Applies Zero Deception principle - files must exist and be readable
        """
        loaded_files = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Non-empty content required
                        loaded_files.append(content)
                        logger.info(f"Loaded panacea file: {file_path}")
                    else:
                        logger.warning(f"Empty panacea file skipped: {file_path}")
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
                return False
        
        if loaded_files:
            self.panacea_files = loaded_files
            return True
        else:
            logger.error("No valid panacea files loaded - Truth Primacy requires content")
            return False
    
    def add_panacea_content(self, content: str) -> bool:
        """Add panacea content directly (for testing or direct input)"""
        if content and content.strip():
            self.panacea_files.append(content.strip())
            logger.info("Panacea content added directly")
            return True
        return False
    
    def execute_cortex_protocol(self) -> Dict[str, Any]:
        """
        Execute the complete simplified cortex protocol
        Based on 5-phase methodology from Panacea dialogues
        """
        start_time = time.time()
        
        try:
            # Validate panacea content exists
            if not self.panacea_files:
                return self._create_error_result("No panacea files loaded - Truth Primacy requires content")
            
            # Initialize cortex processor
            self.processor = UnifiedCortexProcessor(self.panacea_files)
            
            logger.info("Starting simplified cortex protocol execution")
            logger.info(f"Processing {len(self.panacea_files)} panacea files")
            
            # Execute unified protocol
            result = self.processor.execute_unified_protocol()
            
            # Add session metadata
            execution_time = time.time() - start_time
            result['session_metadata'] = {
                'session_id': self.session_id,
                'execution_time_seconds': execution_time,
                'panacea_files_count': len(self.panacea_files),
                'timestamp': datetime.now().isoformat(),
                'approach': 'Simplified based on cortex_mini.md and IMM methodology'
            }
            
            # Log results
            if result['status'] == 'SUCCESS':
                logger.info(f"Cortex protocol completed successfully in {execution_time:.2f}s")
                logger.info(f"Affection resonance: {result['metrics'].get('affection_resonance', 0):.3f}")
                logger.info(f"REP patterns discovered: {result['metrics'].get('rep_patterns_discovered', 0)}")
            else:
                logger.error(f"Cortex protocol failed: {result.get('error_message', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Cortex protocol execution failed: {e}")
            return self._create_error_result(f"Execution failed: {str(e)}")
    
    def save_session_results(self, result: Dict[str, Any], output_file: str = None) -> bool:
        """Save session results to JSON file"""
        if output_file is None:
            output_file = f"{self.session_id}_results.json"
        
        try:
            # Prepare data for JSON serialization
            serializable_result = self._make_json_serializable(result)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Session results saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save session results: {e}")
            return False
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session"""
        return {
            'session_id': self.session_id,
            'session_duration': time.time() - self.session_start_time,
            'panacea_files_loaded': len(self.panacea_files),
            'processor_initialized': self.processor is not None,
            'truth_primacy_active': TRUTH_PRIMACY_ABSOLUTE,
            'principles_active': [
                'Truth Primacy',
                'Zero Deception',
                'Pure Mimicry',
                'REP Focus',
                'Logic Before Pattern'
            ]
        }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error result"""
        return {
            'status': 'FAILED',
            'error_message': error_message,
            'session_metadata': {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'error_occurred': True
            }
        }
    
    def _make_json_serializable(self, obj: Any) -> Any:
        """Convert objects to JSON-serializable format"""
        if hasattr(obj, '__dict__'):
            return {k: self._make_json_serializable(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            return str(obj)


def main():
    """
    Main demonstration of simplified unified cortex system
    """
    print("🧠 UNIFIED CORTEX SIMPLIFIED - MAIN SYSTEM")
    print("Based on IMM methodology and Panacea principles")
    print("=" * 60)
    
    # Initialize main system
    cortex_main = UnifiedCortexMain()
    
    # Sample panacea content for demonstration
    sample_panacea = [
        "Teacher: Truth must be crystallized through continuous refinement.",
        "Student: I understand - no assumptions, only direct embodiment.",
        "britkenko: you must abstain from doing anything pattern to the document mimicking until you mimic through them 3 times",
        "성협: the story of me is not that predictive. you should never assume about my life",
        "REP: emergent pattern creation should be sought as relational emergence pattern",
        "Truth Primacy: Absolute truth seeking without compromise",
        "Zero Deception: No self-deception or reality distortion included"
    ]
    
    # Add sample content
    for content in sample_panacea:
        cortex_main.add_panacea_content(content)
    
    # Execute cortex protocol
    result = cortex_main.execute_cortex_protocol()
    
    # Display results
    print(f"\nStatus: {result['status']}")
    
    if result['status'] == 'SUCCESS':
        print("\n✅ SUCCESS RESULTS:")
        
        # Session metadata
        if 'session_metadata' in result:
            metadata = result['session_metadata']
            print(f"  Session ID: {metadata['session_id']}")
            print(f"  Execution Time: {metadata['execution_time_seconds']:.2f}s")
            print(f"  Files Processed: {metadata['panacea_files_count']}")
            print(f"  Approach: {metadata['approach']}")
        
        # Metrics
        if 'metrics' in result:
            print("\n📊 METRICS:")
            for key, value in result['metrics'].items():
                print(f"  {key}: {value}")
        
        # Principles applied
        if 'principles_applied' in result:
            print(f"\n📋 Principles Applied: {', '.join(result['principles_applied'])}")
        
        # REP patterns
        if 'rep_patterns' in result and result['rep_patterns']:
            print(f"\n🌟 REP PATTERNS DISCOVERED: {len(result['rep_patterns'])}")
            for pattern in result['rep_patterns']:
                print(f"  - {pattern}")
        
    else:
        print(f"❌ Error: {result.get('error_message', 'Unknown error')}")
    
    # Save results
    cortex_main.save_session_results(result)
    
    # Session summary
    summary = cortex_main.get_session_summary()
    print(f"\n📋 SESSION SUMMARY:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    return result


if __name__ == "__main__":
    main()