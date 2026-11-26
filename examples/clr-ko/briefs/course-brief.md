# 강의 공통 브리프: 공통 언어 런타임(CLR)의 기술 개요 (Meijer & Gough 2001)

## 작업 위치 (중요)
- **이 강의는 git worktree에서 만든다.** 강의 폴더는 `/Users/eugene/dev/paper2contents/.claude/worktrees/clr-course/examples/clr-ko`(아래 `$C`)이다.
- 작성하거나 수정하는 파일은 모두 `$C` 안에 있어야 한다.
- **참고 문서와 검사 도구는 원래 체크아웃의 최신본을 읽기 전용으로 쓴다.** 경로는 `/Users/eugene/dev/paper2contents/`(아래 `$M`)이다. 워크트리 안의 `references/`는 오래된 판이라 쓰지 않는다.
- `$M` 아래 파일은 절대 수정하지 않는다.
- git 명령은 쓰지 않으며, commit도 하지 않는다.

이 강의는 Erik Meijer와 John Gough의 "Technical Overview of the Common Language Runtime"(2001, 11쪽)을 한국어 인터랙티브 강의로 만든다. 모듈은 8개이고, 하위 에이전트 3개가 병렬로 작성한다. 너는 그중 일부 파일만 맡는다.

## 사용자 요구 (이 세션에서 확정된 선호)
1. **삽화와 도표를 충분히 넣는다.**
   - 본문 쪽(확인 문제 쪽 제외)마다 다음 중 하나 이상을 둔다: 개념 도식(인라인 SVG), 데이터 표, 그래프, CIL 코드와 스택 상태 그림.
   - 도표 규칙은 `$C/briefs/diagram-guide.md`를 따른다. §2 CLI/JVM 도식 규칙과 §5 GitHub 도표 skill 규칙이 핵심이다.
2. **이전 연구의 한계와 등장 배경**을 충분히 설명한다(2단원).
3. **이후 동향** 단원을 둔다(8단원).
4. **설명을 줄이지 않는다.** 그림, 표, 구체 예시로 보강해 처음 배우는 사람도 따라올 수 있게 한다. 전문 용어에는 반드시 툴팁과 쉬운 풀이를 단다.
5. 비교표 아래 요약 문장은 `<p class="diff-line"><strong>핵심 비교</strong> …</p>`로 쓴다. "차이 한 줄"이라는 이름은 쓰지 않는다.
6. baseline이 나오면 "기준선"으로 쓴다.
7. **하이픈 뒤에 붙는 기호는 KaTeX로 쓰지 않는다.**
   - 본문에서는 `<i class="mi">n</i>`처럼 HTML로 쓴다.
   - 화면 제목(`h3.screen-heading`) 안에 `<i>`, `<code>`, 수식 같은 인라인 요소가 있으면 제목 글자 전체를 `<span>…</span>` 하나로 감싼다. 감싸지 않으면 flex gap 때문에 글자 사이가 벌어진다.
8. 방법(명령어 설계)마다 **대가와 한계**를 함께 쓴다. 예:
   - 다형 명령어는 JIT의 부담을 늘린다.
   - tail call은 보안 경계에서 프레임을 버리지 못한다.
   - unmanaged pointer, 공용체, 주소 산술은 검증할 수 없다.
   - boxing에는 할당 비용이 든다.
9. **이 논문은 실험이 없는 설명·주장 논문이다.** "CLI가 더 낫다"는 저자의 주장으로 쓰고, 해석임을 드러낸다("논문은 ~라고 주장한다", "~로 해석할 수 있다"). 저자의 이해관계(Microsoft 소속, CLR 컴파일러 저자)는 2단원이나 7단원의 한계 부분에서 한 번 언급한다.
10. **코드 예시**
    - CIL 코드는 `<pre><code>` 블록으로 쓴다. 마크업은 `$M/references/interactive-elements.md`의 코드 블록과 의사코드 단계별 풀이를 따른다.
    - 논문 코드는 그대로 옮긴다.
    - 이해를 돕는 C#이나 Java 원천 코드는 "예시"로 밝히고 짧게 쓴다.

