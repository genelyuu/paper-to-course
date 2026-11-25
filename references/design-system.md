# 디자인 시스템 레퍼런스

paper-to-course 시스템의 CSS 디자인 토큰 전체 목록입니다. `styles.css`는 수정 없이 그대로 강의 디렉터리에 복사하고, 강조색만 `_base.html`에서 바꿉니다.

## 목차
1. [디자인 아이덴티티](#디자인-아이덴티티)
2. [색상 팔레트](#색상-팔레트)
3. [타이포그래피](#타이포그래피)
4. [한글 타이포그래피](#한글-타이포그래피)
5. [간격과 레이아웃](#간격과-레이아웃)
6. [그림자와 깊이](#그림자와-깊이)
7. [수식·연구 색상](#수식연구-색상)
8. [SVG 다이어그램 시스템](#svg-다이어그램-시스템)

---

## 디자인 아이덴티티

- 한글+라틴 본문: **Pretendard Variable** (jsDelivr, `v1.3.9` 고정, dynamic-subset으로 필요한 글리프만 로드)
- 라틴 디스플레이(제목의 영문·숫자): **Bricolage Grotesque** (Google Fonts). 한글 글리프는 자동으로 Pretendard로 폴백됩니다.
- 코드: **JetBrains Mono** → D2Coding / Nanum Gothic Coding → Pretendard (한글 주석용 폴백)
- 따뜻한 오프화이트 배경과 주홍색(vermillion) 강조색 — 색 체계는 그대로 유지합니다.

---

## 색상 팔레트

```css
:root {
  /* BACKGROUNDS */
  --color-bg:             #FAF7F2;       /* warm off-white */
  --color-bg-warm:        #F5F0E8;       /* alternating modules */
  --color-bg-code:        #1E1E2E;       /* code blocks */
  --color-text:           #2C2A28;
  --color-text-secondary: #6B6560;
  --color-text-muted:     #9E9790;
  --color-border:         #E5DFD6;
  --color-border-light:   #EEEBE5;
  --color-surface:        #FFFFFF;
  --color-surface-warm:   #FDF9F3;

  /* ACCENT (pick ONE — vermillion default) */
  --color-accent:         #D94F30;
  --color-accent-hover:   #C4432A;
  --color-accent-light:   #FDEEE9;
  --color-accent-muted:   #E8836C;

  /* SEMANTIC */
  --color-success:        #2D8B55;
  --color-success-light:  #E8F5EE;
  --color-error:          #C93B3B;
  --color-error-light:    #FDE8E8;
  --color-info:           #2A7B9B;
  --color-info-light:     #E4F2F7;

  /* ACTORS (research participants, methods, concepts) */
  --color-actor-1:        #D94F30;
  --color-actor-2:        #2A7B9B;
  --color-actor-3:        #7B6DAA;
  --color-actor-4:        #D4A843;
  --color-actor-5:        #2D8B55;
}
```

---

## 타이포그래피

```css
:root {
  /* 라틴은 첫 폰트, 한글은 Pretendard로 자연스럽게 폴백 */
  --font-display: 'Bricolage Grotesque', 'Pretendard Variable', Pretendard, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', Georgia, sans-serif;
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
| 이탤릭 금지 | `em`/`i` → `font-style: normal` + 굵기 600 + 강조색 | 한글에는 이탤릭 글리프가 없어 가짜 기울임(synthetic oblique)이 어색합니다. `font-synthesis: none`으로 합성도 막습니다. KaTeX의 이탤릭은 유지합니다. |
| 드러냄표 | `.ko-emphasis` (`text-emphasis: dot`) | 한국어 전통 강조법. 선택 사항 유틸리티입니다. |
| 라틴/한글 혼용 | 폰트 스택에서 라틴 폰트 → Pretendard | 영문·숫자는 Bricolage, 한글은 Pretendard로 글리프 단위 폴백됩니다. 본문은 Pretendard 하나로 두 문자 모두 일관된 굵기를 가집니다. |
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
  --nav-height:         50px;
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
  --radius-full: 9999px;
}
```

---

## 그림자와 깊이

```css
:root {
  --shadow-sm: 0 1px 2px rgba(44,42,40,0.05);
  --shadow-md: 0 4px 12px rgba(44,42,40,0.08);
  --shadow-lg: 0 8px 24px rgba(44,42,40,0.10);
  --shadow-xl: 0 16px 48px rgba(44,42,40,0.12);
}
```

---

## 수식·연구 색상

```css
:root {
  /* MATH — for equation blocks and derivations */
  --color-math-bg:        #F8F6F1;       /* warm cream */
  --color-math-border:    #D4C5A9;       /* warm gold */
  --color-math-text:      #3D3428;       /* dark brown */

  /* RESEARCH — for lineage/context elements */
  --color-research-bg:    #F0F4F8;       /* cool blue-gray */
  --color-research-accent:#2A5F8F;       /* deep blue */

  /* RESULTS — for experimental result displays */
  --color-result-pos:     #2D8B55;       /* green for improvements */
  --color-result-neg:     #C93B3B;       /* red for underperformance */
  --color-result-neutral: #6B6560;       /* gray for baselines */
}
```

---

## SVG 다이어그램 시스템

모든 다이어그램(순서도, 개념도, 계보 트리, 실험 구성)은 아래 규칙을 따르는 인라인 SVG로 만듭니다.

- 컨테이너: `.svg-diagram` 클래스 — 반응형, 최대 폭 800px, 가운데 정렬
- 노드: `.node-rect`(기본) 또는 `.node-rect.accent`(강조)
- 간선: `.edge-line`(기본) 또는 `.edge-line.accent`
- 텍스트: `var(--font-body)`를 상속하고, 코드는 `.mono` 클래스(`var(--font-mono)`) 사용
- 색상: CSS 변수 사용 (`var(--color-accent)`, `var(--color-border)` 등)
- ViewBox: `viewBox="0 0 WIDTH HEIGHT"`와 `width="100%"`로 반응형 처리
- 3줄 이상의 라벨·문단: `<foreignObject>`로 HTML 텍스트 블록 삽입

```html
<svg class="svg-diagram" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect class="node-rect accent" x="300" y="20" width="200" height="60" />
  <text x="400" y="55" text-anchor="middle" font-weight="700">이 논문</text>
  <line class="edge-line accent" x1="400" y1="80" x2="400" y2="120" />
  <polygon class="edge-arrow accent" points="395,120 405,120 400,130" />
  <!-- 나머지 요소 -->
</svg>
```

### SVG 속 한글 주의사항

- SVG `<text>`는 자동 줄바꿈이 없고, 한글은 글자당 폭이 넓습니다. 노드 폭은 **한글 1자 ≈ 1em**(라틴은 약 0.55em)으로 계산하세요. 예: 14px 글꼴의 한글 8자 라벨은 약 112px에 좌우 여백을 더한 폭이 필요합니다.
- 글꼴은 `font-family` 속성 대신 CSS로 지정합니다. `styles.css`의 `.svg-diagram text`가 이미 `var(--font-body)`를 적용하므로 Pretendard 폴백이 자동으로 적용됩니다. 별도로 지정해야 하면 `style="font-family: var(--font-body)"`를 쓰세요.
- **줄 수별 규칙(하나로 통일):** 한 줄 라벨은 `<text>`를 씁니다. 두 줄이면 `<tspan x="…" dy="1.3em">`으로 나눌 수 있으나 어절 경계에서만 끊고 어절 중간에서는 끊지 마세요. 세 줄 이상이거나 문단 길이의 텍스트는 `<foreignObject>` 안의 `<div>`에 `word-break: keep-all`을 적용해 어절 단위로 줄이 바뀌게 합니다. (`gotchas.md`와 같은 규칙)
- SVG 텍스트에 `font-style="italic"`을 쓰지 않습니다. 한글에는 이탤릭이 없으므로 `font-weight="500"`이나 흐린 `fill`로 구분합니다.
