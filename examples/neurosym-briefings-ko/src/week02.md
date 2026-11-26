## 신경·기호 AI 주간 연구·교육 브리핑

### 1. 조사 범위

- 기준일: **2026년 10월 2일**
- 주요 검색 기간: **2026년 9월 25일~10월 1일**
- 검색원: arXiv, 저자가 연결한 GitHub·데이터 저장소, 검색으로 확인 가능한 학회 채택 정보
- 검색식 계열: `neuro-symbolic`, `ontology learning`, `ontology reasoning`, `knowledge graph reasoning`, `multi-agent trust`, `multi-agent verification`, `agent evaluator`
- 포함 기준: 새로운 방법·벤치마크·실증 결과 또는 재현 가능한 평가 설계를 제시한 연구
- 제외 기준: 단순 제품 홍보, 온톨로지·신뢰와 명목상으로만 관련된 연구, 원문 존재를 확인하지 못한 요약 페이지
- 주의: 출판 데이터베이스 전체를 대상으로 한 체계적 문헌고찰은 아니다. 성능 수치는 별도로 재현한 결과가 아니라 **저자 보고값**이다.

이번 주에는 직접 관련성이 높은 자료 **5건**, 인접 연구 **3건**, 전주 누락 보완 **1건**을 확인했다.

---

## 2. 전체 목록

