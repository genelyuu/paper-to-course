# 인터랙티브 요소 레퍼런스

paper-to-course 튜토리얼의 인터랙티브 요소 구현 패턴이다.

> CSS·JS는 `references/styles.css`·`references/main.js`에 있고 강의 디렉터리에 그대로 복사된다. 아래 HTML만 쓰고 인라인 `<style>`·`<script>`는 쓰지 않는다. 클래스명, `data-*` 속성명, id, HTML 구조는 두 파일이 의존하므로 바꾸지 않는다. 사람이 읽는 텍스트와 속성 값(`data-definition`, `data-explanation-right` 등)만 한국어로 쓴다.

## 목차
아래 `##` 제목 순서와 같다: 작성 원칙 → 모듈 골격 → 코넬 지면(개념 그림·페이지 넘김) → 표지 → 요소별 패턴(수식 유도 … 아이콘 라벨 행) → 첫 페이지·계보·구조도 패턴.

## 한국어 콘텐츠 작성 원칙 (요약)

자세한 규칙은 `references/korean-style-guide.md`.
- **문체(교육 도메인 학습서 문체):** 본문·설명·콜아웃·카드·해설·피드백은 한다체 평서형(`~이다 / ~한다 / ~된다`). 툴팁 정의(`data-definition`)만 명사형 종결(`~것.`, `~함.`, `~임.`, 명사). `여러분`, 수사적 의문문, 감탄, 칭찬 금지. 연구 대화 대사만 해요체 허용.
- **문항 형식:** 발문은 `다음 중 ~에 대한 설명으로 옳은 것은?` / `~으로 옳지 않은 것은?`, 지시는 `~하시오`. 선택지 텍스트 앞에 `①②③④`(`data-value`·`data-correct` 값은 그대로). `정답`/`오답` 표지는 `main.js`가 붙이므로 해설에 쓰지 않는다: `data-explanation-right="② | ~이므로 ~이다."`, `data-explanation-wrong="| 정답은 ②이다. ~이므로 ~이다."`.
- **코너 이름:** `학습 목표`(모듈 맨 앞), `개념 체크`(용어·정의 확인), `탐구 자료`(실험 결과·그래프·대화), `보충 설명`(`callout-info`), `핵심 정리`(`callout-accent`), `더 알아보기`(오해·심화, `callout-warning`), 모듈 끝 문항 묶음 `확인 문제`.
- **학습 목표:** 모듈 맨 위 `이 모듈을 학습하면 다음을 할 수 있다.` 다음에 `GRPO의 어드밴티지 계산 과정을 설명할 수 있다.`처럼 `~을 설명할 수 있다 / ~을 비교할 수 있다` 2~3개.
- **용어 첫 등장:** `한글 용어(English Term)`, 이후 한글만. 약어는 `한글 풀이(English Full Name, ACRONYM)`(`저랭크 적응(Low-Rank Adaptation, LoRA)`), 이후 약어만. 약어가 이름처럼 굳었으면(GRPO, BLEU, GPU) `ACRONYM(English Full Name, 한글 풀이)`도 허용. 트랜스포머, 어텐션 같은 관용 표기는 따른다.
- **괄호:** 항상 ASCII 반각 `( )`, 괄호 앞 공백 없음. 전각 괄호(U+FF08, U+FF09) 금지.
- **조사:** 영문·숫자·수식 뒤는 발음 기준(`LoRA를`, `GRPO는`, `PPO가`, `$x$는`).
- **숫자·단위:** 한글 단위 명사와 `%`, `%p`, `°`는 붙인다(`7개`, `45분`, `3.2%p`). 라틴 SI·컴퓨팅 단위 기호는 띄운다(`3 kg`, `10 ms`, `16 GB`). 모델 규모 `1.7B`는 붙인다.
- **인용:** 큰따옴표 “ ” 또는 " ". 작은따옴표는 속성 값 충돌 때문에 되도록 쓰지 않는다.
- **수식 띄어쓰기:** 인라인 `$...$` 앞뒤 한 칸, 조사는 수식 뒤에 붙인다(`$A_i$는`).

## 모듈 골격과 내비게이션 (Module Skeleton & Navigation)

**공통 레이아웃은 코드로 찍는다.** 머리(`_base.html` + `templates/nav.html`), 꼬리(`_footer.html`), 단원 머리말·코넬 쪽·단서 칸·확인 문제(`templates/*.html`)는 손으로 쓰지 않고 `python3 -I references/scaffold.py init <course> <spec.json>`으로 만든다(형식은 `templates/course.example.json`). 작성자는 `.notes` 본문과 빈자리 `[작성 필요: …]`만 채운다. 남은 빈자리는 `scaffold.py todo <course>`가 보여 주고 `check-pages.py`가 LAY로 막는다. 아래 마크업은 틀이 만드는 결과이다.

**연결:** `main.js`는 `.module`을 문서 순서대로 모아 `.nav-dot`, `.sidebar-item`과 같은 인덱스로 짝짓는다. 셋의 개수와 순서가 같아야 한다. 점은 `data-target` id로, 사이드바는 `href` id로 스크롤한다. 표지(`.course-cover`)는 짝에 들지 않는다.

**모듈 파일(`modules/0N-slug.html`):** 모든 화면은 `.screen.cornell` 한 페이지이고, `.module-header`와 첫 코넬 화면이 함께 첫 페이지를 이룬다.
```html
<section class="module" id="module-1">
  <div class="module-content">
    <div class="module-header">
      <span class="module-number">2</span>
      <h2 class="module-title">어텐션</h2>
      <p class="module-subtitle">토큰 사이의 관련도를 계산하는 과정을 익힌다</p>
    </div>
    <!-- 첫 페이지: 단원 도입 + 첫 코넬 화면(학습 목표 상자는 .cue 또는 .notes 맨 위) -->
    <div class="screen cornell">
      <aside class="cue">
        <span class="cue-label">핵심 질문</span>
        <ul><li>어텐션은 무엇을 계산하는가?</li><!-- 2~4개 --></ul>
      </aside>
      <div class="notes">
        <h3 class="screen-heading">화면 제목</h3>
        <p>본문(한다체)...</p>
      </div>
      <div class="summary"><span class="summary-label">요약</span><p>쿼리와 키의 내적으로 관련도를 구한다.</p></div>
    </div>
    <!-- 이어지는 페이지: 개념 설명, 개념 체크, 탐구 자료 (같은 골격 반복) -->
    <!-- 끝: 핵심 정리(callout) → 확인 문제 페이지:
         <h3 class="screen-heading"><span class="corner-tag outline">확인 문제</span>어텐션 연산</h3>
         <div class="quiz-container" id="quiz-module1">...</div> -->
  </div>
</section>
```

**Rules:**
- `id="module-N"`의 `N`은 0부터 연속(메뉴보다 적게 만들어도 건너뛰지 않는다). 파일명도 `00-`, `01-`, ….
- `.module-number`는 모듈 연속 번호(`1`, `2`, `3` …)이다. 논문 절 번호(`3.2`, `1–2`)나 `0`을 쓰지 않는다. CSS가 64px 교과 색 블록에 흰 숫자로 그리고, `.module-header`는 2px 교과 색 선으로 닫힌다.
- `.module-title`은 논문 절 제목의 한국어 번역이다. 논문 위치는 화면 제목 끝 `.paper-ref`에 쓴다: `<h3 class="screen-heading">스케일드 내적 어텐션<span class="paper-ref">논문 3.2.1절</span></h3>`.
- 제목 단계: 모듈 `<h2 class="module-title">`, 화면 `<h3 class="screen-heading">`, 화면 안 소제목 `<h4>`.
- 모듈당 본문 화면 3~8개(확인 문제 쪽 제외), 각각 한 페이지. 코넬이 아닌 `.screen`은 쓰지 않는다(`check-pages.py`가 보고).
- 한 페이지는 1440×900에 스크롤 없이 들어간다. 넘치면 내용을 줄이지 말고 페이지를 나눈다.
- `.module-content` 밖에 `<html>`, `<head>`, `<script>`를 두지 않는다.

