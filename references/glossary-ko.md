# 한국어 용어집 (AI/ML 논문 강의용)

> **읽는 시점:** 코스 용어표를 만들 때(`korean-style-guide.md` §2.6)와 모듈에서 새 용어를 쓰기 전. 표기 원칙은 가이드 §2. 표에 없는 용어는 가이드 §2.3 절차로 정해 코스 용어표에 기록한다. 새 번역어를 만들지 않는다.

## 사용법

- **권장 표기**가 기본이다. 한 코스 안에서는 한 표기만 쓴다.
- **첫 등장 표기 예**: 모듈마다 처음 나올 때의 병기 형식. **칸이 비어 있으면 `권장 표기(English Title Case)`**이다(예: `지도 학습(Supervised Learning)`). 괄호는 ASCII 반각, 괄호 앞 공백 없음. 괄호 안 영어는 Title Case, 약어·고유 명칭은 원래 표기. 약어가 있으면 `한글 풀이(English Full Name, ACRONYM)`.
- **대안(허용)**: 틀리지 않았지만 기본값이 아니다. 택하면 코스 용어표에 이유를 적는다.
- **비고/출처 약호**
  - `G`: Google 머신러닝 용어집 한국어판(https://developers.google.com/machine-learning/glossary?hl=ko)에서 확인한 항목. 업계 관행이며 학회 표준은 아니다.
  - `조사`: 공개 자료를 조사해 (일반 지식)으로 분류한 판단.
  - `관행`: 검증 출처 없이 국내 교재·논문·커뮤니티 쓰임에 기댄 표기. 학회·TTA·대한수학회 용어집과 대조하지 못했다((미확인)).
  - `논쟁`: 표기가 갈리는 용어. 선택 이유는 `korean-style-guide.md` §2.4.
- 띄어쓰기: 전문 용어는 단어별로 띄우고, 사전에 한 단어로 오른 말(신경망, 표준편차, 기댓값)은 붙인다(가이드 §2.3).

---

## 1. 일반 머신러닝

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| machine learning | 머신러닝 | | 기계 학습 | G 용례("비지도 머신러닝") |
| supervised learning | 지도 학습 | | | G |
| unsupervised learning | 비지도 학습 | | | G |
| self-supervised learning | 자기 지도 학습 | | 자체 지도 학습 | G는 "자체 지도 학습". 커뮤니티 쓰임을 따름(관행) |
| semi-supervised learning | 준지도 학습 | | 반지도 학습 | 관행 |
| classification | 분류 | | | G |
| regression | 회귀 | | | G |
| clustering | 군집화 | | 클러스터링 | 관행 |
| training | 학습 | | 훈련 | 논쟁. G "학습 세트". 훈련은 교재에서 흔함(조사) |
| training set | 학습 세트 | | 훈련 세트 | G |
| validation set | 검증 세트 | | | G |
| test set | 테스트 세트 | | 시험 세트 | G |
| dataset | 데이터셋 | | 데이터 세트 | 관행 |
| label | 레이블 | | 라벨 | 논쟁. G "라벨", 외래어 표기법상 레이블(조사) |
| feature | 특징 | | 특성, 피처 | 논쟁. G는 특징·특성 모두 씀 |
| overfitting | 과적합 | | 오버피팅 | G |
| underfitting | 과소적합 | | | G |
| generalization | 일반화 | | | G |
| regularization | 규제 | | 정규화 | 논쟁. G "정규화"이나 normalization과 충돌 |
| hyperparameter | 하이퍼파라미터 | | 초매개변수 | G |
| parameter | 파라미터 | | 매개변수 | G. 정부 문서는 매개변수(조사) |
| model | 모델 | (병기 불필요) | | 관행 |
| inference | 추론 | | 인퍼런스 | G. reasoning과 함께 나오면 `추론 단계`로 구별(가이드 §2.4) |
| data augmentation | 데이터 증강 | | | G |
| dimensionality reduction | 차원 축소 | | | G |
| sampling | 샘플링 | | 표집 | G |
| ensemble | 앙상블 | | | 조사 |
| transfer learning | 전이 학습 | | | 관행 |
| representation learning | 표현 학습 | | | 관행 |
| curriculum learning | 커리큘럼 학습 | | | 조사 |
| decision boundary | 결정 경계 | | | 관행 |

## 2. 딥러닝 구조

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| deep learning | 딥러닝 | | 심층 학습 | 관행 |
| neural network | 신경망 | | 뉴럴 네트워크 | 조사. G "순환 신경망" 용례 |
| layer | 층 | | 레이어 | 관행. 은닉층·출력층과 일관 |
| hidden layer | 은닉층 | | | 관행 |
| weight | 가중치 | | | 조사 |
| bias (편향 항) | 편향 | 편향(Bias) | 바이어스 | G. 데이터 편향(bias)과 문맥으로 구별 |
| activation function | 활성화 함수 | | | G |
| ReLU | ReLU | ReLU(Rectified Linear Unit) | 렐루 | 관행. 조사는 `ReLU를`(렐루) |
| sigmoid | 시그모이드 | 시그모이드(Sigmoid) 함수 | | 관행 |
| softmax | 소프트맥스 | | | G |
| logit | 로짓 | | | 관행 |
| dropout | 드롭아웃 | | | G |
| batch normalization | 배치 정규화 | | | G |
| layer normalization | 층 정규화 | | 레이어 정규화 | 관행 |
| residual connection | 잔차 연결 | | 스킵 연결 | 관행 |
| feed-forward network | 피드포워드 신경망 | | 순방향 신경망 | 관행 |
| multilayer perceptron | 다층 퍼셉트론 | 다층 퍼셉트론(Multilayer Perceptron, MLP) | MLP | 관행 |
| convolution | 합성곱 | | 컨볼루션 | 논쟁. G "컨볼루션" |
| convolutional neural network | 합성곱 신경망 | 합성곱 신경망(Convolutional Neural Network, CNN) | CNN | 논쟁(위와 같음) |
| pooling | 풀링 | | | 관행 |
| recurrent neural network | 순환 신경망 | 순환 신경망(Recurrent Neural Network, RNN) | RNN | G |
| long short-term memory | LSTM | | 장단기 메모리 | 관행 |
| encoder | 인코더 | | 부호기(비권장) | G |
| decoder | 디코더 | | | 조사 |
| embedding | 임베딩 | | | G |
| latent space | 잠재 공간 | | | G |
| attention | 어텐션 | | 주의 집중 | 조사. 관용 음차 우선 |
| self-attention | 셀프 어텐션 | | 자기 주의 | G |
| multi-head attention | 멀티헤드 어텐션 | | 다중 헤드 어텐션 | 관행 |
| query / key / value | 쿼리 / 키 / 값 | 쿼리(Query), 키(Key), 값(Value) | 밸류 | 관행 |
| transformer | 트랜스포머 | | | 조사. 관용 음차 우선 |
| positional encoding | 위치 인코딩 | | | 관행 |
| autoencoder | 오토인코더 | | | 관행 |
| variational autoencoder | 변분 오토인코더 | 변분 오토인코더(Variational Autoencoder, VAE) | VAE | 관행 |
| generative adversarial network | 생성적 적대 신경망 | 생성적 적대 신경망(Generative Adversarial Network, GAN) | GAN | 관행 |
| diffusion model | 확산 모델 | | 디퓨전 모델 | 관행 |
| vision transformer | 비전 트랜스포머 | 비전 트랜스포머(Vision Transformer, ViT) | ViT | 관행 |
| hidden state | 은닉 상태 | | | 관행 |

## 3. 강화 학습

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| reinforcement learning | 강화 학습 | 강화 학습(Reinforcement Learning, RL) | 강화학습 | G |
| agent | 에이전트 | | | G |
| environment | 환경 | | | G |
| state | 상태 | | | G |
| action | 행동 | | 액션 | 조사. G는 영문 노출 |
| reward | 보상 | | 리워드 | 조사 |
| return | 리턴 | | 누적 보상, 이득 | 논쟁. 관행 |
| policy | 정책 | | 폴리시 | G |
| policy gradient | 정책 경사 | | 정책 그래디언트 | 조사. 굳은 합성어라 `경사` |
| value function | 가치 함수 | | | G |
| Q-function | Q 함수 | | 상태-행동 가치 함수 | G |
| advantage | 어드밴티지 | | 이점 | 관행. `interactive-elements.md` 예시와 일관 |
| discount factor | 할인율 | | 감가율 | 관행 |
| episode | 에피소드 | | | G |
| trajectory | 궤적 | | 트라젝토리 | 관행 |
| Markov decision process | 마르코프 결정 과정 | 마르코프 결정 과정(Markov Decision Process, MDP) | MDP | 관행 |
| Markov property | 마르코프 속성 | | 마르코프 성질 | G. 수학 문서는 "성질"(조사) |
| exploration / exploitation | 탐색 / 활용 | 탐색(Exploration)과 활용(Exploitation) | | 관행 |
| on-policy / off-policy | 온폴리시 / 오프폴리시 | 온폴리시(On-Policy) | 정책 내 / 정책 외 | 관행 |
| actor-critic | 액터-크리틱 | | 행위자-비평자 | 관행 |
| proximal policy optimization | PPO | 근접 정책 최적화(Proximal Policy Optimization, PPO) | | 관행. 약어 주 표기 |
| group relative policy optimization | GRPO | 그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO) | | 관행. `interactive-elements.md` 툴팁 예시와 일관 |
| reward model | 보상 모델 | | 리워드 모델 | 관행 |
| reward hacking | 보상 해킹 | | | 관행 |
| KL penalty | KL 페널티 | | KL 벌점 | 관행 |
| rollout | 롤아웃 | | | 관행 |

