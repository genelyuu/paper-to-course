#!/bin/bash
# 유지보수자용: references/main.js·styles.css를 고친 뒤 한 번 실행해 배포용 압축본을 다시 만든다.
# 강의를 만들 때는 실행하지 않는다(build.sh는 이 폴더의 결과물만 읽고, 표준 라이브러리 python3만 쓴다).
#
#   main.min.js    esbuild 압축(지역 이름 줄이기) → javascript-obfuscator(문자열 표 암호화, 식별자 16진화)
#   styles.min.css esbuild 압축(주석·공백 제거)
#   manifest.json  원본 sha256. build.py가 강의 폴더의 main.js·styles.css와 대조해 압축본을 쓸지 정한다.
#
# 필요: node(npx). 버전은 고정한다.
set -e
cd "$(dirname "$0")"
REF=..
npx -y esbuild@0.24.0 "$REF/main.js" --minify --target=es2018 --legal-comments=none --outfile=.main.esb.js --log-level=warning
npx -y javascript-obfuscator@4.1.1 .main.esb.js --output main.min.js \
  --compact true --identifier-names-generator hexadecimal --rename-globals false \
  --string-array true --string-array-encoding rc4 --string-array-threshold 0.75 \
  --string-array-wrappers-type function --split-strings true --split-strings-chunk-length 8 \
  --control-flow-flattening false --dead-code-injection false --self-defending false \
  --transform-object-keys false --unicode-escape-sequence false --log false
rm -f .main.esb.js
npx -y esbuild@0.24.0 "$REF/styles.css" --minify --legal-comments=none --outfile=styles.min.css --log-level=warning
python3 - "$REF" <<'EOF'
import hashlib, json, sys, pathlib
ref = pathlib.Path(sys.argv[1])
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
json.dump({"main.js": h(ref / "main.js"), "styles.css": h(ref / "styles.css")},
          open("manifest.json", "w"), indent=2)
EOF
echo "vendor 갱신: main.min.js $(wc -c < main.min.js)B, styles.min.css $(wc -c < styles.min.css)B"
