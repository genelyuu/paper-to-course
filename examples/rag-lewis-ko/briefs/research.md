# 확인된 출처와 수치

**규칙**: 수치·주장은 이 파일에 있는 것만 쓴다. 없는 수치는 만들지 말고, 자체 예시 값은 "예시"라고 밝힌다. 원 논문 텍스트 추출본: `/private/tmp/claude-501/-Users-eugene-dev-paper2contents/365a5151-f96b-49fa-bdcf-a9f50729bb5e/scratchpad/lewis/p.txt` (arXiv 2005.11401v4, NeurIPS 2020). 필요하면 직접 grep 한다. 조사 시점: 2026년 11월.

## 원 논문: Lewis et al. 2020, https://arxiv.org/abs/2005.11401
- **초록·1절 문제**: 사전학습 언어 모델은 파라미터에 사실 지식을 저장하지만(암묵적 지식 베이스), ① 기억을 쉽게 늘리거나 고치지 못하고 ② 예측의 근거를 보여 주지 못하며 ③ 환각을 낸다. 지식 집약 과제에서는 과제 전용 구조보다 뒤처진다.
- **1절 선행 하이브리드**: REALM, ORQA는 masked language model과 미분 가능한 retriever를 묶었지만 **오픈 도메인 추출형 QA만** 다뤘다. 이 논문은 이를 "NLP의 일꾼"인 seq2seq 모델로 넓힌다.
- **1절 차이**: memory network 등 이전 외부 기억 구조는 과제별로 처음부터 학습했다. RAG는 parametric·non-parametric 기억 **둘 다 사전학습되어 지식이 미리 채워져** 있어 추가 학습 없이도 지식에 접근할 수 있다.
- **지식 집약 과제**: 사람도 외부 지식원 없이는 합리적으로 해낼 수 없는 과제.
- **2절 구성**: retriever $p_\eta(z|x)$(top-K로 자른 문서 분포), generator $p_\theta(y_i|x,z,y_{1:i-1})$. 검색 문서를 **잠재 변수**로 보고 주변화해 end-to-end 학습.
- **식 RAG-Sequence**: $p_{\text{RAG-Sequence}}(y|x) \approx \sum_{z\in \text{top-}k(p(\cdot|x))} p_\eta(z|x)\, p_\theta(y|x,z) = \sum_{z} p_\eta(z|x)\prod_{i}^{N} p_\theta(y_i|x,z,y_{1:i-1})$ — 답 전체에 같은 문서.
- **식 RAG-Token**: $p_{\text{RAG-Token}}(y|x) \approx \prod_{i}^{N}\sum_{z\in \text{top-}k(p(\cdot|x))} p_\eta(z|x)\, p_\theta(y_i|x,z,y_{1:i-1})$ — 토큰마다 다른 문서. 분류(출력 길이 1)에서는 두 모델이 같다.
- **2.2 DPR**: bi-encoder. $p_\eta(z|x) \propto \exp(\mathbf{d}(z)^\top \mathbf{q}(x))$, $\mathbf{d}(z)=\text{BERT}_d(z)$, $\mathbf{q}(x)=\text{BERT}_q(x)$, 둘 다 BERT-base. top-k는 MIPS 문제이며 준선형 시간에 근사 풀이. DPR 사전학습 bi-encoder로 초기화하고 색인을 만듦. 이 retriever는 TriviaQA와 Natural Questions에서 답이 든 문서를 찾도록 학습되어 있음. 문서 색인 = non-parametric memory.
- **2.3 BART**: BART-large, 400M 파라미터 seq2seq 트랜스포머. 입력 $x$와 검색 문서 $z$를 **단순히 이어 붙여** 넣음. 잡음 제거 목표로 사전학습. generator 파라미터 $\theta$ = parametric memory.
- **2.4 학습**: 어떤 문서를 검색해야 하는지 직접 감독 없이 retriever와 generator를 함께 학습. 손실 $\sum_j -\log p(y_j|x_j)$(음의 주변 로그 가능도), Adam. 문서 인코더 $\text{BERT}_d$를 갱신하면 색인을 주기적으로 다시 만들어야 해 비싸므로(REALM이 사전학습 중 하는 방식) **문서 인코더와 색인은 고정**, query encoder $\text{BERT}_q$와 BART만 fine-tuning.
- **2.5 디코딩**: RAG-Token은 전이 확률 $p'_\theta(y_i|x,y_{1:i-1})=\sum_z p_\eta(z_i|x)p_\theta(y_i|x,z_i,y_{1:i-1})$을 일반 beam decoder에 넣으면 됨. RAG-Sequence는 토큰 단위로 나뉘지 않아 문서마다 beam search → 가설 집합 $Y$ → 어떤 문서의 beam에 없던 가설은 그 문서로 추가 forward pass를 돌려 확률을 구해 합산(**Thorough Decoding**). 출력이 길면 $|Y|$가 커져 비싸므로, beam에 없던 경우 $p_\theta(y|x,z_i)\approx 0$으로 근사(**Fast Decoding**).
- **3절 공통 설정**: 위키백과 2018년 12월 덤프. 문서를 겹치지 않는 **100단어 청크**로 잘라 **2,100만(21M) 문서**. 문서 인코더로 임베딩 → FAISS의 HNSW 근사로 MIPS 색인 하나. 학습 때 $k\in\{5,10\}$, 테스트 $k$는 dev로 정함.
- **3.1 오픈 도메인 QA**: NQ, TriviaQA(TQA), WebQuestions(WQ), CuratedTrec(CT). CT·WQ는 작아서 NQ RAG 모델로 초기화. 지표 EM. TQA는 T5와 비교하려고 TQA-Wiki 테스트셋도 평가. 비교: 추출형 QA(non-parametric 중심), closed-book QA(parametric만).
- **3.2 생성형 QA**: MS MARCO NLG v2.1. 제공 gold 문단은 쓰지 않고 질문·답만 씀 → 오픈 도메인 생성형 QA. 일부 질문은 gold 문단 없이는 참조 답과 맞출 수 없음(예: "What is the weather in Volcano, CA?"), 일부는 위키백과만으로 답할 수 없음.
- **3.3 Jeopardy 질문 생성**: 답(개체)을 주고 그 개체를 가리키는 사실 문장형 질문 생성. 예: 답 "The World Cup" ↔ "In 1986 Mexico scored as the first country to host this international sports competition twice." SearchQA 분할 100K/14K/27K. 비교용 BART 학습. 지표 SQuAD 튜닝 Q-BLEU-1(개체 일치에 가중, 질문 생성에서 사람 판단과 상관 높음). 사람 평가 2종(사실성, 구체성), 쌍대 비교, 4지선다(A 낫다/B 낫다/둘 다 좋다/둘 다 나쁘다).
- **3.4 FEVER**: 주장이 위키백과로 지지/반박/정보 부족인지 분류. 레이블을 출력 토큰 하나로 매핑. **검색 증거 감독을 쓰지 않음**. 3-way와 2-way(supports/refutes), 지표 레이블 정확도.
- **표 1 (오픈 도메인 QA 테스트 EM; TQA는 "표준 / TQA-Wiki")**
  | 구분 | 모델 | NQ | TQA | WQ | CT |
  |---|---|---|---|---|---|
  | closed-book | T5-11B | 34.5 | - / 50.1 | 37.4 | - |
  | closed-book | T5-11B+SSM | 36.6 | - / 60.5 | 44.7 | - |
  | open-book | REALM | 40.4 | - / - | 40.7 | 46.8 |
  | open-book | DPR | 41.5 | 57.9 / - | 41.1 | 50.6 |
  | | RAG-Token | 44.1 | 55.2 / 66.1 | 45.5 | 50.0 |
  | | RAG-Seq. | 44.5 | 56.8 / 68.0 | 45.2 | 52.2 |
