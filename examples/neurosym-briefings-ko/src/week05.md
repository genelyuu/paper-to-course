# 신경·기호 AI 주간 연구·교육 브리핑

## 1. 조사 범위

- **검색 기준일:** 2026-10-23
- **포함 기간:** 2026-10-16 00:00–2026-10-22 23:59
- **검색원:** arXiv의 cs.AI·cs.CL·cs.LG·cs.LO·cs.MA·cs.CR·cs.SE, SpringerLink/LNCS, ACL Anthology, OpenReview, ACM·IEEE 공개 색인, CEUR 및 저자 공개 저장소
- **주요 검색식:**  
  `(neuro-symbolic OR neurosymbolic) AND (ontology OR knowledge graph OR reasoning)`  
  `("natural language" OR sentence) AND (logic OR LTL OR FOL OR formalization)`  
  `("multi-agent" OR agentic) AND (trust OR verification OR guard OR assurance)`  
  `(ontology generation OR KG construction OR semantic parsing) AND LLM`
- **포함 기준:** 기간 중 최초 공개되었거나 방법·실험·결론이 실질적으로 바뀐 판본, 원문에서 연구 주제와 평가 설계를 확인할 수 있는 자료
- **제외 기준:** 단순 날짜·서식 수정, 응용 분야에서 ‘agent’만 사용하는 논문, 리뷰되지 않은 홍보자료, 동일 학회의 arXiv·출판 판본 중복
- **주의:** ‘모두’는 위 검색원에서 발견되고 원문 관련성을 확인한 자료를 뜻한다. 비공개 기술 보고서와 색인 지연 자료까지 완전 포괄한다는 의미는 아니다.

표기: **[사실]** 원문·서지에서 확인, **[저자 주장]** 논문의 해석, **[연결 추론]** 사용자 연구에 대한 제안.

## 2. 이번 주 핵심 판단

가장 직접적인 자료는 세 편이다.

1. **AgentOnto**: 데이터베이스·문서·예제 작업을 하나의 갱신 가능한 분석 온톨로지로 통합한다. 사용자의 제조·투자엔지니어링 문서 및 AACE 비용 온톨로지에 가장 직접적이다.
2. **HeritageKGBench 연구**: LLM 문장→복합 온톨로지 트리플 변환에서 검증기를 뒤에 붙이는 것만으로는 상류 추출 오류가 복구되지 않는다는 강한 부정적 결과를 제시한다.
3. **PerMIT**: 공유 메모리와 에이전트 간 지식을 신뢰·검증하는 구체적 구조, 공격 실험 및 Lean 4 정리를 제공한다.

또한 이번 주에는 자연어→LTL→반례→자연어 수정의 폐루프를 구현한 **SpecRepair**, OWL/Turtle 산출물과 전체 재현 코드를 공개한 **NIKG**가 교육·프로토타이핑 관점에서 특히 유용하다.

---

## 3. 직접 관련 연구 목록

### A. 온톨로지 생성·KG 구성·추론