**배경 지식 표시:** 논문 이전 배경만 다루는 화면(모듈 0의 둘째 쪽부터, 그 밖의 배경 전용 화면)은 맨 위에 아래 콜아웃을 둔다. 모듈 0의 첫 쪽은 논문 1절 "왜 썼나·새로운 점" 쪽이므로 `.paper-ref`(논문 1절)를 달고 이 콜아웃을 두지 않는다("첫 페이지: 왜 썼는가와 새로운 점"). 논문 주장을 다루는 화면에는 쓰지 않고, 화면 제목에 `배경 지식 1.` 같은 접두어를 붙이지 않는다. `보충 설명`·`더 알아보기` 모듈당 2개 상한에 넣지 않는다.
```html
<div class="callout callout-info animate-in">
  <div class="callout-content">
    <strong class="callout-title">배경 지식</strong>
    <p>이 화면은 논문의 주장이 아니라 논문을 읽기 위해 먼저 알아 둘 배경이다.</p>
  </div>
</div>
```

**`_base.html` NAV_DOTS / SIDEBAR_ITEMS(모듈마다 하나씩):**
```html
<button class="nav-dot" data-target="module-1" data-tooltip="2 어텐션" aria-label="2단원 어텐션"></button>
<a class="sidebar-item" data-module="1" href="#module-1"><span class="sidebar-item-num">2</span><span class="sidebar-item-label">어텐션</span><span class="sidebar-item-indicator"></span></a>
```
- `data-target`은 `#` 없이 id, `href`는 `#module-1`.
- `data-tooltip`은 `연속 번호 + 제목`(`2 어텐션`), `aria-label`은 `2단원 어텐션`.
- `sidebar-item-num`은 모듈 번호(앞에 0 없음), `sidebar-item-label`은 제목. 표지 `toc-num`도 같은 번호.
- `active`를 미리 붙이지 않는다(`main.js`가 스크롤에 따라 붙인다).

## 코넬식 페이지와 지면 요소

학습서 지면 + 코넬식 노트 레이아웃이다. CSS는 `styles.css` 끝 "TEXTBOOK PAGE LAYOUT", 와이어프레임은 `design-system.md` "지면 레이아웃".

### 구조: `.screen.cornell`

- `.cue`(왼쪽, 232px): `<span class="cue-label">핵심 질문</span>` + `<ul>` 핵심 질문 2~4개(한다체 의문형 `~는가?`, `~인가?`). 용어 정리 페이지는 `<dl>`(`<dt>` 용어, `<dd>` 뜻).
- `.notes`(오른쪽): 화면 제목과 본문, 수식, 그림, 퀴즈 전부.
- `.summary`(아래): `<span class="summary-label">요약</span><p>한다체 한 문장</p>`.
- 세 영역을 모두 둔다(마크업은 위 모듈 골격과 같다). 1200px 미만에서는 CSS가 한 단으로 접고 높이 제한을 푼다.
- 콜아웃을 `.cue` 안에 둘 수 있다(학습 목표는 첫 페이지 `.cue`에 둘 수 있다). `.notes` 맨 위 콜아웃은 위쪽 여백이 없어진다.

### 쪽 맞춤 규칙 (page-fit)

- 1440×900에서 브라우저 UI와 48px 내비게이션을 뺀 약 765px 안에 스크롤 없이 들어간다. 첫 페이지는 `.module-header`를 포함해 잰다.
- 넘치면 글을 줄이지 말고 페이지를 나누며, 페이지마다 핵심 질문과 요약을 따로 둔다.
- 높은 SVG는 `viewBox`를 유지하고 `max-height`를 둔다. 표와 코드도 높이를 고려한다.
- 퀴즈는 한 페이지에 최대 2문항.
- 작성 후 `python3 references/check-pages.py <course-dir>`로 넘침 0개를 확인한다.

### 코너 이름표: `.corner-tag`

`.screen-heading` 안 맨 앞에 붙는 칩이다. `.corner-tag`는 교과 색 바탕 흰 글자, `.corner-tag.outline`은 테두리만. 코너 이름이 없는 제목은 태그 없이 쓰며 CSS가 교과 색 네모 표지를 붙인다.
```html
<h3 class="screen-heading"><span class="corner-tag">탐구 자료</span>번역 성능 비교</h3>
<h3 class="screen-heading"><span class="corner-tag outline">개념 체크</span>소프트맥스</h3>
```
**개념 체크**는 개념 설명 쪽 끝의 짧은 확인 문항 하나다. 전용 클래스가 없으므로 `.quiz-container` 하나에 문항 1개(선택지 3~4개, `.q-points` 없음)를 넣는다. 마크업은 "객관식 퀴즈"와 같고 id만 `check-module2a`처럼 쓴다.

### 날개: `.wing`

코넬이 아닌 화면의 여백 메모(코넬 화면은 `.cue`가 대신한다). 1200px 이상에서 왼쪽 여백에 뜨고, 좁으면 본문 사이 상자가 된다.
```html
<div class="wing"><span class="wing-title">참고</span>짧은 보충 한두 문장</div>
```

### 단원 도입과 표지 요소

- `.paper-ref`: 화면 제목 끝의 작은 논문 위치 태그. 논문의 해당 절에서 온 화면에만 붙이고 논문 밖 배경·확장 화면(모듈 0 등)에는 붙이지 않는다. 모듈 번호와 별개이다. `.sec-num`(제목 앞 절 번호)은 폐기됐으니 쓰지 않는다.
- `.course-cover`: 아래에 8px 교과 색 띠가 붙는다.

### 개념 그림 (Concept Figures)

새로 도입하는 개념·알고리즘·수식마다 코드로 그린 그림을 하나 둔다(없으면 안 된다). 숫자는 본문과 같게 하고, 765px를 넘지 않도록 `.with-figure` + `figure.figure.side`로 본문 옆에 둔다.
- 선·면: `.ink`, `.ink.strong`, `.ink-fill`(먹색), `.accent`, `.accent-fill`(교과 색), `.guide`, `.guide-axis`, `.guide-fill`(격자·축·보조 면), `.row-accent`(강조 행), `.edge-line.thin`, `.edge-line.dashed`, `.dot`, `.dot-accent`
- 글자: `text.mono`, `text.muted`, `text.accent-text`. 수학 기호는 라벨 안 `<i class="mi">q</i>`, SVG `<text>`에서는 `font-style="italic"`.
- 모양·크기: `.node-rect.sq`(거의 직각, 행렬·칩). 옆 그림 폭은 `figure.figure.side`의 `--figure-side-width`(기본 200px). 너비 맞춤은 `.svg-diagram.fit` + `--diagram-max`. 설명은 `.figure-caption`.
- 색은 먹색 + 교과 색 + 회색만, 그림당 유채색 하나(`design-system.md` "색상 규약").
- 예: 격자 위 내적 벡터, 소프트맥스 가중치 막대, 행렬 형상 n×d_k · d_k×n = n×n, 스케일 전후 소프트맥스 막대, 멀티헤드 분할 512→8×64→연결, BLEU n-gram 겹침 칩.

