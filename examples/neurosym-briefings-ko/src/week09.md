# 신경·기호 AI 주간 연구·교육 브리핑

## 1. 검색 범위

- **검색 기준일:** 2026-11-20
- **대상 기간:** 2026-11-13 00:00–11-19 23:59
- **검색원:** arXiv `cs.AI`, `cs.CL`, `cs.LG`, `cs.LO`, `cs.MA`, `cs.CR`, Nature Communications, ACL Anthology, Springer·MDPI·IEEE/ACM 색인, 논문이 연결한 GitHub·Zenodo
- **검색식**
  - `(ontology OR OWL OR taxonomy) AND (LLM OR neural OR agent)`
  - `("logical form" OR "text-to-logic" OR formalization OR "constraint model") AND LLM`
  - `("knowledge graph" OR KGQA) AND (reasoning OR verification OR retrieval)`
  - `("multi-agent" OR agentic) AND (trust OR authorization OR provenance OR verification OR audit)`
- **중복 통합:** 제목·저자·DOI가 같은 출판사/arXiv 판본은 출판 판본 우선
- **제외**
  - 최초 공개·실질 개정일이 기간 밖인 자료
  - 순수 KG 임베딩 및 일반 RAG 논문
  - 협업 성능만 평가하고 신뢰·검증을 다루지 않은 멀티에이전트 논문
  - 메타데이터만 바뀌고 실험·방법 변경이 확인되지 않은 v2
- **확인 결과:** 직접 관련 10건. 전용 **OWL/Protégé 온톨로지 생성 논문은 미발견**했으며, 자연어→형식표현에서는 constraint-programming 모델 생성이 가장 가까운 연구였다.
- `AutoOntic`은 11월 11일, `Trusting Trust in AI Software Engineering Agents`는 최초 공개가 9월 19일이므로 제목·arXiv 번호가 최근처럼 보이더라도 제외했다. 11월 19일 늦은 제출물은 색인 지연 가능성이 있어 다음 회차에서 소급 확인할 필요가 있다.

아래에서 **[사실]**은 원문·메타데이터, **[저자]**는 저자가 보고한 결과, **[연결]**은 사용자 연구에 대한 해석이다.

---

# 2. 논문·기술 보고서 목록

## 1) CPAM-LLM: Automated Data-to-Model Transformation for Constraint Programming

