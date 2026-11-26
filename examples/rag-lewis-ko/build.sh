#!/bin/bash
# Assembles the course into ONE standalone index.html (오프라인 단독 파일: CSS·JS·글꼴·그림을 모두 안에 넣음).
# Run from anywhere: bash build.sh  (스크립트가 있는 코스 폴더를 조립한다)
# 단원 파일은 modules/00-*.html, 01-*.html … 처럼 2자리 숫자 접두사여야 정렬이 단원 순서와 같다.
# 실제 처리는 build.py(python3 표준 라이브러리만 사용)가 한다.
set -e
cd "$(dirname "$0")"
if [ -f build.py ]; then PY=build.py
elif [ -f ../../references/build.py ]; then PY=../../references/build.py
else echo "ERROR: build.py 가 없습니다. references/build.py를 강의 폴더에 복사하세요." >&2; exit 1; fi
# 인터프리터: $P2C_PYTHON → fontTools가 깔린 기본 venv → python3 (fontTools가 있어야 본문 글꼴 부분 집합을 만든다)
VENV_PY="$HOME/.local/share/paper-to-course/venv/bin/python"
if [ -n "$P2C_PYTHON" ]; then PYTHON="$P2C_PYTHON"
elif [ -x "$VENV_PY" ]; then PYTHON="$VENV_PY"
else PYTHON=python3; echo "NOTE: $VENV_PY 이 없어 python3로 조립합니다 (P2C_PYTHON으로 지정 가능)." >&2; fi
# --allow-todo: [작성 필요: …] 자리를 남긴 채 미리 보기로 조립. --no-prerender: 수식을 미리 렌더링하지 않음
"$PYTHON" "$PY" . "$@"