### 페이지 넘김 (Page Navigation)

`main.js`의 `initPager()`가 쪽(표지, 모듈마다 단원 도입+첫 화면, 이후 각 `.screen`)을 모은다. ←/↑/PageUp 이전, →/↓/PageDown 다음, Home/End 처음/끝. 우하단 `.pager`는 JS가 넣으므로 마크업하지 않는다. `.module`에는 `scroll-snap-align: start`와 `scroll-margin-top`이 걸려 있다.

**Space:** 현재 페이지의 주 버튼을 누른다. 우선순위: 수식 유도 다음 단계 → 의사코드 다음 줄 → 대화 다음 말풍선 → 전환 버튼·탭(`.result-metric-toggle`, `.ablation-tabs`, `.layer-tabs`) 다음 항목 → 문제 정답·해설 공개(선택 없이) → 다음 페이지. Shift+Space는 거꾸로 되돌리고, 되돌릴 것이 없으면 이전 페이지. 그래서 한 페이지에 주 인터랙티브 요소는 가능하면 하나만 둔다. 버튼은 마우스용으로 그대로 둔다. 방향키나 Space를 `preventDefault`하는 `keydown` 핸들러를 추가하지 않는다.

## 표지와 히어로 섹션 (Cover Page)

모든 모듈 앞의 전체 화면 랜딩 페이지이다. `.module`이 아니므로 내비게이션 점·모듈 번호·`scroll-snap-align`이 없다. "학습 시작하기"는 `main.js`의 표지 CTA 리스너가 모듈 0으로 스크롤한다.
```html
<section class="course-cover">
  <div class="course-cover-inner">
    <div class="course-cover-main">
      <span class="course-cover-badge">인터랙티브 튜토리얼</span>
      <h1 class="course-cover-title">프롬프트 공간 교란이 추론 탐색을 넓히는 방법</h1>
      <p class="course-cover-original" lang="en">Nonsense Helps</p>
      <p class="course-cover-subtitle">프롬프트에 노이즈를 더하면 추론 탐색이 넓어지는 원리를 알아본다</p>
      <p class="course-cover-authors">Yuntao Bai et al.</p>
      <div class="course-cover-meta">
        <span class="course-cover-meta-item">arXiv 2026</span>
        <span class="course-cover-meta-item">모듈 7개</span>
        <span class="course-cover-meta-item">약 45분</span>
        <span class="course-cover-meta-item">중급</span>
      </div>
      <div class="course-cover-abstract">
        <span class="course-cover-abstract-label">초록</span>
        <p>2~3문장 요약(한다체)...</p>
      </div>
      <a href="#module-0" class="course-cover-cta">학습 시작하기</a>
    </div>
    <nav class="course-cover-toc" aria-label="차례">
      <span class="course-cover-toc-label">차례</span>
      <ol>
        <li><a href="#module-0"><span class="toc-num">1</span>서론과 배경</a></li>
        <!-- 모듈마다 반복 -->
      </ol>
    </nav>
  </div>
</section>
```

**Rules:**
- 왼쪽 `.course-cover-main`은 왼쪽 정렬 제목 영역, 오른쪽 `.course-cover-toc`는 교과 색 면 위 차례(1024px 미만에서 아래로 내려감). 차례는 사이드바 번호·제목과 같고 `href`는 `#module-N`.
- 버튼 문구 뒤에 `→` 같은 화살표를 붙이지 않는다.
- 한국어 제목은 `.course-cover-title`, 영어 원제는 바로 아래 `.course-cover-original`. 제목 안에 원제를 괄호로 붙이지 않는다. 배지·라벨 문구는 예시 그대로("인터랙티브 튜토리얼", "초록", "차례").
- 저자 줄에는 저자만. 발표처·연도는 메타 첫 항목(`arXiv 2026`)으로 옮기고 가운뎃점(`·`)으로 잇지 않는다.
- 초록은 2~3문장으로 줄인다.
- 메타: 발표처·연도, 모듈 수, 예상 소요 시간(모듈당 5~7분), 난이도. 이모지 없음, 숫자·단위 붙여 쓰기(`모듈 7개`, `약 45분`).
- 난이도: 초급(사전 지식 불필요), 중급(분야 기초 지식 필요), 고급(상당한 수학·분야 배경 필요).

## 수식 유도 단계별 풀이 (Math Derivation Walkthrough)

가장 중요한 교육 요소이다. `main.js`가 모든 `.math-derivation`을 초기화한다(단계 `.math-step`, 컨트롤 `.math-next-btn`·`.math-prev-btn`·`.math-reset-btn`, 진행 `.math-progress`).
```html
<div class="math-derivation animate-in" id="math-deriv-1">
  <div class="math-step" data-step="0">
    <div class="math-equation">
      $$L_{\mathit{GRPO}} = -\mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \rho_i A_i, \mathit{clip}(\rho_i) A_i \right) \right] \tag{1}$$
    </div>
    <div class="math-explanation">
      <p>$\rho_i$는 새 정책과 이전 정책의 확률 비이고, 어드밴티지(Advantage) $A_i$는 각 응답이 평균에 비해 얼마나 좋은지를 나타낸다.</p>
    </div>
  </div>
  <div class="math-step" data-step="1" style="display:none">
    <div class="math-equation">$$A_i = \frac{r_i - \mathit{mean}(\{r_1, ..., r_G\})}{\mathit{std}(\{r_1, ..., r_G\})}$$</div>
    <div class="math-explanation"><p>각 응답의 보상에서 평균을 빼고 표준편차로 나눈다.</p></div>
  </div>
  <!-- 단계 추가 -->
  <div class="math-controls">
    <button class="btn math-prev-btn">이전 단계</button>
    <button class="btn math-next-btn">다음 단계</button>
    <button class="btn math-reset-btn">처음부터</button>
    <span class="math-progress"></span>
  </div>
</div>
```

**Rules:**
- 단계마다 변형 하나 또는 통찰 하나. "미분한다" 같은 기계적 서술이 아니라 쉬운 말로 푼다.
- 수식은 모두 이탤릭: 함수 이름·첨자 낱말은 `\mathit{}`, 벡터는 `\boldsymbol{}`. `\text`·`\mathrm`·`\mathbf` 금지(KO112). 논문에 번호가 있는 식에만 `\tag{n}`. 상세는 `korean-style-guide.md` §7.
- KaTeX가 `$$...$$`를 렌더링하고 새 단계가 보일 때 `main.js`가 다시 렌더링한다. 설명 속 인라인 수식은 `$...$`.

## 의사코드 단계별 풀이 (Pseudocode Walkthrough)

