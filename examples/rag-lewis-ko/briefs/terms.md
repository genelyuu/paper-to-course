# 강의 용어표: RAG (Lewis et al. 2020, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks)

모든 모듈은 이 표의 표기만 쓴다. 원어 우선 규칙(SKILL.md "용어 표기")에 따라 국내 연구자·실무자가 영어로 말하는 개념어는 원어를 본문 표기로 쓰고, 첫 등장에만 한글 뜻을 괄호로 단다. 모듈마다 첫 등장에서 다시 병기하고 툴팁을 단다. `examples/rag-survey-ko/briefs/terms.md`와 표기를 맞췄다.

| English | 한국어 표기 | 첫 등장 표기 | 처음 나오는 모듈 | 비고 |
|---|---|---|---|---|
| retrieval-augmented generation | RAG | 검색 증강 생성(Retrieval-Augmented Generation, RAG) | 1 | 이후 `RAG` |
| RAG-Sequence / RAG-Token | RAG-Sequence / RAG-Token | RAG-Sequence(답 전체에 같은 문서를 씀), RAG-Token(토큰마다 다른 문서를 쓸 수 있음) | 1 | 논문 모델 이름, 원어 |
| knowledge-intensive task | 지식 집약 과제 | 지식 집약 과제(Knowledge-Intensive Task) | 1 | 사람도 외부 자료 없이는 풀기 어려운 과제 |
| parametric memory | parametric memory | parametric memory(모델 파라미터에 저장된 기억) | 1 | 원어 우선. 서베이 강의의 parametric knowledge와 같은 계열 |
| non-parametric memory | non-parametric memory | non-parametric memory(외부 문서 색인에 있는 기억) | 1 | 원어 우선 |
| pre-trained language model | 사전학습 언어 모델 | 사전학습 언어 모델(Pre-trained Language Model) | 1 | `사전학습` 붙여 씀 |
| sequence-to-sequence | seq2seq | seq2seq(Sequence-to-Sequence, 입력 문장을 출력 문장으로 바꾸는 모델) | 1 | 원어 약어 |
| hallucination | 환각 | 환각(Hallucination) | 1 | glossary-ko |
| provenance | 근거 출처 | 근거 출처(Provenance) | 1 | 답의 근거가 된 문서 |
| retriever / generator | retriever / generator | retriever(검색기), generator(생성기) | 1 | 원어 우선 |
| query | query | query(검색 질의) | 1 | 원어 우선 |
| query encoder / document encoder | query encoder / document encoder | query encoder(질의 인코더), document encoder(문서 인코더) | 1 | 원어 우선. 기호 $q(x)$, $d(z)$ |
| document index | 문서 색인 | 문서 색인(Document Index) | 1 | indexing은 `indexing(색인 구축)` |
| dense retrieval / sparse retrieval | dense retrieval / sparse retrieval | dense retrieval(임베딩 벡터 기반 검색), sparse retrieval(단어 일치 기반 검색) | 1 | 원어 우선 |
| embedding | 임베딩 | 임베딩(Embedding) | 1 | |
| dot product / inner product | 내적 | 내적(Inner Product) | 1 | |
| Maximum Inner Product Search | MIPS | MIPS(Maximum Inner Product Search, 최대 내적 검색) | 1 | |
| bi-encoder / cross-encoder | bi-encoder / cross-encoder | bi-encoder(query와 문서를 따로 임베딩), cross-encoder(query와 문서를 함께 읽고 점수) | 2 | |
| Dense Passage Retriever | DPR | DPR(Dense Passage Retriever) | 1 | 고유 명칭 |
| BART | BART | BART(잡음 제거로 사전학습한 seq2seq 모델) | 1 | 고유 명칭 |
| BERT | BERT | BERT(양방향 인코더 사전학습 모델) | 1 | 고유 명칭 |
| T5 | T5 | T5(Text-to-Text Transfer Transformer) | 2 | 고유 명칭 |
| latent variable | 잠재 변수 | 잠재 변수(Latent Variable) | 1 | |
| marginalization | 주변화 | 주변화(Marginalization) | 1 | 여러 경우의 확률을 가중합해 변수를 없앰. "주변화한다" |
| marginal likelihood | 주변 가능도 | 주변 가능도(Marginal Likelihood) | 4 | 손실은 `음의 주변 로그 가능도` |
| likelihood | 가능도 | 가능도(Likelihood) | 1 | glossary 기본값 |
| prior / posterior | 사전 확률 / 사후 확률 | 사전 확률(Prior), 사후 확률(Posterior) | 3 | |
| top-k | top-*k* | top-*k*(상위 $k$개) | 1 | 원어 우선 |
| end-to-end training | end-to-end 학습 | end-to-end 학습(입력부터 출력까지 한 번에 학습) | 1 | |
| fine-tuning | fine-tuning | fine-tuning(미세 조정) | 1 | 원어 우선 |
| pre-training | 사전학습 | 사전학습(Pre-training) | 1 | |
| closed-book / open-book | closed-book / open-book | closed-book(클로즈드북, 외운 지식만으로 답하기), open-book(오픈북, 자료를 찾아 읽고 답하기) | 2 | 원어 우선 |
| extractive / abstractive | 추출형 / 생성형 | 추출형(Extractive, 문서에서 답 구간을 골라냄), 생성형(Abstractive, 답을 새로 써냄) | 2 | |
| retrieve-and-extract | retrieve-and-extract | retrieve-and-extract(검색한 뒤 답 구간 추출) | 2 | 원어 우선 |
| reader | reader | reader(검색 문서에서 답을 읽어 내는 모델) | 2 | 원어 우선 |
| salient span masking | salient span masking | salient span masking(SSM, 개체·날짜 같은 핵심 구간만 가리는 사전학습) | 2 | 원어 우선 |
| masked language model | MLM | MLM(Masked Language Model, 가린 단어 맞히기 모델) | 2 | |
| memory network | memory network | memory network(외부 기억을 읽고 쓰는 신경망) | 2 | 원어 우선 |
| retrieve-and-edit | retrieve-and-edit | retrieve-and-edit(비슷한 예를 찾아 고쳐 쓰기) | 2 | 원어 우선 |
| open-domain question answering | 오픈 도메인 질의응답 | 오픈 도메인 질의응답(Open-Domain QA) | 1 | 이후 `오픈 도메인 QA` 허용 |
| question generation | 질문 생성 | 질문 생성(Question Generation) | 5 | |
| fact verification | 사실 검증 | 사실 검증(Fact Verification) | 1 | |
| beam search | beam search | beam search(빔 탐색) | 4 | 원어 우선 |
| greedy decoding | greedy decoding | greedy decoding(매 단계 가장 높은 토큰 선택) | 4 | 원어 우선 |
| Thorough Decoding / Fast Decoding | Thorough Decoding / Fast Decoding | Thorough Decoding(빠진 후보도 다시 계산), Fast Decoding(빠진 후보는 확률 0으로 근사) | 4 | 논문 고유 명칭 |
| autoregressive | 자기회귀 | 자기회귀(Autoregressive) | 3 | |
| FAISS / HNSW | FAISS / HNSW | FAISS(벡터 검색 라이브러리), HNSW(Hierarchical Navigable Small World, 그래프 기반 근사 최근접 탐색) | 4 | 고유 명칭 |
| approximate nearest neighbor | 근사 최근접 이웃 탐색 | 근사 최근접 이웃 탐색(Approximate Nearest Neighbor, ANN) | 4 | |
| chunk | 청크 | 청크(Chunk) | 5 | 논문은 100단어 단위 문서 |
| exact match | EM | exact match(완전 일치, EM) | 5 | 이후 `EM` |
| BLEU / ROUGE-L / Q-BLEU | BLEU / ROUGE-L / Q-BLEU | BLEU-1(겹치는 단어 비율 기반 지표), ROUGE-L(최장 공통 부분열 기반 지표), Q-BLEU-1(개체 일치에 가중치를 둔 BLEU) | 5 | 지표 이름 원어 |
| label accuracy | 레이블 정확도 | 레이블 정확도(Label Accuracy) | 5 | |
| human evaluation | 사람 평가 | 사람 평가(Human Evaluation) | 6 | |
| factuality / specificity | 사실성 / 구체성 | 사실성(Factuality), 구체성(Specificity) | 6 | |
| diversity (distinct n-gram) | 다양성 | 다양성(Diversity, 서로 다른 n-gram의 비율) | 6 | |
| ablation study | 제거 실험 | 제거 실험(Ablation Study) | 6 | glossary-ko |
| index hot-swapping | index hot-swapping | index hot-swapping(색인 교체로 지식 갱신) | 6 | 원어 우선 |
| retrieval collapse | retrieval collapse | retrieval collapse(입력과 무관하게 같은 문서만 검색하는 현상) | 6 | 원어 우선 |
| null document | null document | null document(빈 문서) | 6 | 부록 F |
| baseline | 기준선 | 기준선(Baseline) | 2 | 사용자 지정. "기준 방법", "기준 모델"로 바꾸지 않음 |
| state of the art | 최고 성능 | 최고 성능(State of the Art) | 1 | glossary-ko |
| benchmark | 벤치마크 | 벤치마크(Benchmark) | 5 | |
| recall@k | Recall@$k$ | Recall@$k$(상위 $k$개 안에 정답 문서가 있는 비율) | 6 | |
| Fusion-in-Decoder | FiD | FiD(Fusion-in-Decoder) | 7 | 고유 명칭 |
| large language model | LLM | 대규모 언어 모델(Large Language Model, LLM) | 7 | |
| in-context learning | in-context learning | in-context learning(문맥 내 학습, ICL) | 7 | 원어 우선 |
| reflection token | reflection token | reflection token(스스로 평가하는 특수 토큰) | 7 | 원어 우선 |
| forward pass | forward pass | forward pass(순전파, 입력을 모델에 통과시켜 출력을 계산하는 일) | 4 | 원어 우선(B 보고로 추가) |
| Adam | Adam | Adam(적응형 학습률 최적화 알고리즘) | 4 | 고유 명칭 |
| softmax | softmax | softmax(소프트맥스, 점수를 합이 1인 확률로 바꾸는 함수) | 4 | 원어 우선 |
| transition probability | 전이 확률 | 전이 확률(Transition Probability) | 4 | 디코딩 한 단계에서 다음 토큰의 확률 |
| sub-linear | 준선형 | 준선형(Sub-Linear) | 4 | 데이터 수보다 느리게 늘어나는 시간 |
| TF-IDF | TF-IDF | TF-IDF(단어 빈도와 희소성으로 매기는 가중치) | 2 | 고유 명칭(A 보고로 추가) |
| BM25 | BM25 | BM25(Best Matching 25, 단어 일치 기반 순위 함수) | 1 | 고유 명칭 |
| encoder / decoder | 인코더 / 디코더 | 인코더(Encoder), 디코더(Decoder) | 1 | 관용 음차 |
| reranker | reranker | reranker(재순위 모델) | 2 | 원어 우선 |
| Natural Questions | Natural Questions | Natural Questions(NQ) | 1 | 데이터셋 이름. 이후 `NQ` |
