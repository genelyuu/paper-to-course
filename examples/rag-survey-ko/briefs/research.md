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