왼쪽 알고리즘, 오른쪽 줄 단위 설명. `main.js`가 모든 `.pseudocode-translation`을 초기화한다.
```html
<div class="pseudocode-translation animate-in" id="pseudo-lope">
  <div class="pseudocode-block">
    <span class="translation-label">알고리즘</span>
    <span class="pseudocode-line">INPUT: 프롬프트 q, 모델 π, 교란 텍스트 P  // 입력</span>
    <span class="pseudocode-line">FOR i = 1 TO G DO  // G번 반복</span>
    <!-- 줄 반복 -->
  </div>
  <div class="pseudocode-explanation">
    <span class="translation-label">설명</span>
    <div class="pseudocode-explanation-lines">
      <p class="pe">입력은 원래 질문, 현재 모델, 교란에 쓸 텍스트(예: Lorem Ipsum)이다.</p>
      <p class="pe">각 샘플링 그룹마다 G번 반복한다.</p>
      <!-- 줄마다 하나 -->
    </div>
  </div>
  <div class="pseudocode-controls">
    <button class="btn pseudocode-prev-btn">이전 줄</button>
    <button class="btn pseudocode-next-btn">다음 줄</button>
    <button class="btn pseudocode-reset-btn">처음부터</button>
    <span class="pseudocode-progress"></span>
  </div>
</div>
```

**Rules:**
- `.pseudocode-line`과 `.pe`는 1:1로 대응한다.
- `.pseudocode-controls`는 반드시 `.pseudocode-translation` **안**에 둔다(밖에 두면 동작하지 않는다).
- 두 열 비율은 `style="--col-a:1.5fr"`(왼쪽 코드)·`--col-b`(오른쪽 설명)로 바꾼다. 인라인 `grid-template-columns`는 쓰지 않는다(lint KO114).
- **코드 색:** IDE 토큰 색(Catppuccin, `.code-keyword`·`.code-function`·`.code-comment`·`.code-number`·`.code-operator`·`.code-string`)을 `main.js`가 자동으로 칠한다(대문자 제어어 INPUT, FOR, DO, END, OUTPUT …은 키워드, `이름(`은 함수, `//` 뒤는 주석, 숫자, `= / * + -`). 줄은 일반 텍스트로 쓴다. 직접 `<span class="code-…">`로 칠한 줄은 건드리지 않는다. 새 색을 정하지 않는다.
- 언어 중립으로 쓴다. `INPUT`, `OUTPUT`, `FOR EACH`, `IF...THEN` 키워드는 영어(Python/C++ 문법 금지), 주석과 설명만 한국어.
- 설명은 "무엇을"과 "왜"를 한다체로 쓴다.

## 결과 비교 인터랙티브 (Result Comparison)

방법·설정별 결과 막대 차트. `main.js`가 모든 `.result-comparison`을 초기화하고, 지표를 전환하면 막대 너비와 값을 갱신한다.
```html
<div class="result-comparison animate-in" data-unit="%" data-max="100">
  <div class="result-header">
    <h4>수학 추론 벤치마크 결과</h4>
    <div class="result-metric-toggle">
      <button class="result-metric active" data-metric="accuracy">정확도</button>
      <button class="result-metric" data-metric="pass1">Pass@1</button>
    </div>
  </div>
  <div class="result-bars">
    <div class="result-bar" data-accuracy="78.3" data-pass1="65.2">
      <span class="result-label">LoPE (본 논문)</span>
      <div class="result-bar-track"><div class="result-fill ours" style="width:0%"></div></div>
      <span class="result-value"></span>
    </div>
    <div class="result-bar" data-accuracy="72.1" data-pass1="58.7">
      <span class="result-label">GRPO 기준 모델</span>
      <div class="result-bar-track"><div class="result-fill baseline" style="width:0%"></div></div>
      <span class="result-value"></span>
    </div>
    <!-- 막대 반복 -->
  </div>
</div>
```

**Rules:**
- 제안 방법은 `.result-fill.ours`(강조색), 기준 모델은 `.result-fill.baseline`(회색).
- `data-unit` 기본 `%`, 단위 없는 지표(BLEU)는 `data-unit=""`. `data-max`는 눈금 최댓값(기본 100). 값 차이가 작으면 낮춘다(BLEU 25~45면 `data-max="50"`).
- `data-metric` 이름은 `dataset` camelCase 규칙을 따르므로 하이픈이 필요한 이름을 피하고 소문자 한 단어로 쓴다(`data-metric="ende"` ↔ `data-ende="28.4"`; `enDe`는 `data-en-de`로 읽힌다).

## 연구 계보 트리 (Research Lineage Tree)

**CSS 기반 트리:** 노드를 누르면 `data-detail`이 펼쳐진다. 갈래는 `.lineage-branch`를 중첩한다. 갈래 메모·루트 배지는 "연구 계보: 이어받은 것과 달라진 것".
```html
<div class="lineage-tree animate-in">
  <div class="lineage-node lineage-root" data-detail="LoPE: 프롬프트에 노이즈를 더해 탐색을 넓히는 방법">
    <span class="lineage-label">LoPE</span>
    <span class="lineage-detail">본 논문 (2026)</span>
  </div>
  <div class="lineage-branch">
    <div class="lineage-edge-label">개선</div>
    <div class="lineage-node" data-detail="그룹 상대 정책 최적화(Group Relative Policy Optimization): 그룹 내 상대 어드밴티지 추정">
      <span class="lineage-label">GRPO</span>
      <span class="lineage-detail">Shao et al., 2024</span>
    </div>
    <div class="lineage-branch"><!-- 더 이른 선행 연구: 같은 구조로 중첩 --></div>
  </div>
  <!-- 형제 갈래(관련 등) 반복 -->
</div>
```

**SVG 기반 트리(복잡한 계보):** "SVG 다이어그램" 패턴과 규칙을 그대로 쓴다. 노드는 `rect.node-rect` + `foreignObject > div.node-label > span`(`LoPE<br/>본 논문, 2026`), 간선은 직각 `<path class="edge-line">`(예: `d="M400,80 V115 H200 V140"`) + `<polygon class="edge-arrow">`, 본 논문 노드와 그리로 들어가는 간선만 `accent`.

## 연구 대화 (Research Dialogue)

개념을 두고 "토론"하는 메신저형 채팅. `main.js`가 모든 `.chat-window`를 초기화한다. 메시지는 `style="display:none"`으로 두면 JS가 차례로 보인다. 화자 색은 교과 색(`--color-accent`)과 먹색(`#1F2328`) 둘뿐이다. `--color-actor-*`와 이모지는 쓰지 않는다. 대사는 해요체를 허용한다.
```html
<div class="chat-window animate-in" id="chat-module2">
  <div class="chat-messages">
    <div class="chat-message" data-msg="0" data-sender="researcher-a" style="display:none">
      <div class="chat-avatar" style="background: var(--color-accent)">학</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: var(--color-accent)">학생 A</span>
        <p>이건 데이터 증강 아닌가요?</p>
      </div>
    </div>
    <!-- data-msg="1" data-sender="researcher-b": 같은 구조, 아바타·이름 색 #1F2328("교", "교사") -->
  </div>
  <div class="chat-typing" style="display:none">
    <div class="chat-avatar">?</div>
    <div class="chat-typing-dots"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>
  </div>
  <div class="chat-controls">
    <button class="btn chat-next-btn">다음 메시지</button>
    <button class="btn chat-all-btn">전체 재생</button>
    <button class="btn chat-reset-btn">다시 보기</button>
    <span class="chat-progress"></span>
  </div>
</div>
```

## SVG 다이어그램 (SVG Diagrams)

