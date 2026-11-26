# 신경·기호 AI 주간 연구·교육 브리핑

## 1. 검색 범위와 판정 기준

- **기준일:** 2026-11-13
- **포함 기간:** 2026-11-06 00:00–2026-11-12 23:59
- **검색원:** arXiv의 cs.AI·cs.CL·cs.MA·cs.LO·cs.CR·cs.DB, ACL Anthology 및 학회 발표 정보, SpringerLink, MDPI, Crossref/DBLP, 연구기관 보고서, 논문이 명시한 GitHub 저장소
- **주요 검색식**
  - `(ontology OR OWL OR taxonomy) AND (LLM OR neural OR agent OR reasoning)`
  - `("logical form" OR semantic parsing OR formalization) AND (Transformer OR LLM)`
  - `("knowledge graph" OR KGQA) AND (reasoning OR verification OR neuro-symbolic)`
  - `("multi-agent" OR "tool-using agent") AND (trust OR verification OR provenance OR authorization OR audit)`
- **포함:** 기간 중 최초 공개된 v1, 온라인 출판된 심사 논문, 실험·방법·결론이 바뀐 실질 개정판
- **제외:** 날짜만 바뀐 메타데이터 수정, 지난 회차 논문의 중복 판본, 순수 임베딩 성능 논문, 신뢰·검증과 무관한 일반 에이전트 벤치마크, 본문을 확인할 수 없는 색인 레코드
- **중복 처리:** 제목·저자·DOI·실험이 같은 arXiv/출판사 판본은 출판 판본을 대표로 통합했다.
- **결과:** 엄격한 기간 내 **핵심 관련 12건**, 방법론적으로 인접한 **3건**을 확인했다. 별도의 문장→FOL/람다식 전용 신규 논문은 발견하지 못했으며, ProVeST·CLADE·URDF2Ontology가 가장 가까운 연결고리였다. 확인한 v2 가운데 본문상 실질 변경을 입증하지 못한 판본은 제외했다.

아래에서 **[사실]**은 메타데이터·논문 본문, **[저자]**는 논문이 보고한 주장, **[연결]**은 사용자 연구에 대한 분석적 제안이다.

---

## 2. 핵심 논문·보고서

### 1) OGDA — Ontology-Grounded Data Agents for Reliable Analysis over Heterogeneous Data Lakes

