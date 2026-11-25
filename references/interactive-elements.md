# 인터랙티브 요소 레퍼런스

paper-to-course 튜토리얼에서 사용하는 모든 인터랙티브 요소의 구현 패턴입니다.

> **구조 참고:** CSS와 JavaScript는 모두 `references/styles.css`와 `references/main.js`에 있으며, 각 강의 디렉터리에 그대로 복사됩니다. 아래 HTML 패턴만 작성하고 인라인 `<style>`이나 `<script>`는 쓰지 않습니다.
> **중요:** 클래스명, `data-*` 속성명, id, HTML 구조는 `main.js`와 `styles.css`가 의존하므로 절대 바꾸지 않습니다. 사람이 읽는 텍스트와 속성 값(`data-definition`, `data-explanation-right` 등)만 한국어로 작성합니다.

## 목차
0. [모듈 골격과 내비게이션 (Module Skeleton & Navigation)](#모듈-골격과-내비게이션-module-skeleton--navigation)
1. [표지와 히어로 섹션 (Cover Page)](#표지와-히어로-섹션-cover-page)
2. [수식 유도 단계별 풀이 (Math Derivation Walkthrough)](#수식-유도-단계별-풀이-math-derivation-walkthrough)
3. [의사코드 단계별 풀이 (Pseudocode Walkthrough)](#의사코드-단계별-풀이-pseudocode-walkthrough)
4. [결과 비교 인터랙티브 (Result Comparison)](#결과-비교-인터랙티브-result-comparison)
5. [연구 계보 트리 (Research Lineage Tree)](#연구-계보-트리-research-lineage-tree)
6. [연구 대화 (Research Dialogue)](#연구-대화-research-dialogue)
7. [SVG 다이어그램 (SVG Diagrams)](#svg-다이어그램-svg-diagrams)
8. [객관식 퀴즈 (Multiple-Choice Quizzes)](#객관식-퀴즈-multiple-choice-quizzes)
9. [드래그 앤 드롭 매칭 (Drag-and-Drop Matching)](#드래그-앤-드롭-매칭-drag-and-drop-matching)
10. [숨은 가정 찾기 (Spot the Assumption)](#숨은-가정-찾기-spot-the-assumption)
11. [어블레이션 토글 (Ablation Toggle)](#어블레이션-토글-ablation-toggle)
12. [콜아웃 박스 (Callout Boxes)](#콜아웃-박스-callout-boxes)
13. [기여 및 개념 카드 (Contribution Cards)](#기여-및-개념-카드-contribution-cards)
14. [논문 인용 카드 (Paper Citation Cards)](#논문-인용-카드-paper-citation-cards)
15. [흐름도 (Flow Diagrams)](#흐름도-flow-diagrams)
16. [용어 툴팁 (Glossary Tooltips)](#용어-툴팁-glossary-tooltips)
17. [번호 단계 카드 (Numbered Step Cards)](#번호-단계-카드-numbered-step-cards)
18. [아이콘 라벨 행 (Icon-Label Rows)](#아이콘-라벨-행-icon-label-rows)

---

## 한국어 콘텐츠 작성 원칙 (요약)

- **문체(EBS 교재 문체):** 본문·설명·콜아웃·카드·툴팁 정의는 한다체 평서형(`~이다 / ~한다 / ~된다`)으로 쓴다. `여러분`, 수사적 의문문, 감탄 표현은 쓰지 않는다. 문항의 해설과 피드백도 한다체이며 칭찬하지 않는다. 예외로 연구 대화(채팅)의 등장인물 대사는 해요체를 허용한다.
- **문항 형식:** 발문은 `다음 중 ~에 대한 설명으로 옳은 것은?` 또는 `~으로 옳지 않은 것은?` 형태로 쓰고, 지시는 `~하시오`로 쓴다. 선택지 텍스트 앞에 `①②③④`를 붙인다(`data-value`, `data-correct` 값은 그대로 둔다). `main.js`가 피드백 앞에 `정답`/`오답` 표지를 자동으로 붙이므로, 해설 속성은 표지 없이 쓴다. 맞힌 경우 `data-explanation-right="② | ~이므로 ~이다."`, 틀린 경우 `data-explanation-wrong="| 정답은 ②이다. ~이므로 ~이다."` 형식이다(화면: **정답** ② | … / **오답** | 정답은 ②이다. …).
- **코너 이름:** `학습 목표`(모듈 맨 앞), `개념 체크`(용어·정의 확인), `탐구 자료`(실험 결과·그래프·대화 자료), `보충 설명`(알아 두면 좋은 정보, `callout-info`), `핵심 정리`(핵심 통찰, `callout-accent`), `더 알아보기`(오해 바로잡기, 심화, `callout-warning`)를 콜아웃 제목에 쓴다. 모듈 끝의 문항 묶음은 `확인 문제`이다.
- **학습 목표 패턴:** 각 모듈 맨 위에 `이 모듈을 학습하면 다음을 할 수 있다.` 다음에 `GRPO의 어드밴티지 계산 과정을 설명할 수 있다.`, `기준선과 제안 방법의 성능을 비교할 수 있다.`처럼 `~을 설명할 수 있다 / ~을 비교할 수 있다` 형태의 목표를 2~3개 쓴다.
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

**모듈 파일(`modules/0N-slug.html`) 골격:**
```html
<section class="module" id="module-1">
  <div class="module-content">

    <div class="module-header">
      <span class="module-number">01</span>
      <h2 class="module-title">핵심 아이디어: 어텐션 연산</h2>
      <p class="module-subtitle">쿼리, 키, 값으로 토큰 사이의 관련도를 계산하는 과정을 익힌다</p>
    </div>

    <!-- 첫 화면: 학습 목표 -->
    <div class="screen">
      <div class="callout callout-info animate-in">
        <div class="callout-icon">&#127919;</div>
        <div class="callout-content">
          <strong class="callout-title">학습 목표</strong>
          <p>이 모듈을 학습하면 다음을 할 수 있다.</p>
          <ol>
            <li>쿼리와 키의 내적이 관련도를 나타내는 이유를 설명할 수 있다.</li>
            <li>소프트맥스 가중합으로 출력이 만들어지는 과정을 설명할 수 있다.</li>
          </ol>
        </div>
      </div>
      <h3 class="screen-heading">화면 제목</h3>
      <p>본문(한다체)...</p>
    </div>

    <!-- 이어지는 화면들: 개념 설명, 개념 체크, 탐구 자료 -->
    <div class="screen">
      <h3 class="screen-heading">다음 화면 제목</h3>
      ...
    </div>

    <!-- 끝: 핵심 정리 → 확인 문제 -->
    <div class="screen">
      <div class="callout callout-accent animate-in">...핵심 정리...</div>
      <h3 class="screen-heading">확인 문제</h3>
      <div class="quiz-container" id="quiz-module1">...</div>
    </div>

  </div>
</section>
```

**Rules:**
- `<section class="module" id="module-N">`의 `N`은 0부터 연속한 번호이다. 메뉴의 모듈 수보다 적게 만들어도 번호를 건너뛰지 않고 `module-0`, `module-1`, …로 매기고 파일명도 `00-`, `01-`, …로 매긴다.
- `.module-number`는 두 자리 숫자(`00`, `01`)이다. 장식 문자이며 CSS가 옅게 표시한다.
- 모듈 제목은 `<h2 class="module-title">`, 화면 제목은 `<h3 class="screen-heading">`이다. 화면 안의 더 작은 제목은 `<h4>`를 쓴다.
- 모듈 하나의 화면(`.screen`)은 3~6개이다. 배경 색 교차(짝수·홀수 모듈)는 CSS가 처리하므로 별도 클래스를 붙이지 않는다.
- `.module-content` 밖에 보일러플레이트(`<html>`, `<head>`, `<script>`)를 두지 않는다.

**배경 지식 표시:** 논문 이전의 배경만 다루는 화면(모듈 0의 모든 화면, 그 밖의 배경 전용 콜아웃)은 화면 맨 위에 `배경 지식` 콜아웃을 둔다. 전용 소형 라벨 클래스가 `styles.css`에 없으므로 `callout callout-info`를 쓴다. 이 콜아웃은 `보충 설명`·`더 알아보기`의 모듈당 2개 상한에 넣지 않는다.
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
<button class="nav-dot" data-target="module-1" data-tooltip="핵심 아이디어: 어텐션 연산" aria-label="모듈 1: 핵심 아이디어: 어텐션 연산"></button>
```
**`_base.html`의 SIDEBAR_ITEMS(모듈마다 하나):**
```html
<a class="sidebar-item" data-module="1" href="#module-1"><span class="sidebar-item-num">01</span><span class="sidebar-item-label">핵심 아이디어: 어텐션 연산</span><span class="sidebar-item-indicator"></span></a>
```

**Rules:**
- `data-target`은 `#` 없이 id만 쓴다(`module-1`). 사이드바의 `href`는 `#module-1`처럼 `#`을 붙인다.
- `data-tooltip`에는 모듈 제목을 쓴다(CSS가 `attr(data-tooltip)`로 표시한다).
- `sidebar-item-num`은 모듈 번호와 같은 두 자리, `sidebar-item-label`은 모듈 제목이다.
- 첫 번째 항목(`module-0`)에만 `active`를 미리 붙이지 않는다. 활성 상태는 스크롤에 따라 `main.js`가 붙인다.

---

## 표지와 히어로 섹션 (Cover Page)

강의 표지는 모든 모듈 앞에 나오는 전체 화면 랜딩 페이지입니다. `.module`이 아니므로 내비게이션 점이 없고 스크롤 스냅에도 참여하지 않습니다.

**연결 방식:** "학습 시작하기" 버튼은 모듈 0으로 스크롤합니다. `main.js`의 표지 CTA 리스너가 처리합니다.

**HTML:**
```html
<section class="course-cover">
  <div class="course-cover-inner">
    <span class="course-cover-badge">인터랙티브 튜토리얼</span>
    <h1 class="course-cover-title">프롬프트 공간 교란이 추론 탐색을 넓히는 방법(Nonsense Helps)</h1>
    <p class="course-cover-subtitle">프롬프트에 무작위 노이즈를 더하면 LLM 학습에서 추론 탐색이 넓어지는 원리를 알아본다</p>
    <p class="course-cover-authors">Yuntao Bai et al. · arXiv 2026</p>
    <div class="course-cover-meta">
      <span class="course-cover-meta-item">&#128218; 모듈 7개</span>
      <span class="course-cover-meta-item">&#9201; 약 45분</span>
      <span class="course-cover-meta-item">&#127891; 중급</span>
    </div>
    <div class="course-cover-abstract">
      <span class="course-cover-abstract-label">초록</span>
      <p>이 논문은 프롬프트 공간에 Lorem Ipsum 같은 무작위 노이즈를 더해 GRPO의 탐색을 촉진하는 LoPE 방법을 제안한다. 이 방법으로 제로 어드밴티지(Zero Advantage) 문제를 해결한다...</p>
    </div>
    <a href="#module-0" class="course-cover-cta">학습 시작하기 →</a>
  </div>
</section>
```

**Rules:**
- 표지는 `.module` 섹션이 아닙니다. `scroll-snap-align`과 모듈 번호를 두지 않습니다.
- "학습 시작하기" 버튼은 모듈 0(사전 지식 모듈)으로 스크롤합니다.
- 논문 제목은 `한국어 제목(English Original Title)` 형식으로 씁니다. 괄호는 반각이고 괄호 앞에 공백을 두지 않습니다(KO103). 배지·메타·라벨 문구는 위 예시 그대로 씁니다("인터랙티브 튜토리얼", "초록").
- 초록은 논문 전체 초록이 아니라 2~3문장으로 줄여 씁니다.
- 메타 배지: 모듈 수, 예상 소요 시간(모듈당 대략 5~7분), 난이도를 넣습니다. 숫자와 단위는 붙여 씁니다(`모듈 7개`, `약 45분`).
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
      $$L_{GRPO} = -\mathbb{E}_{q \sim P(Q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{ref}(o_i|q)} A_i, \text{clip}(\cdot) A_i \right) \right]$$
    </div>
    <div class="math-explanation">
      <p>GRPO의 손실 함수는 모델의 응답이 참조 정책(Reference Policy)과 얼마나 다른지를 측정한다. 어드밴티지(Advantage) $A_i$는 각 응답이 평균에 비해 얼마나 좋은지를 나타낸다.</p>
    </div>
  </div>

  <div class="math-step" data-step="1" style="display:none">
    <div class="math-equation">
      $$A_i = \frac{r_i - \text{mean}(\{r_1, ..., r_G\})}{\text{std}(\{r_1, ..., r_G\})}$$
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
      <span class="result-label">GRPO 기준선</span>
      <div class="result-bar-track"><div class="result-fill baseline" style="width:0%"></div></div>
      <span class="result-value"></span>
    </div>
    <div class="result-bar" data-accuracy="68.5" data-pass1="54.3">
      <span class="result-label">PPO 기준선</span>
      <div class="result-bar-track"><div class="result-fill baseline" style="width:0%"></div></div>
      <span class="result-value"></span>
    </div>
  </div>
</div>
```

**Rules:**
- 제안 방법 막대는 `.result-fill.ours`(강조색), 기준선 막대는 `.result-fill.baseline`(회색)을 씁니다.
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
    <div class="lineage-node" data-detail="인간 피드백 기반 강화학습(Reinforcement Learning from Human Feedback)">
      <span class="lineage-label">RLHF</span>
      <span class="lineage-detail">Ouyang et al., 2022</span>
    </div>
  </div>
</div>
```

**SVG 기반 트리 (복잡한 계보용):**
```html
<div class="svg-diagram">
  <svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <rect class="node-rect accent" x="300" y="20" width="200" height="60" rx="12"/>
    <text x="400" y="50" text-anchor="middle" font-weight="700" font-size="14">LoPE</text>
    <text x="400" y="68" text-anchor="middle" font-size="11" fill="#9E9790">본 논문, 2026</text>

    <line class="edge-line accent" x1="400" y1="80" x2="200" y2="150"/>
    <text x="280" y="115" font-size="10" fill="#9E9790" font-weight="500">개선</text>
    <rect class="node-rect" x="100" y="150" width="200" height="60" rx="12"/>
    <text x="200" y="180" text-anchor="middle" font-weight="700" font-size="14">GRPO</text>

    <line class="edge-line" x1="200" y1="210" x2="200" y2="280"/>
    <rect class="node-rect" x="100" y="280" width="200" height="60" rx="12"/>
    <text x="200" y="310" text-anchor="middle" font-weight="700" font-size="14">PPO</text>
  </svg>
</div>
```

---

## 연구 대화 (Research Dialogue)

연구자나 방법들이 어떤 개념을 두고 "토론"하는 모습을 보여 주는 메신저 스타일 채팅입니다. codebase-to-course의 그룹 채팅과 같은 엔진을 씁니다.

**연결 방식:** `main.js`가 모든 `.chat-window`를 자동으로 초기화합니다. 컨트롤은 `.chat-next-btn`, `.chat-all-btn`, `.chat-reset-btn`, 진행 표시는 `.chat-progress`입니다.

**HTML:**
```html
<div class="chat-window animate-in" id="chat-module2">
  <div class="chat-messages">
    <div class="chat-message" data-msg="0" data-sender="researcher-a" style="display:none">
      <div class="chat-avatar" style="background: var(--color-actor-1)">학</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: var(--color-actor-1)">학생 A</span>
        <p>이거 그냥 데이터 증강(Data Augmentation) 아닌가요? 입력 앞에 무작위 텍스트를 붙이는 게 역번역(Back-translation)과 뭐가 다른가요?</p>
      </div>
    </div>
    <div class="chat-message" data-msg="1" data-sender="researcher-b" style="display:none">
      <div class="chat-avatar" style="background: var(--color-actor-2)">교</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: var(--color-actor-2)">교사</span>
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

**HTML:**
```html
<div class="svg-diagram animate-in">
  <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
    <!-- 예시: 실험 프레임워크 -->
    <rect class="node-rect accent" x="50" y="120" width="160" height="60" rx="12"/>
    <text x="130" y="150" text-anchor="middle" font-weight="700" font-size="13">원본 프롬프트 q</text>

    <line class="edge-line" x1="210" y1="150" x2="290" y2="150"/>
    <polygon class="edge-arrow" points="285,145 295,150 285,155"/>

    <rect class="node-rect" x="290" y="120" width="160" height="60" rx="12"/>
    <text x="370" y="145" text-anchor="middle" font-weight="600" font-size="13">노이즈 추가</text>
    <text x="370" y="163" text-anchor="middle" font-size="11" fill="#9E9790">Lorem Ipsum</text>

    <line class="edge-line" x1="450" y1="150" x2="530" y2="150"/>
    <polygon class="edge-arrow" points="525,145 535,150 525,155"/>

    <rect class="node-rect accent" x="530" y="120" width="160" height="60" rx="12"/>
    <text x="610" y="145" text-anchor="middle" font-weight="700" font-size="13">모델 샘플링</text>
    <text x="610" y="163" text-anchor="middle" font-size="11" fill="#9E9790">π(o|q')</text>
  </svg>
</div>
```

**Rules:**
- 반응형으로 만들기 위해 `viewBox`를 쓰고 SVG에 `width="100%"`를 지정합니다.
- 색상은 인라인 `style` 속성에서 CSS 변수를 참조합니다.
- 노드 텍스트는 짧게(1~2줄) 씁니다.
- **한글 라벨은 박스를 더 넓게 잡습니다.** 한글은 글자 하나가 대략 1em 너비이므로 `font-size="13"`이면 글자당 약 13px로 계산해 박스 너비를 정합니다(위 예시의 "원본 프롬프트 q"는 약 9자라 약 120px가 필요합니다). `text-anchor="middle"`은 줄바꿈이 없습니다.
- **줄 수별 규칙:** 한 줄 라벨은 `<text>`를 씁니다. 두 줄이면 `<tspan x="…" dy="1.3em">`으로 나눌 수 있으나 어절 경계에서만 끊고 어절 중간에서는 끊지 않습니다. 세 줄 이상이거나 문단 길이의 텍스트는 아래처럼 `<foreignObject>` 안의 HTML에 `word-break: keep-all`을 적용합니다.
- SVG 텍스트에 `font-style="italic"`을 쓰지 않습니다. 한글에는 이탤릭이 없으므로 `font-weight="500"`이나 흐린 `fill`로 구분합니다.

```html
<foreignObject x="290" y="120" width="160" height="60">
  <div xmlns="http://www.w3.org/1999/xhtml" style="text-align:center; font-size:13px; word-break:keep-all">
    프롬프트 앞에 무작위 노이즈 추가
  </div>
</foreignObject>
```

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
    <h3 class="quiz-question">한 그룹의 모든 응답이 같은 보상을 받을 때 GRPO에 대한 설명으로 옳은 것은?</h3>
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

**보기형 문항(`<보기>` 상자):** 발문 바로 아래에 `.bogi` 상자를 넣는다. 상자 제목 `<보기>`는 CSS가 표시하므로 쓰지 않는다. 텍스트 속 `<보기>`는 `&lt;보기&gt;`로 이스케이프한다.
```html
<h3 class="quiz-question">LoPE에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?</h3>
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
      <div class="ablation-delta positive">기준선 대비 +6.2%p</div>
      <p class="ablation-description">전체 방법: 무작위 접두어와 그룹 내 정규화 어드밴티지를 모두 사용한다.</p>
    </div>
    <div class="ablation-layer" id="no-prefix" style="display:none">
      <div class="ablation-metric">72.1%</div>
      <div class="ablation-delta neutral">기준선과 같음</div>
      <p class="ablation-description">무작위 접두어를 빼면 방법이 표준 GRPO와 같아진다.</p>
    </div>
    <div class="ablation-layer" id="no-norm" style="display:none">
      <div class="ablation-metric">74.8%</div>
      <div class="ablation-delta positive">기준선 대비 +2.7%p</div>
      <p class="ablation-description">정규화를 빼도 향상은 있지만 효과가 줄어든다.</p>
    </div>
  </div>
</div>
```

---

## 콜아웃 박스 (Callout Boxes)

선택 코너(`보충 설명`, `더 알아보기`)는 모듈당 최대 2개까지 씁니다. 고정 코너인 `학습 목표`와 `핵심 정리`는 이 개수에 넣지 않습니다.

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

## 용어 툴팁 (Glossary Tooltips)

모듈마다 모든 전문 용어를 첫 등장 시 표시합니다.

```html
<p>LoPE는
  <span class="term" data-definition="그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO): 같은 그룹 안의 여러 응답을 서로 비교해 모델을 갱신하는 강화학습 방법으로, 별도의 가치 네트워크를 학습할 필요가 없다.">GRPO</span>를 기본 학습 프레임워크로 삼고
  <span class="term" data-definition="프롬프트 공간(Prompt Space): 모델이 입력으로 받는 텍스트가 이루는 공간이다. 프롬프트를 바꾸면 모델이 보는 입력이 달라진다.">프롬프트 공간</span>에 교란을 도입한다.
</p>
```

**Rules:**
- 모듈마다 모든 전문 용어를 첫 등장 시 표시합니다.
- 정의는 일상어로 1~2문장 안에 씁니다. 정의 문장은 한다체 평서형으로 쓴다.
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

```html
<div class="icon-rows stagger-children animate-in">
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-actor-1)">&#129513;</div>
    <div>
      <strong>수학 추론 벤치마크</strong>
      <p>GSM8K, MATH, Minerva 등의 데이터셋</p>
    </div>
  </div>
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-actor-2)">&#129504;</div>
    <div>
      <strong>모델 규모</strong>
      <p>파라미터 1.7B, 4B, 7B 규모의 모델</p>
    </div>
  </div>
</div>
```
