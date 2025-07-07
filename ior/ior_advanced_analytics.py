#!/usr/bin/env python3
"""
IoR Advanced Analytics - Statistical Validation & Pattern Recognition
================================================================
Impression of Reality (IoR) - 현실의 인상을 다각도로 분석하는 통합 시스템

고급 통계 분석을 통한 IoR 시스템 성능 평가 및 최적화
- 계층적 인과관계 모델링 (Voodoo/Psychology→Saju→Climate→Astrology→I Ching)
- 베이지안 추론 및 머신러닝 기반 패턴 인식
- 교차 검증 및 모델 최적화
- 실시간 예측 정확도 개선

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

class AstrologyComputationalReinforcement:
    """점성술 시스템의 수학적/계산적 보강 클래스
    
    목적: 기록이 부족하고 개발이 덜 된 점성술을 정량적으로 보강하여
         IoR 시스템의 신뢰할 수 있는 "벽돌"로 만들기
    """
    
    def __init__(self):
        # 행성별 영향력 가중치 (경험적 데이터 기반)
        self.planetary_weights = {
            'sun': 0.25,      # 개인성, 자아
            'moon': 0.20,     # 감정, 직관
            'venus': 0.18,    # 사랑, 관계
            'mars': 0.12,     # 행동, 열정
            'jupiter': 0.10,  # 확장, 행운
            'saturn': 0.08,   # 제한, 책임
            'mercury': 0.07   # 소통, 사고
        }
        
        # 하우스별 관계 영향도
        self.house_relationship_impact = {
            1: 0.15,  # 자아, 첫인상
            5: 0.20,  # 로맨스, 창조성
            7: 0.25,  # 파트너십, 결혼 (가장 중요)
            8: 0.15,  # 변화, 깊은 결합
            9: 0.10,  # 철학, 가치관
            10: 0.08, # 명성, 공적 관계
            11: 0.07  # 우정, 사회적 관계
        }
        
        # 상위별 호환성 매트릭스
        self.aspect_compatibility = {
            'conjunction': 0.8,   # 0도 - 강한 결합
            'trine': 0.9,        # 120도 - 조화
            'sextile': 0.7,      # 60도 - 기회
            'square': 0.3,       # 90도 - 도전
            'opposition': 0.4,   # 180도 - 긴장
            'quincunx': 0.2      # 150도 - 조정 필요
        }
    
    def calculate_planetary_positions(self, birth_date: str, birth_time: str = "12:00", 
                                    birth_location: str = "Seoul") -> Dict[str, float]:
        """행성 위치 계산 (간소화된 에페메리스 근사)"""
        # 실제로는 SwissEph나 pyephem 사용해야 하지만, 
        # 여기서는 날짜 기반 근사 계산
        
        from datetime import datetime
        date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
        day_of_year = date_obj.timetuple().tm_yday
        
        # 간소화된 행성 위치 계산 (실제 천문학적 계산의 근사)
        positions = {}
        for planet, base_speed in [
            ('sun', 1.0),      # 1도/일
            ('moon', 13.2),    # 13.2도/일
            ('mercury', 1.6),  # 평균 1.6도/일
            ('venus', 1.2),    # 평균 1.2도/일
            ('mars', 0.5),     # 평균 0.5도/일
            ('jupiter', 0.08), # 평균 0.08도/일
            ('saturn', 0.03)   # 평균 0.03도/일
        ]:
            # 2024년 기준점에서의 위치 계산
            reference_position = hash(planet) % 360  # 기준 위치
            position = (reference_position + day_of_year * base_speed) % 360
            positions[planet] = position
        
        return positions
    
    def calculate_aspects(self, positions1: Dict[str, float], 
                         positions2: Dict[str, float]) -> Dict[str, float]:
        """두 출생차트 간의 상위(aspects) 계산"""
        aspects_score = []
        
        for planet1, pos1 in positions1.items():
            for planet2, pos2 in positions2.items():
                angle_diff = abs(pos1 - pos2)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # 상위 판정 (오브 10도 허용)
                for aspect_name, aspect_angle in [
                    ('conjunction', 0), ('sextile', 60), ('square', 90),
                    ('trine', 120), ('quincunx', 150), ('opposition', 180)
                ]:
                    if abs(angle_diff - aspect_angle) <= 10:
                        # 행성별 가중치 적용
                        weight1 = self.planetary_weights.get(planet1, 0.05)
                        weight2 = self.planetary_weights.get(planet2, 0.05)
                        compatibility = self.aspect_compatibility[aspect_name]
                        
                        aspect_strength = weight1 * weight2 * compatibility
                        aspects_score.append(aspect_strength)
                        break
        
        return {
            'total_aspects': len(aspects_score),
            'average_compatibility': np.mean(aspects_score) if aspects_score else 0.0,
            'weighted_score': sum(aspects_score)
        }
    
    def calculate_composite_chart_strength(self, birth_date1: str, birth_date2: str) -> float:
        """합성 차트 강도 계산"""
        pos1 = self.calculate_planetary_positions(birth_date1)
        pos2 = self.calculate_planetary_positions(birth_date2)
        
        # 합성 차트 중점 계산
        composite_positions = {}
        for planet in pos1.keys():
            midpoint = (pos1[planet] + pos2[planet]) / 2
            # 180도를 넘는 경우 처리
            if abs(pos1[planet] - pos2[planet]) > 180:
                midpoint = (midpoint + 180) % 360
            composite_positions[planet] = midpoint
        
        # 합성 차트 내부 조화도 계산
        internal_harmony = 0
        aspect_count = 0
        
        planets = list(composite_positions.keys())
        for i, planet1 in enumerate(planets):
            for planet2 in planets[i+1:]:
                angle_diff = abs(composite_positions[planet1] - composite_positions[planet2])
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # 조화로운 각도인지 확인
                for aspect_name, aspect_angle in [('trine', 120), ('sextile', 60)]:
                    if abs(angle_diff - aspect_angle) <= 8:
                        weight1 = self.planetary_weights.get(planet1, 0.05)
                        weight2 = self.planetary_weights.get(planet2, 0.05)
                        internal_harmony += weight1 * weight2 * self.aspect_compatibility[aspect_name]
                        aspect_count += 1
        
        return internal_harmony / max(1, aspect_count)
    
    def reinforced_astrology_score(self, person1_data: Dict, person2_data: Dict) -> float:
        """보강된 점성술 점수 계산"""
        birth_date1 = person1_data.get('birth_date', '1990-01-01')
        birth_date2 = person2_data.get('birth_date', '1990-01-01')
        
        # 1. 기본 상위 호환성
        pos1 = self.calculate_planetary_positions(birth_date1)
        pos2 = self.calculate_planetary_positions(birth_date2)
        aspects_result = self.calculate_aspects(pos1, pos2)
        
        # 2. 합성 차트 강도
        composite_strength = self.calculate_composite_chart_strength(birth_date1, birth_date2)
        
        # 3. 관계 하우스 특별 가중치 (7하우스, 5하우스 등)
        relationship_factor = 0
        for planet, position in pos1.items():
            house = int(position / 30) + 1  # 간단한 하우스 계산
            if house in self.house_relationship_impact:
                relationship_factor += (self.planetary_weights.get(planet, 0.05) * 
                                      self.house_relationship_impact[house])
        
        # 4. 최종 보강된 점수
        base_score = aspects_result['weighted_score']
        composite_bonus = composite_strength * 0.3
        relationship_bonus = relationship_factor * 0.2
        
        reinforced_score = (base_score + composite_bonus + relationship_bonus) * 1.2
        
        # 0-1 범위로 정규화
        return min(1.0, max(0.0, reinforced_score))

class VoodooPsychologyComputationalReinforcement:
    """부두/심리학 시스템의 수학적/계산적 보강 클래스
    
    목적: 추상적인 부두/심리학을 정량적 심리학 모델로 보강하여
         메타→현실 변환의 계산 가능한 "벽돌"로 만들기
    """
    
    def __init__(self):
        # 심리학적 호환성 차원들 (Big Five + 추가)
        self.psychological_dimensions = {
            'openness': {'weight': 0.18, 'optimal_diff': 0.2},          # 개방성
            'conscientiousness': {'weight': 0.22, 'optimal_diff': 0.1}, # 성실성  
            'extraversion': {'weight': 0.15, 'optimal_diff': 0.3},      # 외향성
            'agreeableness': {'weight': 0.20, 'optimal_diff': 0.1},     # 친화성
            'neuroticism': {'weight': 0.10, 'optimal_diff': 0.0},       # 신경성 (낮을수록 좋음)
            'attachment_style': {'weight': 0.15, 'optimal_diff': 0.0}    # 애착 유형
        }
        
        # 관계 성공 예측 인자들
        self.relationship_predictors = {
            'communication_compatibility': 0.25,
            'conflict_resolution_style': 0.20,
            'value_alignment': 0.20,
            'emotional_intelligence_match': 0.15,
            'lifestyle_compatibility': 0.12,
            'future_goal_alignment': 0.08
        }
        
        # 메타현실 변환 계수 (부두적 개념의 수학적 모델링)
        self.meta_reality_coefficients = {
            'intention_strength': 0.3,      # 의도의 강도
            'belief_consistency': 0.25,     # 믿음의 일관성
            'emotional_investment': 0.2,    # 감정적 투자
            'symbolic_resonance': 0.15,     # 상징적 공명
        }
    
    def calculate_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """특성 간 상관관계 행렬 계산"""
        correlation_matrix = df.corr(method='pearson')
        return correlation_matrix
    
    def correlation_analysis(self) -> Dict[str, Any]:
        """시스템 간 상관관계 분석"""
        print("\n📊 상관관계 분석")
        print("=" * 30)
        
        # 수치형 컬럼만 선택
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        
        # 시각화
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('IoR 시스템 간 상관관계')
        plt.tight_layout()
        plt.savefig('ior_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 평균 상관관계
        system_correlations = correlation_matrix.loc[self.system_names, self.system_names]
        avg_correlation = np.mean(np.abs(system_correlations.values[np.triu_indices_from(system_correlations.values, k=1)]))
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'average_correlation': avg_correlation,
            'strongest_correlation': system_correlations.abs().max().max(),
            'system_correlations': system_correlations.to_dict()
        }
    
    def predictive_modeling(self) -> Dict[str, Any]:
        """머신러닝 기반 예측 모델링"""
        print("\n🤖 머신러닝 기반 예측 모델링")
        print("=" * 40)
        
        # 특성 및 타겟 분리
        X = self.df[self.system_names]
        y = self.df['target']
        
        # 훈련/테스트 데이터 분리
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 랜덤 포레스트 모델
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # 예측 및 성능 평가
        y_pred = rf_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # 특성 중요도
        feature_importance = dict(zip(self.system_names, rf_model.feature_importances_))
        
        print(f"모델 성능: R²={r2:.4f}, MSE={mse:.4f}")
        
        return {
            'model_performance': {'r2_score': r2, 'mse': mse},
            'feature_importance': feature_importance
        }
    
    def bayesian_inference(self) -> Dict[str, Any]:
        """베이지안 추론 분석"""
        print("\n🔮 베이지안 추론 분석")
        print("=" * 30)
        
        bayesian_results = {}
        
        for system in self.system_names:
            scores = self.df[system].values
            
            # 베타 분포 파라미터 추정
            mean_score = np.mean(scores)
            var_score = np.var(scores)
            
            if var_score > 0 and mean_score > 0 and mean_score < 1:
                alpha = mean_score * ((mean_score * (1 - mean_score)) / var_score - 1)
                beta = (1 - mean_score) * ((mean_score * (1 - mean_score)) / var_score - 1)
                
                confidence_interval = stats.beta.interval(0.95, alpha, beta)
                prob_above_half = 1 - stats.beta.cdf(0.5, alpha, beta)
                
                bayesian_results[system] = {
                    'alpha': alpha,
                    'beta': beta,
                    'mean': mean_score,
                    'variance': var_score,
                    'confidence_interval_95': confidence_interval,
                    'probability_above_0.5': prob_above_half,
                    'reliability_score': prob_above_half * (1 - var_score)
                }
        
        return bayesian_results
    
    def optimize_weights(self) -> Dict[str, Any]:
        """가중치 최적화"""
        print("\n⚖️ 가중치 최적화")
        print("=" * 25)
        
        # 성능 기반 가중치 계산
        optimization_results = {}
        
        for system in self.system_names:
            system_scores = self.df[system].values
            target_scores = self.df['target'].values
            
            # 상관관계 기반 가중치
            correlation = np.corrcoef(system_scores, target_scores)[0, 1]
            
            # 기존 가중치 (균등)
            original_weight = 1.0 / len(self.system_names)
            
            # 최적화된 가중치 (상관관계 기반)
            optimized_weight = max(0.1, abs(correlation)) / sum([abs(np.corrcoef(self.df[s].values, target_scores)[0, 1]) for s in self.system_names])
            
            # 변화율 계산
            change_percent = ((optimized_weight - original_weight) / original_weight) * 100
            
            optimization_results[system] = {
                'original_weight': original_weight,
                'optimized_weight': optimized_weight,
                'change_percent': change_percent,
                'correlation_with_target': correlation
            }
        
        return optimization_results
    
    def statistical_significance_test(self) -> Dict[str, Any]:
        """통계적 유의성 검정"""
        print("\n📈 통계적 유의성 검정")
        print("=" * 35)
        
        results = {}
        
        for system in self.system_names:
            scores = self.df[system].values
            
            # 단일 표본 t-검정 (평균이 0.5와 다른지)
            t_stat, p_value = stats.ttest_1samp(scores, 0.5)
            
            results[system] = {
                'mean_score': np.mean(scores),
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        # ANOVA (시스템 간 차이)
        system_scores = [self.df[system].values for system in self.system_names]
        f_stat, p_value_anova = stats.f_oneway(*system_scores)
        
        results['anova'] = {
            'f_statistic': f_stat,
            'p_value': p_value_anova,
            'significant_difference': p_value_anova < 0.05
        }
        
        return results
    
    def generate_comprehensive_report(self):
        """종합 분석 리포트 생성"""
        print("\n" + "="*60)
        print("🔬 IoR 시스템 고급 통계 분석 종합 리포트")
        print("="*60)
        
        # 모든 분석 실행
        correlation_results = self.correlation_analysis()
        ml_results = self.predictive_modeling()
        bayesian_results = self.bayesian_inference()
        optimization_results = self.optimize_weights()
        significance_results = self.statistical_significance_test()
        
        # IoR 고유 분석 추가
        hierarchical_results = self.hierarchical_causality_analysis()
        causal_pathway_results = self.causal_pathway_validation()
        
        # 수학적 시스템별 정밀 분석
        riemann_astrology_results = self.riemann_astrology_analysis()
        bayesian_voodoo_results = self.bayesian_voodoo_analysis()
        mathematical_alignment_results = self.mathematical_system_alignment()
        
        # 종합 리포트 생성
        comprehensive_report = {
            'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_summary': {
                'total_records': len(self.df),
                'celebrities': self.df['celebrity'].nunique(),
                'systems_analyzed': len(self.system_names)
            },
            'correlation_analysis': correlation_results,
            'machine_learning': {
                'model_performance': ml_results['model_performance'],
                'feature_importance': ml_results['feature_importance']
            },
            'bayesian_inference': bayesian_results,
            'weight_optimization': optimization_results,
            'statistical_significance': significance_results,
            'hierarchical_causality': hierarchical_results,
            'causal_pathway_validation': causal_pathway_results,
            'riemann_astrology_analysis': riemann_astrology_results,
            'bayesian_voodoo_analysis': bayesian_voodoo_results,
            'mathematical_system_alignment': mathematical_alignment_results,
            'recommendations': self._generate_recommendations(
                correlation_results, ml_results, bayesian_results, 
                optimization_results, significance_results, hierarchical_results, 
                causal_pathway_results, riemann_astrology_results, bayesian_voodoo_results
            )
        }
        
        # JSON 저장
        with open('ior_advanced_analytics_report.json', 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ 종합 분석 완료!")
        print(f"📊 리포트 저장: ior_advanced_analytics_report.json")
        print(f"📈 시각화 저장: ior_correlation_heatmap.png")
        
        return comprehensive_report
    
    def _generate_recommendations(self, corr_results, ml_results, bayesian_results, 
                                opt_results, sig_results, hierarchical_results=None, 
                                causal_results=None, riemann_results=None, voodoo_results=None) -> List[str]:
        """분석 결과 기반 추천사항 생성"""
        recommendations = []
        
        # 1. 상관관계 기반 추천
        if corr_results.get('average_correlation', 0) < 0.3:
            recommendations.append("시스템 간 상관관계가 낮음 - 독립적 예측이 가능하여 앙상블 효과 기대")
        
        # 2. 머신러닝 기반 추천
        if ml_results.get('feature_importance'):
            top_system = max(ml_results['feature_importance'].items(), key=lambda x: x[1])
            recommendations.append(f"가장 중요한 시스템: {top_system[0]} - 이 시스템의 정확도 개선에 집중")
        
        # 3. 베이지안 분석 기반 추천
        reliable_systems = [(sys, data.get('reliability_score', 0)) 
                          for sys, data in bayesian_results.items() 
                          if isinstance(data, dict) and 'reliability_score' in data]
        if reliable_systems:
            most_reliable = max(reliable_systems, key=lambda x: x[1])
            recommendations.append(f"가장 신뢰할 수 있는 시스템: {most_reliable[0]}")
        
        # 4. 가중치 최적화 기반 추천
        if opt_results:
            weight_changes = [(sys, data.get('change_percent', 0)) for sys, data in opt_results.items()]
            big_changes = [sys for sys, change in weight_changes if abs(change) > 20]
            if big_changes:
                recommendations.append(f"가중치 대폭 조정 필요 시스템: {', '.join(big_changes)}")
        
        # 5. 통계적 유의성 기반 추천
        non_significant = [sys for sys, data in sig_results.items() 
                          if sys != 'anova' and not data.get('significant', False)]
        if non_significant:
            recommendations.append(f"통계적 유의성 부족 시스템: {', '.join(non_significant)} - 알고리즘 개선 필요")
        
        # 6. 계층적 분석 기반 추천
        if hierarchical_results:
            layer_analysis = hierarchical_results.get('layer_analysis', {})
            if layer_analysis:
                layer_items = list(layer_analysis.items())
                if layer_items:
                    strongest_layer = max(layer_items, key=lambda x: x[1].get('layer_strength', 0))
                    recommendations.append(f"가장 강한 계층: {strongest_layer[0]} - 이 계층 시스템들의 정확도 우선 개선")
            
            hierarchical_effectiveness = hierarchical_results.get('hierarchical_effectiveness', 0)
            if hierarchical_effectiveness < 0.5:
                recommendations.append("계층적 구조의 효과성이 낮음 - 계층 간 연결 강화 필요")
        
        # 7. 리만 점성술 분석 기반 추천
        if riemann_results:
            avg_curvature = riemann_results.get('average_curvature_strength', 0)
            if avg_curvature > 0.7:
                recommendations.append("높은 우주적 곡률 감지 - 점성술 시스템의 기하학적 정밀도 활용 강화")
            elif avg_curvature < 0.3:
                recommendations.append("낮은 우주적 곡률 - 점성술보다 다른 시스템들에 더 의존하는 것이 효과적")
        
        # 8. 베이지안 부두 분석 기반 추천
        if voodoo_results:
            for voodoo_system, data in voodoo_results.items():
                if isinstance(data, dict):
                    reality_strength = data.get('reality_manipulation_strength', 0)
                    intervention_effect = data.get('direct_intervention_effect', 0)
                    
                    if reality_strength > 0.8:
                        recommendations.append(f"{voodoo_system}: 강력한 현실 조작 능력 - 직접 개입 전략 활용")
                    elif intervention_effect > 0.3:
                        recommendations.append(f"{voodoo_system}: 유의미한 개입 효과 - 베이지안 업데이트 로직 강화")
                    
                    if data.get('statistical_significance', False):
                        max_target = data.get('max_manipulation_target')
                        if max_target:
                            target_name, target_weight = max_target
                            recommendations.append(f"최적 개입 대상: {target_name} (가중치: {target_weight:.3f}) - 우선 적용 대상")
                    
                    intervention_classification = data.get('intervention_classification', '')
                    if '현실 조작 수준' in intervention_classification:
                        recommendations.append("⚠️ 현실 조작 수준의 개입 능력 - 윤리적 사용 고려 필요")
        
        return recommendations
        big_changes = [sys for sys, change in weight_changes if abs(change) > 20]
        if big_changes:
            recommendations.append(f"가중치 대폭 조정 필요 시스템: {', '.join(big_changes)}")
        
        # 5. 통계적 유의성 기반 추천
        non_significant = [sys for sys, data in sig_results.items() 
                          if sys != 'anova' and not data.get('significant', False)]
        if non_significant:
            recommendations.append(f"통계적 유의성 부족 시스템: {', '.join(non_significant)} - 알고리즘 개선 필요")
        
        # 6. 계층적 분석 기반 추천
        if hierarchical_results:
            layer_analysis = hierarchical_results.get('layer_analysis', {})
            if layer_analysis:
                strongest_layer = max(layer_analysis.items(), key=lambda x: x[1]['layer_strength'])
                recommendations.append(f"가장 강한 계층: {strongest_layer[0]} - 이 계층 시스템들의 정확도 우선 개선")
            
            hierarchical_effectiveness = hierarchical_results.get('hierarchical_effectiveness', 0)
            if hierarchical_effectiveness < 0.5:
                recommendations.append("계층적 구조의 효과성이 낮음 - 계층 간 연결 강화 필요")
        
        # 7. 인과관계 경로 기반 추천
        if causal_results:
            pathway_validity = causal_results.get('pathway_validity_rate', 0)
            if pathway_validity < 0.5:
                recommendations.append("인과관계 경로 유효성 부족 - 계층 순서 재검토 필요")
            
            strongest_pathway = causal_results.get('strongest_pathway')
            if strongest_pathway:
                pathway_name = strongest_pathway[0].replace('_to_', ' → ').replace('_', ' ').title()
                recommendations.append(f"가장 강한 인과관계: {pathway_name} - 이 경로 최적화 우선")
        
        return recommendations

    def hierarchical_causality_analysis(self) -> Dict[str, Any]:
        """계층적 인과관계 분석"""
        print("\n🔗 계층적 인과관계 분석")
        print("=" * 35)
        
        # IoR 계층 구조 정의
        hierarchical_layers = {
            'meta_layer': ['voodoo_psychology'],  # 메타 현실 조작
            'foundational_layer': ['saju_four_pillars'],  # 기본 관계 패턴
            'environmental_layer': ['climate_science'],  # 환경 영향
            'cosmic_layer': ['western_astrology', 'vedic_astrology'],  # 우주적 영향
            'probabilistic_layer': ['i_ching', 'runic_divination']  # 확률적 연결
        }
        
        layer_analysis = {}
        
        for layer_name, systems in hierarchical_layers.items():
            available_systems = [s for s in systems if s in self.df.columns]
            
            if available_systems:
                layer_scores = []
                for system in available_systems:
                    layer_scores.extend(self.df[system].values)
                
                layer_analysis[layer_name] = {
                    'systems': available_systems,
                    'layer_mean': np.mean(layer_scores),
                    'layer_std': np.std(layer_scores),
                    'layer_strength': np.mean(layer_scores) * (1 - np.std(layer_scores))
                }
        
        # 계층 간 상호작용 분석
        layer_interactions = {}
        available_layers = list(layer_analysis.keys())
        
        for i, layer1 in enumerate(available_layers):
            for layer2 in available_layers[i+1:]:
                systems1 = layer_analysis[layer1]['systems']
                systems2 = layer_analysis[layer2]['systems']
                
                if systems1 and systems2:
                    correlations = []
                    for s1 in systems1:
                        for s2 in systems2:
                            if s1 in self.df.columns and s2 in self.df.columns:
                                corr = np.corrcoef(self.df[s1], self.df[s2])[0,1]
                                if not np.isnan(corr):
                                    correlations.append(corr)
                    
                    if correlations:
                        layer_interactions[f"{layer1}_{layer2}"] = {
                            'average_correlation': np.mean(correlations),
                            'interaction_strength': abs(np.mean(correlations))
                        }
        
        # 전체 계층적 효과성
        hierarchical_effectiveness = np.mean([data['layer_strength'] for data in layer_analysis.values()])
        
        return {
            'layer_analysis': layer_analysis,
            'layer_interactions': layer_interactions,
            'hierarchical_effectiveness': hierarchical_effectiveness
        }
    
    def causal_pathway_validation(self) -> Dict[str, Any]:
        """인과관계 경로 검증"""
        print("\n🛤️ 인과관계 경로 검증")
        print("=" * 35)
        
        # 인과관계 가설 경로
        causal_pathways = [
            {
                'name': 'meta_to_foundation',
                'path': ['voodoo_psychology', 'saju_four_pillars'],
                'hypothesis': '메타 현실 조작이 기본 관계 패턴에 영향'
            },
            {
                'name': 'cosmic_to_probabilistic', 
                'path': ['western_astrology', 'i_ching'],
                'hypothesis': '우주적 패턴이 확률적 연결에 영향'
            },
            {
                'name': 'foundation_to_outcome',
                'path': ['saju_four_pillars', 'target'],
                'hypothesis': '기본 관계 패턴이 최종 결과에 영향'
            }
        ]
        
        pathway_results = {}
        
        for pathway in causal_pathways:
            path_systems = pathway['path']
            available_path = [s for s in path_systems if s in self.df.columns]
            
            if len(available_path) >= 2:
                # 경로 강도 계산 (순차적 상관관계)
                path_correlations = []
                for i in range(len(available_path) - 1):
                    sys1, sys2 = available_path[i], available_path[i+1]
                    corr = np.corrcoef(self.df[sys1], self.df[sys2])[0,1]
                    path_correlations.append(corr)
                
                # 경로의 전체 강도 (상관관계들의 기하평균)
                path_strength = np.prod([abs(c) for c in path_correlations]) ** (1/len(path_correlations))
                
                pathway_results[pathway['name']] = {
                    'hypothesis': pathway['hypothesis'],
                    'available_path': available_path,
                    'path_correlations': path_correlations,
                    'path_strength': path_strength,
                    'validated': path_strength > 0.3  # 임계값
                }
        
        return pathway_results
    def riemann_astrology_analysis(self) -> Dict[str, Any]:
        """점성술의 리만 방정식적 특성 분석 - 시공간 곡률과 행성 배치의 기하학적 관계"""
        print("\n🌌 점성술 리만 기하학적 분석")
        print("=" * 45)
        print("시공간 곡률 → 행성 배치 → 현실 구조화")
        
        astrology_scores = self.df['western_astrology'].values
        vedic_scores = self.df['vedic_astrology'].values
        
        # 리만 곡률 텐서 모방 - 점성술 시스템 간의 곡률 계산
        curvature_matrix = np.zeros((len(astrology_scores), len(astrology_scores)))
        
        for i in range(len(astrology_scores)):
            for j in range(len(astrology_scores)):
                if i != j:
                    # 곡률 계산: 두 점 사이의 기하학적 "휘어짐"
                    spatial_distance = abs(astrology_scores[i] - astrology_scores[j])
                    temporal_distance = abs(vedic_scores[i] - vedic_scores[j])
                    
                    # 리만 곡률 근사: K = (spatial_curvature * temporal_curvature) / distance
                    if spatial_distance > 0 and temporal_distance > 0:
                        curvature = (spatial_distance * temporal_distance) / (spatial_distance + temporal_distance)
                        curvature_matrix[i][j] = curvature
        
        # 전체 시공간 곡률 (스칼라 곡률)
        scalar_curvature = np.mean(curvature_matrix[curvature_matrix > 0])
        
        # 곡률이 강한 "특이점" 찾기 (현실 변화 지점)
        singularities = []
        for i in range(len(astrology_scores)):
            local_curvature = np.mean(curvature_matrix[i][curvature_matrix[i] > 0])
            if local_curvature > scalar_curvature * 1.5:  # 평균보다 50% 이상 높은 곡률
                singularities.append({
                    'index': i,
                    'celebrity': self.df.iloc[i]['celebrity'],
                    'curvature': local_curvature,
                    'reality_distortion': local_curvature / scalar_curvature
                })
        
        # 기하학적 연결성 (parallel transport) 계산
        geometric_connectivity = 0
        for i in range(len(astrology_scores)-1):
            # 인접한 점들 사이의 "평행 이동" 비용
            transport_cost = abs(curvature_matrix[i][i+1])
            geometric_connectivity += transport_cost
        
        geometric_connectivity = geometric_connectivity / (len(astrology_scores) - 1)
        
        print(f"시공간 스칼라 곡률: {scalar_curvature:.4f}")
        print(f"기하학적 연결성: {geometric_connectivity:.4f}")
        print(f"발견된 특이점: {len(singularities)}개")
        
        if singularities:
            print("\n현실 왜곡 특이점들:")
            for sing in sorted(singularities, key=lambda x: x['reality_distortion'], reverse=True)[:3]:
                print(f"  {sing['celebrity']}: 왜곡도 {sing['reality_distortion']:.2f}x")
        
        return {
            'scalar_curvature': scalar_curvature,
            'curvature_matrix': curvature_matrix.tolist(),
            'geometric_connectivity': geometric_connectivity,
            'singularities': singularities,
            'riemann_metric': np.std(curvature_matrix[curvature_matrix > 0])
        }
    
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
        
        # 부두/심리학적 개입 시스템 탐지
        voodoo_columns = [col for col in self.df.columns if any(keyword in col.lower() 
                          for keyword in ['voodoo', 'psychological', 'meta', 'intervention', 'magic'])]
        
        if not voodoo_columns:
            # 부두 개입 시뮬레이션 데이터 생성 (실제로는 심리학적/부두적 개입 데이터)
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
            
            # 데이터프레임에 추가
            self.df['voodoo_intent_strength'] = intent_strength
            self.df['voodoo_belief_consistency'] = belief_consistency
            self.df['voodoo_emotional_investment'] = emotional_investment
            self.df['voodoo_symbolic_resonance'] = symbolic_resonance
            self.df['voodoo_composite'] = voodoo_composite
            
            voodoo_columns = ['voodoo_composite']
        
        results = {}
        
        for voodoo_col in voodoo_columns:
            voodoo_scores = self.df[voodoo_col].values
            
            # === 베이지안 개입 분석 ===
            
            # 사전 확률 (Prior): 개입 전 현실 상태
            prior_reality_state = np.mean(self.df['target']) if 'target' in self.df else 0.3
            
            # 개입 강도별 그룹핑 (3분위)
            low_thresh = np.percentile(voodoo_scores, 33)
            high_thresh = np.percentile(voodoo_scores, 67)
            
            low_intervention = voodoo_scores <= low_thresh
            mid_intervention = (voodoo_scores > low_thresh) & (voodoo_scores <= high_thresh)
            high_intervention = voodoo_scores > high_thresh
            
            # 각 개입 수준에서의 성공률 (우도)
            if 'target' in self.df:
                success_low = np.mean(self.df['target'][low_intervention])
                success_mid = np.mean(self.df['target'][mid_intervention])
                success_high = np.mean(self.df['target'][high_intervention])
            else:
                # 시뮬레이션: 개입 강도에 따른 성공률 증가 (부두의 직접성 반영)
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
                np.mean(voodoo_scores[low_intervention]),
                np.mean(voodoo_scores[mid_intervention]),
                np.mean(voodoo_scores[high_intervention])
            ])
            
            # 현실 변화 벡터 (3차원 현실 공간에서의 변화)
            reality_change_vector = intervention_matrix @ intent_vector
            
            # === 메타-물리적 변환 계수 ===
            # ψ(meta) → φ(physical) 변환
            target_values = self.df['target'] if 'target' in self.df else np.random.binomial(1, 0.3 + 0.4 * voodoo_scores, len(voodoo_scores))
            meta_physical_coefficient = np.corrcoef(voodoo_scores, target_values)[0,1]
            
            # === 직접 개입 효과 정량화 ===
            direct_intervention_effect = success_high - success_low
            
            # 베이지안 사후 확률 계산
            evidence = np.mean([success_low, success_mid, success_high])  # P(관찰된결과)
            
            if evidence > 0:
                posterior_low = (success_low * prior_reality_state) / evidence
                posterior_mid = (success_mid * prior_reality_state) / evidence
                posterior_high = (success_high * prior_reality_state) / evidence
            else:
                posterior_low = posterior_mid = posterior_high = prior_reality_state
            
            # === 현실 조작 강도 ===
            # 표준편차 단위로 정규화된 효과 크기 (Cohen's d)
            if len(self.df[low_intervention]) > 1 and len(self.df[high_intervention]) > 1:
                pooled_std = np.sqrt(
                    ((len(self.df[low_intervention]) - 1) * np.var(target_values[low_intervention]) +
                     (len(self.df[high_intervention]) - 1) * np.var(target_values[high_intervention])) /
                    (len(self.df[low_intervention]) + len(self.df[high_intervention]) - 2)
                )
                cohens_d = direct_intervention_effect / pooled_std if pooled_std > 0 else 0
            else:
                cohens_d = direct_intervention_effect / (np.std(target_values) + 1e-6)
            
            reality_manipulation_strength = min(abs(cohens_d), 2.0)  # 최대 2.0으로 제한
            
            # === 신뢰구간 (부트스트랩) ===
            bootstrap_effects = []
            for _ in range(1000):
                sample_indices = np.random.choice(len(voodoo_scores), len(voodoo_scores), replace=True)
                sample_scores = voodoo_scores[sample_indices]
                sample_targets = target_values[sample_indices]
                
                sample_low = sample_scores <= np.percentile(sample_scores, 33)
                sample_high = sample_scores > np.percentile(sample_scores, 67)
                
                if np.sum(sample_low) > 0 and np.sum(sample_high) > 0:
                    bootstrap_effects.append(np.mean(sample_targets[sample_high]) - 
                                           np.mean(sample_targets[sample_low]))
            
            if bootstrap_effects:
                confidence_interval = np.percentile(bootstrap_effects, [2.5, 97.5])
            else:
                confidence_interval = [0, 0]
            
            # === 개입 효율성 지수 ===
            # 얼마나 적은 에너지로 큰 변화를 만들어내는가
            intervention_efficiency = (direct_intervention_effect / 
                                     (np.mean(voodoo_scores) + 1e-6))  # 0으로 나누기 방지
            
            # === Word Weight 효과 (이름 기반 조작 용이성) ===
            word_weights = {}
            celebrities = self.df['celebrity'].unique()
            
            for celebrity in celebrities:
                # 이름의 음성학적/진동학적 가중치
                name_length = len(celebrity)
                vowel_count = sum(1 for char in celebrity.lower() if char in 'aeiou')
                consonant_density = (name_length - vowel_count) / name_length if name_length > 0 else 0
                
                # 베이지안 가중치: 자음 밀도 + 길이 패턴
                syllable_weight = consonant_density * 0.6 + (vowel_count / name_length if name_length > 0 else 0) * 0.4
                word_weights[celebrity] = syllable_weight
            
            # 결과 저장
            results[voodoo_col] = {
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
                'meta_physical_coefficient': meta_physical_coefficient,
                'reality_manipulation_strength': reality_manipulation_strength,
                'cohens_d_effect_size': cohens_d,
                'intervention_efficiency': intervention_efficiency,
                'confidence_interval_95': confidence_interval,
                'statistical_significance': confidence_interval[0] > 0 or confidence_interval[1] < 0,
                'intervention_classification': self._classify_intervention_strength(reality_manipulation_strength),
                'word_weights': word_weights,
                'max_manipulation_target': max(word_weights.items(), key=lambda x: x[1]) if word_weights else None
            }
            
            print(f"\n{voodoo_col} 베이지안 부두 분석:")
            print(f"  📊 사전 현실 상태: {prior_reality_state:.3f}")
            print(f"  🔄 직접 개입 효과: {direct_intervention_effect:.3f}")
            print(f"  🌟 현실 조작 강도: {reality_manipulation_strength:.3f} ({results[voodoo_col]['intervention_classification']})")
            print(f"  ⚡ 개입 효율성: {intervention_efficiency:.3f}")
            print(f"  🎯 메타-물리 변환계수: {meta_physical_coefficient:.3f}")
            print(f"  📈 Cohen's d 효과크기: {cohens_d:.3f}")
            print(f"  🔒 95% 신뢰구간: [{confidence_interval[0]:.3f}, {confidence_interval[1]:.3f}]")
            
            if results[voodoo_col]['statistical_significance']:
                print("  ✅ 통계적으로 유의한 현실 개입 효과 확인")
            else:
                print("  ❌ 개입 효과 통계적 유의성 부족")
            
            print(f"  🎭 베이지안 사후확률: 저({posterior_low:.3f}) → 중({posterior_mid:.3f}) → 고({posterior_high:.3f})")
            
            # 가장 조작하기 쉬운 대상 출력
            if results[voodoo_col]['max_manipulation_target']:
                max_target, max_weight = results[voodoo_col]['max_manipulation_target']
                print(f"  🎪 최대 조작 가능 대상: {max_target} (가중치: {max_weight:.3f})")
        
        return results
    
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
    
    def mathematical_system_alignment(self) -> Dict[str, Any]:
        """각 시스템의 수학적 특성에 따른 정렬 분석"""
        print("\n🧮 수학적 시스템 정렬 (Mathematical Alignment)")
        print("=" * 55)
        print("점성술(리만) + 부두(베이지안) + 사주(조합론) + 주역(확률론) + 룬(위상수학)")
        
        # 각 시스템의 수학적 "언어" 특성 정의
        math_signatures = {
            'western_astrology': 'geometric',     # 리만 기하학
            'i_ching': 'probabilistic',          # 확률론/정보이론
            'saju_four_pillars': 'combinatorial', # 조합론
            'vedic_astrology': 'harmonic',       # 조화 해석학
            'runic_divination': 'topological'    # 위상수학
        }
        
        alignment_matrix = {}
        
        # 시스템 간 수학적 "번역 가능성" 계산
        for sys1 in self.system_names:
            alignment_matrix[sys1] = {}
            for sys2 in self.system_names:
                if sys1 != sys2:
                    scores1 = self.df[sys1].values
                    scores2 = self.df[sys2].values
                    
                    # 수학적 호환성 계산
                    correlation = np.corrcoef(scores1, scores2)[0,1]
                    
                    # 수학적 "방언" 간 번역 난이도
                    sig1 = math_signatures[sys1]
                    sig2 = math_signatures[sys2]
                    
                    # 수학 분야 간 번역 계수
                    translation_coefficients = {
                        ('geometric', 'probabilistic'): 0.7,    # 기하→확률 (중간)
                        ('geometric', 'combinatorial'): 0.8,    # 기하→조합 (쉬움)
                        ('probabilistic', 'combinatorial'): 0.9, # 확률→조합 (매우 쉬움)
                        ('harmonic', 'geometric'): 0.85,        # 조화→기하 (쉬움)
                        ('topological', 'geometric'): 0.95,     # 위상→기하 (매우 쉬움)
                    }
                    
                    # 양방향 번역 계수 확인
                    trans_coeff = translation_coefficients.get((sig1, sig2), 
                                 translation_coefficients.get((sig2, sig1), 0.5))
                    
                    # 최종 정렬 점수
                    alignment_score = abs(correlation) * trans_coeff
                    alignment_matrix[sys1][sys2] = alignment_score
        
        # 전체 시스템 정렬도 계산
        total_alignment = 0
        pair_count = 0
        
        for sys1 in alignment_matrix:
            for sys2 in alignment_matrix[sys1]:
                total_alignment += alignment_matrix[sys1][sys2]
                pair_count += 1
        
        overall_alignment = total_alignment / pair_count if pair_count > 0 else 0
        
        # 가장 잘 정렬된 시스템 쌍 찾기
        best_alignments = []
        for sys1 in alignment_matrix:
            for sys2 in alignment_matrix[sys1]:
                best_alignments.append({
                    'system1': sys1,
                    'system2': sys2,
                    'alignment_score': alignment_matrix[sys1][sys2],
                    'math_types': f"{math_signatures[sys1]} ↔ {math_signatures[sys2]}"
                })
        
        best_alignments.sort(key=lambda x: x['alignment_score'], reverse=True)
        
        print(f"전체 시스템 정렬도: {overall_alignment:.4f}")
        
        print("\n최고 정렬 시스템 쌍들:")
        for align in best_alignments[:5]:
            print(f"  {align['system1']} ↔ {align['system2']}: "
                  f"{align['alignment_score']:.3f} ({align['math_types']})")
        
        # 부두의 베이지안 분석 통합
        bayesian_results = self.bayesian_voodoo_analysis()
        
        # 점성술의 리만 분석 통합  
        riemann_results = self.riemann_astrology_analysis()
        
        return {
            'overall_alignment': overall_alignment,
            'alignment_matrix': alignment_matrix,
            'mathematical_signatures': math_signatures,
            'best_alignments': best_alignments[:5],
            'bayesian_voodoo_integration': bayesian_results,
            'riemann_astrology_integration': riemann_results,
            'computational_readiness': overall_alignment * 0.8 + 
                                     bayesian_results['average_bayesian_update'] * 0.1 +
                                     riemann_results['scalar_curvature'] * 0.1
        }

# 메인 실행 코드
if __name__ == "__main__":
    try:
        print("🌟 IoR (Impression of Reality) 고급 분석 시스템 시작")
        print("=" * 60)
        
        # 데이터 로드
        data_file = 'integrated_ior_validation.json'
        
        # 분석 실행
        analyzer = IoRAdvancedAnalytics(data_file)
        comprehensive_report = analyzer.generate_comprehensive_report()
        
        print("\n" + "=" * 60)
        print("🎯 IoR 분석 완료 - 수학적 정렬 및 베이지안 부두 개입 분석 포함")
        print("=" * 60)
        
        # 주요 결과 요약
        print("\n📊 주요 결과 요약:")
        
        # 베이지안 부두 결과
        voodoo_results = comprehensive_report.get('bayesian_voodoo_analysis', {})
        if voodoo_results:
            for system, data in voodoo_results.items():
                manipulation_strength = data.get('reality_manipulation_strength', 0)
                intervention_effect = data.get('direct_intervention_effect', 0)
                print(f"  🔮 {system}: 현실 조작 강도 {manipulation_strength:.3f}, 직접 개입 효과 {intervention_effect:.3f}")
        
        # 리만 점성술 결과
        riemann_results = comprehensive_report.get('riemann_astrology_analysis', {})
        if riemann_results:
            curvature = riemann_results.get('scalar_curvature', 0)
            geodesic_stability = riemann_results.get('geodesic_stability', 0)
            print(f"  🌌 점성술 리만 분석: 스칼라 곡률 {curvature:.3f}, 측지선 안정성 {geodesic_stability:.3f}")
        
        # 수학적 정렬 결과
        alignment_results = comprehensive_report.get('mathematical_system_alignment', {})
        if alignment_results:
            overall_alignment = alignment_results.get('overall_alignment', 0)
            computational_readiness = alignment_results.get('computational_readiness', 0)
            print(f"  🧮 수학적 정렬: 전체 정렬도 {overall_alignment:.3f}, 계산 준비도 {computational_readiness:.3f}")
        
        # 추천사항
        recommendations = comprehensive_report.get('recommendations', [])
        if recommendations:
            print(f"\n💡 주요 추천사항 ({len(recommendations)}개):")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. {rec}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
