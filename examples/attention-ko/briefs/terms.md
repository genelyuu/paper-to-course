# 강의별 용어표: 트랜스포머(Attention Is All You Need)

기준: `references/glossary-ko.md`, 결정 절차는 `references/korean-style-guide.md` §2.3. 첫 등장은 모듈마다 다시 병기한다(§2.1).

English Term | 한글 용어 | 첫 등장 표기 | 비고
---|---|---|---
attention | 어텐션 | 어텐션(attention) | glossary: 관용 음차 우선
self-attention | 셀프 어텐션 | 셀프 어텐션(self-attention) | glossary
multi-head attention | 멀티헤드 어텐션 | 멀티헤드 어텐션(multi-head attention) | glossary
Transformer | 트랜스포머 | 트랜스포머(Transformer) | glossary: 모델 이름이므로 영어 대문자 유지
query / key / value | 쿼리 / 키 / 값 | 쿼리(query), 키(key), 값(value) | glossary
scaled dot-product attention | 스케일드 내적 어텐션 | 스케일드 내적 어텐션(scaled dot-product attention) | glossary의 `내적`과 `어텐션`을 조합한 표기(새 번역어 아님)
dot product | 내적 | 내적(dot product) | glossary
softmax | 소프트맥스 | 소프트맥스(softmax) | glossary
vector | 벡터 | 벡터(vector) | glossary
matrix | 행렬 | 행렬(matrix) | glossary
transpose | 전치 | 전치(transpose) | glossary
dimension | 차원 | 차원(dimension) | glossary
variance | 분산 | 분산(variance) | glossary
standard deviation | 표준편차 | 표준편차(standard deviation) | glossary: 붙여 씀
encoder | 인코더 | 인코더(encoder) | glossary
decoder | 디코더 | 디코더(decoder) | glossary
recurrent neural network | 순환 신경망 | 순환 신경망(recurrent neural network, RNN) | glossary
convolutional neural network | 합성곱 신경망 | 합성곱 신경망(convolutional neural network, CNN) | glossary
sequence transduction | 시퀀스 변환 | 시퀀스 변환(sequence transduction) | 용어집에 없음. 절차 4: 쓰임이 있는 표기, 결정 절차에 따라 신규 추가
machine translation | 기계 번역 | 기계 번역(machine translation) | 용어집에 없음. 일반 용어, 신규 추가
parallelization | 병렬화 | 병렬화(parallelization) | 용어집에 없음. 신규 추가
hidden state | 은닉 상태 | 은닉 상태(hidden state) | glossary
token | 토큰 | 토큰(token) | glossary
embedding | 임베딩 | 임베딩(embedding) | glossary
weight | 가중치 | 가중치(weight) | glossary
parameter | 파라미터 | 파라미터(parameter) | glossary
baseline | 기준 모델 | 기준 모델(baseline) | glossary: 논쟁 용어, 기본값 채택
ablation study | 제거 실험 | 제거 실험(ablation study) | glossary
BLEU | BLEU | BLEU(번역 품질 지표) | glossary: 지표명 원어 유지, `BLEU를`(블루)
benchmark | 벤치마크 | 벤치마크(benchmark) | glossary
state of the art | 최고 성능 | 최고 성능(state of the art) | glossary
ensemble | 앙상블 | 앙상블(ensemble) | glossary
lineage | 연구 계보 | 연구 계보 | 본문 용어, 영어 병기 없음

## 개정 추가 용어 (실무자 의견 반영, 2026-11)
원어 우선 규칙(`SKILL.md` "용어 표기")에 따라 현업에서 원어로 굳은 말은 원어를 앞에 둔다.

