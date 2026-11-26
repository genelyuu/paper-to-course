# 도표·삽화 작성 지침 (개정용)

사용자 요구: **삽화와 도표를 충분히 넣는다.** 본문 쪽(확인 문제 쪽 제외)마다 개념 도식(인라인 SVG), 데이터 표, 그래프 중 하나 이상을 둔다. 저장소 규칙(`references/illustration.md`, `references/interactive-elements.md` "SVG 다이어그램", `references/design-system.md` 색상 규약)이 이 문서보다 우선한다. 예를 들어 노드 라벨은 `foreignObject > .node-label > span`으로 쓰고, 색은 먹색과 교과 색만 쓴다.

## 1. 무엇을 그리나: 이름이 아니라 메커니즘
- 상자에 "LSTM"이라고만 쓴 그림은 본문보다 정보가 적다. **데이터가 지나가는 길**, 경계를 넘는 화살표, 빼면 사라지는 간선을 그린다.
- **비교는 차이를 그린다.** 두 방식을 같은 입력, 같은 좌표에 두고 경로만 다르게 그린다(예: 셀프는 Q·K·V 화살표가 한 시퀀스에서 나오고, 크로스는 K·V 화살표가 인코더에서 건너온다). 선택지 상자만 따로 늘어놓은 것은 비교가 아니다.
- **화살표에 라벨을 단다.** "Q", "K·V", "×6", "n×512"처럼 짧게 쓴다. 같은 표기(점선, 교과 색)가 되풀이될 때만 범례를 둔다.
- **복잡도는 판단에 필요한 만큼만** 그린다. 한 단계짜리 개념이면 상자 세 개, 구조도라면 하위 층까지 그린다.
- **그림 하나에 주장 하나.** 캡션(`.figure-caption`)에 그림이 보여 주는 내용을 한 문장으로 쓴다(`그림은 ~을 나타낸 것이다.`). `<svg role="img" aria-label="…">`에도 같은 내용을 넣는다.

