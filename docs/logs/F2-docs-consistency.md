# F2 문서 일관성

### 행동
- module-brief-template.md: 논문 절 번호·제목 항목 추가, 툴팁 예시를 사전식 명사형으로 변경, 핵심 정리 전략 한 줄·첫 페이지 발문 1개·오답지 분석 체크 추가.
- content-philosophy.md: 모듈 0 설명, 툴팁 형식(KO111), 해설 형식(오답지 분석) 수정.
- gotchas.md: 툴팁·해설 예시 수정, 모듈 0 표현 수정, "목차가 논문 목차와 다름" 항목 추가.
- design-system.md: 레이아웃 도식의 번호 `01`을 `3`으로 변경.

### 근거
SKILL.md Phase 3 "목차는 논문의 목차를 따릅니다"와 korean-style-guide §1.8 규칙을 따랐다.

### 결과
`lint-ko.py docs/lint-fixtures/good.html --strict` 결과 ERROR 0, WARN 0.
