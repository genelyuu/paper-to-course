#!/usr/bin/env python3
"""상호작용 회귀 검사: 빌드한 강의 HTML을 헤드리스 Chrome에서 실제로 눌러 보며 동작을 확인한다.

사용법:
    python3 check-interact.py <강의 폴더 또는 index.html> [--quick] [--width 1440] [--height 813] [--chrome PATH]

검사 항목(문제마다 'INT'로 시작하는 줄을 내고 종료 코드 1):
  1. 구조: 내비 점 수 = 사이드바 항목 수 = section.module 수, 내비 점의 data-target이 있는지,
     깨진 href="#id", 중복 id, 불러오지 못한 <img>, .katex-error, 수식 렌더링 뒤에도 남은 $…$ 원문,
     html[lang=ko], 외부 네트워크 요청(data:·blob:·file: 아닌 자원).
  2. 문항: data-correct(쉼표·공백 목록)의 값이 모두 보기의 data-value에 있는지, 정답·오답 해설이 둘 다 있는지.
  3. 퀴즈 흐름(모든 .quiz-container, --quick이면 앞 3개): 오답 고르기 → 정답 확인 → '오답' 해설·정답 보기 강조·
     수식 원문 없음·해설이 잘리지 않음, 다시 풀기 → 표시가 모두 지워짐, 정답 고르기 → 정답 확인 → '정답' 해설.
     오답 해설을 펼친 상태에서 쪽의 내용 끝이 쪽 위에서 (창 높이 - 내비 높이) 안에 드는지(최댓값 보고).
  4. 이동: 가운데 내비 점 클릭 → 스크롤이 멈춘 뒤 그 단원이 창 맨 위(±60px, 내비 높이 감안)에 오고
     점·사이드바 항목이 활성. →/← 키와 쪽 넘김 버튼(다음·이전)이 정확히 한 쪽씩 넘기고 쪽 번호가 바뀌는지.
     퀴즈 쪽에서 스페이스바가 정답을 공개하는지.
  5. 툴팁: 첫째·가운데·마지막 .term에 마우스를 올리면 툴팁이 하나 보이고, 창 안에 다 들어오고, 글이 data-definition과 같은지.
  6. 위 과정 중 생긴 자바스크립트 예외·console.error·자원 로드 실패.

방식: Chrome을 --remote-debugging-pipe로 띄우고 DevTools 프로토콜(표준 입출력 파이프, 웹소켓 불필요)로 조종한다.
검사 스크립트는 Page.addScriptToEvaluateOnNewDocument로 넣으므로 강의 폴더에 임시 파일을 만들지 않는다.
내비 점·쪽 넘김 버튼 클릭, 방향키·스페이스바, 용어 위 마우스 올리기는 실제 입력(Input.dispatch*)으로 보낸다.
퀴즈 보기·확인·다시 풀기는 버튼의 click()(onclick 처리기 그대로)을 쓴다. 부드러운 스크롤은 scrollY가 멈출 때까지 기다린다.
창 크기는 Emulation.setDeviceMetricsOverride로 정확히 맞춘다(기본 1440×813 → 허용 쪽 높이 765px).

종료 코드: INT 줄이 하나라도 있으면 1, 아니면 0. 표준 라이브러리와 Chrome만 쓴다(macOS·Linux).
P2C_INT_DEBUG=1이면 보내는 DevTools 명령을 표준 오류로 찍는다(멈춘 단계 찾기).
"""
import argparse, fcntl, json, os, select, shutil, subprocess, sys, tempfile, time

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]

