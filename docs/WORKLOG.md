# 작업 로그 (근거 기반)

형식: `#번호 | 행동 | 근거 | 결과`. 하위 에이전트 작업은 배정 모델과 배정 이유를 함께 적는다.

---

### #1 | 작업 디렉터리 확인
- **행동:** `/Users/eugene/dev/paper2contents` 조회.
- **근거:** 수정 대상 코드가 로컬에 있는지 확인해야 작업 범위를 정할 수 있음.
- **결과:** 빈 디렉터리, git 저장소 아님 → 업스트림 복제 필요.

### #2 | 업스트림 복제 및 진단
- **행동:** `git clone https://github.com/ZeroxZhang/paper-to-course.git .` (HEAD `624a8cf`), 파일별 한자 포함 줄 수 집계, 핵심 파일 정독.
- **근거:** "output을 한글 콘텐츠에 특화"하려면 출력물을 결정하는 지점(스킬 지시문, HTML 셸, CSS, JS, 예시 문서)을 먼저 식별해야 함.
- **결과:** 한자 포함 줄 수 — README 117, interactive-elements.md 101, onepage_output.html 100, SKILL.md 23, main.js 12, content-philosophy.md 3, gotchas.md 1. `_base.html`은 `lang="zh-CN"`, 라틴 전용 폰트. `styles.css`에 `word-break: keep-all` 없음. 진단 표는 `docs/PLAN.md` §0.

### #3 | 작업 브랜치 생성 및 계획 수립
- **행동:** `korean-localization` 브랜치 생성, `docs/PLAN.md` 작성.
- **근거:** 업스트림 대비 변경점을 diff로 추적 가능하게 하고, 하위 에이전트들이 같은 설계 결정(문체·용어 표기·폰트)을 공유하도록 단일 기준 문서가 필요.
- **결과:** 설계 결정 6개, 단계 A(3작업)/B(6작업)/C(검증) 및 복잡도별 모델 배정 확정.

### #4 | Phase A 병렬 디스패치 (A1 조사·A2 main.js·A3 타이포그래피)
- **행동:** 하위 에이전트 3개를 동시에 실행. A1=sonnet(웹 조사·종합), A2=haiku(문자열 12곳 기계적 치환), A3=sonnet(CSS 디자인 판단).
- **근거:** 세 작업은 서로 다른 파일을 수정하므로 충돌이 없음. 모델은 PLAN §2 복잡도 표 기준 — 판단이 거의 필요 없는 치환은 haiku, 근거 조사·디자인 판단은 sonnet.
- **결과:** 각 에이전트가 `docs/logs/<ID>.md`에 자체 로그를 남기도록 지시(WORKLOG 동시 쓰기 충돌 방지).

### #5 | Phase B 중 선행 의존성 없는 작업 조기 디스패치 (B4·B5·B6)
- **행동:** B4=sonnet(interactive-elements.md 예시 한국어화), B5=sonnet(lint-ko.py), B6=haiku(README·onepage 번역).
- **근거:** 세 작업은 A1 조사 결과가 없어도 PLAN §1 설계 결정만으로 수행 가능 → 대기 시간 단축. B6는 분량은 크나 판단이 단순한 번역이라 haiku. B1·B2·B3(SKILL.md, 스타일 가이드, 용어집, 철학 문서)는 A1의 표준 용어·번역투 근거가 필요하므로 보류.
- **결과:** 실행 중.

### #6 | A2 결과 독립 검증
- **행동:** `node --check references/main.js`, `i18n(` 호출부 grep.
- **근거:** 하위 에이전트 보고는 자기 평가이므로 메인에서 재현 확인 필요.
- **결과:** 문법 검사 통과. 12개 호출부 모두 `i18n()` 사용 확인. 헬퍼 이름이 `t`가 아닌 `i18n`인 이유: 기존 forEach 안의 `const t` 와 충돌(A2 로그 참조). 한자는 zh 사전(원본 보존용, lang="zh*"일 때만 사용)에만 남음 → lint 예외 대상.

