#!/usr/bin/env python3
"""
IoR Astrological Engine - Marriage Prediction Module
==================================================

IoR (Impression of Reality) 점성술 엔진 - 결혼 예측 모듈
실제 유명인 데이터를 통한 결혼 타이밍 예측의 경험적 검증을 위한 
고급 점성술 계산 엔진

통합 요소:
- 서양 열대 점성술 (행성, 하우스, 측면)
- 베다 점성술 원리
- 사건 타이밍을 위한 트랜짓 분석
- 통계적 검증 방법론

"""

import json
import math
import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import numpy as np
from btu_data_collector import BTUDataCollector, CelebrityProfile, MarriageEvent

# External libraries needed: pip install pyephem astropy
try:
    import ephem
    EPHEM_AVAILABLE = True
except ImportError:
    EPHEM_AVAILABLE = False
    print("⚠️ pyephem not available. Install with: pip install pyephem")

@dataclass
class PlanetPosition:
    """Planet position in zodiac"""
    name: str
    longitude: float  # 0-360 degrees
    latitude: float
    sign: str  # Zodiac sign name
    degree: float  # Degree within sign (0-30)
    house: int  # House position (1-12)
    retrograde: bool = False

@dataclass
class AspectData:
    """Planetary aspect information"""
    planet1: str
    planet2: str
    aspect_type: str  # conjunction, opposition, trine, etc.
    orb: float  # Degrees of separation
    exact_orb: float  # Perfect aspect degrees
    applying: bool  # Is aspect applying or separating

@dataclass
class TransitData:
    """Transit information for event analysis"""
    date: str
    transiting_planet: str
    natal_planet: str
    aspect_type: str
    orb: float
    house_activated: int