- 4.1: 네 과제 모두 새 최고 성능(TQA는 T5 비교 분할에서만). REALM·T5+SSM과 달리 비싼 salient span masking 사전학습 없이 달성. 단, RAG의 retriever는 NQ·TQA 검색 감독을 쓴 DPR로 초기화. DPR QA 시스템(BERT cross-encoder reranker + 추출형 reader)보다 낫다 → reranker도 추출형 reader도 필수가 아님. 답이 그대로 들어 있지 않고 단서만 있는 문서도 생성에 기여. **검색 문서 어디에도 정답이 없을 때도 NQ에서 11.8%를 맞힘**(추출형은 0%).
- **표 2 (생성·분류 테스트)**
  | 모델 | Jeopardy B-1 | Jeopardy QB-1 | MSMARCO R-L | MSMARCO B-1 | FEVER-3 | FEVER-2 |
  |---|---|---|---|---|---|---|
  | SotA | - | - | 49.8* | 49.9* | 76.8 | 92.2* |
  | BART | 15.1 | 19.7 | 38.2 | 41.6 | 64.0 | 81.1 |
  | RAG-Tok. | 17.3 | 22.2 | 40.1 | 41.5 | 72.5 | 89.5 |
  | RAG-Seq. | 14.7 | 21.4 | 40.8 | 44.2 | (분류에서는 RAG-Tok.과 같음) | |
  *는 gold 문맥/증거를 쓴 모델. MSMARCO SotA는 [4], FEVER-3 SotA는 [68], FEVER-2는 Thorne and Vlachos [57].