## 2. 트랜스포머 도식에서 특히 지킬 것 (웹 자료 조사 결과)
- **텐서 모양을 단계마다 적는다.** 이름 붙은 차원을 쓴다(n, d_model=512, d_k=64, d_ff=2048). 크기 변화는 직사각형 **폭**으로 보여 준다(512 → 64×8 → 512 → 2048 → 512). 참고: [HF, Mastering Tensor Dimensions in Transformers](https://huggingface.co/blog/not-lain/tensor-dims)
- **크로스 어텐션의 출처를 화살표로 표시한다.** 인코더 출력이 디코더 쪽 K·V로 들어가고 Q는 디코더에서 나온다. 인코더 최종 층 출력 하나가 디코더 N개 층 **모두**로 간다.
- **디코더 쪽에는 인과 마스크를 명시한다.** 삼각 격자에서 가린 칸은 회색 빗금이나 "−∞"로 표시한다.
- **작은 구체 예시를 쓴다.** 짧은 번역 쌍(예: 4토큰 → 4토큰)으로 모양 변화를 따라가고, "예시"라고 밝힌다. 참고: [d2l.ai 11.7](https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html)
- **그래프의 수치는 실제 값으로 계산한다.** 표 3 값이나 식으로 계산한 좌표를 쓴다(예: 위치 인코딩 사인 곡선, n²·d와 n·d² 비교 곡선). 눈대중 좌표를 쓰지 않는다. 자체 예시 값은 캡션에 "예시 값"이라고 쓴다.

## 3. 그리는 방식 (SVG 기법)
- 크기는 `viewBox`로 잡는다. 흐름도는 왼쪽에서 오른쪽, 층 쌓기는 아래에서 위로(논문 그림 1처럼 입력이 아래).
- 화살촉은 `<marker>`나 작은 `<polygon>`으로 그린다. marker id에는 파일 접두사를 붙인다(`ar-arrow` 등, 강의 전체에서 유일해야 함).
- 글자는 11~14px, 라벨은 1~3단어. 설명 문장은 캡션에 쓴다.
- 격자에 맞춘다. 기준선을 공유하고 간격을 고르게 둔다.
- `<script>`나 `<style>`을 SVG 안에 넣지 않는다. 클래스는 `.ink`, `.accent`, `.accent-fill`, `.guide`, `.node-rect`, `.edge-line`, `.edge-arrow` 등 기존 것만 쓴다.
- 페이지 높이는 765px 이하로 지킨다. `.with-figure` + `figure.figure.side`로 본문 옆에 두거나 `.svg-diagram.fit` + `--diagram-max`로 폭을 줄인다. 그래도 넘치면 쪽을 나눈다(단원 본문 최대 8쪽).

## 4. 삽화 (모델 선화, `assets/fig-*.svg`)
메인 에이전트가 만들어 경로를 알려 준다. 넣을 때는 `<img src="assets/fig-x.svg" alt="…">`를 `figure.figure.side` 안에 둔다(기존 00-background 첫 쪽 참고). 본문의 비유와 맞는 쪽에 넣는다.

## 5. GitHub 도표 skill에서 가져온 규칙 (원문 확인, 2026-11)
참고한 원문:
- [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design): `skills/diagram-design/SKILL.md`, `references/layout-budget.md`, `type-bar.md`, `type-architecture.md`
- [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph): `SKILL.md`, `references/composition-quality-contract.md`
- [jimliu/baoyu-skills: baoyu-diagram](https://github.com/jimliu/baoyu-skills/tree/main/skills/baoyu-diagram)

이 강의의 색 규칙(먹색과 교과 색 하나)과 라벨 방식(`foreignObject`)을 그대로 둔 채 아래 구조 규칙만 가져온다.

**그리기 전에 확인한다**
- 같은 내용을 3열 표로 전할 수 있으면 표를 쓴다. 문장 하나로 되면 문장을 쓴다(diagram-design §2·§3).
- 지울 수 있는 노드, 합칠 수 있는 노드, 배치만으로 관계가 보이는 화살표는 지운다. "더 지울 것이 없을 때 완성"이다(diagram-design §1, §9 Remove test).

**복잡도 예산 (그림 하나당)**
- 노드 9개, 화살표 12개 이하. 넘으면 전체 그림과 세부 그림 두 장으로 나눈다. 예: 트랜스포머 전체 구조도와 층 하나의 내부도.
- 교과 색 강조는 1~2곳만 쓴다(그 그림의 핵심 경로 하나). 층 쌓기 그림은 6층 이하, 막대그래프는 막대 8개 이하, 선 그래프는 계열 5개 이하.

**연결선 규칙 (diagram-design §6, fireworks 계약)**
1. 직각 연결만 쓴다. 꺾임은 둥글게(r=6~8). 두 끝의 x나 y가 같을 때만 직선을 쓴다. 대각선은 쓰지 않는다.
2. 화살표 라벨은 선 위에 겹치지 않게 6~10px 떨어뜨린다. 선 위에 놓아야 하면 바탕색 사각형(`fill="var(--color-bg)"` 계열의 기존 클래스나 흰 rect)으로 가린다. 라벨은 짧게, 세로쓰기는 금지.
3. 선끼리 겹치지 않는다. 나란한 경로는 12px 이상 띄운다. 교차를 피하고, 어쩔 수 없으면 한 곳만 교차한다.
4. 한 변에서 여러 선이 나가면 연결점을 나눈다(변 길이 L, 선 N개면 L·k/(N+1)).
5. 끝점이 아닌 상자 뒤로 선이 지나가지 않게 경로를 다시 잡는다.
6. 선을 먼저 그리고 상자를 나중에 그린다(상자가 선 위에 오도록). 한 선에 꺾임은 2번 이하. 더 필요하면 노드 배치를 바꾼다.

**배치**
- 좌표, 폭, 높이, 간격, 안쪽 여백은 4px 격자에 맞춘다. 노드 간격은 20/24/32/40, 안쪽 여백은 8/12/16을 쓴다.
- 같은 역할의 노드는 같은 높이, 같은 행의 노드는 같은 y에 둔다. 범례는 그림 아래 가로 한 줄로 두고 흐름 경로와 겹치지 않게 한다.
- 모든 노드를 똑같은 상자로 그리지 않는다. 역할(입력, 연산, 저장, 출력)에 따라 모양이나 선 굵기를 바꿔 위계를 보여 준다.

**그래프 (diagram-design type-bar)**
- 막대그래프의 값 축은 0에서 시작한다(축을 잘라 차이를 부풀리지 않는다). BLEU처럼 차이가 작은 값을 보이려면 막대 대신 점 그래프를 쓰고, 축의 시작값을 눈금에 분명히 적는다.
- 눈금선은 4~6개, 아주 옅게. 값 라벨은 막대나 점 옆에 두고, 강조할 막대(예: 기본 모델)는 하나만 교과 색으로 칠한다.
- 데이터 좌표는 공식으로 계산하고 반올림만 한다. 격자에 맞추려고 데이터 위치를 옮기지 않는다.

**검사 (fireworks: "명령이 성공했다고 시각 품질이 확인된 것은 아니다")**
- `check-pages.py` 통과 뒤에도 그림을 실제 크기로 렌더링해 **눈으로 본다**. 볼 것은 글자 잘림, 라벨과 선의 충돌, 화살표 방향, 교차, 간격이다.
- 같은 검사에서 두 번 실패하면 방식을 바꾼다. 그림을 나누거나 배치를 바꾼다. 글자를 줄이거나 내용을 숨겨서 통과시키지 않는다.

## 6. 준비된 삽화 (assets/, 모델 선화)
| 파일 | 장면 | 넣을 곳 | 담당 |
|---|---|---|---|
| `assets/fig-openbook.svg` | 책상 위 펼친 책 | 2단원 closed-book vs open-book | A |
| `assets/fig-shelf.svg` | 백과사전이 가득한 책장 | 1단원 non-parametric memory(문서 색인 = 꺼내 읽는 책장) | A |
| `assets/fig-magnifier.svg` | 책 위의 돋보기 | 4단원 retriever(DPR) | B |
| `assets/fig-pen.svg` | 종이에 쓰는 만년필 | 3단원 또는 4단원 generator(BART) | B |
| `assets/fig-buzzer.svg` | 퀴즈 대회 버저 | 5단원 Jeopardy 질문 생성 | C |
| `assets/fig-gavel.svg` | 판사봉 | 5단원 FEVER 사실 검증 | C |

넣는 법: `figure.figure.side` 안에 `<img src="assets/fig-x.svg" alt="…">`를 두고 캡션에 비유 한 줄을 쓴다. 기존 예는 `examples/attention-ko/modules/00-background.html` 첫 쪽이다. 쪽 높이 765px를 넘으면 여유 있는 쪽으로 옮긴다.
