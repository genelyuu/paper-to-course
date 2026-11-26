# 신경·기호 AI 주간 연구·교육 브리핑

## 1. 조사 범위와 판정 기준

- **기준일:** 2026년 10월 30일
- **대상 기간:** 2026년 10월 23일 00:00–10월 29일 23:59
- **검색 범위:** arXiv `cs.AI`, `cs.CL`, `cs.MA`, `cs.LO`, `cs.DB`, `cs.CR`, `cs.SE`, `cs.LG`; ScienceDirect·SpringerLink·ACM DL·IEEE·ACL Anthology와 학회/연구기관 페이지; GitHub·Zenodo·Hugging Face 등 공개 산출물.
- **주요 검색식:**
  - `(neuro-symbolic OR ontology OR OWL OR ABox OR "ontology learning") AND (reasoning OR generation OR extraction)`
  - `("natural language" OR sentence OR text) AND ("logical form" OR DSL OR ABox OR formalization)`
  - `("knowledge graph" OR RDF OR SPARQL) AND (reasoning OR provenance OR evidence OR verification)`
  - `("multi-agent" OR "agentic AI") AND (trust OR verification OR audit OR corroboration OR reliability)`
- **실질 개정 판정:** 새 실험·데이터·방법·결과·코드가 추가된 판본만 포함. 서지·오탈자 수정만으로 보이는 개정은 제외.
- **중복 처리:** arXiv–학회–저널 판본은 DOI·제목·저자 기준으로 통합하고 가장 심사 수준이 높은 판본을 대표 판본으로 삼았다.
- **색인 지연 주의:** 이번 조사 시점에 확인 가능한 arXiv 신규 원문은 주로 10월 27일 UTC 제출분까지였다. 28–29일 늦은 제출분은 다음 회차에 뒤늦게 나타날 수 있다.

표기: **[사실]** 원문·메타데이터에서 직접 확인, **[저자 주장]** 논문의 해석, **[연결 추론]** 사용자 연구에 대한 적용 판단이다.

## 2. 이번 주 결론

가장 중요한 흐름은 다음 세 가지다.

1. **문서→트리플 생성 자체보다 검증·수정·출처 추적이 중심 문제로 이동했다.** MOIE-KG는 온톨로지를 동적 중간표현으로 사용하고, GraphRAGProv는 각 답을 원문 문장까지 역추적한다.
2. **온톨로지를 텍스트 문맥으로만 제공하는 방식에서 OWL/DL 추론기를 도구로 호출하는 방식으로 진전했다.** OA-RAG가 가장 직접적인 사례다.
3. **멀티에이전트 합의나 PASS 선언은 신뢰 근거가 아니다.** 독립 증거 계보, 기계적 재검증, 비용을 고려한 신뢰 정책이 별도 평가 대상이 되고 있다.

Re:Charge에 가장 직접적인 세 자료는 **MOIE-KG → OA-RAG → GraphRAGProv** 순이다.

---

## 3. 직접 관련 연구 목록

