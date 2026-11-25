#!/usr/bin/env python3
"""한 페이지 검사: 코넬식 화면이 데스크톱 한 화면(기본 1440×900)에 스크롤 없이 들어가는지 잰다.

사용법:
    python3 check-pages.py <강의 폴더 또는 index.html> [--width 1440] [--height 900] [--chrome PATH]

페이지 단위:
  - 단원 도입(.module-header) + 바로 뒤 첫 화면 = 1페이지
  - 그 밖의 .screen 하나 = 1페이지
허용 높이 = 창 높이 - 상단 내비게이션 높이(--nav-height).
min-height(100vh)를 풀고 내용의 실제 높이를 잰다.

종료 코드: 넘치는 페이지가 있으면 1, 아니면 0. 표준 라이브러리와 Chrome만 쓴다.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]

PROBE = r"""
<style id="__fit_style">
  .animate-in, .animate-in * { opacity: 1 !important; transform: none !important; transition: none !important; }
  .screen.cornell { min-height: 0 !important; }
  html { scroll-snap-type: none !important; }
</style>
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    var nav = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 48;
    var limit = window.innerHeight - nav;
    var pages = [];
    document.querySelectorAll('.module').forEach(function (mod, mi) {
      var header = mod.querySelector('.module-header');
      var screens = Array.prototype.slice.call(mod.querySelectorAll('.screen'));
      screens.forEach(function (s, si) {
        var r = s.getBoundingClientRect();
        var top = r.top, label = s.querySelector('.screen-heading, h3');
        if (si === 0 && header) top = header.getBoundingClientRect().top;
        pages.push({
          module: mod.id || ('module-' + mi),
          page: si + 1,
          cornell: s.classList.contains('cornell'),
          height: Math.round(r.bottom - top),
          title: label ? label.textContent.trim().replace(/\s+/g, ' ').slice(0, 40) : ''
        });
      });
    });
    var pre = document.createElement('pre');
    pre.id = '__fit_result';
    pre.textContent = JSON.stringify({ limit: Math.round(limit), width: window.innerWidth, pages: pages });
    document.body.appendChild(pre);
  }, 300);
});
</script>
"""


def find_chrome(explicit):
    for c in ([explicit] if explicit else []) + CHROME_CANDIDATES:
        if c and (os.path.isfile(c) or shutil.which(c)):
            return c if os.path.isfile(c) else shutil.which(c)
    sys.exit("Chrome을 찾지 못했다. --chrome으로 경로를 지정하시오.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--chrome")
    a = ap.parse_args()

    path = a.target
    if os.path.isdir(path):
        path = os.path.join(path, "index.html")
    if not os.path.isfile(path):
        sys.exit(f"파일이 없다: {path}")
    html = open(path, encoding="utf-8").read()
    html = re.sub(r"</body>", lambda _: PROBE + "</body>", html, count=1, flags=re.I)

    # 상대 경로(styles.css, main.js)를 그대로 쓰려고 같은 폴더에 임시 파일을 만든다
    fd, tmp = tempfile.mkstemp(prefix=".fit-", suffix=".html", dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        out = subprocess.run(
            [find_chrome(a.chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--window-size={a.width},{a.height}", "--virtual-time-budget=10000",
             "--dump-dom", "file://" + os.path.abspath(tmp)],
            capture_output=True, text=True, timeout=120).stdout
    finally:
        os.remove(tmp)

    m = re.search(r'<pre id="__fit_result">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("측정 결과를 읽지 못했다(페이지 로드 실패).")
    data = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
    limit = data["limit"]
    over = 0
    print(f"기준: {a.width}×{a.height}, 페이지 허용 높이 {limit}px")
    for p in data["pages"]:
        ok = p["height"] <= limit
        over += not ok
        kind = "코넬" if p["cornell"] else "일반"
        flag = "OK  " if ok else "OVER"
        extra = "" if ok else f"  (+{p['height'] - limit}px)"
        print(f"{flag} {p['module']} p{p['page']} [{kind}] {p['height']}px  {p['title']}{extra}")
    plain = sum(not p["cornell"] for p in data["pages"])
    print(f"\n요약: 페이지 {len(data['pages'])}개, 넘침 {over}개, 코넬 아닌 화면 {plain}개")
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
