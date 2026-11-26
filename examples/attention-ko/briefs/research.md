# 확인된 출처와 수치 (개정용, 2026-11)

**규칙**: 수치·주장은 이 파일에 있는 것만 쓴다. 없는 수치는 만들지 말고, 자체 예시 값은 "예시"라고 밝힌다. 원 논문 본문 텍스트 추출본: `/private/tmp/claude-501/-Users-eugene-dev-paper2contents/365a5151-f96b-49fa-bdcf-a9f50729bb5e/scratchpad/paper/p.txt` (arXiv 1706.03762v7, 필요하면 직접 grep).

## 원 논문: Vaswani et al. 2017, https://arxiv.org/abs/1706.03762
- 1절: 순환 모델은 $h_t$를 $h_{t-1}$과 위치 $t$의 입력으로 계산함. 이 순차성 때문에 한 예제 안에서 병렬화가 막히고, 문장이 길수록 메모리 제약으로 배치도 키우기 어려움. "순차 계산이라는 근본 제약은 남아 있다."
- 1절: 어텐션은 거리와 무관하게 의존을 모델링하게 해 주지만 "몇몇 경우를 빼면 순환 신경망과 함께 쓰였다."
- 2절: Extended Neural GPU, ByteNet, ConvS2S는 CNN으로 병렬 계산함. 두 위치를 잇는 연산 수가 거리에 따라 ConvS2S는 선형, ByteNet은 로그로 늘어남. 트랜스포머는 이를 상수로 줄이되, 평균을 내서 해상도가 떨어지는 문제는 멀티헤드로 보완함.
- 2절: 셀프 어텐션(intra-attention)은 한 시퀀스 안의 서로 다른 위치를 관련지어 표현을 만드는 것이고, 독해·요약·텍스트 함의·문장 표현에 이미 쓰였음. 트랜스포머는 RNN·합성곱 없이 셀프 어텐션만 쓴 첫 변환 모델임.
- 3.1절: 인코더 = 동일한 층 N=6개. 층마다 하위 층 2개(멀티헤드 셀프 어텐션, 위치별 FFN). 각 하위 층의 출력은 LayerNorm(x + Sublayer(x)). 잔차 연결을 위해 모든 하위 층과 임베딩의 출력 차원은 d_model=512.
- 3.1절: 디코더 = 동일한 층 N=6개. 세 번째 하위 층으로 인코더 스택 출력에 대한 멀티헤드 어텐션을 넣음. 디코더 셀프 어텐션은 뒤 위치를 보지 못하게 마스킹하고, 출력 임베딩을 한 칸 밀어서 위치 i의 예측이 i보다 앞선 출력에만 의존하게 함.
- 3.2.2절: h=8, d_k=d_v=d_model/h=64. 헤드별 차원이 줄어 총 계산량은 전체 차원의 단일 헤드와 비슷함. MultiHead = Concat(head_1..head_h) W^O, W^O는 (h·d_v)×d_model.
- 3.2.3절: 세 가지 쓰임. ① encoder-decoder attention: 쿼리는 이전 디코더 층에서, 키·값(memory)은 인코더 출력에서 옴. 디코더의 모든 위치가 입력의 모든 위치를 봄. ② 인코더 셀프 어텐션: 키·값·쿼리가 모두 같은 곳(이전 인코더 층 출력)에서 옴. ③ 디코더 셀프 어텐션: 자기 위치까지만 봄. 자기회귀 성질을 지키려고 소프트맥스 입력에서 허용되지 않는 연결을 −∞로 가림.
- 3.3절: FFN(x) = max(0, xW1 + b1)W2 + b2. 위치마다 따로, 같은 방식으로 적용. 층마다 파라미터는 다름. 커널 크기 1인 합성곱 두 번과 같음. 입출력 d_model=512, 내부 d_ff=2048.
- 3.4절: 학습된 임베딩으로 토큰을 d_model 벡터로 바꿈. 두 임베딩 층과 소프트맥스 앞 선형 변환이 같은 가중치 행렬을 공유함. 임베딩에는 √d_model을 곱함.
- 3.5절: 순환·합성곱이 없으므로 위치 정보를 넣어야 함. 위치 인코딩은 d_model 차원이라 임베딩에 더함. PE(pos,2i)=sin(pos/10000^{2i/d_model}), PE(pos,2i+1)=cos(pos/10000^{2i/d_model}). 파장은 2π에서 10000·2π까지 기하급수. 고정 오프셋 k에 대해 PE_{pos+k}는 PE_pos의 선형 함수. 학습형 위치 임베딩도 결과가 거의 같았음(표 3 (E): BLEU 25.7 vs 25.8). 더 긴 길이로 외삽할 수 있을 것이라 보아 사인형을 택함.
- 4절 표 1 (n=길이, d=차원, k=커널, r=이웃 크기)
  | 층 종류 | 층당 복잡도 | 순차 연산 | 최대 경로 길이 |
  |---|---|---|---|
  | 셀프 어텐션 | O(n²·d) | O(1) | O(1) |
  | 순환 | O(n·d²) | O(n) | O(n) |
  | 합성곱 | O(k·n·d²) | O(1) | O(log_k n) |
  | 제한 셀프 어텐션 | O(r·n·d) | O(1) | O(n/r) |
  4절: n < d이면(문장 표현에서 흔함) 셀프 어텐션이 순환 층보다 빠름.