class IoRAstroEngine:
    """Advanced astrological calculation engine for BTU validation"""
    
    def __init__(self):
        self.signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        self.planets = [
            "Sun", "Moon", "Mercury", "Venus", "Mars", 
            "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
        ]
        
        # Marriage significance weights for different factors
        self.marriage_weights = {
            "venus_aspects": 0.25,
            "seventh_house": 0.30,
            "jupiter_transits": 0.20,
            "lunar_aspects": 0.15,
            "composite_score": 0.10
        }
        
        # Aspect significance for marriage
        self.aspect_weights = {
            "conjunction": 1.0,
            "opposition": 0.8,
            "trine": 0.7,
            "square": 0.6,
            "sextile": 0.5,
            "semi-sextile": 0.3,
            "quincunx": 0.4
        }
    
    def calculate_natal_chart(self, birth_data) -> Dict[str, PlanetPosition]:
        """Calculate natal chart positions"""
        if not EPHEM_AVAILABLE:
            return self._mock_natal_positions(birth_data)
        
        # Set up observer location and time
        observer = ephem.Observer()
        observer.lat = str(birth_data.latitude)
        observer.lon = str(birth_data.longitude)
        
        # Parse birth date and time
        birth_datetime = datetime.datetime.strptime(
            f"{birth_data.birth_date} {birth_data.birth_time}", 
            "%Y-%m-%d %H:%M"
        )
        observer.date = birth_datetime
        
        positions = {}
        
        # Calculate planetary positions
        ephemeris_planets = {
            'Sun': ephem.Sun(),
            'Moon': ephem.Moon(),
            'Mercury': ephem.Mercury(),
            'Venus': ephem.Venus(),
            'Mars': ephem.Mars(),
            'Jupiter': ephem.Jupiter(),
            'Saturn': ephem.Saturn(),
            'Uranus': ephem.Uranus(),
            'Neptune': ephem.Neptune(),
            'Pluto': ephem.Pluto()
        }
        
        for planet_name, planet_obj in ephemeris_planets.items():
            planet_obj.compute(observer)
            
            # Convert to degrees
            longitude = math.degrees(planet_obj.ra)  # Right ascension
            latitude = math.degrees(planet_obj.dec)  # Declination
            
            # Convert to zodiacal longitude (simplified)
            zodiac_longitude = (longitude + observer.sidereal_time() * 15) % 360
            
            sign_index = int(zodiac_longitude // 30)
            degree_in_sign = zodiac_longitude % 30
            
            positions[planet_name] = PlanetPosition(
                name=planet_name,
                longitude=zodiac_longitude,
                latitude=latitude,
                sign=self.signs[sign_index],
                degree=degree_in_sign,
                house=self._calculate_house_position(zodiac_longitude, birth_data),
                retrograde=False  # Simplified for now
            )
        
        return positions
    
    def _mock_natal_positions(self, birth_data) -> Dict[str, PlanetPosition]:
        """Mock positions when ephem is not available"""
        # This creates realistic-looking but fake positions for testing
        import random
        
        positions = {}
        random.seed(hash(birth_data.birth_date + birth_data.name))
        
        for planet in self.planets:
            longitude = random.uniform(0, 360)
            sign_index = int(longitude // 30)
            degree_in_sign = longitude % 30
            
            positions[planet] = PlanetPosition(
                name=planet,
                longitude=longitude,
                latitude=random.uniform(-5, 5),
                sign=self.signs[sign_index],
                degree=degree_in_sign,
                house=random.randint(1, 12),
                retrograde=random.choice([True, False])
            )
        
        return positions
    
    def _calculate_house_position(self, longitude: float, birth_data) -> int:
        """Calculate house position (simplified Placidus system)"""
        # This is a simplified calculation
        # Real implementation would need accurate house cusp calculation
        house_size = 30  # Equal house system for simplicity
        ascendant_adjustment = hash(birth_data.birth_time) % 360
        adjusted_longitude = (longitude + ascendant_adjustment) % 360
        return int(adjusted_longitude // house_size) + 1
    
    def calculate_aspects(self, positions: Dict[str, PlanetPosition]) -> List[AspectData]:
        """Calculate planetary aspects"""
        aspects = []
        planet_names = list(positions.keys())
        
        # Major aspects and their exact degrees
        aspect_degrees = {
            "conjunction": 0,
            "semi-sextile": 30,
            "sextile": 60,
            "square": 90,
            "trine": 120,
            "quincunx": 150,
            "opposition": 180
        }
        
        # Orbs for different aspects
        orbs = {
            "conjunction": 8,
            "opposition": 8,
            "trine": 6,
            "square": 6,
            "sextile": 4,
            "semi-sextile": 3,
            "quincunx": 3
        }
        
        for i, planet1 in enumerate(planet_names):
            for planet2 in planet_names[i+1:]:
                pos1 = positions[planet1]
                pos2 = positions[planet2]
                
                # Calculate angular separation
                separation = abs(pos1.longitude - pos2.longitude)
                if separation > 180:
                    separation = 360 - separation
                
                # Check for aspects
                for aspect_name, exact_degrees in aspect_degrees.items():
                    orb_allowed = orbs[aspect_name]
                    orb = abs(separation - exact_degrees)
                    
                    if orb <= orb_allowed:
                        aspects.append(AspectData(
                            planet1=planet1,
                            planet2=planet2,
                            aspect_type=aspect_name,
                            orb=orb,
                            exact_orb=exact_degrees,
                            applying=True  # Simplified
                        ))
        
        return aspects
    
    def calculate_marriage_probability_score(self, positions: Dict[str, PlanetPosition], 
                                           aspects: List[AspectData]) -> Dict[str, float]:
        """Calculate marriage probability based on natal chart factors"""
        scores = {
            "venus_aspects": 0.0,
            "seventh_house": 0.0,
            "jupiter_transits": 0.0,
            "lunar_aspects": 0.0,
            "composite_score": 0.0
        }
        
        # Venus aspects score
        venus_score = 0.0
        for aspect in aspects:
            if "Venus" in [aspect.planet1, aspect.planet2]:
                weight = self.aspect_weights.get(aspect.aspect_type, 0.3)
                orb_factor = max(0, 1 - (aspect.orb / 8))  # Closer aspects = higher score
                venus_score += weight * orb_factor
        
        scores["venus_aspects"] = min(venus_score, 1.0)
        
        # 7th House significance
        seventh_house_planets = [p for p in positions.values() if p.house == 7]
        seventh_house_score = len(seventh_house_planets) * 0.2
        
        # Venus in 7th house bonus
        if positions["Venus"].house == 7:
            seventh_house_score += 0.3
        
        scores["seventh_house"] = min(seventh_house_score, 1.0)
        
        # Jupiter aspects (expansion, marriage)
        jupiter_score = 0.0
        for aspect in aspects:
            if "Jupiter" in [aspect.planet1, aspect.planet2]:
                if aspect.aspect_type in ["trine", "sextile", "conjunction"]:
                    weight = self.aspect_weights.get(aspect.aspect_type, 0.3)
                    orb_factor = max(0, 1 - (aspect.orb / 6))
                    jupiter_score += weight * orb_factor
        
        scores["jupiter_transits"] = min(jupiter_score, 1.0)
        
        # Lunar aspects (emotional connections)
        lunar_score = 0.0
        for aspect in aspects:
            if "Moon" in [aspect.planet1, aspect.planet2]:
                if aspect.aspect_type in ["trine", "sextile", "conjunction"]:
                    weight = self.aspect_weights.get(aspect.aspect_type, 0.3)
                    orb_factor = max(0, 1 - (aspect.orb / 6))
                    lunar_score += weight * orb_factor
        
        scores["lunar_aspects"] = min(lunar_score, 1.0)
        
        # Composite score calculation
        weighted_sum = sum(scores[key] * self.marriage_weights[key] 
                          for key in scores if key != "composite_score")
        scores["composite_score"] = weighted_sum
        
        return scores
    
    def analyze_marriage_timing(self, birth_data, marriage_events: List[MarriageEvent]) -> Dict[str, Any]:
        """Analyze astrological factors for actual marriage dates"""
        natal_positions = self.calculate_natal_chart(birth_data)
        natal_aspects = self.calculate_aspects(natal_positions)
        base_marriage_score = self.calculate_marriage_probability_score(natal_positions, natal_aspects)
        
        marriage_analysis = {
            "natal_chart": {
                "positions": {name: {
                    "sign": pos.sign,
                    "house": pos.house,
                    "degree": round(pos.degree, 2)
                } for name, pos in natal_positions.items()},
                "significant_aspects": [
                    {
                        "planets": f"{asp.planet1}-{asp.planet2}",
                        "aspect": asp.aspect_type,
                        "orb": round(asp.orb, 2)
                    } for asp in natal_aspects if asp.orb <= 3
                ],
                "base_marriage_score": base_marriage_score
            },
            "marriage_events": []
        }
        
        for marriage in marriage_events:
            # Calculate transits for marriage date
            marriage_date = datetime.datetime.strptime(marriage.marriage_date, "%Y-%m-%d")
            
            # Simplified transit analysis
            transit_score = self._calculate_transit_score(marriage_date, natal_positions)
            
            marriage_analysis["marriage_events"].append({
                "spouse": marriage.spouse_name,
                "date": marriage.marriage_date,
                "transit_score": transit_score,
                "predicted_probability": base_marriage_score["composite_score"] * transit_score,
                "location": marriage.marriage_location
            })
        
        return marriage_analysis
    
    def _calculate_transit_score(self, date: datetime.datetime, natal_positions: Dict[str, PlanetPosition]) -> float:
        """Calculate transit activation score for a specific date"""
        # This would normally calculate actual transiting planet positions
        # For now, we'll use a simplified scoring based on date patterns
        
        # Factors that might increase marriage probability on specific dates:
        # - Jupiter transits to Venus or 7th house
        # - Venus returns
        # - Significant lunar phases
        
        # Simplified scoring based on date characteristics
        month = date.month
        day = date.day
        
        # Some months traditionally associated with marriage
        marriage_months = [5, 6, 9, 10]  # May, June, September, October
        month_score = 0.8 if month in marriage_months else 0.6
        
        # Weekend bonus (many marriages on weekends)
        weekend_bonus = 0.1 if date.weekday() >= 5 else 0.0
        
        # Venus cycle approximation (584 days)
        days_since_epoch = (date - datetime.datetime(2000, 1, 1)).days
        venus_cycle_position = (days_since_epoch % 584) / 584
        venus_score = 0.5 + 0.3 * math.sin(2 * math.pi * venus_cycle_position)
        
        total_score = (month_score + weekend_bonus + venus_score) / 2
        return min(total_score, 1.0)

def validate_btu_predictions():
    """Validate BTU predictions against real celebrity marriage data"""
    print("BTU Astrological Engine Validation")
    print("=" * 40)
    
    collector = BTUDataCollector()
    engine = BTUAstroEngine()
    
    validation_results = {
        "total_celebrities": len(collector.celebrities),
        "total_marriages": 0,
        "predictions": [],
        "accuracy_metrics": {}
    }
    
    all_predicted_scores = []
    all_actual_events = []
    
    for name, profile in collector.celebrities.items():
        print(f"\nAnalyzing {profile.birth_data.name}...")
        
        if not profile.marriages:
            continue
        
        analysis = engine.analyze_marriage_timing(profile.birth_data, profile.marriages)
        validation_results["total_marriages"] += len(profile.marriages)
        
        celebrity_prediction = {
            "name": profile.birth_data.name,
            "natal_marriage_score": analysis["natal_chart"]["base_marriage_score"]["composite_score"],
            "marriages": []
        }
        
        for marriage_event in analysis["marriage_events"]:
            predicted_prob = marriage_event["predicted_probability"]
            all_predicted_scores.append(predicted_prob)
            all_actual_events.append(1)  # All events in our data actually happened
            
            celebrity_prediction["marriages"].append({
                "spouse": marriage_event["spouse"],
                "date": marriage_event["date"],
                "predicted_probability": round(predicted_prob, 3),
                "transit_score": round(marriage_event["transit_score"], 3)
            })
        
        validation_results["predictions"].append(celebrity_prediction)
    
    # Calculate accuracy metrics
    if all_predicted_scores:
        mean_prediction = np.mean(all_predicted_scores)
        std_prediction = np.std(all_predicted_scores)
        
        validation_results["accuracy_metrics"] = {
            "mean_predicted_score": round(mean_prediction, 3),
            "std_predicted_score": round(std_prediction, 3),
            "total_marriages_analyzed": len(all_predicted_scores),
            "note": "All events are actual marriages (ground truth = 1.0)"
        }
    
    # Save results
    with open("btu_validation_results.json", "w") as f:
        json.dump(validation_results, f, indent=2)
    
    print("\n" + "=" * 40)
    print("VALIDATION SUMMARY")
    print("=" * 40)
    print(f"Celebrities analyzed: {validation_results['total_celebrities']}")
    print(f"Total marriages: {validation_results['total_marriages']}")
    print(f"Mean prediction score: {validation_results['accuracy_metrics'].get('mean_predicted_score', 'N/A')}")
    print(f"Std deviation: {validation_results['accuracy_metrics'].get('std_predicted_score', 'N/A')}")
    
    print("\nTop Predictions:")
    sorted_predictions = sorted(validation_results["predictions"], 
                               key=lambda x: x["natal_marriage_score"], reverse=True)
    
    for pred in sorted_predictions[:5]:
        print(f"  {pred['name']}: {pred['natal_marriage_score']:.3f}")
    
    print("\n✅ BTU validation complete! Results saved to btu_validation_results.json")
    return validation_results

if __name__ == "__main__":
    validate_btu_predictions()