- 4.2: RAG-Sequence가 Open MS-MARCO NLG에서 BART보다 BLEU 2.6점, ROUGE-L 2.6점 높음. 정성적으로 RAG가 환각이 적음.
- **표 3 예시**(MS-MARCO "define middle ear"): BART "?The middle ear is the part of the ear between the middle ear and the nose." / RAG-T "The middle ear is the portion of the ear internal to the eardrum." / RAG-S "The middle ear includes the tympanic cavity and the three ossicles." Jeopardy "The Divine Comedy": BART "*This epic poem by Dante is divided into 3 parts: the Inferno, the Purgatorio & the Purgatorio" / RAG-S "This 14th century work is divided into 3 sections: "Inferno", "Purgatorio" & "Paradiso"". (? = 사실과 다름, * = 부분적으로 맞음)
- 4.3 + **표 4 (Jeopardy 사람 평가, BART vs RAG-Token, 452쌍)**: 사실성 — BART 나음 7.1%, RAG 나음 42.7%, 둘 다 좋음 11.7%, 둘 다 나쁨 17.7%, 다수 없음 20.8%. 구체성 — 16.8%, 37.4%, 11.8%, 6.9%, 20.1%. (본문은 "both factual 17%"라고 적어 표와 다름. 표 수치를 쓴다.) Jeopardy에서는 RAG-Token이 RAG-Sequence보다 좋음 → 여러 문서 내용을 합치는 데 유리하다고 해석.
- **그림 2 (Hemingway 예, 문서 5개)**: "A Farewell to Arms"를 생성할 때 문서 1(그 소설이 언급됨)의 사후 확률이 높고, "The Sun Also Rises"를 생성할 때 문서 2가 높음. 각 제목의 **첫 토큰 뒤에는 문서 사후 확률이 평평해짐** → 나머지 제목은 parametric memory로 완성. BART에 "The Sun만 주면 "The Sun Also Rises"를 완성함. non-parametric 기억이 parametric 기억 속 지식을 "끌어내는" 역할.
- 4.4: FEVER-3은 최고 성능과 4.3% 차이 이내(최고 성능은 검색 감독을 쓴 복잡한 파이프라인). FEVER-2는 gold 증거 문장을 받은 RoBERTa와 2.7% 차이 이내. RAG의 top-1 문서가 gold 문서인 경우 71%, top-10 안에 gold 문서가 있는 경우 90%.
- **표 5 (서로 다른 trigram 비율)**: MSMARCO — Gold 89.6%, BART 70.7%, RAG-Token 77.8%, RAG-Seq. 83.5%. Jeopardy — Gold 90.0%, BART 32.4%, RAG-Token 46.8%, RAG-Seq. 53.8%. 다양성 촉진 디코딩 없이 얻은 결과.
- **표 6 (dev 제거 실험)**
  | 모델 | NQ | TQA | WQ | CT | Jeo B-1 | Jeo QB-1 | MS R-L | MS B-1 | FVR-3 | FVR-2 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | RAG-Token-BM25 | 29.7 | 41.5 | 32.1 | 33.1 | 17.5 | 22.3 | 55.5 | 48.4 | 75.1 | 91.6 |
  | RAG-Sequence-BM25 | 31.8 | 44.1 | 36.6 | 33.8 | 11.1 | 19.5 | 56.5 | 46.9 | | |
  | RAG-Token-Frozen | 37.8 | 50.1 | 37.1 | 51.1 | 16.7 | 21.7 | 55.9 | 49.4 | 72.9 | 89.4 |
  | RAG-Sequence-Frozen | 41.2 | 52.1 | 41.8 | 52.6 | 11.8 | 19.6 | 56.7 | 47.3 | | |
  | RAG-Token | 43.5 | 54.8 | 46.5 | 51.9 | 17.9 | 22.6 | 56.2 | 49.4 | 74.5 | 90.6 |
  | RAG-Sequence | 44.0 | 55.8 | 44.9 | 53.4 | 15.3 | 21.5 | 57.2 | 47.5 | | |
  FEVER 열은 분류라 두 모델이 같아 한 값만 있음. 해석(논문): 학습한 retrieval이 모든 과제에서 결과를 높임. FEVER는 BM25가 가장 좋음(주장이 개체 중심이라 단어 일치 검색에 잘 맞는다고 추정). 오픈 도메인 QA에서는 미분 가능한 retrieval이 결정적.
