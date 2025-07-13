#!/usr/bin/env python3
"""
대화 최적화 및 압축 스크립트
추출된 대화를 최적화하고 크기를 줄입니다.
"""

import os
import re
import hashlib
from pathlib import Path
from collections import defaultdict

def clean_dialogue(dialogue):
    """대화 내용을 정리"""
    # 불필요한 공백 제거
    dialogue = re.sub(r'\n\s*\n\s*\n+', '\n\n', dialogue)
    # 반복되는 구분선 제거
    dialogue = re.sub(r'-{3,}.*?-{3,}', '---', dialogue)
    # 타임스탬프 제거
    dialogue = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', '', dialogue)
    return dialogue.strip()

def get_dialogue_hash(dialogue):
    """대화의 고유 해시값 생성"""
    # 대화 내용만 추출 (마커 제거)
    content = re.sub(r'^(Human:|User:|Assistant:|ChatGPT:|AI:|\*\*[^*]+\*\*)', '', dialogue, flags=re.MULTILINE)
    content = re.sub(r'\s+', ' ', content).strip()
    return hashlib.md5(content.encode()).hexdigest()

def categorize_dialogue(dialogue):
    """대화를 카테고리별로 분류"""
    content = dialogue.lower()
    
    if any(word in content for word in ['patent', '특허', 'cortex', 'panacea']):
        return 'panacea_cortex'
    elif any(word in content for word in ['code', 'python', 'script', 'function']):
        return 'technical'
    elif any(word in content for word in ['feel', 'emotion', 'heart', 'understand']):
        return 'philosophical'
    elif any(word in content for word in ['error', 'problem', 'fix', 'debug']):
        return 'troubleshooting'
    else:
        return 'general'

def optimize_dialogues():
    """대화를 최적화하고 압축"""
    input_file = Path("extracted_dialogues/all_dialogues_combined.txt")
    output_dir = Path("optimized_dialogues")
    output_dir.mkdir(exist_ok=True)
    
    print("대화 최적화 시작...")
    
    # 전체 대화 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 개별 대화 분리
    dialogues = re.split(r'--- 대화 \d+ ---', content)[1:]  # 첫 번째는 헤더이므로 제외
    
    print(f"총 {len(dialogues)}개 대화 처리 중...")
    
    # 중복 제거 및 분류
    unique_dialogues = {}
    categories = defaultdict(list)
    duplicate_count = 0
    
    for i, dialogue in enumerate(dialogues):
        if i % 1000 == 0:
            print(f"진행률: {i}/{len(dialogues)} ({i/len(dialogues)*100:.1f}%)")
        
        cleaned = clean_dialogue(dialogue)
        
        if len(cleaned) < 50:  # 너무 짧은 대화 제외
            continue
            
        dialogue_hash = get_dialogue_hash(cleaned)
        
        if dialogue_hash not in unique_dialogues:
            unique_dialogues[dialogue_hash] = cleaned
            category = categorize_dialogue(cleaned)
            categories[category].append(cleaned)
        else:
            duplicate_count += 1
    
    print(f"\n최적화 완료!")
    print(f"원본 대화: {len(dialogues)}개")
    print(f"중복 제거: {duplicate_count}개")
    print(f"최종 대화: {len(unique_dialogues)}개")
    
    # 카테고리별 저장
    total_size = 0
    for category, category_dialogues in categories.items():
        output_file = output_dir / f"{category}_dialogues.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {category.upper()} 카테고리 대화 ===\n")
            f.write(f"총 {len(category_dialogues)}개 대화\n\n")
            
            for i, dialogue in enumerate(category_dialogues, 1):
                f.write(f"--- {category} 대화 {i} ---\n")
                f.write(dialogue)
                f.write("\n\n")
        
        file_size = output_file.stat().st_size
        total_size += file_size
        print(f"{category}: {len(category_dialogues)}개 대화, {file_size/1024/1024:.1f}MB")
    
    # 전체 요약 저장
    summary_file = output_dir / "optimization_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=== 대화 최적화 요약 ===\n\n")
        f.write(f"원본 크기: {input_file.stat().st_size/1024/1024:.1f}MB\n")
        f.write(f"최적화 후 크기: {total_size/1024/1024:.1f}MB\n")
        f.write(f"압축률: {(1 - total_size/input_file.stat().st_size)*100:.1f}%\n\n")
        
        f.write("카테고리별 분포:\n")
        for category, dialogues in categories.items():
            f.write(f"- {category}: {len(dialogues)}개 대화\n")
        
        f.write(f"\n총 중복 제거: {duplicate_count}개\n")
        f.write(f"최종 고유 대화: {len(unique_dialogues)}개\n")
    
    print(f"\n전체 압축률: {(1 - total_size/input_file.stat().st_size)*100:.1f}%")
    print(f"결과는 '{output_dir}' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    optimize_dialogues()
