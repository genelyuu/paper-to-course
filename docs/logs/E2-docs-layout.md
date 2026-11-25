# E2 로그: 지면 레이아웃 문서화

### 행동
`references/styles.css`의 "TEXTBOOK PAGE LAYOUT" 절, 토큰 블록, `references/check-pages.py`를 읽고 한국어 문서를 갱신했다. 수정한 파일은 `interactive-elements.md`, `design-system.md`, `SKILL.md`, `module-brief-template.md`, `gotchas.md`, `_base.html`(주석만)이다. `styles.css`, `main.js`, HTML 마크업, `examples/`, `README.md`는 건드리지 않았다.
### 근거
CSS에 이미 구현된 클래스(`.screen.cornell`, `.cue`, `.notes`, `.summary`, `.corner-tag`, `.wing`, `.q-num`, `.q-points`, `.quiz-options.row`)와 토큰 값을 문서에 그대로 옮겼다. 간격 격자의 근거는 Carbon, Atlassian, USWDS, GitHub Primer 문서이며 4px 배수만 채택했다.
### 결과
- interactive-elements.md: 모듈 골격을 코넬 버전으로 교체, `.module-number`가 옅다는 설명을 고침, "코넬식 페이지와 지면 요소" 절 신설, 퀴즈(q-num, q-points, row, 2단, 페이지당 4문항)와 콜아웃(아이콘 숨김, 제목 칩) 갱신.
- design-system.md: 색 토큰 교체, 교과 색 프리셋 표, 간격 토큰·반지름·내비게이션 값 갱신, "간격: 4px 격자"와 "지면 레이아웃" 절(ASCII 와이어프레임), 그림자 값 갱신.
- SKILL.md: 코넬 페이지 규칙, 프리셋 선택, Phase 5의 check-pages.py 실행과 체크리스트, 참고 파일 목록, 디자인 정체성 갱신(약 +18줄).
- module-brief-template.md: 화면별 계획(핵심 질문, 노트 내용, 요약, 쪽 맞춤) 추가.
- gotchas.md: 페이지 넘침, 코넬 아닌 화면, 문항 번호 이중 표기 항목과 최종 점검 명령 추가.
- _base.html: 강조색 주석을 교과 색 프리셋 값으로 교체.
- 검증: grep으로 `옅게`, `오프화이트`, `vermillion` 등 낡은 표현이 남지 않음을 확인했다.
