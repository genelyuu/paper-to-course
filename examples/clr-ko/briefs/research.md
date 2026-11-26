# 확인된 출처와 사실

**규칙**: 주장과 수치는 이 파일에 있는 것만 쓴다. 원 논문 텍스트 추출본은 `/Users/eugene/dev/paper2contents/.claude/worktrees/clr-course/.work/pdf/p.txt`(11쪽, 2001년 10월 PDF, pdfTeX)이다. 필요하면 직접 grep 한다. 직접 만든 예시 값과 코드는 "예시"라고 밝힌다. 조사 시점: 2026년 11월.

## 원 논문: Erik Meijer (Microsoft), John Gough (QUT), "Technical Overview of the Common Language Runtime", 2001
게재처는 추출본에 없다. 표지와 본문에는 **연도 2001**만 쓴다.

### 초록
- .NET의 기능은 CLI의 능력에 기반한다.
- CLI는 다른 VM 기반 시스템과 달리 처음부터 넓은 범위의 언어를 지원하도록 설계했다.
- ECMA 표준화로 여러 플랫폼에서 쓰일 것으로 기대한다.
- JVM은 다른 제약 아래 설계되어 Java가 아닌 언어에는 훨씬 어려운 대상이다.
- 여러 언어 구성 요소를 CLI 기본 연산에 대응시키는 문제도 짧게 다룬다.

### 1절 (서론)
**VM, 중간 언어, 언어 독립 실행 플랫폼의 예**
- UNCOL [6], UCSD P-code [23], ANDF [20], AS-400 [25]
- 하드웨어 에뮬레이터(VMWare), Transmeta Crusoe [30], 이진 번역 [26]
- JVM [19], CLI [2]

**중간 경로를 쓰는 이유 6가지**
- **Portability**: 중간 언어를 쓰면 언어 n개를 플랫폼 m개에 구현하는 데 번역기가 n×m개가 아니라 **n+m개**만 있으면 된다.
- **Compactness**: 중간 코드는 원본보다 작은 경우가 많다. 동적으로 내려받는 코드에서 다시 중요해졌다.
- **Efficiency**: 특정 네이티브 플랫폼에 묶이는 시점을 최대한 늦춰, 실행 플랫폼이 기계 지식이나 프로그램의 동적 행동에 맞게 최적화할 수 있다.
- **Security**: 고수준 중간 코드는 저수준 바이너리보다 보안 제약과 타입 제약을 배포 시점과 실행 시점에 강제하기 쉽다.
- **Interoperability**: 공통 타입 시스템과 고수준 실행 환경(공통 GC 힙, 스레딩, 보안 등)을 공유하면 언어 사이의 상호 운용이 바이너리 수준의 상호 운용보다 쉽다. 이는 다중 언어 라이브러리 설계와 컴포넌트 재사용의 전제 조건이다.
- **Flexibility**: 고수준 중간 코드와 메타데이터를 합치면 (타입 안전한) 메타프로그래밍을 만들 수 있다. 예: reflection, 동적 코드 생성, 직렬화, 타입 탐색.

**JVM을 쓰는 이유와 JVM의 한계**
- JVM의 고수준 런타임 지원, 넓은 보급, 풍부한 Java 라이브러리 때문에 많은 언어 구현자가 JVM을 실행 환경으로 택했다 [29, 7].
- 저자들은 JVM이 **본질적으로 최적이 아닌 다중 언어 플랫폼**이라고 주장한다.
- 타입 안전하지 않은 기능을 인코딩할 방법이 없다: 포인터, immediate descriptor(tagged pointer), 안전하지 않은 형변환.
- Java에 없는 언어 기능을 구현할 기본 연산이 부족하다: unboxed structure와 union(레코드, 가변 레코드), 참조 매개변수, varargs, 다중 반환값, 함수 포인터, 오버플로 감지 산술, lexical closure, tail call, 완전 동적 dispatch, 제네릭, 구조적 타입 동치 등.

