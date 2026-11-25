# 강의 용어표: 대규모 언어 모델을 위한 검색 증강 생성 서베이

모든 모듈은 이 표의 표기만 쓴다. 원어 우선 규칙(SKILL.md 용어 표기): 영어로 통용되는 개념어는 원어를 본문 표기로 쓰고 첫 등장에만 한글 뜻을 괄호로 단다. 모듈마다 첫 등장에서 병기하고 툴팁을 단다.

| English | 한국어 표기 | 첫 등장 표기 | 처음 나오는 모듈 | 비고 |
|---|---|---|---|---|
| retrieval-augmented generation | 검색 증강 생성 | 검색 증강 생성(Retrieval-Augmented Generation, RAG) | 1 | glossary-ko. 이후 `RAG` |
| large language model | 대규모 언어 모델 | 대규모 언어 모델(Large Language Model, LLM) | 1 | glossary-ko. 이후 `LLM` |
| hallucination | 환각 | 환각(Hallucination) | 1 | glossary-ko 기본값 |
| parametric knowledge | parametric knowledge | parametric knowledge(모델 가중치에 저장된 지식) | 1 | 원어 우선(이전 표기 `매개변수 지식` 폐기) |
| non-parametric knowledge | non-parametric knowledge | non-parametric knowledge(외부 문서에 있는 지식) | 1 | 원어 우선(이전 표기 `비매개변수 지식` 폐기) |
| embedding | 임베딩 | 임베딩(Embedding) | 1 | glossary-ko |
| cosine similarity | 코사인 유사도 | 코사인 유사도(Cosine Similarity) | 1 | 관행 |
| vector database | 벡터 데이터베이스 | 벡터 데이터베이스(Vector Database) | 1 | 관행 |
| sparse retrieval | sparse retrieval | sparse retrieval(단어 일치 기반 검색) | 1 | 원어 우선(이전 표기 `희소 검색` 폐기) |
| dense retrieval | dense retrieval | dense retrieval(임베딩 벡터 기반 검색) | 1 | 원어 우선(이전 표기 `밀집 검색` 폐기) |
| BM25 | BM25 | BM25(Best Matching 25) | 1 | 고유 명칭 |
| chunk | 청크 | 청크(Chunk) | 2 | 관용 음차. `조각`은 일반어와 겹쳐 버림(결정 절차 3단계) |
| chunking | chunking | chunking(문서를 청크로 나누기) | 3 | 원어 우선(이전 표기 `청크 분할` 폐기) |
| indexing | indexing | indexing(색인 구축) | 2 | 원어 우선(이전 표기 `인덱싱` 폐기) |
| retrieval | 검색 | 검색(Retrieval) | 1 | search와 같은 말이 되므로 search 엔진은 `검색 엔진`으로만 씀 |
| top-k | top-$k$ | top-$k$(상위 $k$개) | 1 | 원어 우선(이전 표기 `상위 k개` 폐기) |
| query | query | query(검색 질의) | 1 | 원어 우선(이전 표기 `질의` 폐기) |
| query rewriting | query rewriting | query rewriting(질의 재작성) | 3 | 원어 우선(이전 표기 `질의 재작성` 폐기) |
| query expansion | query expansion | query expansion(질의 확장) | 3 | 원어 우선(이전 표기 `질의 확장` 폐기) |
| query routing | query routing | query routing(질의 경로 선택) | 3 | 원어 우선(이전 표기 `질의 라우팅` 폐기) |
| reranking | reranking | reranking(재순위화) | 2 | 원어 우선(이전 표기 `재순위화` 폐기) |
| context compression | context compression | context compression(문맥 압축) | 2 | 원어 우선(이전 표기 `문맥 압축` 폐기) |
| Naive RAG | Naive RAG | Naive RAG | 2 | 원어 우선(이전 표기 `나이브 RAG` 폐기) |
| Advanced RAG | Advanced RAG | Advanced RAG | 2 | 원어 우선(이전 표기 `어드밴스드 RAG` 폐기) |
| Modular RAG | Modular RAG | Modular RAG | 2 | 원어 우선(이전 표기 `모듈형 RAG` 폐기) |
| fine-tuning | fine-tuning | fine-tuning(미세 조정) | 1 | 원어 우선(이전 표기 `미세 조정` 폐기) |
| prompt engineering | 프롬프트 엔지니어링 | 프롬프트 엔지니어링(Prompt Engineering) | 2 | glossary-ko |
| metadata | 메타데이터 | 메타데이터(Metadata) | 3 | |
| knowledge graph | 지식 그래프 | 지식 그래프(Knowledge Graph, KG) | 3 | |
| hybrid retrieval | hybrid retrieval | hybrid retrieval(sparse와 dense를 섞은 검색) | 3 | 원어 우선(이전 표기 `하이브리드 검색` 폐기) |
| adapter | adapter | adapter(작은 추가 모듈) | 3 | 원어 우선(이전 표기 `어댑터` 폐기) |
| lost in the middle | Lost in the Middle | Lost in the Middle(긴 입력 가운데 정보를 놓치는 현상) | 4 | 원어 우선(이전 표기 `중간 망각` 폐기) |
| iterative retrieval | iterative retrieval | iterative retrieval(반복 검색) | 4 | 원어 우선(이전 표기 `반복 검색` 폐기) |
| recursive retrieval | recursive retrieval | recursive retrieval(재귀 검색) | 4 | 원어 우선(이전 표기 `재귀 검색` 폐기) |
| adaptive retrieval | adaptive retrieval | adaptive retrieval(필요할 때만 검색) | 4 | 원어 우선(이전 표기 `적응형 검색` 폐기) |
| reflection token | reflection token | reflection token(스스로 평가하는 특수 토큰) | 4 | 원어 우선(이전 표기 `성찰 토큰` 폐기) |
| multi-hop | multi-hop | multi-hop(여러 문서를 건너 추론) | 4 | 원어 우선(이전 표기 `다중 홉` 폐기) |
| context relevance | context relevance | context relevance(검색 문맥의 관련성) | 5 | 원어 우선(이전 표기 `문맥 관련성` 폐기) |
| answer faithfulness | faithfulness | faithfulness(답이 문맥에 충실한 정도) | 5 | 원어 우선(이전 표기 `답변 충실성` 폐기) |
| answer relevance | answer relevance | answer relevance(답이 질문에 맞는 정도) | 5 | 원어 우선(이전 표기 `답변 관련성` 폐기) |
| noise robustness | noise robustness | noise robustness(잡음 문서에 대한 강건성) | 5 | 원어 우선(이전 표기 `잡음 강건성` 폐기) |
| negative rejection | negative rejection | negative rejection(답이 없으면 답하지 않기) | 5 | 원어 우선(이전 표기 `부정 거부` 폐기) |
| information integration | information integration | information integration(여러 문서 정보 통합) | 5 | 원어 우선(이전 표기 `정보 통합` 폐기) |
| counterfactual robustness | counterfactual robustness | counterfactual robustness(틀린 문서에 속지 않기) | 5 | 원어 우선(이전 표기 `반사실 강건성` 폐기) |
| benchmark | 벤치마크 | 벤치마크(Benchmark) | 5 | glossary-ko |
| long context | long context | long context(긴 입력 문맥) | 6 | 원어 우선(이전 표기 `긴 문맥` 폐기) |
| scaling law | scaling law | scaling law(규모 법칙) | 6 | 원어 우선(이전 표기 `스케일링 법칙` 폐기) |
| multimodal | 멀티모달 | 멀티모달(Multimodal) | 6 | glossary-ko |
| retriever | retriever | retriever(검색기) | 2 | 원어 우선 |
| generator | generator | generator(생성기) | 2 | 원어 우선 |
