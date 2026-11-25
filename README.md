<div align="center">

# Paper-to-Course · Korean Edition

**논문을 검증 가능한 한국어 학습 산출물로 컴파일하는 Claude Code 스킬**

<a href="examples/attention-ko/"><img src="https://img.shields.io/badge/demo-Attention_Is_All_You_Need-1F6FB2?style=flat-square" alt="demo"></a>
<img src="https://img.shields.io/badge/output-ko--KR-1B7A50?style=flat-square" alt="ko-KR">
<img src="https://img.shields.io/badge/lint-16_rules-6B4FA8?style=flat-square" alt="16 lint rules">
<img src="https://img.shields.io/badge/runtime-zero_dependency_HTML-5B6570?style=flat-square" alt="zero dependency">
<a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache_2.0-5B6570?style=flat-square" alt="Apache 2.0"></a>

<br><br>

<img src="docs/images/cover.png" alt="「Attention Is All You Need」에서 생성한 강의의 표지. 왼쪽에 제목과 초록, 오른쪽에 모듈 차례" width="880">

<sub>입력: arXiv 1706.03762 · 출력: <a href="examples/attention-ko/"><code>examples/attention-ko/index.html</code></a> (단일 HTML, 서버 불필요)</sub>

</div>

<br>

## Why this matters

연구 성과는 논문으로 유통되지만, 논문은 **같은 분야 전문가가 읽는 것을 전제로 쓴 문서**다. 실무에서 논문을 만나는 엔지니어, 임상의, 애널리스트에게는 세 겹의 비용이 생긴다.

1. **언어 비용.** 주요 학술지와 학회의 논문은 대부분 영어로 출판된다. 한국어 사용자는 번역과 이해를 동시에 해야 한다.
2. **전제 지식 비용.** 논문은 선수 개념을 설명하지 않는다. 읽는 사람이 계보와 기호 체계를 따로 복원해야 한다.
3. **검증 비용.** LLM에 요약을 맡기면 빠르지만, 결과는 채팅 한 화면에 흩어지고 이해했는지 확인할 장치도, 원문의 어느 절과 대응하는지에 대한 추적성도 없다.

이 스킬의 목표는 **논문 한 편을 비전문가가 체계적으로 학습할 수 있는 산출물로 변환하는 과정을 재현 가능한 파이프라인으로 만드는 것**이다. 핵심 설계 원칙은 세 가지다.

| 원칙 | 구현 |
|---|---|
| **Traceability**: 학습 내용이 원문 어디에서 왔는지 항상 보인다 | 모듈은 `1, 2, 3` 연속 번호로 매기고, 화면 제목 끝에 논문 위치를 작은 태그로 남긴다 (`2 어텐션` → `스케일드 내적 어텐션` + `논문 3.2.1절`) |
| **Verifiability**: 생성 결과를 사람이 아니라 도구가 먼저 검사한다 | 한국어 린터 16개 규칙, 헤드리스 브라우저 기반 레이아웃 검사. 둘 다 CI에서 종료 코드로 판정 가능 |
| **Pedagogical grounding**: 형식은 임의로 정하지 않고 검증된 교육 매체에서 가져온다 | 국내 표준 학습서(EBS 수능특강 등)의 지면 구조, 실제 학습서 192쪽에서 측정한 문장 종결 분포 |

LLM이 논문을 "요약"하는 단계는 이미 일상이 되었다. 다음 단계는 **요약이 아니라 교육 품질의 산출물을, 검증과 함께, 반복 가능하게** 만드는 것이다. 이 저장소는 그 단계를 한국어 사용자를 대상으로 구현한 레퍼런스다.

<br>

## What it produces

<p align="center">
  <img src="docs/images/page-opener.png" alt="2단원 첫 페이지. 왼쪽 단서 칸에 학습 목표, 오른쪽에 본문, 흐름도, 행렬 크기 그림, 하단에 요약" width="880">
</p>

입력은 arXiv URL 또는 PDF, 출력은 브라우저에서 바로 여는 단일 `index.html`이다.

