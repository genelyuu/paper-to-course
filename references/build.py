#!/usr/bin/env python3
"""강의 조립기: 단원 파일을 이어 붙이고, 외부 파일을 모두 안에 넣은 단독(standalone) index.html을 만든다.

    python3 build.py [강의 폴더]      (보통은 build.sh가 부른다)

결과 index.html 하나만 공유하면 된다. 네트워크·서버·다른 파일이 필요 없다(file://로 열림).
  - <link rel=stylesheet href=로컬>  → <style>  (CSS 안의 url(글꼴·그림)은 data URI)
  - <script src=로컬>                → 인라인 <script> (defer였던 것은 </body> 앞으로 옮김)
  - <img src=로컬>                   → data URI
  - 외부 URL(http/https/protocol-relative)을 불러오는 태그가 남아 있으면 오류로 멈춘다.

공유 시 노출을 줄이는 처리:
  - main.js·styles.css는 vendor/의 압축·난독화본(main.min.js, styles.min.css)으로 바꿔 넣는다.
    강의 폴더의 원본이 vendor/manifest.json의 해시와 다르면(수정됨) 원본을 넣고 경고한다
    (CSS는 주석만 지우고, JS는 문자열·정규식을 깨뜨리지 않도록 손대지 않는다).
  - HTML 주석(<!-- -->), SVG 주석·<metadata>·편집기 속성을 지운다.
  - 실행 엔진·템플릿 안내문이 산출물에 남지 않는다. 단, 브라우저에서 돌아가는 코드는 원리상
    완전히 숨길 수 없다(난독화는 읽기 어렵게 만들 뿐이다).

vendor/ 위치: <강의 폴더>/vendor → 이 스크립트 옆의 vendor → <강의 폴더>/../../references/vendor 순으로 찾는다.
fontTools가 설치되어 있으면 본문 글꼴을 강의에 실제로 쓰인 글자만 남기도록 더 줄인다(없으면 그대로 넣음).

node가 있으면 본문의 $…$·$$…$$ 수식을 vendor/katex로 미리 렌더링해 넣는다(첫 화면에 날 TeX가 안 보임).
실행 중 KaTeX auto-render는 그대로 돌지만 남은 구분 기호가 없어 아무것도 바꾸지 않는다.
node가 없거나 실패하면 경고 한 줄만 내고 예전처럼 실행 중 렌더링에 맡긴다. 끄려면 --no-prerender.

"[작성 필요: …]" 자리(scaffold.py가 남김)가 하나라도 있으면 목록을 보이고 실패한다.
미리 보기용으로 그대로 조립하려면 --allow-todo를 준다.
"""
import base64
import hashlib
import html as htmllib
import io
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

PROTECTED = re.compile(r"(<(script|style|pre|textarea)\b.*?</\2\s*>)", re.S | re.I)
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
TODO_RE = re.compile(r"\[작성 필요:[^\]]*\]")
MIME = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".svg": "image/svg+xml",
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".gif": "image/gif"}


# 제3자 구성 요소 라이선스 고지(산출물에 남긴다). strip 대상이 아니다.
NOTICES = {
    "katex.min.js": "/*! KaTeX v0.16.10 | MIT License | (c) Khan Academy and other contributors | github.com/KaTeX/KaTeX */\n",
    "auto-render.min.js": "/*! KaTeX auto-render v0.16.10 | MIT License | github.com/KaTeX/KaTeX */\n",
    "katex.min.css": "/*! KaTeX v0.16.10 | MIT License | KaTeX fonts: SIL OFL 1.1 */\n",
    "fonts.css": "/*! P2C Sans: modified (subset, renamed) Pretendard v1.3.9 (c) 2021 Kil Hyung-jin, SIL OFL 1.1"
                 " | JetBrains Mono (c) 2020 The JetBrains Mono Project Authors, SIL OFL 1.1 */\n",
}


def die(msg):
    sys.exit(f"ERROR: {msg}")