- **index hot-swapping**: 2016년 12월 DrQA 위키 덤프 색인 vs 2018년 12월 색인. 두 시점 사이 바뀐 세계 지도자 82명, 템플릿 "Who is {position}?"(예: "Who is the President of Peru?"). 2016 색인+2016 지도자 70%, 2018 색인+2018 지도자 68%. 어긋나면 낮음: 2018 색인+2016 지도자 12%, 2016 색인+2018 지도자 4%. → non-parametric 기억을 바꾸는 것만으로 지식 갱신, 재학습 불필요.
- **검색 문서 수**: 학습 때 5개와 10개는 큰 차이 없음. 테스트 때 문서를 늘리면 RAG-Sequence의 NQ 성능은 단조 증가, RAG-Token은 10개에서 정점(그림 3 왼쪽). MS-MARCO에서는 문서가 늘면 RAG-Token의 ROUGE-L은 오르고 BLEU-1은 내려감, RAG-Sequence는 효과가 덜함(그림 3 오른쪽). 그림 3 가운데는 NQ Answer Recall@K(RAG-Tok, RAG-Seq, Fixed DPR, BM25) — 그림의 정확한 점 값은 텍스트로 확인되지 않았으므로 **경향만** 쓰고 수치를 읽어 내지 않는다.
- **부록 A**: 오픈 도메인 QA 테스트 수치는 RAG-Token 15개 문서, RAG-Sequence 50개 문서 + Thorough Decoding, QA는 greedy decoding(beam이 도움 안 됨). MSMARCO·Jeopardy는 두 모델 모두 10개 문서, beam 4, RAG-Sequence는 Fast Decoding(Thorough가 성능을 높이지 않음).
- **부록 C**: Fairseq, mixed precision, 32GB V100 GPU 8개로 학습(학습·추론은 GPU 1개로도 가능). MIPS는 CPU에서 충분히 빨라 색인 벡터를 CPU에 둠 → 위키백과 전체에 CPU 메모리 약 100 GB. FAISS 압축으로 36 GB까지 줄임. HuggingFace Transformers로 이식.
- **부록 F (null document)**: 검색할 쓸모 있는 정보가 없는 경우를 위해 빈 문서를 하나 더 두는 방법을 세 가지로 시도했으나 성능이 오르지 않아 뺌. Open MS-MARCO에서는 검색이 덜 도움 되는 질문에 특정 문서 묶음을 늘 검색하도록 학습됨.
- **부록 G (파라미터)**: DPR BERT-base query·document 인코더 각 110M(문서 인코더는 학습하지 않음) + BART-large 406M = 학습 가능 파라미터 총 626M. closed-book 최고인 T5-11B는 110억. 비슷한 크기의 T5-large(770M)는 NQ 28.9 EM으로 RAG-Sequence 44.5보다 크게 낮음. 색인은 학습 파라미터가 아니며 2,100만 개 벡터, 153억 개 값(논문은 728차원이라 적었으나 BERT-base 출력은 768차원이므로 차원 수는 본문에 쓰지 않는다). 8비트로 저장 가능.
- **부록 H (retrieval collapse)**: 이야기 생성 같은 일부 과제에서 retriever가 입력과 무관하게 같은 문서만 검색하도록 붕괴 → generator가 문서를 무시 → BART와 같아짐. 원인으로 사실 지식 요구가 덜 명시적이거나 목표 문장이 길어 retriever에 가는 기울기 정보가 약할 가능성을 듦.
- **표 7 (데이터 수)**: NQ 79,169/8,758/3,611, TQA 78,786/8,838/11,314, WQ 3,418/362/2,033, CT 635/134/635, Jeopardy 97,392/13,714/26,849, MS-MARCO 153,726/12,468/101,093*, FEVER-3 145,450/10,000/10,000, FEVER-2 96,966/6,666/6,666.
- **5절 관련 연구 요지**: 과제별 검색(오픈 도메인 QA, 사실 검증, 대화, 번역, 언어 모델링 등)의 성공을 하나의 구조로 통합. GPT-2·BART·T5 같은 범용 사전학습 모델은 검색 없이 성공. 학습형 retrieval(검색·강화 학습·잠재 변수 [ORQA, REALM]). memory network와 달리 기억이 **원문 텍스트**라 사람이 읽을 수 있고(해석 가능) 사람이 고쳐 쓸 수 있음(색인 편집으로 갱신). retrieve-and-edit와 달리 여러 문서를 모으고 잠재 검색을 학습하며 증거 문서를 검색.
- **6절 향후 과제**: 두 구성 요소를 처음부터 함께 사전학습하는 방법, 두 기억의 상호작용.
- **Broader Impact**: 환각 감소, 통제·해석 가능성. 위키백과도 완전히 사실적이거나 편향이 없지 않음. GPT-2와 비슷한 오남용 우려.

