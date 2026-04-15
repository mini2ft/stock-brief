#!/bin/bash
set -e

# 가상환경 없으면 생성
if [ ! -d ".venv" ]; then
  echo "가상환경 생성 중..."
  python3 -m venv .venv
fi

# 활성화
source .venv/bin/activate

# 의존성 설치
pip install -q -r requirements.txt

# 실행
python main.py