- **Page model.** 화면 하나가 1페이지다. 코넬식 3분할(단서 · 노트 · 요약)을 쓰고, 1440×900 뷰포트에서 스크롤 없이 들어가는지 측정한다 (허용 높이 765px).
- **Structure mirrors the paper.** 모듈 순서와 제목은 논문 목차를 따르고, 번호는 `1, 2, 3 …` 연속 정수로 매긴다. 논문 절 위치는 화면 제목 끝의 `.paper-ref` 태그로 표시한다. 논문에 없는 선수 지식은 별도 모듈로 분리한다.
- **Keyboard paging.** ←→↑↓/PageUp/PageDown/Home/End는 쪽 이동, 스페이스바는 현재 쪽의 주 버튼(다음 단계 진행, 확인 문제는 선택 없이 정답·해설 공개), Shift+스페이스바는 이전 단계이다. 우하단 `‹ n / N ›` 표시로 현재 쪽을 보여 준다. 쪽은 표지, 모듈 첫 페이지, 각 화면 단위이다.
- **Illustrations.** 개념마다 SVG 코드로 그린 도식을 두고, 따로 사물·장면 선화 삽화를 강의마다 3개 이상 넣는다. 삽화는 작은 로컬 모델(SANA-Sprint 0.6B)로 만든 단순한 사물에 화살표·라벨을 SVG로 덧그려, 그림만 보고도 개념의 흐름이 읽히게 한다. `check-pages.py`가 개수를 검사한다.
- **색상 규약.** 색의 역할은 [`references/design-system.md#색상-규약`](references/design-system.md#색상-규약)을 따른다.
- **A figure for every concept.** 새로 도입하는 개념·알고리즘·수식마다 본문 수치와 일치하는 코드 그림을 둔다.
- **Assessment built in.** 개념 체크, 5지선다, `<보기>`형 [3점] 문항을 즉시 채점하고, 해설에는 정답 근거와 대표 오답의 분석을 함께 둔다.
- **Interactive evidence.** 단계별 수식 유도(KaTeX), 의사코드 라인 해설, 지표 전환이 되는 결과 비교, 제거 실험 토글, 연구 계보 트리 등 20종의 요소.

| 확인 문제 | 탐구 자료 |
|:--:|:--:|
| <img src="docs/images/page-quiz.png" alt="번호 블록, 보기 상자, 3점 표시가 있는 확인 문제" width="430"> | <img src="docs/images/page-results.png" alt="지표를 전환할 수 있는 BLEU 결과 비교" width="430"> |

<br>

## Quick start

```bash
git clone https://github.com/genelyuu/paper-to-course.git ~/.claude/skills/paper-to-course
```

Claude Code 세션에서:

```text
https://arxiv.org/abs/1706.03762 강의로 만들어 줘
```

생성된 디렉터리의 `index.html`을 열면 된다. 런타임 의존성은 없다 (KaTeX, 웹 폰트만 CDN).

<br>

## Pipeline

```text
paper (PDF / arXiv)
  │
  ├─ 1. Read          원문 3회 정독, 수식 · 결과표 · 데이터셋 추출
  ├─ 2. Ground        웹 검색으로 선수 개념과 선행 연구 보강
  ├─ 3. Plan          논문 절 → 모듈 매핑, 강의별 용어표로 번역어 고정
  ├─ 4. Generate      모듈별 HTML 작성 (모듈 수가 많으면 하위 에이전트 병렬 생성)
  │                   build.sh → 단일 index.html
  └─ 5. Verify        lint-ko.py --strict  +  check-pages.py   → exit 0 이어야 완료
```

병렬 생성에서 생기는 용어 불일치는 3단계의 용어표(`briefs/terms.md`)와 243개 항목의 기본 용어 사전(`references/glossary-ko.md`)으로 막는다.

<br>

## Verification

생성물은 사람이 읽기 전에 두 도구를 통과해야 한다. 둘 다 표준 라이브러리(+ Chrome)만 쓰고, 실패 시 종료 코드 1을 반환한다.

```bash
python3 references/lint-ko.py <course-dir> --strict
python3 references/check-pages.py <course-dir>
```

**`lint-ko.py`**: HTML 파서 기반 한국어 린터. 코드, 수식, 인용된 대화 블록은 검사 범위에서 제외한다.

| 등급 | 규칙 | 검출 대상 |
|---|---|---|
| ERROR | KO001–KO004 | `lang` 누락, 한자 · 중국어 잔존, 전각 문장부호, 깨진 `data-steps` JSON |
| WARN | KO101–KO112 | 문체 혼용, 번역투, 영문 · 숫자 뒤 조사 불일치, 숫자 · 단위 띄어쓰기, 과도한 문단 길이, 칭찬형 해설, 정답 표지 중복, 서술문형 용어 정의, 똑바른 글꼴 수식 |

**`check-pages.py`**: 헤드리스 Chrome으로 렌더링한 뒤 페이지별 실제 높이를 잰다. 퀴즈 해설을 **모두 펼친 최악 상태**를 기준으로 하므로, 사용자가 답을 확인한 뒤에야 넘치는 경우도 잡는다.

```text
기준: 1440×900, 페이지 허용 높이 765px
OK   module-1 p1 [코넬] 736px  스케일드 내적 어텐션 논문 3.2.1절
...
요약: 페이지 21개, 넘침 0개, 코넬 아닌 화면 0개, 그림 정렬 문제 0개
```

<br>

## Language model: data-derived style rules

학습서 문체를 "느낌"으로 정의하지 않았다. 공개된 국내 학습서 PDF 3권(192쪽)에서 텍스트를 추출해 문장 종결 유형을 집계했고, **글의 역할마다 종결이 다르게 분포한다**는 결과를 규칙으로 옮겼다.

| 역할 | 관측 빈도 | 적용 규칙 | 예 |
|---|--:|---|---|
| 개념 설명 | 한다체 379 | 한다체 평서 | 어텐션은 쿼리와 키의 내적으로 비중을 정한다. |
| 문항 지시 | `~하시오` 120 | `~하시오` | 버튼을 눌러 다음 단계를 보시오. |
| 풀이 전략 | `~하라` 51 | 모듈당 1줄 | 나누는 값을 묻는 문항은 분산이 아니라 그 제곱근인지 확인하라. |
| 용어 정의 | 명사형 34 | 사전식 명사형 (KO111) | 소프트맥스(softmax): 실수 여러 개를 모두 양수이고 합이 1인 값으로 바꾸는 함수. |
| 머리말 · 사용법 | 합니다체 137, 해요체 50 | 미적용 | — |

<sub>정규식 기반 집계로 오차가 있으며 경향 파악 용도다.</sub>

레이아웃 역시 같은 방식으로 정했다. 4px 격자는 Carbon · Atlassian · USWDS의 간격 체계를, 지면 구성과 교과 색 프리셋은 수능특강의 단원 도입 · 날개 · 문항 형식을 조사해 반영했다 (§8).

<br>

## Differences from upstream

[ZeroxZhang/paper-to-course](https://github.com/ZeroxZhang/paper-to-course)는 중국어 강의를 생성한다. 이 포크는 출력 언어 교체에 그치지 않고 생성 규칙, 지면 모델, 검증 계층을 추가했다.

| | Upstream | This fork |
|---|---|---|
| Output language | zh-CN | ko-KR |
| Structure | 교수법 기준 임의 모듈 | 논문 목차 순서 + 연속 번호, 절 위치는 `.paper-ref` (traceable) |
| Style rules | 없음 | 역할별 종결 규칙, 번역투 · 조사 규칙 |
| Layout | 연속 스크롤, 카드 + 그림자 | 고정 높이 코넬식 페이지, 4px 격자 |
| Assessment | 기본 퀴즈 | 5지선다 · `<보기>`형 · 배점, 오답 분석 해설 |
| Terminology | 없음 | 기본 사전 243개 + 강의별 용어표 |
| Verification | 없음 | 린터 16개 규칙 + 레이아웃 검사 (exit code) |
| Bugs fixed | — | 초기화 순서 오류로 전체 인터랙션이 멈추던 문제, 해설 내 수식 미렌더링, 비백분율 지표의 `%` 표기 |

<br>

## Repository layout

```text
SKILL.md                     스킬 정의: 파이프라인, 문체 규칙, 목차 규칙
references/
  korean-style-guide.md      문체 · 조사 · 띄어쓰기 · 번역투 규칙과 린터 대응표
  glossary-ko.md             AI/ML 용어 번역 사전 (243 entries)
  interactive-elements.md    인터랙티브 요소 20종 HTML 패턴
  lint-ko.py                 한국어 린터
  check-pages.py             페이지 레이아웃 검사
  content-philosophy.md      콘텐츠 원칙
  design-system.md           디자인 토큰, 색상 규약
  gotchas.md                 생성 시 자주 나는 문제
  module-brief-template.md   모듈 브리프 양식
  _base.html, _footer.html   생성물 골격 템플릿
  build.sh                   모듈을 index.html로 조립
  illustration.md            삽화 규칙 (도식은 SVG 코드, 사물·장면 선화는 작은 로컬 모델, 강의당 3개 이상)
  illustrate.py              로컬 모델 → 선화 SVG 파이프라인 (선택, 별도 가상환경)
  styles.css, main.js        생성물에 복사되는 런타임
examples/attention-ko/       레퍼런스 출력
docs/
  images/                    README 스크린샷
  lint-fixtures/             린터 검증용 good/bad 예시
```

<br>

## Limitations

- 문체 집계 표본은 한 출판사의 학습서 3권이다. 다른 교육 회사 교재의 본문은 공개 원문을 확보하지 못해 포함하지 않았다.
- 레이아웃 검사는 데스크톱 1440×900 기준이다. 1200px 미만에서는 1단으로 전환되며 페이지 단위 보장을 하지 않는다.
- 생성 품질은 원문 해석에 의존한다. 린터와 레이아웃 검사는 형식을 보장하지만 내용의 정확성은 보장하지 않는다.

<br>

---

<div align="center">
<sub>
Upstream <a href="https://github.com/ZeroxZhang/paper-to-course">ZeroxZhang/paper-to-course</a> (now <a href="https://github.com/ZeroxZhang/zerox-skills/tree/main/zerox-paper-to-course">zerox-skills</a>) ·
Inspired by <a href="https://github.com/zarazhangrui/codebase-to-course">codebase-to-course</a> ·
<a href="LICENSE">Apache License 2.0</a>
</sub>
</div>