## 4. 언어 모델·LLM

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| language model | 언어 모델 | | | 관행 |
| large language model | 대규모 언어 모델 | 대규모 언어 모델(Large Language Model, LLM) | 거대 언어 모델, LLM | G |
| foundation model | 파운데이션 모델 | | 기반 모델 | 논쟁. 관행. base model과 혼동 방지 |
| base model | 기본 모델 | | 베이스 모델 | 관행 |
| token | 토큰 | | | G |
| tokenizer | 토크나이저 | | | 관행 |
| tokenization | 토큰화 | | | 관행 |
| vocabulary | 어휘 | | 어휘 집합 | 관행 |
| prompt | 프롬프트 | | | G |
| system prompt | 시스템 프롬프트 | | | 관행 |
| prompt engineering | 프롬프트 엔지니어링 | | | 관행 |
| context window | 컨텍스트 창 | | 컨텍스트 윈도 | 관행. `윈도우`는 외래어 표기법에 맞지 않음 |
| in-context learning | 맥락 내 학습 | | 인컨텍스트 학습, 문맥 내 학습 | 논쟁. 관행 |
| few-shot learning | 퓨샷 학습 | | 소수 샷 학습 | G |
| zero-shot learning | 제로샷 학습 | | | G |
| chain-of-thought | 사고의 사슬 | 사고의 사슬(Chain-of-Thought, CoT) | 생각의 사슬, CoT | 논쟁. 관행 |
| reasoning | 추론 | | | 관행. inference와 구별은 가이드 §2.4 |
| pre-training | 사전 학습 | | 프리트레이닝 | G |
| fine-tuning | 미세 조정 | | 파인튜닝, 세부 조정 | 논쟁. G "세부 조정" |
| supervised fine-tuning | 지도 미세 조정 | 지도 미세 조정(Supervised Fine-Tuning, SFT) | SFT | 관행 |
| instruction tuning | 지시 조정 | | 인스트럭션 튜닝 | 관행 |
| parameter-efficient fine-tuning | 파라미터 효율적 미세 조정 | 파라미터 효율적 미세 조정(Parameter-Efficient Fine-Tuning, PEFT) | PEFT | 관행 |
| low-rank adaptation | LoRA | 저랭크 적응(Low-Rank Adaptation, LoRA) | | 관행. 약어 주 표기, `LoRA를`(로라) |
| reinforcement learning from human feedback | RLHF | 인간 피드백 기반 강화 학습(Reinforcement Learning from Human Feedback, RLHF) | | G |
| direct preference optimization | DPO | 직접 선호 최적화(Direct Preference Optimization, DPO) | | 관행 |
| preference data | 선호 데이터 | | | 관행 |
| alignment | 정렬 | | 얼라인먼트 | 관행. 정렬 알고리즘(sorting)과 문맥으로 구별 |
| hallucination | 환각 | | 할루시네이션 | 논쟁. G "할루시네이션" |
| next-token prediction | 다음 토큰 예측 | | | 관행 |
| autoregressive | 자기회귀 | 자기회귀(Autoregressive) 모델 | 자동회귀 | 관행 |
| decoding | 디코딩 | | | 관행 |
| greedy decoding | 탐욕적 디코딩 | | 그리디 디코딩 | 관행 |
| beam search | 빔 탐색 | | 빔 서치 | 관행 |
| temperature | 온도 | | | 조사. G 항목 없음(미확인) |
| top-k / top-p sampling | top-k 샘플링 / top-p 샘플링 | top-p 샘플링(Nucleus Sampling) | 핵 샘플링 | 관행. k, p는 기호라 원어 유지 |
| speculative decoding | 추측 디코딩 | | 투기적 디코딩 | 관행 |
| KV cache | KV 캐시 | KV 캐시(Key-Value Cache) | | 관행 |
| mixture of experts | 전문가 혼합 | 전문가 혼합(Mixture of Experts, MoE) | MoE | 조사. G는 영문 노출 |
| quantization | 양자화 | | | 관행 |
| knowledge distillation | 지식 증류 | | 증류 | G는 "증류". 첫 등장은 `지식 증류`, 이후 `증류` 허용 |
| retrieval-augmented generation | 검색 증강 생성 | 검색 증강 생성(Retrieval-Augmented Generation, RAG) | RAG | 관행 |
| tool use | 도구 사용 | | | 관행 |
| scaling law | 스케일링 법칙 | | 규모 법칙 | 조사((미확인)) |
| emergent ability | 창발 능력 | | 창발적 능력 | 관행 |
| test-time compute | 추론 시 연산 | | 테스트 시점 연산 | 관행 |
| synthetic data | 합성 데이터 | | | 관행 |
| jailbreak | 탈옥 | | | 관행 |
| red teaming | 레드팀 평가 | | 레드 티밍 | 관행 |
| multimodal | 멀티모달 | | 다중 모달 | 관행 |
| vision-language model | 시각-언어 모델 | 시각-언어 모델(Vision-Language Model, VLM) | VLM | 관행 |
| perplexity | 퍼플렉시티 | | 혼란도 | G |