- 5.1절: 영어-독일어 WMT 2014 약 450만 문장 쌍, BPE 공유 어휘 약 37000. 영어-프랑스어 3600만 문장, 32000 word-piece.
- 5.2절: P100 GPU 8개. 기본 모델 스텝당 약 0.4초, 100,000스텝(12시간). 큰 모델 스텝당 1.0초, 300,000스텝(3.5일).
- 표 3 (영어-독일어 dev, newstest2013. 적지 않은 값은 기본 모델과 같음)
  | 행 | N | d_model | d_ff | h | d_k | d_v | P_drop | PPL | BLEU | 파라미터(백만) |
  |---|---|---|---|---|---|---|---|---|---|---|
  | base | 6 | 512 | 2048 | 8 | 64 | 64 | 0.1 | 4.92 | 25.8 | 65 |
  | (C) | 2 | | | | | | | 6.11 | 23.7 | 36 |
  | (C) | 4 | | | | | | | 5.19 | 25.3 | 50 |
  | (C) | 8 | | | | | | | 4.88 | 25.5 | 80 |
  | (C) | | 256 | | | 32 | 32 | | 5.75 | 24.5 | 28 |
  | (C) | | 1024 | | | 128 | 128 | | 4.66 | 26.0 | 168 |
  | (C) | | | 1024 | | | | | 5.12 | 25.4 | 53 |
  | (C) | | | 4096 | | | | | 4.75 | 26.2 | 90 |
  | (E) 학습형 위치 임베딩 | | | | | | | | 4.92 | 25.7 | |
  | big | 6 | 1024 | 4096 | 16 | | | 0.3 | 4.33 | 26.4 | 213 |
  6.2절 해석: "(C), (D)에서 예상대로 큰 모델이 더 좋고 드롭아웃이 과적합을 막는 데 크게 도움이 된다."
- 텐서 모양 따라가기(기본 모델, 문장 길이 n, 배치 생략)는 위 3.1~3.4절 값에서 직접 유도함: 토큰 n개 → 임베딩 n×512(+위치 인코딩 n×512, 더해도 n×512) → 헤드마다 Q,K,V n×64 (8개) → 점수 QK^T n×n(디코더 크로스 어텐션에서는 n_tgt×n_src) → 헤드 출력 n×64 → concat n×512 → W^O 곱 n×512 → Add&Norm n×512 → FFN 내부 n×2048 → FFN 출력 n×512 → Add&Norm n×512 → (6층 반복, 모양 불변) → 디코더 최종 n_tgt×512 → 선형 n_tgt×37000 → 소프트맥스(다음 토큰 확률).