# 페이지 안에서 도는 검사 함수들. Python이 단계별로 부르고, 그 사이에 실제 입력을 보낸다.
TEST = r"""
(function () {
  var R = { int: [], quizzes: 0, questions: 0, quizTested: 0, quizFail: 0, worst: { h: 0, id: '' }, limit: 0, terms: 0, timing: {} };
  var bad = function (m) { R.int.push(m); };
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var NAV = 48, modules = [], cover = null, pages = [], containers = [], dots = [], side = [], terms = [];
  function vis(e) {
    if (!e || !e.isConnected) return false;
    var cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    var r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0;
  }
  function shown(e) { return vis(e) && parseFloat(getComputedStyle(e).opacity) > 0.9; }
  async function waitFor(fn, max) { for (var t = 0; t < (max || 1500); t += 30) { if (fn()) return true; await sleep(30); } return !!fn(); }
  var answers = function (b) { return (b.dataset.correct || '').split(/[,\s]+/).filter(Boolean); };
  function txt(e) { return (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30); }
  function center(e) { var r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height }; }
  // 렌더링되지 않은 $…$ 원문이 든 글자 노드
  function rawTex(root) {
    var found = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: function (n) {
      return n.parentElement && n.parentElement.closest('.katex, pre, code, script, style, svg, textarea') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
    for (var n = w.nextNode(); n; n = w.nextNode()) if (/\$[^$\s][^$]{0,200}\$|\$\$/.test(n.nodeValue)) found.push(n.nodeValue.trim().replace(/\s+/g, ' ').slice(0, 50));
    return found;
  }
  // 스크롤이 멈출 때까지(8회 연속 40ms 동안 scrollY 그대로) 기다린 뒤, 스크롤 처리기(50ms 타이머·rAF·600ms 목표 해제)가 돌게 한다
  async function settle(maxMs) {
    var last = -1, same = 0, t = 0;
    await sleep(80);
    while (t < (maxMs || 12000)) {
      var y = window.scrollY;
      if (Math.abs(y - last) < 0.5) { if (++same >= 8) break; } else { same = 0; last = y; }
      await sleep(40); t += 40;
    }
    await sleep(650);
  }
  function jump(y) { window.scrollTo({ top: y, behavior: 'instant' }); }
  function topOf(el) { return el.getBoundingClientRect().top + window.scrollY - (modules.indexOf(el) >= 0 || el === cover ? 0 : NAV); }
  function pageOf(el) {
    var s = el.closest('.screen'), m = el.closest('.module');
    if (s && m && $$('.screen', m)[0] === s) return m;
    return s || m;
  }
  // 쪽 맨 위: 단원 첫 쪽은 단원 위 + 내비(쪽 넘김이 단원 위를 창 맨 위에 두고 내비가 그 위를 덮는다), 그 밖은 화면 위
  function pageTop(s) {
    var m = s.closest('.module');
    if (m && $$('.screen', m)[0] === s) return m.getBoundingClientRect().top + NAV;
    return s.getBoundingClientRect().top;
  }
  // 쪽 안 실제 내용의 아래 끝: 보이는 글자와 그림·버튼·해설 상자의 아래 끝 중 최댓값(min-height로 늘어난 칸은 무시)
  function contentBottom(root) {
    var b = -Infinity, w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), clipOf = new Map();
    // overflow로 잘려 보이지 않는 글자는 자르는 상자의 아래 끝까지만 센다(잘림은 따로 보고한다)
    function clipBottom(e) {
      if (!e || e === root) return Infinity;
      if (clipOf.has(e)) return clipOf.get(e);
      var v = getComputedStyle(e).overflowY !== 'visible' ? Math.min(e.getBoundingClientRect().bottom, clipBottom(e.parentElement)) : clipBottom(e.parentElement);
      clipOf.set(e, v); return v;
    }
    for (var n = w.nextNode(); n; n = w.nextNode()) {
      if (!n.nodeValue.trim()) continue;
      var p = n.parentElement;
      if (!p || p.closest('.katex-mathml, .sr-only, .visually-hidden') || !vis(p)) continue;
      var rg = document.createRange(), cb = clipBottom(p); rg.selectNodeContents(n);
      [].forEach.call(rg.getClientRects(), function (q) { if (q.width) b = Math.max(b, Math.min(q.bottom, cb)); });
    }
    $$('img, svg, canvas, video, button, input, table, .quiz-feedback.show, .callout, .summary', root).forEach(function (e) {
      if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
      if (vis(e)) b = Math.max(b, e.getBoundingClientRect().bottom);
    });
    return b;
  }
  var pager = function () { return document.querySelector('.pager'); };
  var pos = function () { var b = document.querySelector('.pager .pager-pos b'); return b ? parseInt(b.textContent, 10) : NaN; };

  var T = window.__int = {};
  T.R = R;

  /* 수식 렌더링(DOMContentLoaded + 100ms)과 쪽 배치(+250ms, 글꼴 준비 +300ms)를 기다린 뒤 구조·문항 검사 */
  T.init = async function () {
    var t0 = performance.now();
    NAV = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 48;
    R.limit = Math.round(window.innerHeight - NAV);
    // 가려진 창은 타이머가 느려져 결과를 믿을 수 없다
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') bad('검사 환경: 검사 도중 페이지가 숨겨졌다(visibilityState=hidden). 결과를 믿을 수 없으니 다시 돌리시오'); });
    R.viewport = window.innerWidth + 'x' + window.innerHeight;
    var last = -1, same = 0;
    for (var i = 0; i < 100; i++) {
      var k = document.querySelectorAll('.katex').length;
      if (k === last && (k > 0 || typeof window.renderMathInElement === 'function' || i > 20)) { if (++same >= 5) break; } else { same = 0; last = k; }
      await sleep(100);
    }
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await sleep(800);
    R.timing.settle = Math.round(performance.now() - t0);
    modules = $$('.module'); cover = document.querySelector('.course-cover'); pages = [];
    if (cover) pages.push(cover);
    modules.forEach(function (m) { pages.push(m); $$('.screen', m).forEach(function (s, i) { if (i > 0) pages.push(s); }); });
    dots = $$('.nav-dot'); side = $$('.sidebar-item'); containers = $$('.quiz-container');

    /* 1. 구조 */
    var mods = $$('section.module');
    if (dots.length !== mods.length || side.length !== mods.length)
      bad('구조: 내비 점 ' + dots.length + '개, 사이드바 항목 ' + side.length + '개, 단원(section.module) ' + mods.length + '개로 수가 다르다');
    dots.forEach(function (d, i) { if (!d.dataset.target || !document.getElementById(d.dataset.target)) bad('구조: 내비 점 #' + (i + 1) + '의 data-target "' + (d.dataset.target || '') + '"에 해당하는 요소가 없다'); });
    $$('a[href^="#"]').forEach(function (a) {
      var h = a.getAttribute('href').slice(1), id; try { id = decodeURIComponent(h); } catch (e) { id = h; }
      if (id && !document.getElementById(id)) bad('구조: 깨진 링크 href="#' + id + '" "' + txt(a) + '"');
    });
    var seen = {};
    $$('[id]').forEach(function (e) { seen[e.id] = (seen[e.id] || 0) + 1; });
    Object.keys(seen).filter(function (k) { return seen[k] > 1; }).forEach(function (k) { bad('구조: 중복 id "' + k + '" ' + seen[k] + '번'); });
    $$('img').forEach(function (im) { if (!im.complete || im.naturalWidth === 0) bad('구조: 이미지를 불러오지 못했다 ' + (im.getAttribute('src') || '').slice(0, 80)); });
    var ke = $$('.katex-error');
    if (ke.length) bad('구조: 수식 오류(.katex-error) ' + ke.length + '개, 첫째 "' + txt(ke[0]) + '"');
    var raw = rawTex(document.body);
    if (raw.length) bad('구조: 렌더링되지 않은 수식 원문 ' + raw.length + '곳, 첫째 "' + raw[0] + '"');
    if ((document.documentElement.lang || '') !== 'ko') bad('구조: html lang="' + document.documentElement.lang + '" (ko여야 한다)');
    performance.getEntriesByType('resource').forEach(function (r) {
      if (!/^(data:|blob:|file:)/.test(r.name)) bad('구조: 외부 네트워크 요청 ' + r.name.slice(0, 100));
    });

    /* 2. 문항 */
    R.quizzes = containers.length;
    containers.forEach(function (c, ci) {
      var name = c.id || ('퀴즈 #' + (ci + 1));
      var blocks = $$('.quiz-question-block', c);
      if (!blocks.length) bad('문항: ' + name + '에 .quiz-question-block이 없다');
      if (!c.id) bad('문항: 퀴즈 #' + (ci + 1) + '에 id가 없다(checkQuiz·resetQuiz가 id로 찾는다)');
      blocks.forEach(function (b, qi) {
        R.questions++;
        var q = name + ' ' + (qi + 1) + '번';
        var vals = $$('.quiz-option', b).map(function (o) { return o.dataset.value; });
        var ans = answers(b);
        if (vals.length < 2) bad('문항: ' + q + ' 보기가 ' + vals.length + '개다');
        if (!ans.length) bad('문항: ' + q + ' data-correct가 비었다');
        ans.forEach(function (a) { if (vals.indexOf(a) < 0) bad('문항: ' + q + ' data-correct "' + a + '"와 같은 보기(data-value)가 없다 [' + vals.join(', ') + ']'); });
        if (!(b.dataset.explanationRight || '').trim()) bad('문항: ' + q + ' 정답 해설(data-explanation-right)이 없다');
        if (!(b.dataset.explanationWrong || '').trim()) bad('문항: ' + q + ' 오답 해설(data-explanation-wrong)이 없다');
        if (!b.querySelector('.quiz-feedback')) bad('문항: ' + q + ' .quiz-feedback이 없다');
      });
    });
    return R.int.length;
  };

  /* 3. 퀴즈 흐름 */
  T.quizzes = async function (quick) {
    var tq = performance.now();
    var list = quick ? containers.slice(0, quick) : containers;
    R.quizTested = list.length;
    for (var ci = 0; ci < list.length; ci++) {
      var c = list[ci], name = c.id || ('퀴즈 #' + (ci + 1)), n0 = R.int.length;
      var blocks = $$('.quiz-question-block', c);
      var chk = c.querySelector('.quiz-check-btn'), rst = c.querySelector('.quiz-reset-btn');
      var reset = function () { if (rst) rst.click(); else if (c.id) window.resetQuiz(c.id); };
      if (!chk) { bad('퀴즈: ' + name + '에 정답 확인 버튼(.quiz-check-btn)이 없다'); R.quizFail++; continue; }
      if (!rst) bad('퀴즈: ' + name + '에 다시 풀기 버튼(.quiz-reset-btn)이 없다');
      var scr = c.closest('.screen'), pg = pageOf(c);
      if (pg) { jump(topOf(pg)); await sleep(60); }
      var fbs = blocks.map(function (b) { return b.querySelector('.quiz-feedback'); }).filter(Boolean);
      // (가) 오답
      var hasWrong = blocks.map(function (b) {
        var ans = answers(b), w = $$('.quiz-option', b).filter(function (o) { return ans.indexOf(o.dataset.value) < 0; })[0];
        if (w) w.click();
        return !!w;
      });
      chk.click();
      await waitFor(function () { return fbs.every(shown); });   // max-height·opacity 전환
      await sleep(80);
      blocks.forEach(function (b, qi) {
        var q = name + ' ' + (qi + 1) + '번', f = b.querySelector('.quiz-feedback');
        if (!hasWrong[qi]) return;   // 오답 보기가 없는 문항
        if (!f || !shown(f)) { bad('퀴즈: ' + q + ' 오답을 고르고 확인했는데 해설이 보이지 않는다'); return; }
        if (!/오답/.test(f.textContent)) bad('퀴즈: ' + q + ' 오답 해설에 "오답"이 없다: "' + txt(f) + '"');
        if (!b.querySelector('.quiz-option.correct')) bad('퀴즈: ' + q + ' 오답 뒤 정답 보기가 강조(.correct)되지 않았다');
        if (!b.querySelector('.quiz-option.incorrect')) bad('퀴즈: ' + q + ' 고른 오답에 .incorrect 표시가 없다');
        var rt = rawTex(f); if (rt.length) bad('퀴즈: ' + q + ' 해설에 렌더링되지 않은 수식 원문 "' + rt[0] + '"');
        if ($$('.katex-error', f).length) bad('퀴즈: ' + q + ' 해설에 수식 오류(.katex-error)');
        if (getComputedStyle(f).overflowY !== 'visible' && f.scrollHeight > f.clientHeight + 2) bad('퀴즈: ' + q + ' 오답 해설이 잘린다(내용 ' + f.scrollHeight + 'px, 보이는 높이 ' + f.clientHeight + 'px)');
      });
      if (scr) {
        var h = Math.round(contentBottom(scr) - pageTop(scr));
        if (h > R.worst.h) R.worst = { h: h, id: name };
        if (h > R.limit + 2) bad('퀴즈: ' + name + ' 오답 해설을 펼치면 쪽 내용 끝이 ' + h + 'px로 허용 ' + R.limit + 'px을 넘는다(+' + (h - R.limit) + 'px)');
      }
      // (나) 다시 풀기
      reset();
      await waitFor(function () { return !fbs.some(vis); }, 800);
      if (c.querySelector('.quiz-option.selected, .quiz-option.correct, .quiz-option.incorrect')) bad('퀴즈: ' + name + ' 다시 풀기 뒤에도 선택·정답·오답 표시가 남았다');
      if ($$('.quiz-option', c).some(function (o) { return o.disabled; })) bad('퀴즈: ' + name + ' 다시 풀기 뒤에도 보기가 잠겨 있다');
      if (fbs.some(function (f) { return f.classList.contains('show') || f.textContent.trim() || shown(f); })) bad('퀴즈: ' + name + ' 다시 풀기 뒤에도 해설이 보인다');
      if (c.dataset.revealed) bad('퀴즈: ' + name + ' 다시 풀기 뒤에도 data-revealed가 남았다');
      // (다) 정답
      blocks.forEach(function (b) {
        var a = answers(b)[0] || '', o = $$('.quiz-option', b).filter(function (o) { return o.dataset.value === a; })[0];
        if (o) o.click();
      });
      chk.click();
      await waitFor(function () { return fbs.every(shown); });
      blocks.forEach(function (b, qi) {
        var q = name + ' ' + (qi + 1) + '번', f = b.querySelector('.quiz-feedback');
        if (!f || !shown(f)) { bad('퀴즈: ' + q + ' 정답을 고르고 확인했는데 해설이 보이지 않는다'); return; }
        if (!(/정답/.test(f.textContent) || f.classList.contains('success')) || f.classList.contains('error')) bad('퀴즈: ' + q + ' 정답을 골랐는데 정답 해설이 아니다: "' + txt(f) + '"');
        if (b.querySelector('.quiz-option.incorrect')) bad('퀴즈: ' + q + ' 정답을 골랐는데 .incorrect 표시가 있다');
        if (getComputedStyle(f).overflowY !== 'visible' && f.scrollHeight > f.clientHeight + 2) bad('퀴즈: ' + q + ' 정답 해설이 잘린다(내용 ' + f.scrollHeight + 'px, 보이는 높이 ' + f.clientHeight + 'px)');
      });
      reset();
      await sleep(30);
      if (R.int.length > n0) R.quizFail++;
    }
    R.timing.quiz = Math.round(performance.now() - tq);
    return R.int.length;
  };

  /* 4. 이동 */
  T.settle = settle;
  // 맨 위로 가서 가운데 내비 점의 화면 좌표를 돌려준다
  T.dotPrep = async function () {
    jump(0); await settle();
    if (!dots.length) return null;
    var k = Math.floor(dots.length / 2), d = dots[k];
    if (!d.dataset.target || !document.getElementById(d.dataset.target)) {
      // data-target이 깨진 점은 다른 가운데 점으로(구조 검사에서 이미 보고)
      k = dots.findIndex(function (x) { return x.dataset.target && document.getElementById(x.dataset.target); });
      if (k < 0) return null; d = dots[k];
    }
    var c = center(d); c.k = k; c.vis = vis(d);
    if (!c.vis) d.click();
    return c;
  };
  T.dotCheck = async function (k) {
    await settle();
    var d = dots[k], tg = document.getElementById(d.dataset.target);
    var top = tg.getBoundingClientRect().top, n0 = R.int.length;
    if (top < -60 || top > NAV + 60) bad('이동: 내비 점 #' + (k + 1) + ' 클릭 뒤 단원 "' + tg.id + '" 위가 창 위에서 ' + Math.round(top) + 'px에 있다(-60~' + (NAV + 60) + 'px이어야 한다)');
    if (!d.classList.contains('active')) bad('이동: 내비 점 #' + (k + 1) + ' 클릭 뒤 그 점이 활성(.active)이 아니다');
    var si = document.querySelector('.sidebar-item[href="#' + tg.id + '"]') || side[k];
    if (si && !si.classList.contains('active')) bad('이동: 내비 점 #' + (k + 1) + ' 클릭 뒤 사이드바 항목 "' + txt(si) + '"이 활성이 아니다');
    return R.int.length - n0;
  };
  // 쪽 넘김: 현재 쪽 번호와 버튼 좌표. 마지막 쪽이면 한 쪽 앞으로 옮겨 둔다
  T.pagerPrep = async function () {
    if (!pager() || isNaN(pos())) { bad('이동: 쪽 넘김 막대(.pager .pager-pos)가 없다'); return null; }
    if (pos() >= pages.length || pos() <= 1) { jump(topOf(pages[Math.min(Math.max(1, pages.length - 2), Math.floor(pages.length / 2))])); await settle(); }
    var bs = $$('.pager-btn', pager()), o = { pos: pos(), total: pages.length };
    bs.forEach(function (b) { o[b.dataset.dir === '-1' ? 'prev' : 'next'] = vis(b) ? center(b) : null; });
    return o;
  };
  T.pos = function () { return pos(); };
  T.pagerCheck = async function (p0, delta, how) {
    await settle();
    var p1 = pos();
    if (p1 !== p0 + delta) { bad('이동: ' + p0 + '쪽에서 ' + how + '를 누르니 ' + p1 + '쪽이 되었다(' + (p0 + delta) + '쪽이어야 한다)'); return p1; }
    var p = pages[p1 - 1];
    if (p) {
      var want = modules.indexOf(p) >= 0 || p === cover ? 0 : NAV, top = p.getBoundingClientRect().top;
      if (Math.abs(top - want) > 60) bad('이동: ' + how + ' 뒤 ' + p1 + '쪽 위가 창 위에서 ' + Math.round(top) + 'px에 있다(' + want + '±60px이어야 한다)');
    }
    return p1;
  };
  // 스페이스바: 첫 퀴즈의 쪽으로 옮긴다
  var spaceQuiz = null, spaceIdx = 0;
  T.spacePrep = async function () {
    spaceQuiz = containers.filter(function (c) { return c.id && c.closest('.screen') && !c.dataset.revealed; })[0];
    if (!spaceQuiz || !pager()) return null;
    var pg = pageOf(spaceQuiz); spaceIdx = pages.indexOf(pg) + 1;
    jump(topOf(pg)); await settle();
    if (pos() !== spaceIdx) { bad('이동: 퀴즈 ' + spaceQuiz.id + '의 쪽(' + spaceIdx + '쪽) 위로 옮겼는데 쪽 번호가 ' + pos() + '다'); return null; }
    return { id: spaceQuiz.id, idx: spaceIdx };
  };
  T.spaceState = async function () {
    await sleep(120);
    if (pos() !== spaceIdx) await settle();
    return { revealed: !!spaceQuiz.dataset.revealed, pos: pos() };
  };
  T.spaceCheck = function () {
    var q = spaceQuiz;
    if (!q.dataset.revealed) bad('이동: 스페이스바를 눌러도 퀴즈 ' + q.id + '의 정답이 공개되지 않았다(' + spaceIdx + '쪽 → ' + pos() + '쪽)');
    else $$('.quiz-question-block', q).forEach(function (b, qi) {
      var f = b.querySelector('.quiz-feedback');
      if (!f || !/정답/.test(f.textContent)) bad('이동: 스페이스바로 공개한 ' + q.id + ' ' + (qi + 1) + '번에 정답 해설이 없다');
      if (!b.querySelector('.quiz-option.correct')) bad('이동: 스페이스바로 공개한 ' + q.id + ' ' + (qi + 1) + '번에 정답 표시가 없다');
    });
    window.resetQuiz(q.id);
  };

  /* 5. 툴팁: 첫째·가운데·마지막 용어 */
  T.tipList = function () {
    terms = $$('.term').filter(function (t) { return vis(t); });
    R.terms = terms.length;
    if (!terms.length) return 0;
    terms = [terms[0], terms[Math.floor(terms.length / 2)], terms[terms.length - 1]].filter(function (t, i, a) { return a.indexOf(t) === i; });
    return terms.length;
  };
  T.tipPrep = async function (i) {
    var t = terms[i];
    t.scrollIntoView({ block: 'center', behavior: 'instant' }); await settle(3000);
    // 여러 줄로 갈라진 용어는 첫 줄 상자의 가운데
    var r = t.getClientRects()[0] || t.getBoundingClientRect();
    return { x: r.left + Math.min(r.width / 2, 20), y: r.top + r.height / 2 };
  };
  T.tipCheck = async function (i) {
    var t = terms[i], nm = '"' + txt(t) + '"';
    await waitFor(function () { return $$('.term-tooltip').some(shown); }, 1000);
    var tips = $$('.term-tooltip').filter(shown);
    if (tips.length !== 1) { bad('툴팁: 용어 ' + nm + '에 마우스를 올리니 보이는 툴팁이 ' + tips.length + '개다(1개여야 한다)'); return; }
    var r = tips[0].getBoundingClientRect();
    if (r.left < -0.5 || r.top < -0.5 || r.right > window.innerWidth + 0.5 || r.bottom > window.innerHeight + 0.5)
      bad('툴팁: 용어 ' + nm + '의 툴팁이 창 밖으로 나간다(' + [r.left, r.top, r.right, r.bottom].map(Math.round).join(',') + ', 창 ' + window.innerWidth + 'x' + window.innerHeight + ')');
    if (tips[0].textContent !== t.dataset.definition) bad('툴팁: 용어 ' + nm + '의 툴팁 글이 data-definition과 다르다: "' + txt(tips[0]) + '"');
  };
  T.tipGone = async function () { return waitFor(function () { return !$$('.term-tooltip').some(shown); }, 1000); };
})();
"""


