# 삽화 가이드 (수능특강식 문항 그림)

수능특강 문항의 그림은 장식이 아니라 **문제를 푸는 데 쓰는 자료**다. 이 문서는 강의에 그림을 넣을 때의 결정 규칙, 스타일, 만드는 방법을 정한다.

## 1. 먼저 결정: 코드로 그릴까, 모델로 그릴까

| 그림 종류 | 방법 | 이유 |
|---|---|---|
| 좌표·벡터·그래프, 표, 실험 장치 배치, 흐름·구조도, 행렬·격자 | **SVG를 직접 쓴다** | 수치와 위치가 정확해야 문제가 성립한다. 한글·기호 라벨이 정확하다. 모델이 필요 없다 |
| 사물·장면(실험 도구, 사람, 동식물, 기계)처럼 형태가 중요한 그림 | `illustrate.py`(작은 로컬 모델 → 선화 SVG) | 손으로 좌표를 찍기 어렵다 |
| 사진이 꼭 필요한 경우 | 쓰지 않는다 | 교재 지면 스타일과 맞지 않는다. 선화로 바꾼다 |

도식·그래프는 첫째 줄(코드)로 그린다. 그와 별도로 **강의마다 사물·장면 삽화를 최소 3개** 모델로 만들어 넣는다(SKILL.md 작성 규칙, `check-pages.py`가 `figure img[src^="assets/"]` 개수 검사). 장면은 본문의 비유·상황과 맞춘다(예: 번역하는 사람 = 시퀀스 변환, 도서관 색인 카드 = 쿼리·키, 채점 = 평가 지표). 예시 강의 `examples/attention-ko`에 세 장면이 있다.

## 2. 스타일 규칙

- **색:** 먹색 `#1F2328` + 교과 색 하나(`--color-accent`). 회색은 모눈·보조선에만. 다른 유채색 금지(`check-pages.py` 검출). 색 전체 기준은 `design-system.md` "색상 규약"을 따른다.
- **선:** 먹선 1.5px, 강조선 2px, 보조선 1px. 끝과 꺾임은 둥글게.
- **면:** 평면 채움만. 그림자, 그라데이션, 질감, 3D 효과 없음.
- **글자(문항 삽화):** 문항 삽화 속 글자는 SVG `<text>`. 본문 서체, 13px 안팎, 숫자는 고른 폭. 라벨은 기호(A, B, ㄱ, ㄴ, (가), (나), O, x, y)와 짧은 낱말만. 문장은 발문에 쓴다. 수학 기호(`q`, `d`, `x`)는 `<text font-style="italic">`로 쓴다. 도식(개념 그림·`.svg-diagram`)의 노드 라벨은 `<text>`가 아니라 `foreignObject > .node-label > span`이고, 라벨 속 기호는 `<i class="mi">q</i>`이다(`interactive-elements.md` SVG Rules).
- **강조:** 문제의 핵심 대상 하나만 교과 색으로. 나머지는 먹색.
- **틀:** 문항 그림은 1px 테두리 상자(`.q-figure`) 안에. 그림 번호를 붙이지 않고, 발문이 `그림은 ~을 나타낸 것이다.`로 소개한다.
- **배치:** 문항에서는 선택지 오른쪽(`.q-body`). 페이지 높이(765px) 검사는 그림이 들어간 문항에도 그대로 적용된다.

## 3. 코드로 그리는 그림 (권장 경로)

`interactive-elements.md`의 "문항 삽화" 패턴을 쓴다. 좌표 그림은 다음 순서로 만든다.

1. 단위 길이를 정한다(예: 모눈 한 칸 = 40). 원점의 화면 좌표를 정한다.
2. 문제의 수치를 좌표로 옮긴다. 수치가 그림과 정확히 맞아야 한다(예: $\boldsymbol{q}=(2,1)$이면 원점에서 오른쪽 80, 위 40).
3. 모눈(`guide`) → 축(`ink`, 화살촉 marker) → 대상(`ink`, 강조는 `ink accent`) → 라벨 순으로 쓴다.
4. viewBox는 내용 + 여백 8에 맞춘다.
5. 정답·오답 해설의 계산이 그림 좌표와 맞는지 다시 확인한다.

`.figure`와 `.svg-diagram` 안에서는 `.ink`, `.ink.strong`, `.ink-fill`, `.accent`, `.accent-fill`, `.guide`, `.guide-axis`, `.guide-fill`, `.row-accent`, `.edge-line.thin`, `.edge-line.dashed`, `.dot`, `.dot-accent`, `text.mono|muted|accent-text`를 쓴다(문항 삽화에만 쓰던 클래스가 아니다). 캡션은 `.figure-caption`, 너비 맞춤은 `.svg-diagram.fit`과 `--diagram-max`이다.

