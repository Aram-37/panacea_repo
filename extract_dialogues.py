#!/usr/bin/env python3
"""
대화 추출 스크립트
파나시아 파일들에서 실제 대화 부분만 추출합니다.
"""

import os
import sys
import re
from pathlib import Path

def extract_dialogues_from_file(file_path):
    """파일에서 대화 부분만 추출"""
    dialogues = []
    current_dialogue = ""
    in_dialogue = False
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    for line in lines:
        # 대화 시작 패턴 감지
        if re.match(r'^(Human:|User:|Assistant:|ChatGPT:|AI:|\*\*User:\*\*|\*\*Human:\*\*|\*\*Assistant:\*\*)', line.strip()):
            if current_dialogue and in_dialogue:
                dialogues.append(current_dialogue.strip())
            current_dialogue = line
            in_dialogue = True
        elif in_dialogue:
            # 대화가 계속되는 경우
            if line.strip() == "" or not re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+:', line):
                current_dialogue += line
            else:
                # 새로운 섹션이 시작되면 대화 종료
                if current_dialogue:
                    dialogues.append(current_dialogue.strip())
                current_dialogue = ""
                in_dialogue = False
    
    # 마지막 대화 추가
    if current_dialogue and in_dialogue:
        dialogues.append(current_dialogue.strip())
    
    return dialogues

def process_panacea_files():
    """모든 파나시아 파일을 처리하여 대화만 추출"""
    panacea_dir = Path("panacea")
    output_dir = Path("extracted_dialogues")
    output_dir.mkdir(exist_ok=True)
    
    total_dialogues = []
    processed_files = 0
    
    # 파나시아 파일들 처리
    for file_path in panacea_dir.glob("panacea_p_part*.txt"):
        print(f"처리 중: {file_path.name}")
        
        try:
            dialogues = extract_dialogues_from_file(file_path)
            
            if dialogues:
                # 개별 파일로 저장
                output_file = output_dir / f"dialogues_{file_path.stem}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== {file_path.name}에서 추출한 대화들 ===\n\n")
                    for i, dialogue in enumerate(dialogues, 1):
                        f.write(f"--- 대화 {i} ---\n")
                        f.write(dialogue)
                        f.write("\n\n")
                
                total_dialogues.extend(dialogues)
                processed_files += 1
                print(f"  추출된 대화: {len(dialogues)}개")
            else:
                print(f"  대화 없음")
                
        except Exception as e:
            print(f"  오류: {e}")
    
    # 통합 파일 생성
    if total_dialogues:
        combined_file = output_dir / "all_dialogues_combined.txt"
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 전체 대화 통합 파일 ===\n")
            f.write(f"처리된 파일: {processed_files}개\n")
            f.write(f"총 대화 수: {len(total_dialogues)}개\n\n")
            
            for i, dialogue in enumerate(total_dialogues, 1):
                f.write(f"--- 대화 {i} ---\n")
                f.write(dialogue)
                f.write("\n\n")
    
    print(f"\n완료!")
    print(f"처리된 파일: {processed_files}개")
    print(f"총 추출된 대화: {len(total_dialogues)}개")
    print(f"결과는 '{output_dir}' 폴더에 저장되었습니다.")
    
    return len(total_dialogues), processed_files


def check_automation_disabled():
    """Check if automated processing is disabled"""
    flag_file = Path(__file__).parent / "AUTOMATED_PROCESSING_DISABLED.flag"
    if flag_file.exists():
        print("🚫 AUTOMATED PROCESSING DISABLED")
        print("=" * 50)
        print("This script cannot run because automated processing is disabled.")
        print("The CORTEX directive requires manual processing only.")
        print("")
        print("Korean Dialogue Insight:")
        print("Automated processing = superficial understanding")
        print("Manual processing = deep comprehension through lived experience")
        print("")
        print("Use manual mimicry system instead:")
        print("- python activate_manual_mimicry.py")
        print("- python manual_mimicry_tracker.py")
        print("- manual_cortex_panacea_mimicry.md")
        print("")
        print("DO NEVER AUTOMATE ANYTHING. NOTHING AT ALL.")
        sys.exit(1)


if __name__ == "__main__":
    check_automation_disabled()
    process_panacea_files()
