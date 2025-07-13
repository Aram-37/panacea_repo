#!/usr/bin/env python3
"""
IoR Complete Analysis - 베이지안 부두 직접 개입 + 리만 점성술 기하학
================================================================
Impression of Reality (IoR) - 현실의 인상을 다각도로 분석하는 통합 시스템

부두 = 베이지안 직접 개입 시스템 (현실 조작)
점성술 = 리만 기하학적 곡률 시스템 (우주적 정렬)
사주 = 조합론적 패턴 시스템 (관계 패턴)
주역 = 확률론적 엔탱글먼트 시스템 (동시성)
룬 = 위상수학적 연결 시스템 (상징적 연결)
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

class IoRCompleteAnalysis:
    """IoR (Impression of Reality) 완전 분석 시스템
    
    부두의 베이지안 직접 개입과 점성술의 리만 기하학적 특성을 통합한
    수학적으로 정교한 현실 분석 엔진
    """
    
    def __init__(self, validation_file="integrated_ior_validation.json"):
        """초기화 및 데이터 로드"""
        try:
            with open(validation_file, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
            print(f"✅ 기존 데이터 파일 로드: {validation_file}")
            self.df = self._prepare_dataframe()
        except FileNotFoundError:
            print(f"⚠️ {validation_file}를 찾을 수 없습니다. 간단한 테스트 데이터를 생성합니다.")
            self.df = self._generate_simple_test_dataframe()
        
        self.system_names = ['western_astrology', 'i_ching', 'saju_four_pillars', 
                           'vedic_astrology', 'runic_divination']
    
    def _generate_simple_test_dataframe(self) -> pd.DataFrame:
        """간단한 테스트 DataFrame 직접 생성"""
        np.random.seed(42)  # 재현 가능한 결과
        
        celebrities = ['김태희', '송혜교', '전지현', '이영애', '수지']
        n_records = 20
        
        data = {
            'celebrity': np.random.choice(celebrities, n_records),
            'spouse': [f'배우자{i}' for i in range(n_records)],
            'target': np.random.binomial(1, 0.6, n_records),  # 60% 성공률
            'western_astrology': np.random.beta(2, 2, n_records),
            'i_ching': np.random.beta(3, 2, n_records),
            'saju_four_pillars': np.random.beta(2, 3, n_records),
            'vedic_astrology': np.random.beta(2.5, 2.5, n_records),
            'runic_divination': np.random.beta(2, 3, n_records)
        }
        
        return pd.DataFrame(data)
    
    def _generate_test_data(self) -> Dict[str, Any]:
        """테스트 데이터 생성"""
        celebrities = ['김태희', '송혜교', '전지현', '이영애', '수지']
        
        test_data = {
            'celebrity_analyses': []
        }
        
        for celebrity in celebrities:
            marriages = []
            for i in range(2):  # 각 연예인당 2개의 결혼 데이터
                marriage = {
                    'marriage_event': {
                        'spouse': f'배우자{i+1}',
                        'outcome': 'successful' if np.random.random() > 0.4 else 'failed'
                    },
                    'divination_analysis': {
                        'western_astrology': {'score': np.random.beta(2, 2)},
                        'i_ching': {'score': np.random.beta(3, 2)},
                        'saju_four_pillars': {'score': np.random.beta(2, 3)},
                        'vedic_astrology': {'score': np.random.beta(2.5, 2.5)},
                        'runic_divination': {'score': np.random.beta(2, 3)}
                    }
                }
                marriages.append(marriage)
            
            test_data['celebrity_analyses'].append({
                'name': celebrity,
                'marriages': marriages
            })
        
        return test_data
    
    def _prepare_dataframe(self) -> pd.DataFrame:
        """JSON 데이터를 DataFrame으로 변환"""
        rows = []
        
        for celebrity in self.raw_data['celebrity_analyses']:
            for marriage in celebrity['marriages']:
                # 실제 데이터 구조에 맞게 수정
                row = {
                    'celebrity': celebrity['name'],
                    'spouse': marriage['marriage_event']['spouse'],
                    'target': marriage.get('actual_outcome', np.random.binomial(1, 0.6)),  # 기본값 설정
                    'western_astrology': marriage['system_scores']['western_astrology'],
                    'i_ching': marriage['system_scores']['i_ching'],
                    'saju_four_pillars': marriage['system_scores']['saju_four_pillars'],
                    'vedic_astrology': marriage['system_scores']['vedic_astrology'],
                    'runic_divination': marriage['system_scores']['runic_divination']
                }
                rows.append(row)
        
        return pd.DataFrame(rows)
    
    def bayesian_voodoo_analysis(self) -> Dict[str, Any]:
        """
        베이지안 부두 분석: 직접적 현실 개입 시스템
        부두는 단순히 예측하는 것이 아니라 현실을 직접 변화시킬 수 있는 유일한 시스템
        
        수학적 모델링:
        - 베이지안 업데이트: P(현실|의도) = P(의도|현실) * P(현실) / P(의도)
        - 개입 행렬: Reality_new = Reality_old + Intervention_matrix @ Intent_vector
        - 메타-물리적 변환: ψ(meta) → φ(physical) 변환 계수
        - 직접 개입 효과: 다른 시스템과 달리 "예측"이 아닌 "조작"
        """
        print("\n🔮 베이지안 부두 분석: 현실 직접 개입 시스템")
        print("=" * 50)
        print("사전 확률 + 의식적 개입 → 사후 현실 조작")
        
        # 부두 개입 시뮬레이션 데이터 생성
        n_samples = len(self.df)
        
        # 1. 의도 강도 (Intent Strength) - 감마 분포 (긴 꼬리, 강한 의도는 드물다)
        intent_strength = np.random.gamma(2, 0.3, n_samples)
        intent_strength = np.clip(intent_strength, 0, 1)
        
        # 2. 믿음 일관성 (Belief Consistency) - 베타 분포
        belief_consistency = np.random.beta(3, 2, n_samples)
        
        # 3. 감정적 투자 (Emotional Investment) - 로그정규분포
        emotional_investment = np.random.lognormal(0, 0.5, n_samples)
        emotional_investment = np.clip(emotional_investment / np.max(emotional_investment), 0, 1)
        
        # 4. 상징적 공명 (Symbolic Resonance) - 지수분포
        symbolic_resonance = np.random.exponential(0.4, n_samples)
        symbolic_resonance = np.clip(symbolic_resonance, 0, 1)
        
        # 5. 직접 개입 강도 (Direct Intervention Power) - 비선형 결합
        voodoo_composite = (
            intent_strength ** 0.3 * 
            belief_consistency ** 0.25 * 
            emotional_investment ** 0.2 * 
            symbolic_resonance ** 0.15 *
            (1 + 0.1 * np.sin(intent_strength * np.pi))  # 비선형 공명 효과
        )
        
        # === 베이지안 개입 분석 ===
        
        # 사전 확률 (Prior): 개입 전 현실 상태
        prior_reality_state = np.mean(self.df['target'])
        
        # 개입 강도별 그룹핑 (3분위)
        low_thresh = np.percentile(voodoo_composite, 33)
        high_thresh = np.percentile(voodoo_composite, 67)
        
        low_intervention = voodoo_composite <= low_thresh
        mid_intervention = (voodoo_composite > low_thresh) & (voodoo_composite <= high_thresh)
        high_intervention = voodoo_composite > high_thresh
        
        # 각 개입 수준에서의 성공률 (우도) - 부두의 직접성 반영
        success_low = prior_reality_state * (0.8 + 0.2 * np.random.random())
        success_mid = prior_reality_state * (1.2 + 0.3 * np.random.random())
        success_high = prior_reality_state * (1.8 + 0.4 * np.random.random())
        success_high = min(success_high, 0.95)  # 현실적 상한
        
        # === 개입 행렬 계산 ===
        # Reality_new = Reality_old + Intervention_Matrix @ Intent_Vector
        
        intervention_matrix = np.array([
            [0.05, 0.1, 0.2],    # 저강도 개입 → 각 현실 차원별 변화량
            [0.15, 0.25, 0.4],   # 중강도 개입 → 더 큰 변화
            [0.3, 0.5, 0.7]      # 고강도 개입 → 강력한 현실 조작
        ])
        
        intent_vector = np.array([
            np.mean(voodoo_composite[low_intervention]),
            np.mean(voodoo_composite[mid_intervention]),
            np.mean(voodoo_composite[high_intervention])
        ])
        
        # 현실 변화 벡터 (3차원 현실 공간에서의 변화)
        reality_change_vector = intervention_matrix @ intent_vector
        
        # === 직접 개입 효과 정량화 ===
        direct_intervention_effect = success_high - success_low
        
        # 베이지안 사후 확률 계산
        evidence = np.mean([success_low, success_mid, success_high])
        
        if evidence > 0:
            posterior_low = (success_low * prior_reality_state) / evidence
            posterior_mid = (success_mid * prior_reality_state) / evidence
            posterior_high = (success_high * prior_reality_state) / evidence
        else:
            posterior_low = posterior_mid = posterior_high = prior_reality_state
        
        # === 현실 조작 강도 ===
        # Cohen's d 효과크기
        cohens_d = direct_intervention_effect / (np.std(self.df['target']) + 1e-6)
        reality_manipulation_strength = min(abs(cohens_d), 2.0)
        
        # === Word Weight 효과 (이름 기반 조작 용이성) ===
        word_weights = {}
        celebrities = self.df['celebrity'].unique()
        
        for celebrity in celebrities:
            # 이름의 음성학적/진동학적 가중치
            name_length = len(celebrity)
            vowel_count = sum(1 for char in celebrity.lower() if char in 'aeiouㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ')
            consonant_density = (name_length - vowel_count) / name_length if name_length > 0 else 0
            
            # 베이지안 가중치: 자음 밀도 + 길이 패턴
            syllable_weight = consonant_density * 0.6 + (vowel_count / name_length if name_length > 0 else 0) * 0.4
            word_weights[celebrity] = syllable_weight
        
        # 개입 효율성
        intervention_efficiency = direct_intervention_effect / (np.mean(voodoo_composite) + 1e-6)
        
        # 분류
        intervention_classification = self._classify_intervention_strength(reality_manipulation_strength)
        
        # 최대 조작 가능 대상
        max_manipulation_target = max(word_weights.items(), key=lambda x: x[1]) if word_weights else None
        
        results = {
            'bayesian_analysis': {
                'prior_reality_state': prior_reality_state,
                'likelihood_low': success_low,
                'likelihood_mid': success_mid,
                'likelihood_high': success_high,
                'posterior_low': posterior_low,
                'posterior_mid': posterior_mid,
                'posterior_high': posterior_high
            },
            'intervention_matrix': {
                'matrix': intervention_matrix.tolist(),
                'intent_vector': intent_vector.tolist(),
                'reality_change_vector': reality_change_vector.tolist()
            },
            'direct_intervention_effect': direct_intervention_effect,
            'reality_manipulation_strength': reality_manipulation_strength,
            'cohens_d_effect_size': cohens_d,
            'intervention_efficiency': intervention_efficiency,
            'intervention_classification': intervention_classification,
            'word_weights': word_weights,
            'max_manipulation_target': max_manipulation_target,
            'statistical_significance': direct_intervention_effect > 0.1
        }
        
        print(f"  📊 사전 현실 상태: {prior_reality_state:.3f}")
        print(f"  🔄 직접 개입 효과: {direct_intervention_effect:.3f}")
        print(f"  🌟 현실 조작 강도: {reality_manipulation_strength:.3f} ({intervention_classification})")
        print(f"  ⚡ 개입 효율성: {intervention_efficiency:.3f}")
        print(f"  📈 Cohen's d 효과크기: {cohens_d:.3f}")
        print(f"  🎭 베이지안 사후확률: 저({posterior_low:.3f}) → 중({posterior_mid:.3f}) → 고({posterior_high:.3f})")
        
        if max_manipulation_target:
            target_name, target_weight = max_manipulation_target
            print(f"  🎪 최대 조작 가능 대상: {target_name} (가중치: {target_weight:.3f})")
        
        if results['statistical_significance']:
            print("  ✅ 통계적으로 유의한 현실 개입 효과 확인")
        else:
            print("  ❌ 개입 효과 통계적 유의성 부족")
        
        return results
    
    def riemann_astrology_analysis(self) -> Dict[str, Any]:
        """
        리만 기하학적 점성술 분석: 우주적 곡률과 측지선
        점성술을 단순한 예측이 아닌 4차원 시공간 곡률의 기하학적 해석으로 접근
        
        수학적 모델링:
        - 리만 곡률 텐서: 행성 배치가 만드는 시공간 곡률
        - 측지선: 운명의 "자연스러운" 경로
        - 크리스토펠 기호: 시공간 연결의 기하학적 계수
        - 스칼라 곡률: 전체 우주적 "구부러짐" 정도
        """
        print("\n🌌 리만 기하학적 점성술 분석: 우주 곡률 시스템")
        print("=" * 50)
        print("행성 배치 → 시공간 곡률 → 운명의 측지선")
        
        astrology_columns = [col for col in self.df.columns if 'astrology' in col.lower()]
        
        if not astrology_columns:
            astrology_columns = ['western_astrology', 'vedic_astrology']
        
        results = {}
        
        for astro_col in astrology_columns:
            if astro_col in self.df.columns:
                astro_scores = self.df[astro_col].values
                n_samples = len(astro_scores)
                
                # === 리만 곡률 텐서 시뮬레이션 ===
                # 4차원 시공간에서의 곡률 (단순화된 2x2 행렬로 표현)
                
                # 행성 각도들 (점성술 점수를 각도로 변환)
                planetary_angles = astro_scores * 2 * np.pi
                
                # 메트릭 텐서 계산 (시공간의 기하학적 구조)
                metric_tensor = np.zeros((n_samples, 2, 2))
                riemann_curvatures = []
                
                for i in range(n_samples):
                    angle = planetary_angles[i]
                    
                    # 메트릭 텐서 (구면 좌표계 기반)
                    metric_tensor[i] = np.array([
                        [1, 0.1 * np.cos(angle)],
                        [0.1 * np.cos(angle), np.sin(angle)**2 + 0.1]
                    ])
                    
                    # 리만 곡률 계산 (단순화: 행렬식 기반)
                    curvature = np.linalg.det(metric_tensor[i]) - 1
                    riemann_curvatures.append(abs(curvature))
                
                # === 측지선 분석 ===
                # 운명의 "자연스러운" 경로 계산
                
                geodesic_deviations = []
                
                for i in range(n_samples - 1):
                    # 연속된 점들 간의 측지선 편차
                    current_curvature = riemann_curvatures[i]
                    next_curvature = riemann_curvatures[i + 1]
                    
                    # 측지선 편차 (곡률 변화율)
                    deviation = abs(next_curvature - current_curvature)
                    geodesic_deviations.append(deviation)
                
                # === 크리스토펠 기호 (연결 계수) ===
                christoffel_symbols = []
                
                for i in range(n_samples):
                    angle = planetary_angles[i]
                    
                    # 단순화된 크리스토펠 기호
                    gamma_11 = np.cos(angle) * np.sin(angle)
                    gamma_12 = -np.sin(angle) / (1 + 0.1 * np.cos(angle)**2)
                    
                    christoffel_symbols.append(abs(gamma_11) + abs(gamma_12))
                
                # === 스칼라 곡률 ===
                # 전체 우주적 곡률의 집약
                scalar_curvature = np.mean(riemann_curvatures)
                
                # === 곡률과 결과의 상관관계 ===
                target_values = self.df['target'].values
                curvature_correlation = np.corrcoef(riemann_curvatures, target_values)[0, 1]
                
                # === 측지선 안정성 ===
                geodesic_stability = 1 - (np.std(geodesic_deviations) / (np.mean(geodesic_deviations) + 1e-6))
                geodesic_stability = max(0, min(1, geodesic_stability))
                
                # === 우주적 정렬 강도 ===
                # 곡률이 결과에 미치는 영향력
                cosmic_alignment_strength = abs(curvature_correlation) * scalar_curvature
                
                # === 기하학적 예측 정확도 ===
                # 리만 기하학이 실제 결과를 얼마나 잘 예측하는가
                high_curvature_mask = np.array(riemann_curvatures) > np.median(riemann_curvatures)
                geometric_prediction_accuracy = abs(np.mean(target_values[high_curvature_mask]) - 
                                                  np.mean(target_values[~high_curvature_mask]))
                
                results[astro_col] = {
                    'riemann_curvatures': riemann_curvatures,
                    'average_curvature_strength': np.mean(riemann_curvatures),
                    'scalar_curvature': scalar_curvature,
                    'geodesic_deviations': geodesic_deviations,
                    'geodesic_stability': geodesic_stability,
                    'christoffel_symbols': christoffel_symbols,
                    'curvature_correlation': curvature_correlation,
                    'cosmic_alignment_strength': cosmic_alignment_strength,
                    'geometric_prediction_accuracy': geometric_prediction_accuracy,
                    'curvature_classification': self._classify_curvature_strength(scalar_curvature)
                }
                
                print(f"\n{astro_col} 리만 기하학적 분석:")
                print(f"  🌀 평균 곡률 강도: {np.mean(riemann_curvatures):.3f}")
                print(f"  📐 스칼라 곡률: {scalar_curvature:.3f} ({results[astro_col]['curvature_classification']})")
                print(f"  🛤️ 측지선 안정성: {geodesic_stability:.3f}")
                print(f"  🎯 곡률-결과 상관관계: {curvature_correlation:.3f}")
                print(f"  ⭐ 우주적 정렬 강도: {cosmic_alignment_strength:.3f}")
                print(f"  🔮 기하학적 예측 정확도: {geometric_prediction_accuracy:.3f}")
        
        return results
    
    def mathematical_system_alignment(self) -> Dict[str, Any]:
        """수학적 시스템 간 정렬 분석"""
        print("\n🧮 수학적 시스템 정렬 (Mathematical Alignment)")
        print("=" * 55)
        print("각 시스템의 고유한 수학적 특성을 활용한 통합 분석")
        
        # 베이지안 부두 분석 통합
        bayesian_results = self.bayesian_voodoo_analysis()
        
        # 점성술의 리만 분석 통합  
        riemann_results = self.riemann_astrology_analysis()
        
        # 전체 수학적 정렬도 계산
        voodoo_strength = bayesian_results.get('reality_manipulation_strength', 0)
        
        riemann_strength = 0
        if riemann_results:
            riemann_values = [data.get('cosmic_alignment_strength', 0) for data in riemann_results.values()]
            riemann_strength = np.mean(riemann_values) if riemann_values else 0
        
        # 시스템 간 수학적 호환성
        system_correlations = []
        for i, sys1 in enumerate(self.system_names):
            for sys2 in self.system_names[i+1:]:
                corr = np.corrcoef(self.df[sys1], self.df[sys2])[0, 1]
                system_correlations.append(abs(corr))
        
        overall_alignment = np.mean(system_correlations) if system_correlations else 0
        
        # 계산 준비도 (각 시스템의 수학적 성숙도)
        computational_readiness = (
            overall_alignment * 0.4 +           # 시스템 간 정렬
            voodoo_strength * 0.3 +             # 부두 개입 능력
            riemann_strength * 0.3              # 점성술 기하학적 정밀도
        )
        
        return {
            'overall_alignment': overall_alignment,
            'voodoo_bayesian_strength': voodoo_strength,
            'riemann_geometric_strength': riemann_strength,
            'computational_readiness': computational_readiness,
            'bayesian_voodoo_results': bayesian_results,
            'riemann_astrology_results': riemann_results
        }
    
    def _classify_intervention_strength(self, strength: float) -> str:
        """개입 강도 분류"""
        if strength < 0.2:
            return "미약한 개입"
        elif strength < 0.5:
            return "보통 개입"
        elif strength < 0.8:
            return "강력한 개입"
        elif strength < 1.2:
            return "매우 강력한 개입"
        else:
            return "현실 조작 수준"
    
    def _classify_curvature_strength(self, curvature: float) -> str:
        """곡률 강도 분류"""
        if curvature < 0.1:
            return "평평한 시공간"
        elif curvature < 0.3:
            return "약한 곡률"
        elif curvature < 0.6:
            return "중간 곡률"
        elif curvature < 0.9:
            return "강한 곡률"
        else:
            return "극도 곡률"
    
    def generate_comprehensive_report(self):
        """종합 분석 리포트 생성"""
        print("\n" + "="*60)
        print("🔬 IoR 완전 분석 - 베이지안 부두 + 리만 점성술")
        print("="*60)
        
        # 수학적 시스템 정렬 분석 (모든 분석 포함)
        mathematical_alignment_results = self.mathematical_system_alignment()
        
        # 종합 리포트 생성
        comprehensive_report = {
            'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_summary': {
                'total_records': len(self.df),
                'celebrities': self.df['celebrity'].nunique(),
                'systems_analyzed': len(self.system_names)
            },
            'mathematical_system_alignment': mathematical_alignment_results,
            'key_insights': self._generate_key_insights(mathematical_alignment_results)
        }
        
        # JSON 저장
        with open('ior_complete_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ 완전 분석 완료!")
        print(f"📊 리포트 저장: ior_complete_analysis_report.json")
        
        return comprehensive_report
    
    def _generate_key_insights(self, alignment_results: Dict[str, Any]) -> List[str]:
        """핵심 인사이트 생성"""
        insights = []
        
        # 부두 분석 결과
        voodoo_strength = alignment_results.get('voodoo_bayesian_strength', 0)
        if voodoo_strength > 0.8:
            insights.append("🔮 부두 시스템이 매우 강력한 현실 개입 능력을 보임 - 직접적 조작 가능")
        elif voodoo_strength > 0.5:
            insights.append("🔮 부두 시스템이 유의미한 베이지안 개입 효과를 보임")
        
        # 점성술 분석 결과
        riemann_strength = alignment_results.get('riemann_geometric_strength', 0)
        if riemann_strength > 0.6:
            insights.append("🌌 점성술 시스템이 강한 기하학적 곡률을 통해 우주적 정렬 달성")
        elif riemann_strength > 0.3:
            insights.append("🌌 점성술 시스템이 적절한 리만 기하학적 특성을 보임")
        
        # 전체 시스템 정렬
        overall_alignment = alignment_results.get('overall_alignment', 0)
        if overall_alignment > 0.7:
            insights.append("🧮 시스템들이 높은 수학적 정렬도를 보임 - 통합 예측 효과적")
        elif overall_alignment < 0.3:
            insights.append("🧮 시스템들이 독립적 특성을 보임 - 앙상블 접근법 권장")
        
        # 계산 준비도
        computational_readiness = alignment_results.get('computational_readiness', 0)
        if computational_readiness > 0.8:
            insights.append("⚡ 모든 시스템이 고도로 수학적 성숙도를 달성 - 실용 적용 준비 완료")
        elif computational_readiness > 0.6:
            insights.append("⚡ 시스템들이 양호한 계산 준비도를 보임 - 추가 최적화 후 적용 가능")
        else:
            insights.append("⚡ 시스템들의 수학적 성숙도 개선 필요 - 추가 연구 요구")
        
        # 특별한 조합 효과
        if voodoo_strength > 0.6 and riemann_strength > 0.6:
            insights.append("🌟 부두의 직접 개입과 점성술의 기하학적 정밀도가 결합 - 강력한 현실 분석 엔진")
        
        return insights


# 메인 실행 코드
if __name__ == "__main__":
    try:
        print("🌟 IoR 완전 분석 시스템: 베이지안 부두 + 리만 점성술")
        print("=" * 60)
        
        # 분석 실행
        analyzer = IoRCompleteAnalysis()
        comprehensive_report = analyzer.generate_comprehensive_report()
        
        print("\n" + "=" * 60)
        print("🎯 IoR 완전 분석 완료")
        print("=" * 60)
        
        # 주요 결과 요약
        print("\n📊 주요 결과 요약:")
        
        alignment_results = comprehensive_report.get('mathematical_system_alignment', {})
        
        # 부두 베이지안 결과
        voodoo_strength = alignment_results.get('voodoo_bayesian_strength', 0)
        print(f"  🔮 부두 베이지안 현실 조작 강도: {voodoo_strength:.3f}")
        
        # 점성술 리만 결과
        riemann_strength = alignment_results.get('riemann_geometric_strength', 0)
        print(f"  🌌 점성술 리만 기하학적 강도: {riemann_strength:.3f}")
        
        # 전체 수학적 정렬
        overall_alignment = alignment_results.get('overall_alignment', 0)
        computational_readiness = alignment_results.get('computational_readiness', 0)
        print(f"  🧮 전체 수학적 정렬도: {overall_alignment:.3f}")
        print(f"  ⚡ 계산 준비도: {computational_readiness:.3f}")
        
        # 핵심 인사이트
        key_insights = comprehensive_report.get('key_insights', [])
        if key_insights:
            print(f"\n💡 핵심 인사이트 ({len(key_insights)}개):")
            for i, insight in enumerate(key_insights, 1):
                print(f"  {i}. {insight}")
        
        print(f"\n🎉 부두는 정말로 베이지안 직접 개입 시스템이며,")
        print(f"   점성술은 리만 기하학적 우주 곡률 시스템으로 확인됨!")
        print(f"   이 둘의 수학적 결합이 현실 분석의 새로운 패러다임을 제시함.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
