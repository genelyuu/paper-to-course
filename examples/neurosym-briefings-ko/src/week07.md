# 신경·기호 AI 주간 연구·교육 브리핑

## 1. 조사 범위

- **검색 기준일:** 2026년 11월 6일
- **대상 기간:** 2026년 10월 30일 00:00–11월 5일 23:59, 한국시간
- **검색원:** arXiv `cs.AI·CL·DB·LO·LG·MA·CR`, ACL Anthology, SpringerLink, ScienceDirect, IEEE·ACM 색인, 대학·연구기관 페이지, GitHub, 공식 문서·데이터 저장소.
- **주요 검색식:**
  - `(ontology OR OWL OR ABox OR "description logic") AND (generation OR extraction OR reasoning OR retrieval)`
  - `("natural language" OR text) AND ("logical form" OR formalization OR Cypher OR SPARQL OR Datalog)`
  - `("knowledge graph" OR GraphRAG) AND (reasoning OR provenance OR verification OR incompleteness)`
  - `("multi-agent" OR "agentic AI") AND (trust OR assurance OR audit OR authority OR containment OR reputation)`
- **포함:** 기간 중 신규 원문, 심사 논문의 온라인 공개, 방법·실험·공개 산출물이 실질적으로 바뀐 개정판.
- **제외:** 순수 벡터 RAG, 일반 GNN, 신뢰·검증 없는 에이전트 협업, 서지만 변경된 개정판, 이전 주와 동일한 판본.
- **중복 통합:** arXiv와 저널 판본이 함께 있으면 심사 완료 저널 판본을 대표로 사용했다.

표기:

- **[사실]** 원문·공식 메타데이터에서 확인
- **[저자 주장]** 논문의 해석·결론
- **[적용 추론]** 사용자 연구와 Re:Charge에 대한 제안
- 모든 수치는 저자 보고값이며, 별도로 명시하지 않은 한 이번 조사에서 재실행하지 않았다.

## 2. 핵심 결론

이번 주에는 다음 세 변화가 중요하다.

1. **정확 추론과 근사 추론을 결합하는 방식이 구체화됐다.** NIR은 `ALCIQ` 인스턴스 검색을 Transformer로 근사하되, named class와 TBox는 symbolic fallback에 맡긴다.
2. **신경망이 찾고 형식 시스템이 인증하는 패턴이 강해졌다.** Whiel은 LLM이 제안한 loop invariant를 Vampire와 Lean으로 검증한다.
3. **멀티에이전트 신뢰가 “평판 점수”에서 “권한·영향·증거 계보”로 이동했다.** Airlock은 권한 위임 트리와 데이터 provenance DAG를 분리해 오류 전파를 선택적으로 차단한다.

Re:Charge에 대한 이번 주 우선 적용 순서는 다음과 같다.

1. **Lifecycle-aware KG:** Identity–Specification–Released Version–Runtime State 분리  
2. **NIR:** 대규모 후보 검색용 근사 추론, HermiT/Pellet은 최종 승인 gate로 유지  
3. **Airlock:** 에이전트 산출물의 영향 계보와 권한 회수

---

# 3. 신규·실질 개정 자료 목록

## A. 온톨로지 생성·추론 및 산업 KG

### A1. Lifecycle-aware knowledge graphs with human-in-the-loop agentic retrieval for automotive manufacturing

