#!/usr/bin/env python3
"""IoR 시스템 빠른 테스트"""

import json
import numpy as np
import pandas as pd

# 데이터 로드
with open('integrated_ior_validation.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("🌌 IoR (Impression of Reality) 시스템 분석 결과")
print("=" * 50)

# 기본 통계
total_analyses = len(data['celebrity_analyses'])
print(f"📊 분석된 결혼 데이터: {total_analyses}개")

# 시스템별 평균 점수
systems = ['western_astrology', 'i_ching', 'saju_four_pillars', 'vedic_astrology', 'runic_divination']
system_scores = {sys: [] for sys in systems}

for celebrity in data['celebrity_analyses']:
    for marriage in celebrity['marriages']:
        for system, score in marriage['system_scores'].items():
            if system in system_scores:
                system_scores[system].append(score)

print("\n🎯 시스템별 성능:")
for system, scores in system_scores.items():
    avg = np.mean(scores)
    std = np.std(scores)
    print(f"  {system.replace('_', ' ').title()}: {avg:.3f} ± {std:.3f}")

# 가장 높은 점수 시스템
best_system = max(system_scores.items(), key=lambda x: np.mean(x[1]))
print(f"\n🏆 최고 성능 시스템: {best_system[0].replace('_', ' ').title()} ({np.mean(best_system[1]):.3f})")

# 일관성 분석 (낮은 표준편차 = 높은 일관성)
most_consistent = min(system_scores.items(), key=lambda x: np.std(x[1]))
print(f"🎯 가장 일관된 시스템: {most_consistent[0].replace('_', ' ').title()} (std: {np.std(most_consistent[1]):.3f})")

print("\n✅ IoR 시스템이 성공적으로 다중 점술 데이터를 분석했습니다!")
print("💡 전체 고급 분석을 원하시면 ior_advanced_analytics.py를 실행하세요.")