| 연구·상태 | 기여와 방법 | 평가·주요 결과 | 한계와 연구 연결 |
|---|---|---|---|
| **[MOIE-KG](https://doi.org/10.1016/j.knosys.2026.117109)** — Xianhui Liu, Yueying Liu, Yiheng Zhuang, Wenlong Hou; *Knowledge-Based Systems* 352, 117109; 10월 25일 온라인 공개; **심사 저널** | **[사실]** 조정·메모리, 전역정보, 온톨로지 제어, 엔티티, 관계, 검증·수정의 6개 에이전트가 장문 문서를 처리한다. 온톨로지를 고정 스키마가 아닌 통제된 동적 중간표현으로 사용한다. | Re-DocRED, BioRED, ChemDisGene Curated, MINE의 고정·개방 온톨로지 설정과 다중 백본, 절제·민감도·비용 분석. 개방 설정에서 SCR 86.95%, entity fidelity 94.32%, relation fidelity 90.37%. 공개 색인에서 정확한 분할별 수치는 전부 확인되지 않았다. | 공개 코드 저장소는 확인하지 못했다. 다중 에이전트 호출 비용과 오류 상관성이 남는다. **[연결 추론]** Re:Charge의 문서 수집→용어 정규화→트리플→규칙 검증→승인 구조와 가장 유사하다. |
| **[Before Blaming the LLM, Diagnose the Workflow](https://arxiv.org/abs/2610.35267)** — Liang Zhang, Benoît Daireaux, Sergey Alyaev; v1 10월 26일; **미심사** | NL→온톨로지 기반 ABox DSL을 Input–Generator–Output–Validator–Repairer의 5개 역할과 7개 난이도 변수로 진단한다. | 시추 도메인의 “Bottom Hole Depth” 예제 1건을 통한 질적 분석. 벤치마크·통계 검증·평가자 간 일치도는 없다. | **[저자 명시]** 예측 모델이 아니라 경험 기반 진단 틀이다. **[연결 추론]** Transformer 성능만 비교하지 말고 입력 충분성, 온톨로지 문맥, 템플릿 적합성, 검증 강도별 오류를 기록하는 평가표로 활용할 수 있다. |
| **[NeSySpec](https://arxiv.org/abs/2610.35403)** — Pier Mattia Basciano 외 4인; v1 10월 26일; **미심사** | Logic Tensor Networks로 물리 제약을 미분 가능한 술어로 만들고, 위반 제약 진단·변경 필드 귀추·최소 변경 복구·결측 시 기권을 한 파이프라인에서 수행한다. | 항공기 107종; train 44, validation 17, test 16종 및 미관측 family/class 평가. 위반 제약 top-1 94.2% 대 Fellegi–Holt 79.5%, 변경 필드 59.3% 대 30.6%. 합성 오류 비중이 크다. | 실제 사양 위조·도메인 이전 증거가 제한적이다. **[연결 추론]** CAPEX 금액·일정·선후행·용량 제약을 연속 truth degree와 hard OWL/SWRL 규칙으로 분리하는 참고안이다. |
| **[Evolve on Graph](https://arxiv.org/abs/2610.35598)** — Zongyuan Sun 외 10인; v1 10월 26일; **미심사**, [코드](https://github.com/Szy5/EoG) | QA 주석 없이 한 LLM이 Proposer와 Solver를 맡는다. FOL 쿼리를 실행하는 Symbolically Verifiable Topology Synthesis가 정답 집합을 만들고, Solver 경계의 문제를 선택하는 curriculum을 사용한다. | WebQSP, CWQ, GrailQA, GTSQA, WikiWebQuestions 및 500문항 IndustryCarBench. 5개 공개 벤치마크 평균에서 최강 무주석 기준보다 Hit@1 +7.46%p, F1 +12.05%p; 산업 KG에서 84.8% 대 ToG 67.0%. | KG 쿼리 결과를 정답으로 간주하므로 KG 오류를 학습할 수 있다. **[연결 추론]** Re:Charge KG에서 실행 가능한 CQ를 자동 생성해 추론 에이전트의 훈련 자료로 만들 수 있다. |
| **[OA-RAG](https://arxiv.org/abs/2610.36335)** — Hui Yang, Jiaoyan Chen, Yongsheng Gao; University of Manchester·SNOMED International; v1 10월 26일; **미심사** | ReAct 에이전트가 name linking, reasoner-backed ASK, SELECT/DESCRIBE를 호출하고 답을 entailed/supported/related/unrelated로 분류한다. | GO·FoodOn·SNOMED CT 기반 Test-1 1,500문항, Test-2 1,477문항, 6개 의료 QA 6,781문항. Llama-3-8B 평균 50.5%로 최강 비교군 38.9%; Qwen 계열 68.1% 대 60.9%. 완전한 gold evidence 회수율은 MCQ 61.7%, 개방형 23.6%. | grounding label이 모델 자체 판단이며 형식 증명서는 아니다. 합성 문항과 의료 도메인 의존성이 있다. **[연결 추론]** Protégé 온톨로지 추론 결과를 생성 모델의 문맥이 아니라 독립 도구 결과로 제공하는 직접 설계안이다. |
| **[Ontology-guided multi-agent reasoning for explainable differential diagnosis](https://arxiv.org/abs/2610.36325)** — Roxana Szomiu, George Ursu, Adrian Groza; v1 10월 26일; **미심사**, 코드 공개 표시 | 증상 매핑, 감별진단, 누락 증상 선택, 후속 질문을 온톨로지 기반 다중 에이전트로 수행한다. | 198개 사례. Phase 1→2 top-1 18.7→21.2%, top-3 25.8→27.3%; 평균 의미유사도도 소폭 상승했다. | 절대 정확도가 낮고 후속 질문 효과가 작다. 임상 안전성을 입증하지 않았다. **[연결 추론]** 누락된 프로젝트 필드를 질문으로 되묻는 `clarification agent` 설계에 유용하다. |
| **[SFE-O](https://arxiv.org/abs/2610.37123)** — Thomas Pallet 외 6인; v1 10월 27일; IEEE ICAI-TEMS 2026 표기 있으나 공식 수록 확인 전이므로 **미심사로 취급**; [OWL 산출물](https://doi.org/10.5281/zenodo.21983081) | 7개 모듈로 구성된 OWL 2 온톨로지. 공정 topology, 파라미터 provenance, 계산 의존성을 표현하고 ChEBI·QUDT·OWL-Time·PROV-O를 재사용한다. | 실제 pilot batch 1건, HermiT 일관성 검사, competency SPARQL 1건. 성능 벤치마크가 아니다. | 사례 수가 1이고 수치 계산·SHACL·AI 효과 평가는 없다. **[연결 추론]** Protégé 모듈화와 CAPEX 수치의 입력/계산/외부출처/승인값 provenance 모델링에 적합하다. |
| **[Prospector](https://arxiv.org/abs/2610.37121)** — Haiqian Yang, Markus J. Buehler; v1 10월 27일; **미심사**, 코드·adapter·graph 공개 보고 | Qwen-4B 정책이 `find/expand/connect` 도구로 과학 KG를 단계적으로 탐색하고, 검색된 edge chain을 답의 증거로 제시한다. | semiconductor KG의 path-disjoint 평가와 bio-materials·PFAS·materials-property KG로 zero-shot 이전. gated accuracy 0.839±0.015, 동일 도구를 받은 최강 frontier 모델 0.877. | 그래프와 문항 모두 저자 파이프라인이 생성해 외부 정답 기준이 약하다. gate가 인용 edge의 완전한 연결 경로까지 검사하지는 않는다. |
| **[GraphRAGProv](https://arxiv.org/abs/2610.37237)** — Wadie El Amrani, Luis Galárraga; INRIA 등; v1 10월 27일; **미심사** | 원문 span과 연결된 RDF/RDF-star에 SPARQL을 실행하고 how-provenance polynomial로 답에 사용된 statement occurrence 조합을 복원한다. | 2Wiki 200 + MuSiQue 200. 398건 SPARQL 실행, 327건 답 반환, 311건 완전한 원문 trace. 정답이 맞아도 잘못된 추출·누락 join을 발견했다. | accuracy 개선 실험이 아니라 400건 demo 분석이다. **[연결 추론]** 모든 CAPEX 트리플에 문서·페이지·문장 span·추출기 버전을 붙여 승인자가 역추적하게 하는 핵심 설계다. |
| **[Clearing the FoG](https://arxiv.org/abs/2610.37405)** — Zongyuan Sun 외 5인; v1 10월 27일; **미심사** | evidence-grounded question synthesis와 evidence-coverage process reward를 사용해 “답만 맞는” KG 에이전트가 아니라 지원 트리플을 실제로 검색하는 에이전트를 학습한다. | 3개 KGQA 벤치마크, 3B–4B 모델, answer accuracy와 evidence coverage, cross-KG zero-shot. 공개 초록에서 분할·정확한 수치는 확인되지 않았다. | 합성 증거가 KG 자체 오류를 반영할 수 있다. **[연결 추론]** 답 정확도와 별도로 `필수 근거 트리플 회수율`을 Re:Charge 평가 지표로 추가해야 한다. |
| **[Process-Aware Knowledge Graphs for Reliable Multi-Step Service Invocation](https://arxiv.org/abs/2610.37242)** — Saiful Khan, Afrah Farea; v1 10월 27일; **미심사** | OData metadata와 BPMN을 typed property graph로 합쳐 API의 순서·payload key·code-list 제약을 검색 단계에 제공한다. | 42개 서비스, 저 lexical-overlap query 74건에서 Recall@3 +5.7%p; 81개 멀티스텝 업무에서 완료율 38.7% 대 chunk 기준 10.3%. full typed context 사용 시 invalid call 3/101, invented code 0. | 38.7% 완료율은 배포 수준에 낮다. **[연결 추론]** 프로젝트 승인·조달·집행 순서를 KG의 process edge로 표현할 근거다. |
| **[The Structure Gap](https://arxiv.org/abs/2610.37523)** — Kheer Sagar Patel, Mojtaba Soltanalian; v1 10월 27일; **미심사** | 구조를 아는 solver와 구조를 예제에서 다시 학습하는 모델 사이의 유한 데이터 격차를 이론화한다. | inverse problem 증명, sparse recovery, graph reachability. 8-node 16,384개 학습 후 24-node에서 BFS 100%, FCN 73.05%, GNN-8 96.03%; 5 seeds. | 실제 LLM·온톨로지 실험은 아니다. **[연결 추론]** 이미 알려진 선후행·카디널리티 규칙을 Transformer가 재학습하게 하지 말고 추론기에 고정해야 한다는 이론적 근거다. |

---

## 4. 멀티에이전트 신뢰·검증 연구

| 연구·상태 | 평가와 결과 | 중요한 해석 |
|---|---|---|
| **[Can LLMs Trust Appropriately?](https://arxiv.org/abs/2610.34107)** — Mengdi Chu, Jintao Huang; v1 10월 25일, 수정 10월 27일; **미심사** | 23개 협업 범주의 324개 3단계 시나리오, 7개 모델, 36개 controlled-history pair. 최상 모델 decision accuracy 99.0%, all-stage 96.9%; 다른 모델들은 가치가 0인 검사를 구매하거나 과도한 safeguard를 선택했다. | **[연결 추론]** agent trust를 평판 점수가 아니라 오류확률·검사비용·향후 손실을 포함한 정책으로 정의해야 한다. |
| **[PASS Is a Claim, Not an Observation](https://arxiv.org/abs/2610.35950)** — Lei Zhenbing, Lei Chang; v1 10월 24일; **미심사** | 179개 broadcast에서 10개 코드 수정 주장을 재검사. mtime 일치 70%, 주장 파일에서 방어 패턴 발견 60%, 방송만으로 결정론적 재검증 가능 80%; 재검증 가능한 주장 중 50%가 주장 위치 검사를 실패했다. | 사례가 한 플랫폼·10건뿐이다. 그러나 “agent가 검증 완료라 말했다”와 “독립 검사기가 통과했다”를 데이터 모델에서 분리해야 함을 명확히 보여준다. |
| **[Replication or Corroboration?](https://arxiv.org/abs/2610.36151)** — Hoang-Loc Cao 외 8인; v1 10월 26일; **미심사** | 동일 증거의 반복과 독립 증거를 구분하는 root replication invariance와 lineage quotient를 제시. 28,224 direct-star profile, 2,052 DAG, AVeriTeC 기반 277 profile을 exhaustive audit했다. | 증거 root의 독립성 정보가 입력에 이미 제공되어야 한다. **[연결 추론]** 여러 에이전트가 같은 CAPEX 문장을 재인용해도 신뢰도가 증가하지 않도록 `evidenceRootID`로 중복 제거할 수 있다. |
| **[When Is a Relation Worth Trusting?](https://arxiv.org/abs/2610.37239)** — Vincess Dongmo, Astride Melvin Fokam Ninyim; v1 10월 27일; **미심사** | relation별 공격 비용과 exposure를 모델링하고 degree gating·기권 정책을 제안. 6개 graph, 90개 설정에서 clean-trained graph detector가 graph-free 모델보다 낮은 경우가 58건; exposure/cost가 16건 중 15건에서 최적 hardening relation을 선택했다. | 다관계 수가 적으면 대부분 기권하고, 비용 추정이 없으면 적용이 어렵다. CAPEX KG에서는 외부업체 주장, 승인기록, 계산값 등 relation별 조작비용을 다르게 모델링할 수 있다. |
| **[Coverage Under Contradiction](https://arxiv.org/abs/2610.37162)** — Pasha Abrishamchian 외 4인; v1 10월 27일; **미심사**, 데이터 공개 | 6개 데이터셋의 63,372개 원본–부정 편집 evidence pair. 원본을 더 높게 평가한 비율은 BM25 68.8%, Qwen3 dense 56.0%, Jina 52.2%로 dense retriever가 거의 chance에 가까웠다. | 합성된 부정 문서이므로 실제 규정 충돌과 다르다. **[연결 추론]** “승인됨/승인되지 않음”, “포함/제외” 같은 부정·예외 규정을 별도 retrieval 시험군으로 만들어야 한다. |
| **[Dependency Graphs of Mathematical Arguments](https://arxiv.org/abs/2610.36776)** — Eunji Park; v1 10월 27일; **미심사** | source occurrence, context state, inference record와 검토 상태를 분리한 논증 의존 DAG를 제안한다. | **평가 설계만 있고 경험적 결과는 없다.** | 주장된 교육·검토 효과는 미입증이다. 다만 CAPEX 규칙의 전제–추론–결론 의존 관계를 버전 관리하는 데이터 모델로 참고할 수 있다. |

### 제외·보류 자료

- **Who Convinced Whom?**은 이번 주 arXiv 목록에 노출됐지만 최초 제출일이 10월 18일이고 이번 기간의 실질 개정이 확인되지 않아 제외했다.
- **SCOPE**는 arXiv 노출일보다 앞선 EMNLP 데모 논문이 이미 존재하여 신규 연구로 중복 계산하지 않았다.
- **Validating FKG.in v3**는 10월 27일 개정됐지만 접근 가능한 변경 이력만으로 실험·방법의 실질 변화를 확인하지 못해 보류했다.
- 순수 KGE·GNN 성능 논문, 일반 RAG, 협업 비용만 최적화하고 신뢰·검증을 다루지 않은 멀티에이전트 논문은 제외했다.
- 검색한 공식 학회·저널 색인에서 MOIE-KG 이외에 기간 내 새로 온라인 공개된, 직접 관련성이 높은 심사 논문은 확인하지 못했다.

---

## 5. 직접 관련성 상위 3건 적용 설계

### 5.1 MOIE-KG: 문서→온톨로지→검증 에이전트 구조

**적용 단계**

1. 공통 상태를 `Document–Span–Entity–Relation–OntologyTerm–ValidationEvent`로 정의한다.
2. 에이전트를 문서 구조 분석, 용어 정규화, 온톨로지 제어, 엔티티/관계 추출, 검증·수정, 승인 조정자로 나눈다.
3. 에이전트가 새 클래스를 즉시 추가하지 못하게 하고 `candidate → reviewed → accepted/rejected` 상태를 둔다.
4. 트리플에는 반드시 문서 ID, 페이지·문장 span, 추출 모델·prompt 버전, 검증 결과를 저장한다.
5. 최종 OWL 반영은 사람 승인 후에만 수행한다.

**필요 자료**

- 내부 CAPEX 문서와 gold span/triple 표본.
- 현재 Protégé OWL 파일과 competency question.
- 공개 비교용 Re-DocRED 또는 BioRED.
- 논문 코드 저장소는 확인되지 않았으므로 재현보다는 구조 차용으로 시작한다.

**최소 검증 실험**

- 문서 50건 또는 조항 200개.
- `single Transformer` 대 `single + ontology context` 대 `multi-agent + independent verifier`.
- entity/relation micro-F1, ontology 위반률, 근거 span 정확도, 승인자 수정시간, 호출비용을 측정.
- 동일 문서가 train/test에 중복되지 않는 **document-level split**을 사용한다.

### 5.2 OA-RAG: Protégé 추론기를 독립 도구로 사용

**적용 단계**

1. Protégé의 OWL ontology와 annotation을 versioned release로 내보낸다.
2. `entity_link`, `ASK entailment`, `SELECT`, `DESCRIBE`, `explain`을 별도 도구 API로 제공한다.
3. LLM이 답하기 전에 reasoner 도구를 호출하고, 사용한 axiom·triple ID만 evidence digest에 넣는다.
4. 답을 `entailed / supported / related / unsupported`로 분류하되, 첫 항목은 반드시 실제 entailment 결과로 결정한다.
5. inconsistent ontology나 evidence 미회수 시 답을 생성하지 않고 기권한다.

**최소 검증 실험**

- CAPEX CQ 100개: 직접 사실 30, 다중 hop 30, 규칙 entailment 20, 부정·충돌 20.
- 비교: 일반 RAG / ontology text RAG / reasoner-tool agent.
- answer accuracy 외에 evidence precision·recall, entailment-valid answer rate, unsupported answer rate, 호출 수·토큰을 측정한다.
- OA-RAG의 개방형 evidence 회수 약점을 고려해 evidence recall을 주 지표로 둔다.

### 5.3 GraphRAGProv: 원문까지 역추적되는 트리플

**적용 단계**

1. 모든 트리플을 단순 RDF 사실과 그 사실의 occurrence로 분리한다.
2. occurrence에 `sourceDocument`, `page`, `start/end offset`, `extractorVersion`, `reviewStatus`를 연결한다.
3. SPARQL 결과에 사용된 occurrence 조합을 provenance expression으로 저장한다.
4. 승인 화면에는 “답→SPARQL join→트리플→원문 span” 경로를 표시한다.
5. 같은 사실을 여러 에이전트가 복제한 경우 occurrence는 남기되 같은 evidence root로 묶는다.

**최소 검증 실험**

- 100개 질의와 300개 gold 근거 span.
- 최종 답 정확도, 완전 trace 비율, 잘못된 join 비율, unsupported-correct-answer 비율, 감사 소요시간을 측정한다.
- 답이 맞더라도 근거 경로가 틀린 사례를 별도 오류 등급으로 둔다.

---

## 6. 교육공학적 적용

이번 주 논문 중 **교육 효과를 학습자 대상으로 실험한 연구는 확인되지 않았다.** 아래 내용은 모두 논문 결과가 아니라 제안 수업 설계다.

| 연구 | 대상·선수지식 | 관찰 가능한 목표·활동 | 평가와 예상 오개념/피드백 |
|---|---|---|---|
| MOIE-KG | 대학원생; IE·RDF 기초 | 장문 1개를 에이전트 역할별로 처리하고 ontology extension 후보를 심사 | 역할별 오류표 루브릭. “에이전트 수가 많으면 독립 검증”이라는 오개념에는 공유 evidence root를 표시 |
| Workflow Profile | NL2DSL 연구자 | 실패 사례를 7개 변수로 코딩하고 개선 레버를 제안 | 평가자 간 일치도와 개선안의 구체성. 모델 성능과 workflow 난이도를 혼동하지 않게 동일 모델을 고정 |
| NeSySpec | AI·공학 대학원생 | hard rule과 fuzzy constraint를 구분하고 오류 필드를 귀추 | 진단·수정 근거 루브릭. 높은 anomaly score를 인과 설명으로 오해하지 않도록 반례 제공 |
| EoG | KGQA·RL 수강생 | FOL topology로 실행 가능한 질문과 정답 집합 생성 | 쿼리 실행 가능성·정답 완전성. KG 결과를 현실의 절대 진실로 보지 않게 오류 트리플 삽입 |
| OA-RAG | 온톨로지·RAG 수강생 | 텍스트 근거와 논리적 entailment를 구별 | 답·evidence·entailment 각각 채점. “관련 있음=함의됨” 오개념을 반례로 피드백 |
| 진단 멀티에이전트 | 의료정보/설명가능 AI | 후속 질문 전후 entropy와 진단 순위 변화 계산 | 질문의 정보이득과 안전한 기권 평가. 소폭 정확도 상승을 임상 유효성으로 과대해석하지 않게 함 |
| SFE-O | Protégé 입문자 | 모듈 import, 일관성 검사, CQ 실행 | 아래 튜토리얼 체크리스트. `consistent`를 완전·정확한 ontology로 오해하지 않게 미검출 오류 예시 제공 |
| Prospector | KG tool-use 수강생 | 검색 edge만으로 연결된 evidence chain 구성 | 경로 연결성·answer membership을 분리 채점. edge가 검색됐다는 사실과 답을 지지한다는 사실을 구별 |
| GraphRAGProv | 데이터 provenance 수강생 | 답에서 원문 span까지 역추적 | trace 완전성 루브릭. “정답이면 추출도 옳다”는 오개념에 논문의 correct-answer/wrong-evidence 사례 제시 |
| FoG | KGQA 수강생 | answer reward와 evidence-coverage reward를 비교 | answer F1과 evidence recall 모두 채점. 정답 일치가 증거 회수 성공을 의미하지 않음을 확인 |
| Process-aware KG | 소프트웨어·지식공학 | BPMN 순서를 KG edge와 API constraint로 표현 | invalid key/code/order 오류별 채점. code list만 주면 payload도 안전하다는 오개념 교정 |
| Structure Gap | ML 이론 수강생 | node-size 외삽에서 FCN/GNN/BFS 비교 | n=8→24 성능 하락을 해석. 구조 사용을 단순 파라미터 증가로 설명하지 않게 함 |
| Trust Calibration | 멀티에이전트 AI | posterior·검사비용·미래손실로 최적 행동 계산 | regret 기반 문항. 검사는 많을수록 좋다는 오개념에 가치가 0인 검사 사례 제공 |
| PASS 재검증 | 소프트웨어 에이전트 수강생 | PASS 주장과 외부 관찰을 분리한 audit record 작성 | 재현 가능한 locator·command·artifact 요구. agent 자기보고를 ground truth로 채점하지 않음 |
| Replication/Corroboration | 논증·신뢰 AI | 동일 root 복제와 독립 root 추가 시 verdict 변화 비교 | replication invariance 검사. 다른 표현을 독립 증거로 오판하지 않게 lineage 표시 |
| Relation Trust | 그래프 보안 수강생 | relation별 exposure/cost로 사용·gating·기권 결정 | 공격 전후 성능과 비용을 함께 채점. clean accuracy가 높은 relation을 자동 신뢰하지 않게 함 |
| Contradiction Retrieval | IR 수강생 | 긍정/부정 near-twin 문서의 순위를 비교 | pairwise preference·nDCG. 의미 임베딩이 부정을 자동 처리한다는 오개념에 최소대립쌍 제공 |
| Argument Dependency | 수리논증 수강생 | 증명의 premise–inference–conclusion DAG 작성 | 누락 전제·source link·review status 루브릭. graph depth를 증명의 본질적 난이도로 해석하지 않게 함 |

---

## 7. 한국어 정보 기반 미니 튜토리얼

### SFE-O OWL 2 온톨로지를 Protégé에서 검사하기

**형태:** 공개 산출물 기반 비실행형 튜토리얼. 아래 절차는 원문과 공개 OWL 산출물에 근거하지만, 이번 브리핑 작성 환경에서 Protégé를 직접 실행해 재검증하지는 않았다.

### 출처와 버전

- [SFE-O 논문 v1](https://arxiv.org/abs/2610.37123), 2026-10-27
- [SFE-O v0.1.0 OWL 산출물](https://doi.org/10.5281/zenodo.21983081)
- Protégé Desktop 5.x와 HermiT reasoner 권장
- 논문이 재사용한 외부 자원: QUDT, PROV-O, OWL-Time, ChEBI

### 핵심 개념

- **모듈화:** Biomass, Process, Product 등 관심사를 서로 다른 ontology module로 분리한다.
- **Provenance:** 값이 입력값인지, 측정값인지, 계산값인지, 외부 검색값인지, fitting 결과인지 표현한다.
- **일관성:** HermiT가 모순을 발견하지 못한 상태다. 현실 세계의 정확성이나 완전성을 뜻하지 않는다.
- **Competency question:** ontology가 답할 수 있어야 하는 도메인 질문을 SPARQL 또는 DL Query로 시험한다.

### 단계별 절차

1. Zenodo record에서 전체 배포 파일을 내려받고 라이선스·버전이 `v0.1.0`인지 기록한다.
2. Protégé에서 aggregate/main ontology 파일을 연다.
3. `Active Ontology → Imports`에서 7개 로컬 모듈과 외부 ontology import가 해석됐는지 확인한다.
4. `Entities → Classes`에서 Biomass–Process–Product 계층과 parameter provenance 관련 클래스를 찾아본다.
5. `Reasoner → HermiT → Start reasoner`를 실행한다.
6. `owl:Nothing` 아래에 예상하지 않은 named class가 생기는지 확인한다.
7. worked pilot batch individual을 열고 pressure·temperature 등 값에 단위와 provenance가 연결돼 있는지 확인한다.
8. 논문/배포물의 competency query가 제공된다면 SPARQL 탭에서 그대로 실행하고, source pressure·temperature 값이 반환되는지 대조한다.
9. Re:Charge용으로 다음 네 유형의 값 모델을 별도 후보로 작성한다.
   - 문서에 직접 기재된 값
   - 계산된 CAPEX 값
   - 외부 단가에서 가져온 값
   - 사람 검토로 승인된 최종값
10. 새 후보는 원본 SFE-O 파일을 수정하지 말고 별도 import ontology에 작성한다.

### 예상 출력

- HermiT 실행 후 ontology가 consistent로 보고된다.
- 의도하지 않은 unsatisfiable named class가 없어야 한다.
- 논문의 보고에 따르면 competency query는 pilot batch의 source pressure와 temperature를 정확히 돌려준다. 이는 **저자 보고 결과**이지 이번 브리핑에서 독립 재현한 결과는 아니다.

### 검증 질문과 정답 기준

1. **HermiT가 consistent라고 하면 모든 데이터 값이 현실적으로 맞는가?**  
   아니오. 표현된 OWL 공리와 assertion 사이에서 형식 모순을 찾지 못했다는 뜻이다.

2. **계산식을 OWL 안에 넣으면 수치 시뮬레이션까지 수행되는가?**  
   아니오. SFE-O는 계산 의존성을 표현하지만 수치 solver를 포함하지 않는다.

3. **QUDT를 재사용하는 이유는 무엇인가?**  
   측정량·단위 표현을 자체 문자열보다 일관되고 상호운용 가능하게 만들기 위해서다.

4. **Re:Charge에서 가장 먼저 차용할 요소는 무엇인가?**  
   값의 provenance 분류와 계산 의존성, 모듈화 방식이다. CO₂ 추출 도메인 클래스 자체를 그대로 가져오는 것은 적절하지 않다.

### 평가상 주의점

- `consistent/unsatisfiable class 수`만으로 ontology 품질을 평가하지 않는다.
- CQ coverage, SHACL 위반, provenance 누락률, 단위 불일치, 사람이 수정한 assertion 수를 함께 측정한다.
- 외부 import 버전을 고정하지 않으면 같은 실습도 나중에 다른 결과를 낼 수 있다.
- 논문의 한 개 pilot batch 결과를 Re:Charge 일반화 근거로 사용해서는 안 된다.

---

## 8. 다음 회차 작업을 더 구체화하는 추가 지시문

주간 지시문에 다음 조건을 추가하면 결과의 재현성과 연구 활용도가 높아진다.

> ‘실질 개정’은 새 데이터셋·실험·방법·오류 수정·공개 산출물이 추가된 경우로 한정하고 변경 근거를 적는다. 각 자료를 A(직접 적용), B(평가·신뢰 설계), C(인접 이론)로 등급화한다. 모든 트리플 추출 연구에는 document-level split 여부, source-span 평가 여부, ontology consistency·SHACL·reasoner 검증 여부를 기록한다. 멀티에이전트 연구에는 에이전트 오류 독립성, evidence lineage, 독립 verifier, 비용·지연을 기록한다. 교육 설계는 논문에서 검증된 효과와 제안 활동을 별도 열로 분리한다. 공개 코드는 저장소 존재뿐 아니라 라이선스, 실행 지침, 데이터 접근성, 최근 commit을 확인한다. 튜토리얼은 직접 실행 여부와 실행 환경을 첫머리에 명시하고, 재현 실패 시 실패 단계와 필요한 자료를 보고한다.