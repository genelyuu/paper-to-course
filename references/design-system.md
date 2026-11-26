# 디자인 시스템 레퍼런스

paper-to-course CSS 디자인 토큰. `styles.css`는 수정 없이 강의 디렉터리에 복사하고, 강조색만 `_base.html`에서 바꾼다.

## 목차
디자인 아이덴티티 · 색상 팔레트(교과 색 프리셋, 색상 규약) · 타이포그래피 · 한글 타이포그래피 · 간격과 레이아웃(4px 격자, 지면 레이아웃) · 그림자와 깊이 · 수식·연구 색상 · SVG 다이어그램 시스템

---

## 디자인 아이덴티티

- 본문·제목 모두 **Pretendard Variable** `v1.3.9`의 KS X 1001 부분 집합 하나. OFL 예약 이름 조건 때문에 이름은 `P2C Sans`(`references/vendor/fonts/`, 생성: `vendor/ksx-unicodes.py`·`rename-font.py`). 빌드가 data URI로 `index.html`에 넣으므로 CDN 없음. 라틴 디스플레이 서체를 섞지 않는다(한 줄 안에서 서체가 갈라짐).
- 코드: **JetBrains Mono** → D2Coding / Nanum Gothic Coding → Pretendard(한글 주석). 고정폭은 코드(의사코드·코드 블록·줄 번호)에만. 라벨·수치·사이드바 번호는 Pretendard + `tabular-nums`.
- 그림자 대신 선: `--shadow-sm`·`-md`는 1px 링, 떠 있는 요소(툴팁)만 `-lg`·`-xl`. 스크롤 등장 애니메이션·떠오르는 호버 없음.
- 순백 바탕 #FFFFFF + 차가운 회색 면(#F4F6F8, #D3D8DE, #555B62 등) + 교과 색 하나(기본 과학탐구 파랑). 베이지·따뜻한 회색 금지.
- 지면: 수능특강 + 코넬식 노트("지면 레이아웃" 절).

---

## 색상 팔레트

```css
:root {
  --color-bg: #FFFFFF;  --color-bg-subtle: #F4F6F8; /* 면(요약 줄, 날개) */
  --color-bg-code: #1E1E2E;
  --color-text: #222426;  --color-text-secondary: #555B62;  --color-text-muted: #868D95;
  --color-border: #D3D8DE;  --color-border-light: #E6E9ED;
  --color-surface: #FFFFFF;  --color-surface-subtle: #F7F8FA;
  /* ACCENT — 교과 색, 기본 과학탐구 파랑 */
  --color-accent: #1F6FB2;  --color-accent-hover: #185A92;
  --color-accent-light: #E8F1FA;  --color-accent-muted: #6FA3D3;
  /* SEMANTIC */
  --color-success: #2D8B55;  --color-success-light: #E8F5EE;
  --color-error: #C93B3B;  --color-error-light: #FDE8E8;
  --color-info: #2A7B9B;  --color-info-light: #E4F2F7;  /* 파생 규칙이 덮어씀 */
  /* ACTORS (옛 요소 호환용) */
  --color-actor-1: #C2410C;  --color-actor-2: #0F766E;  --color-actor-3: #6B4FA8;
  --color-actor-4: #A16207;  --color-actor-5: #1B7A50;
}
```

강조색은 흰 글자 배경(`.module-number`, `.corner-tag`, `.callout-title`)으로 쓰이므로 흰 글자 대비가 충분해야 한다.

### 교과 색 프리셋

수능특강 교과별 표지 색(출처: namu.wiki/w/수능특강). 분야에 맞는 하나를 `_base.html`의 네 변수에 넣는다.