| 우선도 | 자료 | 방법·평가·결과 | 핵심 한계 | 사용자 연구 연결 |
|---|---|---|---|---|
| **A** | **APOLO: Automatic Prompt Optimization for Ontology Learning** — Mai 외, 9월 28일, ISWC 2026 Posters & Demos 채택 | 12개 공개 온톨로지에서 다중 에이전트가 텍스트–OWL 쌍을 생성하고, Greedy·Autoregressive 학습기의 프롬프트를 GEPA로 최적화한다. DOID·Plant Ontology를 보류 평가에 사용했다. Qwen3.5-27B AR의 DOID axiom precision은 **0.569→0.838**로 증가했다. 엔터티와 공리의 precision/recall을 분리하고, 공리 평가는 reasoner 기반 함의를 사용한다. | 결과가 단일 실행이며, 기반 온톨로지가 LLM 사전학습에 포함됐을 가능성이 있다. 중복 공리를 별도로 벌점화하지 않아 과잉 생성이 유리할 수 있다. PO의 최적화 후 AxP는 0.174로 여전히 낮다. | 사용자의 `문장→논리 표현→트리플`을 **엔터티 추출·공리 생성·일관성 검사**로 분리하고, 정확 문자열 일치 대신 reasoner 기반 entailment 평가를 추가할 수 있다. |
| **A** | **Ontology-Mediated Neurosymbolic Constraint Acquisition from Multiple Stakeholders** — Bischof 외, 9월 24일 공개·이번 주 검색 보완, KG-NeSy@ISWC 2026 채택 | LLM이 수집한 선호와 하드웨어의 물리 제약을 OWL 구성 온톨로지로 통합하고, description logic으로 불만족성을 발견한다. 충돌 설명을 이용해 사용자와 제약을 재협상하며, 남은 충돌은 우선순위 기반 완화로 처리한다. 사례는 FLEXI 마이크로그리드다. | 정량 비교실험이나 대규모 사용자 평가는 제시되지 않은 사례 중심 구조다. 일반화는 저자 주장 단계다. | 멀티에이전트가 생성한 트리플의 권한을 동일하게 보지 않고 `hard_constraint`, `soft_preference`, `source`, `priority`를 부여하는 설계에 직접 적용할 수 있다. |
| **A** | **Safety of Latent Communication in Multi-Agent Systems** — Huzaifa 외, 9월 30일, 프리프린트 | 에이전트 간 텍스트 대신 내부 표현을 전달하는 trainable link를 분석한다. 3개 통신 토폴로지·4개 안전 벤치마크에서 RL 공격 후 평균 harmful-compliance가 **27.9→76.9**로 증가했다. 에이전트 본체를 변경하지 않고 링크만 안전 방향으로 보정하는 복구 실험도 수행했다. | 공개 코드 연결을 확인하지 못했다. 초록만으로 모델·표본별 분산과 외부 모델 일반화 정도를 확정하기 어렵다. | 신뢰를 에이전트 개별 성능이 아니라 **에이전트+메시지 변환기+토폴로지**의 시스템 속성으로 평가해야 한다. 트리플 직렬화·요약·임베딩 전달 과정의 의미 변형 실험과 연결된다. |
| **B** | **PADMÉ: Preference Alignment Data Synthesis for Meta-Evaluation of LM Agent Evaluators** — Chang 외, 9월 28일, NeurIPS 2026 Trust-AI-Eval 워크숍 채택 | 4개 에이전트 도메인·3개 평가 기준에서 **1,000개** 선호 비교 자료를 합성했다. 150개 인간 검증 부분집합에서 판단 일치율이 naive baseline **73%→85%**로 증가했고, 25개 모델 평가에 사용했다. 코드와 데이터가 공개돼 있다. | 인간 검증이 전체 1,000개 중 150개이며, 합성 데이터의 편향을 제거한 것은 아니다. 사람 없이 평가자료를 생성한다는 점과 인간 판단을 대체할 수 있다는 주장은 구분해야 한다. | 트리플 생성 모델의 LLM 평가자를 그대로 신뢰하지 말고, 전문가가 선호한 두 출력 중 어느 것을 평가자가 선택하는지 **meta-evaluation**하는 방법으로 활용 가능하다. |
| **B** | **Neuro-Symbolic Computer Use: Learning Reusable Policies for Reliable and Efficient Execution** — Suh 외, 9월 29일, 프리프린트 | 반복 작업의 순서·반복·분기는 코드로 고정하고, 화면 grounding과 상태 판단만 신경모델에 맡긴다. OSWorld-Verified와 ScienceBoard에서 base agent 대비 Pass³가 **3.6~15.8%p** 높고, 실행당 비용은 **15~217배**, 지연은 **3.4~5.1배** 감소했다고 보고한다. | 오류 판정기가 셸 반환값을 보지 못하고, 실행불가능한 작업을 인식하지 못하며, 늦게 나타난 증상을 최초 오류로 잘못 지정할 수 있다. 이 분석은 19개 실패 작업 중 일부를 제외한 표본에 기반한다. | 온톨로지 추출에서 변하지 않는 절차는 코드·검증 규칙으로 고정하고, 문장 의미 해석만 Transformer에 맡기는 **좁은 신경–기호 경계** 설계에 참고할 수 있다. |
| **B** | **The Crowd in the Machine** — Simon, 9월 25일, 프리프린트 | 2026년 두 자율 에이전트 집단 사건을 crisis informatics 관점에서 비교한다. 조정 품질, 집단 신념의 정확성, 행동의 권한 준수를 서로 다른 평가축으로 분리한다. | 통제실험이 아니라 공개 조사자료와 재구성 기록을 이용한 비교 사례연구다. 원인효과나 발생률을 추정할 수 없다. | 멀티에이전트 평가를 `task_success`, `belief_correctness`, `authorization_compliance`로 분리해야 한다는 개념적 근거로 활용할 수 있다. |
| **C** | **Question-Specific Knowledge Graphs for Efficient Visual Reasoning** — Chen 외, 9월 28일, 9월 30일 개정 | 이미지 전체를 설명문으로 변환하는 대신 질문에 필요한 엔터티–관계만 KG로 생성하도록 RL 학습한다. 과학·수학·일반 시각질문에서 caption 기반 표현보다 토큰을 줄이면서 유사하거나 높은 성능을 보였고, GDPO가 GRPO보다 평균 정확도 **2%p** 높았다고 보고한다. 코드 링크가 제공된다. | OWL 추론이나 온톨로지 일관성을 다루는 연구는 아니다. 질문에 맞춘 정보 선택이 근거 누락을 일으키는지 별도 검증이 필요하다. | 문장 전체를 무조건 트리플화하지 않고, competency question별 **최소 충분 부분 그래프**를 만드는 연구로 확장 가능하다. |
| **C** | **Prototype-Rule Neurosymbolic Regularization…** — Protopapadakis 외, 9월 30일, 프리프린트 | 4개 hyperspectral 데이터셋과 4개 Rank-R 설정을 7-fold·공간 분리 분할로 평가했다. 공간 분할 Macro-F1 변화는 Botswana **+8.82%p**, Indian Pines **+5.49%p**, Pavia **+1.59%p**, Salinas **−0.62%p**였다. | 온톨로지·멀티에이전트 연구가 아니며, 이점 대부분이 학습 정규화에서 발생했다. 데이터셋에 따라 손해도 확인됐다. | 규칙 결합이 항상 성능을 높인다는 가정을 반박하는 비교 사례다. 사용자의 symbolic stage도 `neural-only`, `symbolic-only`, `train-time constraint`, `inference-time reasoning`으로 ablation해야 한다. |
| **C** | **5W1H+Which: Context-Valid Semantic Indexing with Progressive Ontology Binding** — 9월 28일, 프리프린트 | 5W1H 기반 의미 인덱싱과 점진적 온톨로지 결합 구조를 제안한다. | 검색 가능한 원문 정보상 평가는 “계획” 단계이며, 효과를 입증한 완결 실험으로 간주할 수 없다. | 출처·시간·장소·행위자·대상을 트리플 provenance에 구조화하는 아이디어만 참고할 가치가 있다. |