개념 지도, 실험 프레임워크, 알고리즘 흐름, 비교 행렬. 예: 가로 흐름 4단계(같은 폭·간격, 마지막 간선만 강조).
```html
<div class="svg-diagram animate-in">
  <svg viewBox="0 0 800 128" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="그림 내용을 한 문장으로">
    <rect class="node-rect" x="16" y="8" width="156" height="64" rx="12"/>
    <foreignObject x="24" y="12" width="140" height="56"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px; word-break:keep-all; line-height:1.4"><span>원본 프롬프트 <i class="mi">q</i></span></div></foreignObject>
    <path class="edge-line" d="M172,40 H210"/>
    <polygon class="edge-arrow" points="210,45 220,40 210,35"/>
    <!-- 다음 노드 x = 16 + i × (156 + 48) -->
    <foreignObject x="16" y="88" width="768" height="32"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px; color:var(--color-text-secondary)"><span>그림 아래 설명 한 줄</span></div></foreignObject>
  </svg>
</div>
```

**Rules (그림 정렬):**
- **노드 라벨은 `foreignObject` + `.node-label` + `<span>` 하나.** `foreignObject`는 사각형에서 가로 8, 세로 4 안쪽. CSS가 span을 가운데에 두고 `<sub>`를 한 줄 흐름으로 유지한다. span이 없으면 `<sub>` 앞뒤가 떨어진다(`check-pages.py` 검출).
- **같은 단계 노드는 같은 폭·간격.** 가로 흐름 `폭 = (768 − (n−1)×간격) / n`, 시작 x 16. viewBox를 넘으면 안 된다(검출).
- **viewBox는 내용에 맞춘다.** 위아래 여백 8, 높이는 마지막 요소 아래 8에서 끝낸다.
- **간선은 노드 테두리에서 시작해 다른 노드 테두리에서 끝나고 끝에 화살촉이 있다.** 화살촉 길이 10, 반폭 5, 선은 화살촉 밑변에서 멈춘다.
- **간선은 직각.** 대각선 `<line>` 금지, `<path class="edge-line" d="M400,80 V115 H200 V140"/>`처럼 수평·수직 선분. 같은 단계로 갈라질 때는 세로 버스 한 줄에서 분기한다(`design-system.md` "도식 간선은 직각으로").
- 강조(`accent`)는 논문 결론 노드와 그리로 들어가는 간선 하나에만.
- `viewBox` + `width="100%"`, 색은 CSS 변수.
- 한글 라벨은 글자당 약 1em(14px면 약 14px)으로 박스를 넓게 잡는다.
- 수학 기호는 이탤릭(`<i class="mi">q</i>`; 일반 `<i>`는 똑바로 나온다. `<text>`는 `font-style="italic"`), 한글은 똑바로.
- `.node-rect`, `.node-rect.sq`, `.edge-line`, `.edge-arrow`(와 `.accent`)는 `.figure svg` 안에서도 같게 동작한다. 너비·폭·색은 "개념 그림" 참조.

## 문항 삽화 (Question Figure)

발문 아래 그림을 선택지 오른쪽에 둔다(페이지 높이를 늘리지 않는다). 제작 방법은 `illustration.md`.
```html
<div class="quiz-question-block" data-correct="option-d" data-explanation-right="④ | …" data-explanation-wrong="| 정답은 ④이다. …">
  <h3 class="quiz-question"><span class="q-num">3</span>그림은 쿼리 벡터 $\boldsymbol{q}$와 키 벡터 $\boldsymbol{k}_1$을 나타낸 것이다. 이에 대한 설명으로 옳지 <u>않은</u> 것은?</h3>
  <div class="q-body">
    <div class="quiz-options">…선택지 5개…</div>
    <figure class="q-figure" aria-label="그림 내용을 한 문장으로">
      <svg viewBox="0 0 216 136" xmlns="http://www.w3.org/2000/svg" role="img">
        <path class="guide" d="…모눈…"/>
        <line class="ink" …/>                         <!-- 먹선 1.5 -->
        <line class="ink accent" stroke-width="2" …/> <!-- 강조는 하나 -->
        <text font-style="italic" …>O</text>          <!-- 수학 기호는 이탤릭 -->
      </svg>
    </figure>
  </div>
  <div class="quiz-feedback"></div>
</div>
```
- 발문은 `그림은 ~을 나타낸 것이다.`로 그림을 먼저 소개한다. 그림 번호(그림 1)는 쓰지 않는다.
- 색은 먹색 + 교과 색 + 회색만. 클래스: `ink`, `ink-fill`, `accent`·`accent-fill`, `guide`(회색 1px), `accent-text`.
- 폭 기본 280px, `--q-figure-width`로 조절(`style="--q-figure-width: 320px"`). `.q-body` 문항은 선택지가 자동으로 한 줄에 하나(`.row` 불필요). 640px 이하에서 그림이 선택지 아래로 내려간다.
- 탐구 자료 본문 그림은 `<figure class="figure">`(노트 칸 가운데, 최대 60%).
- `check-pages.py`가 래스터 이미지, 불러오지 못한 이미지, 교과 색 외 유채색을 검출한다.

## 객관식 퀴즈 (Multiple-Choice Quizzes)

`main.js`가 `window.selectOption(btn)`, `window.checkQuiz(containerId)`, `window.resetQuiz(containerId)`를 노출한다.
```html
<div class="quiz-container animate-in" id="quiz-module3">
  <div class="quiz-question-block"
       data-correct="option-b"
       data-explanation-right="② | 모든 응답의 보상이 같으면 어드밴티지가 0이 되므로 학습 신호가 없다."
       data-explanation-wrong="| 정답은 ②이다. 모든 응답의 보상이 평균과 같아지므로 어드밴티지가 0이 된다.">
    <h3 class="quiz-question"><span class="q-num">1</span>한 그룹의 모든 응답이 같은 보상을 받을 때 GRPO에 대한 설명으로 옳은 것은?</h3>
    <div class="quiz-options">
      <button class="quiz-option" data-value="option-a" onclick="selectOption(this)"><div class="quiz-option-radio"></div><span>① 응답 하나를 무작위로 정답으로 삼는다.</span></button>
      <button class="quiz-option" data-value="option-b" onclick="selectOption(this)"><div class="quiz-option-radio"></div><span>② 어드밴티지가 0이 되어 모델이 이 그룹에서 학습하지 못한다.</span></button>
      <!-- 선택지 반복(option-c …) -->
    </div>
    <div class="quiz-feedback"></div>
  </div>
  <button class="quiz-check-btn" onclick="checkQuiz('quiz-module3')">정답 확인</button>
  <button class="quiz-reset-btn" onclick="resetQuiz('quiz-module3')">다시 풀기</button>
</div>
```

**Rules:**
- `data-correct`, `data-explanation-right`, `data-explanation-wrong`은 `.quiz-question-block`에 둔다(`.quiz-feedback`이 아니다). 해설 형식은 위 "문항 형식"과 같고 `정답`/`오답` 표지는 쓰지 않는다(KO110).
- 해설 속성 안에 `$…$` 수식을 쓸 수 있다(피드백 삽입 후 KaTeX 재렌더링). 숨은 가정 찾기도 같다.
- 확인 문제는 모듈마다 3~5문항, 하나 이상은 부정형(`옳지 않은 것은?`) 또는 보기형.
- 문항 번호는 `<span class="q-num">1</span>`(텍스트 `1. ` 금지).
- 배점 `<span class="q-points">[3점]</span>`은 어려운 문항 끝에만.
- 선택지가 매우 짧으면(기호, 숫자) `<div class="quiz-options row">`.
- 코넬 페이지 안 1200px 이상에서 문항은 2단(시험지식)으로 놓이고, 정답 확인 버튼은 1열, 다시 풀기는 2열 아래에 놓인다.
- **페이지당 최대 2문항**(선택지 5개씩과 펼쳐진 해설이 765px 안). 3문항 이상이면 `.quiz-container`를 나누어 각각 코넬 페이지에 두고, 각자 고유 id와 자기 버튼(`checkQuiz('quiz-module3a')` 등)을 가진다.

