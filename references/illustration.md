# 삽화 가이드 (학습서 문항 그림)

그림은 장식이 아니라 **문제를 푸는 자료**다.

## 1. 먼저 결정: 코드로 그릴까, 모델로 그릴까

| 그림 종류 | 방법 | 이유 |
|---|---|---|
| 좌표·벡터·그래프, 표, 실험 장치 배치, 흐름·구조도, 행렬·격자 | **SVG 직접** | 수치·위치·라벨이 정확해야 한다 |
| 형태가 중요한 사물·장면(실험 도구, 사람, 동식물, 기계) | `illustrate.py`(로컬 모델 → 선화 SVG) | 손 좌표로 어렵다 |
| 사진 | 금지, 선화로 | 지면 스타일과 안 맞는다 |

도식·그래프와 별도로 **강의마다 사물·장면 삽화를 최소 3개** 모델로 만든다(SKILL.md 작성 규칙, `check-pages.py`가 `figure img[src^="assets/"]` 개수 검사). 장면은 본문의 비유·상황과 맞춘다(번역하는 사람 = 시퀀스 변환, 도서관 색인 카드 = 쿼리·키, 채점 = 평가 지표 — `examples/attention-ko`의 세 장면).

## 2. 스타일 규칙

- **색:** 먹색 `#1F2328` + 교과 색 하나(`--color-accent`). 회색은 모눈·보조선에만, 다른 유채색 금지(`check-pages.py` 검출). 전체 기준은 `design-system.md` "색상 규약".
- **선:** 먹선 1.5px, 강조선 2px, 보조선 1px. 끝과 꺾임은 둥글게.
- **면:** 평면 채움만(그림자, 그라데이션, 질감, 3D 없음).
- **글자(문항 삽화):** SVG `<text>`, 본문 서체, 13px 안팎, 고른 폭 숫자. 라벨은 기호(A, B, ㄱ, ㄴ, (가), (나), O, x, y)와 짧은 낱말만, 문장은 발문에. 수학 기호(`q`, `d`, `x`)는 `<text font-style="italic">`. 도식(개념 그림·`.svg-diagram`)의 노드 라벨은 `foreignObject > .node-label > span`, 라벨 속 기호는 `<i class="mi">q</i>`(`interactive-elements.md` SVG Rules).
- **강조:** 문제의 핵심 대상 하나만 교과 색, 나머지는 먹색.
- **틀:** 문항 그림은 1px 테두리 상자(`.q-figure`) 안에. 그림 번호 없이 발문이 `그림은 ~을 나타낸 것이다.`로 소개한다.
- **배치:** 문항에서는 선택지 오른쪽(`.q-body`). 765px 높이 검사는 그림 든 문항에도 적용.

## 3. 코드로 그리는 그림 (권장 경로)

`interactive-elements.md`의 "문항 삽화" 패턴을 쓴다. 좌표 그림 순서:

1. 단위 길이(예: 모눈 한 칸 = 40)와 원점의 화면 좌표를 정한다.
2. 문제 수치를 좌표로 정확히 옮긴다(예: $\boldsymbol{q}=(2,1)$이면 원점에서 오른쪽 80, 위 40).
3. 모눈(`guide`) → 축(`ink`, 화살촉 marker) → 대상(`ink`, 강조는 `ink accent`) → 라벨 순으로 쓴다.
4. viewBox는 내용 + 여백 8.
5. 정답·오답 해설의 계산이 그림 좌표와 맞는지 다시 확인한다.

`.figure`·`.svg-diagram` 안 클래스(문항 삽화 전용 아님): `.ink`, `.ink.strong`, `.ink-fill`, `.accent`, `.accent-fill`, `.guide`, `.guide-axis`, `.guide-fill`, `.row-accent`, `.edge-line.thin`, `.edge-line.dashed`, `.dot`, `.dot-accent`, `text.mono|muted|accent-text`. 캡션 `.figure-caption`, 너비 맞춤 `.svg-diagram.fit`·`--diagram-max`.

**개념마다 그림.** 본문에서 새로 도입하는 개념·알고리즘·수식에도 코드 그림·그래프를 하나씩 두고, 숫자는 본문과 일치시킨다(내적 벡터 격자, 소프트맥스 가중치 막대, 행렬 형상 n×d_k · d_k×n = n×n, 스케일 전후 막대, 멀티헤드 512→8×64→연결, BLEU n-gram 겹침 칩). 765px를 넘지 않게 `.with-figure` + `figure.figure.side`로 본문 옆에 둔다.

## 4. 모델로 그리는 그림 (`illustrate.py`)

### 모델

| 기본 | 대체 |
|---|---|
| SANA-Sprint 0.6B (`Efficient-Large-Model/Sana_Sprint_0.6B_1024px_diffusers`), 1~2스텝 | SD-Turbo (`stabilityai/sd-turbo`), 1~4스텝, 512px |

**비교 결과** (2026-11-25, Apple M5 Pro, 같은 프롬프트 12개, 시드 7):

