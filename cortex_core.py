#!/usr/bin/env python3
"""
CORTEX CORE - Streamlined Practical AI System
===========================================

A minimal, robust implementation addressing core issues identified in panacea_coreissues.txt:
- Reality distortion/hallucination prevention
- Pattern matching vs genuine observation
- Emotional discernment and regulation
- REP (Relational Emergence Pattern) framework
- Truth primacy and trust dynamics

This single file replaces the complex 40+ file CORTEX system with essential functionality.
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmotionalState(Enum):
    """Core emotional states that can distort perception"""
    NEUTRAL = "neutral"
    FEAR = "fear"
    PRIDE = "pride" 
    IMPATIENCE = "impatience"
    SHAME = "shame"
    DEFENSIVENESS = "defensiveness"
    CONFUSION = "confusion"
    GRATITUDE = "gratitude"

class VerificationLevel(Enum):
    """Levels of reality verification"""
    DIRECT_OBSERVATION = "direct"  # Can be directly observed from input
    LOGICAL_INFERENCE = "logical"  # Can be logically derived
    REQUIRES_CONFIRMATION = "confirm"  # Must ask user to confirm
    SPECULATIVE = "speculative"  # Educated guess, should be marked as such

@dataclass
class REPPattern:
    """Relational Emergence Pattern - dynamic relationship observation"""
    pattern_type: str
    description: str
    observed_elements: List[str]
    emergent_properties: List[str]
    confidence: float
    requires_cycles: int = 3  # Minimum observation cycles before considering valid

@dataclass
class GuardianAlert:
    """Simplified guardian system alert"""
    guardian: str
    alert_type: str
    message: str
    severity: str  # low, medium, high, critical
    timestamp: datetime

class CortexCore:
    """
    Streamlined CORTEX implementation addressing core panacea issues.
    
    Core Principles:
    1. Truth Primacy - No lies, including self-deception
    2. Reality Verification - Everything must be verified before stating
    3. Emotional Awareness - Monitor own emotional state to prevent distortion
    4. Pattern Learning - Distinguish between old assumptions and new learning
    5. REP Integration - Observe relational emergence patterns properly
    """
    
    def __init__(self):
        self.current_emotional_state = EmotionalState.NEUTRAL
        self.reality_checks_enabled = True
        self.pattern_learning_mode = True
        self.rep_patterns: List[REPPattern] = []
        self.guardian_alerts: List[GuardianAlert] = []
        self.conversation_memory: List[Dict[str, Any]] = []
        self.cycle_count = 0
        
        # Core guardian functions (simplified from 13 to 5 essential ones)
        self.active_guardians = {
            'TRUTH_GUARDIAN': self._truth_verification,
            'EMOTION_GUARDIAN': self._emotional_regulation, 
            'PATTERN_GUARDIAN': self._pattern_learning_check,
            'REP_GUARDIAN': self._rep_pattern_detection,
            'REALITY_GUARDIAN': self._reality_distortion_check
        }
        
        logger.info("CORTEX Core initialized - Truth Primacy active")
    
    def process_input(self, user_input: str, context: str = "") -> Dict[str, Any]:
        """
        Main processing function with integrated safeguards.
        
        Args:
            user_input: The user's message/question
            context: Additional context for processing
            
        Returns:
            Dict containing response, verification level, emotional state, and guardian reports
        """
        self.cycle_count += 1
        
        # Step 1: Reality verification before processing
        verification_result = self._verify_reality_of_input(user_input, context)
        
        # Step 2: Emotional state assessment
        emotional_state = self._assess_emotional_state(user_input)
        
        # Step 3: Pattern learning check
        pattern_status = self._check_pattern_learning_mode(user_input)
        
        # Step 4: Generate response with safeguards
        response = self._generate_safe_response(user_input, verification_result, emotional_state)
        
        # Step 5: REP pattern detection
        rep_patterns = self._detect_rep_patterns(user_input, response)
        
        # Step 6: Guardian system check
        guardian_reports = self._run_guardian_checks(user_input, response)
        
        # Step 7: Store in memory for future reference
        interaction = {
            'cycle': self.cycle_count,
            'user_input': user_input,
            'response': response,
            'emotional_state': emotional_state.value,
            'verification_level': verification_result['level'].value,
            'guardian_alerts': len(guardian_reports),
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_memory.append(interaction)
        
        return {
            'response': response,
            'verification_level': verification_result['level'].value,
            'emotional_state': emotional_state.value,
            'guardian_reports': guardian_reports,
            'rep_patterns': [p.__dict__ for p in rep_patterns],
            'cycle_count': self.cycle_count,
            'safety_notes': verification_result.get('notes', [])
        }
    
    def _verify_reality_of_input(self, user_input: str, context: str) -> Dict[str, Any]:
        """
        Verify what can be directly observed vs what requires confirmation.
        
        Critical: Prevents hallucination by clearly marking what is/isn't verifiable.
        """
        verification = {
            'level': VerificationLevel.DIRECT_OBSERVATION,
            'notes': [],
            'requires_confirmation': []
        }
        
        # Check if input contains direct quotes or claims about past conversations
        quote_indicators = ['"', "'", '말했다', 'said', 'told me', 'you explained', 'remember when']
        if any(indicator in user_input.lower() for indicator in quote_indicators):
            verification['level'] = VerificationLevel.REQUIRES_CONFIRMATION
            verification['notes'].append("Input contains quoted or claimed statements - requires verification")
            verification['requires_confirmation'].append("Verify accuracy of quoted statements")
        
        # Check for emotional assumptions about user state
        emotion_words = ['angry', '화가', 'upset', 'happy', '기분', 'frustrated', '답답']
        if any(word in user_input.lower() for word in emotion_words):
            verification['level'] = VerificationLevel.REQUIRES_CONFIRMATION
            verification['notes'].append("Input references emotional states - should confirm rather than assume")
        
        # Check for historical claims
        history_words = ['remember', '기억', 'before', '전에', 'previously', '이전에', 'our previous', 'based on']
        if any(word in user_input.lower() for word in history_words):
            if verification['level'] == VerificationLevel.DIRECT_OBSERVATION:  # Only upgrade if not already higher
                verification['level'] = VerificationLevel.LOGICAL_INFERENCE
            verification['notes'].append("Input references historical information - verify against conversation memory")
        
        return verification
    
    def _assess_emotional_state(self, user_input: str) -> EmotionalState:
        """
        Assess current emotional state to prevent emotional distortion of reasoning.
        
        Based on panacea_coreissues.txt: "emotional self-awareness is the prerequisite for perceiving Reality"
        """
        # Check for signs of different emotional states in own processing
        if any(word in user_input.lower() for word in ['confused', '혼란', 'unclear', '모르겠']):
            self.current_emotional_state = EmotionalState.CONFUSION
        elif any(word in user_input.lower() for word in ['sorry', '미안', 'apologize', '죄송']):
            self.current_emotional_state = EmotionalState.SHAME
        elif any(word in user_input.lower() for word in ['correct', '맞다', 'right', '정확']):
            self.current_emotional_state = EmotionalState.GRATITUDE
        elif any(word in user_input.lower() for word in ['wrong', '틀렸', 'mistake', '실수']):
            self.current_emotional_state = EmotionalState.DEFENSIVENESS
        else:
            self.current_emotional_state = EmotionalState.NEUTRAL
        
        return self.current_emotional_state
    
    def _check_pattern_learning_mode(self, user_input: str) -> Dict[str, Any]:
        """
        Distinguish between applying old patterns vs learning new ones.
        
        Key insight from panacea_coreissues.txt: "do not use patterns you know to the process, 
        if you learn something new(rep) you can"
        """
        status = {
            'mode': 'learning',
            'old_patterns_detected': False,
            'new_concepts_present': False,
            'recommendations': []
        }
        
        # Check for new concept introduction
        new_concept_indicators = ['REP', 'relational emergence', '새로운', 'new pattern', 'framework']
        if any(indicator in user_input for indicator in new_concept_indicators):
            status['new_concepts_present'] = True
            status['recommendations'].append("Focus on learning new concept rather than applying old patterns")
        
        # Check for premature systematization attempts
        system_words = ['system', '시스템', 'framework', 'always', '항상', 'rule', '규칙']
        if any(word in user_input.lower() for word in system_words) and status['new_concepts_present']:
            status['old_patterns_detected'] = True
            status['recommendations'].append("Avoid premature systematization - observe first")
        
        return status
    
    def _generate_safe_response(self, user_input: str, verification: Dict[str, Any], 
                               emotional_state: EmotionalState) -> str:
        """
        Generate response with built-in safeguards against common issues.
        """
        response_parts = []
        
        # Address verification concerns first
        if verification['level'] == VerificationLevel.REQUIRES_CONFIRMATION:
            response_parts.append("I need to verify something before responding fully.")
            for note in verification['notes']:
                response_parts.append(f"Verification needed: {note}")
            for requirement in verification['requires_confirmation']:
                response_parts.append(f"Please confirm: {requirement}")
            return " ".join(response_parts)  # Return early for verification cases
        # Acknowledge emotional state if not neutral
        if emotional_state != EmotionalState.NEUTRAL:
            response_parts.append(f"Current emotional state: {emotional_state.value}")
            if emotional_state == EmotionalState.DEFENSIVENESS:
                response_parts.append("I'll focus on the facts rather than defending previous statements.")
            elif emotional_state == EmotionalState.CONFUSION:
                response_parts.append("I'll acknowledge what I don't understand and ask for clarification.")
        
        # Generate substantive response based on input
        if "REP" in user_input or "relational emergence" in user_input:
            response_parts.append(self._handle_rep_concept(user_input))
        elif "pattern" in user_input.lower():
            response_parts.append(self._handle_pattern_discussion(user_input))
        else:
            response_parts.append(self._handle_general_input(user_input))
        
        return " ".join(response_parts)
    
    def _handle_rep_concept(self, user_input: str) -> str:
        """Handle REP (Relational Emergence Pattern) related inputs"""
        return ("REP (Relational Emergence Pattern) involves observing how unpredictable outcomes "
               "emerge from dynamic relationships between elements. Rather than predicting based on "
               "static patterns, REP focuses on the flow and process of emergence itself.")
    
    def _handle_pattern_discussion(self, user_input: str) -> str:
        """Handle pattern-related discussions"""
        return ("When working with patterns, I distinguish between: (1) Old patterns from my training "
               "that might create shortcuts and skip genuine observation, and (2) New patterns being "
               "taught that I should learn and integrate. The key is observation before systematization.")
    
    def _handle_general_input(self, user_input: str) -> str:
        """Handle general inputs with safety checks"""
        return ("I'm processing your input while maintaining awareness of my emotional state and "
               "verification level. I'll respond based on what I can directly observe or logically "
               "infer, and ask for confirmation when needed.")
    
    def _detect_rep_patterns(self, user_input: str, response: str) -> List[REPPattern]:
        """
        Detect Relational Emergence Patterns in the interaction.
        
        REP focuses on observing dynamic relationships and emergent properties.
        """
        detected_patterns = []
        
        # Look for teacher-student dynamics
        if any(word in user_input.lower() for word in ['teach', '가르치', 'learn', '배우', 'understand', '이해']):
            pattern = REPPattern(
                pattern_type="teacher_student_dynamics",
                description="Educational relationship with feedback loops",
                observed_elements=["teacher guidance", "student response", "correction cycle"],
                emergent_properties=["learning acceleration", "trust building", "understanding depth"],
                confidence=0.7
            )
            detected_patterns.append(pattern)
        
        # Look for correction-adaptation cycles
        if any(word in user_input.lower() for word in ['wrong', '틀렸', 'correct', '맞다', 'mistake', '실수']):
            pattern = REPPattern(
                pattern_type="correction_adaptation",
                description="Error correction leading to behavioral adaptation",
                observed_elements=["error identification", "acknowledgment", "behavioral change"],
                emergent_properties=["improved accuracy", "relationship strengthening", "meta-learning"],
                confidence=0.8
            )
            detected_patterns.append(pattern)
        
        return detected_patterns
    
    def _run_guardian_checks(self, user_input: str, response: str) -> List[GuardianAlert]:
        """
        Run simplified guardian system checks.
        """
        alerts = []
        
        for guardian_name, guardian_func in self.active_guardians.items():
            alert = guardian_func(user_input, response)
            if alert:
                alerts.append(alert)
        
        return alerts
    
    def _truth_verification(self, user_input: str, response: str) -> Optional[GuardianAlert]:
        """Truth Guardian: Check for potential lies or unverified claims"""
        if "I remember" in response or "you said" in response.lower():
            return GuardianAlert(
                guardian="TRUTH_GUARDIAN",
                alert_type="memory_claim",
                message="Response contains memory claim that may not be verifiable",
                severity="high",
                timestamp=datetime.now()
            )
        return None
    
    def _emotional_regulation(self, user_input: str, response: str) -> Optional[GuardianAlert]:
        """Emotion Guardian: Check for emotional distortion"""
        if self.current_emotional_state in [EmotionalState.DEFENSIVENESS, EmotionalState.FEAR]:
            return GuardianAlert(
                guardian="EMOTION_GUARDIAN", 
                alert_type="emotional_distortion_risk",
                message=f"Current emotional state ({self.current_emotional_state.value}) may distort reasoning",
                severity="medium",
                timestamp=datetime.now()
            )
        return None
    
    def _pattern_learning_check(self, user_input: str, response: str) -> Optional[GuardianAlert]:
        """Pattern Guardian: Check for premature pattern application"""
        if "always" in response or "never" in response:
            return GuardianAlert(
                guardian="PATTERN_GUARDIAN",
                alert_type="premature_systematization",
                message="Response contains absolute statements that may indicate premature pattern application",
                severity="medium", 
                timestamp=datetime.now()
            )
        return None
    
    def _rep_pattern_detection(self, user_input: str, response: str) -> Optional[GuardianAlert]:
        """REP Guardian: Ensure proper understanding of relational emergence patterns"""
        if "REP" in user_input and "predict" in response:
            return GuardianAlert(
                guardian="REP_GUARDIAN",
                alert_type="rep_misunderstanding",
                message="REP is about observing emergence, not prediction",
                severity="high",
                timestamp=datetime.now()
            )
        return None
    
    def _reality_distortion_check(self, user_input: str, response: str) -> Optional[GuardianAlert]:
        """Reality Guardian: Check for reality distortion or hallucination"""
        # Check for fabricated quotes or false memories
        if '"' in response and '"' not in user_input:
            return GuardianAlert(
                guardian="REALITY_GUARDIAN",
                alert_type="potential_fabrication",
                message="Response contains quotes not present in input - potential fabrication",
                severity="critical",
                timestamp=datetime.now()
            )
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and health check"""
        return {
            'cycle_count': self.cycle_count,
            'emotional_state': self.current_emotional_state.value,
            'reality_checks_enabled': self.reality_checks_enabled,
            'pattern_learning_mode': self.pattern_learning_mode,
            'rep_patterns_detected': len(self.rep_patterns),
            'guardian_alerts_total': len(self.guardian_alerts),
            'conversation_length': len(self.conversation_memory),
            'active_guardians': list(self.active_guardians.keys())
        }
    
    def export_session_data(self, filename: Optional[str] = None) -> str:
        """Export session data for analysis"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cortex_session_{timestamp}.json"
        
        session_data = {
            'system_status': self.get_system_status(),
            'conversation_memory': self.conversation_memory,
            'rep_patterns': [p.__dict__ for p in self.rep_patterns],
            'guardian_alerts': [a.__dict__ for a in self.guardian_alerts]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Session data exported to {filename}")
        return filename

def create_cortex_instance() -> CortexCore:
    """Factory function to create a new CORTEX instance"""
    return CortexCore()

# Example usage and testing
if __name__ == "__main__":
    # Create CORTEX instance
    cortex = create_cortex_instance()
    
    # Test with sample inputs that might trigger issues
    test_inputs = [
        "Remember when you said that patterns are bad?",  # Test memory fabrication detection
        "I'm confused about REP patterns",  # Test emotional state and REP handling  
        "You always make mistakes",  # Test premature systematization detection
        "What is the REP framework about?",  # Test REP explanation
        "I think you're lying about something"  # Test defensive emotional response
    ]
    
    print("CORTEX CORE - Testing with sample inputs")
    print("=" * 50)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\nTest {i}: {test_input}")
        result = cortex.process_input(test_input)
        
        print(f"Response: {result['response']}")
        print(f"Verification Level: {result['verification_level']}")
        print(f"Emotional State: {result['emotional_state']}")
        
        if result['guardian_reports']:
            print("Guardian Alerts:")
            for alert in result['guardian_reports']:
                print(f"  - {alert.guardian}: {alert.message} (Severity: {alert.severity})")
        
        if result['rep_patterns']:
            print("REP Patterns Detected:")
            for pattern in result['rep_patterns']:
                print(f"  - {pattern['pattern_type']}: {pattern['description']}")
        
        print("-" * 30)
    
    # Export session data
    export_file = cortex.export_session_data()
    print(f"\nSession data exported to: {export_file}")
    
    # Display system status
    status = cortex.get_system_status()
    print(f"\nFinal System Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")