---

## 3. 직접 적용 우선순위 3건

### ① APOLO — 현재 연구에 가장 직접적

**적용 위치**

```text
문장
→ 논리 표현
→ 후보 클래스·개체·공리
→ 파싱 및 일관성 검사
→ 추론기 기반 함의 평가
→ 트리플/OWL 저장
```

현재 exact match 또는 트리플 단위 F1만 사용하고 있다면 다음을 추가할 수 있다.

- Entity precision/recall
- Axiom precision: 생성 공리가 정답 온톨로지에서 함의되는 비율
- Axiom recall: 정답 공리가 생성 온톨로지에서 함의되는 비율
- Parse success rate
- Consistency rate
- Redundant axiom rate
- 원문 인용과 공리 간 evidence alignment

**최소 검증 실험**

- 데이터: 기존 Petrucci 2,000건에서 train/validation/test를 문서 또는 온톨로지 단위로 분리
- 비교군:
  1. 기존 Transformer→논리→트리플
  2. 기존 모델+수동 프롬프트
  3. 기존 모델+자동 최적화 프롬프트
  4. autoregressive ontology context 추가
- 필수 조건: 같은 test set을 프롬프트 최적화 과정에서 반복 조회하지 않는다.
- 권장 통계: 세 개 이상 seed, 문서 단위 bootstrap CI, 도메인별 분리 결과
- 실험상 핵심: APOLO의 평가에서 빠진 **중복 공리율과 과잉 생성률**을 반드시 추가한다.

### ② Ontology-Mediated Constraint Acquisition — 신뢰도 구조 설계

에이전트 출력에 다음 최소 메타데이터를 붙이는 방식이 적합하다.

```text
claim_id
source_agent
source_sentence
formal_axiom
authority = hard | soft
priority
validation_status
conflicts_with
relaxation_history
```

**최소 실험**

- 같은 개념에 대해 상충하는 30~50개 제약 쌍 구성
- 조건:
  - 출처 구분 없음
  - hard/soft 구분만 적용
  - 출처+우선순위+OWL 충돌 검출 적용
