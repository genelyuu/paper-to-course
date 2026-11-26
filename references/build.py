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

"[작성 필요: …]" 자리(scaffold.py가 남김)가 하나라도 있으면 목록을 보이고 실패한다.
미리 보기용으로 그대로 조립하려면 --allow-todo를 준다.
"""
import base64
import hashlib
import html as htmllib
import io
import json
import mimetypes
import re
import sys
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


def build(course: Path, allow_todo: bool = False):
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
    print(f"Built index.html — 단독 파일 {kb:,.0f} KB ({note}). 이 파일 하나만 공유하면 됩니다.")


if __name__ == "__main__":
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    bad = [a for a in opts if a != "--allow-todo"]
    if bad:
        die(f"알 수 없는 옵션: {' '.join(bad)} (사용 가능: --allow-todo)")
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    build(Path(pos[0] if pos else ".").resolve(), allow_todo="--allow-todo" in opts)
