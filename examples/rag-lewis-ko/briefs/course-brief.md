# 강의 공통 브리프: RAG (Lewis et al. 2020)

이 강의(`examples/rag-lewis-ko`)는 Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"(arXiv 2005.11401, NeurIPS 2020)를 한국어 인터랙티브 강의로 만든다. 모듈 7개이며, 하위 에이전트 3개가 병렬로 작성한다. 너는 이 중 일부 파일만 맡는다.

## 사용자 요구 (이 세션에서 확정된 선호)
1. **삽화와 도표를 충분히 넣는다.** 본문 쪽(확인 문제 쪽 제외)마다 개념 도식(인라인 SVG), 데이터 표, 그래프 중 하나 이상을 둔다. 도표 규칙은 `briefs/diagram-guide.md`를 따른다(GitHub 도표 skill에서 가져온 규칙 포함).
2. **이전 연구의 한계와 RAG가 나온 배경**을 충분히 설명한다(2단원).
3. **이후 동향** 단원을 둔다(7단원).
4. **설명을 줄이지 말고** 그림, 표, 구체 예시로 보강한다. 처음 배우는 사람도 따라올 수 있어야 한다. 전문 용어에는 반드시 툴팁과 쉬운 풀이를 단다.
5. **baseline은 "기준선"**으로 쓴다. "기준 방법"이나 "기준 모델"로 바꾸지 않는다.
6. 처음 나오는 평가 지표(EM, BLEU-1, ROUGE-L, Q-BLEU-1, 레이블 정확도)는 작은 수치 예로 직접 계산해 보인다.
7. 방법마다 대가와 실패 사례를 함께 쓴다. 예: Thorough Decoding의 비용, 문서 인코더를 고정한 대가, retrieval collapse, BM25가 이긴 FEVER, null document.

## 단원 구성 (파일 → 화면 번호 → 내부 id → id 접두사 → 담당)
| 파일 | 화면 번호 | id | 제목 | 논문 위치 | id 접두사 | 담당 |
|---|---|---|---|---|---|---|
| modules/00-background.html | 1 | module-0 | 서론과 배경 | 1절 + 선수 개념 | `bg-` | A |
| modules/01-prior.html | 2 | module-1 | 이전 연구와 한계 | 1, 5절 + 보충 | `pr-` | A |
| modules/02-model.html | 3 | module-2 | RAG 모델 | 2, 2.1절 | `md-` | B |
| modules/03-components.html | 4 | module-3 | 검색기, 생성기, 학습 | 2.2~2.5절 | `cp-` | B |
| modules/04-setup.html | 5 | module-4 | 실험 설계 | 3절 | `st-` | C |
| modules/05-results.html | 6 | module-5 | 결과 | 4절, 부록 | `rs-` | C |
| modules/06-trends.html | 7 | module-6 | 이후 동향 | 논문 밖 보충 | `tr-` | C |

`_base.html`과 `_cover.html`은 메인 에이전트가 이미 썼다. 건드리지 않는다. 다른 단원을 가리킬 때는 화면 번호(예: "4단원")를 쓴다. 모듈 파일은 `<section class="module" id="module-N">` 블록만 담는다. 골격은 `examples/attention-ko/modules/*.html`을 그대로 따른다.

## 담당별 내용
### A: 00-background, 01-prior
- **00 서론과 배경**
  - 첫 쪽(논문 1절, paper-ref "논문 1절", `배경 지식` 콜아웃 없음): 쓴 이유(파라미터에만 든 지식의 세 한계: 갱신 불가, 근거 불명, 환각) + **이전 방식 대 제안 방식 비교 그림**(closed-book seq2seq vs RAG: 질문 → 검색 → 문서 + 질문 → 생성) + 새로운 점 3개 이내.
  - 나머지 쪽은 배경 쪽이다. 각 쪽 맨 위에 `배경 지식` 콜아웃을 둔다. 다룰 선수 개념은 4개다.
    - ① parametric memory와 non-parametric memory: 비유는 외운 지식과 책장. 삽화 `fig-shelf`를 쓴다.
    - ② seq2seq와 BART: 입력 문장 → 출력 문장, 인코더와 디코더. 토큰을 하나씩 생성한다.
    - ③ dense retrieval: 문장을 임베딩 벡터로 바꾸고 내적으로 점수를 매긴다. 작은 2차원 예시로 계산하고 top-$k$와 MIPS로 잇는다.
    - ④ 확률의 주변화와 잠재 변수: "어느 문서를 봤는지 모르니 문서별 확률을 가중합한다." 예시 숫자로 계산한다.
  - 지식 지도 SVG(개념 관계)를 넣고, 확인 문제 3~5문항을 둔다.