**CLI의 설계와 지원 범위**
- CLI는 처음부터 다중 언어 대상으로 설계했다. Microsoft는 개발 초기부터 상업·학계 언어 구현자들과 협력했다(www.gotdotnet.com).
- 예: **tail call 명령어는 언어 연구자들의 의견을 반영해 직접 추가했다.** 재귀가 유일한 반복 수단인 선언적 언어에서 tail call은 효율의 필요조건이다.
- 저자들도 CLI가 아직 완벽한 다중 언어 플랫폼은 아니라고 인정한다.
  - 지원이 좋은 쪽: 명령형 언어(COBOL, C, Pascal, Fortran)와 정적 타입 OO 언어(C#, Eiffel, Oberon, Component Pascal).
  - 비표준 패러다임 지원은 개선 중이다 [16].

### 2절 (구조)
**스레드와 활성 레코드**
- CLI는 여러 동시 스레드를 관리한다. 반드시 OS 스레드일 필요는 없다.
- 스레드는 활성 레코드의 단일 연결 리스트로 볼 수 있다.
  - 메서드 호출이 레코드를 만들고 현재 레코드에 연결한다.
  - 완료되면(정상 return, tailcall, 예외) 레코드를 제거한다.
- 런타임 스택에 할당하는 경우가 보통이지만 필수는 아니다.
- 논문에서 "stack"은 **평가 스택**만 가리킨다.

**메서드 상태(활성 레코드)의 구성 요소**
- 명령어 포인터(IP)
- 평가 스택: 중간값을 담는다. JVM 용어로는 operand stack.
- 0부터 번호를 매기는 지역 변수 배열
  - 어떤 타입이든 담을 수 있지만, 한 변수는 타입 일관되게 써야 한다.
  - JVM에서는 한 지역 변수가 어떤 때는 정수, 어떤 때는 float을 담을 수 있다.
- 0부터 번호를 매기는 인수 배열: **JVM과 달리 인수 배열과 지역 변수 배열이 따로 있다.**
- methodInfo 핸들: 시그니처, 지역 변수 타입, 예외 처리기 정보를 담는다.
- 지역 메모리 풀: 동적 할당용이다.
- return state 핸들: 반환할 때 상태를 복원한다. 동적 링크에 해당한다.
- 보안 기술자: assert, permit-only, deny 같은 보안 재정의를 기록한다. managed code가 직접 접근할 수 없고, 보안 메커니즘은 논문 범위 밖이다.

**저장 위치의 크기**
- JVM: 모든 저장 위치(지역 변수, 스택 슬롯, 인수)가 **4바이트**이다.
- CLI: 저장 위치가 다형적이다. 4바이트(32비트 정수)일 수도 있고 수백 바이트(사용자 정의 값 타입)일 수도 있다. 다만 **타입은 프레임이 살아 있는 동안 고정**된다.

### 3절 (어셈블리)
- 어셈블리는 CIL 코드와 메타데이터를 담은 파일(모듈)의 집합이며, CLI 소프트웨어 컴포넌트의 기본 단위이다.
- 보안, 버전 관리, 타입 해석, 프로세스(응용 프로그램 도메인)가 모두 어셈블리 단위로 동작한다. JVM에 비유하면 대략 **JAR 파일**에 해당한다.
- 매니페스트는 다음을 기술한다: 버전, 구성 파일, 내보내는 타입, (선택) 매니페스트 자체의 디지털 서명과 공개 키.
- ILASM 예:
  ```
  .assembly HelloWorld {}
  .assembly extern mscorlib {
    .publickeytoken = (B7 7A 5C 56 19 34 E0 89)
    .ver 1:0:2411:0
  }
  ```
- 어셈블리나 모듈 안에 정의할 수 있는 것:
  - 참조 타입: 클래스, 인터페이스, 배열, 대리자
  - 값 타입: 구조체, enum
  - 중첩 타입
- **JVM과 달리 최상위 메서드와 필드를 허용한다.**
- 모든 선언은 메타데이터에 들어간다. 메타데이터는 **custom attribute로 사용자가 확장할 수 있다**. 논문은 이를 CLI만의 특징이라 부른다.

### 4절 (타입 시스템)
더 형식적인 설명은 Gordon & Syme [8], POPL'01에 있다.

**기본 타입**
- `object`(System.Object), `string`(System.String), `void`
- `bool`(8비트), `char`(16비트 Unicode)
- `int8`~`int64`와 각각의 unsigned, `native int`, `unsigned native int`
- `float32`, `float64`, `native float`(사용자에게 보이지 않음)
- `typed reference`: 포인터와 타입의 쌍. 타입 안전한 varargs에 쓴다.

**타입 생성자**
- `valuetype typeref`, `class typeref`
- `type pinned`: GC가 옮기지 못하게 한다(범위 밖).
- `type[bounds]`: 다차원 배열이다(범위 밖). **CLI는 JVM과 달리 진짜 다차원 배열을 지원한다.**
- `method callConv type*(parameters)`: 함수 포인터(범위 밖).
- `type&`: managed pointer
- `type*`: unmanaged pointer

**자연 크기 타입**
- 해당 타입: `native int`, `unsigned native int`, `object`, `&`, `*`
- 값의 크기 결정을 미루는 장치이다. JIT 시점이나 실행 시점에 프로세서의 자연 크기로 정한다.
- 예: `native int`는 Pentium에서 int32, IA64에서 int64이다.

**포인터 종류**
- `object`: CLI가 관리하는 객체 참조.
- managed pointer `&`
  - object와 비슷하지만 **객체 내부**를 가리킬 수 있다. object 참조와 서로 바꿔 쓸 수 없다.
  - managed heap **밖**을 가리켜도 안전하다. GC가 힙 경계를 알기 때문이다.
- unmanaged pointer `*`와 `native int`
  - 전통적인 주소이며, 네이티브 코드와 상호 운용하는 데 필수이다.
  - managed heap 안을 가리키면 안 된다. GC가 객체를 옮기고 압축하기 때문이다.

**JVM과의 비교**
- JVM은 모든 저장 위치를 미리 32비트로 정해 버린다. 그래서 long과 double이 위치 두 칸을 차지해 컴파일러 작성자를 괴롭힌다.
- 더 큰 약점은 모든 포인터를 참조 타입 하나로 묶어 버려, 더 세밀한 포인터 구분이 필요한 언어나 컴파일러의 길을 막는다는 점이다.

### 5절 (기본 명령어 집합)
**명령어 수와 타입 정보**
- CLI에는 명령어가 **약 220개** 있다. 많은 명령어에 짧은 형식이 있다.
- JVM은 대부분의 명령어에 인수 타입을 박아 넣는다(iload, fload 등).
  - 해석하기는 쉽지만 컴파일러마다 부담이 된다.
- CLI 명령어는 훨씬 다형적이다. 보통 결과 타입만 명시한다.
  - 컴파일러가 CIL을 만들기는 쉽지만 JIT가 할 일이 늘어난다.

**5.1 상수, 인수, 지역 변수, 포인터**
- `ldc.t v`: 타입 T의 값 v를 push한다. T ∈ {int32, int64, float32, float64}이다.
- `ldnull`: null 참조를 push한다.
- 인수: `ldarg n`(push), `ldarga n`(n번째 인수의 주소를 managed pointer `T&`로 push), `starg n`(pop해 n번째 인수에 저장).
- 지역 변수: `ldloc n`, `ldloca n`(주소), `stloc n`.
  - 논문 본문은 stloc이 "n-th argument"에 저장한다고 썼다. **지역 변수의 오기이므로 강의에서는 지역 변수로 쓴다.**
- JIT는 이 값들의 타입을 메서드 시그니처와 문맥에서 안다.
- `ldind.t`: 주소(native int, unmanaged 또는 managed pointer)를 역참조해 값을 push한다.
- `stind.t`: 스택에 있는 주소에 값을 저장한다. 두 명령어 모두 JIT가 결과 타입을 항상 추론하지는 못하므로 t가 필요하다.
- 필드: `ldfld`, `ldsfld`, `stfld`, `stsfld`, `ldflda`, `ldsflda`. 배열에도 비슷한 명령어 계열이 있다.

**Swap 예 (참조 인수)**
```
.method static void Swap(int32& xa, int32& ya) {
  .maxstack 2
  .locals (int32 z)
  ldarg xa; ldind.i4; stloc z
  ldarg xa; ldarg ya; ldind.i4
  stind.i4; ldarg ya; ldloc z
  stind.i4; ret // return
}
```
- 호출하는 쪽:
  ```
  .locals (int32 x, int32 y)
  ldloca x
  ldloca y
  call void Swap(int32&, int32&)
  ```
- `.maxstack 2`이므로 평가 스택은 최대 2칸까지 쌓인다. 줄별 스택 상태 표는 강의에서 직접 계산해 보인다.
- JVM에서 같은 일을 하려면
  - 타입마다 load/store 명령어가 따로 있다: iload, aload, dload(64비트 값 두 칸), fload, lload.
  - 지역 변수의 주소를 가져올 수 없어 byref 인수를 직접 구현할 수 없다. 그래서 원소 하나짜리 배열을 넘기거나 명시적 box 클래스를 쓰는 편법이 필요하다(JVM은 boxing/unboxing도 지원하지 않는다).
  - 설계 공간에 대한 자세한 정리는 Gough [12]에 있다.

**5.2 산술**
- `add`는 스택 맨 위 두 값을 더한다.
- 정수 오버플로는 `.ovf`(부호 있음)나 `.ovf.un`(부호 없음)을 붙여야 감지한다.
- 부동소수점 오버플로는 +∞나 −∞를 돌려준다.
- JVM은 정수 연산에서 오버플로를 알리지 않는다. 그래서 오버플로 감지가 필요한 언어(Ada95, SML)에서는 시간 손해가 클 수 있다.
- JVM은 타입마다 add 명령어가 따로 있다.

**5.3 단순 제어 흐름**
- 분기 명령어: br, beq, bge 등.
- JVM의 "jump subroutine"(jsr) 같은 명령어가 없다.
- **JVM처럼 분기 길이를 64K로 제한하지 않는다.** 사람에게는 큰 문제가 아니지만 JVM 바이트코드를 생성하는 컴파일러에는 실제 문제이다.

### 6절 (값 타입)
**값 타입의 성질**
- C의 struct나 Pascal의 record와 비슷하다.
- 참조 타입은 늘 GC 힙에 할당하지만, 값 타입은 "제자리(in place)"에 할당한다.
- 값 타입도 (정적, 가상, 인스턴스) 메서드를 가질 수 있다.

**6.1 구조체**
```
.class value Point {
  .field public int x
  .field public int y
}
```
CLI는 필드를 어떤 순서로든 저장할 수 있다.

**6.2 공용체**
- 순차 배치와 명시적 배치를 지원한다. C식 union은 명시적 배치로 만든다.
```
.class value explicit FloatOrInt {
  .field [0] public float32 f
  .field [0] public int32 n
}
```

**6.3 enum**
```
.class enum Shape {
  .field public static valuetype Shape RECTANGLE = int32(0)
  .field public static valuetype Shape CIRCLE = int32(1)
}
```
내부 저장 타입과 비트 집합 여부도 지정할 수 있다.

**6.4 초기화**
- `initobj T`는 스택에 있는 값 타입 주소의 모든 필드를 null이나 0으로 초기화한다. 논문은 "polytypic 명령어"의 예로 든다.
- 예: `.locals (valuetype Point p)` → `ldloca p` → `initobj Point`

**JVM과의 비교**
- JVM으로 컴파일하면 enum과 struct를 클래스로, union을 클래스 계층으로 표현해야 해서 비효율적이다 [4, 5장].
- 더 심각한 문제는 의미를 온전히 지원할 수 없다는 점이다. 예: float를 넣고 int로 읽는 타입 안전하지 않은 기법.
```
.locals (valuetype FloatOrInt fi, int32 n)
// fi.f = 3.14
ldloca fi
ldc.r4 3.14
stfld float32 FloatOrInt::f
// n = fi.n
ldloca fi
ldfld int32 FloatOrInt::n
```

### 7절 (참조 타입)
**참조 타입과 메서드 종류**
- 클래스, 인터페이스, 배열, 대리자가 있다. 논문은 클래스만 다룬다.
- 가상 메서드와 정적 메서드(Eiffel, Java처럼)에 더해, C++처럼 **인스턴스 메서드**(비가상)도 지원한다.

**예: Foo와 Bar**
- Foo와 Bar가 각각 다음을 정의한다: `virtual void f()`, `instance void g()`, `static void h()`, `specialname void .ctor()`. Bar는 Foo를 상속한다.
- **논문의 오기**: 본문은 "instance method f, virtual method g"라고 썼지만, 코드에서는 f가 virtual, g가 instance이다. 강의는 **코드를 따른다**.
- 생성자는 늘 `.ctor`라는 이름이고 `specialname`을 붙인다.

**7.1 인스턴스 생성**
- `newobj c`는 생성자 c의 클래스 인스턴스를 할당하고 필드를 초기화한 뒤, 새 인스턴스와 인수로 생성자를 호출한다. 할당과 초기화가 명령어 하나이다.
```
.locals (class Foo f, class Foo b)
newobj void Foo::.ctor(); stloc f
newobj void Bar::.ctor(); stloc b
```
- JVM은 늘 `new c; dup; invokespecial c.<init>()V` 순서를 써야 한다.
  - 그래서 검증기가 복잡한 데이터 흐름 분석으로 다음을 확인해야 한다 [19, 4.9.4]: 초기화 전에 객체를 쓰지 않는지, 두 번 초기화하지 않는지.

### 8절 (메서드 호출)
**호출 명령어**
- 직접 호출 명령어가 2개 있다. 세 번째인 `calli`는 함수 포인터로 간접 호출한다.
- `call m`: 보통 정적 메서드 호출이며 JVM의 invokestatic에 해당한다. 예: `call void Foo::h()`
- `call instance`로 가상 또는 인스턴스 메서드를 부르면 정적으로 조회한다(early bound, JVM의 invokespecial과 비슷).
  - 예: `ldloc bar; call instance void Foo::f()` → bar가 Bar 인스턴스여도 **Foo::f()**를 실행한다.
  - instance 호출 규약은 추가 "this" 매개변수를 뜻한다.
- `callvirt m`: 가상 메서드를 late bound로 호출하며, 실제 메서드는 this의 동적 타입이 정한다.
  - JVM은 invokevirtual과 invokeinterface 두 명령어로 나뉜다.
  - 예: `ldloc bar; callvirt void Foo::f()` → **Bar::f()**를 실행한다(정적 타입 Foo, 동적 타입 Bar).
- 인스턴스 메서드에 callvirt를 쓰면 여전히 early bound 호출이다.

**8.1 Tailcalls**
- 재귀가 유일한 반복 수단인 언어가 있다: Haskell, Scheme, Mercury.
- `tail.` 접두사는 JIT에게 호출 전에 호출자의 스택 프레임을 버리라고 지시한다.
- 예: 다음 메서드는 스택 오버플로 예외 없이 영원히 돈다.
  ```
  .method public static void Bottom() {
    .maxstack 8
    tail. call void Bottom(); ret
  }
  ```
- 신뢰하지 않는 코드에서 신뢰하는 코드를 부를 때는 보안 때문에 프레임을 완전히 버릴 수 없다.
- JVM은 tailcall을 지원하지 않아 trampoline 같은 편법을 써야 한다 [5, 27, 15, 18].

### 9절 (값 타입과 참조 타입의 상호작용)
- 값 타입을 참조 타입 자리에 쓰고 싶은 경우가 있다. 예: Point를 컬렉션에 넣기.
- 동적 언어(Scheme)와 정적 다형 함수형 언어(Haskell, SML)에도 같은 문제가 있다. 다형 함수가 인수의 표현이 균일하기를 기대하기 때문이다.
- 값 타입을 넘길 때마다 클래스 인스턴스를 만들면 성능 부담이 크고, 값 타입마다 새 클래스를 정의하거나 불필요한 형변환을 많이 넣어야 한다.
- CLR은 boxing과 unboxing을 기본으로 지원한다: `box T`로 값 타입 T를 object로, `unbox T`로 되돌린다.

### 10절 (그 밖의 특수 기능)
- 다중 언어에 초점을 두었기 때문에 다른 방법으로는 합성하기 어려운 특수 기능을 제공한다. tail call 외에 다음이 있다.

**함수 포인터와 dispatch**
- 임의 dispatch 방식을 쓰는 OO 언어를 구현하려면 함수 포인터를 값으로 다룰 수 있어야 한다.
- 단일 구현 상속 + 다중 인터페이스 구현의 가상 dispatch는 기본으로 들어 있다. 나머지 경우는 디스패치 테이블을 명시적으로 만들어야 한다.
- `ldftn`은 함수 포인터를 push하고, `calli`는 스택 맨 위의 함수 포인터를 호출한다.
- `jmp`는 메서드 참조를 받아 그 메서드의 진입점으로 제어를 옮긴다.
  - 다중 상속에서 가상 메서드를 dispatch할 때 "this 조정"을 하는 trampoline stub을 만드는 데 쓴다.

**localloc**
- conformant array를 값으로 넘기는 언어는 호출 때 배열 복사본의 공간이 필요하다.
- `localloc`은 현재 활성 레코드를 늘린다. C의 alloca와 같은 의미이다.
- JVM처럼 힙에 동적으로 할당하는 것보다 훨씬 낫다.

**ldtoken**
- 명령어 인수에 있는 타입 참조의 런타임 타입 핸들을 push하며, reflection의 기본 구성 요소이다.
- 타입 참조는 알지만 그 타입의 인스턴스가 없을 때 쓴다.
- JVM에서는 `Class.forName()`으로 같은 기능을 얻지만, 이름을 **실행 시점에** 묶는다.

### 11절 (검증된 코드와 검증되지 않은 코드)
**검증의 범위와 시점**
- 메모리 안전이 중요한 경우를 위해, 기본 연산의 풍부한 부분집합을 안전성을 검증할 수 있는 방식으로 쓸 수 있다.
- JVM처럼 분석은 보수적이지만, 특정 종류의 런타임 오류가 없다는 강한 보장을 준다.
- 검증은 컴포넌트를 **배포할 때나 로드할 때** 하며, 만든 사람에 대한 신뢰에 기대지 않는다.

**검증이 주는 보장**
- 엄격한 정적 타입 언어가 주는 보장과 비슷하다.
  - 객체 참조를 담는 위치는 정적으로 선언한 타입의 계약을 만족하는 객체만 가리킨다.
  - 필드 선택은 알려진 타입에 유효한 필드만 접근한다.
- 정적으로 검증할 수 없는 경우에는 런타임 검사로 보호되는지 확인한다.
  - 예: 배열 인덱스는 경계 검사로 보호되어야 한다.
  - 축소 형변환이 성공해야만 가능한 필드나 메서드 접근도 같은 원리를 따른다.

**제어 흐름의 형식 검사**
- 제어 흐름이 합류하는 지점에서는 모든 경로의 평가 스택이 **높이가 같고 내용의 타입이 호환**되어야 한다.
- 객체 참조라면, 합류 지점에 들어오는 타입 상한들의 **최소 공통 조상**이 그 스택 원소의 정적 타입 상한이 된다.

**검증 가능한 코드를 만드는 조건**
- block copy처럼 본질적으로 검증할 수 없는 명령어가 있다.
- add처럼 평소에는 괜찮아도 주소 산술에 쓰면 검증할 수 없는 경우가 있다.
- 타입 안전하지 않은 대입과 판별자 없는 공용체의 일부 사용을 피해야 한다.
- 각주 3: 참조를 다른 타입과 겹치지 않는 한 검증기가 허용하는 공용체도 있다.

**reference surrogate**
- 정적 타입 안전 언어는 늘 검증 가능한 CIL로 컴파일할 수 있다. 데이터 타입 대응에는 창의성이 필요할 수 있다.
- 예: 정적으로 크기가 정해진 값 배열
  - 검증하지 않는 문맥: 필요한 크기의 value class를 선언하고 주소 산술로 원소에 접근한다.
  - 하지만 검증기는 주소 산술을 허용하지 않고 명시적 경계 검사를 모두 알아보지 못한다.
  - 대안: 같은 크기의 참조 배열을 할당해 CLI 내장 배열 지원을 쓴다. 값 객체를 참조 타입으로 표현하는 이 관용구를 **reference surrogate**라 부른다 [10].

**정리**
- CLR 혁신의 대부분은 검증된 환경에서도 유지된다. 값 클래스, 참조 매개변수, 타입 안전한 공용체를 모두 허용한다.

**peverify**
- 오프라인 검증기 `peverify`는 CIL 생성기에서 흔한 오류 대부분을 찾아 진단한다.
- Project 7 컴파일러 중 하나인 Gardens Point Component Pascal은, peverify가 CIL을 검증 가능하다고 확인하자 **첫 시도에** 자기 자신을 부트스트랩했다.
- 추출본에는 "Gardent Point"로 적혀 있다. 강의에서는 Gardens Point로 쓴다.

### 12절 (결론)
- 저자들은 CLI가 이미 다중 언어 플랫폼으로서 **JVM보다 엄밀히 더 강력하다**고 주장했다.
- MSR과 .NET 제품 그룹이 언어 구현자들과 계속 협력한다.
- 저자들은 언어 구현자들(지금 JVM을 대상으로 하는 사람 포함)에게 CLI를 대상으로 삼아 의견을 달라고 요청한다.

### 해석 시 주의 (강의에 "해석"으로만 쓴다)
- 이 논문은 실험이나 수치 비교가 없는 **설명·주장 논문**이다. "더 낫다"는 저자의 주장이다. 강의에서는 "논문은 ~라고 주장한다", "~로 해석할 수 있다"로 쓴다.
- 저자들은 Microsoft와 CLR 컴파일러 저자(Gough는 Component Pascal 컴파일러와 [10]의 저자)이다. 이해관계가 있는 비교라는 점을 한계 쪽에서 언급할 수 있다.
- 논문의 JVM 설명은 2001년 JVM 명세 2판 기준이다. 이후 바뀐 점은 8단원에서 C 담당이 확인한 사실만 쓴다(예: invokedynamic). 본문 단원(1~7)에서는 "당시 JVM"이라고 쓴다.

## 선행 연구와 배경 (논문 참고문헌에서 확인한 것만)
- [6] M. E. Conway, "Proposal for an UNCOL", CACM 1(10), 1958.
- [23] P. A. Nelson, "A Comparison of PASCAL Intermediate Languages", SIGPLAN Notices 14(8), 1979. UCSD P-code 관련.
- [20] S. Macrakis, "From UNCOL to ANDF", OSF RI, 1993.
- [25] AS/400 시스템 개요, IBM Systems Journal 1999.
- [19] Lindholm & Yellin, The Java Virtual Machine Specification (2e), 1999.
- [12] Gough & Corney, "Evaluating the JVM as a Target for Languages other than Java", JMLC 2000.
- [9] Gough, "Parameter Passing for the Java Virtual Machine", 1998.
- [5] Bothner, "Kawa — Compiling Dynamic Languages to the Java VM", USENIX 1998. Scheme을 JVM에 올린 예이다.
- [18] League, Shao, Trifonov, ICFP 1999. [24] Odersky & Wadler, "Pizza into Java", POPL 1997(제네릭).
- [8] Gordon & Syme, "Typing a Multi-Language Intermediate Code", POPL 2001.
- [16] Kennedy & Syme, "Design and Implementation of Generics for the .NET Common Language Runtime", PLDI 2001.
- [10] Gough, Compiling for the .NET Common Language Runtime, Prentice-Hall 2001.
- [2] ECMA TG3, CLI Partition II: Metadata, 2001.
- 1~2단원의 일반 배경(스택 머신, JIT, GC)은 교과서 수준의 일반 지식으로 설명하고, 출처 링크가 필요하면 C 담당이 확인한 아래 링크만 쓴다.

## 이후 동향 (8단원): C 담당이 WebFetch로 1차 출처를 확인한 뒤 이 아래에 추가하고 쓴다. 확인 못 한 항목은 쓰지 않는다.
후보(확인 필요):
- ECMA-335 표준(2001년 12월 초판)과 ISO/IEC 23271: https://ecma-international.org/publications-and-standards/standards/ecma-335/
- .NET 2.0(2005)의 제네릭: Kennedy & Syme PLDI 2001 설계가 CLR에 들어감. https://www.microsoft.com/en-us/research/publication/design-and-implementation-of-generics-for-the-net-common-language-runtime/
- Mono(오픈 소스 CLI 구현)
- .NET Core 오픈 소스화(2014)와 크로스 플랫폼: https://github.com/dotnet/runtime
- C# 7.2 이후의 `Span<T>`와 ref struct, ref return/ref local: managed pointer(`T&`)를 언어에 드러냄
- NativeAOT: 런타임 JIT 대신 AOT 컴파일
- JVM 쪽 변화
  - Java 7의 invokedynamic(JSR 292, 동적 언어 지원)
  - Project Valhalla(값 타입, 진행 중)
  - Math.addExact(오버플로 감지 라이브러리)
  - JVM 메서드 코드 길이 65535바이트 제한이 아직 남아 있는지
- WebAssembly
  - 다중 언어 바이트코드의 최근 예
  - tail call 제안의 표준 편입 여부
- F#(함수형 언어의 CLR 구현, tail. 접두사 사용)

### C 담당 확인 결과 (2026-11-26, WebFetch로 1차 출처 직접 확인)
아래만 8단원에 쓴다. "확인 못 함"으로 적은 항목은 쓰지 않는다.

**① 표준화와 오픈 소스**
- ECMA-335 "Common Language Infrastructure (CLI)": 1판 2001년 12월, 현재 6판 2012년 6월, ISO/IEC 번호 23271. 출처: https://ecma-international.org/publications-and-standards/standards/ecma-335/
- Mono: "Microsoft .NET Framework의 오픈 소스 구현", C#과 CLR의 ECMA 표준에 기반. Microsoft가 2016년 Xamarin 인수로 관리를 맡았고, 마지막 주요 릴리스는 2019년 7월. 상류 관리는 WineHQ로 넘어감. Microsoft는 dotnet/runtime 저장소에 Mono 런타임의 현대 포크를 유지. 출처: https://www.mono-project.com/
- .NET Core 오픈 소스 발표: 2014년 11월 12일(Immo Landwerth). "런타임과 프레임워크 라이브러리를 포함해 오픈 소스". 발표 당시에는 Windows에서만 빌드·실행 가능했고 크로스 플랫폼은 목표였음. 출처: https://devblogs.microsoft.com/dotnet/net-core-is-open-source/
- 현재 .NET: "free, cross-platform, open-source developer platform", 여러 언어 실행(C#이 가장 많이 쓰임), MIT 라이선스, .NET Foundation 프로젝트, Arm64·x64·x86. 구현 목록: .NET(Core), .NET Framework, Mono. 출처: https://learn.microsoft.com/en-us/dotnet/core/introduction , https://github.com/dotnet/runtime (MIT)

**② 제네릭**
- Kennedy & Syme, "Design and Implementation of Generics for the .NET Common Language Runtime", PLDI 2001. CLR에 매개변수 다형성(제네릭)을 직접 넣음. 값 타입·포인터 타입으로 인스턴스화, 정확한 런타임 타입. 구현은 JIT 시점 타입 특수화와 표현 기반 코드 공유. 출처: https://www.microsoft.com/en-us/research/publication/design-and-implementation-of-generics-for-the-net-common-language-runtime/
- C# 2.0(2005년 11월, Visual Studio 2005)에서 제네릭 도입. 출처: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history
- (.NET Framework 2.0이라는 판 이름은 위 페이지에서 직접 확인하지 못함 → "C# 2.0(2005)"으로만 쓴다.)

**③ managed pointer가 언어로: ref, Span<T>**
- C# 7.0(2017년 3월): ref locals, ref returns. C# 7.2(2017년 11월): `ref struct`("관리 메모리에 직접 접근하며 늘 스택에 할당"), `in` 매개변수, `ref readonly` 반환. C# 11(2022년 11월): ref 필드와 `scoped ref`. 출처: C# 버전 기록(위 링크)
- `Span<T>`: "임의 메모리의 연속 구간을 타입 안전·메모리 안전하게 나타내는 타입". ref struct이므로 boxing, object·인터페이스 변수에 대입, 참조 타입의 필드, await·yield 경계 넘기가 금지됨. 관리 메모리·네이티브 메모리·스택 메모리를 모두 가리킬 수 있음. 적용 버전 목록은 .NET Core 2.1, .NET Standard 2.1부터. 출처: https://learn.microsoft.com/en-us/dotnet/api/system.span-1

**④ JIT 대 AOT**
- Native AOT: 게시 시점에 IL을 네이티브 코드로 AOT 컴파일. 실행 때 JIT를 쓰지 않음, 시작이 빠르고 메모리 사용이 작음, JIT가 금지된 환경에서도 실행. 특정 런타임 환경(예: Linux x64)을 대상으로 함. ".NET 7 이후". 한계: 동적 로딩 불가(Assembly.LoadFile), 런타임 코드 생성 불가(System.Reflection.Emit), trimming 필요, 구조체 인자 제네릭은 인스턴스마다 코드를 미리 생성해 디스크 크기가 커질 수 있음. 출처: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/

**⑤ JVM 쪽의 응답**
- JSR 292 "Supporting Dynamically Typed Languages on the Java Platform": 새 바이트코드 명령어 invokedynamic, Java SE 7, Final(Final Release 2011년 7월 20일). 출처: https://jcp.org/en/jsr/detail?id=292
- `Math.addExact(int, int)`: 결과가 int를 넘치면 ArithmeticException. @since 1.8(Java 8). 출처: https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html
- JVM 명세 SE 21 §4.7.3: "code_length의 값은 0보다 크고 65536보다 작아야 한다." → 메서드 코드 길이 64K 제한은 지금도 남아 있다. 출처: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.3
- JEP 401 "Value Objects (Preview)": Status Integrated, Release 28, 미리보기(preview) 언어·VM 기능. 요약: 불변이고 객체 정체성이 없는 value object를 도입, 필드 값으로만 구별, JVM이 성능에 유리하게 표현할 수 있음. 비목표: C·C#식 struct 도입이 아님. 출처: https://openjdk.org/jeps/401 (WebFetch는 403으로 막혀 curl로 같은 URL 원문을 직접 받아 확인)
- (jsr/ret 금지 여부는 확인하지 못함 → 쓰지 않는다. Valhalla 프로젝트 페이지는 403 → JEP 401만 쓴다.)

**⑥ WebAssembly**
- 정의: "WebAssembly(Wasm)는 스택 기반 가상 머신을 위한 이진 명령어 형식", "프로그래밍 언어를 위한 이식 가능한 컴파일 대상". 출처: https://webassembly.org/
- Tail call 제안: 완료된 제안(phase 4) 목록에 있음, core 명세, 명세 버전 3.0, WG 2024-07-10. Garbage collection도 같은 표에 3.0, 2024-07-10. 출처: https://github.com/WebAssembly/proposals/blob/main/finished-proposals.md

**⑦ F#**
- F#: "universal programming language", "open-source, cross-platform and interoperable". 출처: https://learn.microsoft.com/en-us/dotnet/fsharp/what-is-fsharp
- F# 컴파일러 옵션 `--tailcalls[+|-]`: "tail IL 명령어의 사용을 켜거나 끄며, 꼬리 재귀 함수의 스택 프레임을 재사용하게 함. 기본으로 켜져 있음." 출처: https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-options
