#!/usr/bin/env python3
"""한 페이지 검사: 코넬식 화면이 데스크톱 한 화면(기본 1440×900)에 스크롤 없이 들어가는지 잰다.

사용법:
    python3 check-pages.py <강의 폴더 또는 index.html> [--width 1440] [--height 900] [--chrome PATH]
                           [--mobile-width 390] [--no-mobile]

페이지 단위:
  - 단원 도입(.module-header) + 바로 뒤 첫 화면 = 1페이지
  - 그 밖의 .screen 하나 = 1페이지
허용 높이 = 창 높이 - 상단 내비게이션 높이(--nav-height).
min-height(100vh)를 풀고 내용의 실제 높이를 잰다.
확인 문제는 모든 해설(정답·오답 중 긴 쪽)을 펼친 최악의 상태로 잰다.
그림 정렬도 검사한다: 결과 막대 트랙의 시작 x·폭, SVG 요소의 viewBox 이탈과 노드 라벨 구조,
의사코드 코드 줄과 설명 줄의 세로 위치, 문항 삽화(.q-figure)·그림(.figure)의 형식(SVG만)과 색(교과 색 하나;
인라인 <svg>와 <img>로 넣은 SVG의 fill·stroke·stop-color 모두).
배치도 검사한다(LAY): 화면·노트 칸 밖으로 가로로 넘친 요소, overflow로 잘린 내용, SVG 글자의 그림 경계 이탈,
SVG 글자끼리 겹침, 상자 라벨(foreignObject)의 넘침, 페이지 가로 스크롤, 잘린 사이드바 목차 라벨, 색칠되지 않은 코드 칸.
단원 첫 페이지는 단원 맨 위(내비 아래 여백 포함)부터 잰다.
모바일 배치도 검사한다(LAY): 폭 390px(--mobile-width)로 한 번 더 열고(headless 창은 500px보다 좁아지지 않아 그 폭의 iframe 안에서 연다) KaTeX가 그려질 때까지(약 2초) 기다린 뒤
페이지 전체가 옆으로 밀리는지(scrollWidth > clientWidth) 잰다. 밀리면 원인 요소를 5개까지 알린다
(화면 오른쪽 밖으로 나간 가장 안쪽 요소; 화면 안에 들어오는 가로 스크롤·잘림 상자 안의 요소는 빼고,
absolute 요소는 스크롤 상자를 빠져나간 경우만). --no-mobile로 건너뛴다(Chrome을 한 번 덜 띄운다).

종료 코드: 넘치는 페이지, 그림 정렬 문제, 배치 문제(모바일 포함)가 있으면 1, 아니면 0. 표준 라이브러리와 Chrome만 쓴다.
"""
import argparse, html as htmllib, json, os, re, shutil, subprocess, sys, tempfile

MIN_IMAGES = 3   # 강의 전체 삽화(assets/의 사물·장면 선화, figure img) 최소 개수

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]

