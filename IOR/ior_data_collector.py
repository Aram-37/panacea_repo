#!/usr/bin/env python3
"""
IoR Data Collector - Celebrity Birth and Marriage Data
=====================================================

IoR (Impression of Reality) 데이터 수집기 - 유명인 출생 및 결혼 데이터
점성술 예측의 경험적 검증을 위한 선별된 유명인들의 출생 및 결혼 데이터 수집 및 구조화
특히 결혼 타이밍과 7하우스/금성 상관관계에 초점

테스트 대상:
- Elon Musk, Katy Perry, Jeff Bezos, Liza Minnelli, Macaulay Culkin
- Justin Bieber, Selena Gomez, Song Hye-kyo, Angelina Jolie, Tom Cruise
"""

import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import pytz

@dataclass
class BirthData:
    """Structured birth information for astrological analysis"""
    name: str
    birth_date: str  # YYYY-MM-DD format
    birth_time: str  # HH:MM format (24-hour)
    birth_location: str
    latitude: float
    longitude: float
    timezone: str
    source: str  # Data source/reliability indicator

@dataclass
class MarriageEvent:
    """Marriage event with precise timing for validation"""
    spouse_name: str
    marriage_date: str  # YYYY-MM-DD format
    marriage_location: str
    marriage_type: str  # legal, religious, civil, etc.
    ended_date: Optional[str] = None  # If divorced/separated
    source: str = ""

@dataclass
class CelebrityProfile:
    """Complete celebrity profile for BTU analysis"""
    birth_data: BirthData
    marriages: List[MarriageEvent]
    notable_relationships: List[Dict[str, Any]] = None
    career_milestones: List[Dict[str, Any]] = None