| | SANA-Sprint 0.6B (1024px, 2스텝, bf16) | SD-Turbo (512px, 2스텝, fp16) |
|---|---|---|
| 장당 시간(예열 후) | 1.3초 | 0.3초 |
| 최대 메모리 | 12.6GB | 4.7GB |
| 흰 배경·선화 | 12개 모두 깨끗함 | 종이 질감 배경, 색 채움이 남음 |
| 대상 정확도 | 12/12 | 진자·돋보기를 틀림, 현미경에 가짜 서명 |
| 벡터화 후 | 선 유지, 바로 쓸 수 있음 | 질감이 잡티로 남음 |

→ **기본은 SANA-Sprint 0.6B.** SD-Turbo는 메모리 8GB 이하 기기에서만. 사람이 든 장면은 시드마다 회색 면이 생길 수 있어 시드 3개 중 선화가 가장 깨끗한 것을 고른다. 새 강의를 만들 때 더 작은 모델이 나왔는지 확인한다.

### 설치 (한 번, 저장소 밖)

```bash
python3 references/illustrate.py setup   # 설치 명령을 출력만 한다. 확인한 뒤 직접 실행한다
```

가상환경 `~/.cache/paper-to-course/venv`, 가중치는 Hugging Face 캐시. 강의에는 SVG만 들어가 의존성이 없다.

### 실행

```bash
~/.cache/paper-to-course/venv/bin/python references/illustrate.py run \
  --prompt "a microscope on a desk" --out course/assets/fig-microscope.svg \
  --labels labels.json --accent "#1F6FB2"
```

옵션: `--seed`(기본 7), `--model sana|sdturbo`(기본 `sana`), `--size`(SANA는 32, SD-Turbo는 8의 배수), `--labels`(선택), `--accent`(강의 교과 색, 기본 `#1F6FB2`). 라벨 JSON은 viewBox 기준 0~1 비율 좌표: `[{"text": "A", "x": 0.18, "y": 0.42}, {"text": "ㄱ", "x": 0.7, "y": 0.2, "accent": true}]`.

파이프라인: 생성 → 흑백 이진화·잡티 제거·여백 잘라내기 → vtracer 벡터화(좌표 소수 1자리) → 먹색 하나로 정규화 → 라벨 덧씌우기. 같은 이름의 `.json`에 모델·시드·프롬프트를 남긴다. 결과는 70KB 안팎.

`assets/`에 두고 `<img src="assets/fig-x.svg" alt="…">`로 넣는다. 본문 옆 `.with-figure` + `figure.figure.side`(예: `examples/attention-ko` 1단원 첫 페이지), 문항 `.q-figure`.

스케치·다른 선화 후처리, 라벨만 다시 입히기(둘 다 `--accent` 지원):
```bash
python3 references/illustrate.py from-png sketch.png --out course/assets/fig-x.svg --labels labels.json
python3 references/illustrate.py label fig.svg --labels labels.json --out fig-labeled.svg
```

### 프롬프트

- 영어로, 대상 하나를 구체적으로: `a glass flask and a beaker on a lab bench`
- 스타일 접미사(선화, 평면, 흰 배경, 글자 없음)는 스크립트가 붙인다. 스타일어를 더 넣지 않는다.
- 사람·손은 자주 망가진다. 가능하면 사물로 바꾼다.
- 상태·변화(무너진 다리, 금 간 고리, 가격표 두 장)는 잘 못 그린다. 온전한 사물 하나로 비유를 잡고 상태는 캡션·SVG 라벨로 말한다. 그림이 프롬프트와 다르게 나오면 캡션과 `alt`를 **그림에 맞게** 고친다.
- 동전·간판·종이처럼 글자가 들어가기 쉬운 대상은 가짜 글자가 생긴다. 시드나 대상을 바꾼다.

### 여러 강의를 동시에 만들 때

메모리 부족을 막기 위해 모든 에이전트가 같은 잠금 경로로 한 번에 하나만 돌린다.

```bash
LOCK="$TMPDIR/paper-to-course-illustrate.lock"
until mkdir "$LOCK" 2>/dev/null; do sleep 5; done
~/.cache/paper-to-course/venv/bin/python references/illustrate.py run --prompt "…" --out course/assets/fig-x.svg; rc=$?
rmdir "$LOCK"; exit $rc
```

한 번 실행(시드 하나)마다 잠금을 잡았다 바로 푼다.

### 결과 검사 (사람이 본다)

대상이 맞는가, 선이 닫혔는가, 회색 얼룩·글자 흉내가 없는가. 실패하면 시드를 바꿔 3번까지, 그래도 안 되면 코드로 그리는 단순한 도식으로.

## 5. 저작권

- 출판된 교재 그림을 모델 학습, 이미지 입력(img2img·ControlNet 조건), 따라 그리기에 쓰지 않는다. 가져오는 것은 **스타일 특징**(먹선, 교과 색 하나, 평면, 기호 라벨)뿐이다.
- 모델 라이선스를 따른다. SANA-Sprint(NVIDIA)와 SD-Turbo(Stability AI)는 자체 라이선스이고 상업 이용 조건이 있다. 배포 전 모델 카드의 현재 라이선스를 확인한다.
- 실존 인물, 상표, 기관 로고를 그리지 않는다.