- **서지:** Boyi Zhang 외, HKUST/HKBU; 2026-11-09 v1; 미심사 프리프린트; [원문](https://arxiv.org/abs/2611.12114), [코드](https://github.com/HKUST-KnowComp/OGDA)
- **기여·방법:** 원시 파일에서 스키마·개념·관계를 제안하고 독립 검증기가 이를 검사한다. 분석 단계에서는 온톨로지 기반 task graph가 에이전트가 읽을 수 있는 파일과 실행 순서를 제한한다.
- **평가:** KramaBench 104과제·약 1,700파일·24개 소스·6개 도메인과 DiscoveryBench 239과제. Smolagents, Reflexion, DS-STAR, Data Interpreter, DatawiseAgent와 비교하고 답 정확도, 파이프라인 점수, HMS·ctxF1·varF1을 측정했다.
- **결과:** 세 백본에서 최강 기준선 대비 Krama 답 점수가 각각 10.82, 3.30, 10.46점 높았다. grounding agent 제거 시 73.00→60.94로 하락했다.
- **한계:** OWL/DL 추론기가 아니라 파일·스키마 수준 온톨지다. LLM 평가기 의존, 온톨로지 구축비용, 특정 데이터 분석 벤치마크라는 제약이 있다.
- **연결:** 문장→논리→트리플뿐 아니라 **“어떤 원문·파일에서 그 트리플과 계산값을 얻을 수 있는가”**를 task graph로 통제하는 층을 추가할 수 있다.

### 2) TIGA — Controlled Knowledge Engineering for Taxonomy Induction

- **서지:** Jonas Limniatis 외, Lufthansa Technik 등; 2026-11-10 v1; *Knowledge-Based Systems* 투고 중, 현재 미심사; [원문](https://arxiv.org/abs/2611.13966), [코드](https://github.com/bschaarmann/TIGA)
- **기여·방법:** LLM이 자유 텍스트로 계층을 출력하는 대신 제한된 편집 도구, 명시적 taxonomy 상태, 동적 정책, 선택적 reviewer를 이용한다.
- **평가:** WordNet 761개 하위 트리의 533/114/114 분할, DBLP 5개 taxonomy, TExEval-2 18개 taxonomy, GProd. GPT-5.4-mini와 Gemma4-31b, HF·Chain-of-Layer 기준선, 5회 반복. edge/ancestor P·R·F1, coverage, extraneous entities, 트리 유효성 및 비용을 측정했다.
- **결과:** Gemma 조건에서 ancestor/edge F1이 WordNet 85.82/66.86, DBLP 75.60/55.30, TExEval-2 82.60/64.60, GProd 85.20/71.20. 8개 설정 중 7개에서 최고였지만, 일부 조건에서는 reviewer가 오히려 성능을 낮췄다.
- **한계:** 단일 부모의 rooted tree만 다룬다. 다중 상속, 객체속성, 공리, OWL 일관성은 평가하지 않았고 호출비용이 크다.
- **연결:** Transformer 추출 결과를 Protégé에 바로 넣기 전에, 제한된 `add/move/delete` 연산과 검토 정책으로 taxonomy를 조립하는 중간 계층으로 적합하다.

### 3) Taxonomy-Agnostic Neurosymbolic Grounding of Robot Kinematics

- **서지:** Bastien Dussard, Aurélie Clodic, Guillaume Sarthou; 2026-11-10 v1; AAAI Fall Symposium 2026 proceedings 수록; [원문](https://arxiv.org/abs/2611.13850), [코드](https://github.com/RIS-WITH/urdf2ontology)
- **기여·방법:** URDF를 그래프로 바꾼 뒤, 로컬 `gpt-oss:20b`가 고정된 OWL TBox에 맞춰 ABox를 생성한다. 그래프 정리, bottom-up Tree Track, top-down Chain Track, 구문 검증을 사용한다.
- **평가:** Solo, RB-VOGUI+, PR2, iCub, Ingenuity 등 5개 로봇. 추출된 개체·개념을 질적으로 분석했으며 표준 정확도 기준선이나 train/test 분할은 없다.
- **결과:** 최대 134개 링크의 iCub를 처리했다. 150개 촉각 셀을 그대로 포함하면 문맥 열화와 환각이 나타났고, 필터링 후 개선됐다.
- **한계:** 로봇 5종·TBox 1개, 식별자 의미에 의존하는 사례연구다. OWL reasoner 기반 일관성 검사는 향후 과제로 남았다.
- **연결:** URDF 대신 문장·절·개체를 노드로 한 문서 그래프를 입력하면 사용자 파이프라인에 가깝다. 다만 HermiT/SHACL 검증과 원문 span provenance를 반드시 보강해야 한다.

### 4) ProVeST — Progressive Semantic Verification for Multi-Hop KGQA

- **서지:** Zicheng Zuo 외; *Information* 17(11):1119, 2026-11-09; 심사 논문; DOI [10.3390/info17111119](https://doi.org/10.3390/info17111119)
- **방법:** 질문을 하위 질문으로 분해하고, 그래프 후보를 점수화한 뒤 LLM이 개체와 경로 문맥을 검증한다. 검증된 개체만 다음 hop의 상태에 들어간다.
- **평가:** WebQSP 2,848/250/1,639, CWQ 27,639/3,519/3,531; Hit@1·F1; 3개 LLM 백본. GPT-4 조건에서 WebQSP .803/.741, CWQ .619/.573. 계획 모듈 제거 시 CWQ Hit@1/F1이 .161/.160 하락했다.
- **한계:** LLM 검증은 형식 증명이 아니며 후보 수가 제한된다. 첫-hop 상태 분석도 35문항에 그친다.
- **연결:** 추출된 논리 표현이나 트리플이 검증되기 전에는 다음 추론 단계의 상태로 승격하지 않는 설계에 활용할 수 있다.

### 5) CLADE — Category-Level Answering from Deficient Evidence

- **서지:** S. M. Rayeed, Charles V. Stewart, Yao Ma; 2026-11-10 v1; 미심사 프리프린트; [원문](https://arxiv.org/abs/2611.14355)
- **방법:** 문서가 구체적 질병 대신 상위 질병군만 제공하는 “resolvable insufficiency”를 분석하고, 온톨로지의 하위 후보 목록으로 복구를 시도한다.
- **평가·결과:** PrimeKG에서 상위군 정보는 abstention을 13.8%p 줄였지만 추측의 약 절반이 틀렸다. 정답을 포함한 후보 목록은 98.5% 생성했지만 end-to-end 복구는 10.0%→26.8%에 머물렀다. GloBI에서도 재현했다.
- **한계:** 온톨로지는 후보를 열거할 뿐 올바른 하위 개체를 결정해주지 않는다.
- **연결:** 상위 클래스 근거만으로 특정 instance 트리플을 확정하지 않도록 `class-supported`와 `instance-supported` 상태를 분리할 필요가 있다.

### 6) Graph Visualizations in Prompts for Knowledge Graph Question Answering

- **서지:** Luiz do Valle Miranda, Andreas L. Opdahl, Grzegorz J. Nalepa; 2026-11-06 v1; AACL-IJCNLP 채택 논문; [원문](https://arxiv.org/abs/2611.12938)
- **평가·결과:** WebQSP/CWQ 1,500문항, VLM 6종, 텍스트와 텍스트+그래프 비교. 전체 평균 F1 +1.85, 저복잡도 문제 +4.65였고 path-decomposed/hierarchical layout이 우수했다.
- **한계:** 복잡한 그래프에서는 시각적 혼잡이 커지고 image-only는 열세였다. 형식 추론의 개선을 입증한 것은 아니다.
- **연결:** Protégé 그래프를 그대로 이미지화하기보다 추론 경로 중심의 소그래프로 분해해 Transformer/VLM 검토 입력으로 제공할 수 있다.

### 7) ActiveSecHarness — Compositional Security for Agentic Coding Harnesses

- **서지:** Simon Hegelich 외; 2026-11-10 v1; 미심사 프리프린트; [원문](https://arxiv.org/abs/2611.13960)
- **방법:** 지능과 권한을 분리하고, capability token·4개 권한 ring·`trust × sensitivity` taint lattice·workspace provenance·결정적 Ring-0 guard를 결합한다.
- **평가:** 공격 120, 정상 120, 5단계 kill-chain 12개, 총 252 fixture. 무방비·regex·Qwen judge·Ring-0·hybrid 비교.
- **결과:** Ring-0/hybrid의 공격차단률 1.0, 오탐률 0. LLM judge는 오탐률 .983이었다. Ring-0은 12.7μs로 142.3ms의 live judge보다 약 11,200배 빨랐다.
- **한계:** 합성 fixture와 코딩 하네스 중심이다. 실제 조직의 권한 철회·사람 승인·장기 운영 평가는 부족하다.
- **연결:** 멀티에이전트의 합의가 아니라 도구 호출 직전의 결정적 권한 검사를 신뢰 경계로 삼아야 한다.

### 8) WikiTrace — Evidence-Linked Memory

- **서지:** Yukyeong Lee 외, KAIST/DeepAuto; 2026-11-10 v1; ACL Rolling Review 투고 중; [원문](https://arxiv.org/abs/2611.14320), [코드](https://github.com/yukyeongleee/wikitrace)
- **방법:** 학습된 insight를 요약된 근거와 원시 trajectory에 연결한 3층 메모리다. 모호하거나 충돌하는 insight는 원자료까지 내려가 확인한다.
- **평가:** ALFWorld, ScienceWorld, PlanCraft, AppWorld, τ-bench 계열. 동일 insight만 제공하는 기준선보다 평균 약 8.5%p 개선하고 memory-induced regression을 줄였다고 보고한다.
- **한계:** trajectory 저장·검색비용이 크며, 근거 연결이 곧 논리적 타당성을 보장하지는 않는다.
- **연결:** 각 추출 규칙·온톨로지 수정안을 원문 문장과 생성 실행 기록에 연결하는 provenance memory로 적용할 수 있다.

### 9) FGSE — Falsification-Gated Self-Evolution

- **서지:** Runxuan Tang 외; 2026-11-10 v1; 미심사 프리프린트; [원문](https://arxiv.org/abs/2611.14326)
- **방법:** 새 memory lesson을 전제조건·행동변화·예상효과·verifier로 구성된 가설로 만들고 임시 상태에서 전이·반증·회귀 probe를 통과해야 영구 반영한다.
- **결과:** WebArena 39.8, AppWorld 78.8, τ-Retail/Airline Pass@1 .724/.487; 반증 실패 5.0%, 회귀 손상 1.3%, 해로운 commit 3.6%.
- **한계:** verifier와 회귀 과제를 잘 만들 수 있다는 가정에 크게 의존하고 실험비용이 높다.
- **연결:** 온톨로지 공리·프롬프트·에이전트 규칙의 변경을 임시 branch에서 competency question으로 검사한 뒤 병합하는 방식과 잘 맞는다.

### 10) Multi-Agent Screening: What Agreement and Acceptance Cannot Tell You

- **서지:** Benjamin Chang, Dell Zhang; 2026-11-09 v1; 미심사 이론 프리프린트; [원문](https://arxiv.org/abs/2611.12705)
- **기여:** 에이전트 간 agreement는 정확성을 식별하지 못하며, assessor가 수락된 항목만 평가하면 precision은 추정해도 recall은 하한밖에 얻지 못함을 보인다. 거절 표본을 무작위 심사해야 recall을 식별할 수 있다.
- **평가:** 실증 벤치마크가 아니라 식별조건과 bound의 이론 분석이다.
- **한계:** 교환가능성·상관 구조 등 가정에 민감하다.
- **연결:** 에이전트들이 동의한 트리플만 평가하지 말고, **거절된 트리플을 층화 표집**해 false negative를 추정해야 한다.

### 11) Trust, but Verify, Audit and Attribute

- **서지:** György Eigner, Patrik P. Süli, Roland Hollós; 2026-11-09 v1; 미심사 프리프린트; [원문](https://arxiv.org/abs/2611.13042)
- **방법:** 서로 다른 신뢰 근거를 가진 도구, 결과의 fidelity audit, 고정된 인간 의사결정점, 대화별 attribution을 결합한다. Wolfram·MATLAB·Lean과 Python/R 구현 사례를 제시한다.
- **평가:** 모호한 수학 주장 하나를 두 해석으로 분리해 하나는 반박하고 하나는 증명한 사례연구다.
- **한계:** 실질적으로 2개 claim의 사례이며 대조군과 일반화 평가가 없다.
- **연결:** 논리식이 증명 가능하다는 것과, 그 논리식이 원문 문장을 충실히 나타낸다는 것을 별도의 검사로 분리해야 한다.

### 12) Authorization Assurance for Tool-Using LLM Agents

- **서지:** Mohamed Abbas Elmasry; *International Journal of Information Security*, 2026-11-10; 심사 논문; DOI [10.1007/s10207-026-01343-w](https://doi.org/10.1007/s10207-026-01343-w)
- **방법:** 75개 자료에서 30개 분석 corpus와 92개 source–claim 레코드를 만든 구조화 리뷰다.
- **결과:** strict mediation을 평가한 자료는 5개뿐이며, 에이전트 중심 자료 21개 중 평가 가능한 권한 철회 연구는 없었다. 30개 중 delegation containment 평가도 없었다. 독립 코딩 표본의 κ는 약 .86–.90이었다.
- **한계:** 새로운 보안 시스템의 실험이 아니라 문헌 증거의 공백 분석이다.
- **연결:** 감사 로그를 예방 통제로 오해하지 말고, non-bypass·least privilege·revocation·delegation을 각각 독립 시험해야 한다.

---

## 3. 인접하지만 유용한 자료

### 자동차 CTI–TARA OWL 온톨로지

CAPEC·CWE·CVE/NVD·STRIDE·UN R155·ISO/SAE 21434를 OWL 2 DL로 연결하고 Protégé/HermiT와 competency question으로 검사한다. 59개 CAPEC Meta pattern 중 기술 측면 50개, STRIDE 49개, UN R155 27개가 연결됐다. 제품별 공격 경로와 위험 계산은 범위 밖이다. 사용자 연구에는 **Protégé/HermiT 평가 설계의 직접 예시**다. *Information* 17(11):1122, 2026-11-09, DOI [10.3390/info17111122](https://doi.org/10.3390/info17111122).

### Auditable Human–Agent Teams for Autonomous X-ray Experimentation

세 번의 실제 방사광 실험에서 전체 인간–에이전트·에이전트–에이전트 transcript를 보존했다. 메시지의 61–67%가 해석·판단이었고, 오류 수정의 59–68%가 복수 참여자를 거쳤다. 실제 시스템이라는 강점이 있지만 실험 3건이며 신뢰 기법 간 대조실험은 없다.

### Beyond the Document — Portable Agent Format

결과물에 evidence·provenance·authorization을 함께 패키징한다. 4개 패키지·400문항·12,000응답에서 hosted reader 96%, 지침+원파일 검색 86%였지만 표현 방식과 학습 효과를 분리하지 못했고 한 패키지의 역사 기록 40문항은 offline reader가 전부 실패했다.

---

## 4. 사용자 연구에 대한 우선 적용안 3건

### A. OGDA 기반 “근거 제한형 온톨로지 추출”

1. 프로젝트 문서·CSV·DB의 스키마와 개념을 제안하되 모든 edge에 source ID를 붙인다.
2. 별도 검증기가 데이터 profiling 및 competency question으로 제안을 승인한다.
3. 질의를 `source selection → extraction → logic conversion → reasoner → answer` task graph로 컴파일한다.
4. 각 단계는 task graph가 허용한 파일만 읽게 한다.

**필요 자료:** OGDA 코드, 과거 프로젝트 3–5개, 60–100개 질의, 정답 파일·트리플 표본.

**최소 실험:** 프로젝트 단위 분할로 60개 질의를 사용해 ① 직접 ReAct, ② read-only ontology, ③ 강제 task graph를 비교한다. 답 정확도, 필요 파일 precision/recall, 허가되지 않은 파일 접근, triple F1, 비용을 측정한다.

### B. URDF2Ontology를 문장→OWL 파이프라인으로 변환

1. 문서를 절–문장–개체 그래프로 변환한다.
2. 관련 소그래프와 고정 TBox만 Transformer/LLM에 제공한다.
3. 모델은 class assertion·object property·data property 후보를 생성한다.
4. SHACL과 HermiT가 구문·domain/range·불일치·unsatisfiable class를 검사한다.
5. 실패한 후보는 자동 확정하지 않고 원문 span과 함께 보류한다.

**최소 실험:** 문서 독립 분할의 수작업 표본 200문장으로 ① 단일 프롬프트, ② schema-constrained, ③ 소그래프+reasoner를 비교한다. entity/triple F1, 논리적 유효률, unsatisfiable 수, competency-question 정확도와 비용을 측정한다.

### C. ActiveSecHarness 기반 멀티에이전트 권한 경계

- `raw-read → propose → calculate → ontology-write → approve/export` 권한을 분리한다.
- 데이터에 `trusted/sanitized/derived/untrusted × public/sensitive` 라벨을 전파한다.
- LLM judge는 조언만 하고, DB·파일·Protégé 수정과 외부 전송 직전에 결정적 guard를 둔다.
- 에이전트 위임·권한 철회·간접 prompt injection의 전체 trajectory를 기록한다.

**최소 실험:** 정상 작업 100개, 공격 100개, 다단계 공격 20개에서 prompt-only, LLM judge, regex, lattice guard, hybrid를 비교한다. 공격차단률, 정상 오탐률, 철회 후 write 수, 민감정보 누출, 지연시간을 측정한다.

---

## 5. 교육공학적 적용

**중요:** 이번 논문들은 학습자를 대상으로 한 교육효과 실험을 보고하지 않았다. 아래 내용은 모두 논문 결과를 소재로 만든 **제안 수업 설계**이지, 입증된 교육효과가 아니다.

| 자료 | 학습자·사전지식 | 관찰 가능한 목표와 활동 | 평가·예상 오개념·피드백 |
|---|---|---|---|
| OGDA | 대학원생; KG·데이터 분석 | 동일 질의를 세 접근으로 실행하고 source access 차이를 설명 | 정답 40, 출처 선택 30, 설명 30. “온톨로지가 있으면 자동으로 정확” → grounding ablation 제시 |
| TIGA | AI/지식공학 학부 고학년 | 후보 개체로 valid rooted taxonomy를 구성하고 edge/ancestor F1 계산 | 구조 유효성·의미 정확성 각각 채점. “valid tree=correct taxonomy”를 반례로 교정 |
| URDF2Ontology | 로보틱스·시맨틱웹 학습자 | URDF 요소를 OWL individual/class/property로 구별 | 생성 ABox와 HermiT 결과 평가. TBox와 ABox 혼동을 색상 구분으로 피드백 |
| ProVeST | KGQA 학습자 | hop마다 검증 전후 후보 상태를 추적 | 오류가 처음 유입된 hop 식별. “LLM 확인=증명”은 counterexample로 교정 |
| CLADE | 의료정보학·NLP | 상위 class 근거와 개별 instance 근거를 구별 | 증거수준 라벨링 정확도. 상위군을 특정 질병으로 확정하는 오류 피드백 |
| Graph-Viz KGQA | KG 입문자 | 같은 경로를 force/hierarchical/path layout으로 표현 | 경로 정확성과 인지부하 자기보고. “정보가 많을수록 좋음”을 clutter 사례로 교정 |
| ActiveSecHarness | AI 보안 학습자 | capability와 taint 규칙을 설계하고 공격 trajectory 차단 | ABR·FPR·revocation 시험. “LLM judge가 보안 경계”라는 오개념을 실험으로 반박 |
| WikiTrace | 에이전트 설계 학습자 | insight를 원 trajectory에 연결하고 충돌 시 근거를 역추적 | provenance 완전성·회귀율. “성공 episode의 교훈은 항상 옳음”을 실패사례로 교정 |
| FGSE | 고급 AI 수업 | memory update용 반증·회귀 probe를 설계 | 해로운 commit 탐지율. “한 번 성공하면 영구 저장”을 임시 branch 활동으로 교정 |
| Multi-Agent Screening | 연구방법론 학습자 | accepted/rejected 표본으로 precision·recall의 식별 가능성을 판단 | 식별조건 서술과 계산. agreement와 correctness 혼동을 교정 |
| Trust/Audit/Attribute | 형식방법 학습자 | fidelity·formal validity·human authorization을 별도 검사 | 세 검사 중 누락된 항목 찾기. “증명됨=원문 충실” 오류 피드백 |
| Authorization Review | AI 거버넌스 학습자 | 보안 주장을 mediation·revocation·delegation 증거로 분류 | claim–evidence rubric. 로그 존재를 예방 통제로 간주하면 반례 제공 |
| 자동차 CTI 온톨로지 | Protégé 실습생 | OWL 공리 작성→HermiT→competency question 수행 | 일관성, CQ 정확도, 출처. “일관성 0 오류=완전성” 혼동 교정 |
| X-ray 팀 | 과학자동화 학습자 | transcript에서 제안·결정·오류수정 provenance 코딩 | 코더 간 일치도와 근거 링크. 최종 성공만으로 역할을 추론하지 않도록 피드백 |
| PAF | 연구데이터 관리 학습자 | 결과물에 출처·가정·권한 경계를 패키징 | 누락 근거와 권한 위반 문항. “파일을 함께 주면 provenance가 보존됨”을 교정 |

---

# 6. 한국어 미니 튜토리얼: TIGA로 도구 제약형 Taxonomy 생성 이해하기

## 상태와 출처

- 대상: TIGA arXiv v1, 2026-11-10
- 저장소: [HKUST가 아닌 TIGA 공식 저장소](https://github.com/bschaarmann/TIGA)
- 요구사항: Python 3.11 이상, `uv` 0.7.9 계열, 모델 제공자 자격증명
- **실행 상태:** 아래 명령은 저장소 문서와 설정을 대조했지만, 이번 조사 환경에서 모델 호출까지 실행하지 않았다. 따라서 **비실행 재현 가이드**다. 저장소는 benchmark를 내려받지만 모델 응답과 기준 결과 파일은 제공하지 않는다.

## 핵심 개념

TIGA의 핵심은 LLM에게 전체 taxonomy 문자열을 한 번에 쓰게 하지 않는 것이다.

1. 현재 taxonomy와 미배치 개체를 상태로 유지한다.
2. 모델은 허용된 편집 도구만 호출한다.
3. 정책은 남은 오류나 상태에 따라 갱신된다.
4. reviewer를 선택적으로 사용한다.
5. 최종 결과를 구조 유효성과 의미적 F1로 따로 평가한다.

## 준비와 데이터 검증

```bash
git clone https://github.com/bschaarmann/TIGA.git
cd TIGA
uv sync --locked

uv run tiga prepare-data --config configs/reproduction.toml
uv run tiga validate-data --config configs/reproduction.toml
```

예상되는 것은 각 benchmark 원자료가 준비되고, 레코드 스키마·필수 필드·개체 집합을 검사한 결과다. 정확한 로그 문자열은 환경과 저장소 버전에 따라 달라질 수 있다.

## 최소 smoke test

`configs/reproduction.toml`을 `configs/local.toml`로 복사하고 다음과 같은 최소 조건으로 줄인다.

```toml
prompt_variants = ["no_policy"]
reviewer = false
repetitions = 1
record_limit = 1
```

그다음 실행한다.

```bash
uv run tiga run --config configs/local.toml
```

API 키와 모델 이름은 저장소의 provider 설정에 맞춰 별도로 지정해야 한다. 실행이 성공하면 한 레코드에 대한 모델 호출 기록, taxonomy 상태 변화, 최종 예측 및 평가용 산출물이 생성되어야 한다. 경로나 파일명은 선택한 config와 저장소 버전을 기준으로 확인한다.

## 직접 검증할 조건

최종 taxonomy \(T=(V,E)\)에 대해 다음을 검사한다.

1. 모든 기대 개체가 정확히 한 번 존재하는가?
2. 허용되지 않은 개체가 추가되지 않았는가?
3. root의 부모는 0개이고 다른 노드의 부모는 정확히 1개인가?
4. 모든 노드가 root에서 도달 가능한가?
5. cycle이 없는가?
6. 구조가 유효하더라도 gold parent와 의미적으로 일치하는가?
7. direct-edge F1과 ancestor F1이 왜 다른가?

예를 들어 정답이 `동물→포유류→개`인데 모델이 `동물→개→포유류`를 만들면 rooted tree로서는 유효하지만 의미적으로 틀리다.

## 확인 문제와 정답 기준

1. **Reviewer를 붙이면 항상 더 정확한가?**  
   아니오. TExEval-2 일부 조건에서는 성능이 하락했다.

2. **Ancestor F1이 edge F1보다 높을 수 있는 이유는?**  
   직접 부모를 틀려도 더 먼 상위–하위 관계 일부는 유지될 수 있기 때문이다.

3. **이 결과를 OWL 온톨로지 생성 성능으로 바로 해석할 수 있는가?**  
   아니오. 실험은 단일 부모 taxonomy이며 객체속성·제약·다중 상속·논리적 충족가능성을 평가하지 않는다.

4. **사용자 연구로 옮길 때 추가할 검증은?**  
   원문 span 추적, relation/triple F1, SHACL, HermiT 일관성, competency question, 문서 독립 분할이 필요하다.

## 평가상 주의점

- 모델과 provider 버전이 바뀌면 결과가 달라질 수 있다.
- 같은 개체명이 사전학습에 존재할 수 있으므로 무작위 분할보다 도메인·프로젝트 독립 분할이 낫다.
- 완전한 rooted tree 생성률과 의미 정확도를 합쳐 보고하면 실패 원인이 가려진다.
- reviewer 호출비용과 수정 횟수를 성능과 함께 보고해야 한다.
- 공개 benchmark의 원 라이선스도 별도로 확인해야 한다.

---

## 7. 이번 주의 결론

이번 주의 공통 흐름은 “신경 모델이 더 잘 추론하도록 만드는 것”보다 **신경 모델의 출력을 어떤 상태·도구·근거·권한 경계 안에서만 사용할 것인가**에 있다.

사용자 연구에는 다음 우선순위가 가장 타당하다.

1. 문장→논리/트리플마다 원문 provenance를 보존한다.
2. 검증된 트리플만 온톨로지와 다음 추론 단계에 승격한다.
3. Protégé/HermiT의 일관성과 원문 fidelity를 별도 평가한다.
4. 멀티에이전트 agreement가 아니라 거절 표본의 false negative도 감사한다.
5. 온톨로지·memory·규칙 변경은 반증 및 회귀 검사를 통과한 뒤 반영한다.