- 지표:
  - 미검출 모순 수
  - 잘못 완화한 hard constraint 비율
  - 해결 불가능한 경우의 abstention 정확도
  - 설명에서 실제 충돌 공리를 정확히 지목한 비율

### ③ Safety of Latent Communication — 시스템 수준 신뢰 평가

사용자 연구에서 에이전트 A가 만든 논리 표현을 에이전트 B가 검증한다면, 전달 형식별 성능을 비교할 수 있다.

- 원문 자연어
- 정형 JSON
- 논리식
- 트리플
- 임베딩 또는 압축 표현

각 조건에서 **의미 보존율, 모순 탐지율, 공격 명령 전달률, 최종 트리플 F1**을 함께 측정해야 한다. 개별 에이전트의 정확도가 같아도 통신 변환기가 오류나 공격 성공률을 증가시킬 수 있다는 것이 이번 연구의 핵심 경고다.

---

## 4. 교육공학적 적용안

아래는 논문에서 입증된 교육 효과가 아니라, 논문 결과를 근거로 구성한 **제안 수업 설계**다.

| 요소 | 설계 |
|---|---|
| 대상 | Python·기초 ML을 알고 지식그래프 또는 OWL을 처음 적용하는 연구자·산업 AI 학습자 |
| 사전 지식 | 클래스·개체·관계, precision/recall, train/test 분리 |
| 학습목표 1 | 자연어 문장에서 클래스·개체·공리를 구분해 작성한다 |
| 학습목표 2 | 문자열이 다른 두 공리가 논리적으로 동치 또는 함의 관계인지 reasoner 기준으로 판정한다 |
| 학습목표 3 | 파싱 성공, 일관성, 엔터티 정확도, 공리 정확도를 분리해 보고한다 |
| 학습목표 4 | 에이전트 결과·평가자 결과·인간 검수 결과가 불일치하는 사례를 분류한다 |
| 실습 | 동일 텍스트에 Greedy 추출과 이전 공리를 참조하는 AR 추출을 적용하고, 누락·과잉·모순을 비교 |
| 평가 | 공리 작성 30%, 오류 분류 20%, 지표 계산 20%, 테스트 누출 방지 설계 20%, 한계 기술 10% |

**예상 오개념과 피드백**

- “문법적으로 유효한 OWL이면 올바른 온톨로지다”  
  → 파싱 가능성, 논리적 일관성, 원문 충실성은 별도 조건임을 반례로 확인한다.

- “생성 공리가 많을수록 recall이 높으므로 좋은 결과다”  
  → precision, 중복 공리율, 과잉 생성률을 함께 계산한다.

- “reasoner가 모순을 찾지 못하면 원문 의미를 보존했다”  
  → reasoner는 주어진 공리들의 관계를 검사할 뿐, 자연어–공리 정렬 오류를 자동으로 보장하지 않는다.

- “LLM 평가 점수가 높으면 인간 평가도 대체된다”  
  → PADMÉ에서도 인간 검증은 별도로 수행됐고, 보고된 일치율은 85%이지 100%가 아니다.

---

## 5. 정보 기반 미니 튜토리얼  
### 문자열 일치 대신 추론기 기준으로 온톨로지 출력을 평가하기

**형태:** 비실행형 개념·설계 튜토리얼  
APOLO 원문과 수식·실험표는 공개되어 있지만, 이번 확인 범위에서는 완성된 공식 재현 저장소를 확인하지 못했다. 따라서 아래 절차는 실행 검증된 APOLO 복제 코드가 아니다.

### 준비물