## 선행 연구 (2단원; 저자 이름·연도·핵심만, 수치는 원 논문 표 1에서 가져온 것만)
- DrQA: Chen et al. 2017, https://arxiv.org/abs/1704.00051 — 위키백과 TF-IDF 검색 + 추출형 reader("retrieve-and-extract"의 대표).
- LAMA: Petroni et al. 2019, https://arxiv.org/abs/1909.01066 — 사전학습 언어 모델이 빈칸 질의로 사실 지식을 꺼낼 수 있음을 보임(원 논문 [47]).
- T5 closed-book QA: Roberts, Raffel, Shazeer 2020 "How Much Knowledge Can You Pack Into the Parameters of a Language Model?", https://arxiv.org/abs/2002.08910 — 검색 없이 파라미터만으로 답함. SSM으로 성능 향상.
- ORQA: Lee, Chang, Toutanova 2019, https://arxiv.org/abs/1906.00300 — 검색을 잠재 변수로 둔 오픈 도메인 추출형 QA.
- REALM: Guu et al. 2020, https://arxiv.org/abs/2002.08909 — 검색을 넣은 MLM 사전학습, 사전학습 중 색인을 주기적으로 갱신, 추출형 QA.
- DPR: Karpukhin et al. 2020, https://arxiv.org/abs/2004.04906 — BERT bi-encoder dense retrieval, 오픈 도메인 QA에서 BM25를 넘어섬.
- BART: Lewis et al. 2019, https://arxiv.org/abs/1910.13461 — 잡음 제거 seq2seq 사전학습.
- Memory Networks: Weston, Chopra, Bordes 2014, https://arxiv.org/abs/1410.3916; End-to-End Memory Networks: Sukhbaatar et al. 2015, https://arxiv.org/abs/1503.08895.
- 환각: 원 논문 [38] Maynez et al. 2020, https://arxiv.org/abs/2005.00661 (요약 생성의 사실성).