**보기형 문항(`<보기>` 상자):** 발문 바로 아래 `.bogi`. 상자 제목 `<보기>`는 CSS가 표시한다. 텍스트 속 `<보기>`는 `&lt;보기&gt;`로 이스케이프하고 `<span class="nobr">&lt;보기&gt;에서</span>`로 감싼다.
```html
<h3 class="quiz-question"><span class="q-num">1</span>LoPE에 대한 설명으로 옳은 것만을 <span class="nobr">&lt;보기&gt;에서</span> 있는 대로 고른 것은?</h3>
<div class="bogi">
  <p>ㄱ. 프롬프트 앞에 의미 없는 텍스트를 붙여 응답 분포를 넓힌다.</p>
  <p>ㄴ. 보상 함수를 새로 학습해야 한다.</p>
  <p>ㄷ. 어드밴티지가 0인 그룹의 비율을 줄인다.</p>
</div>
<!-- 선택지: ① ㄱ  ② ㄴ  ③ ㄱ, ㄷ  ④ ㄴ, ㄷ  ⑤ ㄱ, ㄴ, ㄷ -->
```

## 층별 송수신 구조도 (Layered Sender–Receiver Architecture)

여러 모델·에이전트·서비스가 주고받는 논문에서 프로세스·송수신자·구조·단계를 **한 쪽**에서 읽게 하는 인라인 SVG. 좌표가 많으므로 `_tmp/`의 작은 Python 생성기로 만든다. 완성 예: `examples/neurosym-briefings-ko/courses/latent-comm-safety-ko/modules/01-latent-mas.html`의 "전체 아키텍처: 층별 송수신" 쪽.

**배치 규칙**
- `viewBox="0 0 800 H"`(H ≈ 360~400), 세로 칸 3개(폭 약 240, 칸 안 상자 폭 208), 칸 사이는 `edge-line dashed` 세로선.
- 칸 머리(`y≈4~36`)에 **주체 + 상태**를 굵게: `송신자 LLM · 동결`, `통신 링크 f_θ · 학습`, `수신자 LLM · 동결`.
- 칸 안 상자는 위→아래로 데이터가 지나는 층 순서(행 간격 56, 상자 높이 36). 데이터는 `node-rect sq`, 처리 층은 `node-rect`, 학습되는 부분은 `accent`.
- 모든 상자 라벨 앞에 ①②③ 단계 번호, 데이터 상자는 둘째 줄에 형태(`최대 80개 × 3072`).
- 칸 안 화살표는 기본색, **칸 사이 전달 화살표만 `accent`**. 받는 쪽의 정확한 층 상자 왼쪽 가장자리로 직각 경로로 들어간다. 전달 방식(`inputs_embeds` 등)은 받는 칸 안쪽에 `muted mono` 11px로 단다(구분선과 겹치지 않게).
- 모든 주체가 받는 공통 입력(질의 `q`)은 맨 윗줄에서 칸을 가로지르는 화살표 하나와 작은 설명.
- 그림 아래에 "기존 방식이라면 ⑤ 대신 …" 같은 대안 경로 한 줄 상자.
- 캡션: 구성(모델 이름·토폴로지), 색칠한 칸의 뜻, 논문 근거 절.

**함께 두는 쪽(선택)**: 익숙한 구조(WAS 요청 처리·마이크로서비스·네트워크 계층)와의 대응표 `계층 | 익숙한 구조 | 논문 구조(단계 번호)` 7행 이하 + `callout-warning` `비유의 한계`. 대응은 강의 해석이라고 캡션에 쓴다.

**검사**: 765px 안에 문단 1개 + 그림 + 캡션. 상자 라벨 12px 이상, 두 줄을 넘으면 상자 높이를 늘린다.

## 드래그 앤 드롭 매칭 (Drag-and-Drop Matching)

개념과 정의, 방법과 논문 등을 짝짓는다. 칩의 `data-answer`와 칸의 `data-correct`가 짝이며 컨테이너에 `id`가 필요하다.

**동작(main.js):**
- 끌어다 놓거나 **칩을 누른 뒤 칸을 눌러** 놓는다. 찬 칸에 놓으면 이전 칩은 제자리로 돌아간다.
- 칩 안 수식 표기(`<i class="mi">`, `<sub>`)는 칸으로 그대로 옮겨지고 둘레 글자색을 따른다.
- **`매칭 확인` = 채점 + 정답 공개.** 다 놓지 않아도 모든 칸에 정답이 보인다: 맞힌 칸 `correct-placed`, 틀린 칸은 취소선 + `정답 …`(`incorrect-placed`), 빈칸 `정답 …`(`answer-shown`).
- **스페이스바**: 공개 전이면 `매칭 확인`과 같이 공개, 공개 뒤에는 다음 쪽. `초기화`는 공개 상태까지 되돌린다.
```html
<div class="dnd-container animate-in" id="dnd-module2">
  <div class="dnd-chips">
    <div class="dnd-chip" draggable="true" data-answer="grpo">GRPO</div>
    <div class="dnd-chip" draggable="true" data-answer="ppo">PPO</div>
    <!-- 칩 반복 -->
  </div>
  <div class="dnd-zones">
    <div class="dnd-zone" data-correct="grpo">
      <p class="dnd-zone-label">가치 네트워크 없이 그룹 내 상대 어드밴티지를 쓴다.</p>
      <div class="dnd-zone-target">여기에 놓으시오</div>
    </div>
    <!-- 칸 반복 -->
  </div>
  <div style="margin-top:var(--space-4)">
    <button class="btn" onclick="checkDnD('dnd-module2')">매칭 확인</button>
    <button class="btn" onclick="resetDnD('dnd-module2')">초기화</button>
  </div>
</div>
```

## 숨은 가정 찾기 (Spot the Assumption)

주장·실험 설정의 숨은 가정을 찾게 한다. `window.selectAssumption(btn)`, `window.checkAssumption(containerId)`. 해설 속성은 컨테이너에 둔다.
```html
<div class="assumption-challenge animate-in" id="assumption-1"
     data-correct="option-b"
     data-explanation-right="② | 수학 추론에서만 실험했으므로 다른 과제로의 일반화가 숨은 가정이다."
     data-explanation-wrong="| 정답은 ②이다. 실험 범위가 수학 추론으로 한정되어 있다.">
  <h3>다음 결론에 숨어 있는 가정으로 가장 적절한 것을 고르시오.</h3>
  <div class="assumption-claim">“LoPE는 LLM의 추론 탐색 능력을 효과적으로 높였다.”</div>
  <div class="assumption-options">
    <button class="assumption-option" data-value="option-a" onclick="selectAssumption(this)"><div class="quiz-option-radio"></div><span>① Lorem Ipsum이 가장 좋은 교란 텍스트이다.</span></button>
    <button class="assumption-option" data-value="option-b" onclick="selectAssumption(this)"><div class="quiz-option-radio"></div><span>② 수학 추론의 향상이 다른 과제에도 일반화된다.</span></button>
    <!-- 선택지 반복 -->
  </div>
  <div class="assumption-feedback"></div>
  <button class="quiz-check-btn" onclick="checkAssumption('assumption-1')">정답 확인</button>
</div>
```