- **01 이전 연구와 한계**
  - 줄거리는 세 단계다.
    - ① closed-book: LAMA, T5 closed-book. 파라미터에 지식이 들어 있지만 갱신할 수 없고 근거를 보이지 못하며 환각을 낸다. 모델 크기를 키워야 한다. 근거는 T5-11B 110억 파라미터의 NQ 34.5와 RAG 626M의 44.5(부록 G, 표 1)이다.
    - ② retrieve-and-extract: DrQA, ORQA, REALM, DPR. 답을 문서에서 **추출**만 하므로 생성 과제(요약형 답, 질문 생성)에 쓸 수 없다. 문서에 답이 그대로 없으면 0%이다. REALM은 사전학습 중 색인을 갱신하는 데 비용이 크고 salient span masking이 필요하다.
    - ③ memory network와 retrieve-and-edit: 과제마다 처음부터 학습하고, 기억이 텍스트가 아니어서 사람이 읽거나 고칠 수 없다.
  - 그다음 "그래서 RAG는 무엇을 합쳤나"를 쓴다. 사전학습 retriever와 사전학습 generator를 확률 모델 하나로 묶어 end-to-end로 학습하는 구조이다.
  - 연구 계보 트리(`.lineage-note`, `.novelty`)와 `기준 × 접근` 비교표를 넣는다. 비교 기준은 지식 갱신, 근거 제시, 생성 가능, 사전학습 필요다. 표 아래에 핵심 비교를 쓴다.
  - 삽화 `fig-openbook`을 쓴다(closed-book vs open-book).

### B: 02-model, 03-components
- **02 RAG 모델**
  - 전체 구조도(논문 그림 1을 SVG로 다시 그림): query encoder → MIPS → 문서 색인 top-K → generator → 주변화. 오프라인 구획(문서 인코딩, 색인 구축)과 온라인 구획(질의 처리)을 나누고, end-to-end 역전파 범위($q$와 $p_\theta$만)를 표시한다. 이 구조도를 이후 쪽(02, 03)에서 축소해 "지금 보는 부분"을 교과 색으로 표시한다.
  - **따라가기 예시**: 질문 하나가 구조도를 통과하며 단계별로 바뀌는 값을 보인다. 예: "Define middle ear" 또는 Jeopardy "The Divine Comedy". 문서 점수와 확률은 예시 값임을 밝힌다.
  - RAG-Sequence와 RAG-Token 식을 **수식 유도 단계별 풀이**로 보인다. `\tag{1}`, `\tag{2}`는 논문에 번호가 없으므로 달지 않는다.
  - **같은 입력에 대한 두 방식 비교 그림**: 문서 2개, 토큰 3개의 예시 숫자로 두 확률을 직접 계산한다.
  - `기준 × 방식` 비교표(문서 선택 단위, 여러 문서 조합, 디코딩, 잘 맞는 과제, 비용)와 핵심 비교를 넣는다. 분류에서는 두 방식이 같다는 점도 쓴다.
  - 그림 2(Hemingway 예)는 6단원에서 다룬다는 앞참조만 둔다.
