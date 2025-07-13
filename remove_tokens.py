#!/usr/bin/env python3
"""
민감한 토큰 제거 스크립트
Hugging Face 토큰들을 찾아서 제거합니다.
"""

import os
import re
from pathlib import Path

def remove_sensitive_tokens():
    """민감한 토큰들을 찾아서 제거"""
    
    # Hugging Face 토큰 패턴
    hf_token_pattern = r'hf_[A-Za-z0-9]{34}'
    
    # 검색할 디렉토리
    search_dirs = ['optimized_dialogues']
    
    total_replacements = 0
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
            
        for file_path in Path(search_dir).rglob('*.txt'):
            print(f"검사 중: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 토큰 찾기
                tokens_found = re.findall(hf_token_pattern, content)
                
                if tokens_found:
                    print(f"  발견된 토큰: {len(tokens_found)}개")
                    
                    # 토큰을 일반적인 플레이스홀더로 교체
                    new_content = re.sub(hf_token_pattern, 'hf_[REDACTED_TOKEN]', content)
                    
                    # 파일 저장
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    total_replacements += len(tokens_found)
                    print(f"  토큰 제거 완료")
                    
            except Exception as e:
                print(f"  오류: {e}")
    
    print(f"\n총 {total_replacements}개의 토큰을 제거했습니다.")

if __name__ == "__main__":
    remove_sensitive_tokens()