## 5. 확률·통계

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| probability distribution | 확률 분포 | | | 조사 |
| random variable | 확률 변수 | | 확률변수 | 조사 |
| conditional probability | 조건부 확률 | | | 관행 |
| joint probability | 결합 확률 | | | 관행 |
| marginal probability | 주변 확률 | | | 관행 |
| independence | 독립 | | | 관행 |
| i.i.d. | 독립 동일 분포 | 독립 동일 분포(Independent and Identically Distributed, i.i.d.) | | 관행 |
| expectation | 기댓값 | | 기대값 | 논쟁. 표준국어대사전 표기(조사) |
| variance | 분산 | | | 조사 |
| standard deviation | 표준편차 | | 표준 편차 | 조사 |
| covariance | 공분산 | | | 관행 |
| normal distribution | 정규 분포 | | 가우스 분포 | 관행 |
| likelihood | 가능도 | | 우도 | 논쟁. 툴팁에 "우도라고도 한다" |
| maximum likelihood estimation | 최대 가능도 추정 | 최대 가능도 추정(Maximum Likelihood Estimation, MLE) | 최대 우도 추정 | 논쟁(위와 같음) |
| prior | 사전 분포 | | 사전 확률 | 조사 |
| posterior | 사후 분포 | | 사후 확률 | 조사 |
| Bayes' theorem | 베이즈 정리 | | | 조사 |
| entropy | 엔트로피 | | | G |
| cross-entropy | 교차 엔트로피 | | 크로스 엔트로피 | G |
| KL divergence | KL 발산 | KL 발산(Kullback-Leibler Divergence) | 쿨백-라이블러 발산 | 조사 |
| mutual information | 상호 정보량 | | | 관행 |
| Monte Carlo | 몬테카를로 | 몬테카를로(Monte Carlo) 방법 | | 관행 |
| confidence interval | 신뢰 구간 | | | 관행 |
| standard error | 표준 오차 | | | 관행 |
| statistical significance | 통계적 유의성 | | | 관행 |
| p-value | p값 | p값(p-value) | 유의 확률 | 관행 |