## 이전 연구 (배경·계보)
- Bengio, Simard, Frasconi 1994, "Learning long-term dependencies with gradient descent is difficult", IEEE Trans. Neural Networks 5(2):157–166. https://doi.org/10.1109/72.279181 — 시간 간격이 길수록 경사 하강 학습이 어려워짐. 정보를 오래 붙잡는 조건이 곧 기울기를 감쇠시키는 조건이라는 상충관계. 장기 기울기가 지수적으로 감쇠함.
- Hochreiter & Schmidhuber 1997, "Long Short-Term Memory", Neural Computation 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — 특수 내부 단위(상수 오차 흐름)로 기울기가 소실·폭주하지 않게 함. 게이트로 정보를 넣고 꺼냄. (순차 계산이라는 점은 그대로임: 원 논문 1절 근거)
- Sutskever, Vinyals, Le 2014, "Sequence to Sequence Learning with Neural Networks", https://arxiv.org/abs/1409.3215 — 다층 LSTM 인코더가 입력을 고정 차원 벡터로 만들고 다른 LSTM이 출력을 생성함.
- Cho et al. 2014, "Learning Phrase Representations using RNN Encoder–Decoder for SMT", https://arxiv.org/abs/1406.1078 — RNN 인코더-디코더, GRU 제안.
- Bahdanau, Cho, Bengio 2014 (ICLR 2015), "Neural Machine Translation by Jointly Learning to Align and Translate", https://arxiv.org/abs/1409.0473 — 고정 길이 벡터가 인코더-디코더 성능의 병목이라고 추정. 출력 단어마다 관련 입력 위치를 소프트하게 찾게 함(정렬). 인코더는 양방향 RNN. 영어→프랑스어에서 기존 구문 기반 최고 시스템과 비슷한 성능, 긴 문장에서 특히 이점.
- Luong, Pham, Manning 2015, "Effective Approaches to Attention-based Neural Machine Translation", https://arxiv.org/abs/1508.04025 — 전역/지역 어텐션, 내적(dot)·general·concat 점수 함수 비교.
- 셀프 어텐션 선행(원 논문 2절의 참고문헌 [4, 27, 28, 22]): Cheng et al. 2016 (https://arxiv.org/abs/1601.06733), Parikh et al. 2016 decomposable attention (https://arxiv.org/abs/1606.01933), Paulus et al. 2017 (https://arxiv.org/abs/1705.04304), Lin et al. 2017 (https://arxiv.org/abs/1703.03130).
- ByteNet: Kalchbrenner et al. 2016, https://arxiv.org/abs/1610.10099 / ConvS2S: Gehring et al. 2017, https://arxiv.org/abs/1705.03122

## 이후 동향 (6단원)
- BERT: Devlin et al. 2018, https://arxiv.org/abs/1810.04805 — encoder-only, 양방향, MLM과 다음 문장 예측으로 사전학습, 과제별 미세조정.
- GPT-1: Radford et al. 2018 "Improving Language Understanding by Generative Pre-Training" (OpenAI 보고서) — decoder-only, 다음 토큰 예측 사전학습 후 미세조정.
- T5: Raffel et al. 2019, https://arxiv.org/abs/1910.10683 — encoder-decoder, 모든 과제를 text-to-text로 통일.
- BART: Lewis et al. 2019, https://arxiv.org/abs/1910.13461 — encoder-decoder, 잡음 제거 사전학습.
- GPT-3: Brown et al. 2020, https://arxiv.org/abs/2005.14165 — decoder-only 175B 파라미터. 기울기 갱신 없이 프롬프트 속 예시만으로 과제를 푸는 in-context learning(zero/one/few-shot).
- Wang et al. 2022 (ICML), "What Language Model Architecture and Pretraining Objective Works Best for Zero-Shot Generalization?", https://arxiv.org/abs/2204.05832 — 50억 파라미터 이상, 1700억 토큰 이상으로 decoder-only/encoder-decoder × 목표 조합 비교. **순수 비지도 사전학습 직후에는 인과 decoder-only + 자기회귀 LM 목표의 zero-shot 일반화가 가장 좋음.** MLM 사전학습 + 멀티태스크 미세조정을 하면 입력을 양방향으로 보는(non-causal) 모델이 가장 좋음. 인과 디코더를 비인과로 효율적으로 바꿔 경쟁력 있게 만들 수 있음. (BLOOM 논문 https://arxiv.org/abs/2211.05100 이 이 결과를 decoder-only 채택 근거로 인용)
- 원 논문 이후 바뀐 부품 (C 에이전트가 2026-11 arXiv 원문·초록으로 확인. 원 논문 쪽 대응은 위 3.1·3.3·3.5·3.2.2절 항목)
  - Pre-LN: Xiong et al. 2020 (ICML), "On Layer Normalization in the Transformer Architecture", https://arxiv.org/abs/2002.04745 — 원 논문처럼 잔차 블록 사이(덧셈 뒤)에 LayerNorm을 두는 Post-LN은 초기화 시점에 출력층 근처 파라미터의 기댓값 기울기가 커서, 큰 학습률을 쓰면 불안정하고 학습률 warm-up 단계가 필요함. LayerNorm을 잔차 블록 안(하위 층 입력)에 두는 Pre-LN은 초기화 때 기울기가 잘 행동해 warm-up을 없앨 수 있고, warm-up 없이도 기준과 비슷한 결과를 더 짧은 학습 시간·적은 하이퍼파라미터 조정으로 얻음.
  - LLaMA: Touvron et al. 2023, "LLaMA: Open and Efficient Foundation Language Models", https://arxiv.org/abs/2302.13971 (2.2절, ar5iv로 확인) — 원 트랜스포머에서 바꾼 점: ① pre-normalization(GPT-3에서 따옴): 하위 층의 출력이 아니라 입력을 정규화, 정규화 함수는 RMSNorm ② ReLU를 SwiGLU 활성화로 교체(PaLM에서 따옴), FFN 폭은 4d 대신 (2/3)·4d ③ 절대 위치 임베딩을 없애고 층마다 RoPE를 적용(GPTNeo에서 따옴).
  - SwiGLU(GLU 변형): Shazeer 2020, "GLU Variants Improve Transformer", https://arxiv.org/abs/2002.05202 — GLU는 두 선형 사영을 곱하고 그중 하나에 시그모이드를 씌움. 변형은 시그모이드를 다른 함수로 바꿈. 트랜스포머 FFN 하위 층에서 시험했고 일부 변형이 ReLU·GELU보다 품질이 좋았음.
  - RoPE: Su et al. 2021, "RoFormer: Enhanced Transformer with Rotary Position Embedding", https://arxiv.org/abs/2104.09864 — 회전 행렬로 절대 위치를 인코딩하면서 셀프 어텐션 식 안에서 상대 위치 의존이 드러나게 함. 주장한 성질: 시퀀스 길이 유연성, 상대 거리가 멀수록 토큰 간 의존이 줄어듦, 선형 셀프 어텐션과 호환.
  - MQA: Shazeer 2019, "Fast Transformer Decoding: One Write-Head is All You Need", https://arxiv.org/abs/1911.02150 — 점진적(토큰 하나씩) 디코딩은 큰 키·값 텐서를 반복해 불러오느라 메모리 대역폭이 병목. 모든 헤드가 키·값 한 벌을 공유하는 multi-query attention으로 텐서를 크게 줄여 디코딩이 훨씬 빨라지고 품질 저하는 작음.
  - GQA: Ainslie et al. 2023 (EMNLP), "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", https://arxiv.org/abs/2305.13245 — MQA(키·값 헤드 1개)는 디코더 추론을 빠르게 하지만 품질이 떨어질 수 있음. GQA는 키·값 헤드 수를 1보다 많고 쿼리 헤드 수보다 적은 중간값으로 둔 일반화. 기존 멀티헤드 체크포인트를 원 사전학습 계산량의 약 5%로 uptraining 가능. uptrained GQA는 멀티헤드에 가까운 품질, MQA에 가까운 속도.
  - MoE: Shazeer et al. 2017, "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", https://arxiv.org/abs/1701.06538 — 최대 수천 개의 피드포워드 하위 네트워크(전문가)와 학습되는 게이트 네트워크가 예제마다 전문가 일부만 골라 씀(조건부 계산). 계산 효율 손실은 작게 하면서 모델 용량을 1000배 넘게 늘림. LSTM 층 사이에 최대 1370억 파라미터 MoE를 적용.
  - Switch Transformer: Fedus, Zoph, Shazeer 2021, https://arxiv.org/abs/2101.03961 — 트랜스포머의 dense FFN 층을 sparse Switch FFN 층으로 바꿈(그림 2 캡션). 토큰마다 전문가 하나에만 보냄(2.1절, ar5iv로 확인). 파라미터는 많아도 계산 비용은 일정. 같은 계산 자원에서 T5-Base·Large 대비 사전학습 속도 최대 7배.
  - Mixtral: Jiang et al. 2024, "Mixtral of Experts", https://arxiv.org/abs/2401.04088 — 층마다 피드포워드 블록(전문가) 8개, 라우터가 토큰마다 층마다 2개를 고름. 전체 파라미터 47B, 추론 때 쓰는 활성 파라미터 13B.
  - T5 사전학습 목표(ar5iv 3.1.4절로 확인): 입력 토큰 15%를 지우고, 연속으로 지운 구간마다 센티널 토큰 하나로 바꾼 뒤, 지운 구간들을 센티널로 구분해 출력하게 학습(span corruption). 3.3.4절: 평균 구간 길이 3이 대부분의 비번역 벤치마크에서 i.i.d. 목표보다 조금 좋음. https://arxiv.org/abs/1910.10683
  - BART 사전학습(초록으로 확인): 임의의 잡음 함수로 텍스트를 망가뜨리고 원문을 복원하도록 학습. 가장 좋았던 방법은 문장 순서 섞기와, 텍스트 구간을 마스크 토큰 하나로 바꾸는 in-filling. https://arxiv.org/abs/1910.13461
  - 확인하지 못해 쓰지 않는 것: 특정 상용 모델(GPT-4 등)의 내부 구조, 업계 채택 비율.

### decoder-only가 많이 쓰이는 이유 (강의 서술 근거. 논문 결과와 실무적 이유를 구분해 쓴다)
1. 학습 신호: 다음 토큰 예측은 레이블 없는 텍스트의 모든 위치가 정답이 됨(GPT 계열의 사전학습 방식). MLM은 가린 일부(BERT는 15%) 토큰만 예측함 — BERT 논문 3.1절.
2. 과제 통일: 모든 과제를 "프롬프트 다음 글 이어 쓰기"로 표현함 → in-context learning(GPT-3).
3. 실험 근거: Wang et al. 2022(위).
4. 실무: 층 종류가 하나라 구조가 단순해 확장이 쉬움. 생성할 때 앞 토큰의 키·값을 저장해 다시 쓰는 KV 캐시가 인과 마스크와 잘 맞음(앞 토큰의 표현이 뒤 토큰 때문에 바뀌지 않음). → "실무적 이유"로 표기.

## 보충자료 (링크만)
- The Annotated Transformer (Harvard NLP): https://nlp.seas.harvard.edu/annotated-transformer
- Dive into Deep Learning, 11.7 트랜스포머: https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html
- Jay Alammar, The Illustrated Transformer: https://jalammar.github.io/illustrated-transformer/