## 이후 동향 (7단원) — C 담당이 WebFetch로 원문(초록)을 확인한 뒤 아래에 추가하고 쓴다. 확인 못 한 항목은 쓰지 않는다.
- 후보: FiD(Izacard & Grave 2020, https://arxiv.org/abs/2007.01282), RETRO(Borgeaud et al. 2021, https://arxiv.org/abs/2112.04426), Atlas(Izacard et al. 2022, https://arxiv.org/abs/2208.03299), REPLUG(Shi et al. 2023, https://arxiv.org/abs/2301.12652), In-Context RALM(Ram et al. 2023, https://arxiv.org/abs/2302.00083), Self-RAG(Asai et al. 2023, https://arxiv.org/abs/2310.11511), RAG 서베이(Gao et al. 2023, https://arxiv.org/abs/2312.10997; 같은 저장소의 `examples/rag-survey-ko` 강의로 이어짐).

### C 담당 확인 결과 (2026년 11월, arXiv 초록 WebFetch + 필요한 곳은 PDF 본문 확인)
| 연구 | 출처 | 확인한 주장·수치 | RAG(2020)의 어느 칸에서 나왔나 |
|---|---|---|---|
| FiD | Izacard & Grave 2020, https://arxiv.org/abs/2007.01282 | 초록: 생성형 QA 모델이 검색 문단에서 이득을 봄, NQ·TriviaQA 최고 성능, **검색 문단 수를 늘릴수록 성능이 크게 오름** → 여러 문단의 증거를 결합. 본문 3절: 문단마다 질문과 이어 붙여 **인코더가 문단별로 따로** 처리하고, **디코더가 모든 문단 표현을 이어 붙인 것에 어텐션** → "Fusion-in-Decoder". 인코더에서 따로 처리하므로 계산 시간이 문단 수에 **선형**으로 늘어남(제곱 아님). 표 1: FiD(large) NQ EM 51.4(같은 표의 RAG 44.5). 표 2: 학습 문단 5~100개. | RAG는 문서마다 따로 생성하고 확률로 섞음(주변화) → FiD는 디코더 안에서 여러 문서를 한꺼번에 읽음 |
| RETRO | Borgeaud et al. 2021, https://arxiv.org/abs/2112.04426 | 초록: 앞 토큰과의 국소 유사도로 검색한 문서 청크로 자기회귀 LM을 조건화. **2조 토큰 데이터베이스**, Pile에서 GPT-3·Jurassic-1과 비슷한 성능을 **25배 적은 파라미터**로. **고정(frozen) BERT retriever** + 미분 가능한 인코더 + **chunked cross-attention**. 본문: 검색 데이터 양에 선형인 시간 복잡도, 질문 답 청크 64토큰, MassiveText 색인 93 TB(위키 215 GB), 평가 데이터 **누출(leakage)** 이 성능 향상의 일부라고 밝힘. | RAG의 "작은 생성기 + 큰 외부 기억" 아이디어를 사전학습 언어 모델 규모(2조 토큰)로 확장. retriever는 RAG처럼 학습하지 않고 고정 |
| Atlas | Izacard et al. 2022, https://arxiv.org/abs/2208.03299 | 초록: 사전학습한 검색 증강 LM, 적은 예시로 지식 집약 과제 학습, 문서 색인을 쉽게 갱신. **NQ 예시 64개로 42% 넘는 정확도**, 540B 모델보다 3%p 높고 파라미터는 50배 적음. 본문: Contriever(dual-encoder) retriever + FiD 구조 seq2seq, 11B, retriever와 LM을 **함께 사전학습**하는 것이 few-shot에 결정적. 2.4절: retriever를 학습하면 색인 임베딩이 낡아 **주기적 재색인 필요, 비쌈**(3,700만 문서·배치 64·문서 20개·1,000단계마다 갱신이면 약 30% 추가 비용). 대안: 재순위화, **query-side fine-tuning(문서 인코더 고정 = RAG 방식)**. | RAG가 비용 때문에 고정한 문서 인코더 칸(6절 향후 과제: 처음부터 함께 사전학습)을 정면으로 다룸 |
| REPLUG | Shi et al. 2023, https://arxiv.org/abs/2301.12652 | 초록: LM을 블랙박스로 두고 조정 가능한 retriever를 붙임. 검색 문서를 **고정된 블랙박스 LM 입력 앞에 붙임**, LM 출력으로 retriever 학습(REPLUG LSR). GPT-3(175B) 언어 모델링 6.3%, Codex 5-shot MMLU 5.1% 향상. 본문: 문서마다 **따로** 입력 앞에 붙여 여러 번 실행하고 출력 확률을 **가중 평균 앙상블** → 계산을 정확도와 맞바꿈. | RAG-Sequence식 문서별 주변화를 생성기 학습 없이(블랙박스) 적용 |
| In-Context RALM | Ram et al. 2023, https://arxiv.org/abs/2302.00083 | 초록: 기존 RALM은 LM 구조를 바꿔 배포가 복잡 → **구조를 그대로 두고 추가 학습 없이** 검색 문서를 입력 앞에 붙임. 기성 retriever로 모델 크기·말뭉치 전반에서 큰 향상, 순위 매기기를 특화하면 추가 향상. 본문: 기성 BM25로 LM 파라미터 2~3배 증가에 해당하는 향상, 검색 간격(stride)을 줄일수록 좋지만 실행 시간과 맞바꿈. | RAG의 "생성기를 함께 fine-tuning" 칸을 없앰(학습 0) |
| Self-RAG | Asai et al. 2023, https://arxiv.org/abs/2310.11511 | 초록: 필요와 무관하게 **고정 개수 문단을 늘 검색**하면 LM의 범용성이 떨어지거나 도움 안 되는 응답이 나옴 → 필요할 때만(on-demand) 검색하고, **reflection token**으로 검색 문단과 자기 출력을 평가. 7B·13B가 ChatGPT, 검색 증강 Llama2-chat보다 오픈 도메인 QA·추론·사실 검증에서 나음. 본문 표 1: 토큰 4종 Retrieve(검색 여부), IsRel(문단 관련성), IsSup(출력이 문단에 뒷받침되는가), IsUse(유용성 1~5). GPT-4로 라벨 4k~20k개를 만들어 critic 모델(Llama 2-7B)을 학습한 뒤 생성기 학습 → 별도 critic 학습 비용, GPT-4 의존. | RAG는 모든 입력에 top-$k$ 검색(null document 시도 실패, 부록 F) → 검색 여부 자체를 모델이 결정 |
| RAG 서베이 | Gao et al. 2023, https://arxiv.org/abs/2312.10997 | 초록: LLM의 환각, 낡은 지식, 불투명한 추론을 외부 DB로 보완하는 RAG를 정리. Naive, Advanced, Modular 세 패러다임, 검색·생성·증강 구성 요소, 평가, 과제. | 같은 저장소 `examples/rag-survey-ko` 강의 |
- 보충 링크 확인(2026-11): HuggingFace RAG 문서 열림(RagSequenceForGeneration 예시, 색인 교체로 지식 갱신 언급). Meta AI 블로그(2020-09-28) 열림.

## 보충자료 링크
- HuggingFace RAG 문서: https://huggingface.co/docs/transformers/model_doc/rag
- 논문 코드: https://github.com/huggingface/transformers/tree/main/examples/research_projects/rag (원 논문 각주는 master/examples/rag)
- Meta AI 블로그 "Retrieval Augmented Generation: Streamlining the creation of intelligent natural language processing models" (2020): https://ai.meta.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models/ — 링크가 열리는지 확인한 뒤 쓴다.