## 6. 최적화

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| optimization | 최적화 | | | 관행 |
| objective function | 목적 함수 | | | 관행 |
| loss function | 손실 함수 | | 비용 함수, 로스 함수 | G |
| cost function | 비용 함수 | | | 조사. 고전 ML 교재 |
| gradient | 그래디언트 | | 기울기 | 논쟁. 굳은 합성어는 `경사` |
| gradient descent | 경사 하강법 | | 경사하강법 | G "경사하강법"(붙임). 이 스킬은 띄어 씀 |
| stochastic gradient descent | 확률적 경사 하강법 | 확률적 경사 하강법(Stochastic Gradient Descent, SGD) | SGD | G |
| mini-batch | 미니 배치 | | 미니배치 | G |
| batch | 배치 | | | G (일반 문맥은 "일괄") |
| batch size | 배치 크기 | | | 관행 |
| learning rate | 학습률 | | | G |
| learning rate schedule | 학습률 스케줄 | | | 관행 |
| warmup | 워밍업 | | 웜업 | 관행. 외래어 표기 |
| epoch | 에포크 | | | G |
| backpropagation | 역전파 | | 오차 역전파 | G |
| vanishing gradient | 경사 소실 | | 기울기 소실 | 관행. G "경사 폭발"과 짝 |
| exploding gradient | 경사 폭발 | | | G |
| gradient clipping | 그래디언트 클리핑 | | 경사 클리핑 | 관행 |
| momentum | 모멘텀 | | | 관행 |
| Adam | Adam | Adam 옵티마이저 | 아담 | 관행. 고유 명칭, `Adam은`(아담) |
| optimizer | 옵티마이저 | | 최적화기 | 관행 |
| weight decay | 가중치 감쇠 | | | 관행 |
| convergence | 수렴 | | | 관행 |
| local minimum | 지역 최솟값 | | 극솟값 | 관행. 사이시옷 표기(가이드 §2.4) |
| global minimum | 전역 최솟값 | | 최솟값 | 관행 |
| Lagrange multiplier | 라그랑주 승수 | | | 관행 |

