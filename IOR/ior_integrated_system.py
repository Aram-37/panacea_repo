#!/usr/bin/env python3
"""
Integrated IoR System - Multi-Modal Divination Engine
===================================================

IoR (Impression of Reality) 통합 시스템 - 다중 모달 점술 엔진

계층적 인과관계 구조:
Voodoo/Psychology → Saju (Four Pillars) → Climate Science → Western Astrology → I Ching

통합 점술 시스템:
- 서양 점성술 (Western Astrology)
- 중국 주역 (I-Ching)
- 한국 사주 (Four Pillars)
- 베다 점성술 (Vedic Astrology)
- 룬 점술 (Runic Divination)
- 부두교/심리학적 요소 (Voodoo/Psychology)
- 기후과학 (Climate Science)

유명인 결혼 데이터를 통한 경험적 검증
교차 시스템 상관관계 분석
통계적 패턴 인식

"""

import json
import math
import datetime
import random
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

from btu_data_collector import BTUDataCollector, CelebrityProfile, MarriageEvent
from btu_astro_engine import BTUAstroEngine, PlanetPosition

# I-Ching Hexagrams and Trigrams
class IChing:
    """I-Ching (주역) calculation system"""
    
    TRIGRAMS = {
        '111': ('☰', '乾', 'Heaven', 'Creative'),
        '011': ('☱', '兌', 'Lake', 'Joyous'),
        '101': ('☲', '離', 'Fire', 'Clinging'),
        '001': ('☳', '震', 'Thunder', 'Arousing'),
        '110': ('☴', '巽', 'Wind', 'Gentle'),
        '010': ('☵', '坎', 'Water', 'Abysmal'),
        '100': ('☶', '艮', 'Mountain', 'Keeping Still'),
        '000': ('☷', '坤', 'Earth', 'Receptive')
    }
    
    HEXAGRAM_NAMES = [
        "乾 The Creative", "坤 The Receptive", "屯 Difficulty at the Beginning", 
        "蒙 Youthful Folly", "需 Waiting", "訟 Conflict", "師 The Army", 
        "比 Holding Together", "小畜 Small Taming", "履 Treading", 
        # ... (64 hexagrams total, abbreviated for space)
    ]
    
    @classmethod
    def calculate_hexagram(cls, birth_date: str, query_date: str) -> Dict[str, Any]:
        """Calculate I-Ching hexagram for marriage timing"""
        # Use birth date and query date to generate hexagram
        birth_sum = sum(ord(c) for c in birth_date.replace('-', ''))
        query_sum = sum(ord(c) for c in query_date.replace('-', ''))
        
        # Generate hexagram lines (6 lines)
        seed = birth_sum + query_sum
        random.seed(seed)
        
        lines = []
        for i in range(6):
            # Each line can be yin (0), yang (1), changing yin (2), changing yang (3)
            line_value = random.randint(0, 3)
            lines.append(line_value)
        
        # Create primary and secondary hexagrams
        primary_binary = ''.join(['1' if line % 2 == 1 else '0' for line in lines])
        secondary_binary = ''.join(['0' if line > 1 else ('1' if line == 1 else '0') for line in lines])
        
        primary_num = int(primary_binary, 2) % 64
        secondary_num = int(secondary_binary, 2) % 64 if secondary_binary != primary_binary else None
        
        return {
            'primary_hexagram': {
                'number': primary_num + 1,
                'name': cls.HEXAGRAM_NAMES[primary_num] if primary_num < len(cls.HEXAGRAM_NAMES) else f"Hexagram {primary_num + 1}",
                'binary': primary_binary,
                'lines': lines
            },
            'secondary_hexagram': {
                'number': secondary_num + 1 if secondary_num else None,
                'name': cls.HEXAGRAM_NAMES[secondary_num] if secondary_num and secondary_num < len(cls.HEXAGRAM_NAMES) else None,
                'binary': secondary_binary if secondary_binary != primary_binary else None
            } if secondary_num else None,
            'marriage_indication': cls._interpret_marriage_potential(lines, primary_num)
        }
    
    @classmethod
    def _interpret_marriage_potential(cls, lines: List[int], hexagram_num: int) -> Dict[str, Any]:
        """Interpret marriage potential from hexagram"""
        # Marriage-favorable hexagrams (simplified interpretation)
        marriage_hexagrams = [1, 2, 8, 11, 19, 31, 32, 37, 54]  # Selected favorable numbers
        
        base_score = 0.7 if (hexagram_num + 1) in marriage_hexagrams else 0.4
        
        # Line analysis for marriage timing
        changing_lines = sum(1 for line in lines if line > 1)
        change_factor = min(changing_lines * 0.1, 0.3)
        
        # Specific line patterns for relationships
        relationship_lines = lines[1:3]  # Lines 2-3 often relate to relationships
        harmony_score = 0.1 if relationship_lines[0] == relationship_lines[1] else 0.0
        
        total_score = min(base_score + change_factor + harmony_score, 1.0)
        
        return {
            'marriage_probability': total_score,
            'timing_indication': 'favorable' if total_score > 0.6 else 'challenging' if total_score < 0.4 else 'neutral',
            'changing_lines': changing_lines,
            'harmony_indicator': harmony_score > 0
        }

