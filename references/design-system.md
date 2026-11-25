# 디자인 시스템 레퍼런스

paper-to-course 시스템의 CSS 디자인 토큰 전체 목록입니다. `styles.css`는 수정 없이 그대로 강의 디렉터리에 복사하고, 강조색만 `_base.html`에서 바꿉니다.

## 목차
1. [디자인 아이덴티티](#디자인-아이덴티티)
2. [색상 팔레트](#색상-팔레트)
   - [색상 규약](#색상-규약)
3. [타이포그래피](#타이포그래피)
4. [한글 타이포그래피](#한글-타이포그래피)
5. [간격과 레이아웃](#간격과-레이아웃)
   - [간격: 4px 격자](#간격-4px-격자)
   - [지면 레이아웃 (수능특강 + 코넬)](#지면-레이아웃-수능특강--코넬)
6. [그림자와 깊이](#그림자와-깊이)
7. [수식·연구 색상](#수식연구-색상)
8. [SVG 다이어그램 시스템](#svg-다이어그램-시스템)

---

## 디자인 아이덴티티

- 한글+라틴 본문: **Pretendard Variable** (jsDelivr, `v1.3.9` 고정, dynamic-subset으로 필요한 글리프만 로드)
- 제목도 같은 **Pretendard** 하나로 씁니다. 라틴 디스플레이 서체를 섞으면 "트랜스포머(Attention…)"처럼 한 줄 안에서 서체가 갈라져 보이기 때문입니다.
- 코드: **JetBrains Mono** → D2Coding / Nanum Gothic Coding → Pretendard (한글 주석용 폴백). 고정폭은 코드(의사코드·코드 블록·줄 번호)에만 쓰고, 라벨·수치·사이드바 번호는 Pretendard에 `tabular-nums`로 씁니다.
- 그림자 대신 선: `--shadow-sm`·`--shadow-md`는 1px 테두리 링이고, 떠 있는 요소(툴팁 등)만 `--shadow-lg`·`--shadow-xl`을 씁니다. 스크롤 등장 애니메이션과 떠오르는 호버는 쓰지 않습니다.
- 베이지·따뜻한 회색은 쓰지 않습니다. 중립색은 모두 차가운 회색(#F4F6F8, #D3D8DE, #555B62 등)입니다.
- 교재 지면 같은 순백 바탕(#FFFFFF)과 차가운 회색 면, 교과 색 강조색 하나. 기본 강조색은 과학탐구 파랑이며 "교과 색 프리셋"에서 고른다.
- 지면 구성은 수능특강 + 코넬식 노트이다("지면 레이아웃" 절).

---

## 색상 팔레트

```css
:root {
  /* BACKGROUNDS — 교재 지면: 흰 바탕 + 차가운 회색 면 */
  --color-bg:             #FFFFFF;
  --color-bg-subtle:        #F4F6F8;       /* 면(요약 줄, 날개) */
  --color-bg-code:        #1E1E2E;       /* code blocks */
  --color-text:           #222426;
  --color-text-secondary: #555B62;
  --color-text-muted:     #868D95;
  --color-border:         #D3D8DE;
  --color-border-light:   #E6E9ED;
  --color-surface:        #FFFFFF;
  --color-surface-subtle:   #F7F8FA;

  /* ACCENT — 교과 색. 기본값은 과학탐구 파랑 */
  --color-accent:         #1F6FB2;
  --color-accent-hover:   #185A92;
  --color-accent-light:   #E8F1FA;
  --color-accent-muted:   #6FA3D3;

  /* SEMANTIC */
  --color-success:        #2D8B55;
  --color-success-light:  #E8F5EE;
  --color-error:          #C93B3B;
  --color-error-light:    #FDE8E8;
  --color-info:           #2A7B9B;
  --color-info-light:     #E4F2F7;

  /* ACTORS (research participants, methods, concepts) */
  --color-actor-1:        #C2410C;
  --color-actor-2:        #0F766E;
  --color-actor-3:        #6B4FA8;
  --color-actor-4:        #A16207;
  --color-actor-5:        #1B7A50;
}
```

그림자는 평평하고 옅다(아래 "그림자와 깊이"). 강조색은 흰 글자 배경(`.module-number`, `.corner-tag`, `.callout-title`)에 쓰이므로 흰 글자 대비가 충분해야 한다.

### 교과 색 프리셋

수능특강은 교과마다 표지 색이 다르다(국어 노랑, 수학 초록, 영어 주황, 한국사 갈색, 과학탐구 파랑, 사회탐구 보라. 출처: namu.wiki/w/수능특강). 논문 분야에 맞는 프리셋 하나를 골라 `_base.html`의 네 변수에 넣는다. 아래 값은 흰 글자 대비를 측정한 것이다.

| 프리셋 | 분야 | accent | hover | light | muted | 흰 글자 대비 |
|---|---|---|---|---|---|---|
| 과학탐구 파랑 (기본값) | ML, 물리, 생명 등 자연과학 | #1F6FB2 | #185A92 | #E8F1FA | #6FA3D3 | 5.28:1 |
| 수학 초록 | 이론, 최적화, 통계 | #1B7A50 | #145F3E | #E6F4EC | #6BB592 | 5.32:1 |
| 사회탐구 보라 | 경제, 사회과학, HCI | #6B4FA8 | #563F88 | #F0ECF8 | #A08ECB | 6.35:1 |
| 영어 주황 | 언어학, 언어 중심 NLP 논문 | #B85C0F | #964A0B | #FCEFE3 | #E0A06A | 4.59:1 |

국어 노랑은 흰 글자 대비가 부족해 프리셋에서 뺐다. 프리셋 밖의 색을 쓰려면 흰 글자 대비 4.5:1 이상을 확인한다.

---

## 색상 규약

색을 어디에 쓰고 어디에 쓰지 않는지의 기준은 이 절이 정한다. 값은 `styles.css`의 `:root`와 그 뒤 덮어쓰기에서 가져온 실제 값이다. 다른 문서(`interactive-elements.md`, `illustration.md`)는 이 절을 가리킨다.

| 역할 | 토큰·값 | 쓰는 곳 | 쓰지 않는 곳 |
|---|---|---|---|
| 교과 색 | `--color-accent` #1F6FB2(기본), `-hover` #185A92, `-light` #E8F1FA, `-muted` #6FA3D3. 강의마다 한 세트만 고른다([교과 색 프리셋](#교과-색-프리셋)) | 강조 하나(핵심 대상, 활성 상태, 모듈 번호 블록, 코너 이름표, 그림의 강조), 링크·버튼 | 한 화면의 여러 대상을 구분하는 용도, 장식, 본문 글자색 |
| 먹색 | `#1F2328` (그림 선·그림 글자: `.ink`, `.ink-fill`, 그림 속 `text`) | 개념 그림·문항 삽화·도식의 선과 글자 | 본문 글자(본문은 `--color-text`) |
| 글자 | `--color-text` #222426, `--color-text-secondary` #555B62, `--color-text-muted` #868D95 | 본문, 보조 설명, 흐린 표지(`.paper-ref`, 캡션) | `--color-text-muted`를 본문 단락에 쓰지 않는다(명암비 부족) |
| 배경·면 | `--color-bg` #FFFFFF, `--color-surface` #FFFFFF, `--color-bg-subtle` #F4F6F8, `--color-surface-subtle` #F7F8FA | 지면 바탕, 카드, 요약 줄·날개 같은 차가운 회색 면 | 베이지·크림 같은 따뜻한 면 |
| 테두리 | `--color-border` #D3D8DE, `--color-border-light` #E6E9ED | 카드·표·상자 테두리, 구분선 | 강조(테두리 색으로 강조하지 않는다) |
| 그림 회색 | `.guide` → `--color-border`(1px), `.guide-axis` #8C959F, `.guide-fill` #EEF0F2 | 모눈, 축, 보조 면 | 대상 자체(대상은 먹색이나 교과 색) |
| 상태 색 | `--color-success` #2D8B55(+`-light` #E8F5EE), `--color-error` #C93B3B(+`-light` #FDE8E8) | 정답·오답 피드백(퀴즈 선택지, 피드백 상자), 결과 막대의 증감 | 그 밖의 강조·장식. 그림에는 쓰지 않는다 |
| 콜아웃 | `.callout-accent` = 교과 색, `.callout-info` = `--color-info` #2A7B9B(+`-light`), `.callout-warning` = `--color-error` | `callout` 종류 표시(배경 지식은 `callout-info`) | 새 콜아웃 색을 만드는 일 |
| 코드 칸 | 바탕 `--color-bg-code` #1E1E2E. Catppuccin: `.code-keyword` #CBA6F7, `.code-string` #A6E3A1, `.code-function` #89B4FA, `.code-comment` #6C7086, `.code-number` #FAB387, `.code-property` #F9E2AF, `.code-operator` #94E2D5, `.code-tag` #F38BA8. 줄 번호 #6C7086, 라벨 #9399B2, 강조 줄 #CBA6F7 inset(4px) | 의사코드·코드 블록 안에서만. `main.js`의 `colorizePseudocode`가 자동으로 칠한다 | 코드 칸 밖. 새 색을 만들지 않고, 줄마다 손으로 `style`로 칠하지 않는다 |

**규칙**
- 유채색은 교과 색 하나만 쓴다. 예외는 코드 칸과 상태 색(정답·오답)뿐이다. `--color-actor-*`·`--color-info`는 옛 요소 호환용이며 새 그림에 쓰지 않는다.
- 베이지·크림·따뜻한 회색 톤을 쓰지 않는다. 중립색은 차가운 회색이다.
- 그림은 먹색 + 교과 색 + 회색만 쓴다. `check-pages.py`가 그림 하나에 유채색이 둘 이상이면 검출한다.
- 강조는 한 가지 수단으로만 한다(색이면 색, 굵기면 굵기). 색 + 굵게 + 밑줄을 겹치지 않는다.
- 본문 글자와 배경의 명암비는 4.5:1 이상이다. 교과 색을 흰 글자 배경으로 쓸 때도 같다.

---

## 타이포그래피

```css
:root {
  /* 제목과 본문 모두 Pretendard 하나 */
  --font-display: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
  --font-body:    'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
  --font-mono:    'JetBrains Mono', 'D2Coding', 'Nanum Gothic Coding', 'Pretendard Variable', Pretendard, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Fira Code', Consolas, monospace;

  /* 타입 스케일 (1.25 비율) */
  --text-xs:   0.75rem;    /* 라벨, 배지 */
  --text-sm:   0.875rem;   /* 보조 텍스트, 코드 */
  --text-base: 1rem;       /* 본문 */
  --text-lg:   1.125rem;   /* 리드 문단 */
  --text-xl:   1.25rem;    /* 화면 제목 */
  --text-2xl:  1.5rem;     /* 하위 모듈 제목 */
  --text-3xl:  1.875rem;   /* 모듈 부제 */
  --text-4xl:  2.25rem;    /* 모듈 제목 */
  --text-5xl:  3rem;       /* 히어로 텍스트 */
  --text-6xl:  3.75rem;    /* 모듈 번호 */

  /* 행간: 한글은 글자 높이가 꽉 차므로 라틴 기준보다 넉넉하게 */
  --leading-tight:  1.35;  /* 제목 (기존 1.15) */
  --leading-snug:   1.45;  /* 부제·화면 제목 (기존 1.3) */
  --leading-normal: 1.75;  /* 본문 (기존 1.6) */
  --leading-loose:  1.9;   /* 여유 있는 문단 (기존 1.8) */

  /* 대문자 라벨 자간 — 한글에서는 :lang(ko)로 0.01~0.03em으로 축소 */
  --tracking-label:      0.1em;
  --tracking-label-wide: 0.12em;
  --tracking-label-sm:   0.05em;
}
```

---

## 한글 타이포그래피

모든 규칙은 `styles.css` 맨 아래 `KOREAN TYPOGRAPHY` 섹션(과 위 토큰)에 모여 있습니다. `<html lang="ko">`가 전제입니다.

| 규칙 | 값 | 이유 |
|---|---|---|
| 줄바꿈 | `word-break: keep-all` | 한글은 글자 사이 어디서든 끊기는 것이 기본값이라 어절 중간에서 줄이 바뀝니다. keep-all은 띄어쓰기에서만 줄을 바꿔 가독성이 높습니다(MDN `word-break`, W3C klreq). |
| 긴 토큰 처리 | `overflow-wrap: break-word` | `anywhere`는 flex/grid의 min-content 크기까지 줄여 레이아웃이 달라질 수 있어 `break-word`를 택했습니다. 긴 URL·영문 토큰은 여전히 넘치지 않고 줄바꿈됩니다. |
| 행간 | 본문 1.75, 제목 1.35~1.45 | 한글 글리프는 em 박스를 거의 가득 채워 라틴(1.15~1.6)보다 더 넓은 행간이 필요합니다. |
| 자간 | 제목 `-0.02em`, 본문 `-0.005em` | Pretendard는 한글 제목에서 살짝 좁은 자간이 안정적입니다. 대문자 라벨의 `0.1em` 자간은 한글에서 글자가 흩어져 보이므로 `:lang(ko)`에서 `0.01~0.03em`으로 줄입니다(토큰 `--tracking-label*`). |
| 이탤릭 금지 | `em`/`i` → `font-style: normal` + 굵기 600 + 강조색 | 한글에는 이탤릭 글리프가 없어 가짜 기울임(synthetic oblique)이 어색합니다. `font-synthesis: none`으로 합성도 막습니다. KaTeX의 이탤릭은 유지합니다. 라벨 속 수학 기호는 `<i class="mi">q</i>`로 씁니다(`.mi`는 KaTeX 수학 글꼴 + 이탤릭). 일반 `<i>`는 위 규칙에 따라 똑바른 글씨가 됩니다. |
| 드러냄표 | `.ko-emphasis` (`text-emphasis: dot`) | 한국어 전통 강조법. 선택 사항 유틸리티입니다. |
| 라틴/한글 혼용 | 제목·본문 모두 Pretendard 하나 | 한글과 라틴이 같은 서체라 굵기·높이가 맞습니다. 라틴 디스플레이 서체를 섞으면 제목 안에서 서체가 갈라져 보입니다. |
| KaTeX | `.katex { word-break: normal }` + 좌우 `0.12em` 여백 | 상위의 keep-all·자간이 수식 내부 조판에 영향을 주지 않게 하고, 수식과 한글 사이에 숨 쉴 틈을 줍니다. |
| 코드 | `overflow-wrap: anywhere`, `white-space: pre-wrap` | 코드의 긴 토큰은 끊어 줘야 하므로 본문 규칙과 분리합니다. |
| 툴팁 | `keep-all` + 최대 폭 320px | 짧은 용어 설명이 어절 중간에서 끊기지 않게 합니다. |

---

## 간격과 레이아웃

```css
:root {
  --space-1:  0.25rem;   --space-2:  0.5rem;    --space-3:  0.75rem;
  --space-4:  1rem;      --space-5:  1.25rem;   --space-6:  1.5rem;
  --space-8:  2rem;      --space-10: 2.5rem;    --space-12: 3rem;
  --space-16: 4rem;      --space-20: 5rem;      --space-24: 6rem;

  --content-width:      800px;
  --content-width-wide: 1000px;
  --nav-height:         48px;
  --page-height:        calc(100vh - var(--nav-height));
  --page-width:         1040px;   /* 단서 칸 + 간격 + 노트 칸 */
  --cue-width:          232px;
  --cornell-gap:        32px;
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-full: 9999px;
}
```

### 간격: 4px 격자

모든 패딩, 마진, 크기 값은 4px의 배수이다(간격 토큰 4~96px, 모서리 반지름 4/8/12px, 내비게이션 48px). 예외는 선 두께 1px·2px와 2px 진행선뿐이다. 2px, 6px 같은 반단계는 쓰지 않는다.

근거: 널리 쓰이는 디자인 시스템이 4px 또는 8px 단위를 기본으로 삼는다.
- Carbon: 간격 단계 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 160px, "multiples of two, four, and eight" (carbondesignsystem.com/elements/spacing/overview/)
- Atlassian: "base unit of 8 pixels"에 2/4/6px 반단계 (atlassian.design/foundations/spacing)
- USWDS: "multiples of 8px"에 작은 크기 예외 (designsystem.digital.gov/design-tokens/spacing-units/)
- GitHub Primer: 크기 토큰이 4px 단위 (primer.style/foundations/primitives/size)

우리는 이 중 4px 배수만 채택하고 2px, 6px 반단계는 쓰지 않는다.

### 지면 레이아웃 (수능특강 + 코넬)

모든 화면은 `.screen.cornell` 한 페이지이며 1440×900 데스크톱 한 화면(브라우저 UI와 48px 내비게이션을 뺀 약 765px)에 스크롤 없이 들어간다. 1200px 미만에서는 한 단으로 접히고 높이 제한이 풀린다.

```
┌──────────────────────────────── 1440 ───────────────────────────────┐
│ nav 48px                                                            │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──┐                                                                │
│ │ 3│ 모듈 제목 (.module-header: 64px 번호 블록, 아래 2px 교과 색 선)│
│ └──┘                                                                │
│ ══════════════════════════════════════════════════ (2px accent)     │
│ ┌ .cue (232px) ┐ │ ┌ .notes ───────────────────────────────────┐    │
│ │ 핵심 질문    │ │ │ [탐구 자료] 화면 제목  (.corner-tag)      │    │
│ │ ○ 질문 1?    │ │ │                                           │    │
│ │ ○ 질문 2?    │ │ │ 본문, 수식, 그림, 퀴즈 ...                │    │
│ │ ○ 질문 3?    │ │ │                                           │    │
│ └──────────────┘ │ └───────────────────────────────────────────┘    │
│ ┌ .summary ────────────────────────────────────────────────────┐    │
│ │ 요약  한 문장으로 이 페이지의 핵심을 정리한다.               │    │
│ └──────────────────────────────────────────────────────────────┘    │
│ (한 페이지 높이 ≤ 100vh - 48px)                                     │
└─────────────────────────────────────────────────────────────────────┘
```

- 위 그림은 모듈의 첫 페이지이다. 둘째 페이지부터는 `.module-header` 없이 `.cue | .notes / .summary`만 있다.
- `.cue`는 오른쪽에 2px 교과 색 선이 있고 핵심 질문마다 속 빈 원 표지가 붙는다. `.summary`는 위에 2px 교과 색 선과 회색 면이 있다.
- 퀴즈는 코넬 페이지 안에서 1200px 이상일 때 2단(시험지 2단)이 되고, 페이지당 최대 4문항이다.
- 마크업과 쪽 맞춤 규칙은 `interactive-elements.md`의 "코넬식 페이지와 지면 요소"를 따른다. 측정은 `check-pages.py`가 한다.

---

## 그림자와 깊이

```css
:root {
  --shadow-sm: 0 1px 2px rgba(34,36,38,0.04);
  --shadow-md: 0 2px 8px rgba(34,36,38,0.06);
  --shadow-lg: 0 8px 24px rgba(34,36,38,0.08);
  --shadow-xl: 0 16px 48px rgba(34,36,38,0.10);
}
```

그림자는 평평하고 옅게 쓴다. 교재 지면처럼 테두리와 면으로 구분하고 깊이감은 최소로 둔다.

---

## 수식·연구 색상

```css
:root {
  /* MATH — for equation blocks and derivations */
  --color-math-bg:        #F7F8FA;       /* cool gray surface */
  --color-math-border:    #D3D8DE;       /* cool gray border */
  --color-math-text:      #222426;       /* body text */

  /* RESEARCH — for lineage/context elements */
  --color-research-bg:    #F0F4F8;       /* cool blue-gray */
  --color-research-accent:#2A5F8F;       /* deep blue */

  /* RESULTS — for experimental result displays */
  --color-result-pos:     #2D8B55;       /* green for improvements */
  --color-result-neg:     #C93B3B;       /* red for underperformance */
  --color-result-neutral: #8A929B;       /* cool gray for baselines */
}
```

---

## SVG 다이어그램 시스템

모든 다이어그램(순서도, 개념도, 계보 트리, 실험 구성)은 아래 규칙을 따르는 인라인 SVG로 만듭니다.

- 컨테이너: `<div class="svg-diagram">`로 `<svg>`를 감싼다 — 반응형, 최대 폭 800px, 가운데 정렬
- 노드: `.node-rect`(기본) 또는 `.node-rect.accent`(강조). 모서리를 거의 직각으로 둘 때(행렬·칩)는 `.node-rect.sq`(`rx: 2px`)
- 간선: `.edge-line`(기본) 또는 `.edge-line.accent`. 직각 `<path>`로만 그린다([도식 간선은 직각으로](#도식-간선은-직각으로))
- 텍스트: `var(--font-body)`를 상속하고, 코드는 `.mono` 클래스(`var(--font-mono)`) 사용
- 색상: CSS 변수 사용 (`var(--color-accent)`, `var(--color-border)` 등)
- ViewBox: `viewBox="0 0 WIDTH HEIGHT"`와 `width="100%"`로 반응형 처리
- 노드 라벨: `<foreignObject>` + `.node-label` + `<span>` 하나(가운데 정렬·자동 줄바꿈). 노드 밖의 짧은 표지만 `<text>`

```html
<div class="svg-diagram">
  <svg viewBox="0 0 800 160" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="그림 내용을 한 문장으로">
    <rect class="node-rect accent" x="300" y="20" width="200" height="60" />
    <foreignObject x="308" y="24" width="184" height="52"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>이 논문</span></div></foreignObject>
    <path class="edge-line accent" d="M400,80 V112" />
    <polygon class="edge-arrow accent" points="395,112 405,112 400,122" />
    <!-- 나머지 요소 -->
  </svg>
</div>
```

### 그림 정렬 규칙

본문 그림은 "같은 것은 같은 자리에서 시작한다"는 원칙 하나로 정렬한다. `check-pages.py`가 아래 항목을 자동으로 검사하고, 어기면 종료 코드 1을 낸다.

| 대상 | 규칙 | 구현 |
|---|---|---|
| 결과 막대 | 모든 트랙이 **같은 x에서 시작하고 폭이 같다.** 값 비교는 길이로 하므로 트랙이 다르면 그래프가 틀린 말을 한다 | `.result-bars`가 3열 격자(라벨 · 트랙 · 수치), 각 막대는 `subgrid`. 라벨 오른쪽 정렬, 수치 오른쪽 정렬·고른 숫자 폭 (검출) |
| SVG 노드 | 같은 단계 노드는 같은 폭·간격, 라벨은 상자의 가로·세로 가운데 | `.node-label > span` 구조, 폭 공식은 `interactive-elements.md` (검출: 라벨 구조, viewBox 이탈) |
| SVG 간선 | 노드 테두리에서 시작해 노드 테두리에서 끝나고 화살촉이 있다 | 허공에서 끝나는 선 금지 |
| 의사코드 | 코드 줄 *i*와 설명 줄 *i*가 같은 y에서 시작한다 | `main.js`가 두 줄의 높이를 맞춤(2단일 때만) (검출) |
| 연구 계보 | 자식 노드가 같은 x에서 시작한다 | 관계 라벨 폭 96px 고정 |
| 흐름 단계 | 단계 원 사이 간격이 같고 화살표는 원의 세로 가운데 | 단계 폭 112px 고정, 화살표 높이 = 원 높이 |
| 제거 실험 | 한 부품 안의 정렬 축은 하나 | 수치·표지·설명 모두 가운데 |

**여백 규칙**
- 부품 안 마지막 요소의 아래 여백은 0이다. 부품 사이 여백은 부품 쪽 `margin`이 정한다(본문 단락 여백이 부품 안으로 새어 들지 않게 한다).
- 그림 위 소개 문장(`그림은 ~을 나타낸 것이다.`)과 그림 사이, 그림과 해석 문장 사이는 같은 간격을 쓴다.
- 한 번에 한 단계만 보이는 부품(수식 유도)에는 단계 사이 구분선을 두지 않는다.
- 절대 위치(`position: absolute`) 라벨은 기준이 되는 부모에 `position: relative`가 있을 때만 쓴다. 없으면 라벨이 문서 맨 위로 빠져나간다.

### SVG 속 한글 주의사항

- SVG `<text>`는 자동 줄바꿈이 없고, 한글은 글자당 폭이 넓습니다. 노드 폭은 **한글 1자 ≈ 1em**(라틴은 약 0.55em)으로 계산하세요. 예: 14px 글꼴의 한글 8자 라벨은 약 112px에 좌우 여백을 더한 폭이 필요합니다.
- 글꼴은 `font-family` 속성 대신 CSS로 지정합니다. `styles.css`의 `.svg-diagram text`가 이미 `var(--font-body)`를 적용하므로 Pretendard 폴백이 자동으로 적용됩니다. 별도로 지정해야 하면 `style="font-family: var(--font-body)"`를 쓰세요.
- **라벨 방식(하나로 통일):** 상자 안 라벨은 줄 수와 관계없이 `<foreignObject>` 안의 `.node-label > span`으로 씁니다. `word-break: keep-all`로 어절 단위로 줄이 바뀌고, 상자의 세로 가운데에 놓입니다. `<text>`는 상자 밖의 짧은 표지(축 이름, 간선 라벨)에만 씁니다.
- **수학 기호는 이탤릭, 한글은 똑바로.** 수학 기호를 담은 `<text>`는 `font-style="italic"`을 쓴다(`.mi`·KaTeX 수학 글꼴과 맞춘다). 한글 라벨은 이탤릭을 쓰지 않고, 구분이 필요하면 `font-weight="500"`이나 흐린 `fill`을 쓴다. `foreignObject` 라벨 속 기호는 `<i class="mi">q</i>`, 아래첨자는 `<i class="mi">d</i><sub>k</sub>`이다.

### 개념 그림 클래스와 페이지 넘김

- `.figure`, `.svg-diagram` 안의 그림 클래스: `.ink`, `.ink.strong`, `.ink-fill`, `.accent`, `.accent-fill`, `.guide`, `.guide-axis`, `.guide-fill`, `.row-accent`, `.edge-line.thin`, `.edge-line.dashed`, `.dot`, `.dot-accent`, `text.mono|muted|accent-text`. 색 사용 기준은 [색상 규약](#색상-규약)을 따른다. 캡션은 `.figure-caption`, 너비 맞춤은 `.svg-diagram.fit`(`--diagram-max`: 그림 최대 폭, 기본 100%). 본문 옆 그림 폭은 `figure.figure.side`의 `--figure-side-width`(기본 200px). 라벨 속 수학 기호는 `.mi`, 각진 노드는 `.node-rect.sq`. 새 개념마다 이런 그림을 하나 두고, 본문 옆(`.with-figure` + `figure.figure.side`)에 놓아 페이지가 765px를 넘지 않게 한다.
- 모듈 번호는 `1, 2, 3 …` 연속 정수이다. 논문 위치는 화면 제목 끝의 `.paper-ref`(작고 흐린 태그)로 적는다. `.sec-num`은 폐기됐다(CSS만 남김).
- 페이지 넘김: `html { scroll-padding-top: var(--nav-height) }`, `.module { scroll-snap-align: start; scroll-margin-top: calc(-1 * var(--nav-height)) }`. 우하단 고정 `.pager`(‹ n / N ›와 안내 문구)는 `main.js`가 넣는다.

### 도식 간선은 직각으로

노드를 잇는 간선은 수평·수직 선분만 쓴다(`<path d="M x,y H … V … H …">`). 대각선 간선은 쓰지 않는다. 여러 노드로 갈라질 때는 세로 버스 한 줄에서 직각으로 분기한다. 화살촉은 마지막 수평 선분 끝에 둔다. 좌표평면의 벡터 화살표는 간선이 아니므로 방향 그대로 그린다. 노드 위치는 간선 때문에 옮기지 않는다.

### 헤더 세로 정렬

- 상단 내비게이션의 제목과 점은 본문 열과 같은 세로선에 놓는다. 제목의 왼쪽 끝은 단서 칸 왼쪽, 점의 오른쪽 끝은 노트 칸 오른쪽이다(1025px 이상, `styles.css` "헤더 세로 정렬").
- 단원 도입의 번호 상자(64px)는 제목과 부제를 묶은 덩어리와 위아래 끝을 맞춘다. 제목 `line-height: 1.15`, 부제 위 여백 4px로 덩어리 높이가 64px 안팎이 되게 한다. 제목이나 부제를 두 줄로 쓰지 않는다.
