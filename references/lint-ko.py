#!/usr/bin/env python3
"""lint-ko.py - 한국어 코스 HTML 린터 (표준 라이브러리만 사용)

사용법:
  python3 lint-ko.py <코스 디렉터리 | HTML 파일> [--strict] [--json]

종료 코드: ERROR가 있으면 1 (--strict 이면 WARN도 1), 아니면 0.
디렉터리를 주면 *.html 을 모두 검사한다(modules/ 가 함께 있으면 빌드 산출물 index.html 은 중복이라 제외).
작업 폴더(_tmp/, _src/ 처럼 밑줄로 시작하는 폴더)와 vendor/ 안의 파일은 강의 본문이 아니므로 건너뛴다.
<script>, <style>, <code>, <pre>, KaTeX 렌더 결과(class="katex"), $...$ / $$...$$ 수식은 본문 검사에서 제외한다.
이모지(KO113)는 본문·속성·그림·코드 어디에도 쓰지 않는다(ERROR).
EBS 문체(KO102/108/109)는 chat/dialogue/message/bubble 클래스 요소와 lang이 ko가 아닌 요소 안에서는 검사하지 않는다.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_TAGS = {"script", "style", "code", "pre"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}

HANJA_RE = re.compile(r"[一-鿿㐀-䶿]+")
FULLWIDTH = {
    "（": "(", "）": ")", "，": ",", "：": ":", "；": ";",
    "！": "!", "？": "?", "。": ".", "、": ",", "「": "'", "」": "'",
}
FULLWIDTH_RE = re.compile("[" + "".join(FULLWIDTH) + "]")

# (정규식, 설명, 제안)
TRANSLATIONESE = [
    (r"에\s*의[해하]서?|에\s*의한", "'~에 의해' 번역투(영어 수동태 'by')", "능동문으로 바꾸거나 '~이/가', '~(으)로'를 쓰세요"),
    (r"[을를]\s*(?:가지고\s*있|가지는)", "'~을 가지고 있다/가지는' 번역투(have)", "'~이 있다', '~한', '~을 갖는' 등으로 바꾸세요"),
    (r"에\s*있어서", "'~에 있어서' 번역투(in/at)", "'~에서', '~할 때', '~의 경우'로 바꾸세요"),
    (r"되어\s*(?:지|진|집)", "이중 피동 '되어지다'", "'되다'만 쓰세요 (예: 사용되어진다 -> 사용된다)"),
    (r"에\s*대해서는?", "'~에 대해(서)' 번역투(about/on)", "'~을/를', '~의', '~에 관한'으로 바꿔 보세요"),
    (r"로부터", "'~로부터' 번역투(from)", "'~에서', '~에게서'로 바꾸세요"),
    (r"하는\s*것이\s*가능하", "'~하는 것이 가능하다' 번역투(it is possible to)", "'~할 수 있다'로 줄이세요"),
    (r"할\s*수\s*있을\s*것이다", "'~할 수 있을 것이다' 불필요한 추측 표현", "'~할 수 있다'로 단정하세요"),
    (r"[가-힣]+적인\s+[가-힣]*적인", "'~적인 ~적인' 연속 사용", "하나는 풀어 쓰세요 (예: 효율적인 -> 효율이 높은)"),
    (r"[가-힣]+들의\s+[가-힣]+들", "이중 복수 '~들의 ~들'", "한쪽 '들'을 빼세요"),
    (r"그것(?:은|이)", "'그것은/그것이' 영어 대명사 직역(it)", "주어를 생략하거나 구체적인 명사로 바꾸세요"),
]
TRANSLATIONESE = [(re.compile(p), d, s) for p, d, s in TRANSLATIONESE]
TONGHAE_RE = re.compile(r"[을를]\s*통해")
TONGHAE_MAX = 3

# EBS 교재 문체: 본문은 한다체. 합니다체/해요체 종결을 잡는다.
# (?!아): "아니다"(한다체 부정)는 합니다체가 아니다 — C1 E2E 테스트에서 오탐 확인
FORMAL_RE = re.compile(r"(?:(?!아)[가-힣]니다|십시오)(?=\s*[.!?]|\s*$)")
POLITE_RE = re.compile(r"(?:(?<![필중주수개긴소불])요|죠)(?=\s*[.!?])")
PRAISE_RE = re.compile(r"잘\s*했|훌륭|멋져|멋지|대단|축하|(?<=[가-힣])!(?=\s|$)")
MATH_RE = re.compile(r"\$\$.*?\$\$|\$(?=\S)[^$\n]*?(?<=\S)\$(?!\d)", re.S)
YEOREOBUN_RE = re.compile(r"여러분")
OPERATOR_RE = re.compile(r"\\(cos|sin|tan|max|min|arg|argmax|log|exp|lim|det)(?![A-Za-z])")
CHAT_WORDS = ("chat", "dialogue", "message", "bubble")
PROSE_TAGS = {"p", "li", "td", "th"}
PROSE_CLASS_PARTS = ("callout", "card", "quiz-question")
PAREN_SPACE_RE = re.compile(r"([가-힣])\s+\((?=[A-Za-z])")
SENT_END_RE = re.compile(r"[다요죠][.!?]")
COUNTERS = "개|분|초|시간|단계|장|절|번|명|배|차례|가지|권|편"
NUMUNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)[ \t]+(" + COUNTERS + r")"
    r"(?=(?:으로|에서|이나|정도|마다|짜리|은|는|이|가|을|를|의|에|만|씩|째|간|로|도|과|와|나|쯤)?(?![가-힣]))")

# 영어 알파벳 읽기 기준 받침: L 엘, M 엠, N 엔, R 알
LETTER_BATCHIM = {"L": "ㄹ", "M": "ㅁ", "N": "ㄴ", "R": "ㄹ"}
DIGIT_BATCHIM = {"0": "ㅇ", "1": "ㄹ", "2": None, "3": "ㅁ", "4": None,
                 "5": None, "6": "ㄱ", "7": "ㄹ", "8": "ㄹ", "9": None}
PARTICLE_PAIRS = {  # 받침 있을 때 / 없을 때
    "은": ("은", "는"), "는": ("은", "는"),
    "이": ("이", "가"), "가": ("이", "가"),
    "을": ("을", "를"), "를": ("을", "를"),
    "과": ("과", "와"), "와": ("과", "와"),
}
ACRO_RE = re.compile(
    r"(?<![A-Za-z0-9-])([A-Z][A-Z0-9-]*[A-Z0-9]|[A-Z]{2,})(으로|로|은|는|이|가|을|를|과|와)")
DIGIT_PARTICLE_RE = re.compile(r"(?<![\w.-])(\d+)(으로|로|은|는|이|가|을|를|과|와)(?![가-힣])")


def batchim_of(token):
    last = token[-1]
    if last.isdigit():
        return DIGIT_BATCHIM[last]
    return LETTER_BATCHIM.get(last)


def particle_fix(token, particle):
    """잘못된 조사면 올바른 조사를, 맞으면 None."""
    b = batchim_of(token)
    if particle in ("으로", "로"):
        right = "으로" if (b and b != "ㄹ") else "로"
    else:
        right = PARTICLE_PAIRS[particle][0 if b else 1]
    return None if right == particle else right


def blank_math(text):
    """수식을 같은 길이의 공백으로 치환(줄바꿈 보존해 위치 유지)."""
    def rep(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"\$\$.*?\$\$", rep, text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", rep, text, flags=re.S)
    text = re.sub(r"\$[^$\n]+?\$", rep, text)
    return text


class Linter(HTMLParser):
    def __init__(self, src, fname):
        super().__init__(convert_charrefs=True)
        self.fname = fname
        self.issues = []
        self.stack = []        # (tag, attrs)
        self.segs = []         # (text, line, lang_ok)
        self.p_blocks = []     # (text, line)
        self._p = None         # [parts, line]
        self.seen_html = False
        self.tonghae = []      # lines
        self.src = src

    # ---- 보고 ----
    def add(self, line, sev, rid, msg, fix):
        self.issues.append({"file": self.fname, "line": line, "severity": sev,
                            "id": rid, "message": msg, "fix": fix})

    # ---- 파서 콜백 ----
    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.seen_html = True
            lang = a.get("lang", "").strip().lower()
            if not lang.startswith("ko"):
                self.add(line, "ERROR", "KO001",
                         f'<html lang>가 없거나 "ko"로 시작하지 않습니다 (현재: {a.get("lang", "(없음)")!r})',
                         '<html lang="ko">로 지정하세요')
        if "data-steps" in a:
            try:
                json.loads(a["data-steps"])
            except Exception as e:
                self.add(line, "ERROR", "KO004", f"data-steps JSON 파싱 실패: {e}",
                         "작은따옴표 대신 큰따옴표, 끝의 쉼표 제거, 속성 내부 따옴표는 &quot; 로 이스케이프하세요")
        cls = a.get("class", "").split()
        if "term" in cls and "data-definition" in a:
            d = a["data-definition"]
            if not re.search(r"[가-힣]", d):
                self.add(line, "WARN", "KO107", "용어 정의(data-definition)에 한글이 없습니다",
                         "한국어 정의로 바꾸세요 (예: 정책 경사(Policy Gradient): ...)")
            if re.search(r"[（）]", d):
                self.add(line, "WARN", "KO107", "용어 정의에 전각 괄호가 있습니다",
                         "반각 괄호 ( )를 쓰세요")
            # KO111: 용어 뜻풀이는 사전식 명사형 종결(~것. ~함. ~임.)로 쓴다 (style-guide §1.8)
            body = d.split(":", 1)[1] if ":" in d else d
            m = re.search(r"[가-힣](?:이다|한다|된다|있다|없다|진다|는다|했다|였다|니다|어요|아요|예요|이에요)\.", body)
            if m:
                self.add(line, "WARN", "KO111", f"용어 뜻풀이가 서술문으로 끝납니다: '{m.group(0)}'",
                         "사전식 명사형 종결로 쓰세요 (예: '~하는 값.', '~을 나타냄.', '~인 함수.')")
            # 속성 값에도 한자/전각 문장부호 검사
            self.check_text(d, line, self.lang_ok_now(a), attr=True, ctx=self.ctx(a)[:2] + (True,))
        for k in ("data-explanation-right", "data-explanation-wrong"):
            if k in a:
                c = self.ctx(a)
                self.check_text(a[k], line, self.lang_ok_now(a), attr=True, ctx=c[:2] + (True,), feedback=True)
        if tag in VOID:
            return
        self.stack.append((tag, a))
        if tag == "p":
            self._p = [[], line]

    def handle_startendtag(self, tag, attrs):
        # <br/> 등: 스택에 올리지 않고 시작 처리만
        saved = len(self.stack)
        self.handle_starttag(tag, attrs)
        del self.stack[saved:]

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag == "p" and self._p:
            parts, line = self._p
            self.p_blocks.append(("".join(parts), line))
            self._p = None

    def skipping(self):
        for tag, a in self.stack:
            if tag in SKIP_TAGS or "katex" in a.get("class", "").split() \
                    or any(c.startswith("katex") for c in a.get("class", "").split()):
                return True
        return False

    def lang_ok_now(self, extra=None):
        items = list(self.stack[1:] if self.stack and self.stack[0][0] == "html" else self.stack)
        if extra:
            items.append(("", extra))
        for _, a in items:
            lg = a.get("lang", "").lower()
            if lg.startswith("zh") or lg.startswith("ja") or "hanja" in a.get("class", "").split():
                return True
        return False

    def ctx(self, extra=None):
        """(chat 안인가, ko 아닌 lang 안인가, 본문 요소 안인가)"""
        items = list(self.stack[1:] if self.stack and self.stack[0][0] == "html" else self.stack)
        if extra:
            items.append(("", extra))
        chat = other = prose = False
        for tag, a in items:
            cl = " ".join(a.get("class", "").split()).lower()
            if any(w in cl for w in CHAT_WORDS):
                chat = True
            lg = a.get("lang", "").lower()
            if lg and not lg.startswith("ko"):
                other = True
            if tag in PROSE_TAGS or any(x in cl for x in PROSE_CLASS_PARTS):
                prose = True
        return chat, other, prose

    def handle_data(self, data):
        if self.skipping() or not data.strip():
            return
        line = self.getpos()[0]
        if self._p is not None:
            self._p[0].append(data)
        self.check_text(data, line, self.lang_ok_now(), ctx=self.ctx())

    # ---- 본문 검사 ----
    def check_text(self, raw, line, lang_ok, attr=False, ctx=(False, False, False), feedback=False):
        text = blank_math(raw)

        def ln(m):
            return line + text.count("\n", 0, m.start())

        if not lang_ok:
            for m in HANJA_RE.finditer(text):
                self.add(ln(m), "ERROR", "KO002", f"한자/중국어 문자 '{m.group(0)}' 발견 (중국어 잔재 가능성)",
                         "한국어로 번역하세요. 의도한 한자 병기라면 <span class=\"hanja\"> 또는 lang=\"zh\"/\"ja\"로 감싸세요")
        for m in FULLWIDTH_RE.finditer(text):
            self.add(ln(m), "ERROR", "KO003", f"중국어식 전각 문장부호 '{m.group(0)}'",
                     f"반각 '{FULLWIDTH[m.group(0)]}' 로 바꾸세요")
        chat, other, prose = ctx
        if prose and not chat and not other:
            m = FORMAL_RE.search(text)
            if m:
                self.add(ln(m), "WARN", "KO102",
                         f"합니다체 종결 '{m.group(0)}': EBS 교재 본문은 한다체여야 합니다",
                         "한다체로 바꾸세요 (예: ~합니다 -> ~한다, ~입니다 -> ~이다, ~하십시오 -> ~하시오)")
            m = POLITE_RE.search(text)
            if m:
                self.add(ln(m), "WARN", "KO102",
                         f"해요체 종결 '{m.group(0)}': EBS 교재 본문은 한다체여야 합니다",
                         "한다체로 바꾸세요 (예: ~해요 -> ~한다, ~예요 -> ~이다). 대화(chat) 요소 안의 대사만 해요체 허용")
            m = YEOREOBUN_RE.search(text)
            if m:
                self.add(ln(m), "WARN", "KO109", "본문에서 '여러분'으로 독자를 직접 부릅니다",
                         "독자 호칭을 빼고 서술형으로 바꾸세요 (예: 여러분이 ~하면 -> ~하면)")
        if feedback and not chat and not other:
            m = PRAISE_RE.search(text)
            if m:
                self.add(ln(m), "WARN", "KO108", f"해설에 칭찬·감탄 표현 '{m.group(0)}'",
                         "정답/오답 표지와 한다체 해설(~이므로 ~이다.)만 쓰세요")
            # KO110: main.js가 '정답'/'오답' 표지를 자동으로 붙이므로 해설에 다시 쓰면 화면에 두 번 나온다
            m = re.match(r"\s*(정답|오답)(?![가-힣])\s*[.:!|]?", text)
            if m:
                self.add(ln(m), "WARN", "KO110", f"해설이 '{m.group(1)}' 표지로 시작합니다 (main.js가 표지를 자동으로 붙여 중복 표시됨)",
                         "표지를 빼고 쓰세요: 맞힌 경우 '② | ~이다.', 틀린 경우 '| 정답은 ②이다. ~이다.'")
        # KO112: 수식은 모두 이탤릭체 (\mathrm·\mathbf·\text·\operatorname 대신 \mathit·\boldsymbol)
        # 파싱된 본문·속성에서만 본다(script/style/pre/code/주석은 handle_data 단계에서 이미 제외).
        # 통화 기호($5, $10 등)를 수식으로 오인하지 않도록 여는 $ 뒤는 공백이 아니고, 닫는 $ 앞은 공백이 아니며 뒤에 숫자가 오지 않아야 한다
        for m in MATH_RE.finditer(raw):
            u = re.search(r"\\(mathrm|mathbf|text|textrm|operatorname|rm|bf)\b", m.group(0))
            if u:
                self.add(line + raw.count("\n", 0, m.start() + u.start()), "WARN", "KO112",
                         f"수식에 똑바른 글꼴 명령 '\\{u.group(1)}'이 있습니다 (수식은 모두 이탤릭체)",
                         "\\mathrm·\\text·\\operatorname → \\mathit, \\mathbf → \\boldsymbol")
            o = OPERATOR_RE.search(m.group(0))
            if o:
                self.add(line + raw.count("\n", 0, m.start() + o.start()), "WARN", "KO112",
                         f"수식에 이름 있는 연산자 '\\{o.group(1)}'이 있습니다 (KaTeX가 똑바른 글꼴로 그림, 수식은 모두 이탤릭체)",
                         "\\cos·\\max·\\log 등 -> \\mathit{cos}·\\mathit{max}·\\mathit{log} (\\sum·\\prod·\\int 기호는 그대로)")
        if attr:
            return
        for rx, desc, fix in TRANSLATIONESE:
            for m in rx.finditer(text):
                self.add(ln(m), "WARN", "KO101", f"번역투: {desc} -> '{m.group(0)}'", fix)
        for m in TONGHAE_RE.finditer(text):
            self.tonghae.append(ln(m))
        for m in PAREN_SPACE_RE.finditer(text):
            self.add(ln(m), "WARN", "KO103", "한글 용어와 영문 병기 괄호 사이에 공백이 있습니다",
                     "공백을 제거하세요 (예: 정책 경사(Policy Gradient))")
        for m in ACRO_RE.finditer(text):
            tok, par = m.group(1), m.group(2)
            fx = particle_fix(tok, par)
            if fx:
                self.add(ln(m), "WARN", "KO104", f"조사 불일치: '{tok}{par}' (읽는 발음 기준)",
                         f"올바른 표기: {tok}{fx}")
        for m in DIGIT_PARTICLE_RE.finditer(text):
            tok, par = m.group(1), m.group(2)
            fx = particle_fix(tok, par)
            if fx:
                self.add(ln(m), "WARN", "KO104", f"조사 불일치: '{tok}{par}' (읽는 발음 기준)",
                         f"올바른 표기: {tok}{fx}")
        for m in NUMUNIT_RE.finditer(text):
            self.add(ln(m), "WARN", "KO105", f"수 단위 띄어쓰기: '{m.group(1)} {m.group(2)}'",
                     f"붙여 쓰세요: '{m.group(1)}{m.group(2)}' (한글 맞춤법 제43항)")

    # ---- 종료 후 블록 검사 ----
    def finish(self):
        if len(self.tonghae) > TONGHAE_MAX:
            self.add(self.tonghae[0], "WARN", "KO101",
                     f"'~을 통해' 과다 사용 ({len(self.tonghae)}회, 기준 {TONGHAE_MAX}회 초과; 첫 위치)",
                     "'~(으)로', '~해서', '~하면' 등으로 일부를 바꾸세요")
        for text, line in self.p_blocks:
            t = blank_math(text)
            n = len(SENT_END_RE.findall(t))
            if n > 3:
                self.add(line, "WARN", "KO106", f"문단이 {n}문장입니다 (최대 3문장)",
                         "문단을 나누거나 핵심만 남기세요")


# KO113: 이모지 금지(그림 문자·딩뱃 체크 표시·변형 선택자, 문자 참조 &#128161; 포함). 표의 갖춤 표시는 ○·△·×
EMOJI_CHARS = r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]"
EMOJI_CHAR_RE = re.compile(EMOJI_CHARS)
# \uBB38\uC790 \uCC38\uC870\uB294 \uD480\uC5B4\uC11C \uAC19\uC740 \uBB38\uC790 \uC9D1\uD569\uC73C\uB85C \uD310\uC815\uD55C\uB2E4(&#12593; \u3131\u00B7&#12300; \u300C \uAC19\uC740 \uD55C\uAE00\u00B7CJK\uB294 \uD1B5\uACFC)
EMOJI_RE = re.compile(EMOJI_CHARS + r"|&#(\d{1,8});|&#[xX]([0-9A-Fa-f]{1,7});")


def emoji_matches(body):
    for m in EMOJI_RE.finditer(body):
        if m.group(1) is None and m.group(2) is None:
            yield m
            continue
        cp = int(m.group(1), 10) if m.group(1) is not None else int(m.group(2), 16)
        if cp <= 0x10FFFF and EMOJI_CHAR_RE.match(chr(cp)):
            yield m


def lint_file(path):
    src = Path(path).read_text(encoding="utf-8", errors="replace")
    lt = Linter(src, str(path))
    lt.feed(src)
    lt.close()
    lt.finish()
    body = re.sub(r"<(script|style)\b.*?</\1>", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S | re.I)
    for m in emoji_matches(body):
        lt.add(body.count("\n", 0, m.start()) + 1, "ERROR", "KO113", f"이모지 '{m.group(0)}'",
               "이모지를 지우시오. 표의 갖춤/없음 표시는 ○·△·×, 화살표는 →를 쓴다")
    lt.issues.sort(key=lambda i: (i["line"], i["id"]))
    return lt.issues


def collect(target):
    p = Path(target)
    if p.is_file():
        return [p]
    files = sorted(p.rglob("*.html"))
    # 원문 HTML(_src/), 생성 스크립트·스크린숏용 임시 HTML(_tmp/), vendor/는 검사 대상이 아니다
    files = [f for f in files
             if not any(part.startswith("_") or part == "vendor" for part in f.relative_to(p).parts[:-1])]
    if (p / "modules").is_dir():
        files = [f for f in files if f.name != "index.html" or f.parent != p]
    return files


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    unknown = [a for a in argv if a.startswith("--") and a not in ("--strict", "--json")]
    if unknown:
        print(f"알 수 없는 옵션: {' '.join(unknown)} (사용 가능: --strict, --json)", file=sys.stderr)
        return 2
    strict, as_json = "--strict" in argv, "--json" in argv
    if len(args) != 1:
        print(__doc__)
        return 2
    if not Path(args[0]).exists():
        print(f"경로를 찾을 수 없습니다: {args[0]}", file=sys.stderr)
        return 2
    files = collect(args[0])
    allissues = []
    for f in files:
        allissues += lint_file(f)
    errs = sum(i["severity"] == "ERROR" for i in allissues)
    warns = sum(i["severity"] == "WARN" for i in allissues)
    fail = errs > 0 or (strict and warns > 0)
    if as_json:
        print(json.dumps({"files": [str(f) for f in files], "issues": allissues,
                          "summary": {"errors": errs, "warnings": warns, "failed": fail}},
                         ensure_ascii=False, indent=2))
    else:
        for f in files:
            iss = [i for i in allissues if i["file"] == str(f)]
            print(f"== {f} ({len(iss)}건)")
            for i in iss:
                print(f"  {f}:{i['line']}  {i['severity']:5} {i['id']}  {i['message']}")
                print(f"        -> 제안: {i['fix']}")
        print(f"\n요약: 파일 {len(files)}개, ERROR {errs}건, WARN {warns}건"
              + (" (--strict: WARN도 실패 처리)" if strict else ""))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
