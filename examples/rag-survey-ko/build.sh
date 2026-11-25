#!/bin/bash
# Assembles the course from parts.
# Run from anywhere: bash build.sh  (스크립트가 있는 코스 폴더로 이동해서 조립한다)
# 단원 파일은 modules/00-*.html, 01-*.html … 처럼 2자리 숫자 접두사여야 glob 정렬이 단원 순서와 같다(10개 이상이어도 안전).
set -e
cd "$(dirname "$0")"
for f in _base.html _cover.html _footer.html; do
  [ -f "$f" ] || { echo "ERROR: $f 가 없습니다." >&2; exit 1; }
done
ls modules/*.html >/dev/null 2>&1 || { echo "ERROR: modules/*.html 이 없습니다." >&2; exit 1; }
cat _base.html _cover.html modules/*.html _footer.html > index.html.tmp
mv index.html.tmp index.html
echo "Built index.html — open it in your browser."