## 7. 선형대수·미적분

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| scalar | 스칼라 | | | 관행 |
| vector | 벡터 | | | 관행 |
| matrix | 행렬 | | | 관행 |
| tensor | 텐서 | | | 관행 |
| dot product | 내적 | | 점곱 | 관행 |
| matrix multiplication | 행렬 곱 | | 행렬 곱셈 | 관행 |
| transpose | 전치 | | | 관행 |
| dimension | 차원 | | | 관행 |
| norm | 노름 | | | 관행 |
| rank | 랭크 | | 계수 | 관행. LoRA 설명의 `저랭크`와 일관 |
| eigenvalue / eigenvector | 고윳값 / 고유 벡터 | 고윳값(Eigenvalue) | 고유값 | 관행. 사이시옷 표기 |
| singular value decomposition | 특잇값 분해 | 특잇값 분해(Singular Value Decomposition, SVD) | 특이값 분해 | 관행 |
| orthogonal | 직교 | | | 관행 |
| linear transformation | 선형 변환 | | | 관행 |
| derivative | 도함수 | | 미분 | 관행. 미분 계수와 구별 |
| partial derivative | 편미분 | | | 관행 |
| chain rule | 연쇄 법칙 | | | 관행 |
| Jacobian | 야코비 행렬 | | 야코비안 | 관행 |
| Hessian | 헤세 행렬 | | 헤시안 | 관행 |
| integral | 적분 | | | 관행 |
| logarithm | 로그 | | | 관행 |
| exponential function | 지수 함수 | | | 관행 |

## 8. 평가·실험

| English | 권장 표기 | 첫 등장 표기 예 | 대안(허용) | 비고/출처 |
|---|---|---|---|---|
| accuracy | 정확도 | | 정확성 | G "정확성". 지표명은 정확도(조사) |
| precision | 정밀도 | | | G |
| recall | 재현율 | | | G |
| F1 score | F1 점수 | | | 관행 |
| confusion matrix | 혼동 행렬 | | | 관행 |
| evaluation metric | 평가 지표 | | | 관행 |
| benchmark | 벤치마크 | | | 조사 |
| baseline | 기준 모델 | | 기준선, 베이스라인 | 논쟁. G "기준" |
| ablation study | 제거 실험 | | 어블레이션, 절제 | 논쟁. G "절제" |
| state of the art | 최고 성능 | 최고 성능(State of the Art, SOTA) | SOTA | 관행 |
| leaderboard | 리더보드 | | | 관행 |
| cross-validation | 교차 검증 | | | 관행 |
| human evaluation | 사람 평가 | | 인간 평가 | 관행 |
| win rate | 승률 | | | 관행 |
| pass@k | pass@k | pass@k(문제당 k개 중 하나 이상 정답일 확률) | | 관행. 지표명 원어 유지 |
| out-of-distribution | 분포 외 | 분포 외(Out-of-Distribution, OOD) 데이터 | OOD | 관행 |
| robustness | 강건성 | | 견고성 | 관행 |
| reproducibility | 재현성 | | | 관행 |
| data contamination | 데이터 오염 | | | 관행 |
| random seed | 난수 시드 | | 시드 | 관행 |
| error bar | 오차 막대 | | | 관행 |
| hyperparameter search | 하이퍼파라미터 탐색 | | | 관행 |
| BLEU / ROUGE | BLEU / ROUGE | BLEU(번역 품질 지표) | 블루 / 루지 | 관행. 지표명 원어 유지, `BLEU를`(블루) |