**개념마다 그림.** 문항뿐 아니라 본문에서 새로 도입하는 개념·알고리즘·수식에도 코드로 그린 그림이나 그래프를 하나씩 둔다. 그림의 숫자는 본문과 일치해야 한다(내적 벡터 격자, 소프트맥스 가중치 막대, 행렬 형상 n×d_k · d_k×n = n×n, 스케일 전후 막대, 멀티헤드 512→8×64→연결, BLEU n-gram 겹침 칩). 페이지가 765px를 넘지 않게 `.with-figure` + `figure.figure.side`로 본문 옆에 둔다.

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
| 벡터화 후 | 선 유지, 강의 지면에 바로 쓸 수 있음 | 질감이 잡티로 남음 |

→ **기본은 SANA-Sprint 0.6B.** SD-Turbo는 메모리가 8GB 이하인 기기에서만 대안으로 쓴다. 사람이 든 장면은 시드마다 회색 면이 생길 수 있으므로 시드 3개를 만들어 선화가 가장 깨끗한 것을 고른다.

크기와 품질은 바뀌므로 새 강의를 만들 때 더 작은 모델이 나왔는지 확인한다.

### 설치 (한 번, 저장소 밖)

```bash
python3 references/illustrate.py setup   # 설치 명령을 출력한다. 확인한 뒤 직접 실행한다
```

가상환경은 `~/.cache/paper-to-course/venv`, 모델 가중치는 Hugging Face 캐시에 들어간다. 생성된 강의에는 SVG 파일만 들어가므로 강의 자체는 여전히 의존성이 없다.

### 실행

```bash
~/.cache/paper-to-course/venv/bin/python references/illustrate.py run \
  --prompt "a microscope on a desk" --out course/assets/fig-microscope.svg \
  --labels labels.json --accent "#1F6FB2"
```

파이프라인: 생성 → 흑백 이진화·잡티 제거·여백 잘라내기 → vtracer 벡터화(좌표 소수 1자리) → 먹색 하나로 정규화 → 라벨 덧씌우기. 같은 이름의 `.json`에 모델·시드·프롬프트를 남긴다. 결과는 70KB 안팎이다.

강의에 넣을 때는 `assets/`에 두고 `<img src="assets/fig-x.svg" alt="…">`로 넣는다. 본문 옆에 둘 때는 `.with-figure` + `figure.figure.side`(예: `examples/attention-ko`의 1단원 첫 페이지), 문항에서는 `.q-figure`를 쓴다.

직접 그린 스케치나 다른 선화도 같은 후처리를 거칠 수 있다:
```bash
python3 references/illustrate.py from-png sketch.png --out course/assets/fig-x.svg --labels labels.json
```

### 프롬프트

- 영어로, 대상 하나를 구체적으로: `a glass flask and a beaker on a lab bench`
- 스타일 접미사는 스크립트가 붙인다(선화, 평면, 흰 배경, 글자 없음). 프롬프트에 스타일어를 더 넣지 않는다.
- 사람·손은 작은 모델이 자주 망가뜨린다. 가능하면 사물로 바꾼다.
- 상태·변화(무너진 다리, 금 간 고리, 가격표 두 장)는 작은 모델이 잘 그리지 못한다. 온전한 사물 하나로 비유를 잡고, 상태는 캡션·SVG 라벨로 말한다. 그림이 프롬프트와 다르게 나오면 캡션과 `alt`를 **그림에 맞게** 고친다.
- 동전·간판·종이처럼 글자가 들어가기 쉬운 대상은 가짜 글자가 생긴다. 시드를 바꾸거나 다른 대상으로 바꾼다.

### 여러 강의를 동시에 만들 때

모델을 동시에 여러 개 띄우면 메모리가 부족해진다. 모든 에이전트가 같은 잠금 경로를 써서 한 번에 하나만 돌린다.

```bash
LOCK="$TMPDIR/paper-to-course-illustrate.lock"
until mkdir "$LOCK" 2>/dev/null; do sleep 5; done
~/.cache/paper-to-course/venv/bin/python references/illustrate.py run --prompt "…" --out course/assets/fig-x.svg; rc=$?
rmdir "$LOCK"; exit $rc
```

삽화 하나를 만든 뒤 바로 잠금을 푼다. 시드 여러 개를 시험할 때도 한 번 실행마다 잠금을 잡았다 푼다.

### 결과 검사 (사람이 본다)

- 대상이 맞는가, 선이 닫혀 있는가, 회색 얼룩이 남지 않았는가, 글자 흉내가 없는가.
- 실패하면 시드를 바꿔 3번까지 다시 만든다. 그래도 안 되면 코드로 그리는 단순한 도식으로 바꾼다.

## 5. 저작권

- EBS·출판사 교재의 그림을 모델 학습, 이미지 입력(img2img·ControlNet 조건), 따라 그리기에 쓰지 않는다. 가져오는 것은 **스타일 특징**(먹선, 교과 색 하나, 평면, 기호 라벨)뿐이다.
- 모델 라이선스를 따른다. SANA-Sprint는 NVIDIA, SD-Turbo는 Stability AI의 자체 라이선스이고 상업 이용 조건이 있다. 강의를 배포하기 전에 모델 카드의 현재 라이선스를 확인한다.
- 실존 인물, 상표, 기관 로고를 그리지 않는다.