- **저자/기관:** Chao Yang, Ying Liu, Hao Dong, Peixing Zhang, Jinzhi Lu, Bing Zhu, Risto Ojala, Kari Tammi; Aalto University 등
- **공개:** 2026년 11월, 온라인 확인 11월 1일
- **상태:** *Advanced Engineering Informatics* 76, 105122, **심사 저널·오픈 액세스**
- **DOI:** [10.1016/j.aei.2026.105122](https://doi.org/10.1016/j.aei.2026.105122)
- **기여·방법:** 제조 객체를 `persistent identity`, `engineering specification`, `released version`, `runtime state`로 분리한 lifecycle KG와, 자연어를 검증 가능한 Cypher subgraph/path query로 바꾸는 complexity-adaptive agent를 제안한다. 복잡하거나 모호한 조건에는 사람 확인 gate를 둔다.
- **평가:** 실제 자동차 제조 데이터, 단순·다중 hop 산업 질의, conventional generative baseline 비교. **실행 정확도 95.0%**. 공개 초록에는 문항 수·정확한 분할이 노출되지 않았다. 코드는 요청 시 제공이다.
- **한계:** 공개 코드가 아니며, HITL 확인 비용과 다른 제조 도메인 이전성이 충분히 측정되지 않았다.
- **[적용 추론]:** Re:Charge의 `Project/Asset Identity`, `Engineering Revision`, `Approved Baseline`, `Calculation Runtime State`를 서로 다른 객체로 분리해야 한다. 현재 L1–L3 구조와 직접 맞는다.
- **등급:** **A—즉시 설계 전이 가능**

### A2. Dam defects ontology and knowledge graph construction from multi-source hazard data using LLMs

- **저자/기관:** Jianfeng Huang, Wenang Hou, Shichen Zhang, Zhenhan Du, Jiangshan Yin; 중국 수리·댐 연구기관 계열
- **공개:** 2026년 11월 1일경
- **상태:** *Advanced Engineering Informatics* 76, 104987, **심사 저널**
- **DOI:** [10.1016/j.aei.2026.104987](https://doi.org/10.1016/j.aei.2026.104987)
- **기여:** Dam Defects Ontology와 OHCF를 결합한다. OHCF는 fine-tuning, temperature-perturbed voting, ontology consistency check, expert validation을 거쳐 ontology를 반자동 확장한다.
- **평가:** 중국의 결함·위험 댐 22,076건 보고서로 KG 구축. 저자 보고상 분류 평가 지표가 모두 90% 이상이며 component ablation을 수행했다. 접근 가능한 초록에서는 데이터 분할·비교군별 수치가 확인되지 않았다.
- **한계:** 폐쇄적인 산업 데이터, expert-validation 비용, 세부 오류 유형·source-span 정확도가 공개 초록에 부족하다.
- **[적용 추론]:** CAPEX 문서 분류에서도 단일 LLM 판정보다 다중 샘플 voting→온톨로지 제약→Cost Engineer 승인 순서를 적용할 수 있다.
- **등급:** **A**

### A3. OntoDoc: Automatically Generating Ontology Resource Descriptions

- **저자:** Juan Guajardo Gutierrez, Mike Tran, Nasim Shirvani Mahdavi, Chengkai Li
- **최초 공개:** 2026년 10월 31일, arXiv:2611.01276 v1
- **상태:** ISWC 2026 제출 표기, 공식 채택 확인 전이므로 **미심사**
- **원문:** [arXiv:2611.01276](https://arxiv.org/abs/2611.01276)
- **기여:** IRI 하나에 대해 SPARQL로 KG 문맥을 수집하는 agent, 웹 문맥 agent, assumption agent, description agent로 자연어 ontology documentation을 생성한다.
- **평가:** 생의학·농업·범용 KG 3개, LLM automatic judge와 인간 11명. naive LLM보다 평균 completeness가 12% 개선되고 template verbalizer보다 최대 5점 척도 2.8점 높았다.
- **한계:** 생성 설명이 형식 공리와 논리적으로 동치인지 검증하지 않으며, 웹 근거의 편향과 LLM judge 문제가 남는다.
- **[적용 추론]:** Re:Charge ontology의 class/property 설명문·UI tooltip 초안 생성에는 유용하지만 OWL 정의 자체를 수정할 권한을 주면 안 된다.
- **등급:** **B—방법 전이 가능**

### A4. NIR: Approximate Neural Instance Retrieval for ALCIQ

- **저자/기관:** N’Dah Jean Kouagou, Pritilata Saha, Caglar Demir, Axel-Cyrille Ngonga Ngomo; Paderborn University DICE
- **최초 공개:** 2026년 11월 2일, v1
- **상태:** **미심사**
- **원문·코드:** [arXiv](https://arxiv.org/abs/2611.02842) · [OWLAPY](https://github.com/dice-group/owlapy)
- **기여:** `ALCIQ` class expression의 인스턴스 membership을 KG embedding으로 근사한다. GRU·LSTM·Transformer와 논리 연산자별 subnet을 갖는 compositional encoder를 비교한다.
- **평가:** 8개 benchmark, Pellet이 만든 정답, class-expression 길이 최대 9. ABox를 25·50·75%만 유지하는 불완전 조건도 평가한다. Jaccard 0.691–0.994. 대형 Carcinogenesis·Mutagenesis 설정에서 3분 이내인 반면 EBR 비교군은 96시간 내 완료하지 못했다. Transformer가 불완전 ABox에 가장 강하고 compositional model은 완전 KG에서 논리 구조를 더 잘 반영했다.
- **한계:** 정확성 보장이 없고, Pellet이 생성한 label 자체에 의존한다. 주요 속도 비교가 H100 GPU 기준이며 surface syntax에 민감하다.
- **[적용 추론]:** 대규모 CAPEX ABox의 후보 검색에는 적합하지만 승인·금액 규칙·applicability 판단은 여전히 HermiT/Pellet/SQL constraint가 결정해야 한다.
- **등급:** **A**

---

## B. 지식그래프 추론·문장→실행 논리

### B1. Explore-over-Graph: Hybrid Embedding–LLM Reasoning for KGQA under Incompleteness

- **저자:** Ola El Khatib, Djellel Difallah
- **공개:** 2026년 11월 1일
- **상태:** *Findings of IJCNLP-AACL 2026*, **심사 학회**
- **원문:** [ACL Anthology](https://aclanthology.org/2026.findings-aacl.98/)
- **기여:** KG에 edge가 없을 때 LLM이 사실을 직접 생성하지 않고, type-level relation 통계와 KG embedding으로 누락 경로 후보를 복원한다. LLM은 후보 선택·계획·추론만 담당한다.
- **평가:** WebQSP, CWQ, Wikidata 기반 BRINK; 완전 KG와 인위적 불완전 KG, 여러 LLM backbone 및 planning-based baseline. 불완전 KG에서 task-specific KGQA 학습이 없는 비교군보다 일관되게 우수하고 token을 최대 33% 절감했다. 공개 abstract에는 세부 점수가 없다.
- **한계:** embedding이 제안한 edge는 사실 확인이 아니라 plausibility다. 복원된 경로를 provenance상 원래 KG 사실처럼 저장하면 안 된다.
- **[적용 추론]:** Re:Charge에서는 누락된 비용·공정 관계를 `asserted`가 아닌 `candidateHypothesis`로 분리하고 사람 승인 전 계산에 사용하지 않아야 한다.
- **등급:** **A/B**

### B2. Less but Sufficient: Relation Knowledge Selects Compact KG Contexts

- **저자:** Seunghui Jwa, Minsu Oh, Sangwoo Hong, Yeo Chan Yoon
- **최초 공개:** 2026년 11월 1일, v1
- **상태:** **미심사**
- **원문:** [arXiv:2611.01733](https://arxiv.org/abs/2611.01733)
- **기여:** relation path 지식으로 작은 KG context를 선택하고 derivability·consistency check와 routing gate를 적용한다.
- **평가:** CLUTRR, MetaQA, PathQuestion, WebQSP, CWQ; 7개 open LLM. CWQ에서 SubgraphRAG와 유사한 성능을 약 1/4 prompt token으로 달성했다. 사전 지정 held-out precision gate는 WebQSP 17.6% coverage/89.8% precision, CWQ 4.9%/95.9%였다.
- **한계:** 고정밀 gate의 coverage가 매우 낮다. consistency check가 검사할 수 있는 named-entity fact는 2.5% 정도이며, KG에 이미 존재하는 잘못된 사실은 대부분 통과한다.
- **[적용 추론]:** 높은 확신의 일부 질의만 자동 처리하고 나머지는 승인자에게 넘기는 `answerability gate`의 실증 근거다.
- **등급:** **A**

### B3. NeuroGraph: graph-driven neuro-symbolic threat reasoning in advanced manufacturing

- **저자/기관:** Padmeswari Nandiya, Ahmad Mohsin, Iqbal H. Sarker, Ahmed Ibrahim, Helge Janicke
- **최초 판본:** arXiv 2026년 9월
- **저널 공개:** 2026년 11월 5일
- **상태:** *International Journal of Information Security* 25:185, **심사 저널·오픈 액세스**
- **DOI:** [10.1007/s10207-026-01345-8](https://doi.org/10.1007/s10207-026-01345-8)
- **방법:** 첫 LLM이 자연어를 ontology-constrained Cypher로 바꾸고, Neo4j 실행 결과만 두 번째 LLM의 답변 근거로 허용한다. symbolic query가 실패하면 embedding으로 anchor만 복구한 뒤 다시 Cypher를 실행한다.
- **평가:** 공개 CTI benchmark, baseline 대비 reasoning accuracy·hallucination·multi-hop·adversarial robustness·runtime 분석. 접근 가능한 abstract에는 정확한 데이터 규모와 표별 수치가 없었다.
- **한계:** 자연어→Cypher 오류와 KG completeness에 의존하며, 제조 보안 도메인 밖 이전성은 미검증이다.
- **[적용 추론]:** Re:Charge의 자연어 질의를 바로 SQL로 보내기보다 ontology-constrained query plan→실행→근거 기반 답변으로 분리하는 참고 구조다.
- **등급:** **A**

### B4. Whiel: A Neurosymbolic Platform for Certified Relational Program Verification

- **저자/기관:** Jesse Comer, Fangzhu Shen, Shuo Zhang, Mayur Naik, Sudeepa Roy, Val Tannen; Duke University
- **최초 공개:** 2026년 11월 3일, v1
- **상태:** **미심사**
- **원문·코드:** [arXiv](https://arxiv.org/abs/2611.05612) · [GitHub](https://github.com/JesseComer/whiel)
- **방법:** Datalog·graph query·schema mapping을 imperative relational program과 Hoare triple로 표현한다. LLM이 invariant를 제안하고 Vampire가 verification condition을 검사하며, 최종 결과를 Lean proof certificate로 재구성한다.
- **평가:** equivalence 64, containment 18 등 총 86개 task—valid 69, invalid 17. GPT-5.5 기준 Whiel 73/86(85%), one-round 46/86(53%), DirectLean 20/86(23%). 평균 189초, 2.95 rounds, $0.49.
- **한계:** curated benchmark이며 실제 enterprise query migration 규모는 아직 작다. 86개 중 13개는 해결하지 못했다.
- **[적용 추론]:** 비용 규칙·SQL query rewrite·revision comparison 로직의 동치성과 containment를 proof-carrying rule change로 확장할 수 있다.
- **등급:** **A/B**

### B5. Math Foundation Formalization Agent

- **저자:** Jiaxin Xie, Guowei Dou, Xiang Ji, Wensheng Yu
- **공개:** 2026년 11월 2일, v1
- **상태:** **미심사**
- **원문:** [arXiv:2611.02843](https://arxiv.org/abs/2611.02843)
- **기여:** LLM, Rocq proof assistant, task classification, execution feedback, state management을 결합해 집합론·실수·명제논리·선택공리 formalization을 다룬다.
- **평가:** 네 수학 기초 case study로 source completion, interactive verification, reproducible compilation을 구분한다. 정량 benchmark는 공개 abstract에 제시되지 않았다.
- **한계:** 일반 자연어→논리 데이터셋이나 산업 규정 formalization 평가가 아니다.
- **[적용 추론]:** “코드 생성 성공”과 “proof assistant 재컴파일 성공”을 분리하는 평가 관점은 규칙 DSL 생성에 적용할 수 있다.
- **등급:** **C—배경·방법 참고**

---

## C. 멀티에이전트 신뢰·검증

### C1. Airlock: Bounding the Multi-Agent Blast Radius via Selective Online Containment

- **저자:** Zhonghao Zhan, Javad Forough, Yefan Zhang, Krinos Li, Xiao Ma, Hamed Haddadi
- **공개:** 2026년 11월 4일, v1
- **상태:** **미심사**
- **원문·코드:** [arXiv](https://arxiv.org/abs/2611.06727) · [EdgeCitadel](https://github.com/EdgeCitadelTeam/EdgeCitadel)
- **방법:** 권한은 parent→child delegation tree로 제한하고, 데이터 소비는 append-only provenance DAG로 추적한다. 경보 후 forward trace로 오염된 실행을 차단하고 backward trace로 근원을 좁힌다.
- **평가:** testbed 1,832회, 물리 smart-home LLM 161회, simulation record 24,266건. 주 testbed에서 경보 후 잘못된 actuation을 전부 차단하고 convergence 후 leak 0. A2A·LangGraph native control 대비 정상 업무를 68–96%p 더 보존했다.
- **한계:** 올바른 경보가 적시에 들어온다는 전제가 강하다. symptom-only detection과 외부 서비스의 원자적 commit은 미완성이다.
- **[적용 추론]:** 잘못된 설비단가를 사용한 하위 견적·BOE·승인 대기 작업만 동결하고 무관한 프로젝트 계산은 유지하는 구조로 전이 가능하다.
- **등급:** **A**

### C2. Assurance-Conditioned Continuous Authorization for Autonomous AI Agents

- **저자:** Mehdi Shajari
- **공개:** 2026년 11월 3일, v1
- **상태:** **미심사**
- **원문:** [arXiv:2611.05632](https://arxiv.org/abs/2611.05632)
- **기여:** evidence validity와 applicability를 분리하고, 현재 유효한 증거에서 agent의 effective-authority envelope를 계속 재계산한다. authority epoch가 바뀌면 오래된 action을 effect-time에서 거부한다.
- **평가:** trading profile의 default-deny, 권한 축소·회복, 정책 불일치, stale action 거부를 regression scenario로 구현했다. 정량 비교 연구는 아니다.
- **한계:** dependency graph completeness가 보장되지 않고 중간 authorization-basis version 경로가 구현·시험되지 않았다.
- **[적용 추론]:** 승인자·Estimator 권한을 정적 role만으로 정하지 않고, 현재 RuleSet·데이터 버전·검증 상태가 바뀌면 산출 실행 권한을 회수하는 데 적합하다.
- **등급:** **A/B**

### C3. Who Audits Whom, on What Substrate, with What Evidence? v2

- **저자/기관:** Mohamed Chahine Ghanem, Baidaa Al-Bander; Keele 계열
- **최초 공개:** 2026년 9월 16일
- **실질 개정:** 2026년 10월 31일, v2
- **상태:** **미심사**
- **원문:** [arXiv:2609.18272](https://arxiv.org/abs/2609.18272)
- **개정 내용:** 주체·기반모델/도구·증거의 독립성을 3축으로 등급화하고 weakest-link로 결합한다. v2는 common-cause failure의 closed-form 분석, declared-scope predicate, false-flag rate·detection floor를 구체화했다. 공개 파일 크기도 크게 증가했다.
- **평가:** procurement-control agent를 세 audit grade로 분석. 동일 모델 계열 공통고장 비율 0.90, 내부 보고확률 0.6이라는 선언 조건에서 conventional internal audit가 관찰 가능한 fault의 5.9%만 표면화한다. 이는 실제 측정값이 아니라 모델 기반 조건부 결과다.
- **한계:** 입력한 공통고장·보고확률에 결과가 민감하다.
- **[적용 추론]:** 생성 agent와 verifier가 같은 모델·prompt·retrieval stack을 공유하면 “다중 에이전트”여도 독립 검증으로 간주하지 않아야 한다.
- **등급:** **A**

### C4. Anduin: A sybil-resistant agentic marketplace reputation system

- **저자:** Reza Ramji, Preston Vander Vos, Ziming Zeng, Duc V. Le
- **공개:** 2026년 11월 3일, v1
- **상태:** **미심사**
- **원문:** [arXiv:2611.05586](https://arxiv.org/abs/2611.05586)
- **방법:** buyer–provider payment graph와 기존 신뢰 network에서 max-flow 계열 provider rating을 계산한다.
- **평가:** 16개 blockchain, 157일, 6,600만 transaction, $6.1M, buyer 813명. 모의 Sybil 공격의 조작 비용이 구매자 총지출의 약 20%이며 standard similarity보다 약 23배 어려웠다.
- **한계:** 결제 규모는 업무 결과의 정확성이나 품질 증거가 아니다. blockchain marketplace 밖 일반화가 불명확하다.
- **[적용 추론]:** Re:Charge에서는 “에이전트 평판”보다 승인된 산출물·독립 검사·재작업 기록을 edge로 사용해야 한다.
- **등급:** **B/C**

### C5. Secure LLM deployment in smart-grid energy informatics

- **저자:** Shuaichen Tong, Bin Zhang, Heyang Sun, Yang Liu 외
- **공개:** 2026년 11월 4일
- **상태:** *Energy Informatics*, **심사 저널·오픈 액세스**
- **DOI:** [10.1186/s42162-026-00700-2](https://doi.org/10.1186/s42162-026-00700-2)
- **방법:** power KG evidence, permission-aware entailment, 계층형 위험지표와 confidence calibration으로 LLM response risk를 검증한다.
- **평가:** 전력 업무 4개 시나리오, 비식별 interaction과 adversarial sample. rule scoring·TextCNN·RoBERTa·일반 LLM 판별과 비교해 Macro-F1 94.6%, 위험 정량화 오류 18.7% 감소, scoring consistency 12.4% 향상. 400 req/s에서 143ms, 800 req/s에서 verification success 98.4%.
- **한계:** 데이터 규모와 분할이 공개 abstract에 충분히 나오지 않으며 내부 전력 시뮬레이션 기반이다.
- **[적용 추론]:** RLS가 허용한 데이터라는 사실과 해당 데이터가 현재 질의에 적용 가능한 근거인지를 분리하는 설계에 유용하다.
- **등급:** **A/B**

---

## 4. 미발견·보류 사항

- 이 기간에는 **문장→ABox 또는 문장→1차 논리 표현을 전용 benchmark로 정량 평가한 신규 연구를 확인하지 못했다.** 대신 자연어→Cypher, Datalog/Hoare triple formalization, ontology description generation 연구가 확인됐다.
- `Who May Overrule the Agent?`와 `Agent Harness Awareness`는 11월 5일 arXiv 신규 목록에 나타났지만 원문 색인의 최초 제출일이 각각 9월 12·13일로 표시되는 메타데이터 충돌이 있었다. 이번 회차의 엄격한 날짜 기준에서는 본 목록에서 제외하고 다음 회차에 이력을 재확인한다.
- MOIE-KG·OA-RAG·GraphRAGProv 등 지난주 자료는 이번 기간의 새 판본이 확인되지 않아 반복 수록하지 않았다.
- Spring/ACM/IEEE 검색에서는 위 목록 외에 기간 조건과 직접 관련성을 모두 만족하는 신규 심사 논문을 추가로 확인하지 못했다.

---

# 5. 직접 관련성 상위 3건 상세 적용

## 5.1 Lifecycle-aware KG → Re:Charge 객체·Revision 모델 개편

### 적용 단계

1. `Asset`에서 다음 객체를 분리한다.
   - `AssetIdentity`
   - `EngineeringSpecification`
   - `ReleasedRevision`
   - `ObservedRuntimeState`
2. 비용 산출도 같은 패턴으로 분리한다.
   - `EstimateIdentity`
   - `EstimateBasis`
   - `ApprovedEstimateRevision`
   - `CalculationRun`
3. 자연어 질의를 바로 SQL/Cypher로 실행하지 않고 `QueryIntent → GraphPattern → Validation → Execution` 상태를 기록한다.
4. 결과를 바꾸는 모호성이 있을 때만 Cost Engineer에게 확인한다.
5. 확인 결과를 prompt history가 아니라 versioned domain decision으로 저장한다.

### 필요 코드·데이터

- 현재 Re:Charge ontology와 PostgreSQL revision schema
- 승인·개정 이력이 존재하는 실적 프로젝트 3–5개
- 자연어 competency question 60개 이상
- 논문 코드는 요청 필요이므로 구조를 독립 구현해야 한다.

### 최소 검증 실험

- 단순 조회 20, 다중 hop 20, revision-sensitive 20문항.
- 비교:
  1. 직접 text-to-SQL
  2. schema prompt 기반
  3. lifecycle KG + validation/HITL
- 지표: executable query rate, execution accuracy, 잘못된 revision 선택률, 확인 요청률, 승인자 수정시간.
- 같은 query template이 train/test에 동시에 들어가지 않도록 template-disjoint split을 사용한다.

## 5.2 NIR → Protégé 추론의 후보검색 가속 계층

### 적용 단계

1. HermiT/Pellet로 200개 CQ class expression의 exact instance set을 생성한다.
2. 동일 ontology에서 individual·relation embedding을 만든다.
3. NIR Transformer가 반환한 후보와 exact set을 비교한다.
4. NIR 결과를 최종 결론으로 쓰지 않고 다음 정책으로 사용한다.
   - high-score 후보: exact reasoner 재검증
   - low-score 또는 정책 중요 규칙: 바로 exact reasoner
   - 승인·금액·접근권한: NIR 사용 금지
5. ontology revision별 threshold와 calibration을 다시 측정한다.

### 필요 자료

- [OWLAPY](https://github.com/dice-group/owlapy), MIT license
- 공개 Family·Carcinogenesis·Mutagenesis KG
- [NIR pretrained models](https://files.dice-research.org/datasets/CNIR/trained_models.zip)
- Re:Charge OWL export와 CQ 200개

### 최소 검증 실험

- class-expression 길이 2–9를 균형 있게 구성.
- 완전 ABox와 25·50·75% retention 조건.
- Transformer NIR / compositional NIR / HermiT 또는 Pellet 비교.
- Jaccard, precision, recall, false-negative rate, P95 latency, GPU/CPU 비용을 측정.
- 업무 안전성 때문에 최적 threshold는 accuracy가 아니라 **recall 하한**을 기준으로 정한다.

## 5.3 Airlock → 에이전트 산출물의 영향 격리

### 적용 단계

1. 각 agent에 독립 실행 ID와 권한 ceiling을 부여한다.
2. 입력 데이터 소비를 다음 edge로 기록한다.  
   `source artifact → agent run → derived artifact → calculator run → approval candidate`
3. 잘못된 단가·환율·RuleSet이 발견되면 descendant 작업을 forward trace한다.
4. 외부 효과가 없는 조회 작업은 유지하고, 계산·DB write·승인 제출만 fence한다.
5. 원인이 해소된 뒤 affected run만 재계산하고 snapshot을 비교한다.

### 필요 코드·데이터

- [EdgeCitadel 코드](https://github.com/EdgeCitadelTeam/EdgeCitadel)
- 현재 audit event·snapshot·calculator run ID
- fault injection이 가능한 POC 환경

### 최소 검증 실험

- 4개 agent: 문서 추출, ontology mapper, calculator, approval-preparer.
- 오류 30건: 잘못된 단가, stale 환율, 잘못된 applicable rule, 위조 approval status.
- 비교: source agent만 중지 / 전체 workflow 중지 / provenance 기반 선택 격리.
- 지표: post-alert unauthorized write, 정상 작업 보존률, containment latency, 재실행 수, 잘못 격리된 작업 수.

---

# 6. 교육공학적 적용

이번 주 연구 가운데 **학습자를 대상으로 교육 효과를 검증한 논문은 확인되지 않았다.** 다음 표는 모두 논문 결과를 기반으로 제안한 수업 설계다.

| 연구 | 대상·사전지식 | 관찰 가능한 목표·활동 | 평가·오개념과 피드백 |
|---|---|---|---|
| Lifecycle KG | 제조·지식공학 대학원생; RDF/Cypher | 동일 설비를 identity/spec/revision/state로 분해하고 자연어 질의를 graph pattern으로 변환 | revision 정확도 루브릭. “최신 상태가 항상 승인 baseline”이라는 오개념에 승인되지 않은 runtime 반례 제공 |
| Dam DDO/OHCF | 산업 NLP 수강생; 분류·ontology | voting→constraint→expert gate를 순서대로 적용 | 단계별 오류 감소와 비용 채점. 다수결을 사실 검증으로 오해하지 않도록 공통 hallucination 사례 제시 |
| OntoDoc | Protégé 입문자 | IRI 설명을 생성하고 공리·SPARQL 근거와 대조 | 정확성·완전성·출처성 3축. 자연스러운 설명을 논리적 동치로 보지 않게 피드백 |
| NIR | DL·ML 수강생 | `ALCIQ` expression의 exact와 approximate instance set 비교 | Jaccard·recall·latency. 높은 Jaccard를 soundness guarantee로 해석하지 않도록 false-negative 확인 |
| XoG | KGQA 수강생 | 누락 edge를 asserted fact와 hypothesis로 분리 | hypothesis provenance와 최종 검증 여부 채점. embedding score를 진실 확률로 해석하지 않게 함 |
| Less but Sufficient | IR/KG 수강생 | compact context와 100-fact context를 token·정확도로 비교 | precision–coverage curve. 높은 precision이 높은 전체 자동화율을 뜻하지 않음을 설명 |
| NeuroGraph | 산업 보안·AI | 자연어→Cypher→evidence→answer trace를 작성 | Cypher 실행성과 evidence sufficiency를 분리 채점 |
| Whiel | DB·형식검증 | Datalog equivalence를 Hoare triple로 표현하고 counterexample 또는 proof 확인 | Lean certificate 존재 여부. LLM이 invariant를 제시했다는 사실을 증명으로 채점하지 않음 |
| MFF-Agent | 논리·증명보조기 입문자 | 자연어 정의를 Rocq source로 만들고 재컴파일 | source completion/interactive proof/reproducible build를 별도 채점 |
| Airlock | 멀티에이전트 시스템 | 오염된 artifact의 descendants를 찾아 최소 격리 집합 구성 | leak·healthy-work retention 루브릭. source agent만 끄면 전파가 끝난다는 오개념 교정 |
| ACCA | AI governance | evidence 만료·환경 변경에 따라 authority envelope 재계산 | stale action 거부 여부. identity와 현재 authority를 동일시하지 않게 함 |
| Audit Independence v2 | 신뢰 AI | principal/substrate/evidence independence를 실제 시스템에 등급화 | weakest-link 근거 요구. agent 수를 독립성으로 세지 않음 |
| Anduin | graph security | Sybil node 추가 전후 rating 변화를 계산 | manipulation cost·품질 상관 분리. 결제량을 품질로 오해하지 않도록 함 |
| Smart-grid KG security | 산업 AI 보안 | permission과 semantic applicability를 별도 판정 | F1·calibration·latency 평가. 접근 가능 데이터를 답변 근거로 자동 인정하지 않음 |

---

# 7. 한국어 미니 튜토리얼

## OWLAPY NIRReasoner로 신경·기호 인스턴스 검색 시험하기

**형태:** 공개 코드·모델 기반의 **미실행 튜토리얼**이다. 명령과 코드는 공식 OWLAPY 1.6.4 문서에서 확인했지만, 이번 회차에서 모델 파일을 내려받아 실행하지는 않았다.

### 7.1 출처·버전

- 논문: [NIR: Approximate Neural Instance Retrieval for ALCIQ](https://arxiv.org/abs/2611.02842), v1
- 코드: [dice-group/owlapy](https://github.com/dice-group/owlapy)
- 문서 확인 버전: OWLAPY 1.6.4
- 공개 모델: [trained_models.zip](https://files.dice-research.org/datasets/CNIR/trained_models.zip)
- 공개 KG: [KGs.zip](https://files.dice-research.org/projects/Ontolearn/KGs.zip)

### 7.2 개념

`NIRReasoner`는 다음처럼 작동한다.

- named class와 짧은 TBox/ABox 질의: symbolic fallback
- 복잡한 class expression: Transformer/LSTM/GRU/compositional encoder가 각 individual의 membership score를 계산
- 기본 threshold: 0.5
- 결과는 **근사 후보 집합**이며 OWL entailment certificate가 아니다.

### 7.3 준비

```bash
git clone https://github.com/dice-group/owlapy
cd owlapy
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pip install torch transformers pandas

wget https://files.dice-research.org/projects/Ontolearn/KGs.zip -O KGs.zip
unzip KGs.zip

wget https://files.dice-research.org/datasets/CNIR/trained_models.zip -O trained_models.zip
unzip trained_models.zip
```

Windows에서는 가상환경 활성화 명령을 `.venv\Scripts\activate`로 바꾼다.

### 7.4 최소 실행 예시

아래 코드는 Family ontology의 실제 class/property IRI가 배포본에서 `male`, `female`, `hasChild`로 노출된다는 공식 예시를 따른다. 파일 구조가 다르면 먼저 signature를 출력해 이름을 확인해야 한다.

```python
from owlapy.owl_ontology import Ontology
from owlapy.owl_reasoner import NIRReasoner
from owlapy.class_expression import (
    OWLClass,
    OWLObjectIntersectionOf,
    OWLObjectSomeValuesFrom,
)
from owlapy.owl_property import OWLObjectProperty
from owlapy import owl_expression_to_dl

ontology_path = "KGs/Family/family-benchmark_rich_background.owl"

onto = Ontology(ontology_path)

classes = {c.remainder.lower(): c for c in onto.classes_in_signature()}
properties = {
    p.remainder.lower(): p for p in onto.object_properties_in_signature()
}

male = classes["male"]
female = classes["female"]
has_child = properties["haschild"]

query = OWLObjectIntersectionOf([
    male,
    OWLObjectSomeValuesFrom(has_child, female),
])

reasoner = NIRReasoner(
    onto,
    model_path=(
        "trained_models/nir_pretrained_models/"
        "NIR_Transformer_family"
    ),
    embeddings_path=(
        "trained_models/embeddings/family/"
        "DeCaL_entity_embeddings.csv"
    ),
    th=0.5,
    symbolic_max_length=1,
)

instances = list(reasoner.instances(query))

print("DL query:", owl_expression_to_dl(query))
print("Retrieved individuals:")
for individual in instances:
    print(individual)
print("Stats:", reasoner.retrieval_stats())
```

### 7.5 예상 출력

정확한 individual 목록은 모델·파일 버전과 threshold에 따라 달라질 수 있다. 다음 형태를 기대한다.

```text
DL query: male ⊓ (∃ hasChild.female)
Retrieved individuals:
OWLNamedIndividual(...)
...
Stats: {
  'n_retrieval_calls': 1,
  'n_nir_calls': 1,
  'n_symbolic_calls': 0,
  ...
}
```

`n_nir_calls`가 0이면 query가 `symbolic_max_length` 이하이거나 코드가 symbolic fallback을 사용한 것이다.

### 7.6 exact reasoner와 비교

NIR 결과만 보지 말고 Pellet 또는 HermiT의 exact result와 비교해야 한다.

```python
from owlapy.owl_reasoner import SyncReasoner

exact = SyncReasoner(
    ontology=ontology_path,
    reasoner="Pellet",
)

gold = set(exact.instances(query))
pred = set(instances)

intersection = gold & pred
union = gold | pred

precision = len(intersection) / len(pred) if pred else 0.0
recall = len(intersection) / len(gold) if gold else 0.0
jaccard = len(intersection) / len(union) if union else 1.0

print({
    "exact_count": len(gold),
    "nir_count": len(pred),
    "precision": precision,
    "recall": recall,
    "jaccard": jaccard,
})
```

이 코드 역시 이번 회차에서 직접 실행하지 않았다. Pellet 연동에는 Java 환경이 추가로 필요할 수 있다.

### 7.7 검증 질문

1. **NIR 결과가 Pellet 결과와 95% 일치하면 OWL 추론을 대체할 수 있는가?**  
   아니오. 나머지 5%에 승인·안전·금액 관련 사례가 포함될 수 있으며 soundness·completeness가 보장되지 않는다.

2. **왜 incomplete ABox 조건을 따로 평가해야 하는가?**  
   실제 프로젝트 KG는 문서 미수집·추출 실패·승인 대기로 assertion이 빠져 있기 때문이다.

3. **Re:Charge에서 NIR 사용이 부적절한 질의는?**  
   최종 승인 여부, 접근권한, 적용 RuleSet, 금액 확정처럼 false positive/negative가 업무 통제에 직접 영향을 주는 질의다.

4. **가장 적절한 역할은?**  
   대규모 individual 중 exact reasoner가 검사할 후보를 줄이는 pre-filter 또는 exploratory search다.

### 7.8 평가상 주의점

- random query split뿐 아니라 **expression-template-disjoint split**을 사용한다.
- precision만 보고 threshold를 선택하지 말고 critical query의 recall 하한을 정한다.
- ontology revision이 바뀌면 embedding·threshold·calibration을 다시 검증한다.
- H100에서 얻은 속도를 일반 CPU 또는 Mac 환경에 그대로 적용하지 않는다.
- Protégé에서 일관성을 통과했다는 사실과 NIR 검색 정확도는 서로 다른 검증 항목이다.

이번 주의 가장 실행 가치가 높은 결과는 **Lifecycle KG의 4계층 객체 분리**, **NIR의 근사-후보/정확-승인 이중 추론**, **Airlock의 provenance 기반 선택 격리**다.