## 어블레이션 토글 (Ablation Toggle)

구성 요소를 하나씩 제거한 결과를 탭으로 보인다. `window.showLayer(layerId, btn)`(레이어 토글과 같은 엔진). 레이어 id는 문서 전체에서 고유해야 한다(전역 `#id`로 찾는다). 첫 레이어만 `display:block`.
```html
<div class="ablation-demo animate-in">
  <div class="ablation-tabs">
    <button class="ablation-tab active" onclick="showLayer('full', this)">전체 LoPE</button>
    <button class="ablation-tab" onclick="showLayer('no-prefix', this)">무작위 접두어 제거</button>
    <!-- 탭 반복 -->
  </div>
  <div class="ablation-viewport">
    <div class="ablation-layer" id="full" style="display:block">
      <div class="ablation-metric">78.3%</div>
      <div class="ablation-delta positive">기준 모델 대비 +6.2%p</div>
      <p class="ablation-description">무작위 접두어와 정규화를 모두 사용한다.</p>
    </div>
    <div class="ablation-layer" id="no-prefix" style="display:none">
      <div class="ablation-metric">72.1%</div>
      <div class="ablation-delta neutral">기준 모델과 같음</div>
      <p class="ablation-description">무작위 접두어를 빼면 방법이 표준 GRPO와 같아진다.</p>
    </div>
    <!-- 레이어 반복 -->
  </div>
</div>
```

## 콜아웃 박스 (Callout Boxes)

선택 코너(`보충 설명`, `더 알아보기`)는 모듈당 최대 2개. 고정 코너 `학습 목표`·`핵심 정리`와 `배경 지식`은 개수에 넣지 않는다. `.callout-title`은 교과 색(또는 변형 색) 칩으로 그려진다. 이모지는 어디에도 쓰지 않고(본문·표·그림·콜아웃), `.callout-icon` div도 쓰지 않는다. 표의 갖춤/없음은 ○·△·×.
```html
<div class="callout callout-accent animate-in">
  <div class="callout-content">
    <strong class="callout-title">핵심 정리</strong>
    <p>LoPE는 모델이나 보상 함수를 바꾸지 않고 입력만 바꾼다.</p>
  </div>
</div>
```
**변형:** `callout-accent` 핵심 통찰(핵심 정리) / `callout-info` 알아 두면 좋은 정보(보충 설명) / `callout-warning` 흔한 오해(더 알아보기) / `callout-info` + `배경 지식` 배경 전용 화면 표시("모듈 골격과 내비게이션").

## 기여 및 개념 카드 (Contribution Cards)

```html
<div class="contribution-cards stagger-children animate-in">
  <div class="contribution-card">
    <div class="contribution-num">1</div>
    <div class="contribution-text">
      <strong>프롬프트 공간 교란</strong>
      <p>원래 질문 앞에 무작위 텍스트를 붙여 모델의 입력 분포를 바꾼다.</p>
    </div>
  </div>
  <!-- 카드 반복 -->
</div>
```

## 논문 인용 카드 (Paper Citation Cards)

```html
<div class="paper-citation animate-in">
  <div class="paper-citation-title">DeepSeekMath: Pushing the Limits of Mathematical Reasoning</div>
  <div class="paper-citation-authors">Shao et al., 2024</div>
  <div class="paper-citation-summary">그룹 내 상대 어드밴티지 추정으로 가치 네트워크를 대체한 GRPO 방법을 제안했다.</div>
</div>
```

## 흐름도 (Flow Diagrams)

```html
<div class="flow-steps animate-in">
  <div class="flow-step"><div class="flow-step-num">1</div><p>원본 프롬프트</p></div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step"><div class="flow-step-num">2</div><p>노이즈 접두어 추가</p></div>
  <!-- 화살표 + 단계 반복 -->
</div>
```

## 단 나누기 (Column Layout)

본문 안에서 그림과 설명, 카드 여러 개를 나란히 둘 때 쓴다. 인라인 `display:grid`·`display:flex`·`grid-template-columns`는 쓰지 않는다(lint KO114). 폭·비율만 인라인 변수로 바꾸고, `margin`은 인라인으로 둬도 된다. 640px 이하에서는 모두 한 단(`.cols-flex`는 세로)으로 바뀐다.

| 클래스 | 배치 | 바꾸는 변수 |
|---|---|---|
| `.cols-2` · `.cols-3` | 같은 너비 2·3단 | 비율 `--col-a`·`--col-b`·`--col-c` (기본 `1fr`) |
| `.cols-4` · `.cols-5` | 같은 너비 4·5단(수치 카드 줄) | 없음 |
| `.cols-label` | 앞 열 고정 폭 + 나머지 | `--col-w` (기본 `230px`) |
| `.cols-aside` | 나머지 + 뒤 열 고정 폭 | `--col-w` (기본 `300px`) |
| `.cols-1` | 한 단 격자(간격만) | 없음 |
| `.cols-flex` | 가로 한 줄 flex, 자식 `flex:1`로 나눔 | 없음 |

간격은 기본 `var(--space-4)`, `.gap-0`·`.gap-2`·`.gap-3`·`.gap-5`·`.gap-6`으로 바꾼다(토큰에 없는 값만 인라인 `gap:`). 세로 정렬은 기본 늘이기(stretch), `.align-start`·`.align-center`·`.align-end`. 기존 카드 묶음(`.contribution-cards`·`.step-cards`·`.dnd-zones`·`.quiz-options.row`)도 같은 클래스를 덧붙여 2·3단으로 만든다.
```html
<div class="cols-2 gap-5 align-start" style="--col-a:1.2fr">
  <figure class="figure">…</figure>
  <div>…설명…</div>
</div>
<div class="cols-label align-center" style="--col-w:300px; margin-top:var(--space-2)">…</div>
<div class="contribution-cards cols-2 gap-3">…</div>
```
의사코드 두 열의 비율은 `.pseudocode-translation`에 같은 변수로 준다: `<div class="pseudocode-translation" style="--col-a:1.5fr">`.

## 데이터 표 (Data Table)

논문 표를 옮기거나 항목을 비교할 때 일반 `<table>` 대신 `.data-table`을 쓴다. 숫자 열은 `th`·`td` 모두 `.num`(오른쪽 정렬), 강조 행은 `tr.hl`(교과 색 하나). 캡션은 표 아래에 표시되며 `~을 나타낸 것이다.` + 논문 표 번호. 한 페이지의 표는 8행 이하, 넘치면 페이지를 나눈다.
```html
<table class="data-table animate-in">
  <caption>표는 번역 품질(BLEU)과 학습 비용을 모델별로 나타낸 것이다. (논문 표 II)</caption>
  <thead><tr><th>모델</th><th class="num">BLEU</th><th class="num">학습 비용</th></tr></thead>
  <tbody>
    <tr><td>기준 모델</td><td class="num">25.2</td><td class="num">2.3</td></tr>
    <tr class="hl"><td>제안 방법</td><td class="num">28.4</td><td class="num">0.9</td></tr>
  </tbody>
</table>
```

## 용어 툴팁 (Glossary Tooltips)