| 프리셋 | 분야 | accent | hover | light | muted | 흰 글자 대비 |
|---|---|---|---|---|---|---|
| 과학탐구 파랑 (기본값) | ML, 물리, 생명 등 자연과학 | #1F6FB2 | #185A92 | #E8F1FA | #6FA3D3 | 5.28:1 |
| 수학 초록 | 이론, 최적화, 통계 | #1B7A50 | #145F3E | #E6F4EC | #6BB592 | 5.32:1 |
| 사회탐구 보라 | 경제, 사회과학, HCI | #6B4FA8 | #563F88 | #F0ECF8 | #A08ECB | 6.35:1 |
| 영어 주황 | 언어학, 언어 중심 NLP 논문 | #B85C0F | #964A0B | #FCEFE3 | #E0A06A | 4.59:1 |

국어 노랑은 흰 글자 대비 부족으로 제외. 프리셋 밖 색은 흰 글자 대비 4.5:1 이상 확인.

---

## 색상 규약

색 사용 기준의 정본(`interactive-elements.md`, `illustration.md`가 이 절을 가리킴). 값은 `styles.css` 실제 값.

| 역할 | 토큰·값 | 쓰는 곳 | 쓰지 않는 곳 |
|---|---|---|---|
| 교과 색 | `--color-accent` 네 값(위). 강의당 한 세트 | 강조 하나(핵심 대상, 활성 상태, 모듈 번호 블록, 코너 이름표, 그림 강조), 링크·버튼 | 여러 대상 구분, 장식, 본문 글자색 |
| 먹색 | `#1F2328` (`.ink`, `.ink-fill`, 그림 속 `text`) | 그림·문항 삽화·도식의 선과 글자 | 본문 글자(`--color-text`) |
| 글자 | `--color-text` #222426, `-secondary` #555B62, `-muted` #868D95 | 본문, 보조 설명, 흐린 표지(`.paper-ref`, 캡션) | `-muted`를 본문 단락에(명암비 부족) |
| 배경·면 | `--color-bg`·`--color-surface` #FFFFFF, `--color-bg-subtle` #F4F6F8, `--color-surface-subtle` #F7F8FA | 바탕, 카드, 요약 줄·날개 | 베이지·크림 |
| 테두리 | `--color-border` #D3D8DE, `-light` #E6E9ED | 카드·표·상자 테두리, 구분선 | 강조 |
| 그림 회색 | `.guide` → `--color-border`(1px), `.guide-axis` #8C959F, `.guide-fill` #EEF0F2 | 모눈, 축, 보조 면 | 대상 자체(먹색·교과 색) |
| 상태 색 | `--color-success` #2D8B55(+`-light` #E8F5EE), `--color-error` #C93B3B(+`-light` #FDE8E8) | 정답·오답 피드백, 결과 막대 증감 | 그 밖의 강조·장식, 그림 |
| 콜아웃 | `.callout-accent` = 교과 색, `.callout-info` = `--color-info`(+`-light`), `.callout-warning` = `--color-error` | 콜아웃 종류(배경 지식은 `callout-info`) | 새 콜아웃 색 |
| 코드 칸 | 바탕 #1E1E2E. Catppuccin: `.code-keyword` #CBA6F7, `.code-string` #A6E3A1, `.code-function` #89B4FA, `.code-comment` #6C7086, `.code-number` #FAB387, `.code-property` #F9E2AF, `.code-operator` #94E2D5, `.code-tag` #F38BA8. 줄 번호 #6C7086, 라벨 #9399B2, 강조 줄 #CBA6F7 inset(4px) | 코드 칸 안. `main.js` `colorizePseudocode`가 자동 색칠 | 코드 칸 밖, 새 색, 줄마다 손 `style` |

**규칙**
- 유채색은 교과 색 하나. 예외는 코드 칸과 상태 색뿐. `--color-actor-*`·`--color-info` 원값은 새 그림에 쓰지 않는다.
- 그림은 먹색 + 교과 색 + 회색만(`check-pages.py`가 그림당 유채색 2개 이상 검출).
- 강조 수단은 하나(색 + 굵게 + 밑줄 겹치기 금지).
- 본문 글자·배경 명암비 4.5:1 이상(교과 색 위 흰 글자도).