- **03 검색기, 생성기, 학습**
  - DPR bi-encoder(식, BERT-base 둘, 내적, softmax), MIPS/FAISS/HNSW(근사 최근접, 준선형), 색인 규모(2,100만 문서, 100단어 청크, CPU 메모리 약 100 GB → 압축 36 GB)를 다룬다. 삽화 `fig-magnifier`를 쓴다.
  - BART generator: 입력과 문서를 이어 붙이는 그림, 400M. 삽화 `fig-pen`을 쓴다.
  - 학습: 손실(음의 주변 로그 가능도), 무엇을 학습하고 무엇을 고정하나. 그림에서 학습 대상은 교과 색, 고정 대상은 회색으로 그린다. 문서 인코더를 고정하는 이유와 대가(REALM과 비교), 학습 파라미터 626M 내역(110M + 406M + 고정 110M)을 다룬다.
  - 디코딩:
    - RAG-Token은 일반 beam이다.
    - RAG-Sequence는 Thorough Decoding과 Fast Decoding이다. **의사코드 단계별 풀이**(줄별 설명)를 쓰고, 추가 forward pass 비용을 예시 값으로 계산한다.
    - 부록 A의 실제 설정(QA는 greedy, RAG-Seq는 50개 문서 + Thorough, 생성 과제는 beam 4 + Fast)을 표로 정리한다.

### C: 04-setup, 05-results, 06-trends
- **04 실험 설계**
  - 공통 설정: 위키 2018년 12월, 21M 문서, $k\in\{5,10\}$.
  - 과제 네 갈래와 입력·출력 예시 표: 오픈 도메인 QA / MS MARCO / Jeopardy / FEVER. 표 7 데이터 수를 쓴다.
  - 지표마다 작은 수치 예로 계산한다: EM, BLEU-1, ROUGE-L, Q-BLEU-1, 레이블 정확도.
  - 비교 대상: closed-book(T5), open-book(REALM, DPR), BART 기준선, gold 문맥을 쓴 SotA.
  - 삽화 `fig-buzzer`(Jeopardy)와 `fig-gavel`(FEVER)을 쓴다.
- **05 결과**
  - **결과 비교 인터랙티브**: 표 1, 표 2. 지표나 과제를 전환하는 기존 마크업을 쓴다.
  - 사람 평가(표 4), 다양성(표 5), 그림 2 Hemingway 문서 사후 확률. 그림 2는 토큰 × 문서 격자로 정성적 경향만 그리고, 예시 칸 값임을 밝힌다.
  - 제거 실험(표 6): BM25/Frozen/학습. 어블레이션 토글을 쓰고, FEVER에서 BM25가 이긴 이유를 해석한다.
  - index hot-swapping: 70/68/12/4% 2×2 격자.
  - 검색 문서 수의 영향(경향만), 부록 G 파라미터 비교(T5-large 28.9 대 RAG 44.5).
  - 한계: retrieval collapse, null document, 위키 편향, DPR 초기화가 NQ·TQA 감독을 썼다는 점.
- **06 이후 동향**
  - 논문 밖 보충이므로 paper-ref를 달지 않는다. 첫 쪽 콜아웃에 "논문 이후의 보충, 조사 시점 2026년 11월"을 밝힌다.
  - `briefs/research.md` 후보(FiD, RETRO, Atlas, REPLUG, In-Context RALM, Self-RAG, 서베이)를 **WebFetch로 각 arXiv 초록을 확인한 뒤** research.md에 확인된 주장과 함께 추가하고 쓴다.
  - 정리 틀은 "무엇을 풀려는가 → 핵심 아이디어 그림 → 한계·비용 → RAG(2020)의 어느 칸에서 나왔나"다.
  - 마지막에 같은 저장소의 RAG 서베이 강의로 이어진다는 안내와 더 읽을거리(HuggingFace RAG 문서 등)를 둔다.