def warn(msg):
    print(f"WARN: {msg}", file=sys.stderr)


def find_vendor(course: Path) -> Path:
    for c in (course / "vendor", Path(__file__).resolve().parent / "vendor",
              course / ".." / ".." / "references" / "vendor"):
        if (c / "manifest.json").is_file():
            return c.resolve()
    die("vendor/ 폴더를 찾지 못했습니다. references/vendor/를 강의 폴더에 vendor/로 복사하세요.")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def data_uri(p: Path, raw: bytes = None) -> str:
    mime = MIME.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    raw = p.read_bytes() if raw is None else raw
    if mime == "image/svg+xml":  # SVG는 base64보다 짧은 퍼센트 인코딩으로 넣는다
        svg = re.sub(r"\s+", " ", clean_svg(raw.decode("utf-8")))
        # '&'·"'"도 인코딩한다: 속성값 디코딩에서 &amp;가 &로 풀리면 XML이 깨진다
        return "data:image/svg+xml," + quote(svg, safe=" /:=;,()-._~!*+?@$")
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def clean_svg(s: str) -> str:
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<metadata\b.*?</metadata>", "", s, flags=re.S | re.I)
    s = re.sub(r'\s(?:inkscape|sodipodi|sketch|serif|data-generator):[\w-]+="[^"]*"', "", s)
    return s.strip()


def strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def inline_css_urls(css: str, base: Path, fonts: dict) -> str:
    def rep(m):
        ref = m.group(2)
        if ref.startswith("data:") or ref.startswith("#"):
            return m.group(0)
        if EXTERNAL.match(ref):
            die(f"CSS에 외부 url()이 있습니다: {ref}")
        p = (base / ref).resolve()
        if not p.is_file():
            die(f"CSS url() 파일이 없습니다: {p}")
        raw = fonts.get(p.name)
        return f'url("{data_uri(p, raw)}")'
    return re.sub(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""", rep, css)


def subset_text(html: str, extra_files) -> str:
    """강의에 화면으로 나올 수 있는 글자 모음: 텍스트 노드뿐 아니라 모든 속성값(해설·용어 풀이·툴팁·
    aria-label·alt·title)까지 들어가도록 태그를 지우지 않고 문자 참조만 푼다.
    extra_files: 넣을 JS·CSS(정답/오답 문구, CSS content: 문자열)."""
    parts = [htmllib.unescape(html)]
    for f in extra_files:
        try:
            parts.append(Path(f).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            pass
    return "\n".join(parts)


def find_todos(files, course: Path, limit: int = 10):
    """[작성 필요: …] 자리: (전체 개수, 앞 limit개의 '파일:줄 내용')."""
    found, n = [], 0
    for p in files:
        for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for t in TODO_RE.findall(line):
                n += 1
                if len(found) < limit:
                    found.append(f"{p.relative_to(course)}:{ln} {t}")
    return n, found


def protect_scripts(html: str):
    """<script>…</script> 본문을 자리표로 바꿔 둔다(그림·스타일·링크 치환이 작성자 JS를 건드리지 않도록)."""
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return f"\x00P2CSCRIPT{len(saved) - 1}\x00"
    return re.sub(r"<script\b[^>]*>.*?</script\s*>", keep, html, flags=re.S | re.I), saved


def restore_scripts(html: str, saved) -> str:
    return re.sub(r"\x00P2CSCRIPT(\d+)\x00", lambda m: saved[int(m.group(1))], html)


def subset_body_font(font: Path, text: str):
    """fontTools가 있으면 강의에 쓰인 글자만 남긴다. 없으면 None."""
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        import brotli  # noqa: F401  (woff2 저장에 필요)
    except ImportError:
        return None
    chars = set(text) | set(chr(c) for c in range(0x20, 0x7F)) | set("·…‘’“”—–→←↑↓×÷±≤≥≠∑√∞")
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    f = TTFont(str(font))
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return buf.getvalue()


def strip_html_comments(html: str) -> str:
    parts = PROTECTED.split(html)
    out = []
    i = 0
    while i < len(parts):
        chunk = parts[i]
        if i % 3 == 0:
            chunk = re.sub(r"<!--.*?-->\s*", "", chunk, flags=re.S)
            out.append(chunk)
            i += 1
        else:
            out.append(chunk)
            i += 2  # 그룹 2(태그 이름)는 건너뛴다
    return "".join(out)


def attr(tag: str, name: str):
    m = re.search(rf"""\b{name}\s*=\s*(["'])(.*?)\1""", tag, re.S | re.I)
    return m.group(2) if m else None


def script_block(js: str) -> str:
    return "<script>" + js.replace("</script", "<\\/script") + "</script>"


# ── 수식 미리 렌더링 ─────────────────────────────────────────────
# main.js의 renderMathInElement(document.body, {$$ display, $ inline, throwOnError:false})와 같은 결과를
# 조립 때 만든다. 글 조각 나누기는 KaTeX auto-render 0.16.10(splitAtDelimiters·findEndOfMath)를 그대로 옮겼다.
# auto-render가 들어가지 않는 태그(ignoredTags)·원문 텍스트 태그와 svg·math·template은 건너뛴다
# (svg 안의 수식은 예전처럼 열 때 렌더링된다). 속성값(data-explanation-* 등)은 건드리지 않는다.
MATH_DELIMS = (("$$", True), ("$", False))
RAWTEXT_TAGS = ("script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes", "noscript")
MATH_SKIP = set(RAWTEXT_TAGS) | {"pre", "code", "option", "svg", "math", "template"}
TAG_RE = re.compile(r"""<!--.*?-->|<![^>]*>|<\?[^>]*>|</?([A-Za-z][A-Za-z0-9:-]*)(?:[^>"']|"[^"]*"|'[^']*')*>""", re.S)
AMS_RE = re.compile(r"^\\begin\{")
KATEX_NODE = r"""
const fs = require('fs');
const katex = require(process.env.P2C_KATEX);
const items = JSON.parse(fs.readFileSync(0, 'utf8'));
const macros = {};   // auto-render처럼 문서 전체가 매크로 표 하나를 함께 쓴다(\gdef 등)
const out = items.map(([tex, display]) => {
  try {
    return katex.renderToString(tex, {displayMode: display, throwOnError: false, macros: macros});
  } catch (e) { return null; }   // ParseError가 아닌 예외: 원문을 남겨 열 때 렌더링에 맡긴다
});
process.stdout.write(JSON.stringify(out));
"""


def _end_of_math(delim: str, text: str, start: int) -> int:
    """auto-render findEndOfMath: 중괄호 깊이 0에서 닫는 구분 기호 위치. 역슬래시 다음 글자는 건너뛴다."""
    i, depth = start, 0
    while i < len(text):
        c = text[i]
        if depth <= 0 and text.startswith(delim, i):
            return i
        if c == "\\":
            i += 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return -1


def split_math(text: str):
    """auto-render splitAtDelimiters: [("text", s) | ("math", tex, raw, display)]."""
    out = []
    while True:
        k = text.find("$")
        if k == -1:
            break
        if k > 0:
            out.append(("text", text[:k]))
            text = text[k:]
        left, display = next(d for d in MATH_DELIMS if text.startswith(d[0]))
        k = _end_of_math(left, text, len(left))
        if k == -1:
            break
        raw = text[:k + len(left)]
        out.append(("math", raw if AMS_RE.match(raw) else text[len(left):k], raw, display))
        text = text[k + len(left):]
    if text:
        out.append(("text", text))
    return out


def _skip_element(html: str, name: str, pos: int) -> int:
    """name 요소의 여는 태그 바로 뒤(pos)부터 짝이 맞는 닫는 태그 뒤까지 건너뛴 위치."""
    if name == "option":  # 닫는 태그를 생략할 수 있다
        m = re.compile(r"</option\s*>|<option\b|<optgroup\b|</select\s*>", re.I).search(html, pos)
        return (m.end() if m.group(0).lower().startswith("</option") else m.start()) if m else len(html)
    if name in RAWTEXT_TAGS:
        m = re.compile(rf"</{name}\s*>", re.I).search(html, pos)
        return m.end() if m else len(html)
    depth = 1
    for m in re.compile(rf"""<(/?){name}\b(?:[^>"']|"[^"]*"|'[^']*')*>""", re.I).finditer(html, pos):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return m.end()
        elif not m.group(0).endswith("/>"):
            depth += 1
    return len(html)


def prerender_math(html: str, vendor: Path):
    """<body> 텍스트의 수식을 KaTeX HTML로 바꾼다 → (새 html, 렌더링한 수식 수). 실패하면 예외."""
    node = shutil.which("node")
    katex_js = vendor / "katex" / "katex.min.js"
    if not node:
        raise RuntimeError("node가 없습니다")
    if not katex_js.is_file():
        raise RuntimeError(f"{katex_js} 가 없습니다")
    body = re.search(r"""<body\b(?:[^>"']|"[^"]*"|'[^']*')*>""", html, re.I)
    if not body:
        return html, 0
    # 1) 수식이 든 텍스트 조각 모으기: (시작, 끝, 나눈 결과)
    runs, pos = [], body.end()
    while pos < len(html):
        m = TAG_RE.search(html, pos)
        end = m.start() if m else len(html)
        if "$" in html[pos:end]:
            parts = split_math(htmllib.unescape(html[pos:end]))
            if any(p[0] == "math" for p in parts):
                runs.append((pos, end, parts))
        if not m:
            break
        pos = m.end()
        name = (m.group(1) or "").lower()
        if name in MATH_SKIP and not m.group(0).startswith("</") and not m.group(0).endswith("/>"):
            pos = _skip_element(html, name, pos)
    items = [(p[1], p[3]) for _, _, parts in runs for p in parts if p[0] == "math"]
    if not items:
        return html, 0
    # 2) node 한 번으로 전부 렌더링(수식 목록은 표준 입력 JSON으로)
    with tempfile.TemporaryDirectory() as td:
        script = Path(td) / "katex-prerender.js"
        script.write_text(KATEX_NODE, encoding="utf-8")
        r = subprocess.run([node, str(script)], input=json.dumps(items), capture_output=True,
                           encoding="utf-8", timeout=300, env={**os.environ, "P2C_KATEX": str(katex_js)})
    if r.returncode != 0:
        raise RuntimeError((r.stderr.strip().splitlines() or ["node 실패"])[-1])
    rendered = json.loads(r.stdout)
    if len(rendered) != len(items):
        raise RuntimeError("node 결과 개수가 맞지 않습니다")
    # 3) 바꿔 넣기: 텍스트는 다시 이스케이프, 수식은 auto-render처럼 <span>으로 감싼다
    esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")  # noqa: E731
    out, last, k, n = [], 0, 0, 0
    for start, end, parts in runs:
        out.append(html[last:start])
        for p in parts:
            if p[0] == "text":
                out.append(esc(p[1]))
                continue
            h, k = rendered[k], k + 1
            if h is None:
                out.append(esc(p[2]))
            else:
                out.append("<span>" + h + "</span>")
                n += 1
        last = end
    out.append(html[last:])
    return "".join(out), n


def build(course: Path, allow_todo: bool = False, prerender: bool = True):
    for f in ("_base.html", "_cover.html", "_footer.html"):
        if not (course / f).is_file():
            die(f"{f} 가 없습니다.")
    mods = sorted((course / "modules").glob("*.html"))
    if not mods:
        die("modules/*.html 이 없습니다.")
    parts = [course / "_base.html", course / "_cover.html", *mods, course / "_footer.html"]
    n_todo, todos = find_todos(parts, course)
    if n_todo:
        msg = (f"아직 쓰지 않은 [작성 필요: …] 자리가 {n_todo}개 남아 있습니다"
               + (f" (앞 {len(todos)}개만 보임)" if n_todo > len(todos) else "") + ":\n  "
               + "\n  ".join(todos))
        if not allow_todo:
            die(msg + "\n채운 뒤 다시 조립하시오 (python3 -I scaffold.py todo <강의 폴더>로 확인)."
                " 미리 보기로만 조립하려면 --allow-todo (bash build.sh --allow-todo).")
        warn(msg + "\n--allow-todo: 자리를 남긴 채 조립합니다(공유 금지).")
    html = "".join(p.read_text(encoding="utf-8") for p in parts)

    vendor = find_vendor(course)
    manifest = json.loads((vendor / "manifest.json").read_text(encoding="utf-8"))

    def resolve(ref: str) -> Path:
        ref = ref.split("?")[0].split("#")[0]
        if ref.startswith("vendor/"):
            return vendor / ref[len("vendor/"):]
        return course / ref

    def load_engine(ref: str, p: Path):
        """main.js·styles.css → 압축·난독화본. 원본이 바뀌었으면 원본을 주석만 지워 쓴다."""
        name = p.name
        mini = {"main.js": "main.min.js", "styles.css": "styles.min.css"}.get(name)
        if mini and ref == name:
            if p.is_file() and sha256(p) == manifest.get(name):
                return (vendor / mini).read_text(encoding="utf-8"), vendor
            if p.is_file():
                warn(f"{name} 파일이 references 원본과 다릅니다. 압축본 대신 원본을 넣습니다"
                     " (references/vendor/make-vendor.sh로 압축본을 다시 만드세요).")
        if not p.is_file():
            die(f"파일이 없습니다: {p}")
        src = p.read_text(encoding="utf-8")
        if p.is_relative_to(vendor):  # 제3자 구성 요소: 압축본 그대로 두고 라이선스 고지만 붙인다
            return NOTICES.get(p.name, "") + (strip_css_comments(src) if p.suffix == ".css" else src), p.parent
        # 작성자 JS는 그대로 넣는다(정규식 주석 지우기는 'figs/*.svg'·/a*/ 같은 문자열·정규식을 깨뜨린다)
        return (strip_css_comments(src) if p.suffix == ".css" else src), p.parent

    # 수식 미리 렌더링(선택). 글꼴 부분 집합보다 먼저 한다(KaTeX 결과 글자까지 부분 집합에 들어가도록).
    n_math = 0
    if prerender:
        try:
            html, n_math = prerender_math(strip_html_comments(html), vendor)
        except Exception as e:  # 조립은 멈추지 않는다: 예전처럼 열 때 렌더링
            warn(f"수식 미리 렌더링을 건너뜁니다 ({e}). 열 때 KaTeX가 렌더링합니다.")

    # 본문 글꼴 부분 집합(선택)
    fonts = {}
    body_font = vendor / "fonts" / "P2CSans-Variable.woff2"
    if body_font.is_file():
        extra = []
        for tag in re.findall(r"<(?:script|link)\b[^>]*>", html, re.I):
            ref = attr(tag, "src") or attr(tag, "href")
            if not ref or EXTERNAL.match(ref) or ref.startswith(("data:", "#")):
                continue
            p = resolve(ref)
            extra.append(p)  # 강의 폴더의 main.js·styles.css 원본(압축본은 문자열이 암호화되어 있다)
            mini = {"main.js": "main.min.js", "styles.css": "styles.min.css"}.get(p.name)
            if mini:
                extra.append(vendor / mini)
        text = subset_text(html, extra)
        sub = subset_body_font(body_font, text)
        if sub:
            fonts[body_font.name] = sub

    deferred = []

    def rep_link(m):
        tag = m.group(0)
        rel = (attr(tag, "rel") or "").lower()
        href = attr(tag, "href") or ""
        if rel in ("preconnect", "dns-prefetch", "preload", "prefetch"):
            return ""
        if rel != "stylesheet":
            return tag
        if EXTERNAL.match(href):
            die(f"외부 스타일시트가 남아 있습니다: {href}")
        css, base = load_engine(href, resolve(href))
        return "<style>" + inline_css_urls(css, base, fonts) + "</style>"

    def rep_script(m):
        tag, body = m.group(1), m.group(2)
        src = attr(tag, "src")
        if not src:
            return m.group(0)
        if EXTERNAL.match(src):
            die(f"외부 스크립트가 남아 있습니다: {src}")
        js, _ = load_engine(src, resolve(src))
        block = script_block(js)
        if re.search(r"\b(defer|type\s*=\s*[\"']module)", tag, re.I):
            deferred.append(block)
            return ""
        return block

    def rep_img(m):
        tag = m.group(0)
        src = attr(tag, "src")
        if not src or src.startswith("data:"):
            return tag
        if EXTERNAL.match(src):
            die(f"외부 그림이 남아 있습니다: {src}")
        p = resolve(src)
        if not p.is_file():
            die(f"그림 파일이 없습니다: {p}")
        tag = tag.replace(src, data_uri(p), 1)
        if src.startswith("assets/"):  # check-pages.py가 삽화 개수를 셀 표지
            tag = tag.replace("<img", "<img data-asset", 1)
        return tag

    # 순서가 중요하다: 그림·인라인 <style>을 먼저 처리하고, 엔진 CSS·JS는 마지막에 넣는다
    # (넣은 JS 문자열 안의 '<img'·'<style' 같은 조각을 다시 건드리지 않도록).
    html = strip_html_comments(html)
    html, scripts = protect_scripts(html)
    html = re.sub(r"<img\b[^>]*>", rep_img, html, flags=re.I)
    html = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)",
                  lambda m: m.group(1) + inline_css_urls(strip_css_comments(m.group(2)), course, fonts) + m.group(3),
                  html, flags=re.S | re.I)
    html = re.sub(r"<link\b[^>]*>", rep_link, html, flags=re.I)
    html = restore_scripts(html, scripts)
    html = re.sub(r"(<script\b[^>]*>)(.*?)</script\s*>", rep_script, html, flags=re.S | re.I)
    if deferred:
        html = re.sub(r"</body>", lambda _: "\n".join(deferred) + "\n</body>", html, count=1, flags=re.I)

    # 최종 점검: 외부 자원을 불러오는 속성이 남았는가(일반 하이퍼링크 <a href>는 허용)
    left = re.findall(r"<(?:script|link|img|iframe|source|video|audio)\b[^>]*\b(?:src|href)\s*=\s*[\"']((?:https?:)?//[^\"']+)",
                      html, re.I)
    if left:
        die("외부 자원이 남아 있습니다: " + ", ".join(left[:5]))

    out = course / "index.html"
    tmp = course / "index.html.tmp"
    tmp.write_text(html, encoding="utf-8")
    tmp.replace(out)
    kb = out.stat().st_size / 1024
    note = "본문 글꼴 부분 집합 적용" if fonts else "본문 글꼴 전체(KS X 1001) 포함 — fontTools를 설치하면 더 작아짐"
    if n_math:
        note += f", 수식 {n_math}개 미리 렌더링"
    print(f"Built index.html — 단독 파일 {kb:,.0f} KB ({note}). 이 파일 하나만 공유하면 됩니다.")


if __name__ == "__main__":
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    bad = [a for a in opts if a not in ("--allow-todo", "--no-prerender")]
    if bad:
        die(f"알 수 없는 옵션: {' '.join(bad)} (사용 가능: --allow-todo, --no-prerender)")
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    build(Path(pos[0] if pos else ".").resolve(), allow_todo="--allow-todo" in opts,
          prerender="--no-prerender" not in opts)
