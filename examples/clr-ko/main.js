/**
 * PAPER-TO-COURSE — COMPLETE JS ENGINE
 * Copy this file verbatim into the course output directory.
 * Never regenerate it. It handles all interactivity generically.
 *
 * Engines included:
 *  - Navigation & progress bar
 *  - Scroll-triggered reveal animations
 *  - Keyboard navigation
 *  - Glossary tooltips
 *  - Quiz (multiple-choice & scenario)
 *  - Drag-and-drop matching
 *  - Group chat / research dialogue animation
 *  - Data flow / message flow animation
 *  - Architecture diagram
 *  - "Spot the bug" / "Spot the assumption" challenge
 *  - Layer toggle / ablation toggle
 *  - KaTeX auto-render
 *  - Math derivation walkthrough
 *  - Pseudocode walkthrough
 *  - Result comparison
 *  - Research lineage tree
 */
(function () {
  'use strict';

  /* ── HELPERS ──────────────────────────────────────────────── */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.from((ctx || document).querySelectorAll(sel)); }

  /* ── I18N (UI strings; language from <html lang>, default ko) ── */
  const I18N = {
    // ko: EBS 교재 문체 — 표지(정답/오답) + 한다체 해설, 지시는 '~하시오'
    ko: {
      selectFirst: '먼저 답을 고르시오.',
      correct: '정답',
      incorrect: '오답',
      dropHere: '여기에 끌어다 놓으시오',
      step: (n, total) => `${n}단계 / ${total}`,
      clickNextToStart: "'다음'을 눌러 시작하시오.",
      found: '정답',
      notThisLine: '이 줄이 아니다. 다시 찾아보시오.'
    },
    // zh: upstream 원본 문구 보존 (lang="zh*" 일 때만 사용)
    zh: {
      selectFirst: '请先选择一个答案！',
      correct: '正确！',
      incorrect: '不太对。',
      dropHere: '拖放到这里',
      step: (n, total) => `步骤 ${n} / ${total}`,
      clickNextToStart: '点击"下一步"开始',
      found: '找到了！',
      notThisLine: '不是这一行，继续找...'
    },
    en: {
      selectFirst: 'Please choose an answer first!',
      correct: 'Correct!',
      incorrect: 'Not quite.',
      dropHere: 'Drop here',
      step: (n, total) => `Step ${n} / ${total}`,
      clickNextToStart: 'Click "Next" to start',
      found: 'Found it!',
      notThisLine: 'Not this line — keep looking…'
    }
  };
  function i18n(key, ...args) {
    const lang = (document.documentElement.lang || 'ko').toLowerCase().slice(0, 2);
    const dict = I18N[lang] || I18N.ko;
    const v = dict[key] ?? I18N.ko[key];
    return typeof v === 'function' ? v(...args) : v;
  }

  /* Feedback HTML: set content, then render any $…$ / $$…$$ math inside it
     (KaTeX auto-render only runs once at page load, so injected math stays raw otherwise). */
  function setFeedbackHTML(el, html) {
    el.innerHTML = html;
    if (typeof window.renderMathInElement === 'function') {
      try {
        window.renderMathInElement(el, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      } catch (e) { /* leave raw text on failure */ }
    }
  }

  /* ── KATEX AUTO-RENDER ────────────────────────────────────── */
  function initKaTeX() {
    if (typeof renderMathInElement === 'function') {
      renderMathInElement(document.body, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false}
        ],
        throwOnError: false
      });
    }
  }
  // KaTeX is loaded via _base.html with defer + onload, but also try on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initKaTeX, 100);
  });

  /* ── NAVIGATION & PROGRESS BAR ────────────────────────────── */
  const progressBar = $('#progress-bar');
  const navDots     = $$('.nav-dot');
  const modules     = $$('.module');

  function updateProgress() {
    if (!progressBar) return;
    const scrollTop    = window.scrollY;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct          = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    progressBar.style.width = pct + '%';
    progressBar.setAttribute('aria-valuenow', Math.round(pct));
    updateNavDots();
    updateSidebar();
  }

  function updateNavDots() {
    const scrollMid = window.scrollY + window.innerHeight / 2;
    modules.forEach((mod, i) => {
      const dot = navDots[i];
      if (!dot) return;
      const top    = mod.offsetTop;
      const bottom = top + mod.offsetHeight;
      if (scrollMid >= top && scrollMid < bottom) {
        dot.classList.add('active');
        dot.classList.remove('visited');
      } else if (window.scrollY + window.innerHeight > top) {
        dot.classList.remove('active');
        dot.classList.add('visited');
      } else {
        dot.classList.remove('active', 'visited');
      }
    });
  }

  window.addEventListener('scroll', () => requestAnimationFrame(updateProgress), { passive: true });
  // Deferred: updateProgress() → updateSidebar() reads `sidebarItems`, declared further below.
  // A synchronous call here threw "Cannot access 'sidebarItems' before initialization" (upstream bug)
  // and aborted the rest of this file, so quizzes and other widgets never registered.
  setTimeout(updateProgress, 0);

  navDots.forEach(dot => {
    dot.addEventListener('click', () => {
      const target = $('#' + dot.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });

  /* ── PAGE NAVIGATION (방향키·페이지 넘김 버튼) ─────────────────
     페이지 = 표지, 단원(도입 + 첫 화면), 그 밖의 .screen 하나. check-pages.py의 페이지 단위와 같다.
     ←/↑/PageUp: 이전 페이지, →/↓/PageDown: 다음 페이지, Home/End: 처음·끝. */
  function initPager() {
    const pages = [];
    const cover = $('.course-cover');
    if (cover) pages.push(cover);
    modules.forEach(mod => {
      pages.push(mod);
      $$('.screen', mod).forEach((s, i) => { if (i > 0) pages.push(s); });
    });
    if (!pages.length) return;
    const navH = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 48;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const topOf = el => el.getBoundingClientRect().top + window.scrollY - (modules.includes(el) || el === cover ? 0 : navH());

    // 부드러운 스크롤 중에는 목표 쪽수를 기억해 두어, 키를 빠르게/계속 눌러도 한 쪽씩 정확히 넘어가게 한다
    let target = null, targetTimer = 0;
    const clearTarget = () => { target = null; clearTimeout(targetTimer); update(); };
    window.addEventListener('scrollend', clearTarget);

    function currentIndex() {
      if (target !== null) return target;
      // 문서 맨 아래(마지막 쪽이 짧아 위쪽 기준에 닿지 못하는 경우)에서는 마지막 쪽으로 본다
      if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) return pages.length - 1;
      const y = window.scrollY + 8;
      let idx = 0;
      // 표지·단원은 맨 위(top)가, 화면은 내비게이션 높이를 뺀 위치(top-navH)가 기준 — topOf와 같은 값
      pages.forEach((p, i) => { if (topOf(p) <= y) idx = i; });
      return idx;
    }
    function go(i) {
      i = Math.max(0, Math.min(pages.length - 1, i));
      target = i;
      clearTimeout(targetTimer);
      targetTimer = setTimeout(clearTarget, 600);   // scrollend를 지원하지 않는 브라우저 대비
      window.scrollTo({ top: topOf(pages[i]), behavior: reduce ? 'auto' : 'smooth' });
      update();
    }

    const pager = document.createElement('nav');
    pager.className = 'pager';
    pager.setAttribute('aria-label', '페이지 넘김');
    pager.innerHTML = '<span class="pager-hint">방향키: 페이지, 스페이스바: 다음 단계·정답</span>' +
      '<button class="pager-btn" type="button" data-dir="-1" aria-label="이전 페이지">&lsaquo;</button>' +
      '<span class="pager-pos" aria-live="polite"><b>1</b> / ' + pages.length + '</span>' +
      '<button class="pager-btn" type="button" data-dir="1" aria-label="다음 페이지">&rsaquo;</button>';
    document.body.appendChild(pager);
    const [prevBtn, nextBtn] = $$('.pager-btn', pager);
    const pos = $('.pager-pos b', pager);
    prevBtn.addEventListener('click', () => go(currentIndex() - 1));
    nextBtn.addEventListener('click', () => go(currentIndex() + 1));

    function update() {
      const i = currentIndex();
      pos.textContent = i + 1;
      prevBtn.disabled = i === 0;
      nextBtn.disabled = i === pages.length - 1;
      pager.classList.toggle('on-cover', !!cover && i === 0);   // 표지에서는 목차 패널과 겹치므로 숨김
    }
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (ticking) return; ticking = true;
      setTimeout(() => { ticking = false; update(); }, 50);   // rAF는 백그라운드 탭에서 멈추므로 타이머로
    }, { passive: true });
    window.addEventListener('resize', update);
    update();

    /* 페이지 안의 요소인가: 단원은 도입부 + 첫 .screen만 그 쪽에 속한다 */
    function inPage(el, page) {
      if (!page.contains(el)) return false;
      if (!modules.includes(page)) return true;
      return !$$('.screen', page).slice(1).some(s => s.contains(el));
    }
    const inCur = (sel, page) => $$(sel, page).filter(el => inPage(el, page));

    /* 스페이스바: 현재 쪽의 "주 동작"(수식 다음 단계 → 의사코드 다음 줄 → 대화 다음 말풍선 → 다음 전환 버튼·탭 → 정답 공개 → 다음 쪽).
       Shift+Space는 반대로 이전 단계, 더 없으면 이전 쪽 */
    function pageAction(back) {
      const page = pages[currentIndex()];
      if (back) {
        for (const [sel, btn, idxKey] of [['.math-derivation', '.math-prev-btn', 'step'], ['.pseudocode-translation', '.pseudocode-prev-btn', 'line']]) {
          for (const el of inCur(sel, page)) {
            const b = $(btn, el);
            if (b && Number(el.dataset[idxKey] || 0) > 0) { b.click(); return; }
          }
        }
        for (const grp of inCur('.result-metric-toggle, .ablation-tabs, .layer-tabs', page)) {
          const bs = $$('button', grp), i = bs.findIndex(b => b.classList.contains('active'));
          if (i > 0) { bs[i - 1].click(); return; }
        }
        go(currentIndex() - 1);
        return;
      }
      for (const el of inCur('.math-derivation', page)) {
        const n = $$('.math-step', el).length, b = $('.math-next-btn', el);
        if (b && Number(el.dataset.step || 0) < n - 1) { b.click(); return; }
      }
      for (const el of inCur('.pseudocode-translation', page)) {
        const n = $$('.pseudocode-line', el).length, b = $('.pseudocode-next-btn', el);
        if (b && Number(el.dataset.line || -1) < n - 1) { b.click(); return; }
      }
      // 대화창: 다음 말풍선
      for (const el of inCur('.chat-window', page)) {
        if (el.dataset.pending === '1') return;
        const n = $$('.chat-message', el).length, b = $('.chat-next-btn', el);
        if (b && Number(el.dataset.shown || 0) < n) { b.click(); return; }
      }
      // 전환 버튼 묶음(결과 지표 전환, 제거 실험 탭): 활성 버튼 다음 것을 누른다. 마지막이면 넘어간다
      for (const grp of inCur('.result-metric-toggle, .ablation-tabs, .layer-tabs', page)) {
        const bs = $$('button', grp), i = bs.findIndex(b => b.classList.contains('active'));
        if (i >= 0 && i < bs.length - 1) { bs[i + 1].click(); return; }
      }
      for (const el of inCur('.quiz-container', page)) {
        const done = el.dataset.revealed || $$('.quiz-option', el).every(o => o.disabled);
        if (el.id && !done) { window.revealQuiz(el.id); return; }
      }
      go(currentIndex() + 1);
    }

    // keydown 리스너는 이것 하나뿐. 수정키·입력 위젯·가로 스크롤 영역에서는 브라우저 기본 동작에 맡긴다
    document.addEventListener('keydown', e => {
      if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
      const t = e.target;
      if (t.closest && t.closest('input,textarea,select,[contenteditable],[role=slider],[role=listbox],audio,video')) return;
      if (e.key === ' ') { e.preventDefault(); pageAction(e.shiftKey); return; }
      if (e.shiftKey) return;
      const step = { ArrowRight: 1, ArrowDown: 1, PageDown: 1, ArrowLeft: -1, ArrowUp: -1, PageUp: -1 }[e.key];
      if (step) {
        // 가로로 실제 스크롤되는 영역(코드 블록 등) 안에서는 좌우 키를 그대로 둔다
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
          const sc = t.closest && t.closest('pre,.pseudocode-block,.math-block');
          if (sc && sc.scrollWidth > sc.clientWidth) return;
        }
        e.preventDefault(); go(currentIndex() + step); return;
      }
      if (e.key === 'Home') { e.preventDefault(); go(0); }
      if (e.key === 'End') { e.preventDefault(); go(pages.length - 1); }
    });
    // 버튼에 포커스가 있어도 스페이스바가 keyup에서 버튼을 또 누르지 않게 막는다
    document.addEventListener('keyup', e => {
      if (e.key === ' ' && !(e.target.closest && e.target.closest('input,textarea,select,[contenteditable]'))) e.preventDefault();
    });
  }
  initPager();

  /* ── SIDEBAR NAVIGATION ────────────────────────────────────── */
  const sidebarItems = $$('.sidebar-item');
  const sidebarToggle = $('#sidebar-toggle');
  const sidebar = $('#sidebar');
  let sidebarOverlay = null;

  function updateSidebar() {
    const scrollMid = window.scrollY + window.innerHeight / 2;
    modules.forEach((mod, i) => {
      const item = sidebarItems[i];
      if (!item) return;
      const top = mod.offsetTop;
      const bottom = top + mod.offsetHeight;
      if (scrollMid >= top && scrollMid < bottom) {
        item.classList.add('active');
        item.classList.remove('visited');
      } else if (window.scrollY + window.innerHeight > top) {
        item.classList.remove('active');
        item.classList.add('visited');
      } else {
        item.classList.remove('active', 'visited');
      }
    });
  }

  sidebarItems.forEach(item => {
    item.addEventListener('click', () => {
      const target = $(item.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
      if (window.innerWidth <= 1024) closeSidebar();
    });
  });

  function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    if (sidebarToggle) sidebarToggle.setAttribute('aria-expanded', 'true');
    if (!sidebarOverlay) {
      sidebarOverlay = document.createElement('div');
      sidebarOverlay.className = 'sidebar-overlay';
      document.body.appendChild(sidebarOverlay);
      sidebarOverlay.addEventListener('click', closeSidebar);
    }
    sidebarOverlay.classList.add('visible');
  }

  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (sidebarToggle) sidebarToggle.setAttribute('aria-expanded', 'false');
    if (sidebarOverlay) sidebarOverlay.classList.remove('visible');
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    });
  }

  /* ── COVER CTA ─────────────────────────────────────────────── */
  const coverCta = $('.course-cover-cta');
  if (coverCta) {
    coverCta.addEventListener('click', e => {
      e.preventDefault();
      const firstModule = modules[0];
      if (firstModule) firstModule.scrollIntoView({ behavior: 'smooth' });
    });
  }

  /* ── SCROLL-TRIGGERED REVEAL ───────────────────────────────── */
  document.body.classList.add('js-reveal');

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px', threshold: 0 });

  $$('.animate-in').forEach(el => revealObserver.observe(el));

  $$('.stagger-children').forEach(parent => {
    Array.from(parent.children).forEach((child, i) => {
      child.style.setProperty('--stagger-index', i);
    });
  });

  /* ── GLOSSARY TOOLTIPS ─────────────────────────────────────── */
  let activeTooltip = null;

  function positionTooltip(term, tip) {
    const rect     = term.getBoundingClientRect();
    const tipWidth = Math.min(320, Math.max(200, window.innerWidth * 0.8));
    let left = rect.left + rect.width / 2 - tipWidth / 2;
    left = Math.max(8, Math.min(left, window.innerWidth - tipWidth - 8));
    tip.style.left  = left + 'px';
    tip.style.width = tipWidth + 'px';
    document.body.appendChild(tip);
    const tipHeight = tip.offsetHeight;
    if (rect.top - tipHeight - 12 < 0) {
      tip.style.top = (rect.bottom + 8) + 'px';
      tip.classList.add('flip');
    } else {
      tip.style.top = (rect.top - tipHeight - 8) + 'px';
      tip.classList.remove('flip');
    }
  }

  function showTooltip(term, tip) {
    if (activeTooltip && activeTooltip !== tip) {
      activeTooltip.classList.remove('visible');
      activeTooltip.remove();
    }
    positionTooltip(term, tip);
    requestAnimationFrame(() => tip.classList.add('visible'));
    activeTooltip = tip;
  }

  function hideTooltip(tip) {
    tip.classList.remove('visible');
    setTimeout(() => { if (!tip.classList.contains('visible')) tip.remove(); }, 150);
    if (activeTooltip === tip) activeTooltip = null;
  }

  $$('.term').forEach(term => {
    const tip = document.createElement('span');
    tip.className = 'term-tooltip';
    tip.textContent = term.dataset.definition;

    term.addEventListener('mouseenter', () => showTooltip(term, tip));
    term.addEventListener('mouseleave', () => hideTooltip(tip));
    term.addEventListener('click', e => {
      e.stopPropagation();
      tip.classList.contains('visible') ? hideTooltip(tip) : showTooltip(term, tip);
    });
  });

  document.addEventListener('click', () => {
    if (activeTooltip) { activeTooltip.classList.remove('visible'); activeTooltip.remove(); activeTooltip = null; }
  });

  /* ── QUIZ ENGINE ───────────────────────────────────────────── */
  window.selectOption = function (btn) {
    const block = btn.closest('.quiz-question-block');
    $$('.quiz-option', block).forEach(o => o.classList.remove('selected'));
    btn.classList.add('selected');
  };

  window.checkQuiz = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.quiz-question-block', container).forEach(q => {
      const selected  = $('.quiz-option.selected', q);
      const feedback  = $('.quiz-feedback', q);
      if (!feedback) return;
      const correct   = q.dataset.correct;
      const rightExp  = q.dataset.explanationRight  || '';
      const wrongExp  = q.dataset.explanationWrong  || '';

      if (!selected) {
        feedback.textContent = i18n('selectFirst');
        feedback.className = 'quiz-feedback show warning';
        return;
      }
      $$('.quiz-option', q).forEach(o => o.disabled = true);

      if (selected.dataset.value === correct) {
        selected.classList.add('correct');
        setFeedbackHTML(feedback, '<strong>' + i18n('correct') + '</strong> ' + rightExp);
        feedback.className = 'quiz-feedback show success';
      } else {
        selected.classList.add('incorrect');
        const correctBtn = $(`.quiz-option[data-value="${CSS.escape(correct || '')}"]`, q);
        if (correctBtn) correctBtn.classList.add('correct');
        setFeedbackHTML(feedback, '<strong>' + i18n('incorrect') + '</strong> ' + wrongExp);
        feedback.className = 'quiz-feedback show error';
      }
    });
    if ($$('.quiz-question-block', container).every(q => $('.quiz-option.selected', q))) container.dataset.revealed = '1';
  };

  /* 스페이스바용: 고르지 않아도 정답을 바로 공개한다(정답이 여러 개면 모두 표시) */
  window.revealQuiz = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.quiz-question-block', container).forEach(q => {
      const feedback = $('.quiz-feedback', q);
      const answers  = (q.dataset.correct || '').split(/[,\s]+/).filter(Boolean);
      $$('.quiz-option', q).forEach(o => {
        o.classList.remove('selected', 'correct', 'incorrect');
        if (answers.includes(o.dataset.value)) o.classList.add('selected', 'correct');
        o.disabled = true;
      });
      if (!feedback) return;
      setFeedbackHTML(feedback, '<strong>' + i18n('correct') + '</strong> ' + (q.dataset.explanationRight || ''));
      feedback.className = 'quiz-feedback show success';
    });
    container.dataset.revealed = '1';
  };

  window.resetQuiz = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.quiz-option', container).forEach(o => {
      o.classList.remove('selected', 'correct', 'incorrect');
      o.disabled = false;
    });
    $$('.quiz-feedback', container).forEach(f => { f.className = 'quiz-feedback'; f.textContent = ''; });
    container.removeAttribute('data-revealed');
  };

  /* ── DRAG-AND-DROP ENGINE ──────────────────────────────────── */
  function initDnD(containerEl) {
    if (!containerEl) return;
    const chips = $$('.dnd-chip', containerEl);
    const zones = $$('.dnd-zone', containerEl);

    chips.forEach(chip => {
      chip.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', chip.dataset.answer);
        chip.classList.add('dragging');
      });
      chip.addEventListener('dragend', () => chip.classList.remove('dragging'));
    });

    zones.forEach(zone => {
      const target = $('.dnd-zone-target', zone);
      if (!target) return;
      target.addEventListener('dragover',  e => { e.preventDefault(); target.classList.add('drag-over'); });
      target.addEventListener('dragleave', ()  => target.classList.remove('drag-over'));
      target.addEventListener('drop', e => {
        e.preventDefault();
        target.classList.remove('drag-over');
        const answer = e.dataTransfer.getData('text/plain');
        const chip   = $(`.dnd-chip[data-answer="${answer}"]`, containerEl);
        if (!chip) return;
        target.textContent    = chip.textContent;
        target.dataset.placed = answer;
        chip.classList.add('placed');
      });
    });

    chips.forEach(chip => {
      chip.addEventListener('touchstart', e => {
        e.preventDefault();
        const touch = e.touches[0];
        const ghost = chip.cloneNode(true);
        ghost.classList.add('touch-ghost');
        ghost.style.cssText = `position:fixed;z-index:9999;pointer-events:none;left:${touch.clientX - 40}px;top:${touch.clientY - 20}px;`;
        document.body.appendChild(ghost);
        chip._ghost  = ghost;
        chip._answer = chip.dataset.answer;
      }, { passive: false });

      chip.addEventListener('touchmove', e => {
        e.preventDefault();
        const touch = e.touches[0];
        if (chip._ghost) {
          chip._ghost.style.left = (touch.clientX - 40) + 'px';
          chip._ghost.style.top  = (touch.clientY - 20) + 'px';
        }
        zones.forEach(z => { const t = $('.dnd-zone-target', z); if (t) t.classList.remove('drag-over'); });
        const el = document.elementFromPoint(touch.clientX, touch.clientY);
        const zt = el && el.closest('.dnd-zone-target');
        if (zt) zt.classList.add('drag-over');
      }, { passive: false });

      chip.addEventListener('touchend', e => {
        if (chip._ghost) { chip._ghost.remove(); chip._ghost = null; }
        const touch = e.changedTouches[0];
        const el    = document.elementFromPoint(touch.clientX, touch.clientY);
        const zt    = el && el.closest('.dnd-zone-target');
        if (zt) {
          zt.textContent    = chip.textContent;
          zt.dataset.placed = chip._answer;
          chip.classList.add('placed');
        }
        zones.forEach(z => { const t = $('.dnd-zone-target', z); if (t) t.classList.remove('drag-over'); });
      });
    });
  }

  window.checkDnD = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.dnd-zone', container).forEach(zone => {
      const target  = $('.dnd-zone-target', zone);
      if (!target || !target.dataset.placed) return;
      if (target.dataset.placed === zone.dataset.correct) {
        target.classList.add('correct-placed');
      } else {
        target.classList.add('incorrect-placed');
      }
    });
  };

  window.resetDnD = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.dnd-zone-target', container).forEach(t => {
      t.textContent = i18n('dropHere');
      delete t.dataset.placed;
      t.classList.remove('correct-placed', 'incorrect-placed');
    });
    $$('.dnd-chip', container).forEach(c => c.classList.remove('placed', 'dragging'));
  };

  $$('.dnd-container').forEach(el => initDnD(el));

  /* ── GROUP CHAT / RESEARCH DIALOGUE ENGINE ─────────────────── */
  function initChat(containerEl) {
    if (!containerEl) return;
    const messages    = $$('.chat-message', containerEl);
    const typingEl    = $('.chat-typing', containerEl);
    const typingAvEl  = $('#' + containerEl.id + '-typing-avatar') || $('.chat-avatar', typingEl);
    const progressEl  = $('.chat-progress', containerEl);
    let index = 0;

    const actors = {};
    messages.forEach(msg => {
      const sender = msg.dataset.sender;
      const avatar = $('.chat-avatar', msg);
      if (avatar && !actors[sender]) {
        actors[sender] = { initial: avatar.textContent.trim(), style: avatar.style.background };
      }
    });

    function updateProgress() {
      if (progressEl) progressEl.textContent = index + ' / ' + messages.length;
    }

    function showNext() {
      if (index >= messages.length || containerEl.dataset.pending === '1') return;
      containerEl.dataset.pending = '1';
      const msg    = messages[index];
      const sender = msg.dataset.sender;

      if (typingEl && actors[sender]) {
        if (typingAvEl) {
          typingAvEl.textContent       = actors[sender].initial;
          typingAvEl.style.background  = actors[sender].style;
        }
        typingEl.style.display = 'flex';
      }

      setTimeout(() => {
        if (typingEl) typingEl.style.display = 'none';
        msg.style.display = 'flex';
        msg.style.animation = 'fadeSlideUp 0.3s var(--ease-out)';
        index++;
        containerEl.dataset.pending = '';
        containerEl.dataset.shown = index;
        updateProgress();
      }, 800);
    }

    function showAll() {
      const iv = setInterval(() => {
        if (index >= messages.length) { clearInterval(iv); return; }
        showNext();
      }, 1200);
    }

    function reset() {
      index = 0;
      containerEl.dataset.shown = 0;
      messages.forEach(m => { m.style.display = 'none'; m.style.animation = ''; });
      if (typingEl) typingEl.style.display = 'none';
      updateProgress();
    }

    const nextBtn  = $('.chat-next-btn',  containerEl);
    const allBtn   = $('.chat-all-btn',   containerEl);
    const resetBtn = $('.chat-reset-btn', containerEl);
    if (nextBtn)  nextBtn.addEventListener('click',  showNext);
    if (allBtn)   allBtn.addEventListener('click',   showAll);
    if (resetBtn) resetBtn.addEventListener('click', reset);

    updateProgress();
  }

  $$('.chat-window').forEach(el => initChat(el));

  /* ── FLOW ANIMATION ENGINE ─────────────────────────────────── */
  function initFlow(containerEl) {
    if (!containerEl) return;
    const stepsData  = JSON.parse(containerEl.dataset.steps || '[]');
    const labelEl    = $('.flow-step-label', containerEl);
    const progressEl = $('.flow-progress',   containerEl);
    const packet     = $('.flow-packet',     containerEl);
    let step = 0;

    function updateProgress() {
      if (progressEl) progressEl.textContent = i18n('step', step, stepsData.length);
    }

    function animatePacket(fromId, toId) {
      if (!packet) return;
      const fromEl = $('#' + fromId);
      const toEl   = $('#' + toId);
      if (!fromEl || !toEl) return;
      const fromR = fromEl.getBoundingClientRect();
      const toR   = toEl.getBoundingClientRect();
      const contR = containerEl.getBoundingClientRect();
      const fx = fromR.left + fromR.width / 2  - contR.left;
      const fy = fromR.top  + fromR.height / 2 - contR.top;
      const tx = toR.left   + toR.width / 2    - contR.left;
      const ty = toR.top    + toR.height / 2   - contR.top;
      packet.style.setProperty('--packet-from-x', fx + 'px');
      packet.style.setProperty('--packet-from-y', fy + 'px');
      packet.style.setProperty('--packet-to-x',   tx + 'px');
      packet.style.setProperty('--packet-to-y',   ty + 'px');
      packet.style.display    = 'block';
      packet.style.animation  = 'none';
      packet.offsetHeight;
      packet.style.animation  = 'packetMove 0.8s var(--ease-in-out) forwards';
      setTimeout(() => { packet.style.display = 'none'; }, 850);
    }

    function next() {
      if (step >= stepsData.length) return;
      const s = stepsData[step];
      $$('.flow-actor', containerEl).forEach(a => a.classList.remove('active'));
      if (s.highlight) {
        const hEl = $('#' + s.highlight, containerEl) || $('#flow-' + s.highlight);
        if (hEl) hEl.classList.add('active');
      }
      if (s.packet && s.from && s.to) animatePacket('flow-' + s.from, 'flow-' + s.to);
      if (labelEl) labelEl.textContent = s.label || '';
      step++;
      updateProgress();
    }

    function reset() {
      step = 0;
      $$('.flow-actor', containerEl).forEach(a => a.classList.remove('active'));
      if (labelEl) labelEl.textContent = i18n('clickNextToStart');
      if (packet)  packet.style.display = 'none';
      updateProgress();
    }

    const nextBtn  = $('.flow-next-btn',  containerEl);
    const resetBtn = $('.flow-reset-btn', containerEl);
    if (nextBtn)  nextBtn.addEventListener('click',  next);
    if (resetBtn) resetBtn.addEventListener('click', reset);

    updateProgress();
  }

  $$('.flow-animation').forEach(el => initFlow(el));

  /* ── ARCHITECTURE DIAGRAM ──────────────────────────────────── */
  $$('.arch-component').forEach(comp => {
    comp.addEventListener('click', function () {
      const diagram = this.closest('.arch-diagram');
      $$('.arch-component', diagram).forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const descEl = $('.arch-description', diagram);
      if (descEl) descEl.textContent = this.dataset.desc || '';
    });
  });

  /* ── BUG / ASSUMPTION CHALLENGE ────────────────────────────── */
  window.checkBugLine = function (el, isCorrect) {
    const challenge = el.closest('.bug-challenge') || el.closest('.assumption-challenge');
    const feedback  = challenge && ($('.bug-feedback', challenge) || $('.assumption-feedback', challenge));
    if (isCorrect) {
      el.classList.add('correct');
      if (feedback) {
        setFeedbackHTML(feedback, '<strong>' + i18n('found') + '</strong> ' + (el.dataset.explanation || ''));
        feedback.className  = (feedback.className.includes('bug') ? 'bug-feedback' : 'assumption-feedback') + ' show success';
      }
      $$('.bug-line, .assumption-option', challenge).forEach(l => l.style.pointerEvents = 'none');
    } else {
      el.classList.add('incorrect');
      if (feedback) {
        setFeedbackHTML(feedback, (el.dataset.hint || i18n('notThisLine')));
        feedback.className  = (feedback.className.includes('bug') ? 'bug-feedback' : 'assumption-feedback') + ' show error';
      }
      setTimeout(() => {
        el.classList.remove('incorrect');
        if (feedback) feedback.className = feedback.className.includes('bug') ? 'bug-feedback' : 'assumption-feedback';
      }, 1800);
    }
  };

  /* ── ASSUMPTION CHALLENGE (quiz-style) ─────────────────────── */
  window.selectAssumption = function (btn) {
    const block = btn.closest('.assumption-challenge');
    $$('.assumption-option', block).forEach(o => o.classList.remove('selected'));
    btn.classList.add('selected');
  };

  window.checkAssumption = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    const selected = $('.assumption-option.selected', container);
    const feedback = $('.assumption-feedback', container);
    const correct  = container.dataset.correct;

    if (!selected) {
      feedback.textContent = i18n('selectFirst');
      feedback.className = 'assumption-feedback show warning';
      return;
    }
    $$('.assumption-option', container).forEach(o => o.disabled = true);

    if (selected.dataset.value === correct) {
      selected.classList.add('correct');
      setFeedbackHTML(feedback, '<strong>' + i18n('correct') + '</strong> ' + (container.dataset.explanationRight || ''));
      feedback.className = 'assumption-feedback show success';
    } else {
      selected.classList.add('incorrect');
      const correctBtn = $(`.assumption-option[data-value="${correct}"]`, container);
      if (correctBtn) correctBtn.classList.add('correct');
      setFeedbackHTML(feedback, '<strong>' + i18n('incorrect') + '</strong> ' + (container.dataset.explanationWrong || ''));
      feedback.className = 'assumption-feedback show error';
    }
  };

  /* ── LAYER / ABLATION TOGGLE ───────────────────────────────── */
  window.showLayer = function (layerId, btn) {
    const demo = btn ? btn.closest('.layer-demo') || btn.closest('.ablation-demo') : null;
    if (!demo) return;
    $$('.layer, .ablation-layer', demo).forEach(l => l.style.display = 'none');
    $$('.layer-tab, .ablation-tab', demo).forEach(t => t.classList.remove('active'));
    const layer = $('#' + layerId);
    if (layer) layer.style.display = 'block';
    btn.classList.add('active');
  };

  /* ── MATH DERIVATION WALKTHROUGH ───────────────────────────── */
  function initMathDerivation(containerEl) {
    if (!containerEl) return;
    const steps      = $$('.math-step', containerEl);
    const progressEl = $('.math-progress', containerEl);
    let current = 0;

    // Hide all steps except first
    steps.forEach((s, i) => { s.style.display = i === 0 ? 'block' : 'none'; });

    function updateProgress() {
      containerEl.dataset.step = current;   // 스페이스바 단축키가 읽는 현재 단계(0부터)
      if (progressEl) progressEl.textContent = i18n('step', current + 1, steps.length);
    }

    function showStep(idx) {
      steps.forEach(s => s.style.display = 'none');
      if (steps[idx]) {
        steps[idx].style.display = 'block';
        // Re-render KaTeX for newly visible step
        if (typeof renderMathInElement === 'function') {
          renderMathInElement(steps[idx], {
            delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false}
            ],
            throwOnError: false
          });
        }
      }
      updateProgress();
    }

    function next() {
      if (current < steps.length - 1) { current++; showStep(current); }
    }
    function prev() {
      if (current > 0) { current--; showStep(current); }
    }
    function reset() {
      current = 0; showStep(0);
    }

    const nextBtn  = $('.math-next-btn',  containerEl);
    const prevBtn  = $('.math-prev-btn',  containerEl);
    const resetBtn = $('.math-reset-btn', containerEl);
    if (nextBtn)  nextBtn.addEventListener('click',  next);
    if (prevBtn)  prevBtn.addEventListener('click',  prev);
    if (resetBtn) resetBtn.addEventListener('click', reset);

    updateProgress();
  }

  $$('.math-derivation').forEach(el => initMathDerivation(el));

  /* ── PSEUDOCODE WALKTHROUGH ────────────────────────────────── */
  /* ── 의사코드 색칠: IDE 토큰 색(Catppuccin, .code-* 클래스)을 자동으로 입힌다 ──
     이미 <span class="code-…">로 직접 칠한 줄은 건드리지 않는다.
     키워드(대문자 제어어) · 함수(대문자 이름 + 괄호) · 주석(// 뒤) · 숫자 · 연산자 · 문자열 */
  const PSEUDO_KEYWORDS = /^(INPUT|OUTPUT|RETURN|FOR|EACH|OF|IN|TO|DO|END|IF|THEN|ELSE|ELIF|WHILE|REPEAT|UNTIL|AND|OR|NOT|USING|LET|SET|BREAK|CONTINUE|FUNCTION|PROCEDURE)$/;
  const CODE_ESC = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const CODE_SPAN = (cls, t) => '<span class="code-' + cls + '">' + CODE_ESC(t) + '</span>';
  const CIL_KEYWORDS = /^(public|private|family|assembly|static|instance|virtual|specialname|rtspecialname|hidebysig|newslot|abstract|sealed|extends|implements|explicit|sequential|auto|value|enum|extern|class|valuetype|interface|cil|managed|pinned|initonly|literal)$/;
  const CIL_TYPES = /^(void|bool|char|string|object|int|int8|int16|int32|int64|uint8|uint16|uint32|uint64|unsigned|native|float32|float64|typedref)$/;
  const CIL_OPCODE = /^(?:ld(?:arga?|loca?|c|null|ind|s?flda?|ftn|virtftn|token|elema?|len|str|obj)|st(?:arg|loc|ind|s?fld|elem|obj)|call(?:i|virt)?|newobj|newarr|initobj|ret|box|unbox(?:\.any)?|add|sub|mul|div|rem|neg|and|or|xor|shl|shr|br|brtrue|brfalse|beq|bne|bge|bgt|ble|blt|dup|pop|jmp|localloc|cpblk|initblk|castclass|isinst|throw|rethrow|nop|conv|leave|switch|ceq|cgt|clt)(?:\.[a-z0-9]+)*$/;
  const CLIKE_KEYWORDS = /^(abstract|as|async|await|base|break|case|catch|class|const|continue|default|delegate|do|else|enum|event|explicit|extends|extern|false|final|finally|fixed|for|foreach|goto|if|implements|implicit|import|in|interface|internal|is|let|lock|namespace|new|null|operator|out|override|package|params|private|protected|public|readonly|record|ref|return|scoped|sealed|stackalloc|static|struct|super|switch|this|throw|throws|true|try|typeof|unsafe|using|var|virtual|void|volatile|while|yield)$/;
  const CLIKE_TYPES = /^(bool|boolean|byte|char|decimal|double|float|int|long|nint|object|sbyte|short|string|uint|ulong|ushort)$/;
  const SCHEME_KEYWORDS = /^(define|lambda|let|let\*|letrec|if|cond|else|begin|set!|quote|and|or|when|unless|do)$/;

  /* 코드 덩어리의 언어를 고른다: data-lang이 있으면 그것, 없으면 내용으로 추정 */
  function detectCodeLang(el, text) {
    const host = el.closest('[data-lang]');
    if (host) return host.dataset.lang;
    if (/^\s*;|\(define\b/m.test(text)) return 'scheme';
    if (/^\s*\.(method|locals|class|assembly|maxstack|field|module)\b/m.test(text) ||
        /(^|\s)(ldarga?|ldloca?|ldind|stind|stloc|starg|callvirt|newobj|initobj|ldfld|stfld|ldc|tail\.)\b/m.test(text)) return 'cil';
    if (/\b(INPUT|OUTPUT|RETURN|FOR EACH|IF|THEN|WHILE)\b/.test(text) && !/[;{}]/.test(text)) return 'pseudo';
    return 'clike';
  }

  /* 텍스트 한 덩어리를 언어 규칙으로 토큰화해 HTML 문자열을 돌려준다 */
  function tokenizeCode(text, lang) {
    let re, out = '', last = 0, m;
    if (lang === 'cil') {
      // 1 주석 2 문자열 3·4 Type::member 5 지시어(.method) 6 낱말(+괄호) 7 숫자 8 연산자
      re = /(\/\/.*$)|("[^"]*")|([A-Za-z_][\w]*)::(\.?[A-Za-z_][\w]*)|((?<![\w.])\.[a-z][a-z_]*)|([A-Za-z_][\w]*(?:\.[A-Za-z0-9]+)*\.?)(\s*\()?|(\b0x[0-9A-Fa-f]+\b|\b\d+(?:\.\d+)?\b)|([&*=+\-])/gm;
      while ((m = re.exec(text))) {
        out += CODE_ESC(text.slice(last, m.index));
        if (m[1]) out += CODE_SPAN('comment', m[1]);
        else if (m[2]) out += CODE_SPAN('string', m[2]);
        else if (m[3]) out += CODE_SPAN('type', m[3]) + CODE_SPAN('operator', '::') + CODE_SPAN('function', m[4]);
        else if (m[5]) out += CODE_SPAN(m[5] === '.ctor' ? 'function' : 'directive', m[5]);
        else if (m[6]) {
          const w = m[6], paren = m[7] || '';
          if (w === 'tail.' || CIL_OPCODE.test(w)) out += CODE_SPAN('opcode', w) + CODE_ESC(paren);
          else if (CIL_KEYWORDS.test(w)) out += CODE_SPAN('keyword', w) + CODE_ESC(paren);
          else if (CIL_TYPES.test(w)) out += CODE_SPAN('type', w) + CODE_ESC(paren);
          else if (paren) out += CODE_SPAN('function', w) + CODE_ESC(paren);
          else out += CODE_ESC(w);
        }
        else if (m[8]) out += CODE_SPAN('number', m[8]);
        else if (m[9]) out += CODE_SPAN('operator', m[9]);
        last = re.lastIndex;
      }
    } else if (lang === 'scheme') {
      // 1 주석 2 문자열 3 인용 기호 4 여는 괄호 뒤 낱말 5 숫자 6 연산자
      re = /(;.*$)|("[^"]*")|('[\w\-!?*]+)|\((\s*[A-Za-z_!?*<>=+\-][\w\-!?*<>=]*)|(\b\d+(?:\.\d+)?\b)/gm;
      while ((m = re.exec(text))) {
        out += CODE_ESC(text.slice(last, m.index));
        if (m[1]) out += CODE_SPAN('comment', m[1]);
        else if (m[2] || m[3]) out += CODE_SPAN('string', m[2] || m[3]);
        else if (m[4]) {
          const w = m[4].trim(), lead = m[4].slice(0, m[4].length - w.length);
          const cls = SCHEME_KEYWORDS.test(w) ? 'keyword' : (/^[=<>+\-*\/]+$/.test(w) ? 'operator' : 'function');
          out += '(' + CODE_ESC(lead) + CODE_SPAN(cls, w);
        }
        else if (m[5]) out += CODE_SPAN('number', m[5]);
        last = re.lastIndex;
      }
    } else if (lang === 'pseudo') {
      re = /(\/\/.*$)|("[^"]*")|((?<![A-Za-z0-9_가-힣])'[^']*')|([A-Za-z_][A-Za-z0-9_]*)(\s*\()?|(\d+(?:\.\d+)?)|(<=|>=|!=|==|[=+\-*\/<>←])/gm;
      while ((m = re.exec(text))) {
        out += CODE_ESC(text.slice(last, m.index));
        if (m[1]) out += CODE_SPAN('comment', m[1]);
        else if (m[2] || m[3]) out += CODE_SPAN('string', m[2] || m[3]);
        else if (m[4]) {
          if (PSEUDO_KEYWORDS.test(m[4])) out += CODE_SPAN('keyword', m[4]) + CODE_ESC(m[5] || '');
          else if (m[5]) out += CODE_SPAN('function', m[4]) + CODE_ESC(m[5]);
          else out += CODE_ESC(m[4]);
        }
        else if (m[6]) out += CODE_SPAN('number', m[6]);
        else if (m[7]) out += CODE_SPAN('operator', m[7]);
        last = re.lastIndex;
      }
    } else {
      // C#·Java: 1 주석 2 문자열 3 문자 4 낱말(+괄호) 5 숫자 6 연산자
      re = /(\/\/.*$)|("(?:[^"\\]|\\.)*")|('(?:[^'\\]|\\.)')|([A-Za-z_][\w]*)(\s*\()?|(\b0x[0-9A-Fa-f]+\b|\b\d+(?:\.\d+)?[fFdDmML]?\b)|(=>|==|!=|<=|>=|&&|\|\||\+\+|--|[=+\-*\/%<>!?:&|])/gm;
      while ((m = re.exec(text))) {
        out += CODE_ESC(text.slice(last, m.index));
        if (m[1]) out += CODE_SPAN('comment', m[1]);
        else if (m[2] || m[3]) out += CODE_SPAN('string', m[2] || m[3]);
        else if (m[4]) {
          const w = m[4], paren = m[5] || '';
          if (CLIKE_KEYWORDS.test(w)) out += CODE_SPAN('keyword', w) + CODE_ESC(paren);
          else if (CLIKE_TYPES.test(w)) out += CODE_SPAN('type', w) + CODE_ESC(paren);
          else if (paren) out += CODE_SPAN('function', w) + CODE_ESC(paren);
          else if (/^[A-Z]/.test(w)) out += CODE_SPAN('type', w);
          else out += CODE_ESC(w);
        }
        else if (m[6]) out += CODE_SPAN('number', m[6]);
        else if (m[7]) out += CODE_SPAN('operator', m[7]);
        last = re.lastIndex;
      }
    }
    return out + CODE_ESC(text.slice(last));
  }

  /* 요소 안의 텍스트 노드만 색칠한다. 직접 칠한 <span class="code-…">와 수식은 건드리지 않는다(멱등) */
  function highlightCode(el, lang) {
    if (!el || el.dataset.colored) return;
    el.dataset.colored = '1';
    const text = el.textContent;
    if (text.indexOf('$') >= 0 && /\$[^$]+\$/.test(text)) return;   // 수식이 섞인 줄
    lang = lang || detectCodeLang(el, text);
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
      acceptNode: n => (n.parentElement.closest('[class^="code-"], [class*=" code-"], .katex') &&
                        n.parentElement.closest('[class^="code-"], [class*=" code-"], .katex') !== el)
                       ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(n => {
      if (!n.nodeValue.trim()) return;
      const tpl = document.createElement('template');
      tpl.innerHTML = tokenizeCode(n.nodeValue, lang);
      n.parentNode.replaceChild(tpl.content, n);
    });
  }
  function colorizePseudocode(line, lang) { highlightCode(line, lang); }

  function initPseudocodeWalkthrough(containerEl) {
    if (!containerEl) return;
    const lines      = $$('.pseudocode-line', containerEl);
    const codeLang = detectCodeLang(containerEl, lines.map(l => l.textContent).join('\n'));
    lines.forEach(l => colorizePseudocode(l, codeLang));
    const explLines  = $$('.pe', containerEl);
    const progressEl = $('.pseudocode-progress', containerEl);
    let current = -1;

    function updateProgress() {
      containerEl.dataset.line = current;   // 스페이스바 단축키가 읽는 현재 줄(-1이면 시작 전)
      if (progressEl) progressEl.textContent = (current + 1) + ' / ' + lines.length;
    }

    function highlightLine(idx) {
      lines.forEach(l => l.classList.remove('highlighted'));
      explLines.forEach(l => l.classList.remove('active'));
      if (lines[idx]) {
        lines[idx].classList.add('highlighted');
      }
      if (explLines[idx]) {
        explLines[idx].classList.add('active');
      }
      updateProgress();
    }

    function next() {
      if (current < lines.length - 1) { current++; highlightLine(current); }
    }
    function prev() {
      if (current > 0) { current--; highlightLine(current); }
    }
    function reset() {
      current = -1;
      lines.forEach(l => l.classList.remove('highlighted'));
      explLines.forEach(l => l.classList.remove('active'));
      updateProgress();
    }

    const nextBtn  = $('.pseudocode-next-btn',  containerEl);
    const prevBtn  = $('.pseudocode-prev-btn',  containerEl);
    const resetBtn = $('.pseudocode-reset-btn', containerEl);
    if (nextBtn)  nextBtn.addEventListener('click',  next);
    if (prevBtn)  prevBtn.addEventListener('click',  prev);
    if (resetBtn) resetBtn.addEventListener('click', reset);

    // 코드 줄 i와 설명 줄 i의 높이를 맞춰 두 열의 행이 같은 y에서 시작하게 한다(2단일 때만)
    const blockEl = $('.pseudocode-block', containerEl);
    const explEl  = $('.pseudocode-explanation', containerEl);
    function alignRows() {
      if (!blockEl || !explEl) return;
      const pairs = [[$('.translation-label', blockEl), $('.translation-label', explEl)]];
      lines.forEach((l, i) => pairs.push([l, explLines[i]]));
      pairs.forEach(([a, b]) => { if (a) a.style.minHeight = ''; if (b) b.style.minHeight = ''; });
      const sideBySide = Math.abs(blockEl.getBoundingClientRect().top - explEl.getBoundingClientRect().top) < 2;
      if (!sideBySide) return;
      pairs.forEach(([a, b]) => {
        if (!a || !b) return;
        const h = Math.max(a.getBoundingClientRect().height, b.getBoundingClientRect().height);
        a.style.minHeight = b.style.minHeight = h + 'px';
      });
    }
    alignRows();
    window.addEventListener('resize', alignRows);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(alignRows);

    updateProgress();
  }

  $$('.pseudocode-translation').forEach(el => initPseudocodeWalkthrough(el));
  // 일반 코드 블록(<pre><code>)도 같은 규칙으로 색칠한다
  $$('pre > code').forEach(el => highlightCode(el));

  /* ── RESULT COMPARISON ─────────────────────────────────────── */
  function initResultComparison(containerEl) {
    if (!containerEl) return;
    const metricBtns = $$('.result-metric', containerEl);
    const allBars    = $$('.result-bar', containerEl);

    function showMetric(metricName) {
      metricBtns.forEach(b => b.classList.remove('active'));
      const activeBtn = $(`.result-metric[data-metric="${metricName}"]`, containerEl);
      if (activeBtn) activeBtn.classList.add('active');

      allBars.forEach(bar => {
        const value = bar.dataset[metricName] || bar.dataset.value || '0';
        const fill  = $('.result-fill', bar);
        const valEl = $('.result-value', bar);
        // data-unit (default '%') and data-max (default 100) on .result-comparison
        // let unitless metrics such as BLEU be shown on their own scale.
        const unit = containerEl.dataset.unit !== undefined ? containerEl.dataset.unit : '%';
        const max  = parseFloat(containerEl.dataset.max) || 100;
        const pct  = Math.max(0, Math.min(100, (parseFloat(value) || 0) / max * 100));
        if (fill) fill.style.width = pct + '%';
        if (valEl) valEl.textContent = value + unit;
      });
    }

    metricBtns.forEach(btn => {
      btn.addEventListener('click', () => showMetric(btn.dataset.metric));
    });

    // Initialize with first metric
    if (metricBtns.length > 0) {
      showMetric(metricBtns[0].dataset.metric);
    }
  }

  $$('.result-comparison').forEach(el => initResultComparison(el));

  /* ── RESEARCH LINEAGE TREE ─────────────────────────────────── */
  $$('.lineage-node').forEach(node => {
    node.addEventListener('click', function () {
      const tree = this.closest('.lineage-tree');
      // Toggle expanded state
      const wasExpanded = this.classList.contains('expanded');
      $$('.lineage-node', tree).forEach(n => n.classList.remove('expanded'));
      if (!wasExpanded) {
        this.classList.add('expanded');
      }
      // Show detail in a description area if present
      const descEl = $('.lineage-description', tree);
      if (descEl) {
        descEl.textContent = wasExpanded ? '' : (this.dataset.detail || '');
      }
    });
  });

})();