PROBE = r"""
<style id="__fit_style">
  .animate-in, .animate-in *:not(svg, svg *) { opacity: 1 !important; transform: none !important; transition: none !important; }
  .screen.cornell { min-height: 0 !important; }
  html { scroll-snap-type: none !important; }
  .quiz-feedback { transition: none !important; }
</style>
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    // 최악의 경우: 모든 문항의 해설을 더 긴 쪽(정답/오답)으로 펼친 상태에서 잰다
    document.querySelectorAll('.quiz-question-block').forEach(function (b) {
      var f = b.querySelector('.quiz-feedback'); if (!f) return;
      var r = b.dataset.explanationRight || '', w = b.dataset.explanationWrong || '';
      f.innerHTML = '<strong>오답</strong> ' + (w.length > r.length ? w : r);
      f.className = 'quiz-feedback show error';
      // 실제 화면처럼 해설 속 $…$ 수식도 렌더링해서 높이를 잰다
      if (typeof window.renderMathInElement === 'function') {
        try {
          window.renderMathInElement(f, { delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false });
        } catch (e) {}
      }
    });
    var nav = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 48;
    var limit = window.innerHeight - nav;
    var pages = [];
    document.querySelectorAll('.module').forEach(function (mod, mi) {
      var header = mod.querySelector('.module-header');
      var screens = Array.prototype.slice.call(mod.querySelectorAll('.screen'));
      screens.forEach(function (s, si) {
        var r = s.getBoundingClientRect();
        var top = r.top, label = s.querySelector('.screen-heading, h3');
        if (si === 0 && header) top = mod.getBoundingClientRect().top + nav;
        pages.push({
          module: mod.id || ('module-' + mi),
          page: si + 1,
          cornell: s.classList.contains('cornell'),
          height: Math.round(r.bottom - top),
          title: label ? Array.prototype.map.call(label.childNodes, function (n) { return n.textContent.trim(); }).join(' ').replace(/\s+/g, ' ').slice(0, 40) : ''
        });
      });
    });
    // 그림 정렬 검사
    var fig = [];
    document.querySelectorAll('.result-bars').forEach(function (bars, bi) {
      var xs = Array.prototype.map.call(bars.querySelectorAll('.result-bar-track'), function (t) { var r = t.getBoundingClientRect(); return Math.round(r.left) + '/' + Math.round(r.width); });
      if (new Set(xs).size > 1) fig.push('결과 막대 #' + (bi + 1) + ': 트랙 시작 x/폭이 다르다 ' + xs.join(', '));
    });
    document.querySelectorAll('.svg-diagram svg').forEach(function (svg, si) {
      var vb = (svg.getAttribute('viewBox') || '').split(/\s+/).map(Number); if (vb.length !== 4) return;
      svg.querySelectorAll('rect, foreignObject, line').forEach(function (e) {
        var b = e.getBBox();
        if (b.x < vb[0] - 0.5 || b.y < vb[1] - 0.5 || b.x + b.width > vb[0] + vb[2] + 0.5 || b.y + b.height > vb[1] + vb[3] + 0.5)
          fig.push('SVG #' + (si + 1) + ': ' + e.tagName + '가 viewBox 밖으로 나간다 (' + [b.x, b.y, b.width, b.height].map(Math.round).join(',') + ')');
      });
      svg.querySelectorAll('foreignObject > div').forEach(function (d) {
        if (d.children.length !== 1 || d.childNodes.length !== 1) fig.push('SVG #' + (si + 1) + ': 노드 라벨을 <span> 하나로 감싸지 않았다 "' + d.textContent.trim().slice(0, 20) + '"');
      });
    });
    // 문항 삽화·그림: SVG만 허용, 색은 검정·회색 + 교과 색 하나(인라인 <svg>와 <img>로 넣은 SVG 모두)
    function addHue(hues, c) {
      var m = /rgba?\((\d+), (\d+), (\d+)(?:, ([\d.]+))?/.exec(c || '');
      if (!m || (m[4] !== undefined && +m[4] === 0)) return;
      var r = +m[1], g = +m[2], b = +m[3];
      if (Math.max(r, g, b) - Math.min(r, g, b) < 24) return;   // 검정·회색·흰색
      hues.add(r + ',' + g + ',' + b);
    }
    var colorProbe = document.createElement('span');
    document.body.appendChild(colorProbe);
    function cssColor(v) {   // SVG 속성의 색 값 → 계산된 rgb(). none·url(#…) 등은 ''
      colorProbe.style.color = '';
      colorProbe.style.color = v.trim();
      return colorProbe.style.color ? getComputedStyle(colorProbe).color : '';
    }
    function svgText(src) {   // data URI(퍼센트·base64) 또는 check-pages.py가 읽어 둔 .svg 파일
      var m = /^data:image\/svg\+xml(;[^,]*)?,(.*)$/is.exec(src);
      try {
        if (m) return /;base64/i.test(m[1] || '') ? decodeURIComponent(escape(atob(m[2]))) : decodeURIComponent(m[2]);
      } catch (e) { return ''; }
      return (window.__p2cSvg || {})[src] || '';
    }
    var figCount = { 'q-figure': 0, 'figure': 0 };
    document.querySelectorAll('.q-figure, .figure').forEach(function (f) {
      var kind = f.classList.contains('q-figure') ? 'q-figure' : 'figure';
      var name = (kind === 'q-figure' ? '문항 삽화 #' : '그림 #') + (++figCount[kind]);
      var hues = new Set();
      f.querySelectorAll('img').forEach(function (im) {
        var src = im.getAttribute('src') || '';
        if (!/\.svg(\?|#|$)/i.test(src) && !/^data:image\/svg\+xml[,;]/i.test(src)) fig.push(name + ': SVG가 아닌 이미지 ' + src.slice(0, 80) + ' (래스터는 벡터화해서 넣는다)');
        if (!im.complete || im.naturalWidth === 0) fig.push(name + ': 이미지를 불러오지 못했다 ' + src.slice(0, 80));
        var t = svgText(src), re = /(?:^|[\s;{"'])(fill|stroke|stop-color)\s*(?:=\s*["']([^"']*)["']|:\s*([^;"'}<>]+))/g, mm;
        while ((mm = re.exec(t))) addHue(hues, cssColor(mm[2] !== undefined ? mm[2] : mm[3]));
      });
      f.querySelectorAll('svg *').forEach(function (e) {
        var cs = getComputedStyle(e);
        [cs.stroke, cs.fill].forEach(function (c) { addHue(hues, c); });
      });
      if (hues.size > 1) fig.push(name + ': 유채색이 ' + hues.size + '개다 (교과 색 하나만) ' + Array.from(hues).join(' | '));
    });
    colorProbe.remove();
    document.querySelectorAll('.pseudocode-translation').forEach(function (pc, pi) {
      var a = pc.querySelectorAll('.pseudocode-line'), b = pc.querySelectorAll('.pe');
      if (a.length !== b.length) fig.push('의사코드 #' + (pi + 1) + ': 코드 줄 ' + a.length + '개, 설명 줄 ' + b.length + '개');
      for (var i = 0; i < Math.min(a.length, b.length); i++) {
        var d = Math.abs(a[i].getBoundingClientRect().top - b[i].getBoundingClientRect().top);
        if (d > 1) { fig.push('의사코드 #' + (pi + 1) + ': ' + (i + 1) + '번째 줄이 설명과 ' + Math.round(d) + 'px 어긋난다'); break; }
      }
    });
    // 배치 검사(LAY)
    var lay = [];
    function vis(el) {
      if (el.closest && el.closest('.katex-mathml, .sr-only, .visually-hidden, .term-tooltip, [role=tooltip]')) return false;
      var cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      var r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0;
    }
    function nm(el) { var c = el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className; return el.tagName.toLowerCase() + (c ? '.' + String(c).split(/\s+/)[0] : ''); }
    function tx(el) { return (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24); }
    document.querySelectorAll('.module').forEach(function (mod) {
      mod.querySelectorAll('.screen').forEach(function (s, si) {
        if (!vis(s)) return;
        var where = (mod.id || 'module') + ' p' + (si + 1), sr = s.getBoundingClientRect();
        var notes = s.querySelector(':scope > .notes'), nr = notes ? notes.getBoundingClientRect() : sr;
        var seen = 0;
        s.querySelectorAll('*').forEach(function (e) {
          if (seen > 2) return;
          if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
          if (!vis(e)) return;
          var r = e.getBoundingClientRect(), box = notes && notes.contains(e) ? nr : sr;
          if (r.right > box.right + 2 || r.left < box.left - 2) {
            var inner = Array.prototype.some.call(e.children, function (c) { var q = c.getBoundingClientRect(); return vis(c) && (q.right > box.right + 2 || q.left < box.left - 2); });
            if (!inner) { lay.push(where + ': 가로로 ' + Math.round(Math.max(r.right - box.right, box.left - r.left)) + 'px 넘친다 ' + nm(e) + ' "' + tx(e) + '"'); seen++; }
          }
          var cs = getComputedStyle(e), dx = e.scrollWidth - e.clientWidth, dy = e.scrollHeight - e.clientHeight;
          if (((cs.overflowX === 'hidden' || cs.overflowX === 'clip') && dx > 2) || ((cs.overflowY === 'hidden' || cs.overflowY === 'clip') && dy > 2)) {
            if (!e.closest('.sidebar') && !e.classList.contains('pseudocode-translation')) { lay.push(where + ': 내용이 잘린다(overflow) ' + nm(e) + ' dx=' + dx + ' dy=' + dy + ' "' + tx(e) + '"'); seen++; }
          } else if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && dx > 2) { lay.push(where + ': 가로 스크롤이 생긴다 ' + nm(e) + ' dx=' + dx); seen++; }
        });
        s.querySelectorAll('svg').forEach(function (svg, k) {
          if (!vis(svg)) return;
          var SR = svg.getBoundingClientRect(), clip = getComputedStyle(svg).overflow !== 'visible', bs = [];
          svg.querySelectorAll('text').forEach(function (t) {
            if (!vis(t) || !tx(t)) return;
            var TR = t.getBoundingClientRect();
            if (clip && (TR.left < SR.left - 1 || TR.top < SR.top - 1 || TR.right > SR.right + 1 || TR.bottom > SR.bottom + 1))
              lay.push(where + ': SVG #' + (k + 1) + ' 글자가 그림 경계 밖에서 잘린다 "' + tx(t) + '"');
            bs.push([TR, tx(t)]);
          });
          // 상자 라벨: 보이는 글자(KaTeX의 숨은 MathML 제외)가 foreignObject 밖으로 2px 넘게 나가면 상자가 빡빡하다
          svg.querySelectorAll('foreignObject').forEach(function (fo) {
            var c = fo.firstElementChild; if (!c || !vis(c)) return;
            var FR = fo.getBoundingClientRect(), g = null, w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
            for (var n = w.nextNode(); n; n = w.nextNode()) {
              if (!n.nodeValue.trim() || n.parentElement.closest('.katex-mathml')) continue;
              var rg = document.createRange(); rg.selectNodeContents(n);
              [].forEach.call(rg.getClientRects(), function (q) {
                if (!q.width) return;
                g = g ? { l: Math.min(g.l, q.left), t: Math.min(g.t, q.top), r: Math.max(g.r, q.right), b: Math.max(g.b, q.bottom) } : { l: q.left, t: q.top, r: q.right, b: q.bottom };
              });
            }
            if (!g) return;
            var over = Math.max(FR.left - g.l, FR.top - g.t, g.r - FR.right, g.b - FR.bottom);
            if (over > 2) lay.push(where + ': SVG #' + (k + 1) + ' 상자 라벨이 ' + Math.round(over) + 'px 넘친다(상자를 키우거나 줄을 나눈다) "' + tx(c) + '"');
          });
          for (var i = 0; i < bs.length; i++) for (var j = i + 1; j < bs.length; j++) {
            var a = bs[i][0], b = bs[j][0];
            var ix = Math.min(a.right, b.right) - Math.max(a.left, b.left), iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
            var ar = Math.min(a.width * a.height, b.width * b.height);
            if (ix > 1 && iy > 1 && ar > 0 && ix * iy / ar > 0.25 && !(bs[i][1] === bs[j][1] && Math.abs(a.left - b.left) < 1 && Math.abs(a.top - b.top) < 1))
              lay.push(where + ': SVG #' + (k + 1) + ' 글자가 겹친다 "' + bs[i][1] + '" × "' + bs[j][1] + '"');
          }
        });
        s.querySelectorAll('pre, .pseudocode-line').forEach(function (c) {
          if (c.matches('.pseudocode-line') && c.closest('pre')) return;
          if (/[A-Z]{2,}|\d|[:=←→≥≤≠∧∨∪∈"']|\w\(|\/\/|^\s*[A-Z][a-z]+\b/.test(c.textContent) && !c.querySelector('[class^="code-"], [class*=" code-"], .katex'))
            lay.push(where + ': 코드 색칠이 안 됐다 ' + nm(c) + ' "' + tx(c) + '"');
        });
      });
    });
    var dw = document.documentElement.scrollWidth - window.innerWidth;
    if (dw > 2) lay.push('페이지: 가로 스크롤 ' + dw + 'px');
    document.querySelectorAll('.sidebar-item-label').forEach(function (e) {
      if (e.scrollWidth > e.clientWidth + 1) lay.push('사이드바: 목차 라벨이 잘린다 "' + e.textContent.trim() + '" (더 짧게)');
    });
    // scaffold.py가 남긴 빈자리
    ((function () { var r = document.querySelector('main') || document.body, t = r.textContent; r.querySelectorAll('*').forEach(function (e) { for (var i = 0; i < e.attributes.length; i++) { var v = e.attributes[i].value; if (v.indexOf('작성 필요') >= 0) t = v + ' ' + t; } }); return t; })().match(/\[작성 필요: [^\]]*\]/g) || []).slice(0, 5).forEach(function (t) {
      lay.push('미작성 자리가 남았다 ' + t + ' (scaffold.py todo로 위치 확인)');
    });
    var pre = document.createElement('pre');
    pre.id = '__fit_result';
    var images = document.querySelectorAll('figure img[src^="assets/"], figure img[data-asset]').length;   // 모델 삽화(사물·장면 선화)
    pre.textContent = JSON.stringify({ limit: Math.round(limit), width: window.innerWidth, pages: pages, fig: fig, lay: lay, images: images });
    document.body.appendChild(pre);
  }, 300);
});
</script>
"""

