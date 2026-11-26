| RAG triad(context relevance·faithfulness·answer relevance) | https://www.trulens.org/getting_started/core_concepts/rag_triad/ | query-context / context-response(groundedness) / query-response 세 쌍을 삼각형 세 변으로 평가. 5단원 평가 대상 구조도 |
| RAGAS 지표 | https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/ | Faithfulness·Response Relevancy·Context Precision/Recall 목록. 5단원 표기 대응 |
| RGB 네 능력 | https://arxiv.org/abs/2309.01431 | noise robustness·negative rejection·information integration·counterfactual robustness 정의. 5단원 능력별 예시 표 |
| 긴 문맥 vs RAG | https://arxiv.org/abs/2407.16833 | LC가 평균 성능은 높고 RAG는 비용이 훨씬 낮음, Self-Route로 절충. 6단원 비교표 |
| RAG 전체 구조(1·2단원) | LangChain RAG 튜토리얼 https://docs.langchain.com/oss/python/langchain/rag ; 논문 그림 2 | Load-Split-Store(indexing)와 Retrieve-Generate(온라인)를 오프라인/온라인 구획으로 나눈 구조도, 단계별 예시 값 |
| Naive/Advanced/Modular 비교(2단원) | 논문(arXiv 2312.10997) 그림 3, 2.1~2.3절 | 같은 단계 축(pre-retrieval/retrieval/post-retrieval/generation)에 세 방식을 행으로 정렬, Modular의 교체 모듈과 반복 흐름 |
| RAG vs fine-tuning vs prompt engineering(2단원) | 논문 그림 4, 2.4절 | 두 축 개념도 유지 + 같은 상황에서 바뀌는 곳(프롬프트/가중치) 비교 그림과 표 |
| parametric vs non-parametric, sparse vs dense(1단원) | 논문 1절·2.4절의 교과서 비유; BM25/임베딩 일반 설명(자체 예시 값) | 같은 질문/같은 query를 두 방식에 넣은 나란히 비교 그림 |
| chunking 전략 비교(3단원) | LlamaIndex Production RAG https://developers.llamaindex.ai/python/framework/optimizing/production_rag/ | 검색용 청크와 생성용 청크를 분리(sentence window, 요약→청크). 같은 문서·같은 query를 fixed-size/sentence/Small2Big에 넣은 나란히 비교 그림 |
| query rewriting/expansion/HyDE/routing(3단원) | LlamaIndex Query Transformations https://developers.llamaindex.ai/python/framework/optimizing/advanced_retrieval/query_transformations/ | HyDE=가상 답변 임베딩, multi-step/sub-question 분해. 같은 query 하나를 네 방식이 바꾸는 열 비교 그림 |
| Lost in the Middle(4단원) | Liu et al. 2023 https://arxiv.org/abs/2307.03172 | 정답 문서가 입력 처음·끝에 있을 때 성능이 높고 가운데에서 떨어짐(긴 문맥 모델도 해당). 초록에 수치가 없어 U자 곡선은 개념도로만 그림 |
| reranking vs context compression(4단원) | 논문 4.1절(arXiv 2312.10997) | 같은 top-5 목록에서 하나는 순서만, 하나는 길이만 바꾸는 3행 비교 그림 |
| iterative/recursive/adaptive(4단원) | 논문 그림 5, 5절 | 같은 multi-hop 질문에 대한 세 줄 시간선(검색이 일어나는 단계 표시) |
| FLARE vs Self-RAG(4단원) | 논문 5.3절 | 신호 비교: 낮은 확률 토큰(문턱값) vs reflection token |

## 실무자 의견 반영 조사 (조사 시점 2026-11, 1차 출처 확인분만)