---

## 타이포그래피

```css
:root {
  --font-display / --font-body: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
  --font-mono: 'JetBrains Mono', 'D2Coding', 'Nanum Gothic Coding', 'Pretendard Variable', Pretendard, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Fira Code', Consolas, monospace;
  /* 타입 스케일 (1.25) */
  --text-xs: 0.75rem (라벨, 배지);  --text-sm: 0.875rem (보조, 코드);  --text-base: 1rem (본문);
  --text-lg: 1.125rem (리드);  --text-xl: 1.25rem (화면 제목);  --text-2xl: 1.5rem (하위 모듈 제목);
  --text-3xl: 1.875rem (모듈 부제);  --text-4xl: 2.25rem (모듈 제목);  --text-5xl: 3rem (히어로);  --text-6xl: 3.75rem (모듈 번호);
  /* 행간 (한글은 라틴보다 넉넉히) */
  --leading-tight: 1.35 (제목);  --leading-snug: 1.45 (부제·화면 제목);  --leading-normal: 1.75 (본문);  --leading-loose: 1.9;
  /* 라벨 자간 (:lang(ko)에서 0.01~0.03em으로 축소) */
  --tracking-label: 0.1em;  --tracking-label-wide: 0.12em;  --tracking-label-sm: 0.05em;
}
```

---

## 한글 타이포그래피

`styles.css` 맨 아래 `KOREAN TYPOGRAPHY` 섹션. `<html lang="ko">` 전제.

| 규칙 | 값 | 이유 |
|---|---|---|
| 줄바꿈 | `word-break: keep-all` | 어절 중간 줄바꿈 방지 |
| 긴 토큰 | `overflow-wrap: break-word` | `anywhere`는 flex/grid min-content를 줄여 레이아웃이 바뀜 |
| 행간 | 본문 1.75, 제목 1.35~1.45 | 한글 글리프가 em 박스를 채움 |
| 자간 | 제목 `-0.02em`, 본문 `-0.005em`, 라벨 `:lang(ko)` 0.01~0.03em | `0.1em`은 한글이 흩어져 보임 |
| 이탤릭 금지 | `em`/`i` → `font-style: normal` + 600 + 강조색, `font-synthesis: none` | 한글 가짜 기울임 방지. KaTeX 이탤릭은 유지. 라벨 속 수학 기호는 `<i class="mi">q</i>`(KaTeX 수학 글꼴 + 이탤릭) |
| 드러냄표 | `.ko-emphasis` (`text-emphasis: dot`) | 선택 유틸리티 |
| KaTeX | `.katex { word-break: normal }` + 좌우 `0.12em` | keep-all·자간이 수식에 영향 주지 않게, 한글과 틈 |
| 코드 | `overflow-wrap: anywhere`, `white-space: pre-wrap` | 긴 코드 토큰 끊기 |
| 툴팁 | `keep-all` + 최대 폭 320px | 어절 중간 끊김 방지 |

---