# 모바일 폭 검사: 페이지가 옆으로 밀리는지와 그 원인 요소
MOBILE_PROBE = r"""
<style id="__fit_style">
  .animate-in, .animate-in *:not(svg, svg *) { opacity: 1 !important; transform: none !important; transition: none !important; }
</style>
<script>
window.addEventListener('load', function () {
  setTimeout(function () {   // KaTeX·글꼴이 자리 잡을 때까지 기다린다
    var de = document.documentElement, W = de.clientWidth, dw = de.scrollWidth - W, found = [];
    function nm(el) { var c = el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className; return el.tagName.toLowerCase() + (c ? '.' + String(c).trim().split(/\s+/)[0] : ''); }
    function tx(el) {   // 보이는 글자만(KaTeX의 숨은 MathML·TeX 원문은 뺀다)
      if (el.querySelector && el.querySelector('.katex-mathml')) { el = el.cloneNode(true); el.querySelectorAll('.katex-mathml').forEach(function (k) { k.remove(); }); }
      return (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24);
    }
    // 화면 안에 들어오는 가로 스크롤·잘림 상자(조상)를 찾는다
    function scroller(e) {
      for (var p = e.parentElement; p && p !== document.body && p !== de; p = p.parentElement) {
        var s = getComputedStyle(p);
        if (/(auto|scroll|hidden|clip)/.test(s.overflowX) && p.getBoundingClientRect().right <= W + 1) return p;
      }
      return null;
    }
    if (dw > 2) {
      var seen = {};
      document.querySelectorAll('body *').forEach(function (e) {
        var r = e.getBoundingClientRect();
        if (r.width === 0 || r.right <= W + 2) return;
        if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
        var cs = getComputedStyle(e);
        if (cs.position === 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') return;
        var sc = scroller(e);
        if (cs.position === 'absolute') {
          // 기준 상자(offsetParent)가 스크롤 상자 안이면 그 안에서 잘리므로 괜찮다
          var op = e.offsetParent;
          if (sc && op && (sc === op || sc.contains(op))) return;
        } else {
          if (sc) return;
          // 가장 안쪽 요소만: 자식이 함께 넘치면 자식을 알린다
          if (Array.prototype.some.call(e.children, function (k) { return k.getBoundingClientRect().right > W + 2 && !(k.closest('svg') && k.tagName.toLowerCase() !== 'svg'); })) return;
        }
        // 선택자 요약: 요소 + 클래스가 있는 조상 둘(tr·tbody 같은 맨 태그는 건너뛴다)
        var chain = [], p = e.parentElement;
        for (; chain.length < 2 && p && p !== document.body; p = p.parentElement) if (nm(p).indexOf('.') > 0) chain.push(nm(p));
        var key = (cs.position === 'absolute' ? '[absolute] ' : '') + nm(e) + (chain.length ? ' < ' + chain.join(' < ') : '');
        var mod = e.closest('.module'), scr = e.closest('.screen');
        var where = mod ? (mod.id || 'module') + (scr ? ' p' + (Array.prototype.indexOf.call(mod.querySelectorAll('.screen'), scr) + 1) : '') : '';
        if (!seen[key]) { seen[key] = { key: key, where: where, right: 0, n: 0, text: tx(e) }; found.push(seen[key]); }
        seen[key].n++; seen[key].right = Math.max(seen[key].right, Math.round(r.right));
      });
      found.sort(function (a, b) { return b.right - a.right; });
    }
    // 바깥 틀(MOBILE_FRAME)에 결과를 넘긴다
    parent.postMessage('__fit_result' + JSON.stringify({ width: W, inner: window.innerWidth, dw: dw, culprits: found.slice(0, 5), total: found.length }), '*');
  }, 2000);
});
</script>
"""