### #7 | A3 결과 독립 검증 (styles.css 한글 타이포그래피 블록)
- **행동:** `styles.css` 2020행 이후 `KOREAN TYPOGRAPHY` 블록 정독.
- **근거:** A3 보고서에 `:lang(ko) em, i`처럼 범위가 새는 것처럼 보이는 선택자 표기가 있어, 전역 `<i>` 이탤릭 제거 같은 부작용이 있는지 확인 필요.
- **결과:** 실제 선택자는 `:lang(ko) em, :lang(ko) i` 로 범위가 올바름 → 수정 불필요. KaTeX 수식 이탤릭은 KaTeX 자체 폰트(KaTeX_Math-Italic)로 처리되므로 `font-synthesis: none` 영향 없음. `word-break: keep-all` + `overflow-wrap: break-word` 선택(anywhere 대신)은 flex/grid min-content 축소를 피하기 위함 — 타당. Pretendard v1.3.9 URL은 A3가 `curl -sI`로 200 확인.

### #8 | B6 결과 독립 검증 (README·onepage)
- **행동:** 한자 잔존 grep, `lang` 속성 확인, README 업스트림 안내의 날짜를 원문(`git show HEAD:README.md`)과 대조.
- **근거:** 번역 과정에서 사실(날짜·저장소 이름)이 지어지거나 바뀌지 않았는지 확인해야 함.
- **결과:** 한자 0/0, `lang="ko"` 확인. "2026-10-14"와 `zerox-skills/zerox-paper-to-course`는 원문 마이그레이션 공지와 일치. `onepage_output.png`는 중국어 화면 캡처 그대로임 → Phase C에서 헤드리스 Chrome으로 다시 캡처하기로 함(로컬에 Chrome 설치 확인).

### #9 | B4 결과 독립 검증 (interactive-elements.md)
- **행동:** 업스트림과 현재 파일의 `class="…"`·`data-*=` 집합을 diff, main.js가 읽는 `dataset.*` 키 목록 추출.
- **근거:** 예시 문서의 클래스·속성명이 바뀌면 생성된 강의에서 main.js/styles.css 연결이 끊김. 번역은 텍스트에만 적용되어야 함.
- **결과:** 클래스·data 속성 집합 완전 동일. 한자 0줄. 부수 발견: main.js는 `dataset.steps`(=`data-steps`, 519행)를 읽지만 예시 문서에는 해당 패턴이 없음(업스트림 원래 상태) → 수정 범위 밖으로 두되 B1(SKILL.md) 지시에 실제 속성명만 쓰도록 반영.

### #10 | B5 결과 독립 검증 (lint-ko.py)
- **행동:** `python3 -I references/lint-ko.py`를 good/bad 픽스처에 재실행, B5가 지적한 interactive-elements.md 580·582행 중국어 잔존 여부 재확인.
- **근거:** 린터가 완료 기준(PLAN §3-4)의 판정 도구이므로 오탐·미탐을 직접 확인해야 함. B5 지적은 B4와 동시 실행된 시점 차이일 가능성.
- **결과:** good=ERROR 0·WARN 0, bad=ERROR 11·WARN 24(KO001–KO107 모두 발화). 580·582행은 이미 한국어(B4가 이후 수정) → 조치 불필요. 알려진 한계: KO104는 서술격 조사 '이'와 주격 '이'를 구분 못 함(B5 로그 기재).