## 반드시 먼저 읽을 것 (저장소 루트 = /Users/eugene/dev/paper2contents)
- `SKILL.md`(이 강의를 만드는 스킬의 원본. 특히 "용어 표기", "작성 규칙 (필수, 모든 모듈에 적용)", Phase 3의 학습서 구성, 순차 경로의 코넬 페이지 규칙)
- `references/korean-style-guide.md` 전체
- `references/interactive-elements.md`: **여기 있는 클래스와 마크업만 쓴다.** CSS와 JS는 새로 만들지 않는다.
- `references/design-system.md`(색상 규약, 그림 정렬 규칙), `references/illustration.md`, `references/content-philosophy.md`, `references/gotchas.md`
- 이 강의의 `briefs/terms.md`(반드시 따른다), `briefs/research.md`(**수치와 주장은 여기 있는 것만 쓴다**), `briefs/diagram-guide.md`(도표 규칙과 삽화 배치)
- 형식 참고: `examples/attention-ko/modules/`(최근 개정판. 코넬 쪽, SVG 클래스, 퀴즈, 토글, 수식 단계 풀이, 의사코드, 연구 계보의 실제 마크업)

## 형식 제약
- **쪽 구성**
  - 한 화면 = `.screen.cornell` 1장. 1440×900에서 쪽 높이 765px 이하.
  - 단원마다 본문 쪽 3~8개(확인 문제 쪽 제외). 확인 문제는 3~5문항, 문제 쪽당 최대 2문항이고, 하나 이상은 부정형이나 `<보기>`형이다.
  - 단원 첫 쪽의 cue에 `학습 목표` 2~3개를 둔다. 도입 문장은 `이 모듈을 학습하면 다음을 할 수 있다.`이다.
- **용어와 표기**
  - `paper-ref`는 논문 내용일 때만 단다.
  - 용어는 첫 등장에 `term` 툴팁(명사형 종결)과 terms.md의 첫 등장 표기를 쓴다. 모듈마다 다시 병기한다.
  - 수식은 모두 이탤릭이다(`\mathit`, KO112 0건). 그림 속 수학 기호도 이탤릭이다.
- **id와 링크**
  - id는 강의 전체에서 유일해야 한다. 새 id, marker id, 퀴즈 id, 토글 id에 위 표의 접두사를 붙인다.
  - 출처는 `<a href target="_blank" rel="noopener">`로 단다. 외부 `<img>`, `<script>`, `<link>`는 금지한다.
- **도식**
  - 색은 먹색과 교과 색만 쓴다. 간선은 직각이다.
  - 노드 라벨은 `foreignObject > div.node-label > span`이다. CSS가 `.svg-diagram` 밖에서도 가운데로 정렬하므로 inline 정렬 스타일은 넣지 않는다.
- **작업 범위**
  - 맡은 파일 외에는 수정하지 않는다. C는 research.md에 추가하는 것만 예외다. terms.md에 없는 용어가 필요하면 보고에 적는다.
  - git commit 하지 않는다.

## 검증 (반드시, 저장소 루트에서)
```bash
bash examples/rag-lewis-ko/build.sh
python3 references/lint-ko.py --strict examples/rag-lewis-ko/modules/<맡은 파일>   # 파일마다, ERROR 0, WARN 0
python3 references/check-pages.py examples/rag-lewis-ko                               # 맡은 단원 넘침 0, 그림 정렬 0
```
- 다른 에이전트가 동시에 빌드한다. 다른 단원의 문제나 모듈 파일이 아직 없어서 생기는 일시적 실패는 무시하고 다시 실행한다. 삽화 3개 미만 경고도 초기에는 무시한다.
- **렌더링 확인**: `/private/tmp/claude-501/-Users-eugene-dev-paper2contents/365a5151-f96b-49fa-bdcf-a9f50729bb5e/scratchpad/shot.py`를 너의 작업 폴더에 복사한다. 복사본에서 임시 파일 이름 `__shot.html`을 `__shot_<담당>_<module>.html`로 바꿔 충돌을 피한다. `cd / && ~/.cache/paper-to-course/venv/bin/python -P <복사본> /Users/eugene/dev/paper2contents/examples/rag-lewis-ko module-N <출력폴더>`로 맡은 단원의 모든 쪽을 PNG로 만들고 Read로 직접 본다. 잘림, 겹침, 작은 글자, 정렬, 수식 오류를 고친다.
- 마지막 보고(한국어, 짧게): 쪽 제목 목록, 문항 수, 도식·표·삽화 수, 사용 출처, terms.md에 추가가 필요한 용어, 남은 문제.
