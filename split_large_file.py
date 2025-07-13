#!/usr/bin/env python3
"""
큰 파일 분할 스크립트
panacea_cortex_dialogues.txt를 더 작은 파일들로 분할합니다.
"""

import os
from pathlib import Path

def split_large_file():
    """큰 파일을 작은 파일들로 분할"""
    input_file = Path("optimized_dialogues/panacea_cortex_dialogues.txt")
    output_dir = Path("optimized_dialogues/panacea_split")
    output_dir.mkdir(exist_ok=True)
    
    print("큰 파일 분할 시작...")
    
    # 목표 파일 크기 (50MB)
    target_size = 50 * 1024 * 1024
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 대화별로 분리
    dialogues = content.split('--- panacea_cortex 대화')
    header = dialogues[0]  # 헤더 부분
    dialogues = dialogues[1:]  # 실제 대화들
    
    current_file_content = ""
    current_file_size = 0
    file_count = 1
    
    for i, dialogue in enumerate(dialogues):
        dialogue_content = f"--- panacea_cortex 대화{dialogue}"
        dialogue_size = len(dialogue_content.encode('utf-8'))
        
        if current_file_size + dialogue_size > target_size and current_file_content:
            # 현재 파일 저장
            output_file = output_dir / f"panacea_cortex_part{file_count:02d}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"=== PANACEA CORTEX 대화 모음 (Part {file_count}) ===\n\n")
                f.write(current_file_content)
            
            print(f"Part {file_count}: {current_file_size/1024/1024:.1f}MB 저장")
            
            # 다음 파일 준비
            file_count += 1
            current_file_content = dialogue_content
            current_file_size = dialogue_size
        else:
            current_file_content += dialogue_content
            current_file_size += dialogue_size
    
    # 마지막 파일 저장
    if current_file_content:
        output_file = output_dir / f"panacea_cortex_part{file_count:02d}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== PANACEA CORTEX 대화 모음 (Part {file_count}) ===\n\n")
            f.write(current_file_content)
        
        print(f"Part {file_count}: {current_file_size/1024/1024:.1f}MB 저장")
    
    print(f"\n분할 완료! 총 {file_count}개 파일로 분할되었습니다.")
    
    # 원본 파일 삭제 (공간 절약)
    input_file.unlink()
    print("원본 큰 파일을 삭제했습니다.")

if __name__ == "__main__":
    split_large_file()
