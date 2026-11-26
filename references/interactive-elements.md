# 인터랙티브 요소 레퍼런스

paper-to-course 튜토리얼에서 사용하는 모든 인터랙티브 요소의 구현 패턴입니다.

> **구조 참고:** CSS와 JavaScript는 모두 `references/styles.css`와 `references/main.js`에 있으며, 각 강의 디렉터리에 그대로 복사됩니다. 아래 HTML 패턴만 작성하고 인라인 `<style>`이나 `<script>`는 쓰지 않습니다.
> **중요:** 클래스명, `data-*` 속성명, id, HTML 구조는 `main.js`와 `styles.css`가 의존하므로 절대 바꾸지 않습니다. 사람이 읽는 텍스트와 속성 값(`data-definition`, `data-explanation-right` 등)만 한국어로 작성합니다.

## 목차
0. [모듈 골격과 내비게이션 (Module Skeleton & Navigation)](#모듈-골격과-내비게이션-module-skeleton--navigation)
0.5. [코넬식 페이지와 지면 요소](#코넬식-페이지와-지면-요소)
   - [개념 그림 (Concept Figures)](#개념-그림-concept-figures)
   - [페이지 넘김 (Page Navigation)](#페이지-넘김-page-navigation)
1. [표지와 히어로 섹션 (Cover Page)](#표지와-히어로-섹션-cover-page)
2. [수식 유도 단계별 풀이 (Math Derivation Walkthrough)](#수식-유도-단계별-풀이-math-derivation-walkthrough)
3. [의사코드 단계별 풀이 (Pseudocode Walkthrough)](#의사코드-단계별-풀이-pseudocode-walkthrough)
4. [결과 비교 인터랙티브 (Result Comparison)](#결과-비교-인터랙티브-result-comparison)
5. [연구 계보 트리 (Research Lineage Tree)](#연구-계보-트리-research-lineage-tree)
6. [연구 대화 (Research Dialogue)](#연구-대화-research-dialogue)
7. [SVG 다이어그램 (SVG Diagrams)](#svg-다이어그램-svg-diagrams)
   - [문항 삽화 (Question Figure)](#문항-삽화-question-figure)
8. [객관식 퀴즈 (Multiple-Choice Quizzes)](#객관식-퀴즈-multiple-choice-quizzes)
9. [드래그 앤 드롭 매칭 (Drag-and-Drop Matching)](#드래그-앤-드롭-매칭-drag-and-drop-matching)
10. [숨은 가정 찾기 (Spot the Assumption)](#숨은-가정-찾기-spot-the-assumption)
11. [어블레이션 토글 (Ablation Toggle)](#어블레이션-토글-ablation-toggle)
12. [콜아웃 박스 (Callout Boxes)](#콜아웃-박스-callout-boxes)
13. [기여 및 개념 카드 (Contribution Cards)](#기여-및-개념-카드-contribution-cards)
14. [논문 인용 카드 (Paper Citation Cards)](#논문-인용-카드-paper-citation-cards)
15. [흐름도 (Flow Diagrams)](#흐름도-flow-diagrams)
15.5. [데이터 표 (Data Table)](#데이터-표-data-table)
16. [용어 툴팁 (Glossary Tooltips)](#용어-툴팁-glossary-tooltips)
17. [번호 단계 카드 (Numbered Step Cards)](#번호-단계-카드-numbered-step-cards)
18. [아이콘 라벨 행 (Icon-Label Rows)](#아이콘-라벨-행-icon-label-rows)
19. [첫 페이지: 왜 썼는가와 새로운 점](#첫-페이지-왜-썼는가와-새로운-점)
20. [연구 계보: 이어받은 것과 달라진 것](#연구-계보-이어받은-것과-달라진-것)

---

## 한국어 콘텐츠 작성 원칙 (요약)

- **문체(EBS 교재 문체):** 본문·설명·콜아웃·카드는 한다체 평서형(`~이다 / ~한다 / ~된다`)으로 쓴다. 용어 툴팁 정의(`data-definition`)만 사전식 명사형 종결(`~것.`, `~함.`, `~임.`, 명사)로 쓴다. `여러분`, 수사적 의문문, 감탄 표현은 쓰지 않는다. 문항의 해설과 피드백도 한다체이며 칭찬하지 않는다. 예외로 연구 대화(채팅)의 등장인물 대사는 해요체를 허용한다.
- **문항 형식:** 발문은 `다음 중 ~에 대한 설명으로 옳은 것은?` 또는 `~으로 옳지 않은 것은?` 형태로 쓰고, 지시는 `~하시오`로 쓴다. 선택지 텍스트 앞에 `①②③④`를 붙인다(`data-value`, `data-correct` 값은 그대로 둔다). `main.js`가 피드백 앞에 `정답`/`오답` 표지를 자동으로 붙이므로, 해설 속성은 표지 없이 쓴다. 맞힌 경우 `data-explanation-right="② | ~이므로 ~이다."`, 틀린 경우 `data-explanation-wrong="| 정답은 ②이다. ~이므로 ~이다."` 형식이다(화면: **정답** ② | … / **오답** | 정답은 ②이다. …).
- **코너 이름:** `학습 목표`(모듈 맨 앞), `개념 체크`(용어·정의 확인), `탐구 자료`(실험 결과·그래프·대화 자료), `보충 설명`(알아 두면 좋은 정보, `callout-info`), `핵심 정리`(핵심 통찰, `callout-accent`), `더 알아보기`(오해 바로잡기, 심화, `callout-warning`)를 콜아웃 제목에 쓴다. 모듈 끝의 문항 묶음은 `확인 문제`이다.
- **학습 목표 패턴:** 각 모듈 맨 위에 `이 모듈을 학습하면 다음을 할 수 있다.` 다음에 `GRPO의 어드밴티지 계산 과정을 설명할 수 있다.`, `기준 모델과 제안 방법의 성능을 비교할 수 있다.`처럼 `~을 설명할 수 있다 / ~을 비교할 수 있다` 형태의 목표를 2~3개 쓴다.
- **용어 첫 등장:** `한글 용어(English Term)` 형식으로 쓰고, 이후에는 한글만 쓴다. 약어는 첫 등장 시 `한글 풀이(English Full Name, ACRONYM)`로 쓰고(`저랭크 적응(Low-Rank Adaptation, LoRA)`) 이후에는 약어만 쓴다. 한국어 실무에서 약어가 이름처럼 굳었으면(GRPO, BLEU, GPU) `ACRONYM(English Full Name, 한글 풀이)`도 허용한다. 트랜스포머, 어텐션처럼 관용 표기가 굳은 용어는 관용 표기를 따른다.
- **반각 괄호:** 괄호는 항상 ASCII 반각 `( )`를 쓰고, 괄호 앞에는 공백을 두지 않는다. 전각 괄호(U+FF08, U+FF09)는 쓰지 않는다.
- **조사 처리:** 영문·숫자·수식 뒤의 조사는 읽는 발음을 기준으로 고른다. 예: `LoRA를`, `GRPO는`, `PPO가`, `$x$는`(엑스는).
- **숫자·단위:** 한글 단위 명사와 `%`, `%p`, `°`는 숫자에 붙인다(`7개`, `45분`, `3.2%p`). 라틴 SI·컴퓨팅 단위 기호는 한 칸 띄운다(`3 kg`, `10 ms`, `16 GB`). 모델 규모 `1.7B`는 붙인다.
- **인용:** 인용문은 큰따옴표 “ ” 또는 " "로 묶는다. 작은따옴표는 속성 값 안의 충돌을 피하기 위해 되도록 쓰지 않는다.
- **수식 주변 띄어쓰기:** 인라인 수식 `$...$` 앞뒤에는 한 칸을 띄우고, 조사는 수식 뒤에 공백 없이 붙인다(`$A_i$는`).
- **자세한 규칙은** `references/korean-style-guide.md`를 참고한다.

---

## 모듈 골격과 내비게이션 (Module Skeleton & Navigation)

모든 모듈 파일과 `_base.html`의 내비게이션이 따라야 하는 기본 마크업이다. 클래스명은 `styles.css`와 `main.js`가 의존하므로 바꾸지 않는다.

**연결 방식:** `main.js`는 `.module` 요소를 문서 순서대로 모아 `.nav-dot`, `.sidebar-item`과 **같은 순서(인덱스)로** 짝짓는다. 따라서 모듈 수, `.nav-dot` 수, `.sidebar-item` 수가 같아야 하고 순서도 같아야 한다. 점을 누르면 `data-target`의 id로, 사이드바 항목은 `href`의 id로 스크롤한다. 표지(`.course-cover`)는 `.module`이 아니므로 짝에 들어가지 않는다.

**모듈 파일(`modules/0N-slug.html`) 골격:** 모든 `.screen`은 `.screen.cornell` 한 페이지이다. 단원 도입(`.module-header`)과 첫 코넬 화면이 함께 첫 페이지를 이룬다.
```html
<section class="module" id="module-1">
  <div class="module-content">

    <div class="module-header">
      <span class="module-number">2</span>
      <h2 class="module-title">어텐션</h2>
      <p class="module-subtitle">쿼리, 키, 값으로 토큰 사이의 관련도를 계산하는 과정을 익힌다</p>
    </div>

    <!-- 첫 페이지: 단원 도입 + 첫 코넬 화면. 학습 목표 상자는 .cue에 둘 수 있다 -->
    <div class="screen cornell">
      <aside class="cue">
        <span class="cue-label">핵심 질문</span>
        <ul>
          <li>어텐션은 무엇을 계산하는가?</li>
          <li>쿼리와 키의 내적은 왜 관련도를 나타내는가?</li>
        </ul>
      </aside>
      <div class="notes">
        <h3 class="screen-heading">화면 제목</h3>
        <p>본문(한다체)...</p>
      </div>
      <div class="summary"><span class="summary-label">요약</span><p>쿼리와 키의 내적으로 관련도를 구하고, 이를 가중치로 값을 합한다.</p></div>
    </div>

    <!-- 이어지는 페이지들: 개념 설명, 개념 체크, 탐구 자료 -->
    <div class="screen cornell">
      <aside class="cue">
        <span class="cue-label">핵심 질문</span>
        <ul><li>소프트맥스는 왜 필요한가?</li></ul>
      </aside>
      <div class="notes">
        <h3 class="screen-heading"><span class="corner-tag">탐구 자료</span>번역 성능 비교</h3>
        ...
      </div>
      <div class="summary"><span class="summary-label">요약</span><p>…한다.</p></div>
    </div>

    <!-- 끝: 핵심 정리(.cue 또는 .notes 안 callout) → 확인 문제(퀴즈 페이지) -->
    <div class="screen cornell">
      <aside class="cue">
        <span class="cue-label">핵심 질문</span>
        <ul><li>이 모듈의 내용을 문제에 적용할 수 있는가?</li></ul>
      </aside>
      <div class="notes">
        <h3 class="screen-heading"><span class="corner-tag outline">확인 문제</span>어텐션 연산</h3>
        <div class="quiz-container" id="quiz-module1">...</div>
      </div>
      <div class="summary"><span class="summary-label">요약</span><p>…한다.</p></div>
    </div>

  </div>
</section>
```
학습 목표 상자(`callout callout-info`)는 첫 페이지의 `.cue`에 넣어도 되고 `.notes` 맨 위에 넣어도 된다. 한 페이지에 들어가는지는 아래 "코넬식 페이지와 지면 요소"의 쪽 맞춤 규칙과 `check-pages.py`로 확인한다.

**Rules:**
- `<section class="module" id="module-N">`의 `N`은 0부터 연속한 번호이다. 메뉴의 모듈 수보다 적게 만들어도 번호를 건너뛰지 않고 `module-0`, `module-1`, …로 매기고 파일명도 `00-`, `01-`, …로 매긴다.
- `.module-number`는 **모듈의 연속 번호**(`1`, `2`, `3` …)이다. 논문 절 번호(`3.2`, `1–2`)나 `0`을 쓰지 않는다. `.module-title`은 해당 논문 절 제목의 한국어 번역이다. 논문 위치는 화면 제목 끝의 `.paper-ref`에 적는다(예: `<h3 class="screen-heading">스케일드 내적 어텐션<span class="paper-ref">논문 3.2.1절</span></h3>`). CSS가 교과 색 64px 사각 블록에 흰 숫자로 표시한다(옅은 장식이 아니다). `.module-header` 아래에는 2px 교과 색 선이 그려진다.
- 모듈 제목은 `<h2 class="module-title">`, 화면 제목은 `<h3 class="screen-heading">`이다. 화면 안의 더 작은 제목은 `<h4>`를 쓴다.
- 모듈 하나의 화면(`.screen.cornell`)은 본문 3~8개(확인 문제 쪽 제외)이며 각각 한 페이지이다. 코넬 형식이 아닌 `.screen`은 쓰지 않는다(`check-pages.py`가 보고한다).
- 한 페이지는 데스크톱 한 화면(1440×900)에 스크롤 없이 들어가야 한다. 넘치면 내용을 줄이지 말고 페이지를 나눈다.
- `.module-content` 밖에 보일러플레이트(`<html>`, `<head>`, `<script>`)를 두지 않는다.

**배경 지식 표시:** 논문 이전의 배경만 다루는 화면(모듈 0, 곧 id 기준 첫 모듈이자 화면 번호 1인 모듈의 둘째 쪽부터, 그 밖의 배경 전용 콜아웃)은 화면 맨 위에 `배경 지식` 콜아웃을 둔다. 예외로 모듈 0의 첫 쪽은 논문 1절 "왜 썼나·새로운 점" 쪽이므로 `.paper-ref`(논문 1절)를 달고 `배경 지식` 콜아웃을 두지 않는다. 모듈 0의 나머지 쪽이 배경 쪽이다(첫 쪽 구성은 아래 "첫 페이지: 왜 썼는가와 새로운 점"). 전용 소형 라벨 클래스가 `styles.css`에 없으므로 `callout callout-info`를 쓴다. 이 콜아웃은 `보충 설명`·`더 알아보기`의 모듈당 2개 상한에 넣지 않는다.
```html
<div class="callout callout-info animate-in">
  <div class="callout-icon">&#128214;</div>
  <div class="callout-content">
    <strong class="callout-title">배경 지식</strong>
    <p>이 화면은 논문의 주장이 아니라 논문을 읽기 위해 먼저 알아 둘 배경이다.</p>
  </div>
</div>
```
논문의 주장을 다루는 화면에는 이 콜아웃을 쓰지 않는다. 화면 제목에 `배경 지식 1.` 같은 접두어를 따로 붙이지 않는다.

**`_base.html`의 NAV_DOTS(모듈마다 하나):**
```html
<button class="nav-dot" data-target="module-1" data-tooltip="2 어텐션" aria-label="2단원 어텐션"></button>
```
**`_base.html`의 SIDEBAR_ITEMS(모듈마다 하나):**
```html
<a class="sidebar-item" data-module="1" href="#module-1"><span class="sidebar-item-num">2</span><span class="sidebar-item-label">어텐션</span><span class="sidebar-item-indicator"></span></a>
```

**Rules:**
- `data-target`은 `#` 없이 id만 쓴다(`module-1`). 사이드바의 `href`는 `#module-1`처럼 `#`을 붙인다.
- `data-tooltip`에는 연속 번호와 모듈 제목을 함께 쓴다(`2 어텐션`, CSS가 `attr(data-tooltip)`로 표시한다). `aria-label`은 `2단원 어텐션` 형식이다.
- `sidebar-item-num`은 모듈 번호(`1`, `2`, `3` …, 앞에 0을 붙이지 않는다), `sidebar-item-label`은 모듈 제목이다. 표지 `toc-num`도 같은 번호를 쓴다.
- 첫 번째 항목(`module-0`)에만 `active`를 미리 붙이지 않는다. 활성 상태는 스크롤에 따라 `main.js`가 붙인다.

---

## 코넬식 페이지와 지면 요소

수능특강 지면과 코넬식 노트를 합친 레이아웃이다. 클래스명과 구조는 `styles.css`(맨 끝 "TEXTBOOK PAGE LAYOUT")가 정의한다. 와이어프레임은 `design-system.md`의 "지면 레이아웃" 절을 본다.

### 구조: `.screen.cornell`

한 페이지는 세 영역이다.
- `.cue`(왼쪽, 232px): `<span class="cue-label">핵심 질문</span>` + `<ul>`에 핵심 질문 2~4개. 질문은 한다체 의문형(`~는가?`, `~인가?`)으로 쓴다. 용어를 정리하는 페이지는 `<ul>` 대신 `<dl>`(`<dt>` 용어, `<dd>` 뜻)을 쓴다.
- `.notes`(오른쪽): 화면 제목(`.screen-heading`)과 본문, 수식, 그림, 퀴즈 등 내용 전부.
- `.summary`(아래 가로줄): `<span class="summary-label">요약</span><p>한 문장</p>`. 요약은 한다체 한 문장이다.

```html
<div class="screen cornell">
  <aside class="cue">
    <span class="cue-label">핵심 질문</span>
    <ul><li>어텐션은 무엇을 계산하는가?</li></ul>
  </aside>
  <div class="notes">
    <h3 class="screen-heading"><span class="corner-tag">탐구 자료</span>번역 성능 비교</h3>
    ...
  </div>
  <div class="summary"><span class="summary-label">요약</span><p>…한다.</p></div>
</div>
```

**Rules:**
- 모든 화면이 `.screen.cornell`이다. `.cue`, `.notes`, `.summary` 세 영역을 모두 둔다.
- 1200px 미만에서는 CSS가 한 단(`cue` → `notes` → `summary`)으로 접고 높이 제한을 푼다. 마크업은 따로 만들지 않는다.
- 모듈의 첫 페이지는 `.module-header`와 첫 `.screen.cornell`을 합친 것이다. 학습 목표 콜아웃은 이 첫 페이지의 `.cue`에 둘 수 있다.
- 코너 상자(콜아웃)를 `.cue` 안에 둘 수 있다. `.notes` 맨 위 콜아웃은 위쪽 여백이 없어진다.

### 쪽 맞춤 규칙 (page-fit)

- 한 페이지(`.screen.cornell`)는 한 화면이다. 1440×900 데스크톱에서 브라우저 UI와 48px 내비게이션을 뺀 약 765px 안에 스크롤 없이 들어가야 한다. 첫 페이지는 `.module-header`를 포함해 잰다.
- 넘치면 글을 줄여 억지로 맞추지 말고 내용을 여러 페이지로 나눈다. 페이지마다 핵심 질문과 요약을 따로 둔다.
- 높은 SVG는 높이를 제한한다(`viewBox`는 유지하고 `max-height`를 둔다). 표와 코드도 페이지 높이를 고려해 줄인다.
- 퀴즈는 한 페이지에 최대 2문항이다(선택지 5개씩과 펼쳐진 해설이 765px 안에 들어와야 한다. 아래 "객관식 퀴즈").
- 작성 후 `python3 references/check-pages.py <course-dir>`를 실행해 넘침 0개를 확인한다.

### 코너 이름표: `.corner-tag`

`.screen-heading` 안 맨 앞에 코너 이름(개념 체크, 탐구 자료, 확인 문제 등)을 칩으로 붙인다.
```html
<h3 class="screen-heading"><span class="corner-tag">탐구 자료</span>번역 성능 비교</h3>
<h3 class="screen-heading"><span class="corner-tag outline">개념 체크</span>소프트맥스</h3>
```
- `.corner-tag`: 교과 색 바탕에 흰 글자. `.corner-tag.outline`: 테두리만 있는 칩.
- **개념 체크**는 개념 설명 쪽 끝에 두는 짧은 확인 문항 하나이다. `styles.css`에 전용 클래스가 없으므로 `.quiz-container` 하나에 문항 1개(선택지 3~4개, 배점 `.q-points` 없음)를 넣는 형태를 쓴다.
```html
<h3 class="screen-heading"><span class="corner-tag outline">개념 체크</span>소프트맥스</h3>
<div class="quiz-container animate-in" id="check-module2a">
  <div class="quiz-question-block" data-correct="option-b"
       data-explanation-right="② | 소프트맥스는 출력의 합을 1로 맞추므로 확률처럼 해석할 수 있다."
       data-explanation-wrong="| 정답은 ②이다. 소프트맥스 출력은 모두 양수이고 합이 1이다.">
    <h3 class="quiz-question"><span class="q-num">1</span>소프트맥스 출력에 대한 설명으로 옳은 것은?</h3>
    <div class="quiz-options">
      <button class="quiz-option" data-value="option-a" onclick="selectOption(this)"><div class="quiz-option-radio"></div><span>① 출력의 합이 입력의 합과 같다.</span></button>
      <button class="quiz-option" data-value="option-b" onclick="selectOption(this)"><div class="quiz-option-radio"></div><span>② 출력의 합이 항상 1이다.</span></button>
      <button class="quiz-option" data-value="option-c" onclick="selectOption(this)"><div class="quiz-option-radio"></div><span>③ 출력에 음수가 섞일 수 있다.</span></button>
    </div>
    <div class="quiz-feedback"></div>
  </div>
  <button class="quiz-check-btn" onclick="checkQuiz('check-module2a')">정답 확인</button>
  <button class="quiz-reset-btn" onclick="resetQuiz('check-module2a')">다시 풀기</button>
</div>
```
- 코너 이름이 없는 화면 제목은 `.corner-tag` 없이 쓴다. CSS가 제목 앞에 교과 색 네모 표지를 붙인다.

### 날개: `.wing`

코넬이 아닌 화면에서 쓰는 여백 메모이다(코넬 화면은 `.cue`가 그 역할을 한다). 1200px 이상에서 왼쪽 여백으로 나가 떠 있고, 그보다 좁으면 본문 사이의 상자가 된다.
```html
<div class="wing"><span class="wing-title">참고</span>짧은 보충 한두 문장</div>
```

### 단원 도입과 표지 요소

- `.paper-ref`: 화면 제목 끝에 붙이는 작고 흐린 논문 위치 태그(`<span class="paper-ref">논문 3.2.1절</span>`). 논문의 해당 절에서 온 화면에만 붙이고, 논문 밖 배경 지식·확장 화면(모듈 0 등)에는 붙이지 않는다. 모듈 번호와 별개이다. `.sec-num`(제목 앞 절 번호)은 폐기됐다. 옛 강의용으로 CSS만 남아 있으니 새로 쓰지 않는다.
- `.module-number`: 64px 교과 색 블록에 흰 숫자. `.module-header`는 2px 교과 색 선으로 닫힌다.
- `.course-cover`: 아래에 8px 교과 색 띠가 붙는다.

### 개념 그림 (Concept Figures)

새로 도입하는 개념·알고리즘·수식마다 코드로 그린 그림을 둔다. 숫자는 본문과 같게 하고, 페이지가 765px를 넘지 않도록 `.with-figure` + `figure.figure.side`로 본문 옆에 둔다. `.figure`와 `.svg-diagram` 안에서 쓰는 클래스는 다음과 같다.
- 선·면: `.ink`, `.ink.strong`, `.ink-fill`(검정 계열), `.accent`, `.accent-fill`(교과 색), `.guide`, `.guide-axis`, `.guide-fill`(격자·축·보조 면), `.row-accent`(강조 행), `.edge-line.thin`, `.edge-line.dashed`(간선), `.dot`, `.dot-accent`(점)
- 글자: `text.mono`, `text.muted`, `text.accent-text`. 수학 기호는 라벨 안에서 `<i class="mi">q</i>`(KaTeX 수학 글꼴 + 이탤릭), SVG `<text>`에서는 `font-style="italic"`.
- 모양·크기: `.node-rect.sq`(거의 직각인 노드, 행렬·칩). 본문 옆 그림 폭은 `figure.figure.side`에 `--figure-side-width`(기본 200px)를 주어 바꾼다.
- 색 사용 기준(먹색 + 교과 색 + 회색만, 그림당 유채색 하나)은 `design-system.md` "색상 규약"을 따른다.
- 설명: `.figure-caption`. 너비에 맞추려면 `.svg-diagram.fit`에 `--diagram-max`를 준다.
- 새 개념을 도입하는데 그림이 없으면 안 된다. 개념마다 그림 하나를 둔다.
- 예: 격자 위 내적 벡터, 소프트맥스 가중치 막대, 행렬 형상 n×d_k · d_k×n = n×n, 스케일 전후 소프트맥스 막대, 멀티헤드 분할 512→8×64→연결, BLEU n-gram 겹침 칩.

### 페이지 넘김 (Page Navigation)

`main.js`의 `initPager()`가 쪽을 모은다. 쪽은 표지, 모듈마다 단원 도입과 첫 화면, 그 뒤의 각 `.screen`이다. ←/↑/PageUp은 이전 쪽, →/↓/PageDown은 다음 쪽, Home/End는 처음/끝 쪽으로 간다. 우하단 고정 `.pager`(‹ n / N ›와 "방향키로도 넘길 수 있다" 안내)는 JS가 넣으므로 마크업을 쓰지 않는다. 방향키를 `preventDefault`하는 다른 `keydown` 핸들러를 추가하지 않는다.

**Space 키.** Space는 현재 페이지의 주 버튼을 누른다. 우선순위는 수식 유도의 다음 단계 → 의사코드의 다음 줄 → 대화의 다음 말풍선 → 전환 버튼·탭(`.result-metric-toggle`, `.ablation-tabs`, `.layer-tabs`)의 다음 항목 → 문제의 정답·해설 공개(선택 없이 바로) → 다음 페이지이다. Shift+Space는 단계·탭을 거꾸로 되돌리고, 되돌릴 것이 없으면 이전 페이지로 간다. 더 할 일이 없으면(마지막 단계이거나 주 버튼이 없으면) 다음 페이지로 넘어간다. 따라서 한 페이지에는 주 인터랙티브 요소를 가능하면 하나만 둔다. 버튼은 마우스 사용자를 위해 그대로 둔다. Space를 `preventDefault`하는 다른 `keydown` 핸들러를 추가하지 않는다. `.module`에는 `scroll-snap-align: start`와 `scroll-margin-top`이 걸려 있다.

---

## 표지와 히어로 섹션 (Cover Page)

강의 표지는 모든 모듈 앞에 나오는 전체 화면 랜딩 페이지입니다. `.module`이 아니므로 내비게이션 점이 없고 스크롤 스냅에도 참여하지 않습니다.

**연결 방식:** "학습 시작하기" 버튼은 모듈 0으로 스크롤합니다. `main.js`의 표지 CTA 리스너가 처리합니다.

**HTML:**
```html
<section class="course-cover">
  <div class="course-cover-inner">
    <div class="course-cover-main">
      <span class="course-cover-badge">인터랙티브 튜토리얼</span>
      <h1 class="course-cover-title">프롬프트 공간 교란이 추론 탐색을 넓히는 방법</h1>
      <p class="course-cover-original" lang="en">Nonsense Helps</p>
      <p class="course-cover-subtitle">프롬프트에 무작위 노이즈를 더하면 LLM 학습에서 추론 탐색이 넓어지는 원리를 알아본다</p>
      <p class="course-cover-authors">Yuntao Bai et al.</p>
      <div class="course-cover-meta">
        <span class="course-cover-meta-item">arXiv 2026</span>
        <span class="course-cover-meta-item">모듈 7개</span>
        <span class="course-cover-meta-item">약 45분</span>
        <span class="course-cover-meta-item">중급</span>
      </div>
      <div class="course-cover-abstract">
        <span class="course-cover-abstract-label">초록</span>
        <p>이 논문은 프롬프트 공간에 Lorem Ipsum 같은 무작위 노이즈를 더해 GRPO의 탐색을 촉진하는 LoPE 방법을 제안한다. 이 방법으로 제로 어드밴티지(Zero Advantage) 문제를 해결한다...</p>
      </div>
      <a href="#module-0" class="course-cover-cta">학습 시작하기</a>
    </div>
    <nav class="course-cover-toc" aria-label="차례">
      <span class="course-cover-toc-label">차례</span>
      <ol>
        <li><a href="#module-0"><span class="toc-num">1</span>서론과 배경</a></li>
        <li><a href="#module-1"><span class="toc-num">2</span>…</a></li>
      </ol>
    </nav>
  </div>
</section>
```

**Rules:**
- 표지는 `.module` 섹션이 아닙니다. `scroll-snap-align`과 모듈 번호를 두지 않습니다.
- 왼쪽(`.course-cover-main`)은 왼쪽 정렬 제목 영역, 오른쪽(`.course-cover-toc`)은 교과 색 면 위의 차례입니다. 차례는 사이드바의 모듈 제목·번호와 같게 쓰고, `href`는 `#module-N`입니다. 1024px 미만에서는 차례가 제목 아래로 내려갑니다.
- "학습 시작하기" 버튼은 모듈 0(사전 지식 모듈)으로 스크롤합니다. 버튼 문구 뒤에 `→` 같은 화살표를 붙이지 않습니다.
- 한국어 제목은 `.course-cover-title`에, 영어 원제는 바로 아래 `<p class="course-cover-original" lang="en">`에 씁니다. 제목 안에 원제를 괄호로 붙이지 않습니다(큰 글자에서 원제가 어색하게 줄바꿈되기 때문). 배지·라벨 문구는 위 예시 그대로 씁니다("인터랙티브 튜토리얼", "초록", "차례").
- 저자 줄에는 저자만 쓰고, 발표처·연도는 메타 첫 항목(`arXiv 2026`)으로 옮깁니다. 가운뎃점(`·`)으로 잇지 않습니다.
- 초록은 논문 전체 초록이 아니라 2~3문장으로 줄여 씁니다.
- 메타 항목: 발표처·연도, 모듈 수, 예상 소요 시간(모듈당 대략 5~7분), 난이도를 넣습니다. 이모지를 붙이지 않습니다. 숫자와 단위는 붙여 씁니다(`모듈 7개`, `약 45분`).
- 난이도: 초급(사전 지식 불필요), 중급(해당 분야 기초 지식 필요), 고급(상당한 수학·분야 배경 필요)

---

## 수식 유도 단계별 풀이 (Math Derivation Walkthrough)

가장 중요한 교육 요소입니다. 수식을 보여 주고, 학습자가 클릭하며 유도 단계를 하나씩 따라가게 합니다.

**연결 방식:** `main.js`가 모든 `.math-derivation`을 자동으로 초기화합니다. 단계는 `.math-step` 요소이고, 컨트롤은 `.math-next-btn`, `.math-prev-btn`, `.math-reset-btn`, 진행 표시는 `.math-progress`입니다.

**HTML:**
```html
<div class="math-derivation animate-in" id="math-deriv-1">
  <div class="math-step" data-step="0">
    <div class="math-equation">
      $$L_{\mathit{GRPO}} = -\mathbb{E}_{q \sim P(Q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathit{ref}}(o_i|q)} A_i, \mathit{clip}(\cdot) A_i \right) \right] \tag{1}$$
    </div>
    <div class="math-explanation">
      <p>GRPO의 손실 함수는 모델의 응답이 참조 정책(Reference Policy)과 얼마나 다른지를 측정한다. 어드밴티지(Advantage) $A_i$는 각 응답이 평균에 비해 얼마나 좋은지를 나타낸다.</p>
    </div>
  </div>

  <div class="math-step" data-step="1" style="display:none">
    <div class="math-equation">
      $$A_i = \frac{r_i - \mathit{mean}(\{r_1, ..., r_G\})}{\mathit{std}(\{r_1, ..., r_G\})}$$
    </div>
    <div class="math-explanation">
      <p>어드밴티지는 그룹 내 정규화로 계산한다. 각 응답의 보상에서 평균을 빼고 표준편차로 나눈다. 이렇게 하면 같은 그룹의 다른 응답과 비교해 각 응답이 얼마나 나은지 알 수 있다.</p>
    </div>
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
- 각 단계에서는 변형 하나 또는 통찰 하나만 설명합니다.
- 설명은 "미분한다" 같은 기계적 서술이 아니라 쉬운 말로 풀어 씁니다.
- 수식은 모두 이탤릭이다. 함수 이름·첨자 낱말은 `\mathit{}`, 벡터는 `\boldsymbol{}`를 쓰고 `\text`·`\mathrm`·`\mathbf`는 쓰지 않는다(KO112). 논문에 번호가 있는 식에만 `\tag{n}`을 단다(위 예의 `\tag{1}`). 규칙은 `korean-style-guide.md` §7.
- KaTeX가 `$$...$$` 블록을 자동으로 렌더링하며, 새 단계가 나타날 때 `main.js`가 다시 렌더링합니다.
- 설명 안의 인라인 수식은 `$...$`를 씁니다. 수식 앞뒤는 한 칸 띄우고, 조사는 읽는 발음에 맞춥니다(`$A_i$는`).

---

## 의사코드 단계별 풀이 (Pseudocode Walkthrough)

코드 번역 블록과 비슷하지만 알고리즘 의사코드를 다룹니다. 왼쪽 패널에는 알고리즘을, 오른쪽 패널에는 줄 단위 설명을 둡니다.

**연결 방식:** `main.js`가 모든 `.pseudocode-translation`을 자동으로 초기화합니다. 컨트롤은 `.pseudocode-next-btn`, `.pseudocode-prev-btn`, `.pseudocode-reset-btn`, 진행 표시는 `.pseudocode-progress`입니다.

**HTML:**
```html
<div class="pseudocode-translation animate-in" id="pseudo-lope">
  <div class="pseudocode-block">
    <span class="translation-label">알고리즘</span>
    <span class="pseudocode-line">INPUT: 프롬프트 q, 모델 π, 교란 텍스트 P  // 입력</span>
    <span class="pseudocode-line">FOR i = 1 TO G DO  // G번 반복</span>
    <span class="pseudocode-line">  q' = CONCAT(random_prefix(P), q)  // 노이즈 접두어 붙이기</span>
    <span class="pseudocode-line">  o_i = SAMPLE(π, q')  // 응답 생성</span>
    <span class="pseudocode-line">  r_i = REWARD(o_i, q)  // 원래 질문 기준 보상</span>
    <span class="pseudocode-line">END FOR  // 반복 끝</span>
    <span class="pseudocode-line">A = NORMALIZE({r_1, ..., r_G})  // 어드밴티지 계산</span>
    <span class="pseudocode-line">UPDATE π USING A  // 모델 갱신</span>
  </div>
  <div class="pseudocode-explanation">
    <span class="translation-label">설명</span>
    <div class="pseudocode-explanation-lines">
      <p class="pe">입력은 원래 질문, 현재 모델, 교란에 쓸 텍스트(예: Lorem Ipsum)이다.</p>
      <p class="pe">각 샘플링 그룹마다 G번 반복한다.</p>
      <p class="pe">교란 텍스트에서 무작위로 한 구간을 잘라 질문 앞에 붙인다.</p>
      <p class="pe">노이즈가 섞인 질문에 대해 모델이 응답을 생성한다.</p>
      <p class="pe">보상 함수로 응답 품질을 평가한다. 기준은 교란된 질문이 아니라 원래 질문이다.</p>
      <p class="pe">반복을 종료한다.</p>
      <p class="pe">모든 보상을 정규화해 어드밴티지 값을 구한다.</p>
      <p class="pe">어드밴티지로 모델 파라미터를 갱신한다.</p>
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
- **코드 색:** 코드 칸은 IDE 토큰 색(Catppuccin, `styles.css`의 `.code-keyword`·`.code-function`·`.code-comment`·`.code-number`·`.code-operator`·`.code-string`)을 따른다. `main.js`가 줄을 읽어 대문자 제어어(INPUT, FOR, DO, END, OUTPUT …)는 키워드, `이름(`은 함수, `//` 뒤는 주석, 숫자와 `= / * + -`는 각각 숫자·연산자로 자동 색칠한다. 줄은 일반 텍스트로 쓰면 되고, 직접 `<span class="code-…">`로 칠한 줄은 건드리지 않는다. 다른 색을 새로 정하지 않는다.
- `.pseudocode-controls`(이전·다음·처음부터 버튼과 `.pseudocode-progress`)는 반드시 `.pseudocode-translation` 컨테이너 **안**에 둔다. `main.js`가 컨테이너 안에서만 버튼을 찾으므로 밖에 두면 동작하지 않는다.
- 의사코드는 특정 언어에 얽매이지 않게 씁니다. `INPUT`, `OUTPUT`, `FOR EACH`, `IF...THEN` 같은 키워드는 관례대로 영어를 유지하고(Python/C++ 문법은 쓰지 않습니다), 주석(`//`)과 오른쪽 설명만 한국어로 씁니다.
- 각 줄은 설명 줄과 1:1로 대응합니다.
- 설명은 "무엇을"만이 아니라 "왜"를 설명합니다. 설명 문장은 한다체 평서형으로 쓴다.

---

## 결과 비교 인터랙티브 (Result Comparison)

방법이나 설정별 실험 결과를 비교하는 인터랙티브 막대 차트입니다.

**연결 방식:** `main.js`가 모든 `.result-comparison`을 자동으로 초기화합니다. 지표 토글 버튼은 `data-metric` 속성이 있는 `.result-metric`이고, 막대는 지표별 `data-*` 속성을 가진 `.result-bar`입니다.

**HTML:**
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
    <div class="result-bar" data-accuracy="68.5" data-pass1="54.3">
      <span class="result-label">PPO 기준 모델</span>
      <div class="result-bar-track"><div class="result-fill baseline" style="width:0%"></div></div>
      <span class="result-value"></span>
    </div>
  </div>
</div>
```

**Rules:**
- 제안 방법 막대는 `.result-fill.ours`(강조색), 기준 모델 막대는 `.result-fill.baseline`(회색)을 씁니다.
- 기본값에서 데이터 값은 백분율이며 `%`를 붙여 표시하고 막대 너비(%)로 씁니다.
- `.result-comparison`에 `data-unit`과 `data-max`를 줄 수 있습니다. `data-unit`의 기본값은 `%`이고, BLEU처럼 단위가 없는 지표는 `data-unit=""`로 씁니다. `data-max`는 막대 눈금의 최댓값이며 기본값은 100입니다(BLEU 25~45처럼 값의 차이가 작으면 `data-max="50"`으로 낮춰 막대 폭 차이를 키웁니다).
- `data-metric` 이름은 `dataset`의 camelCase 규칙으로 `data-*` 속성에 대응합니다. `data-metric="enDe"`는 `data-en-de`로 읽히므로 하이픈이 필요한 이름을 피하고 `ende`처럼 소문자 단어 하나를 씁니다(`data-metric="ende"` ↔ `data-ende="28.4"`).
- 지표를 전환하면 `main.js`가 막대 너비를 애니메이션하고 값을 갱신합니다.

---

## 연구 계보 트리 (Research Lineage Tree)

이 논문이 선행 연구와 어떻게 이어지는지 보여 주는 시각적 트리입니다.

**HTML (CSS 기반 트리):**
```html
<div class="lineage-tree animate-in">
  <div class="lineage-node lineage-root" data-detail="LoPE: 프롬프트에 무작위 노이즈를 더해 추론 탐색 공간을 넓히는 방법">
    <span class="lineage-label">LoPE</span>
    <span class="lineage-detail">본 논문 (2026)</span>
  </div>
  <div class="lineage-branch">
    <div class="lineage-edge-label">개선</div>
    <div class="lineage-node" data-detail="그룹 상대 정책 최적화(Group Relative Policy Optimization): 그룹 내 상대 어드밴티지 추정">
      <span class="lineage-label">GRPO</span>
      <span class="lineage-detail">Shao et al., 2024</span>
    </div>
    <div class="lineage-branch">
      <div class="lineage-edge-label">기반</div>
      <div class="lineage-node" data-detail="근접 정책 최적화(Proximal Policy Optimization): 정책 변화를 제한하며 안정적으로 학습">
        <span class="lineage-label">PPO</span>
        <span class="lineage-detail">Schulman et al., 2017</span>
      </div>
    </div>
  </div>
  <div class="lineage-branch">
    <div class="lineage-edge-label">관련</div>
    <div class="lineage-node" data-detail="인간 피드백 기반 강화 학습(Reinforcement Learning from Human Feedback)">
      <span class="lineage-label">RLHF</span>
      <span class="lineage-detail">Ouyang et al., 2022</span>
    </div>
  </div>
</div>
```

**SVG 기반 트리 (복잡한 계보용):** 간선은 직각 `<path>`와 화살촉 `<polygon>`, 노드 라벨은 `foreignObject > div.node-label > span`이다.
```html
<div class="svg-diagram">
  <svg viewBox="0 0 800 368" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LoPE가 GRPO를 거쳐 PPO를 이어받음">
    <rect class="node-rect accent" x="300" y="8" width="200" height="72" rx="12"/>
    <foreignObject x="308" y="12" width="184" height="64"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>LoPE<br/>본 논문, 2026</span></div></foreignObject>

    <path class="edge-line accent" d="M400,80 V115 H200 V140"/>
    <polygon class="edge-arrow accent" points="195,140 205,140 200,150"/>
    <rect class="node-rect" x="100" y="150" width="200" height="72" rx="12"/>
    <foreignObject x="108" y="154" width="184" height="64"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>GRPO<br/>Shao et al., 2024</span></div></foreignObject>

    <path class="edge-line" d="M200,222 V270"/>
    <polygon class="edge-arrow" points="195,270 205,270 200,280"/>
    <rect class="node-rect" x="100" y="280" width="200" height="72" rx="12"/>
    <foreignObject x="108" y="284" width="184" height="64"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>PPO<br/>Schulman et al., 2017</span></div></foreignObject>
  </svg>
</div>
```
간선은 수평·수직 선분만 쓴다(`design-system.md` "도식 간선은 직각으로"). 화살촉은 마지막 선분 끝에 두고, 선은 화살촉 밑변에서 멈춘다.

---

## 연구 대화 (Research Dialogue)

연구자나 방법들이 어떤 개념을 두고 "토론"하는 모습을 보여 주는 메신저 스타일 채팅입니다. codebase-to-course의 그룹 채팅과 같은 엔진을 씁니다.

**색:** 화자 구분은 교과 색(`--color-accent`)과 먹색(`#1F2328`) 두 가지로만 한다. `--color-actor-*`와 이모지는 쓰지 않는다(`design-system.md` "색상 규약").

**연결 방식:** `main.js`가 모든 `.chat-window`를 자동으로 초기화합니다. 컨트롤은 `.chat-next-btn`, `.chat-all-btn`, `.chat-reset-btn`, 진행 표시는 `.chat-progress`입니다.

**HTML:**
```html
<div class="chat-window animate-in" id="chat-module2">
  <div class="chat-messages">
    <div class="chat-message" data-msg="0" data-sender="researcher-a" style="display:none">
      <div class="chat-avatar" style="background: var(--color-accent)">학</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: var(--color-accent)">학생 A</span>
        <p>이거 그냥 데이터 증강(Data Augmentation) 아닌가요? 입력 앞에 무작위 텍스트를 붙이는 게 역번역(Back-translation)과 뭐가 다른가요?</p>
      </div>
    </div>
    <div class="chat-message" data-msg="1" data-sender="researcher-b" style="display:none">
      <div class="chat-avatar" style="background: #1F2328">교</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: #1F2328">교사</span>
        <p>완전히 같지는 않아요. 데이터 증강은 학습 데이터의 분포를 바꾸지만, LoPE는 추론할 때의 프롬프트 공간을 바꿔요. 모델은 그대로고, 모델이 탐색하는 방식만 달라져요.</p>
      </div>
    </div>
  </div>
  <div class="chat-typing" style="display:none">
    <div class="chat-avatar">?</div>
    <div class="chat-typing-dots">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  </div>
  <div class="chat-controls">
    <button class="btn chat-next-btn">다음 메시지</button>
    <button class="btn chat-all-btn">전체 재생</button>
    <button class="btn chat-reset-btn">다시 보기</button>
    <span class="chat-progress"></span>
  </div>
</div>
```

---

## SVG 다이어그램 (SVG Diagrams)

개념 지도, 실험 프레임워크, 알고리즘 흐름, 비교 행렬에 씁니다.

**HTML:** 가로 흐름 4단계 예. 노드 폭·간격이 모두 같고, 마지막 간선만 강조색이다.
```html
<div class="svg-diagram animate-in">
  <svg viewBox="0 0 800 128" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="그림 내용을 한 문장으로">
    <rect class="node-rect" x="16" y="8" width="156" height="64" rx="12"/>
    <foreignObject x="24" y="12" width="140" height="56"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px; word-break:keep-all; line-height:1.4"><span>원본 프롬프트 <i class="mi">q</i></span></div></foreignObject>
    <path class="edge-line" d="M172,40 H210"/>
    <polygon class="edge-arrow" points="210,45 220,40 210,35"/>
    <!-- 다음 노드 x = 16 + i × (156 + 48) -->
    …
    <foreignObject x="16" y="88" width="768" height="32"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px; color:var(--color-text-secondary)"><span>그림 아래 설명 한 줄</span></div></foreignObject>
  </svg>
</div>
```

**Rules (그림 정렬):**
- **노드 라벨은 `foreignObject` + `.node-label` + `<span>` 하나**로 쓴다. `foreignObject`는 사각형에서 가로 8, 세로 4만큼 안쪽으로 잡는다. CSS가 span을 사각형의 가로·세로 가운데에 놓고, span 안의 글자와 `<sub>`는 한 줄 흐름을 유지한다. span 없이 쓰면 `<sub>` 앞뒤가 따로 떨어진다(`check-pages.py`가 검출).
- **같은 단계의 노드는 같은 폭·같은 간격**으로 둔다. 가로 흐름은 `폭 = (768 − (n−1)×간격) / n`, 시작 x는 16이다. 노드의 마지막 x가 viewBox를 넘으면 안 된다(검출).
- **viewBox는 내용에 맞춘다.** 위아래 여백은 8 단위만 두고, 높이는 마지막 요소 아래 8에서 끝낸다. 빈 띠를 남기지 않는다.
- **모든 간선은 노드의 테두리에서 시작해 다른 노드의 테두리에서 끝나고, 끝에 화살촉이 있다.** 허공에서 끝나는 선을 두지 않는다. 화살촉은 길이 10, 반폭 5이고, 선은 화살촉 밑변에서 멈춘다.
- 강조(`accent`)는 논문의 결론 노드와 그리로 들어가는 간선 하나에만 쓴다.
- 반응형으로 만들기 위해 `viewBox`와 `width="100%"`를 쓴다. 색상은 CSS 변수를 쓴다.
- **한글 라벨은 박스를 더 넓게 잡는다.** 한글은 글자당 약 1em이다(14px면 글자당 약 14px).
- **간선은 직각이다.** 대각선 `<line>`을 쓰지 않고 `<path class="edge-line" d="M400,80 V115 H200 V140"/>`처럼 수평·수직 선분과 화살촉 `<polygon>`으로 그린다. 같은 단계로 갈라질 때는 세로 버스 한 줄에서 분기한다.
- **수학 기호는 이탤릭, 한글은 똑바로.** 라벨 속 기호는 `<i class="mi">q</i>`(일반 `<i>`는 똑바른 글씨가 된다), `<text>` 속 기호는 `font-style="italic"`. 한글 라벨에는 이탤릭을 쓰지 않는다.
- `.node-rect`, `.node-rect.sq`, `.edge-line`, `.edge-arrow`(와 `.accent` 변형)는 `.svg-diagram` 안뿐 아니라 `.figure svg` 안에서도 같게 동작한다(본문 옆 `figure.figure.side`의 인라인 SVG 등).
- 각진 노드는 `.node-rect.sq`, 너비 맞춤은 `.svg-diagram.fit` + `--diagram-max`, 본문 옆 그림 폭은 `--figure-side-width`이다. 색은 `design-system.md` "색상 규약"을 따른다.

---

## 문항 삽화 (Question Figure)

수능특강 문항처럼 발문 아래에 그림을 둔다. 선택지 오른쪽에 놓아 페이지 높이를 늘리지 않는다. 그림을 만드는 방법과 스타일 규칙은 `illustration.md`에 있다.

```html
<div class="quiz-question-block" data-correct="option-d" data-explanation-right="④ | …" data-explanation-wrong="| 정답은 ④이다. …">
  <h3 class="quiz-question"><span class="q-num">3</span>그림은 좌표평면 위에 쿼리 벡터 $\boldsymbol{q}$와 키 벡터 $\boldsymbol{k}_1$, $\boldsymbol{k}_2$를 나타낸 것이다. 모눈 한 칸의 길이는 1이다. 이에 대한 설명으로 옳지 <u>않은</u> 것은?</h3>
  <div class="q-body">
    <div class="quiz-options">…선택지 5개…</div>
    <figure class="q-figure" aria-label="그림 내용을 한 문장으로">
      <svg viewBox="0 0 216 136" xmlns="http://www.w3.org/2000/svg" role="img">
        <path class="guide" d="…모눈…"/>
        <line class="ink" …/>                       <!-- 먹선 1.5 -->
        <line class="ink accent" stroke-width="2" …/> <!-- 강조는 하나 -->
        <text font-style="italic" …>O</text>   <!-- 수학 기호는 이탤릭 -->
      </svg>
    </figure>
  </div>
  <div class="quiz-feedback"></div>
</div>
```

- 발문은 `그림은 ~을 나타낸 것이다.`로 그림을 먼저 소개한 뒤 묻는다. 그림 번호(그림 1)는 쓰지 않는다.
- 색은 먹색 + 교과 색 + 회색만 쓴다(`design-system.md` "색상 규약").
- 클래스: `ink`(먹선), `ink-fill`(먹 채움), `accent`·`accent-fill`(교과 색), `guide`(모눈·보조선, 회색 1px), `accent-text`(강조 라벨).
- 폭은 기본 280px이며 `.q-figure`(또는 상위 요소)에 `--q-figure-width`를 주어 조절한다(예: `style="--q-figure-width: 320px"`). 발문에 그림이 있어 `.q-body`를 쓰는 문항은 선택지가 자동으로 한 줄에 하나씩 배치된다(`.row` 불필요). 640px 이하에서는 그림이 선택지 아래로 내려간다.
- 탐구 자료 본문의 그림은 `<figure class="figure">`(노트 칸 가운데, 최대 60%)를 쓴다.
- `check-pages.py`가 래스터 이미지, 불러오지 못한 이미지, 교과 색 외 유채색을 검출한다.

---

## 객관식 퀴즈 (Multiple-Choice Quizzes)

codebase-to-course와 같은 패턴이며 논문 내용에 맞게 조정했습니다.

**연결 방식:** `main.js`가 `window.selectOption(btn)`, `window.checkQuiz(containerId)`, `window.resetQuiz(containerId)`를 노출합니다.

**HTML:**
```html
<div class="quiz-container animate-in" id="quiz-module3">
  <div class="quiz-question-block"
       data-correct="option-b"
       data-explanation-right="② | 그룹 안의 모든 응답이 같은 보상을 받으면 어드밴티지가 0이 되므로 모델은 해당 그룹에서 학습할 수 없다."
       data-explanation-wrong="| 정답은 ②이다. 그룹 안의 모든 응답이 같은 보상을 받으면 보상의 평균과 각 응답의 보상이 같아지므로 어드밴티지가 0이 된다.">
    <h3 class="quiz-question"><span class="q-num">1</span>한 그룹의 모든 응답이 같은 보상을 받을 때 GRPO에 대한 설명으로 옳은 것은?</h3>
    <div class="quiz-options">
      <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>① 모델이 응답 하나를 무작위로 골라 정답으로 삼는다.</span>
      </button>
      <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>② 어드밴티지가 0이 되어 모델이 이 그룹에서 학습하지 못한다.</span>
      </button>
      <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>③ 모델이 모든 응답의 확률을 낮춘다.</span>
      </button>
    </div>
    <div class="quiz-feedback"></div>
  </div>

  <button class="quiz-check-btn" onclick="checkQuiz('quiz-module3')">정답 확인</button>
  <button class="quiz-reset-btn" onclick="resetQuiz('quiz-module3')">다시 풀기</button>
</div>
```

**Rules:**
- `data-correct`, `data-explanation-right`, `data-explanation-wrong`은 `.quiz-question-block`에 둔다(`main.js`가 이 요소에서 읽는다). `.quiz-feedback`에 두지 않는다.
- 해설 형식은 `data-explanation-right="② | ~이므로 ~이다."`, `data-explanation-wrong="| 정답은 ②이다. ~이다."`이다. `정답`/`오답` 표지는 `main.js`가 붙이므로 쓰지 않는다(KO110).
- 해설 속성 안에 `$…$` 수식을 쓸 수 있다. `main.js`가 피드백을 삽입한 뒤 KaTeX를 다시 렌더링한다. 숨은 가정 찾기의 해설도 같다.
- 확인 문제는 모듈마다 3~5문항이며 하나 이상은 부정형(`옳지 않은 것은?`) 또는 보기형이다.
- **문항 번호:** `.quiz-question` 맨 앞에 `<span class="q-num">1</span>`을 쓴다. 문항 번호 블록은 CSS가 그리므로 `1. `을 텍스트로 쓰지 않는다.
- **배점:** 어려운 문항 끝에 `<span class="q-points">[3점]</span>`을 붙인다(수능 관례). 모든 문항에 붙이지 않는다.
- **짧은 선택지:** 선택지가 매우 짧으면(기호, 숫자) `<div class="quiz-options row">`로 한 줄에 여러 개 배치한다.
- **2단:** 코넬 페이지 안에서 1200px 이상이면 문항이 2단(시험지식)으로 배치된다. 정답 확인 버튼은 1열, 다시 풀기 버튼은 2열 아래에 놓인다.
- **페이지당 최대 2문항:** 선택지 5개씩과 정답 확인 뒤 펼쳐지는 해설이 765px 안에 들어와야 한다. 3문항 이상이면 `.quiz-container`를 여러 개로 나누어 각각 코넬 페이지에 둔다. 각 컨테이너는 고유한 id와 자기 `정답 확인`/`다시 풀기` 버튼(`checkQuiz('quiz-module3a')` 등)을 가진다.

**보기형 문항(`<보기>` 상자):** 발문 바로 아래에 `.bogi` 상자를 넣는다. 상자 제목 `<보기>`는 CSS가 표시하므로 쓰지 않는다. 텍스트 속 `<보기>`는 `&lt;보기&gt;`로 이스케이프하고, 줄바꿈으로 `<보기` / `>`가 갈라지지 않도록 `<span class="nobr">&lt;보기&gt;에서</span>`로 감싼다.
```html
<h3 class="quiz-question"><span class="q-num">1</span>LoPE에 대한 설명으로 옳은 것만을 <span class="nobr">&lt;보기&gt;에서</span> 있는 대로 고른 것은?</h3>
<div class="bogi">
  <p>ㄱ. 프롬프트 앞에 의미 없는 텍스트를 붙여 응답 분포를 넓힌다.</p>
  <p>ㄴ. 보상 함수를 새로 학습해야 한다.</p>
  <p>ㄷ. 어드밴티지가 0인 그룹의 비율을 줄인다.</p>
</div>
<!-- 선택지: ① ㄱ  ② ㄴ  ③ ㄱ, ㄷ  ④ ㄴ, ㄷ  ⑤ ㄱ, ㄴ, ㄷ -->
```

---

## 드래그 앤 드롭 매칭 (Drag-and-Drop Matching)

codebase-to-course와 같은 패턴이며 개념과 정의, 방법과 논문 등을 짝짓는 데 맞게 조정했습니다.

**HTML:**
```html
<div class="dnd-container animate-in" id="dnd-module2">
  <div class="dnd-chips">
    <div class="dnd-chip" draggable="true" data-answer="grpo">GRPO</div>
    <div class="dnd-chip" draggable="true" data-answer="ppo">PPO</div>
    <div class="dnd-chip" draggable="true" data-answer="reinforce">REINFORCE</div>
  </div>
  <div class="dnd-zones">
    <div class="dnd-zone" data-correct="grpo">
      <p class="dnd-zone-label">그룹 내 상대 어드밴티지를 추정하며 가치 네트워크가 필요 없다.</p>
      <div class="dnd-zone-target">여기에 놓으시오</div>
    </div>
    <div class="dnd-zone" data-correct="ppo">
      <p class="dnd-zone-label">클리핑한 목적 함수로 정책 갱신 폭을 제한한다.</p>
      <div class="dnd-zone-target">여기에 놓으시오</div>
    </div>
    <div class="dnd-zone" data-correct="reinforce">
      <p class="dnd-zone-label">몬테카를로 샘플링을 쓰는 가장 기본적인 정책 경사 방법이다.</p>
      <div class="dnd-zone-target">여기에 놓으시오</div>
    </div>
  </div>
  <div style="margin-top:var(--space-4)">
    <button class="btn" onclick="checkDnD('dnd-module2')">매칭 확인</button>
    <button class="btn" onclick="resetDnD('dnd-module2')">초기화</button>
  </div>
</div>
```

---

## 숨은 가정 찾기 (Spot the Assumption)

주장이나 실험 설정을 보여 주고 숨은 가정을 찾게 합니다.

**연결 방식:** `window.selectAssumption(btn)`과 `window.checkAssumption(containerId)`로 퀴즈 방식의 선택을 처리합니다.

**HTML:**
```html
<div class="assumption-challenge animate-in" id="assumption-1"
     data-correct="option-b"
     data-explanation-right="② | 논문은 수학 추론 과제에서만 실험했으므로, 코드나 상식 추론 같은 다른 추론 유형에서도 효과가 있다는 가정이 숨어 있다. 이 가정은 검증되지 않았다."
     data-explanation-wrong="| 정답은 ②이다. 실험 범위가 수학 추론으로 한정되어 있으므로 결론이 다른 과제에도 일반화되는지가 핵심이다.">
  <h3>다음 결론에 숨어 있는 가정으로 가장 적절한 것을 고르시오.</h3>
  <div class="assumption-claim">
    “LoPE는 프롬프트 공간에 교란을 더해 대규모 언어 모델의 추론 탐색 능력을 효과적으로 높였다.”
  </div>
  <div class="assumption-options">
    <button class="assumption-option" data-value="option-a" onclick="selectAssumption(this)">
      <div class="quiz-option-radio"></div>
      <span>① Lorem Ipsum이 가장 좋은 교란 텍스트라고 가정한다.</span>
    </button>
    <button class="assumption-option" data-value="option-b" onclick="selectAssumption(this)">
      <div class="quiz-option-radio"></div>
      <span>② 수학 추론에서 얻은 향상이 다른 추론 과제에도 일반화된다고 가정한다.</span>
    </button>
    <button class="assumption-option" data-value="option-c" onclick="selectAssumption(this)">
      <div class="quiz-option-radio"></div>
      <span>③ 더 큰 모델일수록 항상 더 큰 향상을 얻는다고 가정한다.</span>
    </button>
  </div>
  <div class="assumption-feedback"></div>
  <button class="quiz-check-btn" onclick="checkAssumption('assumption-1')">정답 확인</button>
</div>
```

---

## 어블레이션 토글 (Ablation Toggle)

구성 요소를 하나씩 제거했을 때의 실험 결과를 보여 줍니다. 각 탭은 한 부분을 제거했을 때 어떻게 되는지 나타냅니다.

**연결 방식:** `window.showLayer(layerId, btn)`을 쓰며 레이어 토글과 같은 엔진입니다.

**HTML:**
```html
<div class="ablation-demo animate-in">
  <div class="ablation-tabs">
    <button class="ablation-tab active" onclick="showLayer('full', this)">전체 LoPE</button>
    <button class="ablation-tab" onclick="showLayer('no-prefix', this)">무작위 접두어 제거</button>
    <button class="ablation-tab" onclick="showLayer('no-norm', this)">정규화 제거</button>
  </div>
  <div class="ablation-viewport">
    <div class="ablation-layer" id="full" style="display:block">
      <div class="ablation-metric">78.3%</div>
      <div class="ablation-delta positive">기준 모델 대비 +6.2%p</div>
      <p class="ablation-description">전체 방법: 무작위 접두어와 그룹 내 정규화 어드밴티지를 모두 사용한다.</p>
    </div>
    <div class="ablation-layer" id="no-prefix" style="display:none">
      <div class="ablation-metric">72.1%</div>
      <div class="ablation-delta neutral">기준 모델과 같음</div>
      <p class="ablation-description">무작위 접두어를 빼면 방법이 표준 GRPO와 같아진다.</p>
    </div>
    <div class="ablation-layer" id="no-norm" style="display:none">
      <div class="ablation-metric">74.8%</div>
      <div class="ablation-delta positive">기준 모델 대비 +2.7%p</div>
      <p class="ablation-description">정규화를 빼도 향상은 있지만 효과가 줄어든다.</p>
    </div>
  </div>
</div>
```

---

## 콜아웃 박스 (Callout Boxes)

선택 코너(`보충 설명`, `더 알아보기`)는 모듈당 최대 2개까지 씁니다. 고정 코너인 `학습 목표`와 `핵심 정리`는 이 개수에 넣지 않습니다.

콜아웃은 테두리 상자이며 `.callout-title`이 교과 색(또는 변형 색) 칩으로 그려진다. `.callout-icon`은 CSS가 숨기므로 이모지는 화면에 보이지 않는다. 아이콘 div는 있어도 없어도 되며, 새로 쓸 때는 생략해도 된다.

```html
<div class="callout callout-accent animate-in">
  <div class="callout-icon">&#128161;</div>
  <div class="callout-content">
    <strong class="callout-title">핵심 정리</strong>
    <p>LoPE는 모델이나 보상 함수를 바꾸지 않고 입력만 바꾼다. 이 점이 LoPE에서 가장 직관에 반하는 부분이다.</p>
  </div>
</div>
```

**변형:**
- `callout-accent`: 핵심 통찰 (제목: 핵심 정리)
- `callout-info`: 알아 두면 좋은 정보 (제목: 보충 설명)
- `callout-warning`: 흔한 오해 (제목: 더 알아보기)
- `callout-info` + 제목 `배경 지식`: 배경 전용 화면 표시("모듈 골격과 내비게이션" 절). 개수 상한에 넣지 않는다.

---

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
  <div class="contribution-card">
    <div class="contribution-num">2</div>
    <div class="contribution-text">
      <strong>제로 어드밴티지 문제 해결</strong>
      <p>교란으로 샘플링 결과를 다양하게 만들어 모든 응답이 같은 보상을 받는 상황을 피한다.</p>
    </div>
  </div>
</div>
```

---

## 논문 인용 카드 (Paper Citation Cards)

```html
<div class="paper-citation animate-in">
  <div class="paper-citation-title">DeepSeekMath: Pushing the Limits of Mathematical Reasoning</div>
  <div class="paper-citation-authors">Shao et al., 2024</div>
  <div class="paper-citation-summary">그룹 내 상대 어드밴티지 추정으로 가치 네트워크를 대체해 RL 학습 과정을 단순화한 GRPO 방법을 제안했다. 본 논문은 이를 바탕으로 프롬프트 공간 교란을 더 깊이 탐구한다.</div>
</div>
```

---

## 흐름도 (Flow Diagrams)

```html
<div class="flow-steps animate-in">
  <div class="flow-step">
    <div class="flow-step-num">1</div>
    <p>원본 프롬프트</p>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step">
    <div class="flow-step-num">2</div>
    <p>노이즈 접두어 추가</p>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step">
    <div class="flow-step-num">3</div>
    <p>모델이 응답 G개 샘플링</p>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step">
    <div class="flow-step-num">4</div>
    <p>보상 평가 및 GRPO 갱신</p>
  </div>
</div>
```

---

## 데이터 표 (Data Table)

논문의 표를 옮기거나 항목을 비교할 때 쓴다. 일반 `<table>` 대신 `.data-table`을 쓴다. 숫자 열은 `th`와 `td` 모두에 `.num`을 달아 오른쪽 정렬하고, 강조할 행은 `tr.hl`로 교과 색 하나만 쓴다. 캡션은 표 아래에 표시되며 `~을 나타낸 것이다.` 형식과 논문 표 번호를 쓴다. 한 페이지의 표는 8행 이하로 하고, 넘치면 페이지를 나눈다.
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

---

## 용어 툴팁 (Glossary Tooltips)

모듈마다 모든 전문 용어를 첫 등장 시 표시합니다.

```html
<p>LoPE는
  <span class="term" data-definition="그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO): 같은 그룹 안의 여러 응답을 서로 비교해 모델을 갱신하는 강화 학습 방법. 별도의 가치 네트워크가 필요 없음.">GRPO</span>를 기본 학습 프레임워크로 삼고
  <span class="term" data-definition="프롬프트 공간(Prompt Space): 모델이 입력으로 받는 텍스트가 이루는 공간. 프롬프트를 바꾸면 모델이 보는 입력이 달라짐.">프롬프트 공간</span>에 교란을 도입한다.
</p>
```

**Rules:**
- 모듈마다 모든 전문 용어를 첫 등장 시 표시합니다.
- 정의는 일상어로 1~2문장 안에 씁니다. 정의는 사전식 명사형 종결(`~것.`, `~함.`, `~임.`, 명사)로 끝낸다. `~이다.`, `~한다.`, `~없다.`로 끝내지 않는다(KO111).
- 이중 언어 형식 `한글 용어(English Term): 설명`을 씁니다. 괄호는 반각 `( )`이며 괄호 앞에 공백을 두지 않습니다. 예: `정책 경사(Policy Gradient): 보상을 높이는 방향으로 정책 파라미터를 직접 갱신하는 최적화 방법`
- 같은 화면에서 같은 용어를 두 번 표시하지 않습니다.
- `cursor: pointer`를 씁니다(`cursor: help`는 쓰지 않습니다).

---

## 번호 단계 카드 (Numbered Step Cards)

```html
<div class="step-cards stagger-children animate-in">
  <div class="step-card">
    <div class="step-num">1</div>
    <div class="step-body">
      <strong>샘플링 단계</strong>
      <p>질문마다 응답 G개를 생성한다. 표준 GRPO 샘플링을 사용한다.</p>
    </div>
  </div>
  <div class="step-card">
    <div class="step-num">2</div>
    <div class="step-body">
      <strong>교란 단계</strong>
      <p>일부 샘플의 질문 앞에 무작위 Lorem Ipsum 접두어를 붙인다.</p>
    </div>
  </div>
</div>
```

---

## 아이콘 라벨 행 (Icon-Label Rows)

아이콘 칸에는 이모지 대신 짧은 글자나 단순한 기호 글자를 넣고, 배경은 교과 색 또는 먹색만 쓴다(`--color-actor-*` 금지).

```html
<div class="icon-rows stagger-children animate-in">
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-accent)">M</div>
    <div>
      <strong>수학 추론 벤치마크</strong>
      <p>GSM8K, MATH, Minerva 등의 데이터셋</p>
    </div>
  </div>
  <div class="icon-row">
    <div class="icon-circle" style="background: #1F2328">B</div>
    <div>
      <strong>모델 규모</strong>
      <p>파라미터 1.7B, 4B, 7B 규모의 모델</p>
    </div>
  </div>
</div>
```


## 첫 페이지: 왜 썼는가와 새로운 점

1단원(`module-0`, 화면 번호 1) 첫 페이지(단원 도입 + 첫 화면)는 한 장으로 논문의 동기와 기여를 전한다. 이 쪽은 논문 1절 "왜 썼나·새로운 점" 쪽이므로 화면 제목에 `.paper-ref`(논문 1절)를 달고 `배경 지식` 콜아웃은 두지 않는다. 모듈 0의 나머지 쪽이 배경 지식 쪽이다. 765px 안에 다음 세 가지를 순서대로 둔다.

1. **문제 문단:** 이전 방식의 한계와 이 논문을 쓴 이유를 2~3문장으로.
2. **비교 그림:** `.svg-diagram`을 둘로 나누어 왼쪽 "이전 방식", 오른쪽 "제안 방식"(교과 색). 같은 입력(예: $x_1, \ldots, x_4$)을 같은 위치에 두고 처리 경로만 다르게 그린다. 간선은 직각, 패널 아래에 차이를 한 줄로(예: "순차 단계 $n$번" 대 "1번").
3. **새로운 점:** `.callout.callout-accent` 안 `<ol>` 3개 이내. 항목마다 `<strong>이름:</strong>` + 논문 수치 근거.

**비교 그림 골격.** 하나의 `.svg-diagram` 안 viewBox를 둘로 나눈다(왼쪽 0~392 이전 방식, 오른쪽 408~800 제안 방식). 입력 노드는 두 패널에서 같은 y에 놓고, 간선은 직각 `<path>`로 그린다.
```html
<div class="svg-diagram animate-in">
  <svg viewBox="0 0 800 216" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="이전 방식은 순차 처리, 제안 방식은 한 번에 처리함">
    <!-- 왼쪽: 이전 방식 (먹색) -->
    <foreignObject x="16" y="8" width="360" height="24"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span>이전 방식</span></div></foreignObject>
    <rect class="node-rect" x="16" y="48" width="72" height="48" rx="12"/>
    <foreignObject x="20" y="52" width="64" height="40"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label"><span><i class="mi">x</i><sub>1</sub></span></div></foreignObject>
    <path class="edge-line" d="M88,72 H112"/>
    <polygon class="edge-arrow" points="112,67 122,72 112,77"/>
    <!-- … 같은 간격으로 x₂, x₃, x₄ -->
    <!-- 오른쪽: 제안 방식 (교과 색) — 입력 위치는 왼쪽과 같게 -->
    <rect class="node-rect accent" x="408" y="48" width="72" height="48" rx="12"/>
    <!-- … -->
    <!-- 패널 아래: 핵심 비교 -->
    <foreignObject x="16" y="176" width="368" height="32"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px; color:var(--color-text-secondary)"><span>순차 단계 <i class="mi">n</i>번</span></div></foreignObject>
    <foreignObject x="408" y="176" width="376" height="32"><div xmlns="http://www.w3.org/1999/xhtml" class="node-label" style="font-size:14px"><span>한 번에 1번</span></div></foreignObject>
  </svg>
</div>
```
교과 색(`accent`)은 제안 방식 쪽에만 쓴다(그림당 유채색 하나).

## 연구 계보: 이어받은 것과 달라진 것

갈래마다 노드 뒤에 `<p class="lineage-note">이어받은 것. → <strong class="novelty">달라진 것</strong>.</p>`를 둔다. 루트 노드에는 `<span class="novelty-badge">한 줄 기여</span>`. `.lineage-branch`는 가로 flex이므로 `edge-label`, 노드, `.lineage-note`가 한 줄에 놓이고, 더 이른 선행 연구는 그 갈래 안에 `.lineage-branch`를 중첩한다.
```html
<div class="lineage-tree animate-in">
  <div class="lineage-node lineage-root" data-detail="어텐션 기반 번역 모델: 순환 없이 어텐션만으로 시퀀스를 변환하는 방법">
    <span class="lineage-label">트랜스포머</span>
    <span class="lineage-detail">본 논문 (2017)</span>
    <span class="novelty-badge">순환 없이 어텐션만 사용</span>
  </div>
  <div class="lineage-branch">
    <div class="lineage-edge-label">개선</div>
    <div class="lineage-node" data-detail="어텐션 결합 RNN(Attention-based RNN): 순환 신경망의 출력에 어텐션을 더한 번역 모델">
      <span class="lineage-label">어텐션 RNN</span>
      <span class="lineage-detail">Bahdanau et al., 2014</span>
    </div>
    <p class="lineage-note">입력 위치별 가중합으로 문맥을 읽는 어텐션. → <strong class="novelty">순환을 없애고 병렬로 계산</strong>한다.</p>
    <div class="lineage-branch">
      <div class="lineage-edge-label">기반</div>
      <div class="lineage-node" data-detail="순차열 변환(Seq2Seq): 인코더와 디코더 두 RNN으로 시퀀스를 다른 시퀀스로 바꾸는 모델">
        <span class="lineage-label">Seq2Seq</span>
        <span class="lineage-detail">Sutskever et al., 2014</span>
      </div>
      <p class="lineage-note">인코더-디코더 구조. → <strong class="novelty">고정 길이 벡터 병목</strong>을 없앤다.</p>
    </div>
  </div>
</div>
```
 단서 칸에는 "새로운 점" 콜아웃으로 앞선 연구와의 차이를 한 문장으로 쓴다.


## 구조도와 차이 비교(보충 자료 조사 결과를 담는 패턴)

**전체 구조도.** `.svg-diagram`에 구성 요소를 `.node-rect.sq`, 흐름을 직각 `path.edge-line`으로 그린다. 오프라인/온라인 구획은 `guide-fill` 배경 사각형 두 개와 왼쪽 위 작은 라벨(`text.muted`)로 나눈다. 상자 안 둘째 줄에 입력·출력 예를 `text.mono`로 단다(예: `질문 → 768차원 벡터`).

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

**차이 비교.** 같은 입력 하나를 형제 개념 각각에 넣은 결과를 세로 칸으로 나란히 그리고(칸 제목 = 개념 이름, 같은 높이의 단계 상자), 아래에 비교표와 `핵심 비교`를 둔다.

```html
<table class="data-table">
  <thead><tr><th>기준</th><th>Naive RAG</th><th>Advanced RAG</th><th>Modular RAG</th></tr></thead>
  <tbody>
    <tr><td>검색 전</td><td>없음</td><td>query rewriting</td><td>모듈로 교체·추가</td></tr>
    <tr><td>검색 후</td><td>없음</td><td>reranking, 압축</td><td>모듈로 교체·추가</td></tr>
    <tr><td>흐름</td><td>한 방향</td><td>한 방향</td><td>반복·분기 가능</td></tr>
  </tbody>
  <caption>표는 세 방식의 차이를 나타낸 것이다.</caption>
</table>
<p class="diff-line"><strong>핵심 비교</strong> Naive는 검색 → 생성뿐, Advanced는 그 앞뒤를 다듬고, Modular는 단계 자체를 갈아 끼운다.</p>
```