# headless Chrome 창은 폭 500px보다 좁아지지 않는다. 그래서 모바일 폭은 그 폭의 iframe 안에서 연다.
MOBILE_FRAME = """<!doctype html><meta charset="utf-8"><body style="margin:0">
<iframe src="{src}" width="{w}" height="{h}" style="border:0;display:block"></iframe>
<script>
window.addEventListener('message', function (e) {{
  if (typeof e.data !== 'string' || e.data.indexOf('__fit_result') !== 0) return;
  var pre = document.createElement('pre'); pre.id = '__fit_result';
  pre.textContent = e.data.slice(12); document.body.appendChild(pre);
}});
</script></body>"""


def render(chrome, src_path, html, width, height, frame=False):
    """html을 src_path와 같은 폴더의 임시 파일로 써서 Chrome으로 열고 결과 JSON을 돌려준다.
    frame=True면 폭 width의 iframe에 넣어 연다(창 최소 폭보다 좁은 모바일 폭)."""
    # 상대 경로(styles.css, main.js)를 그대로 쓰려고 같은 폴더에 임시 파일을 만든다
    d = os.path.dirname(os.path.abspath(src_path))
    tmps = []
    try:
        fd, tmp = tempfile.mkstemp(prefix=".fit-", suffix=".html", dir=d)
        tmps.append(tmp)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        open_path, win = tmp, (width, height)
        if frame:
            fd, open_path = tempfile.mkstemp(prefix=".fit-frame-", suffix=".html", dir=d)
            tmps.append(open_path)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(MOBILE_FRAME.format(src=htmllib.escape(os.path.basename(tmp)), w=width, h=height))
            win = (max(width, 500) + 20, height + 20)
        try:
            out = subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                 f"--window-size={win[0]},{win[1]}", "--virtual-time-budget=10000",
                 "--dump-dom", "file://" + os.path.abspath(open_path)],
                capture_output=True, text=True, timeout=120).stdout
        except subprocess.TimeoutExpired:
            sys.exit(f"Chrome이 120초 안에 끝나지 않았다(폭 {width}px 측정 실패).")
    finally:
        for t in tmps:
            os.remove(t)
    m = re.search(r'<pre id="__fit_result">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit(f"측정 결과를 읽지 못했다(폭 {width}px, 페이지 로드 실패).")
    return json.loads(htmllib.unescape(m.group(1)))


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
    ap.add_argument("--mobile-width", type=int, default=390, help="모바일 검사 폭(기본 390px, 높이 844px)")
    ap.add_argument("--no-mobile", action="store_true", help="모바일 폭 가로 밀림 검사를 건너뛴다")
    a = ap.parse_args()

    path = a.target
    if os.path.isdir(path):
        path = os.path.join(path, "index.html")
    if not os.path.isfile(path):
        sys.exit(f"파일이 없다: {path}")
    html = orig = open(path, encoding="utf-8").read()
    chrome = find_chrome(a.chrome)
    # 빌드 전 페이지의 <img src="….svg">: 색 검사용으로 SVG 원문을 미리 읽어 넣는다(file://에서는 fetch가 막힘)
    base = os.path.dirname(os.path.abspath(path))
    svgs = {}
    for src in re.findall(r"""<img\b[^>]*\bsrc\s*=\s*["']([^"']+\.svg)(?:[?#][^"']*)?["']""", html, re.I):
        f = os.path.join(base, htmllib.unescape(src))
        if not re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", src, re.I) and os.path.isfile(f):
            svgs[src] = open(f, encoding="utf-8", errors="replace").read()
    pre = "<script>window.__p2cSvg = " + json.dumps(svgs).replace("</", "<\\/") + ";</script>" if svgs else ""
    html = re.sub(r"</body>", lambda _: pre + PROBE + "</body>", html, count=1, flags=re.I)
    data = render(chrome, path, html, a.width, a.height)
    lay = data.get("lay", [])

    # 모바일 폭: 페이지 전체가 옆으로 밀리는지
    mobile_note = "모바일 검사 건너뜀"
    if not a.no_mobile:
        mhtml = re.sub(r"</body>", lambda _: MOBILE_PROBE + "</body>", orig, count=1, flags=re.I)
        mob = render(chrome, path, mhtml, a.mobile_width, 844, frame=True)
        mw = a.mobile_width
        if abs(mob["inner"] - mw) > 1:
            print(f"주의: 모바일 창 폭이 {mob['inner']}px로 열렸다(요청 {mw}px)")
        mobile_note = f"모바일 {mob['inner']}px 가로 밀림 {max(mob['dw'], 0)}px"
        if mob["dw"] > 2:
            fix = "(좁은 화면 CSS나 상자 폭을 고친다)"
            head = f"모바일({mw}px)에서 페이지가 옆으로 {mob['dw']}px 밀린다: "
            for c in mob["culprits"]:
                where = f"[{c['where']}] " if c["where"] else ""
                more = f" 외 {c['n'] - 1}곳" if c["n"] > 1 else ""
                lay.append(f"{head}{where}{c['key']} \"{c['text']}\"{more} {fix}")
            if not mob["culprits"]:
                lay.append(f"{head}원인 요소를 특정하지 못했다 {fix}")
            elif mob["total"] > len(mob["culprits"]):
                lay.append(f"{head}원인 요소가 {mob['total'] - len(mob['culprits'])}종 더 있다 {fix}")

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
    fig = data.get("fig", [])
    if fig:
        print("\n그림 정렬:")
        for f in fig:
            print("FIG  " + f)
    if lay:
        print("\n배치:")
        for f in lay:
            print("LAY  " + f)
    images = data.get("images", 0)
    if images < MIN_IMAGES:
        print(f"\nIMG  삽화(assets/ 선화)가 {images}개다 (최소 {MIN_IMAGES}개, references/illustrate.py로 만든다)")
    print(f"\n요약: 페이지 {len(data['pages'])}개, 넘침 {over}개, 코넬 아닌 화면 {plain}개, 그림 정렬 문제 {len(fig)}개, 배치 문제 {len(lay)}개, 삽화 {images}개, {mobile_note}")
    sys.exit(1 if over or fig or lay or images < MIN_IMAGES else 0)


if __name__ == "__main__":
    main()