## 단원 구성
| 파일 | 화면 번호 | id | 제목 | 논문 위치 | id 접두사 | 담당 |
|---|---|---|---|---|---|---|
| modules/00-background.html | 1 | module-0 | 서론과 배경 | 1절 + 선수 개념 | `bg-` | A |
| modules/01-prior.html | 2 | module-1 | 이전 연구와 JVM의 한계 | 1절, 참고문헌 | `pr-` | A |
| modules/02-architecture.html | 3 | module-2 | CLI 구조와 어셈블리 | 2, 3절 | `ar-` | A |
| modules/03-types.html | 4 | module-3 | 타입 시스템과 기본 명령어 | 4, 5절 | `ty-` | B |
| modules/04-values.html | 5 | module-4 | 값 타입과 참조 타입 | 6, 7, 9절 | `va-` | B |
| modules/05-calls.html | 6 | module-5 | 메서드 호출과 특수 명령어 | 8, 10절 | `ca-` | C |
| modules/06-verification.html | 7 | module-6 | 검증 | 11, 12절 | `ve-` | C |
| modules/07-trends.html | 8 | module-7 | 이후 동향 | 논문 밖 보충 | `tr-` | C |

- `_base.html`과 `_cover.html`은 메인 에이전트가 이미 썼으므로 건드리지 않는다.
- 다른 단원을 가리킬 때는 화면 번호를 쓴다(예: "4단원").
- 모듈 파일은 `<section class="module" id="module-N">` 블록만 담는다. 골격은 `$M/examples/rag-lewis-ko/modules/*.html`이나 `$M/examples/attention-ko/modules/*.html`을 그대로 따른다.
- **전체에 꼭 들어가야 하는 요소와 위치**
  - 수식 유도 단계별 풀이: 1단원의 n+m 대 n×m 계산
  - 연구 계보 트리: 2단원
  - 의사코드(CIL 코드) 단계별 풀이: 4단원 Swap
  - 결과 비교 인터랙티브: 6단원 call/callvirt, 그리고 CLI 대 JVM 비교 전환(탭이나 토글)
  - 각 단원의 확인 문제

## 담당별 내용
### A: 00-background, 01-prior, 02-architecture
- **00 서론과 배경**
  - **첫 쪽** (논문 1절, paper-ref "논문 1절", `배경 지식` 콜아웃 없음)
    - 왜 썼나: JVM 위에 다른 언어를 올리려는 시도가 늘었지만, JVM은 다중 언어 플랫폼으로는 최적이 아니다.
    - 이전 대 제안 비교 그림: 여러 언어 → JVM(우회책 필요) / 여러 언어 → CLI(직접 대응).
    - 새로운 점 3개 이내.
    - 용어 정리를 넣는다: CLI는 명세, CLR은 Microsoft 구현, CIL은 중간 언어.
  - **배경 쪽** (각 쪽 맨 위에 `배경 지식` 콜아웃. A가 RAG 강의에서 한 것처럼 cue 맨 위에 두어도 된다)
    - ① 컴파일러, 기계어, 인터프리터, 가상 머신, 중간 언어. 논문이 든 여섯 가지 이유(Portability, Compactness, Efficiency, Security, Interoperability, Flexibility)를 표로 정리한다.
    - ② **n+m 대 n×m 수식 유도 단계별 풀이**와 그림. 예시: 언어 3개, 플랫폼 3개.
    - ③ 스택 머신과 평가 스택. `2+3*4`를 스택 명령어로 계산하는 예시와 스택 상태 그림을 넣고, 삽화 `fig-plates`를 쓴다.
    - ④ JIT 컴파일: 중간 코드 → 실행 직전 기계어. 인터프리터와 비교한다.
    - ⑤ 타입 안전성과 GC, managed code.
  - 지식 지도 SVG와 확인 문제 3~5문항을 넣는다.