## 간격과 레이아웃

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem; --space-5: 1.25rem; --space-6: 1.5rem;
  --space-8: 2rem; --space-10: 2.5rem; --space-12: 3rem; --space-16: 4rem; --space-20: 5rem; --space-24: 6rem;
  --content-width: 800px;  --content-width-wide: 1000px;
  --nav-height: 48px;  --page-height: calc(100vh - var(--nav-height));
  --page-width: 1040px; /* 단서 칸 + 간격 + 노트 칸 */  --cue-width: 232px;  --cornell-gap: 32px;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 9999px;
}
```

### 간격: 4px 격자

모든 패딩·마진·크기는 4px 배수(간격 4~96px, 반지름 4/8/12px, 내비 48px). 예외는 선 두께 1px·2px와 2px 진행선뿐. 2px·6px 반단계 금지. 근거: Carbon(2/4/8 배수), Atlassian(8px 기본), USWDS(8px 배수), GitHub Primer(4px 단위) 중 4px 배수만 채택.

### 지면 레이아웃 (수능특강 + 코넬)

모든 화면은 `.screen.cornell` 한 페이지이며 1440×900 한 화면(보이는 영역 약 813px − 내비 48px = 765px)에 스크롤 없이 들어간다. 1200px 미만에서는 한 단으로 접히고 높이 제한이 풀린다.

```
┌ nav 48px ──────────────────────────────────────────────┐
│ [3] 모듈 제목 (.module-header: 64px 번호 블록)         │
│ ════════════ 2px 교과 색 선 ═══════════════════════════ │
│ ┌ .cue 232px ┐ │ ┌ .notes ─────────────────────────┐   │
│ │ ○ 질문 1?  │ │ │ [탐구 자료] 화면 제목 (.corner-tag)│ │
│ │ ○ 질문 2?  │ │ │ 본문, 수식, 그림, 퀴즈 ...       │   │
│ └────────────┘ │ └─────────────────────────────────┘   │
│ ┌ .summary ─ 요약 한 문장 ───────────────────────────┐ │
│ (높이 ≤ 100vh − 48px)                                  │
└────────────────────────────────────────────────────────┘
```

- 위는 모듈 첫 페이지. 둘째 페이지부터는 `.module-header` 없이 `.cue | .notes / .summary`.
- `.cue`: 오른쪽 2px 교과 색 선, 질문마다 속 빈 원. `.summary`: 위 2px 교과 색 선 + 회색 면, 오른쪽에 `.pager`가 겹치지 않게 패딩. `.bogi` 마지막 자식 아래 여백 0.
- 퀴즈: 1200px 이상에서 2단, 페이지당 최대 2문항(선택지 5개와 펼친 해설이 765px 안).
- `check-pages.py`가 765px로 잰다. `--page-height`는 런타임 최소 높이라 짧은 페이지에서 `.summary`가 맨 아래(의도된 동작).
- 마크업·쪽 맞춤은 `interactive-elements.md` "코넬식 페이지와 지면 요소".
- **여백 토큰.** `.module` 좌우 `--space-10`, 위아래 `--page-pad-y: 32px`, 본문 블록(표·그림·콜아웃·퀴즈·유도·수식) 사이 `--block-gap: 16px`. 첫 블록 위·마지막 블록 아래 여백 0. 꽉 찬 페이지는 `.screen.cornell.dense`(24px·12px, 첫 페이지면 머리말 여백도 축소).
- **요약 위치.** 둘째 페이지부터 `--page-height`, 첫 페이지는 `main.js` `initPageLayout`이 `100vh - 머리말까지의 거리`로 최소 높이를 정해 요약이 모든 페이지에서 같은 자리.
- **단서 칸 용어 정리(`.cue-terms`).** 고급 페이지에서 `main.js`가 핵심 질문 아래에 경계선 + `용어 정리` 표지 + `dl`(`dt` 굵게, `dd` `--text-xs` 회색)을 쪽 높이 안에서만 넣는다.
- **사이드바 라벨**은 한 줄 말줄임, 약 14자 이내.

#### 교과 색 파생 규칙

컴포넌트 색은 교과 색에서 파생된다(콜아웃 `배경 지식`·`보충 설명`, 퀴즈 경고, 연구 노트, 수식 상자 테두리).

| 토큰 | 값 |
|---|---|
| `--color-info`, `.callout-info` | `var(--color-accent-hover)` |
| `--color-info-light`, `.quiz-feedback.warning` 배경 | `var(--color-accent-light)` |
| `--color-research-accent` | `var(--color-accent-hover)` |
| `--color-research-bg` | `color-mix(in srgb, var(--color-accent) 6%, var(--color-surface))` |
| `--color-math-border` | `color-mix(in srgb, var(--color-accent) 18%, var(--color-border))` |

성공·오류 색과 코드 칸 Catppuccin 색만 교과 색과 무관.

---

## 그림자와 깊이

```css
--shadow-sm: 0 1px 2px rgba(34,36,38,0.04);   --shadow-md: 0 2px 8px rgba(34,36,38,0.06);
--shadow-lg: 0 8px 24px rgba(34,36,38,0.08);  --shadow-xl: 0 16px 48px rgba(34,36,38,0.10);
```

평평하고 옅게. 테두리와 면으로 구분한다.

---

## 수식·연구 색상

```css
--color-math-bg: #F7F8FA;  --color-math-border: #D3D8DE;  --color-math-text: #222426;
--color-research-bg: #F0F4F8;  --color-research-accent: #2A5F8F;   /* 초기값, 파생 규칙이 덮어씀 */
--color-result-pos: #2D8B55;  --color-result-neg: #C93B3B;  --color-result-neutral: #8A929B; /* 기준선 */
```

---

## SVG 다이어그램 시스템

모든 다이어그램(순서도, 개념도, 계보 트리, 실험 구성)은 인라인 SVG.

- 컨테이너 `<div class="svg-diagram">`(반응형, 최대 800px, 가운데). `viewBox="0 0 W H"` + `width="100%"`.
- 노드 `.node-rect` / `.node-rect.accent` / 각진 `.node-rect.sq`(`rx: 2px`, 행렬·칩).
- 간선 `.edge-line` / `.edge-line.accent`, 직각 `<path>`만([도식 간선은 직각으로](#도식-간선은-직각으로)).
- 글자는 `var(--font-body)` 상속, 코드는 `.mono`. 색은 CSS 변수.
- 노드 라벨: `<foreignObject>` + `.node-label` + `<span>` 하나. 노드 밖 짧은 표지만 `<text>`.

```html
<div class="svg-diagram">
  <svg viewBox="0 0 800 160" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="그림 내용을 한 문장으로">
    <rect class="node-rect accent" x="300" y="20" width="200" height="60" />
    <foreignObject x="308" y="24" width="184" height="52"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>이 논문</span></div></foreignObject>
    <path class="edge-line accent" d="M400,80 V112" />
    <polygon class="edge-arrow accent" points="395,112 405,112 400,122" />
  </svg>