# Korean Four Pillars (사주) System
class SajuSystem:
    """Korean Four Pillars (사주) calculation system"""
    
    HEAVENLY_STEMS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    EARTHLY_BRANCHES = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    ELEMENTS = {
        '갑': '목', '을': '목', '병': '화', '정': '화', '무': '토',
        '기': '토', '경': '금', '신': '금', '임': '수', '계': '수'
    }
    
    ZODIAC_ANIMALS = ['쥐', '소', '범', '토끼', '용', '뱀', '말', '양', '원숭이', '닭', '개', '돼지']
    
    @classmethod
    def calculate_four_pillars(cls, birth_date: str, birth_time: str) -> Dict[str, Any]:
        """Calculate Four Pillars (사주) from birth data"""
        date_obj = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
        
        # Calculate year pillar
        year_index = (date_obj.year - 4) % 60
        year_stem = cls.HEAVENLY_STEMS[year_index % 10]
        year_branch = cls.EARTHLY_BRANCHES[year_index % 12]
        
        # Calculate month pillar (simplified)
        month_index = (date_obj.month - 1 + year_index * 2) % 60
        month_stem = cls.HEAVENLY_STEMS[month_index % 10]
        month_branch = cls.EARTHLY_BRANCHES[month_index % 12]
        
        # Calculate day pillar
        days_since_epoch = (date_obj - datetime.datetime(1900, 1, 1)).days
        day_index = days_since_epoch % 60
        day_stem = cls.HEAVENLY_STEMS[day_index % 10]
        day_branch = cls.EARTHLY_BRANCHES[day_index % 12]
        
        # Calculate hour pillar
        hour = int(birth_time.split(':')[0]) if ':' in birth_time else 12
        hour_index = ((hour + 1) // 2 + day_index) % 60
        hour_stem = cls.HEAVENLY_STEMS[hour_index % 10]
        hour_branch = cls.EARTHLY_BRANCHES[hour_index % 12]
        
        four_pillars = {
            'year': (year_stem, year_branch),
            'month': (month_stem, month_branch),
            'day': (day_stem, day_branch),
            'hour': (hour_stem, hour_branch)
        }
        
        return {
            'four_pillars': four_pillars,
            'elements': cls._analyze_elements(four_pillars),
            'marriage_analysis': cls._analyze_marriage_compatibility(four_pillars),
            'zodiac_year': cls.ZODIAC_ANIMALS[year_index % 12]
        }
    
    @classmethod
    def _analyze_elements(cls, pillars: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
        """Analyze five elements distribution"""
        element_count = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
        
        for pillar_name, (stem, branch) in pillars.items():
            element_count[cls.ELEMENTS[stem]] += 1
            # Branches also have elements (simplified mapping)
            branch_element = cls.ELEMENTS[cls.HEAVENLY_STEMS[hash(branch) % 10]]
            element_count[branch_element] += 1
        
        return element_count
    
    @classmethod
    def _analyze_marriage_compatibility(cls, pillars: Dict[str, Tuple[str, str]]) -> Dict[str, Any]:
        """Analyze marriage potential from Four Pillars"""
        day_stem, day_branch = pillars['day']
        spouse_palace = pillars['day'][1]  # Day branch represents spouse palace
        
        # Marriage timing indicators
        year_stem, year_branch = pillars['year']
        
        # Element harmony analysis
        day_element = cls.ELEMENTS[day_stem]
        spouse_element = cls.ELEMENTS[cls.HEAVENLY_STEMS[hash(spouse_palace) % 10]]
        
        # Five elements generation/destruction cycle
        generation_cycle = {'목': '화', '화': '토', '토': '금', '금': '수', '수': '목'}
        destruction_cycle = {'목': '토', '토': '수', '수': '화', '화': '금', '금': '목'}
        
        relationship_quality = 0.5  # Neutral base
        if generation_cycle[day_element] == spouse_element or generation_cycle[spouse_element] == day_element:
            relationship_quality = 0.8  # Generating relationship
        elif destruction_cycle[day_element] == spouse_element or destruction_cycle[spouse_element] == day_element:
            relationship_quality = 0.3  # Destructive relationship
        
        return {
            'spouse_palace': spouse_palace,
            'day_element': day_element,
            'marriage_probability': relationship_quality,
            'element_harmony': relationship_quality > 0.6,
            'marriage_timing': 'early' if hash(spouse_palace) % 3 == 0 else 'middle' if hash(spouse_palace) % 3 == 1 else 'late'
        }

# Vedic Astrology System
class VedicAstrology:
    """Vedic Astrology (Jyotish) calculation system"""
    
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    @classmethod
    def calculate_vedic_chart(cls, birth_date: str, latitude: float, longitude: float) -> Dict[str, Any]:
        """Calculate Vedic astrological factors"""
        date_obj = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
        
        # Calculate Ayanamsa (precession correction)
        ayanamsa = cls._calculate_ayanamsa(date_obj)
        
        # Calculate Nakshatra (lunar mansion)
        lunar_longitude = (date_obj.timetuple().tm_yday * 13.176) % 360  # Simplified
        nakshatra_index = int((lunar_longitude + ayanamsa) / 13.333) % 27
        
        # Calculate 7th house lord for marriage analysis
        seventh_house_analysis = cls._analyze_seventh_house(date_obj, ayanamsa)
        
        return {
            'ayanamsa': ayanamsa,
            'nakshatra': {
                'name': cls.NAKSHATRAS[nakshatra_index],
                'index': nakshatra_index,
                'pada': int((lunar_longitude % 13.333) / 3.333) + 1
            },
            'seventh_house_analysis': seventh_house_analysis,
            'marriage_yogas': cls._identify_marriage_yogas(date_obj, ayanamsa)
        }
    
    @classmethod
    def _calculate_ayanamsa(cls, date: datetime.datetime) -> float:
        """Calculate Lahiri Ayanamsa"""
        # Simplified Lahiri Ayanamsa calculation
        years_since_1900 = (date.year - 1900) + date.timetuple().tm_yday / 365.25
        ayanamsa = 22.460 + (years_since_1900 * 0.013972)  # Approximate
        return ayanamsa % 360
    
    @classmethod
    def _analyze_seventh_house(cls, date: datetime.datetime, ayanamsa: float) -> Dict[str, Any]:
        """Analyze 7th house for marriage indications"""
        # Simplified 7th house analysis
        seventh_house_strength = (hash(str(date)) % 100) / 100
        
        return {
            'strength': seventh_house_strength,
            'marriage_potential': seventh_house_strength,
            'timing_indication': 'early' if seventh_house_strength > 0.7 else 'delayed' if seventh_house_strength < 0.3 else 'normal'
        }
    
    @classmethod
    def _identify_marriage_yogas(cls, date: datetime.datetime, ayanamsa: float) -> List[Dict[str, Any]]:
        """Identify marriage-related yogas"""
        yogas = []
        
        # Simplified yoga identification
        date_hash = hash(str(date))
        
        if date_hash % 7 == 0:
            yogas.append({
                'name': 'Kalatra Karaka Yoga',
                'strength': 0.8,
                'description': 'Favorable for marriage timing'
            })
        
        if date_hash % 11 == 0:
            yogas.append({
                'name': 'Venus-Jupiter Conjunction',
                'strength': 0.9,
                'description': 'Very auspicious for marriage'
            })
        
        return yogas

# Runic System
class RunicSystem:
    """Nordic Runic divination system"""
    
    ELDER_FUTHARK = {
        'ᚠ': ('Fehu', 'Wealth', 'Manifestation of goals'),
        'ᚢ': ('Uruz', 'Strength', 'Determination'),
        'ᚦ': ('Thurisaz', 'Giant', 'Challenges'),
        'ᚨ': ('Ansuz', 'God', 'Communication'),
        'ᚱ': ('Raidho', 'Journey', 'Travel, movement'),
        'ᚲ': ('Kenaz', 'Beacon', 'Knowledge, creativity'),
        'ᚷ': ('Gebo', 'Gift', 'Partnerships, marriage'),
        'ᚹ': ('Wunjo', 'Joy', 'Happiness, harmony'),
        # ... (24 runes total, showing key ones for marriage)
    }
    
    @classmethod
    def cast_runes_for_marriage(cls, birth_date: str, query_date: str) -> Dict[str, Any]:
        """Cast runes for marriage prediction"""
        # Use dates to seed rune selection
        seed = hash(birth_date + query_date)
        random.seed(seed)
        
        # Three-rune spread: Past, Present, Future
        rune_keys = list(cls.ELDER_FUTHARK.keys())
        selected_runes = random.sample(rune_keys, 3)
        
        spread = {}
        positions = ['past', 'present', 'future']
        marriage_score = 0.0
        
        for i, rune in enumerate(selected_runes):
            rune_data = cls.ELDER_FUTHARK[rune]
            spread[positions[i]] = {
                'rune': rune,
                'name': rune_data[0],
                'meaning': rune_data[1],
                'interpretation': rune_data[2]
            }
            
            # Marriage-favorable runes
            if rune in ['ᚷ', 'ᚹ']:  # Gebo (partnership) and Wunjo (joy)
                marriage_score += 0.4
            elif rune in ['ᚠ', 'ᚱ']:  # Fehu (manifestation) and Raidho (journey)
                marriage_score += 0.2
        
        return {
            'rune_spread': spread,
            'marriage_probability': min(marriage_score, 1.0),
            'overall_interpretation': cls._interpret_marriage_spread(spread, marriage_score)
        }
    
    @classmethod
    def _interpret_marriage_spread(cls, spread: Dict, score: float) -> str:
        """Interpret the three-rune spread for marriage"""
        if score > 0.6:
            return "Very favorable for marriage and partnerships"
        elif score > 0.4:
            return "Moderate potential for marriage, timing important"
        else:
            return "Challenges in partnership area, patience required"

# Integrated BTU System
class IntegratedIoRSystem:
    """Complete BTU system integrating all divination methods"""
    
    def __init__(self):
        self.astro_engine = BTUAstroEngine()
        self.system_weights = {
            'western_astrology': 0.30,
            'i_ching': 0.20,
            'saju_four_pillars': 0.25,
            'vedic_astrology': 0.15,
            'runic_divination': 0.10
        }
    
    def comprehensive_analysis(self, profile: CelebrityProfile, marriage_event: MarriageEvent) -> Dict[str, Any]:
        """Perform comprehensive multi-system analysis"""
        birth_data = profile.birth_data
        
        # Western Astrology Analysis
        astro_analysis = self.astro_engine.analyze_marriage_timing(birth_data, [marriage_event])
        western_score = astro_analysis["natal_chart"]["base_marriage_score"]["composite_score"]
        
        # I-Ching Analysis
        iching_result = IChing.calculate_hexagram(birth_data.birth_date, marriage_event.marriage_date)
        iching_score = iching_result['marriage_indication']['marriage_probability']
        
        # Saju (Four Pillars) Analysis
        saju_result = SajuSystem.calculate_four_pillars(birth_data.birth_date, birth_data.birth_time)
        saju_score = saju_result['marriage_analysis']['marriage_probability']
        
        # Vedic Astrology Analysis
        vedic_result = VedicAstrology.calculate_vedic_chart(
            birth_data.birth_date, birth_data.latitude, birth_data.longitude
        )
        vedic_score = vedic_result['seventh_house_analysis']['marriage_potential']
        
        # Runic Analysis
        runic_result = RunicSystem.cast_runes_for_marriage(birth_data.birth_date, marriage_event.marriage_date)
        runic_score = runic_result['marriage_probability']
        
        # Calculate weighted composite score
        composite_score = (
            western_score * self.system_weights['western_astrology'] +
            iching_score * self.system_weights['i_ching'] +
            saju_score * self.system_weights['saju_four_pillars'] +
            vedic_score * self.system_weights['vedic_astrology'] +
            runic_score * self.system_weights['runic_divination']
        )
        
        return {
            'celebrity': birth_data.name,
            'marriage_event': {
                'spouse': marriage_event.spouse_name,
                'date': marriage_event.marriage_date,
                'location': marriage_event.marriage_location
            },
            'system_scores': {
                'western_astrology': round(western_score, 3),
                'i_ching': round(iching_score, 3),
                'saju_four_pillars': round(saju_score, 3),
                'vedic_astrology': round(vedic_score, 3),
                'runic_divination': round(runic_score, 3)
            },
            'composite_btu_score': round(composite_score, 3),
            'detailed_analysis': {
                'western': astro_analysis["natal_chart"]["significant_aspects"][:3],
                'iching': iching_result['primary_hexagram'],
                'saju': saju_result['four_pillars'],
                'vedic': vedic_result['nakshatra'],
                'runes': runic_result['rune_spread']
            },
            'cross_system_correlation': self._calculate_correlation({
                'western': western_score,
                'iching': iching_score,
                'saju': saju_score,
                'vedic': vedic_score,
                'runes': runic_score
            })
        }
    
    def _calculate_correlation(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate cross-system correlation analysis"""
        score_values = list(scores.values())
        mean_score = np.mean(score_values)
        std_score = np.std(score_values)
        
        # Agreement level between systems
        agreement_threshold = 0.2
        agreements = sum(1 for score in score_values if abs(score - mean_score) < agreement_threshold)
        agreement_percentage = (agreements / len(score_values)) * 100
        
        return {
            'mean_score': round(mean_score, 3),
            'standard_deviation': round(std_score, 3),
            'system_agreement': f"{agreement_percentage:.1f}%",
            'consensus_level': 'high' if agreement_percentage > 60 else 'moderate' if agreement_percentage > 40 else 'low'
        }

def comprehensive_btu_validation():
    """Run comprehensive BTU validation across all systems"""
    print("Integrated BTU System - Comprehensive Validation")
    print("=" * 50)
    
    collector = BTUDataCollector()
    integrated_system = IntegratedBTUSystem()
    
    validation_results = {
        'total_analyses': 0,
        'system_performance': {},
        'celebrity_analyses': [],
        'cross_system_correlations': []
    }
    
    all_scores = {system: [] for system in integrated_system.system_weights.keys()}
    all_composite_scores = []
    
    for name, profile in collector.celebrities.items():
        if not profile.marriages:
            continue
        
        celebrity_results = {
            'name': profile.birth_data.name,
            'marriages': []
        }
        
        for marriage in profile.marriages:
            print(f"\nAnalyzing {profile.birth_data.name} - {marriage.spouse_name} ({marriage.marriage_date})")
            
            analysis = integrated_system.comprehensive_analysis(profile, marriage)
            celebrity_results['marriages'].append(analysis)
            
            # Collect scores for statistical analysis
            for system, score in analysis['system_scores'].items():
                all_scores[system].append(score)
            
            all_composite_scores.append(analysis['composite_btu_score'])
            validation_results['total_analyses'] += 1
        
        validation_results['celebrity_analyses'].append(celebrity_results)
    
    # Calculate system performance metrics
    for system, scores in all_scores.items():
        if scores:
            validation_results['system_performance'][system] = {
                'mean_score': round(np.mean(scores), 3),
                'std_deviation': round(np.std(scores), 3),
                'min_score': round(min(scores), 3),
                'max_score': round(max(scores), 3)
            }
    
    validation_results['composite_statistics'] = {
        'mean_composite': round(np.mean(all_composite_scores), 3),
        'std_composite': round(np.std(all_composite_scores), 3),
        'total_marriages_analyzed': len(all_composite_scores)
    }
    
    # Save comprehensive results
    with open("integrated_btu_validation.json", "w", encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 50)
    print("INTEGRATED BTU VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total marriages analyzed: {validation_results['total_analyses']}")
    print(f"Mean composite BTU score: {validation_results['composite_statistics']['mean_composite']}")
    print(f"Standard deviation: {validation_results['composite_statistics']['std_composite']}")
    
    print("\nSystem Performance Comparison:")
    for system, metrics in validation_results['system_performance'].items():
        print(f"  {system.replace('_', ' ').title()}: {metrics['mean_score']} ± {metrics['std_deviation']}")
    
    print("\nTop Composite Scores:")
    top_scores = sorted(all_composite_scores, reverse=True)[:5]
    for i, score in enumerate(top_scores, 1):
        print(f"  #{i}: {score}")
    
    print(f"\n✅ Comprehensive BTU validation complete!")
    print(f"📊 Results saved to: integrated_btu_validation.json")
    
    return validation_results

if __name__ == "__main__":
    comprehensive_btu_validation()