- **01 이전 연구와 JVM의 한계**
  - 계보: UNCOL(1958) → UCSD P-code → ANDF → AS/400 → JVM → CLI. `.lineage-note`와 `.novelty`를 쓰고, 연대와 무엇을 남겼는지를 적는다. 참고문헌에 있는 사실만 쓴다.
  - JVM이 인기 있는 이유: 고수준 런타임, 보급, 라이브러리.
  - **JVM의 한계를 언어 기능별 표로** 정리한다. 표 열: 기능, 필요한 언어, JVM에서 막히는 이유, 우회책. 1절 목록과 본문(5~10절)에 나온 우회책을 쓴다.
    - 참조 매개변수 → 원소 하나짜리 배열이나 box 클래스
    - tail call → trampoline
    - 공용체 → 클래스 계층
    - 오버플로 → 매 연산 검사
    - 64K 분기 제한
    - 다차원 배열
  - **한 예를 그림으로 따라간다**: Scheme의 재귀 루프를 JVM에서 trampoline으로 돌리는 구조와 CLI의 `tail.`을 비교한다. 개념 그림이며, 코드는 예시이다.
  - "그래서 CLI는 무엇을 했나": 처음부터 다중 언어 설계, 언어 구현자와 협력(tail call 명령어가 그 결과), 지원 범위(명령형·정적 OO는 좋고, 비표준 패러다임은 개선 중). `기준 × 플랫폼` 비교표와 핵심 비교를 넣는다.
  - 저자의 이해관계를 언급한다.
- **02 CLI 구조와 어셈블리**
  - 스레드 = 활성 레코드 연결 리스트(그림).
  - **활성 레코드 구성 요소 8가지**를 그림 하나와 표로 보인다: IP, 평가 스택, 지역 변수 배열, 인수 배열, methodInfo, 지역 메모리 풀, return state, 보안 기술자. JVM과 다른 점(인수·지역 분리, 타입 고정)을 교과 색으로 표시한다.
  - 저장 위치 크기: JVM은 4바이트 고정, CLI는 다형적이다(그림: long과 double이 JVM에서 두 칸 대 CLI에서 한 칸).
  - 어셈블리: 파일 묶음, 매니페스트, 메타데이터, custom attribute. ILASM 예는 줄별 설명을 단다. JAR와 비교표를 넣고 삽화 `fig-container`를 쓴다. 최상위 메서드와 필드도 다룬다.
  - 확인 문제를 넣는다.

### B: 03-types, 04-values
- **03 타입 시스템과 기본 명령어**
  - 기본 타입 표, 타입 생성자.
  - 자연 크기 타입: `native int`가 Pentium에서 int32, IA64에서 int64인 그림.
  - **포인터 세 종류 메모리 그림**: object, managed `&`(객체 내부 가능, 힙 밖도 안전), unmanaged `*`(힙 안은 금지). GC가 객체를 옮길 때 무엇이 갱신되는지를 보인다.
  - JVM의 단일 참조 타입과 비교한다.
  - 명령어 약 220개, 다형 명령어 대 JVM 타입별 명령어(`add` 하나 대 iadd/ladd/fadd/dadd). 비교 그림을 넣고 대가(JIT 부담)를 쓴다.
  - load/store 계열 표.
  - **Swap 의사코드 단계별 풀이**: 줄별 설명과 각 줄 뒤의 평가 스택 상태. 예시 값은 x=3, y=5, 주소는 예시이다. 호출하는 쪽 코드도 넣고, JVM 우회책(원소 하나짜리 배열)과 나란히 비교한다.
  - 산술 오버플로(`add`, `add.ovf`, `add.ovf.un`): int32 예시 계산(2147483647 + 1)과 float 무한대.
  - 분기: jsr 없음, 64K 제한 없음.
  - 논문 오기(stloc 설명)는 바로잡아 쓰되 굳이 강조하지 않는다.
- **04 값 타입과 참조 타입**
  - 값 타입 대 참조 타입 저장 위치 그림.
  - Point 구조체, FloatOrInt 공용체(바이트 겹침 그림: 같은 4바이트를 f와 n이 공유). 3.14를 넣고 int로 읽는 코드를 줄별로 설명한다. 읽히는 정수 값은 IEEE-754 비트 패턴 0x4048F5C3 = 1078523331이다(직접 계산한 값이므로 "계산 값"으로 밝힌다).
  - enum Shape, initobj.
  - JVM에서는 클래스나 클래스 계층으로 흉내 내야 하고, 타입 안전하지 않은 기법은 아예 불가능하다.
  - 참조 타입: Foo/Bar 클래스(코드를 따른다: f는 virtual, g는 instance, h는 static), 메서드 세 종류 표.
  - newobj 대 JVM의 `new; dup; invokespecial`: 스택 상태 비교 그림. 검증기가 복잡해지는 이유를 쓴다.
  - **boxing/unboxing**(9절): 값 → 힙 상자 복사 그림, 삽화 `fig-parcel`. 컬렉션에 Point를 넣는 예시, 다형 함수형 언어의 균일 표현, 대가(할당과 복사).
  - 확인 문제를 넣는다.