English Term | 한글 용어 | 첫 등장 표기 | 비고
---|---|---|---
long short-term memory | LSTM | LSTM(long short-term memory) | 약어가 관용
vanishing gradient | 기울기 소실 | 기울기 소실(vanishing gradient) | 
exploding gradient | 기울기 폭주 | 기울기 폭주(exploding gradient) | 
gate | 게이트 | 게이트(gate) | LSTM 내부
sequence-to-sequence | seq2seq | seq2seq(sequence-to-sequence) | 원어 우선
context vector | 문맥 벡터 | 문맥 벡터(context vector) | 고정 길이 벡터
fixed-length vector | 고정 길이 벡터 | 고정 길이 벡터(fixed-length vector) | 
alignment | 정렬 | 정렬(alignment) | Bahdanau
additive attention | 가산 어텐션 | 가산 어텐션(additive attention) | 
cross-attention | 크로스 어텐션 | 크로스 어텐션(cross-attention) | 논문 용어는 encoder-decoder attention. 첫 등장에 "논문은 인코더-디코더 어텐션이라 부름"을 밝힘
masked self-attention | 마스크드 셀프 어텐션 | 마스크드 셀프 어텐션(masked self-attention) | 
causal mask | 인과 마스크 | 인과 마스크(causal mask) | 
auto-regressive | 자기회귀 | 자기회귀(auto-regressive) | 
feed-forward network | FFN | FFN(feed-forward network, 피드포워드 신경망) | 원어 약어 우선
residual connection | 잔차 연결 | 잔차 연결(residual connection) | 
layer normalization | LayerNorm | LayerNorm(layer normalization, 층 정규화) | 수식 표기와 맞춤
sub-layer | 하위 층 | 하위 층(sub-layer) | 
layer | 층 | 층(layer) | "레이어"와 혼용 금지
positional encoding | 위치 인코딩 | 위치 인코딩(positional encoding) | 
tensor shape | 텐서 모양 | 텐서 모양(tensor shape) | 
hyperparameter | 하이퍼파라미터 | 하이퍼파라미터(hyperparameter) | 
complexity | 복잡도 | 복잡도(complexity) | 
path length | 경로 길이 | 경로 길이(path length) | 
encoder-only | encoder-only | encoder-only(인코더만 쓰는 구조) | 원어 우선
encoder-decoder (계열) | encoder-decoder | encoder-decoder(인코더와 디코더를 모두 쓰는 구조) | 6단원 분류명. 부품명 "인코더", "디코더"는 그대로
decoder-only | decoder-only | decoder-only(디코더만 쓰는 구조) | 원어 우선
large language model | LLM | LLM(large language model, 대규모 언어 모델) | 
pre-training | 사전학습 | 사전학습(pre-training) | 붙여 씀
fine-tuning | 미세조정 | 미세조정(fine-tuning) | 붙여 씀
masked language modeling | MLM | MLM(masked language modeling) | 
next-token prediction | 다음 토큰 예측 | 다음 토큰 예측(next-token prediction) | 
in-context learning | in-context learning | in-context learning(ICL) | 원어 우선
zero-shot | zero-shot | zero-shot(예시 없이 바로 푸는 것) | 원어 우선
KV cache | KV 캐시 | KV 캐시(KV cache) | 
gated recurrent unit | GRU | GRU(gated recurrent unit) | Cho et al. 2014, 원어 약어 우선
perplexity | 퍼플렉서티 | 퍼플렉서티(perplexity, PPL) | 표 3 지표
post-layer normalization | Post-LN | Post-LN(잔차 덧셈 뒤 정규화) | 원 논문 방식
pre-layer normalization | Pre-LN | Pre-LN(하위 층 앞 정규화) | Xiong et al. 2020
rotary position embedding | RoPE | RoPE(rotary position embedding, 회전 위치 임베딩) | Su et al. 2021
SwiGLU | SwiGLU | SwiGLU(게이트가 있는 FFN 활성화) | Shazeer 2020
multi-query attention | MQA | MQA(multi-query attention, 멀티쿼리 어텐션) | Shazeer 2019
grouped-query attention | GQA | GQA(grouped-query attention, 그룹 쿼리 어텐션) | Ainslie et al. 2023
mixture of experts | MoE | MoE(mixture of experts, 전문가 혼합) | 
warm-up | 예열 | 학습률 예열(warm-up) | 
dropout | 드롭아웃 | 드롭아웃(dropout) | 표 3 P_drop