- **저자·기관:** Zhengqi Shi, Jin Huang, Xinyu Li 외; Huazhong University of Science and Technology
- **공개:** 2026-11-19, *Nature Communications*
- **심사:** 동료심사 완료, 오픈 액세스
- **DOI:** [10.1038/s41467-026-78715-2](https://doi.org/10.1038/s41467-026-78715-2)
- **기여·방법 [사실]:** 자연어 최적화 문제를 실행 가능한 constraint-programming 모델로 변환한다. formal concept analysis 기반 RAG, 구조 검증, chaos-mapping 데이터 증강, 변화한 요구사항에 대한 동적 제약 갱신을 결합한다.
- **평가 [사실]:** DNA 서열 설계, 재구성형 에너지 저장장치, 무인차량 물류 등을 포함한 5개 시나리오. 공개 색인에서 정확한 분할·기준선·수치표는 확보하지 못했다.
- **결과 [저자]:** 다섯 도메인에서 데이터→형식모델 파이프라인과 요구사항 변화에 대한 적응 가능성을 보고했다.
- **한계:** 접근 가능한 초록만으로는 모델별 성능, 실행 성공률, solver-equivalence를 검증할 수 없다. 재현 코드 링크도 확인되지 않았다.
- **연결:** 사용자 연구의 `문장 → 논리 표현`을 단순 문자열 exact match 대신 **실행 가능성·충족가능성·정답 동치성**으로 평가하는 근거가 된다.

## 2) NeSySy: Synthetic Neurosymbolic Task Generation with Controlled Constraint Complexity

- **저자:** Mykhailo Buleshnyi, Zsolt Zombori, Michael Benedikt
- **공개:** 2026-11-14 v1
- **심사:** arXiv 자체는 미심사. Zenodo에서 TACAS 2027 artifact로 명시
- **원문·자료:** [arXiv](https://arxiv.org/abs/2611.19597), [Artifact v1.0](https://doi.org/10.5281/zenodo.23640674)
- **기여·방법:** CNFgen·Z3가 SAT/SMT 제약을 만들고, RC2 MaxSAT 또는 Z3 OMT가 비일관 출력의 최소 수정을 계산한다. Boolean·실수 제약, 입력 의존 제약, distant supervision을 지원한다.
- **평가 설계:** 기본 3,000개 generator 학습점, 생성 데이터 5,000개, 70/10/20 분할, 데이터 seed 5개×학습 seed 5개. Base, BaseSolver, DRL, CCN+, BaseSeq, DeepProbLog을 accuracy·violation rate·MAE로 비교한다. supervision-size 실험은 총 20,000개와 학습표본 80–16,000개를 사용했다.
- **결과:** solver 기반 최소 수정이 복잡한 조건에서도 안정적이었다. fixing 방식은 filtering보다 다양한 동시에 어려운 데이터를 만들었고, hidden 1,024 조건의 Base accuracy가 filtering .8515, fixing .5821이었다.
- **한계:** 실제 문서나 온톨로지가 아닌 합성 제약 중심이다. 정수·시계열·표본 간 제약은 미지원이며 비교한 신경·기호 시스템도 제한적이다.
- **연결:** Transformer가 출력한 논리식의 난이도와 위반율을 독립적으로 통제하는 **회귀시험 생성기**로 사용할 수 있다.

## 3) GRASP: Query-Adaptive Graph Retrieval with Path-Sufficiency Verification

- **저자:** Rui Xu, Le Wang, Tianyue Wang
- **공개:** 2026-11-14 v1
- **심사:** 미심사 프리프린트
- **원문:** [arXiv](https://arxiv.org/abs/2611.19441)
- **방법:** query–edge cross-attention, 적응형 stopping gate, 경로 충분성 분류기, 불충분한 경로의 국소 재검색을 결합한다.
- **평가:** RiTeK 3,500/1,500/100, MedKGent-KG 672/288/100, PMC 3,500/1,500/100. MedKGent는 15.6만 개체·297만 트리플이다. BFS-2/3, G-Retriever, GNN-RAG, MINERVA와 Hits@1/3, MRR, Path Recall, unsupported-claim rate로 비교하고 5 seed와 10,000회 bootstrap을 적용했다.
- **결과:** GRASP의 Hits@1은 RiTeK 85.2, MedKGent 76.8로 MINERVA보다 10.0·10.4%p 높았다. unsupported-claim rate는 세 데이터셋에서 8.9–13.2%p 감소했다. 다만 국소 재검색의 전체 정확경로 복구율은 38.5%였다.
- **한계:** 생의학 도메인, 테스트 각 100문항으로 작다. NLI 기반 unsupported 판정은 인간 검증 F1이 클래스별 약 .70–.86이며 형식 증명이 아니다.
- **연결:** Protégé KG에서 검색된 경로가 질문에 충분한지 판단한 뒤, 충분한 경로만 Transformer 답변에 제공하는 gate로 적용할 수 있다.

## 4) ACaM: Automated Capability Modeling for Agentic AI Security

- **저자·기관:** Monika Santra 외; Penn State, IBM Research
- **공개:** 2026-11-17 v1
- **심사:** 미심사 프리프린트
- **원문:** [arXiv](https://arxiv.org/abs/2611.23507)
- **방법:** agent/tool Python 코드를 정적 분석해 Agent Capability Property Graph를 만든다. 정적 분석이 확정한 사실은 LLM이 낮추거나 덮어쓸 수 없고, LLM은 코드 구조만으로 결정할 수 없는 의미 판정만 보충한다.
- **평가:** 실제 agent 43개, 그중 MAS 9개. 수작업 주석 24개에서 capability macro-F1, 삽입된 위협 경로에서 chain reconstruction, 실제 코드에서 PoC를 평가했다.
- **결과:** capability macro-F1 98.3%, 위협경로 점수 .980으로 최강 LLM-only 기준선 .903보다 약 8%p 높았다. 123개 code-execution/credential-exposure 경로와 약 1,800개 중·고위험 경로를 찾고 10개를 PoC로 확인했다.
- **한계:** Python white-box 분석에 한정되고, 동적 코드·reflection·원격 black-box 도구는 범위 밖이다. worst-case taint 전파로 오탐이 발생할 수 있다. 코드 공개 링크는 원문에서 확인하지 못했다.
- **연결:** RE:CHARGE의 Calculator·Policy Engine·DB tool이 “설명상 무엇을 하는가”가 아니라 **코드상 무엇에 접근·기록·전송할 수 있는가**를 graph로 사전 감사하는 방식이다.

## 5) TRACE-MAS: Diagnosing and Repairing Collaboration Failures

- **저자:** Zekai Chen 외
- **공개:** 2026-11-17 v1
- **심사:** 미심사 프리프린트
- **원문:** [arXiv](https://arxiv.org/abs/2611.23362)
- **방법:** 정상 trajectory에서 agent state·message transition·task dependency의 실행 contract를 학습하고, partial-order event graph에서 이상 위치와 실제 원인을 구분해 최소 수정을 선택한다.
- **평가:** GSM8K, CSQA, HotPotQA, InjecAgent, PoisonRAG; L1–L3 공격. Oracle, BlindGuard, G-Safeguard, AcMAS, A-Trust와 trajectory F1/AUROC, 원인 Hit@1·거리, task recovery를 비교한다.
- **결과:** 모든 benchmark×attack-level 셀에서 최고 F1, 최강 기준선 대비 셀 평균 +15.5%p. 저자는 root-cause localization이 60.2% 개선됐다고 보고한다.
- **한계:** 정상 trajectory의 대표성에 의존하고, 새 업무·새 topology가 정상 변화인지 공격인지 구분하기 어렵다. 공개 코드 링크는 확인되지 않았다.
- **연결:** 트리플 오류가 발견된 마지막 agent만 탓하지 않고, 잘못된 원문 전달·변환·승인 중 최초 원인을 event graph에서 찾는 데 적합하다.

## 6) Agent Trust Infrastructure — ATI

- **저자:** Viet K. Nguyen, Mohammad I. Husain
- **공개:** 2026-11-17 v1
- **심사:** 미심사 프리프린트
- **원문·코드:** [arXiv](https://arxiv.org/abs/2611.23202), [GitHub](https://github.com/CalPolyPomonaCS/Agent-Trust-Infrastructure-ATI-Official)
- **방법:** 조직별 AgentCA, PKI, Zero Trust, WIMSE token, Entity Attestation Token으로 agent identity와 model/tool/system-prompt 구성을 확인한다.
- **평가:** 8개 조직·6개 프레임워크·조직별 5-agent team. 보안 실험은 2개 조직, 공격 14종·정상 6종, 5개 agent model, 공격별 5변형×3회.
- **결과:** 전체 enforcement 적용 시 공격 containment 43→84%, 요청당 오버헤드 약 174μs.
- **한계:** simulated federation이며 판정에 judge-model panel을 사용한다. 인증된 구성의 런타임 행동이 안전하다는 보장은 없다.
- **연결:** 다른 팀·협력사 agent가 BOE나 원가 데이터를 요청할 때 identity, 승인된 tool configuration, 요청 권한을 별도 검증하는 L6 Governance 구현 후보이다.

## 7) Evaluating Authorization and Trust Boundaries in Agentic Orchestration Frameworks

- **저자:** Sahaya Jestus Lazer, Kshitiz Aryal, Maanak Gupta, Elisa Bertino
- **공개:** 2026-11-16 v1
- **심사:** 미심사 프리프린트
- **원문:** [arXiv](https://arxiv.org/abs/2611.21259)
- **평가:** LangChain, LangGraph, AutoGen, OpenClaw, 공통 `gpt-4o-mini`, OWASP Agentic Top 10에 매핑한 12개 공격 실험.
- **결과:** unauthorized tool chaining과 symlink TOCTOU는 네 프레임워크 모두 취약했다. 위임·감사로 위장한 prompt injection은 LangChain·LangGraph·OpenClaw에서 권한 없는 도구 호출을 유발했다. canonical path/sandbox를 둔 traversal 공격은 네 구성 모두 차단했다.
- **한계:** 공격별 소수 deterministic trial이고 공통 모델 하나를 사용해 프레임워크와 모델 효과를 분리하기 어렵다.
- **연결:** tool 보유 권한과 특정 task에서의 tool 사용 권한을 분리하고, 파일 경로는 검사 시점이 아니라 실제 접근 시점에 재검증해야 한다.

## 8) Aligning AI Teams

- **저자·기관:** Siddarth Srinivasan, Morgan Jane Matthews, Jascha Sohl-Dickstein, Erik Jones; Harvard, Constellation Institute, Anthropic
- **공개:** 2026-11-13 v1
- **심사:** 미심사 프리프린트
- **원문·코드:** [arXiv](https://arxiv.org/abs/2611.17820), [실험](https://github.com/safety-research/aligning-ai-teams), [magelab](https://github.com/sidsrinivasan/magelab)
- **평가:** Anthropic 모델 5종. Sepsis 400/100, fake-news recommender 359/90, consulting task 10종. 단일 agent와 PM+coder 8명의 팀, group chat·review·safety lead·safety document 등을 비교하며 셀당 중앙값 약 30회 실행했다.
- **결과:** sepsis에서 team safety가 단일 agent보다 최대 약 59%p 낮았다. 일반 review와 group chat은 일관되게 회복시키지 못했으며, **safety document+지정 safety lead**가 가장 안정적으로 단일-agent 범위까지 회복시켰다.
- **한계:** 한 회사의 모델군 중심, 의도적으로 양립 불가능한 목표, transcript 판정에도 LLM을 사용했다.
- **연결:** 모든 agent에게 공동 책임을 부여하기보다, 전체 추론·승인 경로를 검사할 독립 Safety/Assurance Lead를 지정하는 편이 타당하다.

## 9) FinVerify: A Verification Framework for Financial Agents

- **저자:** Mao Guan, Qian Chen, Ge Meng, Xiao-Yang Liu
- **공개:** 2026-11-16 v1
- **심사:** NeurIPS 2026 *Who Verifies the Agents?* 워크숍 채택
- **원문:** [arXiv](https://arxiv.org/abs/2611.20423)
- **방법:** 시간 무결성, 출처 충실성, 비교 가능성, 회계 일관성, 재무모델 충실성의 5개 protocol. LLM은 claim과 근거를 구조화하고 deterministic validator·Z3가 판정하며 증거 부족 시 abstain한다.
- **평가:** Agent Finance Reasoning 357, FinQA 600, TAT-QA 600, FinanceBench-67, XBRLFiling 600. Direct 및 zero-shot LLM judge와 precision·accuracy·coverage를 비교했다.
- **결과:** Agent Finance Reasoning precision 76.7%, coverage 81.2%로 judge의 56.4%/99.7%보다 precision은 높지만 abstention도 많았다. XBRLFiling precision 99.8%, accuracy 97.0%.
- **한계:** FinVerify만 추가 SEC·XBRL 자료를 읽어 동일 근거 조건의 비교가 아니다. protocol별 ablation도 없다.
- **연결:** CAPEX 계산이 실행됐다는 사실만 보지 말고 기준시점·단위·스코프·공식 실적 근거·계산식 버전을 함께 검증해야 한다.

## 10) FutureBench: Knowledge–Context Conflict

- **저자:** Yi-Cheng Lai, Hen-Hsen Huang
- **공개:** 2026-11-17 v1
- **심사:** 미심사 프리프린트
- **원문:** [arXiv](https://arxiv.org/abs/2611.23601)
- **방법·평가:** timestamped question, 참·거짓·통제 passage triplet, no-context probe로 3,629문항·6개 모델을 평가한다. 별도 902개 post-cutoff 질문에서 네 prompt를 비교했다.
- **결과:** 검증과 passage 우선권을 한 prompt에 넣으면 pre-cutoff 정답을 거짓 passage로 대체하는 현상이 다섯 모델 모두에서 증가했다. adversarial-aware prompt는 밀려난 정답의 82.5–98.9%를 복원했다.
- **한계:** 사실 QA 중심이며 KG·온톨로지 추론을 직접 수행하지 않는다. 모델 내부 지식이 맞는 경우와 최신 외부 근거가 맞는 경우의 정책이 다르다.
- **연결:** “검색 문서를 무조건 우선하라”가 아니라 승인일·revision·source authority에 따라 외부 근거와 기존 온톨로지의 우선순위를 결정해야 한다.

---

# 3. 직접 적용 우선순위 3건

## A. CPAM-LLM → 문장·요구사항을 실행 가능한 논리 모델로 변환

**권장 적용 단계 [연결]**

1. 원문을 `Entity–Variable–Domain–Constraint–Objective–SourceSpan` 중간표현으로 변환한다.
2. 온톨로지에서 단위·설비유형·공정·적용 규칙을 검색한다.
3. 중간표현을 OWL axiom, SHACL 또는 Z3/CP-SAT 식으로 결정적으로 컴파일한다.
4. syntax, satisfiability, 단위, 범위, 공식 계산 결과를 각각 검사한다.
5. 실패 시 전체 재생성 대신 실패한 constraint와 원문 span만 수정한다.

**필요 자료**

- CAPEX·설계 규칙 50개 이상
- 수작업 정답 중간표현과 OWL/Z3 모델
- Protégé/HermiT 또는 Pellet
- Z3 또는 OR-Tools
- 문서·revision·page/section/offset provenance

**최소 검증 실험**

- 문서가 겹치지 않도록 프로젝트 단위 분할
- 최소 200문장, 50개 실행 모델
- 비교: 직접 LLM → schema-constrained → schema+compiler+solver
- 지표: entity/relation F1, 실행 성공률, satisfiable rate, competency-question 정확도, 계산결과 동치율, 잘못 승인된 constraint 비율

## B. GRASP → 온톨로지 경로 충분성 Gate

1. 질문에서 예상 답 유형과 시작 개체를 찾는다.
2. relation 후보를 질문 token과 cross-attention으로 점수화한다.
3. 매 hop에서 계속 탐색할지 중단할지 판정한다.
4. 완성 경로가 질문의 모든 조건을 지지하는지 검사한다.
5. 불충분하면 가장 약한 hop으로 돌아가 다른 relation을 선택한다.
6. 충분성 검사를 통과한 경로만 답 생성기와 BOE에 제공한다.

**최소 실험**

- 실제 RE:CHARGE competency question 100개
- 프로젝트 3개 이상, 프로젝트 독립 분할
- BFS, vector retrieval, 고정 2-hop, adaptive+gate 비교
- Hits@1, Path Recall, CQ 정확도, unsupported claim, 평균 탐색 edge 수, latency 측정

**중요 주의점:** GRASP의 NLI 검증을 OWL entailment와 동일시해서는 안 된다. 명시적 공리는 HermiT가, 문장 근거의 의미적 지지는 NLI/LLM이 담당하도록 분리한다.

## C. ACaM → 멀티에이전트 Capability Graph

1. FastAPI route, calculator, DB client, 파일 처리기, 외부 API를 tool/component로 식별한다.
2. 환경변수·DB·파일·메시지·외부 네트워크를 conduit로 모델링한다.
3. `PUBLIC–INTERNAL–SECRET`와 `UNTRUSTED`를 분리 추적한다.
4. 정적 분석이 확정한 read/write/network 사실은 LLM이 완화하지 못하게 한다.
5. 여러 tool을 거치는 `read historical cost → shared state → report export` 경로를 분석한다.
6. 권한정책은 위험 경로와 대조해 배포 전 차단하거나 HITL 대상으로 올린다.

**최소 실험**

- 실제 또는 공개 가능한 tool 20–30개
- 정상 chain 30개, 공격 chain 30개
- tool description-only LLM, Semgrep/CodeQL-only, hybrid 비교
- capability macro-F1, chain exact match, false negative, false positive, 분석시간 측정

---

# 4. 교육공학적 적용

이번 10건 중 **학습자를 대상으로 교육효과를 검증한 연구는 없다.** 아래는 논문에서 입증된 AI 성능과 별개의 **제안 수업 설계**다.

| 연구 | 대상·사전지식 | 관찰 가능한 학습목표·활동 | 평가·오개념·피드백 |
|---|---|---|---|
| CPAM-LLM | 대학원생; Python·최적화 | 자연어 요구를 변수·목적함수·제약으로 변환하고 실행 | 실행 30, 의미동치 40, provenance 30. “실행되면 정확” → 잘못 모델링됐지만 실행되는 반례 |
| NeSySy | ML·논리 입문자 | 제약 난이도를 변화시키고 위반율·정확도 변화를 설명 | 실험표·해석 rubric. “합성 데이터는 모두 쉬움” → CVR·fixing 비교 |
| GRASP | KGQA 학습자 | gold path와 검색경로를 비교하고 불충분 hop 식별 | Path Recall·근거 설명. “답 개체가 있으면 충분” → 도달 불가능한 경로 반례 |
| ACaM | AI 보안 학습자 | tool description과 실제 코드 capability 차이 탐지 | source–sink 경로 정확도. “도구 이름이 행동을 설명” → capability laundering 예제 |
| TRACE-MAS | MAS 학습자 | 증상 발생 위치와 최초 원인을 구분 | root-cause Hit@1·복구 결과. 마지막 오류 agent만 탓하면 event graph 피드백 |
| ATI | 보안·거버넌스 학습자 | identity·attestation·authorization을 별도 설계 | 위조 요청 차단 rubric. “인증된 agent=안전한 행동” 오류 교정 |
| Authorization Boundaries | 실무 개발자 | tool chaining·TOCTOU 공격을 재현하고 boundary를 수정 | 공격차단·정상작업 통과. “사전 path 검사로 충분” → 접근 시점 재검사 |
| Aligning AI Teams | MAS 설계자 | review·group chat·safety lead를 비교 | safety/business 및 tail 성능. “agent 수/리뷰 증가=안전” 반례 |
| FinVerify | CAPEX·재무 AI 학습자 | 숫자 claim을 시점·단위·출처·계산식으로 분해 | false accept를 가장 크게 감점. “계산 코드가 실행되면 claim도 옳음” 교정 |
| FutureBench | RAG 학습자 | 내부지식과 외부 근거가 충돌할 때 authority 정책 작성 | source-priority 판단 문항. “검색문서는 항상 최신·정확” 오류 교정 |

---

# 5. 한국어 미니 튜토리얼  
## NeSySy로 ‘논리 제약을 만족하는 학습 데이터’ 검사하기

### 출처와 실행 상태

- 논문: arXiv v1, 2026-11-14
- artifact: Zenodo v1.0, DOI [10.5281/zenodo.23640674](https://doi.org/10.5281/zenodo.23640674)
- 파일: `nesysy-artifact.zip`, 328.7KB
- 공개 체크섬: `bfe3d5c64c30905c6370d944d4f7f31c`
- artifact에는 `README.md`, `install.sh`, `smoke_test.sh`, `simple_example.py`, 예제 pipeline, 테스트, 논문 수치 파일이 포함된다.
- **이번 조사에서는 파일 구조와 공개 메타데이터까지만 확인했으며 설치·실행하지 않았다.** 아래는 비실행 재현 절차다.

## 개념

Boolean 출력 \(O_1,O_2,O_3\)에 다음 제약이 있다고 하자.

\[
(\neg O_1 \lor O_2 \lor O_3)
\land
(O_1 \lor \neg O_2 \lor O_3)
\]

이 식은 `100`, `010`을 허용하지 않는다. 일반 신경망이 `100`을 예측하면 다음 두 방식이 가능하다.

- **Filtering:** 해당 표본을 버리고 새 표본을 뽑는다.
- **Fixing:** MaxSAT으로 최소 비트만 바꿔 `101`과 같은 가장 가까운 만족 해를 만든다.

Filtering은 원래 생성분포를 덜 왜곡하지만 다양성이 낮아질 수 있고, fixing은 입력을 보존하지만 제약 경계에 표본이 몰릴 수 있다.

## 준비

- Linux 또는 WSL 권장
- Python 환경
- 전체 distant-supervision 실험은 GPU가 유리하지만 기본·smoke test는 CPU 대상
- `unzip`, shell
- 전체 artifact 사용 전 `README.md`, `install.sh`를 먼저 검토할 것

## 단계별 절차

```bash
unzip nesysy-artifact.zip
cd nesysy

md5sum ../nesysy-artifact.zip
sed -n '1,240p' README.md
sed -n '1,220p' install.sh
sed -n '1,200p' smoke_test.sh
```

체크섬은 공개값과 같아야 한다.

```text
bfe3d5c64c30905c6370d944d4f7f31c
```

내용과 설치 위치를 검토한 뒤:

```bash
bash install.sh
bash smoke_test.sh
python simple_example.py
```

논문 전체 재현 대신 일부만 확인하려면 artifact의 `run_subset.sh`와 `experiments/` 설정을 README에 따라 사용한다. 전체 실험은 25회 반복과 일부 A100 실험을 포함하므로 교육 실습에는 적합하지 않다.

## 예상해야 할 출력 특성

정확한 stdout 문자열은 실행하지 않아 제시하지 않는다. 대신 다음 조건을 확인해야 한다.

1. 생성된 논리식이 SAT/SMT solver에서 satisfiable이다.
2. 생성 데이터의 모든 `(input, output)` 쌍이 제약을 만족한다.
3. fixing 전후 출력의 Hamming 또는 \(L_1\) 거리가 기록 가능하다.
4. 모델 결과에서 accuracy와 violation rate가 별도로 계산된다.
5. solver correction을 적용한 결과의 violation rate는 0이어야 한다.
6. 같은 seed에서 생성 설정과 데이터가 재현되어야 한다.

## 최소 과제

- CVR을 두 수준으로 바꿔 각각 5,000개 표본을 생성한다.
- Base와 BaseSolver를 동일 분할에서 비교한다.
- 다음 표를 제출한다.

| 설정 | Accuracy | Violation rate | 평균 수정거리 | 실행시간 |
|---|---:|---:|---:|---:|
| Base, 낮은 CVR |  |  | – |  |
| BaseSolver, 낮은 CVR |  |  |  |  |
| Base, 높은 CVR |  |  | – |  |
| BaseSolver, 높은 CVR |  |  |  |  |

## 검증 질문·정답 기준

1. **BaseSolver accuracy가 항상 Base보다 높아야 하는가?**  
   아니오. solver는 제약 만족을 보장하지만 여러 만족 해 중 gold와 다른 해를 선택할 수 있다.

2. **Violation rate 0이면 의미적으로 정확한가?**  
   아니오. 제약이 불완전하거나 잘못되면 틀린 결과도 제약을 만족한다.

3. **Filtering과 fixing 중 어느 것이 항상 우수한가?**  
   항상 우수한 방법은 없다. filtering은 선택편향, fixing은 분포왜곡을 일으킬 수 있다.

4. **Protégé 연구에 그대로 적용할 수 있는가?**  
   직접 적용은 어렵다. CNF/QF-LRA 대신 OWL 공리, SHACL shape, competency question을 생성·검사하는 adapter가 필요하다.

## 평가상 주의점

- 학습 데이터와 테스트 데이터가 동일 제약 생성 seed를 공유하면 일반화가 과대평가될 수 있다.
- accuracy와 constraint satisfaction을 하나의 점수로 합치지 않는다.
- 수정 후 출력만 보고하면 원 모델의 위반 정도가 숨겨진다.
- 실제 온톨로지에서는 “제약 만족” 외에 원문 충실성, domain/range, 출처, revision, open-world assumption을 별도로 평가해야 한다.

---

## 6. 이번 주 핵심 결론

1. **문장→논리**는 문자열 생성보다 실행·충족가능성·정답 동치 검증으로 이동하고 있다.
2. **KG 추론**은 최종 답만 평가하지 않고 검색 경로의 충분성과 unsupported claim을 분리한다.
3. **멀티에이전트 신뢰**는 agent의 선언·합의보다 코드 capability, 권한 경계, 메시지·task dependency의 실제 trajectory를 검사하는 방향이 강하다.
4. RE:CHARGE에는 `문장→중간표현→OWL/Z3 컴파일→reasoner/solver→근거·권한 gate`가 가장 직접적인 통합 구조다.
5. 멀티에이전트 조직에는 분산된 “모두의 안전 책임”보다 **지정 Assurance Lead + 명시적 안전 명세 + tool-boundary enforcement**가 더 강한 실험적 근거를 갖는다.