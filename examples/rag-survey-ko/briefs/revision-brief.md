# 개정 공통 브리프 (실무자 의견 7건 반영, 2026-11)

이 강의(`examples/rag-survey-ko`)는 Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey"(arXiv 2312.10997)를 한국어 인터랙티브 강의로 만든 것이다. 도메인 실무자 의견을 반영해 6단원을 8단원으로 개정한다. 너는 이 중 일부 파일만 맡는다.

## 실무자 의견 (전부 반영 대상)
1. "닫힌 책/열린 책" 표현 대신 closed-book/open-book(원어 우선)
2. dense retriever의 단점 예시 부족
3. Advanced RAG·Modular RAG의 단점 부족
4. in-context learning(ICL) 소개 부족
5. Recall, F1 등 지표 설명 부족
6. top-down 구성 + 서베이 이후 동향(GraphRAG, PRAG, Agentic RAG 등)
7. 처음 배우는 사람에게 어렵다. **설명을 줄이지 말고** 그림·그래프·구체 예시로 보강한다. 전문 용어는 반드시 툴팁과 쉬운 풀이를 단다.

## 새 단원 구성 (파일 → 단원 번호 → 내부 id)
| 파일 | 화면 번호 | id | 제목 |
|---|---|---|---|
| modules/00-bigpicture.html | 1 | module-0 | 훑어보기 |
| modules/01-background.html | 2 | module-1 | 서론과 배경 |
| modules/02-overview.html | 3 | module-2 | RAG 개요 |
| modules/03-retrieval.html | 4 | module-3 | 검색 |
| modules/04-generation.html | 5 | module-4 | 생성과 증강 |
| modules/05-evaluation.html | 6 | module-5 | 과제와 평가 |
| modules/06-discussion.html | 7 | module-6 | 논의와 향후 전망 |
| modules/07-trends.html | 8 | module-7 | 서베이 이후 동향 |

본문에서 다른 단원을 가리킬 때는 화면 번호("4단원")를 쓴다. `_base.html`, `_cover.html`, 모듈 id, module-number는 이미 고쳐 두었다. 건드리지 않는다.

## 반드시 먼저 읽을 것 (저장소 루트 = /Users/eugene/dev/paper2contents)
- `SKILL.md`: 특히 "용어 표기", Phase 3의 EBS 교재 구성(학습 목표·개념 체크·탐구 자료·핵심 정리·확인 문제), Phase 4의 작성 규칙, "코넬식 페이지" 규칙
- `references/korean-style-guide.md`: 문체(한다체·EBS 교재 문체), 린터 규칙
- `references/interactive-elements.md`: 마크업 양식(퀴즈, 어블레이션 토글, 수식 단계 풀이, 연구 계보, 데이터 표, 콜아웃 등). **여기 있는 클래스와 마크업만 쓴다.** CSS·JS는 새로 만들지 않는다.
- `references/design-system.md`: 색상 규약(먹색 + 교과 색 하나), 그림 정렬 규칙
- `references/illustration.md`: 도식은 인라인 SVG로 직접 쓴다
- `references/content-philosophy.md`, `references/gotchas.md`
- 이 강의의 `briefs/terms.md`(용어 표기 고정, 반드시 따름)와 `briefs/research.md`(확인된 출처. **수치·주장은 여기 있는 것만 쓴다.** 없는 수치는 만들지 말고 "예시"라고 밝힌 자체 예시 값만 쓴다)
- 기존 모듈 파일에서 같은 종류의 쪽이 어떻게 쓰였는지 보고 그대로 따라 한다(코넬 쪽, SVG 클래스, 퀴즈 마크업).

## 형식 제약
- 한 화면 = `.screen.cornell` 1장. 1440×900에서 쪽 높이 765px 이하여야 한다(넘치면 쪽을 나눈다).
- 단원마다 본문 쪽 3~8개(확인 문제 쪽 제외), 확인 문제 3~5문항, 문제 쪽당 최대 2문항. 그중 하나 이상은 부정형(`옳지 않은 것은?`) 또는 `<보기>`형.
- 단원 첫 쪽은 `.module-header` 다음 쪽이며, 단서 칸(cue)에 `학습 목표` 2~3개(`~을 설명할 수 있다.`).
- 화면 제목 끝 논문 위치 태그 `<span class="paper-ref">논문 N절</span>`은 논문 내용일 때만. 논문 밖 보충(배경, 이후 동향)에는 달지 않고, 필요하면 "보충" 성격을 콜아웃으로 밝힌다.
- 용어: 첫 등장에 `term` 툴팁(`data-definition`은 사전식 명사형 종결, 예: `…하는 것.`, `…함.`)과 terms.md의 첫 등장 표기. 이후 표기 통일.
- id는 강의 전체에서 유일해야 한다. 새 id·SVG marker id·퀴즈 id·토글 id에는 파일 접두사를 붙인다: 00→`bp-`, 01→`bg-`, 02→`ov-`, 03→`rt-`, 04→`gn-`, 05→`ev-`, 06→`ds-`, 07→`tr-`.
- 출처는 그림 캡션이나 본문에 `<a href="…" target="_blank" rel="noopener">`로 단다(하이퍼링크는 허용). `<img>`·`<script>`·`<link>`로 외부 자원을 불러오지 않는다(빌드가 실패한다).
- 색: 먹색과 교과 색(`accent` 클래스)만. 다른 유채색 금지.
- 기존 설명을 삭제·축약하지 않는다(맡은 작업에서 명시한 교체 제외).
- 맡은 파일 외에는 수정하지 않는다. git commit 하지 않는다.

## 검증 (맡은 파일을 다 쓴 뒤 반드시 실행, 저장소 루트에서)
```bash
bash examples/rag-survey-ko/build.sh
python3 references/lint-ko.py --strict examples/rag-survey-ko/modules/<맡은 파일>
python3 references/check-pages.py examples/rag-survey-ko
```
- 린터: 맡은 파일 ERROR 0, WARN 0.
- check-pages: 맡은 단원 쪽(`module-N p…`)에 넘침(FAIL)·그림 정렬 문제가 없어야 한다. 다른 에이전트가 동시에 다른 파일을 고치고 있으므로 다른 단원의 문제나 일시적 빌드 실패는 무시하고 다시 실행한다.
- 마지막 보고: 추가·변경한 쪽 제목 목록, 문항 수, 사용한 출처, 남은 문제.