### C: 05-calls, 06-verification, 07-trends
- **05 메서드 호출과 특수 명령어**
  - call, call instance, callvirt. **결과 비교 인터랙티브**: 같은 `bar` 객체에 대해 명령어를 바꾸면 실행되는 메서드(Foo::f 대 Bar::f)가 바뀌는 토글이나 탭. 정적 타입 대 동적 타입 그림을 넣는다.
  - JVM 명령어 대응표: invokestatic/invokespecial/invokevirtual/invokeinterface 대 call/callvirt.
  - tail call: Bottom 예, 스택 프레임 그림(tail.이 없으면 프레임이 쌓이고, 있으면 교체된다), 재귀 언어. 보안 경계에서의 제약, JVM은 trampoline.
  - 10절: ldftn/calli(디스패치 테이블 그림), jmp(다중 상속 this 조정 trampoline stub), localloc(활성 레코드 확장 대 힙 할당), ldtoken(reflection, Class.forName과 바인딩 시점 비교).
  - 확인 문제를 넣는다.
- **06 검증**
  - 검증이 무엇을 보장하나: 배포나 로드 시점, 생산자를 신뢰하지 않음. 삽화 `fig-inspector`.
  - 정적으로 못 하는 것은 런타임 검사(경계 검사, 축소 형변환).
  - **합류 지점 규칙 그림**: if/else 두 경로가 만나는 곳에서 스택 높이와 타입. 최소 공통 조상 예시(Bar와 Baz가 합류하면 Foo). 통과 예와 실패 예를 함께 보인다.
  - 검증할 수 없는 것: block copy, 주소 산술, 타입 안전하지 않은 대입, 일부 공용체(각주 3).
  - reference surrogate: 고정 크기 값 배열 → 참조 배열(그림).
  - peverify와 Gardens Point Component Pascal 부트스트랩 일화.
  - 12절 결론과 한계: 저자 주장, 이해관계, 2001년 시점, 실험 없음.
  - 확인 문제를 넣는다.
- **07 이후 동향**
  - 논문 밖 보충이므로 paper-ref를 달지 않는다. 첫 쪽 콜아웃에 "논문 이후의 보충, 조사 시점 2026년 11월"을 밝힌다.
  - `briefs/research.md` 끝의 후보를 **WebFetch로 1차 출처(공식 문서, 표준, 논문, 저장소)에서 확인한 뒤** research.md에 확인된 주장과 함께 추가하고 쓴다. 확인 못 한 것은 쓰지 않는다.
  - 정리 틀: "무엇을 풀려는가 → 핵심 아이디어 그림 → 한계·비용 → 2001년 논문의 어느 칸에서 이어지나".
  - 추천 축:
    - ① 표준화와 오픈 소스: ECMA-335, Mono, .NET Core
    - ② 논문이 예고한 제네릭(Kennedy & Syme [16]) → .NET 2.0
    - ③ managed pointer가 언어로 드러난 `Span<T>`, ref
    - ④ JIT 대 AOT(NativeAOT)
    - ⑤ JVM 쪽의 응답: invokedynamic, Valhalla
    - ⑥ WebAssembly
    - ⑦ CLR 위의 함수형 언어 F#
  - 마지막에 한눈에 비교표와 더 읽을거리를 둔다.

## 반드시 먼저 읽을 것
- `$M/SKILL.md`가 없으면 `/Users/eugene/.claude/skills/paper-to-course/SKILL.md`를 읽는다. 특히 다음 부분이다.
  - "용어 표기"
  - "작성 규칙 (필수, 모든 모듈에 적용)"
  - Phase 3의 학습서 구성
  - 코넬 페이지 규칙
- `$M/references/`
  - `korean-style-guide.md` 전체
  - `interactive-elements.md`: **여기 있는 클래스와 마크업만 쓴다.** CSS와 JS는 새로 만들지 않는다.
  - `design-system.md`(색상 규약, 그림 정렬 규칙)
  - `illustration.md`, `content-philosophy.md`, `gotchas.md`