- [APOLO v1 원문](https://arxiv.org/abs/2609.34540)
- Protégé
- HermiT 또는 ELK reasoner
- 두 개의 OWL 파일:
  - `gold.owl`: 전문가 정답
  - `predicted.owl`: 모델 생성 결과
- 원문 문장과 생성 공리를 연결한 표

### 예제

원문:

> 모든 전기 모터는 설비이며, Motor-01은 전기 모터이다.

정답 공리:

```text
ElectricMotor SubClassOf Equipment
Motor01 Type ElectricMotor
```

모델 출력 A:

```text
ElectricMotor SubClassOf Equipment
Motor01 Type ElectricMotor
```

모델 출력 B:

```text
Motor01 Type Equipment
```

모델 출력 C:

```text
ElectricMotor DisjointWith Equipment
Motor01 Type ElectricMotor
```

### 단계별 평가

1. **파싱 검사**

   각 출력이 OWL 문법으로 로드되는지 확인한다. 로드되지 않으면 APOLO 방식에서는 해당 출력 점수를 0으로 처리한다.

2. **일관성 검사**

   Reasoner를 실행한다. 출력 C는 `ElectricMotor ⊑ Equipment`라는 정답 구조와 함께 사용할 경우 배타 공리와 충돌할 수 있다.

3. **엔터티 평가**

   `ElectricMotor`, `Equipment`, `Motor01`의 추출 여부를 precision·recall로 계산한다.

4. **공리 precision 평가**

   모델 공리 각각이 `gold.owl`에서 함의되는지 검사한다.

   - A의 두 공리: 모두 함의됨
   - B의 `Motor01 Type Equipment`: 정답에 명시되지는 않았지만 두 정답 공리로부터 함의됨
   - 따라서 B를 단순 문자열 불일치만으로 오답 처리하면 안 된다.

5. **공리 recall 평가**

   정답 공리 각각이 `predicted.owl`에서 함의되는지 검사한다.

   - B는 `Motor01 Type Equipment`만 포함하므로 원래의 클래스 계층과 직접 타입 공리를 복구하지 못한다.
   - 최종 사실 하나를 맞혔지만 온톨로지 구조의 재현성은 낮다.

6. **원문 충실성 검사**

   각 생성 공리에 근거 문장을 연결한다. Reasoner 통과 여부와 별개로, 원문이 실제로 해당 공리를 지지하는지 사람이 확인한다.

### 기대 출력

| 출력 | 파싱 | 일관성 | 함의 기반 precision | 구조 recall | 판정 |
|---|---:|---:|---:|---:|---|
| A | 통과 | 통과 | 높음 | 높음 | 적합 |
| B | 통과 | 통과 | 높을 수 있음 | 낮음 | 불완전 |
| C | 통과 | 실패 가능 | 낮음 | 판정 전 수정 필요 | 모순 |

### 검증 문항

1. `Motor01 Type Equipment`가 정답 파일에 문자열로 없으면 무조건 오답인가?  
   **정답:** 아니다. 정답 온톨로지에서 논리적으로 함의되는지 확인해야 한다.

2. 일관성 있는 생성 온톨로지는 원문을 충실히 표현했는가?  
   **정답:** 보장되지 않는다. 잘못된 공리끼리도 일관적일 수 있다.

3. axiom recall만 최대화하면 어떤 문제가 발생하는가?  
   **정답:** 불필요하거나 근거 없는 공리를 대량 생성해 recall을 높일 수 있으므로 precision·중복률·과잉 생성률을 같이 봐야 한다.

### 평가상 주의

- reasoner 종류와 지원하는 OWL 프로파일을 고정해야 한다.
- 동치 공리, 추이 관계, 복수의 유효한 형식화를 고려해야 한다.
- 개발 과정에서 같은 test ontology를 반복 조회하면 프롬프트가 테스트셋에 맞춰질 수 있다.
- APOLO 결과는 단일 실행이므로, 적용 연구에서는 seed 반복과 신뢰구간 보고가 필요하다.
- 바이오·식물 온톨로지에서의 결과를 사용자 도메인으로 직접 일반화할 수 없다. APOLO 연구 자체도 PO에서 상대적으로 낮은 공리 성능을 보였다.