### #11 | 사용자 지시 반영: "말투는 EBS 교재의 문체를 적용한다."
- **행동:** WebSearch 2회(EBS 수능특강 구성·문체, 교과서 문체 집필 기준) 후 `docs/PLAN.md` §1 문체 결정을 "본문 합니다체 / UI 해요체" → "EBS 교재 문체"로 교체.
- **근거:** 사용자 직접 지시. 검색으로 EBS 수능특강의 코너 구성(개념 체크·탐구 자료·보충 설명·수능 2점/3점 테스트)은 확인([알라딘 수능특강 목록](https://aladin.co.kr/shop/wbrowse.aspx?CID=77441), [EBSi](https://www.ebsi.co.kr/ebs/pot/potg/BookSeriesInfoList.ebs)). 한다체·발문 형식을 규정한 공개 집필 지침은 찾지 못함 → EBS·검정 교과서 관행(본문 `~이다`, 학습 목표 `~할 수 있다`, 발문 `옳은 것은?`, 해설 `~이므로 ~이다`)을 규칙으로 채택하고 "관행"임을 명시. 국립국어원 자료([교과서 문장](https://www.korean.go.kr/nkview/nklife/1999_4/1999_0402.pdf))는 교과서 문장이 규범적이어야 한다는 전제만 뒷받침.
- **결과:** 적용 범위 = 학습자에게 보이는 생성물. 연구 대화(채팅) 대사만 해요체 예외(EBS 탐구 자료의 인용 대화 관행). 작성자용 지시문(SKILL.md 등)은 문체 규칙 대상 아님.

### #12 | 완료된 작업의 EBS 문체 재작업 지시 (B4·B5·A1 재개)
- **행동:** 완료된 B4(sonnet)·B5(sonnet)·A1(sonnet) 에이전트를 SendMessage로 재개해 각각 예시 문체 수정, 린터 KO102 교체·KO108/KO109 추가, EBS 근거 조사 추가를 지시.
- **근거:** 같은 에이전트를 재개하면 이전 맥락(파일 구조·제약)을 유지하므로 새 에이전트보다 재작업 비용과 오류 위험이 낮음.
- **결과:** B4 — 발문·①②③·"정답. ~이다." 해설·코너명 반영, 클래스/data 속성 불변. B5 — good 0/0, bad ERROR 11·WARN 44, 채팅 요소(`chat-*`)와 `lang≠ko` 제외. A1 — research §6 "EBS 교재 문체" 추가(대부분 "미확인, 관행" 표기, PLAN과 일치).

### #13 | main.js 한국어 UI 문구를 EBS 문체로 직접 수정
- **행동:** `I18N.ko`를 `먼저 답을 고르시오.` / `정답` / `오답` / `여기에 끌어다 놓으시오` / `'다음'을 눌러 시작하시오.` / `이 줄이 아니다. 다시 찾아보시오.`로 변경.
- **근거:** 8개 문자열 교체라 하위 에이전트 호출보다 직접 수정이 빠르고 정확함. EBS 해설 관행: 정답/오답 표지 + 한다체 해설, 감탄·칭찬 없음, 지시는 `~하시오`.
- **결과:** `node --check` 통과. 린터 good 픽스처 `--strict` 종료 코드 0.

### #14 | Phase B 핵심 문서 디스패치 (B1·B2·B3)
- **행동:** B1=opus(SKILL.md 전면 재작성), B2=opus(korean-style-guide.md + glossary-ko.md 신규), B3=sonnet(content-philosophy·gotchas·module-brief-template).
- **근거:** B1·B2는 스킬의 동작과 모든 하위 문서의 기준이 되는 핵심 설계·규범 종합이라 가장 강한 모델 배정. B3는 기존 원칙의 번역·보강이라 sonnet. A1 조사가 끝나 의존성 해소.
- **결과:** 실행 중. (참고: good 픽스처 `lint-ko.py --strict` 종료 코드 0 확인)

### #15 | onepage_output.png 한국어 화면으로 재캡처
- **행동:** 헤드리스 Chrome(`--force-device-scale-factor=2 --window-size=800,3817`)으로 `onepage_output.html`을 캡처해 기존 PNG를 교체.
- **근거:** README 상단 이미지가 중국어 화면이면 한국어 특화판 안내와 어긋남(B6 보고). 기존 PNG 크기(1600×7634)를 `sips`로 측정해 같은 크기로 맞춤 → README의 `width="800"` 표시와 호환.
- **결과:** 1600×7634 PNG 생성. 원래 해상도 부분 확대로 확인: Pretendard 적용, 어절 단위 줄바꿈(`keep-all`) 정상, 중국어 없음.

### #16 | B3 결과 검증 및 KO105 서술 불일치 수정
- **행동:** B3가 "대조하지 않았다"고 밝힌 gotchas.md의 숫자·단위 항목을 `lint-ko.py` KO105 구현(279행 "붙여 쓰세요… 제43항")과 대조, 불일치 부분을 직접 수정.
- **근거:** 지침 문서와 린터가 반대로 말하면 모듈 작성 에이전트가 린터 경고를 계속 유발함. 또한 B3 원문은 `개`를 "의존 명사"로 잘못 분류함(`개`는 단위 명사). research §2.1(국립국어원 "띄어쓰기의 이해"): 단위 명사는 띄어 쓰는 것이 원칙, 아라비아 숫자 뒤에서는 붙여 쓰기 허용.
- **결과:** "숫자+한글 단위 명사는 붙여 씀(허용 규정으로 통일), %·%p·°는 붙임, 영문 SI 기호는 한 칸 띄움"으로 정정 → 린터와 일치. 세 파일 한자 0줄 확인.

### #17 | B1 결과 검증 (SKILL.md)
- **행동:** 원본 SKILL.md의 기술 규칙 키워드 20개(styles.css·main.js 복사, build.sh, proximity, 100dvh, course-cover, KaTeX, briefs, data-steps 등)와 신규 규칙(lint-ko.py, korean-style-guide, glossary-ko, terms.md, lang="ko", 학습 목표, 확인 문제)의 존재를 grep으로 대조. 한자 grep.
- **근거:** 전면 재작성 시 원본 규칙 누락이 가장 큰 위험. `aligned`(KaTeX 팁)는 원본 SKILL.md에도 없고 gotchas.md에 있는 규칙이라 해당 파일에서 확인.
- **결과:** 모든 키워드 존재, 한자 0줄, frontmatter YAML 파싱 통과(B1이 Ruby `YAML.safe_load`로 확인). 전각 괄호 `（）` 2회는 "금지 예시"로 의도된 것.

### #18 | B2 결과 검증 및 통합 수정 (표지 중복 버그, <보기> 상자, 콜아웃 개수)
- **행동:** B2가 보고한 미결 사항 4건을 메인에서 직접 처리.
  1. `interactive-elements.md` 382·383·454·455행, `good.html` 픽스처, `SKILL.md` 문체 표의 해설 예시에서 `정답.`/`오답.` 접두를 제거하고 `② | …` / `| 정답은 ②이다. …` 형식으로 통일.
  2. `lint-ko.py`에 **KO110**(해설 속성이 `정답`/`오답`으로 시작하면 WARN) 추가, `bad.html`에 발화 사례 추가.
  3. `styles.css`에 `.bogi`(`<보기>` 상자) 추가, 스타일 가이드·예시 문서에 사용법 기재.
  4. 콜아웃 "모듈당 최대 2개" 제한을 선택 코너(보충 설명·더 알아보기)에만 적용, 고정 코너(학습 목표·핵심 정리)는 제외로 확정.
- **근거:** (1) `main.js`가 `'<strong>' + i18n('correct') + '</strong> ' + 해설`로 표지를 자동으로 붙이므로(#13), 해설에도 표지가 있으면 화면에 `정답 정답.`이 나옴 — 실제 출력 버그. (2) 같은 실수를 모듈 작성 에이전트가 반복할 수 있어 자동 검출 필요. (3) `<보기>` 상자는 EBS·평가원 보기형 문항의 핵심 형식(research §6.1)인데 CSS가 없어 에이전트마다 임의 마크업을 만들 위험. (4) EBS 흐름상 학습 목표·핵심 정리는 모든 모듈에 고정으로 들어가므로 이를 세면 선택 코너를 하나도 못 씀.
- **결과:** CSS 중괄호 360/360 균형. good 픽스처 `--strict` ERROR 0·WARN 0, bad 픽스처에서 KO110 2건 발화(ERROR 11·WARN 46). 저장소 전체 Markdown 한자 0줄. 용어집은 243개(요청 ~150개 초과) — 분량이 문제 되지 않으므로 유지. B2의 쟁점 용어 결정(regularization→규제, fine-tuning→미세 조정, gradient→그래디언트, 단 경사 하강법은 유지)은 `docs/logs/B2.md`에 근거 기재.

### #19 | Phase C1: 종단(E2E) 샘플 강의 생성 디스패치
- **행동:** 새 sonnet 에이전트에게 "Attention Is All You Need(arXiv 1706.03762)를 강의로 만들어 줘" 요청을 SKILL.md대로 처리하게 함(테스트용으로 모듈 3개로 축소). 출력 `examples/attention-ko/`, 린터 `--strict` 0/0까지 반복, 지시문의 모호·모순 지점 기록 요구.
- **근거:** 문서 단위 검증만으로는 "생성되는 출력이 실제로 한글·EBS 문체에 특화되는가"를 증명할 수 없음 → 완료 기준 PLAN §3-4(샘플 빌드 + lint 통과). 이전 맥락이 없는 새 에이전트를 써야 SKILL.md 지시문만으로 재현되는지 확인 가능. 린터 오탐을 에이전트가 린터 수정으로 덮지 못하게 린터 수정 금지.
- **결과:** 실행 중.

### #20 | C1 결과 분석과 분류
- **행동:** C1 보고(`docs/logs/C1.md`)의 지적 사항을 분류. 결과: 린터 오탐 1건, 출력 버그 2건(해설 속 `$수식$` 미렌더링, 의사코드 컨트롤이 컨테이너 밖에 있어 버튼 미동작), 결과 막대의 `%` 고정 표시, 문서 사이 모순 14건, 골격 마크업 미기재 2건.
- **근거:** 실제로 SKILL.md만 보고 만든 결과물에서 드러난 문제이므로 모두 "생성 출력의 품질"과 직결됨. 문서 수정은 7개 파일에 걸친 판단 위주 작업이라 sonnet 에이전트(D1)에 결정 사항을 명시해 위임하고, 코드 수정(main.js·린터)은 범위가 작아 메인에서 직접 처리.
- **결과:** D1 디스패치(결정 15개 명시). 수치 검증은 web-fetch 에이전트로 병렬 실행.

### #21 | 린터 오탐 수정: `아니다` → 합니다체 오인 (KO102)
- **행동:** `FORMAL_RE`의 `[가-힣]니다`를 `(?!아)[가-힣]니다`로 변경, good 픽스처에 회귀 문장 `BLEU는 백분율 단위가 아니다.` 추가.
- **근거:** C1 샘플 `02-results.html:64` "BLEU의 단위가 아니다."가 WARN으로 잡힘. `아니다`는 한다체 부정 서술어라 EBS 문체에서 매우 자주 쓰임 → 방치하면 모든 강의에서 오탐 발생.
- **결과:** 단위 테스트: `아니다.`→미검출, `설명합니다.`/`모델입니다.`/`않습니다.`/`하십시오.`→검출. good `--strict` 0/0, 샘플 `--strict` ERROR 0·WARN 0.

### #22 | main.js 보강: 피드백 속 KaTeX 재렌더링, 결과 막대 단위·척도
- **행동:** `setFeedbackHTML()` 헬퍼 추가(innerHTML 설정 후 `renderMathInElement` 호출) 및 피드백 6곳 교체. `.result-comparison`에 `data-unit`(기본 `%`)·`data-max`(기본 100) 지원 추가. 샘플에 `data-unit="" data-max="45"` 적용.
- **근거:** KaTeX auto-render는 페이지 로드 때 한 번만 돌기 때문에 해설에 수식을 넣으면 원문 `$…$`가 그대로 보임(C1 지적). BLEU처럼 백분율이 아닌 지표에 `%`가 붙으면 잘못된 정보. 기본값을 기존 동작과 같게 두어 하위 호환 유지.
- **결과:** `node --check` 통과. 헤드리스 Chrome 실행: 피드백 수식 `.katex` 1개 렌더링 확인, 막대 값 `28.4,27.3,25.16,24.6`(단위 없음), 폭 `63.1%…`(45 기준).

### #23 | 업스트림 치명 버그 수정: `sidebarItems` TDZ로 main.js 전체 중단
- **행동:** 헤드리스 Chrome 콘솔에서 `Uncaught ReferenceError: Cannot access 'sidebarItems' before initialization`(main.js:184) 발견 → 143행 초기 `updateProgress()` 동기 호출을 `setTimeout(updateProgress, 0)`으로 지연.
- **근거:** `git show HEAD:references/main.js`에서도 같은 순서(117행 선언, 앞선 초기 호출)를 확인 → **업스트림 원래 버그**. 이 예외 때문에 파일 나머지가 실행되지 않아 `selectOption`/`checkQuiz`가 정의되지 않음(콘솔 오류 2건 추가 확인) → 퀴즈 등 모든 인터랙션이 동작하지 않음. 한국어 출력의 퀴즈·해설 검증이 불가능하므로 범위 안의 수정으로 판단.
- **결과:** 재실행 시 콘솔 오류 0건. 프로브 결과 `{"lang":"ko","katex":55,"rawDollar":0,"bodyFont":"Pretendard Variable…","wordBreak":"keep-all","quizWrong":"오답 | 정답은 ②이다. …","quizRight":"정답 ② | …"}` — 표지 한 번만 표시, 수식 원문 노출 0.

### #24 | 샘플 강의 수치 원문 대조
- **행동:** web-fetch 에이전트로 https://arxiv.org/html/1706.03762v7 의 Table 2·3과 하이퍼파라미터 추출 후 샘플의 모든 수치와 대조.
- **근거:** C1이 표 수치 일부를 기억에 의존했다고 보고 → 교재에 틀린 수치가 들어가면 안 됨.
- **결과:** 전부 일치(Transformer big 28.4/41.8, base 27.3/38.1, ConvS2S 25.16/40.46, GNMT+RL 24.6/39.92, 헤드 h=1 24.9·h=8 25.8·h=32 25.4, d_model 512·h 8·d_k 64, P100 8개·3.5일). 참고: h=16도 25.8이라 "8개가 최선"이라고 단정할 수 없음 — 샘플 확인 문제 해설도 이 점을 근거로 삼고 있어 정확.

### #25 | 한글 라벨의 모노스페이스 어절 간격 수정
- **행동:** 화면 캡처에서 `모듈  3개`, `인터랙티브  튜토리얼`처럼 어절 간격이 두 배로 보이는 문제 발견 → `:lang(ko)`에서 한글이 들어가는 라벨 11개 클래스(`.course-cover-badge`, `.course-cover-meta-item`, `.result-label`, `.chat-sender` 등)를 본문 폰트로 전환. 숫자 라벨(`.result-value`, `.line-num`, `.sidebar-item-num` 등)은 고정폭 유지.
- **근거:** JetBrains Mono에는 한글 글리프가 없어 한글은 대체 폰트로 그려지지만 공백은 Mono의 0.6em 폭을 써서 간격이 벌어짐. 숫자 정렬에는 고정폭이 필요하므로 한글 라벨만 선별.
- **결과:** 재캡처에서 정상 간격 확인. CSS 중괄호 361/361. 샘플의 styles.css·main.js를 references와 다시 동기화(복사 원칙 유지).

### #26 | D1 결과 검증 (문서 모순 정리)
- **행동:** 의사코드 예시의 컨트롤 위치를 main.js 호출부(`.pseudocode-translation` 단위로 `initPseudocodeWalkthrough` 호출, 786행)와 대조, 신설된 "모듈 골격과 내비게이션" 마크업의 `data-target`·`href`를 main.js 150·205행과 대조. 픽스처·샘플 린트 재실행.
- **근거:** 문서가 실제 코드와 다르면 C1에서 본 "버튼이 동작하지 않는" 결과물이 다시 생김.
- **결과:** 컨트롤이 `.pseudocode-translation` 안으로 이동했고 규칙 문장도 추가됨. nav-dot `data-target`, sidebar-item `href`가 main.js와 일치. 배경 표시는 `callout callout-info` + 제목 `배경 지식`으로 확정(D1 판단, 기존 CSS 재사용이라 수용). good·샘플 `--strict` 0/0.

### #27 | README 보강
- **행동:** "이 포크에서 달라진 점"에 EBS 교재 문체, 업스트림 main.js 버그 수정, 예시 강의 항목 추가.
- **근거:** B6가 README를 쓴 뒤에 생긴 변경(사용자 문체 지시 #11, 버그 수정 #22·#23, 샘플 #19)이 사용자 안내에 빠져 있었음.
- **결과:** 반영 완료.

### #28 | 완료 기준 최종 점검 (PLAN §3)
- **행동:** 저장소 전체 한자 grep, 린터, `node --check`, 샘플과 references의 동기화(`cmp`) 확인.
- **근거:** PLAN §3의 5개 완료 기준을 증거로 확인해야 작업을 끝낼 수 있음.
- **결과:**
  1. **중국어 잔존 0**: 남은 한자는 모두 의도된 것이다. `main.js`·샘플 `main.js`의 zh 사전(원본 보존, `lang="zh*"`에서만 사용), `lint-ko.py`의 한자 검출 정규식, 린터 픽스처(한자 병기·스크립트 예외 테스트, bad 케이스), `PLAN.md` 업스트림 진단 인용, research의 `적(的)` 설명, 작업 로그. 학습자에게 보이는 출력 파일(`_base.html`, `styles.css`, 예시 문서, SKILL.md, 샘플 강의 HTML)에는 0건.
  2. **기본값**: `_base.html` `lang="ko"`, Pretendard v1.3.9(HTTP 200), `word-break: keep-all`(헤드리스 Chrome 계산값으로 확인).
  3. **main.js**: `node --check` 통과, 콘솔 오류 0, UI 문구 EBS 문체 한국어.
  4. **샘플 빌드 + lint**: `examples/attention-ko` `build.sh` 성공, `lint-ko.py --strict` ERROR 0·WARN 0, styles.css·main.js가 references와 byte 단위로 동일.
  5. **로그**: 메인 `docs/WORKLOG.md`(#1–#28) + 하위 에이전트 로그 11개(`docs/logs/A1–A3, B1–B6, C1, D1.md`), 모두 행동/근거/결과 형식.
- **알려진 한계:** KO104는 서술격 조사 `이다`와 주격 `이`를 구분하지 못하고, 대소문자 혼합 약어(LoRA 등)는 조사 검사에서 제외한다(style-guide §3.3에 기재). EBS 문체 규칙 중 한다체·발문·해설 형식은 공개 집필 지침으로 확인하지 못해 "관행"으로 표기. 커밋은 하지 않음(사용자 요청 없음). 작업은 브랜치 `korean-localization`의 작업 트리에 보존.