def find_chrome(explicit):
    for c in ([explicit] if explicit else []) + CHROME_CANDIDATES:
        if c and (os.path.isfile(c) or shutil.which(c)):
            return c if os.path.isfile(c) else shutil.which(c)
    sys.exit("Chrome을 찾지 못했다. --chrome으로 경로를 지정하시오.")


class CDP:
    """--remote-debugging-pipe: Chrome은 fd 3에서 명령을 읽고 fd 4에 응답·이벤트를 쓴다(메시지는 NUL로 끝난다)."""

    def __init__(self, chrome, prof):
        cr, self.w = os.pipe()   # 우리가 w에 쓰고 Chrome이 cr(fd 3)에서 읽는다
        self.r, cw = os.pipe()   # Chrome이 cw(fd 4)에 쓰고 우리가 r에서 읽는다
        hi = [fcntl.fcntl(cr, fcntl.F_DUPFD, 10), fcntl.fcntl(cw, fcntl.F_DUPFD, 10)]

        def pre():
            os.dup2(hi[0], 3)
            os.dup2(hi[1], 4)
        self.p = subprocess.Popen(
            [chrome, "--headless=new", "--remote-debugging-pipe", "--disable-gpu", "--hide-scrollbars",
             "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             # 창이 가려지거나 뒤로 가도 타이머·스크롤 처리기가 느려지지 않게(가려지면 visibilityState가 hidden이 된다)
             "--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows",
             "--disable-renderer-backgrounding", "--disable-features=CalculateNativeWinOcclusion",
             "--user-data-dir=" + prof, "about:blank"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            pass_fds=(3, 4), preexec_fn=pre)
        for fd in [cr, cw] + hi:
            os.close(fd)
        self.buf, self.id, self.events, self.session = b"", 0, [], None

    def _read(self, timeout):
        end = time.time() + timeout
        while b"\0" not in self.buf:
            left = end - time.time()
            if left <= 0 or not select.select([self.r], [], [], left)[0]:
                raise TimeoutError
            chunk = os.read(self.r, 1 << 20)
            if not chunk:
                raise EOFError
            self.buf += chunk
        msg, self.buf = self.buf.split(b"\0", 1)
        return json.loads(msg)

    def call(self, method, params=None, timeout=120, session=True):
        if os.environ.get("P2C_INT_DEBUG"):
            print("..", method, json.dumps(params or {}, ensure_ascii=False)[:100], file=sys.stderr, flush=True)
        self.id += 1
        m = {"id": self.id, "method": method, "params": params or {}}
        if session and self.session:
            m["sessionId"] = self.session
        os.write(self.w, json.dumps(m).encode() + b"\0")
        while True:
            msg = self._read(timeout)
            if msg.get("id") == self.id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg)

    def wait_event(self, name, timeout=60):
        end = time.time() + timeout
        while True:
            for i, e in enumerate(self.events):
                if e["method"] == name:
                    return self.events.pop(i)
            msg = self._read(max(0.01, end - time.time()))
            if "method" in msg:
                self.events.append(msg)

    def js(self, expr, timeout=300):
        r = self.call("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True}, timeout=timeout)
        if "exceptionDetails" in r:
            d = r["exceptionDetails"]
            raise RuntimeError("검사 스크립트 오류: " + (d.get("exception", {}).get("description") or d.get("text", "")).split("\n")[0])
        return r.get("result", {}).get("value")

    def click(self, x, y):
        self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        for t in ("mousePressed", "mouseReleased"):
            self.call("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left", "clickCount": 1})

    def key(self, name):
        code, vk, text = {"ArrowRight": ("ArrowRight", 39, ""), "ArrowLeft": ("ArrowLeft", 37, ""), " ": ("Space", 32, " ")}[name]
        down = {"type": "keyDown" if text else "rawKeyDown", "key": name, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
        if text:
            down["text"] = text
        self.call("Input.dispatchKeyEvent", down)
        self.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": name, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk})

    def close(self):
        try:
            self.call("Browser.close", session=False, timeout=5)
        except Exception:
            pass
        try:
            self.p.wait(5)
        except subprocess.TimeoutExpired:
            self.p.kill()
        os.close(self.w)
        os.close(self.r)


def errors_from(events):
    out = []
    for e in events:
        m, p = e["method"], e.get("params", {})
        if m == "Runtime.exceptionThrown":
            d = p.get("exceptionDetails", {})
            desc = (d.get("exception", {}).get("description") or d.get("text") or "").split("\n")[0]
            out.append(f"예외: {desc} ({(d.get('url') or '').split('/')[-1][:40]}:{d.get('lineNumber', 0) + 1})")
        elif m == "Runtime.consoleAPICalled" and p.get("type") in ("error", "assert"):
            args = " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))
            out.append(f"console.{p['type']}: {args[:200]}")
        elif m == "Log.entryAdded" and p.get("entry", {}).get("level") == "error":
            en = p["entry"]
            out.append(f"로그 오류({en.get('source')}): {en.get('text', '')[:160]} {en.get('url', '')[-60:]}".rstrip())
    seen, uniq = set(), []
    for o in out:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    return uniq


def run(cdp, url, a):
    page = next((t for t in cdp.call("Target.getTargets", session=False)["targetInfos"] if t["type"] == "page"), None)
    tid = page["targetId"] if page else cdp.call("Target.createTarget", {"url": "about:blank"}, session=False)["targetId"]
    cdp.session = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True}, session=False)["sessionId"]
    for m in ("Page.enable", "Runtime.enable", "Log.enable"):
        cdp.call(m)
    cdp.call("Page.bringToFront")
    cdp.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
    cdp.call("Emulation.setDeviceMetricsOverride", {"width": a.width, "height": a.height, "deviceScaleFactor": 1, "mobile": False})
    cdp.call("Page.addScriptToEvaluateOnNewDocument", {"source": TEST})
    cdp.call("Page.navigate", {"url": url})
    cdp.wait_event("Page.loadEventFired", 60)
    times = {}
    t = time.time()
    cdp.js("__int.init()")
    cdp.js(f"__int.quizzes({3 if a.quick else 0})")
    times["quiz"] = time.time() - t
    t = time.time()
    # 4. 내비 점(실제 클릭)
    d = cdp.js("__int.dotPrep()")
    if d:
        if d["vis"]:
            cdp.click(d["x"], d["y"])
        cdp.js(f"__int.dotCheck({d['k']})")
    # 쪽 넘김: →, ←, 다음 버튼, 이전 버튼(실제 키·클릭)
    p = cdp.js("__int.pagerPrep()")
    if p:
        for how, delta, act in (("→ 키", 1, "ArrowRight"), ("← 키", -1, "ArrowLeft"), ("다음 쪽 버튼", 1, "next"), ("이전 쪽 버튼", -1, "prev")):
            p0 = cdp.js("__int.pos()")
            if act in ("next", "prev"):
                b = cdp.js("__int.pagerPrep()")
                if not b or not b.get(act):
                    cdp.js(f"__int.R.int.push({json.dumps('이동: ' + how + '이 보이지 않는다')})")
                    continue
                p0 = b["pos"]
                cdp.click(b[act]["x"], b[act]["y"])
            else:
                cdp.key(act)
            cdp.js(f"__int.pagerCheck({p0}, {delta}, {json.dumps(how)})")
        # 스페이스바(실제 키): 퀴즈 쪽에서 앞선 단계를 넘기며 최대 30번
        s = cdp.js("__int.spacePrep()")
        if s:
            for _ in range(30):
                cdp.key(" ")
                st = cdp.js("__int.spaceState()")
                if st["revealed"] or st["pos"] != s["idx"]:
                    break
            cdp.js("__int.spaceCheck()")
    times["nav"] = time.time() - t
    t = time.time()
    # 5. 툴팁(실제 마우스 이동)
    for i in range(cdp.js("__int.tipList()")):
        c = cdp.js(f"__int.tipPrep({i})")
        cdp.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": c["x"], "y": c["y"]})
        cdp.js(f"__int.tipCheck({i})")
        cdp.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 2, "y": a.height - 2})
        cdp.js("__int.tipGone()")
    times["tip"] = time.time() - t
    cdp.call("Runtime.evaluate", {"expression": "0"})   # 남은 이벤트를 받는다
    return cdp.js("__int.R"), times


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--quick", action="store_true", help="퀴즈 흐름을 앞 3개 퀴즈에서만 검사한다")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=813, help="창 높이(기본 813: 허용 쪽 높이 813-48=765px)")
    ap.add_argument("--chrome")
    a = ap.parse_args()

    path = a.target
    if os.path.isdir(path):
        path = os.path.join(path, "index.html")
    if not os.path.isfile(path):
        sys.exit(f"파일이 없다: {path}")
    chrome = find_chrome(a.chrome)
    prof = tempfile.mkdtemp(prefix="p2c-int-")
    t0 = time.time()
    lines, R, times = [], None, {}
    cdp = CDP(chrome, prof)
    try:
        R, times = run(cdp, "file://" + os.path.abspath(path), a)
    except (TimeoutError, EOFError):
        lines.append("Chrome이 응답하지 않는다(검사 실패).")
    except RuntimeError as e:
        lines.append(str(e))
        try:
            R = cdp.js("__int.R", timeout=10)
        except Exception:
            pass
    finally:
        try:
            errs = errors_from(cdp.events)
        except Exception:
            errs = []
        cdp.close()
        shutil.rmtree(prof, ignore_errors=True)
    secs = time.time() - t0

    R = R or {"int": [], "quizzes": 0, "questions": 0, "quizTested": 0, "quizFail": 0, "worst": {}}
    lines = R["int"] + lines + ["오류: " + e for e in errs]
    nav = sum(l.startswith("이동") for l in lines)
    tip = sum(l.startswith("툴팁") for l in lines)
    tm = ", ".join(f"{k} {v:.1f}초" for k, v in times.items())
    print(f"기준: 창 {R.get('viewport', '?')}, 허용 쪽 높이 {R.get('limit', '?')}px, 걸린 시간 {secs:.1f}초" + (f" ({tm})" if tm else ""))
    for l in lines:
        print("INT  " + l)
    w = R.get("worst") or {}
    if w.get("id"):
        print(f"오답 해설을 펼친 쪽의 내용 끝 최댓값: {w['h']}px ({w['id']}, 허용 {R.get('limit')}px)")
    tested = R.get("quizTested", 0)
    q = f"퀴즈 {R['quizzes']}개(문항 {R['questions']}개)" + ("" if tested == R["quizzes"] else f" 중 {tested}개")
    q += " 흐름 " + ("통과" if not R["quizFail"] else f"실패 {R['quizFail']}개")
    if not nav and not tip:
        n = "내비·쪽 넘김·툴팁 통과"
    else:
        n = "내비·쪽 넘김 " + ("통과" if not nav else f"문제 {nav}개") + ", 툴팁 " + ("통과" if not tip else f"문제 {tip}개")
    print(f"요약: {q}, {n}, 상호작용 문제 {len(lines)}개")
    sys.exit(1 if lines else 0)


if __name__ == "__main__":
    main()