```html
<p>LoPE는 <span class="term" data-definition="그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO): 같은 그룹의 응답을 서로 비교해 모델을 갱신하는 강화 학습 방법. 가치 네트워크가 필요 없음.">GRPO</span>를 기본 학습 프레임워크로 삼는다.</p>
```
**Rules:**
- 모듈마다 모든 전문 용어를 첫 등장 시 표시하고, 같은 화면에서 같은 용어를 두 번 표시하지 않는다.
- 정의는 일상어 1~2문장, `한글 용어(English Term): 설명` 형식(반각 괄호, 앞 공백 없음). 사전식 명사형 종결(`~것.`, `~함.`, `~임.`, 명사)로 끝내고 `~이다.`, `~한다.`, `~없다.`로 끝내지 않는다(KO111). 예: `정책 경사(Policy Gradient): 보상을 높이는 방향으로 정책 파라미터를 직접 갱신하는 최적화 방법`
- `cursor: pointer`(`cursor: help` 금지).

## 번호 단계 카드 (Numbered Step Cards)

```html
<div class="step-cards stagger-children animate-in">
  <div class="step-card">
    <div class="step-num">1</div>
    <div class="step-body">
      <strong>샘플링 단계</strong>
      <p>질문마다 응답 G개를 생성한다.</p>
    </div>
  </div>
  <!-- 카드 반복 -->
</div>
```

## 아이콘 라벨 행 (Icon-Label Rows)

아이콘 칸에는 이모지 대신 짧은 글자·단순 기호를 넣고, 배경은 교과 색 또는 먹색만(`--color-actor-*` 금지).
```html
<div class="icon-rows stagger-children animate-in">
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-accent)">M</div>
    <div><strong>수학 추론 벤치마크</strong><p>GSM8K, MATH, Minerva 등의 데이터셋</p></div>
  </div>
  <!-- 행 반복(먹색은 style="background: #1F2328") -->
</div>
```

## 첫 페이지: 왜 썼는가와 새로운 점

1단원(`module-0`, 화면 번호 1) 첫 페이지(단원 도입 + 첫 화면)는 한 장으로 동기와 기여를 전한다. 화면 제목에 `.paper-ref`(논문 1절)를 달고 `배경 지식` 콜아웃은 두지 않는다. 765px 안에 순서대로:

1. **문제 문단:** 이전 방식의 한계와 이 논문을 쓴 이유 2~3문장.
2. **비교 그림:** 하나의 `.svg-diagram` viewBox를 둘로 나눈다(왼쪽 0~392 "이전 방식" 먹색, 오른쪽 408~800 "제안 방식" 교과 색). 같은 입력(예: $x_1, \ldots, x_4$)을 두 패널의 같은 위치(같은 y)에 두고 처리 경로만 다르게, 간선은 직각, 패널 아래에 차이 한 줄(예: "순차 단계 $n$번" 대 "1번"). `accent`는 제안 방식 쪽에만.
3. **새로운 점:** `.callout.callout-accent` 안 `<ol>` 3개 이내, 항목마다 `<strong>이름:</strong>` + 논문 수치 근거.
```html
<div class="svg-diagram animate-in">
  <svg viewBox="0 0 800 216" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="이전 방식은 순차 처리, 제안 방식은 한 번에 처리함">
    <foreignObject x="16" y="8" width="360" height="24"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>이전 방식</span></div></foreignObject>
    <rect class="node-rect" x="16" y="48" width="72" height="48" rx="12"/>
    <foreignObject x="20" y="52" width="64" height="40"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span><i class="mi">x</i><sub>1</sub></span></div></foreignObject>
    <!-- 간선 + 같은 간격으로 x₂, x₃, x₄ -->
    <rect class="node-rect accent" x="408" y="48" width="72" height="48" rx="12"/> <!-- … 오른쪽 패널 -->
    <!-- y=176: 패널마다 차이 한 줄 foreignObject(왼쪽 color:var(--color-text-secondary)) -->
  </svg>
</div>
```

## 연구 계보: 이어받은 것과 달라진 것

갈래마다 노드 뒤에 `<p class="lineage-note">이어받은 것. → <strong class="novelty">달라진 것</strong>.</p>`, 루트 노드에는 `<span class="novelty-badge">한 줄 기여</span>`. `.lineage-branch`는 가로 flex라 `edge-label`, 노드, `.lineage-note`가 한 줄에 놓이고, 더 이른 선행 연구는 그 갈래 안에 `.lineage-branch`를 중첩한다. 단서 칸에는 "새로운 점" 콜아웃으로 앞선 연구와의 차이를 한 문장으로 쓴다.
```html
<div class="lineage-tree animate-in">
  <div class="lineage-node lineage-root" data-detail="…">
    <span class="lineage-label">트랜스포머</span>
    <span class="lineage-detail">본 논문 (2017)</span>
    <span class="novelty-badge">순환 없이 어텐션만 사용</span>
  </div>
  <div class="lineage-branch">
    <div class="lineage-edge-label">개선</div>
    <div class="lineage-node" data-detail="…">
      <span class="lineage-label">어텐션 RNN</span>
      <span class="lineage-detail">Bahdanau et al., 2014</span>
    </div>
    <p class="lineage-note">입력 위치별 가중합으로 문맥을 읽는 어텐션. → <strong class="novelty">순환을 없애고 병렬로 계산</strong>한다.</p>
    <!-- 중첩 .lineage-branch(기반: Seq2Seq …) -->
  </div>
</div>
```

## 구조도와 차이 비교(보충 자료 조사 결과를 담는 패턴)

**전체 구조도.** `.svg-diagram`에 구성 요소는 `.node-rect.sq`, 흐름은 직각 `path.edge-line`. 오프라인/온라인 구획은 `guide-fill` 배경 사각형 두 개와 왼쪽 위 `text.muted` 라벨. 상자 둘째 줄에 입력·출력 예를 `text.mono`로(예: `질문 → 768차원 벡터`).
```html
<figure class="svg-diagram fit" style="--diagram-max:720px">
  <svg viewBox="0 0 720 260" role="img" aria-label="RAG 구조도: 오프라인 indexing과 온라인 retrieval·generation">
    <rect class="guide-fill" x="0" y="0" width="720" height="100" rx="4"/>
    <text class="muted" x="10" y="16">오프라인: 색인 구축</text>
    <rect class="guide-fill" x="0" y="120" width="720" height="140" rx="4"/>
    <text class="muted" x="10" y="136">온라인: 질문 처리</text>
    <!-- 상자·흐름: node-rect.sq + path.edge-line (M… H… V…) + edge-arrow -->
  </svg>
  <figcaption class="figure-caption">그림은 ~을 나타낸 것이다. 출처: 논문 그림 2, 공식 문서(링크)를 참고해 다시 그림.</figcaption>
</figure>
```

**지도 표시.** 구조도를 다룬 뒤의 페이지에는 같은 구조도를 작게(`--diagram-max:280px`) 단서 칸에 두고, 지금 설명하는 상자만 `node-rect.sq.accent`로 칠한다.

**차이 비교.** 같은 입력 하나를 형제 개념 각각에 넣은 결과를 세로 칸으로 나란히 그리고(칸 제목 = 개념 이름, 같은 높이의 단계 상자), 아래에 비교표(`.data-table`, 위 "데이터 표" 형식)와 `핵심 비교` 한 줄을 둔다.
```html
<p class="diff-line"><strong>핵심 비교</strong> Naive는 검색 → 생성뿐, Advanced는 그 앞뒤를 다듬고, Modular는 단계 자체를 갈아 끼운다.</p>
```