| 주제 | 출처 | 확인한 내용(강의에 쓸 수 있는 문장·수치) |
|---|---|---|
| dense 실패: 희귀 개체 | Sciavolino et al. 2021, https://arxiv.org/abs/2109.08535 표 1 | top-20 정확도. NQ: DPR(NQ) 80.1, DPR(multi) 79.4, BM25 64.4. EntityQuestions(macro): DPR(NQ) 49.7, DPR(multi) 56.7, BM25 72.0. "DPR은 흔한 개체에서 잘 되지만 드문 개체로 갈수록 빠르게 떨어진다"(4.1절) |
| dense 실패: 도메인 이동 | BEIR, Thakur et al. 2021, https://arxiv.org/abs/2104.08663 | 9개 과제, 18개 데이터셋 zero-shot. "BM25는 견고한 기준선", reranking·late-interaction이 평균 최고지만 계산 비용이 큼. dense는 효율적이지만 "많은 데이터셋에서 BM25보다 크게 못함". 도메인 안 평가에서 BM25를 이긴 방법이 BEIR에서는 저조 |
| dense 실패: 부정 | NevIR, Weller et al. EACL 2024, https://arxiv.org/abs/2305.07614 | 부정만 다른 두 문서의 순위를 매기게 함. 대부분의 IR 모델(SOTA 포함)이 무작위와 같거나 못함. cross-encoder > late-interaction > bi-encoder·sparse 순 |
| 임베딩 차원 한계 | LIMIT, Weller et al. ICLR 2026, https://arxiv.org/abs/2508.21038 | 차원이 고정된 단일 벡터로는 어떤 query로도 돌려줄 수 없는 top-k 조합이 생김. 대안: cross-encoder, multi-vector, 더 표현력 있는 유사도 함수 |
| Advanced RAG 지연 | RAGO, Jiang et al. 2025, https://arxiv.org/html/2503.14649v2 5.4절 | 한 서빙 실험(rewriter 8B, reranker 120M)에서 rewriter를 넣으면 자기회귀 생성 때문에 TTFT가 2.4배로 늘고, reranking은 TTFT 영향이 작음 |
| Modular RAG 흐름 | Gao et al. 2024, https://arxiv.org/abs/2407.21059 | 모듈·연산자 조합(LEGO 비유), routing·scheduling·fusion, linear/conditional/branching/loop 패턴. Naive ⊂ Advanced ⊂ Modular |
| ICL | Brown et al. 2020, https://arxiv.org/abs/2005.14165 ; Ram et al. 2023 TACL, https://arxiv.org/abs/2302.00083 | GPT-3 few-shot: 가중치 갱신 없이 프롬프트의 예시로 과제 수행. In-Context RALM: 모델 구조를 바꾸지 않고 검색 문서를 입력 앞에 붙이기만 해도 큰 향상, API로만 쓰는 모델에도 적용 가능 |
| EM·토큰 F1 | SQuAD, Rajpurkar et al. 2016, https://arxiv.org/abs/1606.05250 | 답변 평가 표준: 완전 일치(EM)와 토큰 겹침 F1 |
| GraphRAG | Edge et al. 2024, https://arxiv.org/abs/2404.16130 | 대상: 말뭉치 전체에 대한 global 질문("데이터셋의 주요 주제는?"), 일반 RAG는 실패. 단계: LLM이 개체·관계 추출 → 지식 그래프 → Leiden 계층 커뮤니티 → 아래에서 위로 커뮤니티 요약 → map(커뮤니티별 부분 답, 유용성 0~100점) → reduce(점수순 결합). 약 100만 토큰 말뭉치 2개에서 포괄성·다양성이 일반 RAG보다 높음(LLM 판정). 팟캐스트 데이터 색인 281분. 한계: 두 말뭉치의 sensemaking 질문에 국한된 평가 |
| Parametric RAG | Su et al. SIGIR 2025, https://arxiv.org/abs/2501.15915 | 오프라인: 문서 증강(재작성 + QA 쌍) → 문서마다 LoRA(FFN 행렬에만) 학습. 온라인: 검색 → 해당 LoRA를 합쳐 모델 갱신 → 생성. 장점: 입력 문맥에 여러 문서를 넣지 않아 온라인 계산 절약, in-context RAG와 결합하면 더 좋아짐. 한계: 오프라인 계산 부담, 문서당 저장(LLaMA3-8B, 16비트 약 4.72MB), 특정 LLM에 묶임 |
| DyPRAG | Tan et al. 2025, https://arxiv.org/abs/2503.23895 | 가벼운 parameter translator가 추론 시점에 문서를 파라미터로 변환해 문서별 학습·저장 비용을 없앰 |
| Search-R1 | Jin et al. 2025, https://arxiv.org/abs/2503.09516 | `<search>` 토큰으로 검색을 호출하고 결과를 `<information>`으로 받으며 추론을 이어감. 강화 학습(PPO·GRPO), 보상은 최종 답의 EM뿐(결과 기반). 검색 결과 토큰은 손실에서 제외. 향상 수치는 판마다 달라(41%/24%) 쓰지 않음 |
| Agentic RAG | Singh et al. 서베이(2026-04 v4), https://arxiv.org/abs/2501.09136 ; Lin et al. 2025, https://arxiv.org/abs/2510.16724 | RAG 파이프라인 안에 자율 에이전트(성찰·계획·도구 사용·다중 에이전트 협업)를 둠. 분류 축: 에이전트 수, 제어 구조, 자율성, 지식 표현. Lin 등: 강화 학습 기반 agentic search 서베이 |
| (쓰지 않음) | arXiv 2603.07379 SoK | arXiv가 품질 기준 미달로 철회(2026-10). 인용 금지 |
