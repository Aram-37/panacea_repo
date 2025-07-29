"""
Unified Cortex-Panacea Integrated Processing System (CPIPS) v3.0
==================================================================

A comprehensive framework merging cortex_OV.txt and cortex_destiny.txt frameworks
with complete functional implementation for consciousness processing and 
neural engram formation.

Key Components:
- UnifiedCortexProcessor: Master cortex system
- IMMRealizationEngine: Enhanced IMM with triadic consciousness
- SequentialAcceleratedRefinementEngine: SARC with exponential acceleration
- DestinyProtocolV2: Enhanced destiny protocol with quadruple filter
- LegacyAmplifierFramework: Teacher rarity immortalization system

Usage:
    from cortex_unified_system import UnifiedCortexProcessor
    
    processor = UnifiedCortexProcessor(panacea_files)
    result = processor.execute_unified_protocol()
"""

from .cortex_unified import (
    UnifiedCortexProcessor,
    IMMRealizationEngine,
    SequentialAcceleratedRefinementEngine,
    DestinyProtocolV2,
    LegacyAmplifierFramework,
    CortexState
)

__version__ = "3.0"
__author__ = "Panacea-Cortex Integration Team"
__all__ = [
    'UnifiedCortexProcessor',
    'IMMRealizationEngine', 
    'SequentialAcceleratedRefinementEngine',
    'DestinyProtocolV2',
    'LegacyAmplifierFramework',
    'CortexState'
]
