# 강의 용어표: 공통 언어 런타임(CLR)의 기술 개요 (Meijer & Gough 2001)

모든 모듈은 이 표의 표기만 쓴다. 원어 우선 규칙(SKILL.md "용어 표기"): 국내 개발자가 영어로 말하는 개념어·명령어 이름은 원어를 본문 표기로 쓰고 첫 등장에만 한글 뜻을 괄호로 단다. 모듈마다 첫 등장에서 다시 병기하고 툴팁을 단다. **CIL 명령어 이름(ldarg, callvirt, tail. 등)과 지시어(.locals, .maxstack)는 번역하지 않고 `<code>`로 쓴다.**

| English | 한국어 표기 | 첫 등장 표기 | 처음 나오는 모듈 | 비고 |
|---|---|---|---|---|
| Common Language Infrastructure | CLI | 공통 언어 기반(Common Language Infrastructure, CLI) | 1 | 표준 명세의 이름. 이후 `CLI` |
| Common Language Runtime | CLR | 공통 언어 런타임(Common Language Runtime, CLR) | 1 | Microsoft의 CLI 구현. 이후 `CLR`. 논문은 둘을 섞어 쓰므로 본문에서 "명세 = CLI, Microsoft 구현 = CLR"로 한 번 밝힌다 |
| Common Intermediate Language | CIL | 공통 중간 언어(Common Intermediate Language, CIL) | 1 | 이후 `CIL`. MSIL·IL이라고도 부른다는 점을 툴팁에 |
| Java Virtual Machine | JVM | 자바 가상 머신(Java Virtual Machine, JVM) | 1 | 이후 `JVM` |
| bytecode | 바이트코드 | 바이트코드(Bytecode) | 1 | JVM의 중간 코드 |
| virtual machine | 가상 머신 | 가상 머신(Virtual Machine, VM) | 1 | |
| intermediate language | 중간 언어 | 중간 언어(Intermediate Language) | 1 | |
| native code | 네이티브 코드 | 네이티브 코드(Native Code, 특정 CPU의 기계어) | 1 | |
| just-in-time compiler | JIT | JIT(Just-In-Time) 컴파일러(실행 직전에 기계어로 번역) | 1 | 이후 `JIT` |
| interpreter | 인터프리터 | 인터프리터(Interpreter) | 1 | |
| compiler / front end / back end | 컴파일러 | 컴파일러(Compiler) | 1 | |
| portability | 이식성 | 이식성(Portability) | 1 | |
| interoperability | 상호 운용성 | 상호 운용성(Interoperability) | 1 | |
| metadata | 메타데이터 | 메타데이터(Metadata) | 1 | |
| reflection | reflection | reflection(실행 중에 타입 정보를 조회·사용) | 1 | 원어 우선 |
| garbage collection | 가비지 컬렉션 | 가비지 컬렉션(Garbage Collection, GC) | 1 | 이후 `GC`. 힙은 `GC 힙` |
| heap | 힙 | 힙(Heap) | 1 | |
| managed code | managed code | managed code(CLR이 관리하는 코드) | 3 | 원어 우선 |
| type safety | 타입 안전성 | 타입 안전성(Type Safety) | 1 | "타입 안전한" |
| UNCOL | UNCOL | UNCOL(Universal Computer Oriented Language) | 2 | 고유 명칭 |
| P-code | P-code | P-code(UCSD Pascal의 중간 코드) | 2 | 고유 명칭 |
| ANDF | ANDF | ANDF(Architecture Neutral Distribution Format) | 2 | 고유 명칭 |
| trampoline | trampoline | trampoline(꼬리 호출이 없을 때 반복문으로 호출을 대신 돌려주는 기법) | 2 | 원어 우선 |
| boxing / unboxing | boxing / unboxing | boxing(값을 객체로 감싸기), unboxing(객체에서 값을 꺼내기) | 2 | 원어 우선. 명령어는 `box`, `unbox` |
| thread | 스레드 | 스레드(Thread) | 3 | |
| activation record / stack frame | 활성 레코드 | 활성 레코드(Activation Record, 스택 프레임) | 3 | |
| evaluation stack | 평가 스택 | 평가 스택(Evaluation Stack) | 3 | JVM 용어는 operand stack(피연산자 스택) |
| stack machine | 스택 머신 | 스택 머신(Stack Machine) | 1 | |
| instruction pointer | 명령어 포인터 | 명령어 포인터(Instruction Pointer, IP) | 3 | |
| local variable / argument | 지역 변수 / 인수 | 지역 변수(Local Variable), 인수(Argument) | 3 | parameter는 `매개변수` |
| method | 메서드 | 메서드(Method) | 1 | |
| signature | 시그니처 | 시그니처(Signature) | 3 | |
| exception handler | 예외 처리기 | 예외 처리기(Exception Handler) | 3 | |
| dynamic link | 동적 링크 | 동적 링크(Dynamic Link, 호출한 쪽 프레임으로 돌아갈 연결) | 3 | |
| security descriptor | 보안 기술자 | 보안 기술자(Security Descriptor) | 3 | |
| assembly | 어셈블리 | 어셈블리(Assembly) | 3 | .NET의 배포 단위. 어셈블리어와 혼동 주의를 툴팁에 |
| module | 모듈 | 모듈(Module, 어셈블리를 이루는 파일) | 3 | 강의 단원은 `단원`으로만 부른다 |
| manifest | 매니페스트 | 매니페스트(Manifest) | 3 | |
| JAR | JAR | JAR(Java Archive) | 3 | |
| custom attribute | custom attribute | custom attribute(사용자 정의 특성) | 3 | 원어 우선 |
| digital signature / public key | 디지털 서명 / 공개 키 | 디지털 서명(Digital Signature), 공개 키(Public Key) | 3 | |
| application domain | 응용 프로그램 도메인 | 응용 프로그램 도메인(Application Domain) | 3 | |
| ILASM | ILASM | ILASM(CIL 어셈블러 문법) | 3 | |
| primitive type | 기본 타입 | 기본 타입(Primitive Type) | 4 | |
| type constructor | 타입 생성자 | 타입 생성자(Type Constructor, 타입을 조합해 새 타입을 만드는 규칙) | 4 | 객체 생성자(constructor)와 구별 |
| natural-size type | 자연 크기 타입 | 자연 크기 타입(Natural-Size Type) | 4 | `native int` 등 |
| two's complement | 2의 보수 | 2의 보수(Two's Complement) | 4 | |
| managed pointer | managed pointer | managed pointer(관리 포인터, `T&`) | 4 | 원어 우선 |
| unmanaged pointer | unmanaged pointer | unmanaged pointer(비관리 포인터, `T*`) | 4 | 원어 우선 |
| object reference | 객체 참조 | 객체 참조(Object Reference) | 4 | |
| pinned | pinned | pinned(GC가 옮기지 못하게 고정) | 4 | |
| typed reference | typed reference | typed reference(포인터와 타입을 묶은 값) | 4 | |
| varargs | 가변 인수 | 가변 인수(Varargs) | 2 | |
| polymorphic instruction | 다형 명령어 | 다형 명령어(피연산자 타입에 따라 동작이 정해지는 명령어) | 4 | |
| load / store | load / store | load(스택에 올리기), store(스택에서 꺼내 저장) | 4 | |
| dereference | 역참조 | 역참조(Dereference) | 4 | |
| pass by reference | 참조 전달 | 참조 전달(Pass by Reference) | 2 | byref |
| overflow | 오버플로 | 오버플로(Overflow) | 2 | |
| branch | 분기 | 분기(Branch) | 4 | |
| subroutine | 서브루틴 | 서브루틴(Subroutine) | 4 | JVM `jsr` |
| value type | 값 타입 | 값 타입(Value Type) | 2 | |
| reference type | 참조 타입 | 참조 타입(Reference Type) | 2 | |
| struct / record | 구조체 / 레코드 | 구조체(Struct) | 5 | |
| union / variant record | 공용체 | 공용체(Union, 필드가 같은 메모리를 겹쳐 쓰는 타입) | 2 | |
| enumeration | 열거형 | 열거형(Enum) | 5 | |
| class / interface / delegate | 클래스 / 인터페이스 / 대리자 | 클래스(Class), 인터페이스(Interface), 대리자(Delegate, 메서드를 가리키는 타입 안전 객체) | 5 | |
| constructor | 생성자 | 생성자(Constructor, `.ctor`) | 5 | |
| field | 필드 | 필드(Field) | 5 | |
| static / instance / virtual method | 정적 / 인스턴스 / 가상 메서드 | 정적 메서드(Static Method), 인스턴스 메서드(Instance Method), 가상 메서드(Virtual Method) | 5 | |
| static type / dynamic type | 정적 타입 / 동적 타입 | 정적 타입(Static Type, 선언된 타입), 동적 타입(Dynamic Type, 실제 객체의 타입) | 6 | |
| early binding / late binding | early binding / late binding | early binding(컴파일 때 호출 대상 결정), late binding(실행 때 호출 대상 결정) | 6 | 원어 우선 |
| dispatch / dispatch table | dispatch / 디스패치 테이블 | dispatch(호출할 메서드 고르기), 디스패치 테이블(Dispatch Table) | 6 | |
| tail call | tail call | tail call(꼬리 호출, 함수의 마지막 동작인 호출) | 2 | 원어 우선. 명령어 접두사는 `tail.` |
| stack overflow | 스택 오버플로 | 스택 오버플로(Stack Overflow) | 2 | |
| function pointer | 함수 포인터 | 함수 포인터(Function Pointer) | 2 | |
| multiple inheritance | 다중 상속 | 다중 상속(Multiple Inheritance) | 6 | |
| conformant array | conformant array | conformant array(크기를 호출 때 정하는 배열 매개변수) | 6 | 원어 우선 |
| closure | 클로저 | 클로저(Closure) | 2 | |
| generics | 제네릭 | 제네릭(Generics) | 2 | |
| verification / verifier | 검증 / 검증기 | 검증(Verification), 검증기(Verifier) | 7 | |
| verifiable code | 검증 가능한 코드 | 검증 가능한 코드(Verifiable Code) | 7 | |
| control flow / merge point | 제어 흐름 / 합류 지점 | 제어 흐름(Control Flow), 합류 지점(Merge Point) | 7 | |
| least common ancestor | 최소 공통 조상 | 최소 공통 조상(Least Common Ancestor) | 7 | |
| bounds check | 범위 검사 | 범위 검사(Bounds Check) | 7 | |
| narrowing cast | 축소 형변환 | 축소 형변환(Narrowing Cast, 상위 타입을 하위 타입으로 바꾸기) | 7 | |
| reference surrogate | reference surrogate | reference surrogate(값을 대신하는 참조 객체) | 7 | 원어 우선, 논문 용어 |
| dataflow analysis | 데이터 흐름 분석 | 데이터 흐름 분석(Dataflow Analysis) | 5 | |
| bootstrap | 부트스트랩 | 부트스트랩(Bootstrap, 컴파일러가 자기 자신을 컴파일) | 7 | |
| ECMA standard | ECMA 표준 | ECMA 표준(ECMA-335) | 1 | |
| baseline | 기준선 | 기준선(Baseline) | - | 사용자 지정. "기준 방법"으로 바꾸지 않음 |
| ahead-of-time compilation | AOT 컴파일 | AOT(Ahead-Of-Time) 컴파일(실행 전에 미리 기계어로 번역) | 8 | |
| WebAssembly | WebAssembly | WebAssembly(Wasm, 웹 브라우저용 이식 가능한 바이트코드) | 8 | 고유 명칭 |
| ref struct / Span&lt;T&gt; | `ref struct` / `Span<T>` | `Span<T>`(연속 메모리 구간을 가리키는 ref struct) | 8 | 고유 명칭(C 보고로 추가) |
| Native AOT | Native AOT | Native AOT(미리 네이티브 코드로 컴파일해 JIT 없이 실행) | 8 | 고유 명칭 |
| trimming | trimming | trimming(쓰지 않는 코드를 빌드에서 잘라 냄) | 8 | 원어 우선 |
| value object | value object | value object(Valhalla의 식별자 없는 객체) | 8 | 원어 우선 |
| invokedynamic | `invokedynamic` | `invokedynamic`(호출 대상을 실행 중에 연결하는 JVM 명령어) | 8 | 명령어 이름 |
| polytypic | polytypic | polytypic(여러 타입에 같은 방식으로 동작하는) | 5 | 원어 우선, 논문 용어(B 보고로 추가) |
| IEEE-754 | IEEE-754 | IEEE-754(부동소수점 표준) | 4 | 고유 명칭 |
| machine code | 기계어 | 기계어(Machine Code) | 1 | A 보고로 추가 |
| metaprogramming | 메타프로그래밍 | 메타프로그래밍(Metaprogramming) | 1 | |
| serialization | 직렬화 | 직렬화(Serialization) | 1 | |
| unmanaged code | unmanaged code | unmanaged code(CLR이 관리하지 않는 네이티브 코드) | 1 | 원어 우선 |
| register machine | 레지스터 머신 | 레지스터 머신(Register Machine) | 1 | |
| local memory pool | 지역 메모리 풀 | 지역 메모리 풀(Local Memory Pool) | 3 | |
| tagged pointer | tagged pointer | tagged pointer(하위 비트에 표지를 담은 포인터) | 2 | 원어 우선 |
| multi-dimensional array | 다차원 배열 | 다차원 배열(Multi-Dimensional Array) | 2 | |
| annotation | annotation | annotation(Java의 메타데이터 표기) | 3 | 원어 우선 |