</div>
```

### 그림 정렬 규칙

원칙: 같은 것은 같은 자리에서 시작한다. (검출) 항목은 `check-pages.py`가 검사해 어기면 종료 코드 1.

| 대상 | 규칙 | 구현 |
|---|---|---|
| 결과 막대 | 모든 트랙이 같은 x에서 시작, 같은 폭 | `.result-bars` 3열 격자(라벨 · 트랙 · 수치), 막대는 `subgrid`. 라벨·수치 오른쪽 정렬, 고른 숫자 폭 (검출) |
| SVG 노드 | 같은 단계는 같은 폭·간격, 라벨은 가로·세로 가운데 | `.node-label > span`, 폭 공식은 `interactive-elements.md` (검출: 라벨 구조, viewBox 이탈) |
| SVG 간선 | 노드 테두리에서 시작·끝, 화살촉 | 허공에서 끝나는 선 금지 |
| 의사코드 | 코드 줄 *i*와 설명 줄 *i*가 같은 y | `main.js`가 높이 맞춤(2단일 때) (검출) |
| 연구 계보 | 자식 노드가 같은 x | 관계 라벨 폭 96px |
| 흐름 단계 | 원 간격 같음, 화살표는 원 세로 가운데 | 단계 폭 112px, 화살표 높이 = 원 높이 |
| 제거 실험 | 한 부품 안 정렬 축 하나 | 수치·표지·설명 모두 가운데 |

**여백 규칙**
- 부품 안 마지막 요소 아래 여백 0. 부품 사이 여백은 부품 `margin`이 정한다.
- 소개 문장(`그림은 ~을 나타낸 것이다.`)–그림–해석 문장 간격은 같다.
- 한 번에 한 단계만 보이는 부품(수식 유도)에는 단계 구분선 없음.
- `position: absolute` 라벨은 부모에 `position: relative`가 있을 때만(없으면 문서 맨 위로 빠짐).

### SVG 속 한글 주의사항

- `<text>`는 자동 줄바꿈 없음. 폭은 한글 1자 ≈ 1em, 라틴 ≈ 0.55em(14px 한글 8자 ≈ 112px + 좌우 여백).
- 글꼴은 `font-family` 속성 대신 CSS(`.svg-diagram text`가 이미 `var(--font-body)`). 필요하면 `style="font-family: var(--font-body)"`.
- 상자 안 라벨은 줄 수와 무관하게 `<foreignObject>` 안 `.node-label > span`(keep-all, 세로 가운데). `<text>`는 상자 밖 짧은 표지(축 이름, 간선 라벨)만.
- 수학 기호 `<text>`는 `font-style="italic"`, 한글은 똑바로(구분은 `font-weight="500"`이나 흐린 `fill`). `foreignObject` 속 기호는 `<i class="mi">q</i>`, 아래첨자 `<i class="mi">d</i><sub>k</sub>`.

### 개념 그림 클래스와 페이지 넘김

- 그림 클래스(`.figure`, `.svg-diagram` 안): `.ink`, `.ink.strong`, `.ink-fill`, `.accent`, `.accent-fill`, `.guide`, `.guide-axis`, `.guide-fill`, `.row-accent`, `.edge-line.thin`, `.edge-line.dashed`, `.dot`, `.dot-accent`, `text.mono|muted|accent-text`. 색은 [색상 규약](#색상-규약). `.node-rect`, `.node-rect.sq`, `.edge-line`, `.edge-arrow`(+`.accent`)는 `.svg-diagram`과 `.figure svg`에서 같게 동작.
- 캡션 `.figure-caption`. 너비 맞춤 `.svg-diagram.fit`(`--diagram-max`, 기본 100%). 본문 옆 그림 `figure.figure.side`(`--figure-side-width`, 기본 200px). 문항 삽화 `.q-figure`(`--q-figure-width`, 기본 280px), `.q-body`가 있으면 선택지는 한 줄에 하나.
- 새 개념마다 그림 하나를 본문 옆(`.with-figure` + `figure.figure.side`)에 두어 765px를 넘지 않게 한다.
- 모듈 번호는 `1, 2, 3 …` 연속 정수. 논문 위치는 화면 제목 끝 `.paper-ref`. `.sec-num`은 폐기(CSS만 남음).
- 페이지 넘김: `html { scroll-padding-top: var(--nav-height) }`, `.module { scroll-snap-align: start; scroll-margin-top: calc(-1 * var(--nav-height)) }`. 우하단 `.pager`(‹ n / N › + 안내)는 `main.js`가 넣는다.

### 도식 간선은 직각으로

간선은 수평·수직 선분만(`<path d="M x,y H … V … H …">`), 대각선 금지. 여러 노드로 갈라지면 세로 버스 한 줄에서 직각 분기. 화살촉은 마지막 수평 선분 끝. 좌표평면 벡터 화살표는 간선이 아니므로 방향 그대로. 간선 때문에 노드를 옮기지 않는다.

### 헤더 세로 정렬

- 상단 내비 제목 왼쪽 끝 = 단서 칸 왼쪽, 점 오른쪽 끝 = 노트 칸 오른쪽(1025px 이상, `styles.css` "헤더 세로 정렬").
- 단원 도입 번호 상자(64px)는 제목+부제 덩어리와 위아래 끝을 맞춘다: 제목 `line-height: 1.15`, 부제 위 여백 4px. 제목·부제를 두 줄로 쓰지 않는다.