- 이 강의의 브리프
  - `$C/briefs/terms.md`: 반드시 따른다.
  - `$C/briefs/research.md`: **주장과 사실은 여기 있는 것만 쓴다.**
  - `$C/briefs/diagram-guide.md`
- 형식 참고: `$M/examples/rag-lewis-ko/modules/`와 `$M/examples/attention-ko/modules/`(최근 판). 코넬 쪽, SVG 클래스, 퀴즈, 토글, 수식 단계 풀이, 의사코드, 연구 계보의 실제 마크업을 보여 준다.

## 형식 제약
- **쪽 구성**
  - 한 화면 = `.screen.cornell` 1장이다. 1440×900에서 쪽 높이는 765px 이하이다.
  - 단원마다 본문 쪽은 3~8개이다(확인 문제 쪽 제외).
  - 확인 문제는 3~5문항이다.
    - 문제 쪽당 최대 2문항이다.
    - 하나 이상은 부정형이나 `<보기>`형이다.
  - 단원 첫 쪽 cue에 `학습 목표` 2~3개를 둔다. 도입은 `이 모듈을 학습하면 다음을 할 수 있다.`이다.
- **용어와 출처 표기**
  - `paper-ref`는 논문 내용일 때만 단다.
  - 용어는 첫 등장에 `term` 툴팁을 단다. 정의는 명사형으로 끝낸다. 표기는 terms.md의 첫 등장 표기를 쓰고, 모듈마다 다시 병기한다.
  - 수식은 모두 이탤릭(`\mathit`, KO112 0건)이다. 그림 속 수학 기호도 이탤릭이다.
- **id와 링크**
  - id는 강의 전체에서 유일해야 한다. 새 id, marker id, 퀴즈 id, 토글 id에 위 표의 접두사를 붙인다.
  - 출처 링크는 `<a href target="_blank" rel="noopener">`로 단다.
  - 외부 `<img>`, `<script>`, `<link>`는 금지한다.
- **그림**
  - 색은 먹색과 교과 색만 쓴다.
  - 간선은 직각으로 그린다.
  - 노드 라벨은 `foreignObject > div.node-label > span`으로 쓴다. inline flex 정렬 스타일은 넣지 않는다.
- **작업 범위**
  - 맡은 파일 외에는 수정하지 않는다. 예외로 C는 research.md에 추가만 할 수 있다.
  - terms.md에 없는 용어가 필요하면 보고에 적는다.

## 검증 (반드시 실행)
```bash
C=/Users/eugene/dev/paper2contents/.claude/worktrees/clr-course/examples/clr-ko
M=/Users/eugene/dev/paper2contents
bash $C/build.sh
python3 $M/references/lint-ko.py --strict $C/modules/<맡은 파일>   # 파일마다 ERROR 0, WARN 0
python3 $M/references/check-pages.py $C                             # 맡은 단원 넘침 0, 그림 정렬 0
```
- **다른 에이전트와의 동시 작업**
  - 다른 에이전트가 동시에 빌드한다. 다른 단원 문제나 파일이 아직 없어서 생기는 일시적 실패는 무시하고 다시 실행한다.
  - 삽화 3개 미만 경고는 초기에 무시한다.
- **렌더링 확인**
  - 실행 명령: `cd / && SHOT_TMP=__shot_<담당>_<module>.html ~/.cache/paper-to-course/venv/bin/python -P /Users/eugene/dev/paper2contents/.claude/worktrees/clr-course/.work/scripts/shot.py $C module-N <출력폴더>`
  - 출력 폴더는 `/Users/eugene/dev/paper2contents/.claude/worktrees/clr-course/.work/<담당>/` 아래에 둔다.
  - 맡은 단원의 모든 쪽을 PNG로 만들어 Read로 직접 본다. 잘림, 겹침, 작은 글자, 정렬, 수식 오류, 코드 줄바꿈을 고친다.
  - 끝나면 강의 폴더에 `__shot*.html`이 남지 않게 지운다.
- **마지막 보고** (한국어, 짧게)
  - 쪽 제목 목록과 문항 수
  - 도식, 표, 삽화 수
  - 사용한 출처
  - terms.md에 추가가 필요한 용어
  - 남은 문제