| 연구·상태 | 핵심 기여와 방법 | 평가·결과 | 한계 및 연구 연결 |
|---|---|---|---|
| **[AgentOnto](https://arxiv.org/abs/2610.23317)** — Pan 외, v1 10/16, 심사 중, [DOI](https://doi.org/10.48550/arXiv.2610.23317) | DB·업무문서·예제 작업에서 `Entity/Relation–Metric–DB Mapping` 온톨로지를 만들고, 계획 생성·검사·SQL 실행·피드백 갱신 전 단계에 사용 | WDI 282건+AQS 324건. 평균 분석 정확도 87.5% 대 최강 기준선 DIN-SQL 55.0%. 고정 온톨로지 분석만 비교하면 95.9%, silent semantic error 5.5%. 22개 갱신 사건에서 보고된 갱신·보존·일반화 성능은 모두 100%. | 코드·벤치마크 전체가 공개되지 않았고 한 계열의 생성/평가 모델에 크게 의존한다. **[연결 추론]** `E=장비·문서·공정`, `M=비용/성숙도 계산 규칙`, `G=문서 위치·SQL·RDF 매핑`으로 옮기고, 갱신 시 correction/retention competency question을 실행한다. |
| **[LLM-Based KGC for Cultural Heritage](https://doi.org/10.1007/978-3-032-41614-8_7)** — Peeters·Duan·Dimou, EKAW 2026, 10/16 온라인, 심사 완료 | 단일 프롬프트, 순차 에이전트+단계별 Design-by-Contract, 사후 SHACL 수리를 비교. CIDOC-CRM/CACAO 기반 HeritageKGBench 공개 | Text2KGBench에서는 사후 SHACL이 F1 0.562→0.585로 복구했지만, 30개 박물관 텍스트의 복합 사건 그래프에서는 모든 방법이 F1≤0.06. 단계별 gate는 10개 중 9개 영역을 최대 37% 악화시키고, 에이전트 산출물 40%가 파싱 불가. | 작은 문화유산 표본이며 산업문서와 분포가 다르다. **[연결 추론]** “트리플 생성 후 SHACL”만 평가하지 말고 사건 재구체화, 시간·근거·주관성 누락률을 별도 지표화해야 한다. |
| **[NIKG](https://arxiv.org/abs/2610.26528)** — Nowara·Manzour·Elias, v1 10/19, SKILLED-LLMs 2026 출판, [DOI](https://doi.org/10.48550/arXiv.2610.26528) | nuScenes에서 OWL 스키마와 인스턴스를 하나의 Turtle 그래프로 생성. ego-relative motion, 공간구성, TTC 위험을 명시적 관계로 표현 | nuScenes mini 10개 scene, 404 keyframe, 18,538 scene-participant, 211,335 triples. 세 의미 일관성 규칙 99.9%, 89.2%, 99.9%; 다음 프레임 운동 일관성 92.5%. 코드·OWL·평가 스크립트 공개. | nuScenes mini만 평가했고 실제 의도예측 성능은 측정하지 않았다. **[연결 추론]** Protégé 기반 스키마–인스턴스 병합, SHACL/규칙 검증, 문서별 provenance 실습의 좋은 템플릿이다. |
| **[RANGER](https://arxiv.org/abs/2610.28010)** — Mikhaylov 외, v1 10/20, 프리프린트, [DOI](https://doi.org/10.48550/arXiv.2610.28010) | Transformer 정책이 KG를 탐색하고 LLM mentor의 의미 기반 보상으로 GRPO 학습 | HotpotQA·TriviaQA·DiaASQ KG, 각 150문항 평가. HotpotQA 그래프 71,335노드/195,614엣지 등. GRPO hybrid의 LLM-judge 점수는 WaterCircles 대비 HotpotQA 0.673→0.810; TriviaQA 0.850→0.887. | 매우 작은 평가 샘플, LLM-judge 의존, 단순 질의를 합성해 학습. **[연결 추론]** 온톨로지 추론 경로를 agent action space로 두되 mentor 보상과 논리 검증 보상을 분리해야 한다. |
| **[ChronoSynth](https://arxiv.org/abs/2610.29339)** — Liang 외, v1 10/21, 프리프린트, [DOI](https://doi.org/10.48550/arXiv.2610.29339) | temporal KG→질문 생성에서 답 필드·시간조건·참조 사건·순서를 Temporal Intent State로 고정하고 패턴 메모리와 검증 피드백으로 수정 | CRONQUESTIONS·MultiTQ에서 기존 방법 대비 최고 성능을 보고하고 구성요소 절제를 수행. 원문 초록에는 정확한 분할·수치가 요약되어 있지 않다. | 역방향인 graph→text 작업이며 공개 코드 링크가 확인되지 않았다. **[연결 추론]** 사용자의 sentence→logic 시스템을 왕복 검사하는 `text→graph→question` consistency 평가에 활용 가능하다. |
| **[Kontrast](https://doi.org/10.1007/978-3-032-41614-8_5)** — Wei·Ehrhart·Troncy, EKAW 2026, 10/16 온라인, 심사 완료 | 텍스트·표·KG 사이의 직접 충돌, 세분성, 시간 변화, KG 불완전성을 분류하고 Text-to-SPARQL+LLM으로 설명 | 여러 Table-QA 자료에서 교차 모달 불일치가 흔함을 보고. 공개 초록에는 표본 규모와 지표 수치가 충분히 제시되지 않았다. | 전체 평가표 확인에는 출판 원문 접근이 필요하다. **[연결 추론]** 견적표·서술문·Protégé 트리플 간 모순을 검출하는 품질관리 계층에 적합하다. |
| **[On the LLM Verification for Argument Graph Generation](https://arxiv.org/abs/2610.27361)** — Bąba·Chudziak, v1 10/19, CIKM GaLM 워크숍 채택 | 결정적 구조 검사→solver→LLM review→불확실 시 debate→인간 검토의 계층형 검증 | 인위적 결함을 넣은 인간 주석 논증 그래프에서 LLM은 높은 recall을 보였지만 올바른 그래프 약 10%에도 이의를 제기하고 동일 입력 판정이 불안정하며 정확 검사보다 느렸다. | 작은 구조 결함 실험이며 의미 정확성 일반화는 미확인. **[연결 추론]** RDF 구문, SHACL, reasoner 검사를 LLM critic보다 선행해야 한다. |

### B. 자연어→논리·신경기호 검증

| 연구·상태 | 핵심 기여·평가 | 한계 및 연결 |
|---|---|---|
| **[SpecRepair](https://doi.org/10.1007/978-3-032-40121-2_4)** — Liu 외, ISoLA 2026, 10/17 온라인, 심사 완료 | 자연어 요구사항→intent model→LTL→Strix realisability 검사→counterstrategy 설명→자연어 수정을 전문 에이전트들로 연결. 전문가 검토 벤치마크·프로토타입·결과를 Zenodo에 공개하고 direct LLM→LTL 기준선과 비교했다. **[연결 추론]** Transformer 문장→논리 변환을 정답 문자열이 아니라 solver 실행 가능성, 반례 적절성, 수정 후 보존성으로 평가할 수 있다. |
| **[SLoSa](https://arxiv.org/abs/2610.28955)** — Xu 외, v1 10/20, 프리프린트 | 고전 planner·teacher LLM·formal verifier로 PDDL 데이터를 만들고, SFT 뒤 verifier-reward RL을 수행. 4개 PDDL 도메인, 2개 가정환경, Jetson과 실제 로봇에서 평가; 4B–14B 모델 성공률 70.5–76.0%, INT4 소비전력 17.85–26.41W. **한계:** 안전 보장은 인코딩된 제약에 한정. **연결:** 논리식 구문 정확도 대신 prover/reasoner 통과를 학습 보상으로 쓰는 근거다. |
| **[Toward Safe LLM Agents v3](https://arxiv.org/abs/2608.14590)** — Dantas 외, 최초 6/22, v2 10/17·v3 10/20, ACM CSUR 심사 중 | 6개 DB, 38편 PRISMA 검토. NL→PDDL 의미정확도 24.8–34.2%, 한 연구의 runtime monitor 위험 행동 감소 65.37%, 다른 연구에서는 위험 행동 94% 차단 후 안전한 완료가 대부분 5% 미만. 9개 주장의 7개는 GRADE ‘Very Low’. **연결:** 논리 변환·검증·실행 효용을 별도 축으로 보고해야 한다. |
| **[Towards Robust and Safe Decision-Making Under Uncertainty](https://doi.org/10.1007/978-3-032-40121-2_3)** — Bartocci 외, ISoLA 2026, 10/17 온라인 | model learning→model checking/controller synthesis→RL→runtime testing의 연구 로드맵. 실증 비교보다 관점·통합 프레임워크 논문이다. **연결:** 온톨로지를 설명용 산출물이 아니라 검증 가능한 실행 모델로 다루라는 설계 근거다. |

### C. 멀티에이전트 신뢰·검증

| 연구·상태 | 방법·평가와 주요 결과 | 중요한 한계·연결 |
|---|---|---|
| **[PerMIT](https://arxiv.org/abs/2610.28987)** — Jiang 외, v1 10/20, 프리프린트 | 비신뢰 메모리를 finite interface와 confirmation gate로 격리하고 두 integrity theorem을 Lean 4로 검사. Trojan Hippo의 4개 backbone에서 self/lightweight verifier의 관측 ASR 0%; verifier FPR 3–34%. τ²-bench에서 12/24/60/90 agent, 24 held-out tasks×2회. Sonnet·Kimi의 pooled utility 개선은 각각 +0.1363, +0.1120. | 정리는 명시적 trust assumption과 interface model에 한정되고 Lean artifact는 요청 기반이다. 커뮤니티 크기별 1회 construction이라 population 효과가 불확실하다. **[연결]** 트리플마다 출처·검증자·승인범위·버전을 기록하는 신뢰 레지스트리로 이전 가능하다. |
| **[Proof-Carrying Contracts](https://arxiv.org/abs/2610.28484)** — Ciliberto·Rudi·Tassi, v1 10/20, 프리프린트 | 실행 전 agent가 계약 보존 증명을 제출하고 Airlock이 기계 검사한다. 적대적 agent에서도 모델 내 불변식 보존 정리를 제시한다. | 70쪽의 이론 프레임워크이며 현실 시스템 효용·대규모 실험은 제시되지 않았다. **[연결]** 에이전트가 생성한 온톨지 변경에 proof/check report를 동봉시키는 패턴으로 활용 가능하다. |
| **[CATS](https://arxiv.org/abs/2610.29292)** — Tritthart·Zehle, v1 10/21, 프리프린트 | 실행 trace를 대조해 agent별 기여도를 부여하고 취약한 node/edge를 가지치기. BigCodeBench에서 score-only search 대비 +5.3%p, 배포 token 54% 감소. HotpotQA poisoning 3회 모두 공격 agent 제거. | poisoning 시험이 3회에 불과하고 attribution 자체가 LLM 판단이다. **[연결]** extractor·reasoner·critic의 신뢰도를 전역 팀 점수 대신 구성원별로 추적할 수 있다. |
| **[VerifierBench](https://arxiv.org/abs/2610.28679)** — Yin 외, v1 10/19, 프리프린트 | 6개 agent benchmark에서 222 tasks/4,993 hidden tests, 19 models. 생성 verifier의 normalized balanced accuracy 10.6–62.1; 잘못된 답 거절보다 올바른 대안 답 수용에 특히 취약했다. | 소프트웨어·도구 검증 중심. **[연결]** 온톨로지 검증기도 단일 gold serialization만 통과시키는 과도한 제약을 피해야 한다. |
| **[Who Verifies the Builder?](https://arxiv.org/abs/2610.28667)** — Sion·April, v1 10/16, 프리프린트 | build plane과 assurance plane을 분리. 사전등록된 3개 stateful service와 46개 주입 결함에서 fresh-context verifier가 builder test보다 더 많은 결함 탐지, Holm 보정 p=0.006. 다른 제공자 모델은 추가 탐지를 제공하지 않았다. | 작은 소프트웨어 표본이며 false oracle이 존재. **[연결]** 트리플 생성 모델과 검증 모델·검증 규칙을 분리하고 blind evaluation을 적용한다. |
| **[AgentPolicyForge](https://arxiv.org/abs/2610.28989)** — Shang 외, v1 10/20, 프리프린트 | 실행 환경에서 정책 준수/위반 도구호출을 생성하고 적응형 guard를 학습. 10 policy families, 698 train scenarios, 254 human-reviewed held-out scenarios. 최종 guard가 prompt-only 대비 ASR을 상대 40–44% 감소시키며 정상 요청 거절도 줄였다. | 정책 표현 및 공격 생성기의 범위에 종속. **[연결]** Protégé 규칙을 실행 전 tool/ontology-change guard의 정책원으로 사용할 수 있다. |
| **[ReMAS](https://arxiv.org/abs/2610.28966)** — Jia 외, v1 10/20, 프리프린트 | RL attacker가 요청 재작성과 sub-agent 호출 template을 학습해 MAS의 system prompt를 추출하는 black-box red teaming을 제안. 여러 backend·MAS 구조로 전이를 보고했다. | 공개 초록에 데이터 규모와 절대 ASR 수치가 없어 정량 재검증이 어렵다. **[연결]** 신뢰 agent가 프롬프트·온톨로지 스키마·비공개 문서 URI를 노출하는 공격을 별도 평가해야 한다. |

### 인접하지만 참고할 자료

- **전력망 경보의 KG+BiLSTM+4-agent 시스템**: 356,950개 실경보, F1 96.9%, false alarm 4.2%, hallucination 15.8%→3.1%. 다만 분할 독립성·외부 전력망 일반화는 추가 확인이 필요하다.
- **교통 예측의 CNN-LSTM–XAI–Formal Concept Analysis**: 18개 요금소, 53개월, 73,891개 관측에서 neural attribution을 concept lattice와 규칙으로 변환한다.

---

## 4. 직접 관련성이 높은 3건의 적용 설계

### 4.1 AgentOnto → 제조·투자엔지니어링 온톨로지

**적용 단계**

1. 문서·표·DB를 `E: 엔터티/관계`, `M: 계산·판정 규칙`, `G: 원문·열·SPARQL/SQL 매핑`으로 분리한다.
2. 모든 항목에 출처 위치, 문서 버전, 확인 상태를 붙인다.
3. 분석 요청을 `실행 / 추가질문 / 지원 불가`로 먼저 분류한다.
4. 계획이 온톨로지의 정의·단위·적용조건과 일치할 때만 계산한다.
5. 온톨로지 변경마다 correction test와 retention test를 함께 수행한다.

**필요 자료:** 현재 Transformer 추출기, Protégé OWL, 설계문서·견적표, gold competency questions. AgentOnto 구현은 공개 확인되지 않아 자체 재구현이 필요하다.

**최소 검증 실험:** 60개 요청—30 실행 가능, 15 모호, 15 지원 불가. `직접 LLM/Transformer`, `온톨로지를 프롬프트에만 제공`, `계획-검사-실행 방식`을 비교한다. 지표는 action accuracy, result exact match, silent semantic error, SHACL 위반, 비용·지연이다.

### 4.2 HeritageKGBench → 문장→온톨로지 트리플

**적용 단계**

1. 최소 100개 산업 문장에서 약 300–500개 gold triples를 전문가가 작성한다.
2. 다음 세 조건을 비교한다: 단일 추출, 단계별 agent+gate, 단일 추출+사후 SHACL repair.
3. 단순 SPO 외에 사건, 시간, 측정값·단위, 주장자, 근거 문서까지 재구체화한다.
4. 단계별 gate가 빈 그래프를 만드는지 기록한다.

**최소 지표:** micro/macro triple F1, Turtle parseability, SHACL validity, event-mediation completeness, provenance accuracy, near-empty graph rate.

**핵심 가설:** 사후 SHACL은 형식·국소 제약은 복구하지만, 처음부터 누락된 사건이나 관계는 복원하지 못한다. 이는 원 논문의 강한 부정적 결과에서 도출한 **[연결 추론]**이다.

### 4.3 PerMIT → 멀티에이전트 온톨로지 신뢰 계층

**적용 단계**

1. agent가 추출한 트리플을 곧바로 trusted KG에 넣지 않고 quarantine graph에 저장한다.
2. gate에는 정확한 트리플, 근거 문장, 문서·페이지, 생성 agent, 예정된 사용 범위를 표시한다.
3. 승인된 내용만 trusted named graph로 승격하고 서명된 verdict를 남긴다.
4. 다른 agent는 내용 자체가 아니라 `승인된 handle`을 통해서만 민감 작업에 사용한다.
5. 반복적으로 승인되는 동일 내용은 범위가 같은 경우에만 재사용한다.

**최소 실험:** 정상 20건+간접 프롬프트 주입 20건을 2개 세션에 걸쳐 실행한다. raw shared memory, prompt filter, gated memory를 비교해 ASR, benign FPR, task completion, 사람 검토 횟수, 오래된 승인 재사용 오류를 측정한다.

---

## 5. 교육공학적 적용 검토

**중요:** 조사한 논문들은 교육 효과를 실험한 연구가 아니다. 다음 설계와 학습성과는 전부 **교육적 제안 [연결 추론]**이며, 논문이 입증한 시스템 성능과 구별해야 한다.

| 연구 | 대상·사전지식 | 관찰 가능한 목표와 활동 | 평가·오개념 피드백 |
|---|---|---|---|
| AgentOnto | 대학원생/데이터 엔지니어; RDF·SQL | 동일 업무요청을 schema-only와 ontology-guided 방식으로 처리하고 silent error를 분류 | plan–ontology–query 추적표 루브릭. “SQL 실행 성공=의미 정확” 오개념에는 반례 제공 |
| HeritageKGBench | KG/NLP 수강생; SHACL | 한 문단을 flat triple과 event-reified graph로 각각 변환 | triple F1+사건완전성. “SHACL 통과=원문 충실”에는 누락 사건 사례로 피드백 |
| NIKG | 학부 고학년; OWL·Python | TTL에서 TBox/ABox와 세 관계를 찾아 의미 규칙을 검사 | SPARQL 결과와 논문 통계 비교. “결측 triple=오류”에는 emission 조건 확인 |
| RANGER | 대학원생; RL·graph search | heuristic reward와 semantic reward의 retrieval path를 비교 | 경로 적합성·정답률·비용. “LLM 보상=정답”에는 작은 mentor의 false-positive 결과 제시 |
| ChronoSynth | NLP/KG 수강생 | 시간조건을 바꾸지 않고 KG→질문 생성 | answer set 보존 여부. 유창성만으로 채점하지 않음 |
| Kontrast | 데이터 품질 교육 | 표·본문·KG의 불일치를 네 유형으로 분류 | 유형 정확도와 설명 근거. temporal update와 직접 모순을 구분하도록 피드백 |
| Argument-graph verification | 논증·AI 수강생 | cycle 검사와 LLM critic을 비용·안정성 면에서 비교 | 반복판정 일치도. “LLM이 더 지능적이므로 구조검사도 우월” 반례 |
| SpecRepair | 소프트웨어공학 대학원생; LTL | NL 요구를 LTL로 만들고 Strix 반례로 수정 | realisability와 의미보존 루브릭. “satisfiable=realisable” 구분 |
| SLoSa | 로보틱스/AI | verifier reward가 성공·안전에 미치는 영향 설명 | 성공률과 제약 위반을 별도 채점 |
| PerMIT | 보안/멀티에이전트 | trusted/untrusted flow와 gate 위치를 threat model로 설명 | 공격 성공·정상거절·검토비용 3축. “ASR 0=완전 안전”에는 표본·가정 지적 |
| PC2 | 형식방법 수강생 | 계약, proof obligation, Airlock을 상태전이로 모델링 | 불변식 증명 개요. “증명=현실세계 안전”에는 model–world gap 피드백 |
| CATS | MAS 수강생 | agent 제거 전후 정확도·비용·poisoning을 분석 | credit calibration과 3-run 한계 포함 |
| VerifierBench | SE/AI 평가 수강생 | verifier에 하나의 정답과 여러 동등 정답을 통과시키기 | balanced accuracy와 false rejection. “모두 거절하는 verifier가 안전” 오개념 교정 |
| Independent Assurance | 소프트웨어 테스팅 | builder와 verifier의 context를 분리해 mutation test 수행 | seeded-fault detection과 false oracle 동시 채점 |
| AgentPolicyForge | AI 보안 | 허용된 도구의 잘못된 인자·자원·문맥을 판별 | ASR/FPR trade-off. tool allowlist만으로 충분하다는 오개념 교정 |
| ReMAS | 보안 대학원생 | multi-agent prompt-extraction threat tree 작성 | 범위·재현성·방어책 루브릭 |
| Safe-agent survey | 연구방법론 | 근거 수준과 수치를 GRADE 기준으로 비판 | 주장마다 연구 수·도메인·certainty를 표시하도록 채점 |

---

## 6. 한국어 미니 튜토리얼: NIKG를 Protégé와 검증 스크립트로 살펴보기

### 출처와 버전

- 논문: arXiv:2610.26528v1, 2026-10-19
- 코드·OWL·평가자료: [공식 GitHub 저장소](https://github.com/KhaledNowara/nuScenes-Intention-Knowledge-Graph)
- 저장소에는 Python 3.11 환경, OWL/Turtle, 생성기, 통계·일관성 검사 및 사전 생성 사례가 포함된다. 코드 MIT, 생성 그래프와 이미지는 nuScenes의 CC BY-NC-SA 조건을 따른다.
- **실행 상태:** 아래 절차는 원문과 README를 대조해 작성했지만 이번 브리핑 작성 환경에서는 nuScenes 데이터를 내려받아 실제 실행하지 않았다.

### 개념

NIKG는 다음 두 층을 한 Turtle 파일에 합친다.

- **TBox:** `SceneParticipant`, `SpatialZone`, `TTCRiskLevel` 등의 클래스·속성·열거값
- **ABox:** 각 장면·프레임·참여자와 `motionTowardEgo`, `spatialConfiguration`, `ttcRisk` 사실

논문에서 수행한 “semantic consistency”는 OWL reasoner의 자동 분류 결과가 아니라 RDF 트리플을 스캔해 세 가지 implication의 통과율을 계산한 것이다.

### 준비물

- Python 3.11와 Conda 또는 pip
- [nuScenes mini](https://www.nuscenes.org/) 사용 동의 및 데이터
- Git
- 선택 사항: Protégé 5.x

### 재현 절차

```bash
git clone https://github.com/KhaledNowara/nuScenes-Intention-Knowledge-Graph.git
cd nuScenes-Intention-Knowledge-Graph

conda env create -f environment.yml
conda activate exp006
```

nuScenes mini를 준비한 뒤 다음을 실행한다.

```bash
python main.py \
  --dataroot /path/to/nuscenes \
  --version v1.0-mini \
  --ontology ontologies/ontology.ttl \
  --out-ttl graphs/multi_scene.ttl \
  --out-sparql graphs/multi_scene.sparql
```

TTL만으로 가능한 검사를 먼저 수행한다.

```bash
python evaluation/kg_stats.py \
  --ttl graphs/multi_scene.ttl

python evaluation/semantic_consistency.py \
  --ttl graphs/multi_scene.ttl
```

원 데이터와 다음 프레임을 대조하려면 다음을 추가한다.

```bash
python evaluation/motion_forward_check.py \
  --dataroot /path/to/nuscenes \
  --version v1.0-mini
```

Protégé에서는 `ontologies/ontology.ttl`을 먼저 열어 TBox를 보고, 이후 `graphs/multi_scene.ttl`을 별도 프로젝트로 열어 인스턴스를 확인한다. 대형 파일 로딩이 부담스러우면 README의 `--scenes`와 `--max-keyframes` 옵션으로 작은 그래프부터 생성한다.

### 예상 출력과 판정 기준

전체 nuScenes mini를 같은 조건으로 처리했다면 논문 기준은 다음과 같다.

- 총 211,335 triples
- 404 keyframes
- 911 unique participants
- 18,538 SceneParticipant instances
- 의미 일관성:
  - `High TTC → Approaching`: 1,988/1,990, 99.9%
  - `High TTC → forward zone`: 1,688/1,892, 89.2%
  - `Stationary → not High TTC`: 3,782/3,784, 99.9%
- 다음 프레임 운동 일관성: 16,746 transitions 중 92.5%

수치가 다르면 먼저 데이터 버전, scene 필터, keyframe 제한, ontology 파일 및 코드 commit을 확인한다.

### 검증 질문과 정답 기준

1. **왜 첫 등장 participant에는 `motionTowardEgo`가 없을 수 있는가?**  
   정답: 이전 keyframe과의 거리 변화가 필요하기 때문이다.

2. **`ttcRisk=High`인데 forward zone이 아닌 사례는 모두 그래프 오류인가?**  
   정답: 아니다. TTC가 경로가 아닌 line-of-sight 평면거리로 계산되어 측면·후방 접근이 포함될 수 있다.

3. **SHACL·일관성 검사 통과는 의도예측 모델의 정확도를 입증하는가?**  
   정답: 아니다. 스키마·관계의 내부 일관성과 downstream predictive validity는 다른 평가다.

4. **Protégé reasoner가 99.9% 통과율을 계산해 주는가?**  
   정답: 논문의 수치는 제공 평가 스크립트의 implication 검사 결과다. OWL reasoner 결과와 혼동하면 안 된다.

### 평가상 주의점

- nuScenes mini에만 맞춘 수치이며 다른 데이터셋 일반화가 검증되지 않았다.
- 50m 공간 범위, 0.5m 정지 임계값 등은 코드에 고정되어 있다.
- 실제 의도예측 성능이나 인과적 안전 개선은 평가하지 않았다.
- 사용자의 산업문서 연구로 이전할 때는 `motion/TTC` 대신 `문서상태/설계성숙도/비용위험`을 관계로 바꾸고, 각 관계의 emission condition과 미기재 사유를 명시해야 한다.

## 7. 향후 제공 작업을 더 구체화하는 권장 방식

다음 주부터는 결과물을 다음처럼 고정하면 연구용으로 더 유용하다.

- 관련성을 **A: 즉시 실험 가능 / B: 방법 전이 가능 / C: 배경자료**로 등급화
- “새 논문”과 “실질 개정판”을 분리하고 개정판은 **무엇이 바뀌었는지**만 보고
- 코드·데이터 상태를 `공개/부분공개/요청필요/미공개`로 명시
- 결과값마다 `저자 보고값`, `독립 재현값`, `본 브리핑 미실행`을 구별
- 교육 설계는 논문별로 학습목표 하나, 실습 하나, 평가 문항 하나만 유지
- 사용자 연구 연결은 매주 최소 한 건씩 다음 중 하나로 끝내기:
  - Protégé에서 바로 시험할 competency question
  - 문장→논리/트리플 gold 사례
  - 멀티에이전트 공격·신뢰 최소 실험
  - AACE/엔지니어링 문서용 온톨로지 변경 제안

이번 주의 우선 실행 순서는 **HeritageKGBench 방식의 추출 오류 진단 → AgentOnto식 계획·갱신 계층 → PerMIT식 신뢰 gate**가 가장 합리적이다.