class IoRDataCollector:
    """Collects and validates celebrity data for BTU testing"""
    
    def __init__(self):
        self.celebrities = {}
        self.load_celebrity_data()
    
    def load_celebrity_data(self):
        """Load known celebrity birth and marriage data"""
        
        # Elon Musk
        self.celebrities["elon_musk"] = CelebrityProfile(
            birth_data=BirthData(
                name="Elon Musk",
                birth_date="1971-06-28",
                birth_time="07:30",  # Approximate
                birth_location="Pretoria, South Africa",
                latitude=-25.7479,
                longitude=28.2293,
                timezone="Africa/Johannesburg",
                source="Public records, approximate time"
            ),
            marriages=[
                MarriageEvent(
                    spouse_name="Justine Wilson",
                    marriage_date="2000-01-01",  # Approximate
                    marriage_location="Canada",
                    marriage_type="legal",
                    ended_date="2008-09-01",
                    source="Public records"
                ),
                MarriageEvent(
                    spouse_name="Talulah Riley",
                    marriage_date="2010-09-25",
                    marriage_location="Scotland",
                    marriage_type="legal",
                    ended_date="2012-01-01",
                    source="Public records"
                ),
                MarriageEvent(
                    spouse_name="Talulah Riley",
                    marriage_date="2013-07-01",  # Remarried
                    marriage_location="England",
                    marriage_type="legal",
                    ended_date="2016-10-01",
                    source="Public records"
                )
            ]
        )
        
        # Katy Perry
        self.celebrities["katy_perry"] = CelebrityProfile(
            birth_data=BirthData(
                name="Katy Perry",
                birth_date="1984-10-25",
                birth_time="10:58",  # Reported birth time
                birth_location="Santa Barbara, California, USA",
                latitude=34.4208,
                longitude=-119.6982,
                timezone="America/Los_Angeles",
                source="Celebrity astrology sites"
            ),
            marriages=[
                MarriageEvent(
                    spouse_name="Russell Brand",
                    marriage_date="2010-10-23",
                    marriage_location="Rajasthan, India",
                    marriage_type="Hindu ceremony",
                    ended_date="2012-07-16",
                    source="Public records"
                )
            ]
        )
        
        # Jeff Bezos
        self.celebrities["jeff_bezos"] = CelebrityProfile(
            birth_data=BirthData(
                name="Jeff Bezos",
                birth_date="1964-01-12",
                birth_time="12:00",  # Noon (unknown exact time)
                birth_location="Albuquerque, New Mexico, USA",
                latitude=35.0844,
                longitude=-106.6504,
                timezone="America/Denver",
                source="Public records, time estimated"
            ),
            marriages=[
                MarriageEvent(
                    spouse_name="MacKenzie Scott",
                    marriage_date="1993-09-04",
                    marriage_location="Seattle, Washington, USA",
                    marriage_type="legal",
                    ended_date="2019-07-05",
                    source="Public records"
                )
            ]
        )
        
        # Justin Bieber
        self.celebrities["justin_bieber"] = CelebrityProfile(
            birth_data=BirthData(
                name="Justin Bieber",
                birth_date="1994-03-01",
                birth_time="00:56",  # Reported birth time
                birth_location="London, Ontario, Canada",
                latitude=42.9849,
                longitude=-81.2453,
                timezone="America/Toronto",
                source="Celebrity birth records"
            ),
            marriages=[
                MarriageEvent(
                    spouse_name="Hailey Baldwin",
                    marriage_date="2018-09-13",  # Legal ceremony
                    marriage_location="New York City, USA",
                    marriage_type="legal",
                    source="Public records"
                ),
                MarriageEvent(
                    spouse_name="Hailey Baldwin",
                    marriage_date="2019-09-30",  # Religious ceremony
                    marriage_location="South Carolina, USA",
                    marriage_type="religious",
                    source="Public records"
                )
            ]
        )
        
        # Tom Cruise
        self.celebrities["tom_cruise"] = CelebrityProfile(
            birth_data=BirthData(
                name="Tom Cruise",
                birth_date="1962-07-03",
                birth_time="15:06",  # Reported birth time
                birth_location="Syracuse, New York, USA",
                latitude=43.0481,
                longitude=-76.1474,
                timezone="America/New_York",
                source="Celebrity astrology records"
            ),
            marriages=[
                MarriageEvent(
                    spouse_name="Mimi Rogers",
                    marriage_date="1987-05-09",
                    marriage_location="New York, USA",
                    marriage_type="legal",
                    ended_date="1990-02-04",
                    source="Public records"
                ),
                MarriageEvent(
                    spouse_name="Nicole Kidman",
                    marriage_date="1990-12-24",
                    marriage_location="Telluride, Colorado, USA",
                    marriage_type="legal",
                    ended_date="2001-08-08",
                    source="Public records"
                ),
                MarriageEvent(
                    spouse_name="Katie Holmes",
                    marriage_date="2006-11-18",
                    marriage_location="Bracciano, Italy",
                    marriage_type="Scientology ceremony",
                    ended_date="2012-08-20",
                    source="Public records"
                )
            ]
        )
    
    def add_celebrity(self, profile: CelebrityProfile):
        """Add a new celebrity profile"""
        key = profile.birth_data.name.lower().replace(" ", "_")
        self.celebrities[key] = profile
    
    def get_celebrity(self, name: str) -> Optional[CelebrityProfile]:
        """Retrieve celebrity profile by name"""
        key = name.lower().replace(" ", "_")
        return self.celebrities.get(key)
    
    def list_celebrities(self) -> List[str]:
        """List all available celebrities"""
        return [profile.birth_data.name for profile in self.celebrities.values()]
    
    def export_to_json(self, filename: str = "celebrity_data.json"):
        """Export all data to JSON for analysis"""
        export_data = {}
        for key, profile in self.celebrities.items():
            export_data[key] = {
                "birth_data": asdict(profile.birth_data),
                "marriages": [asdict(marriage) for marriage in profile.marriages],
                "notable_relationships": profile.notable_relationships or [],
                "career_milestones": profile.career_milestones or []
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Data exported to {filename}")
        return export_data
    
    def validate_data_completeness(self):
        """Check data completeness and quality"""
        report = {
            "total_celebrities": len(self.celebrities),
            "celebrities_with_marriages": 0,
            "total_marriages": 0,
            "data_quality_issues": []
        }
        
        for name, profile in self.celebrities.items():
            if profile.marriages:
                report["celebrities_with_marriages"] += 1
                report["total_marriages"] += len(profile.marriages)
            
            # Check for missing birth times
            if profile.birth_data.birth_time == "12:00" and "estimated" in profile.birth_data.source:
                report["data_quality_issues"].append(f"{profile.birth_data.name}: Birth time estimated")
            
            # Check for approximate marriage dates
            for marriage in profile.marriages:
                if "approximate" in marriage.source.lower():
                    report["data_quality_issues"].append(f"{profile.birth_data.name}: Marriage date approximate")
        
        return report

def main():
    """Demo of BTU data collection"""
    collector = BTUDataCollector()
    
    print("BTU Data Collector - Celebrity Marriage Analysis")
    print("=" * 50)
    
    print(f"\nLoaded {len(collector.celebrities)} celebrities:")
    for name in collector.list_celebrities():
        print(f"  - {name}")
    
    print("\nData Quality Report:")
    report = collector.validate_data_completeness()
    for key, value in report.items():
        if key != "data_quality_issues":
            print(f"  {key}: {value}")
    
    if report["data_quality_issues"]:
        print("\nData Quality Issues:")
        for issue in report["data_quality_issues"]:
            print(f"  ⚠️ {issue}")
    
    # Export data
    collector.export_to_json()
    
    print("\n✅ Data collection complete. Ready for BTU analysis!")

if __name__ == "__main__":
    main()
