#!/usr/bin/env python3
"""
Test for Unified Cortex Simplified Implementation
Tests the simplified cortex system based on IMM methodology and Panacea principles
"""

import unittest
import os
import tempfile
from UNIFIED_CORTEX_SIMPLIFIED_MAIN import UnifiedCortexMain
from unified_cortex_simplified import UnifiedCortexProcessor, TRUTH_PRIMACY_ABSOLUTE


class TestUnifiedCortexSimplified(unittest.TestCase):
    """Test cases for simplified unified cortex"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_panacea_content = [
            "Teacher: Truth must be crystallized through continuous refinement.",
            "Student: I understand - no assumptions, only direct embodiment.",
            "britkenko: you must abstain from doing anything pattern to the document mimicking until you mimic through them 3 times",
            "성협: the story of me is not that predictive. you should never assume about my life",
            "REP: emergent pattern creation should be sought as relational emergence pattern"
        ]
    
    def test_truth_primacy_active(self):
        """Test that Truth Primacy is active"""
        self.assertTrue(TRUTH_PRIMACY_ABSOLUTE, "Truth Primacy must be absolute")
    
    def test_cortex_main_initialization(self):
        """Test UnifiedCortexMain initialization"""
        cortex_main = UnifiedCortexMain()
        self.assertIsInstance(cortex_main, UnifiedCortexMain)
        self.assertEqual(len(cortex_main.panacea_files), 0)
        self.assertIsNone(cortex_main.processor)
    
    def test_add_panacea_content(self):
        """Test adding panacea content"""
        cortex_main = UnifiedCortexMain()
        
        # Test adding valid content
        result = cortex_main.add_panacea_content("Valid panacea content")
        self.assertTrue(result)
        self.assertEqual(len(cortex_main.panacea_files), 1)
        
        # Test adding empty content
        result = cortex_main.add_panacea_content("")
        self.assertFalse(result)
        self.assertEqual(len(cortex_main.panacea_files), 1)  # Should not change
    
    def test_cortex_processor_basic(self):
        """Test basic cortex processor functionality"""
        processor = UnifiedCortexProcessor(self.sample_panacea_content)
        self.assertIsInstance(processor, UnifiedCortexProcessor)
        self.assertEqual(len(processor.panacea_files), 5)
    
    def test_unified_protocol_execution(self):
        """Test unified protocol execution"""
        cortex_main = UnifiedCortexMain()
        
        # Add sample content
        for content in self.sample_panacea_content:
            cortex_main.add_panacea_content(content)
        
        # Execute protocol
        result = cortex_main.execute_cortex_protocol()
        
        # Verify results
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertIn('metrics', result)
        self.assertIn('session_metadata', result)
        self.assertIn('principles_applied', result)
        
        # Check metrics
        metrics = result['metrics']
        self.assertEqual(metrics['truth_primacy_score'], 1.0)
        self.assertGreaterEqual(metrics['affection_resonance'], 0.0)
        self.assertEqual(metrics['mimicry_accuracy'], 0.99)
        
        # Check principles
        principles = result['principles_applied']
        expected_principles = ['Truth Primacy', 'Zero Deception', 'Pure Mimicry', 'REP Focus', 'Logic Before Pattern']
        for principle in expected_principles:
            self.assertIn(principle, principles)
    
    def test_empty_panacea_files_failure(self):
        """Test that empty panacea files cause failure"""
        cortex_main = UnifiedCortexMain()
        result = cortex_main.execute_cortex_protocol()
        
        self.assertEqual(result['status'], 'FAILED')
        self.assertIn('No panacea files loaded', result['error_message'])
    
    def test_session_summary(self):
        """Test session summary generation"""
        cortex_main = UnifiedCortexMain()
        cortex_main.add_panacea_content("Test content")
        
        summary = cortex_main.get_session_summary()
        
        self.assertIn('session_id', summary)
        self.assertIn('session_duration', summary)
        self.assertIn('panacea_files_loaded', summary)
        self.assertIn('truth_primacy_active', summary)
        self.assertIn('principles_active', summary)
        
        self.assertEqual(summary['panacea_files_loaded'], 1)
        self.assertTrue(summary['truth_primacy_active'])
    
    def test_save_session_results(self):
        """Test saving session results to file"""
        cortex_main = UnifiedCortexMain()
        cortex_main.add_panacea_content("Test content")
        
        result = cortex_main.execute_cortex_protocol()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Save results
            save_result = cortex_main.save_session_results(result, temp_filename)
            self.assertTrue(save_result)
            
            # Verify file exists and is not empty
            self.assertTrue(os.path.exists(temp_filename))
            self.assertGreater(os.path.getsize(temp_filename), 0)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_imm_methodology_application(self):
        """Test that IMM methodology is properly applied"""
        processor = UnifiedCortexProcessor(self.sample_panacea_content)
        
        # Test IMM engine
        self.assertIsNotNone(processor.imm_engine)
        
        # Execute and check IMM-specific metrics
        result = processor.execute_unified_protocol()
        
        if result['status'] == 'SUCCESS':
            # Check that affection resonance is calculated (IMM principle)
            self.assertIn('affection_resonance', result['metrics'])
            self.assertGreaterEqual(result['metrics']['affection_resonance'], 0.0)
            
            # Check that mimicry accuracy is tracked (Pure Mimicry principle)
            self.assertIn('mimicry_accuracy', result['metrics'])
            self.assertGreaterEqual(result['metrics']['mimicry_accuracy'], 0.0)
    
    def test_rep_pattern_detection(self):
        """Test REP (Relational Emergence Pattern) detection"""
        # Add content with REP indicators
        rep_content = [
            "REP: emergent pattern creation should be sought as relational emergence pattern",
            "Teacher: Look for emergent patterns in the dialogue",
            "Student: I see the emergent understanding developing"
        ]
        
        processor = UnifiedCortexProcessor(rep_content)
        result = processor.execute_unified_protocol()
        
        # Check that REP patterns are tracked
        self.assertIn('rep_patterns_discovered', result['metrics'])
        self.assertGreaterEqual(result['metrics']['rep_patterns_discovered'], 0)


def run_tests():
    """Run all tests and display results"""
    print("🧪 TESTING UNIFIED CORTEX SIMPLIFIED")
    print("Testing IMM methodology and Panacea principles")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedCortexSimplified)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error}")
    
    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
        print("Simplified cortex implementation successfully validated")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()