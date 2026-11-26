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
      // 드래그 매칭: 칩을 놓지 않았어도 정답을 공개한다(매칭 확인과 같은 동작)
      for (const el of inCur('.dnd-container', page)) {
        if (el.id && !el.dataset.revealed) { window.checkDnD(el.id); return; }
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

    // 칩을 칸에 놓는다. 수식 마크업(<i>, <sub>)을 그대로 옮기고, 칸에 있던 칩은 되돌리며, 채점 표시는 지운다
    function place(target, chip) {
      const prev = target.dataset.placed;
      if (prev) {
        const old = $(`.dnd-chip[data-answer="${prev}"]`, containerEl);
        if (old) old.classList.remove('placed');
      }
      target.innerHTML      = `<span>${chip.innerHTML}</span>`;
      target.dataset.placed = chip.dataset.answer;
      chip.classList.add('placed');
      chip.classList.remove('selected', 'dragging');
      $$('.dnd-zone-target', containerEl).forEach(t => t.classList.remove('correct-placed', 'incorrect-placed', 'answer-shown'));
    }

    // 끌기가 어려운 환경(트랙패드·키보드)용: 칩을 누른 뒤 칸을 누르면 놓인다
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        if (chip.classList.contains('placed')) return;
        const was = chip.classList.contains('selected');
        chips.forEach(c => c.classList.remove('selected'));
        if (!was) chip.classList.add('selected');
      });
    });

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
        place(target, chip);
      });
      target.addEventListener('click', () => {
        const sel = $('.dnd-chip.selected', containerEl);
        if (sel) place(target, sel);
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
        if (zt) place(zt, chip);
        zones.forEach(z => { const t = $('.dnd-zone-target', z); if (t) t.classList.remove('drag-over'); });
      });
    });
  }

  /* 매칭 확인 = 채점 + 정답 공개. 칩을 다 놓지 않았어도(하나도 놓지 않았어도) 모든 칸에 정답을 보여 준다.
     맞힌 칸: correct-placed / 틀린 칸: 고른 칩에 취소선 + 정답(incorrect-placed) / 빈칸: 정답(answer-shown) */
  window.checkDnD = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    const chipHTML = a => { const c = $(`.dnd-chip[data-answer="${a}"]`, container); return c ? c.innerHTML : a; };
    $$('.dnd-zone', container).forEach(zone => {
      const target = $('.dnd-zone-target', zone);
      if (!target) return;
      const placed = target.dataset.placed, want = zone.dataset.correct;
      target.classList.remove('correct-placed', 'incorrect-placed', 'answer-shown');
      if (placed && placed === want) {
        target.classList.add('correct-placed');
        return;
      }
      const label = `<span><span class="dnd-answer-label">${i18n('correct')}</span> ${chipHTML(want)}</span>`;
      if (placed) {
        target.innerHTML = `<s class="dnd-wrong">${chipHTML(placed)}</s>${label}`;
        target.classList.add('incorrect-placed');
      } else {
        target.innerHTML = label;
        target.classList.add('answer-shown');
      }
    });
    $$('.dnd-chip', container).forEach(c => c.classList.add('placed'));
    container.dataset.revealed = '1';
  };

  window.resetDnD = function (containerId) {
    const container = $('#' + containerId);
    if (!container) return;
    $$('.dnd-zone-target', container).forEach(t => {
      t.textContent = i18n('dropHere');
      delete t.dataset.placed;
      t.classList.remove('correct-placed', 'incorrect-placed', 'answer-shown');
    });
    $$('.dnd-chip', container).forEach(c => c.classList.remove('placed', 'dragging', 'selected'));
    delete container.dataset.revealed;
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
  /* ── 코드 색칠: IDE 토큰 색(Catppuccin, .code-* 클래스)을 자동으로 입힌다 ──
     의사코드 줄(.pseudocode-line)과 모든 코드 칸(pre)에 쓴다. 이미 <span class="code-…">로 칠한 부분,
     KaTeX 결과, $…$가 남은 글자는 건드리지 않는다(수식 렌더링이 뒤에 오므로).
     주석(// -- # %) · 문자열 · 키워드(대문자 제어어, Python·Lean·Cypher·While 키워드) · 함수(이름+괄호)
     · 접두 이름(ex:Thing, :Label) · 숫자 · 연산자(:= ← → ≥ ∧ ∪ 등) */
  const CODE_KEYWORDS = new Set(('INPUT OUTPUT RETURN RETURNS FOR EACH OF IN TO DO END IF THEN ELSE ELIF WHILE REPEAT UNTIL AND OR NOT USING LET SET BREAK CONTINUE FUNCTION PROCEDURE CALL '
    + 'MATCH WHERE WITH OPTIONAL CONTAINS AS ORDER BY LIMIT UNWIND CREATE MERGE DISTINCT DELETE DETACH SELECT FROM ASK CONSTRUCT FILTER PREFIX UNION '
    + 'from import def return if elif else for in while not and or class lambda None True False with as yield pass raise try except assert '
    + 'structure theorem lemma where by fun let have show match then do end skip true false begin od fi inductive instance').split(' '));
  const CODE_RE = new RegExp([
    '((?:\\/\\/|(?:^|(?<=\\s))--\\s|(?:^|(?<=\\s))#\\s|^%).*$)',          // 1 주석
    '("[^"\\n]*"|(?<![A-Za-z0-9_가-힣])\'[^\'\\n]*\')',                    // 2 문자열
    '((?:[A-Za-z_][\\w-]*)?:[A-Za-z_][\\w]*)(?![\\w(])(?!\\s*=)',            // 3 접두 이름·레이블(ex:Thing, v:CVE, :HAS_CWE)
    '([A-Za-z_][A-Za-z0-9_]*(?:-[A-Za-z][A-Za-z0-9_]*)*)(\\s*\\()?',       // 4 이름, 5 여는 괄호
    '(\\d+(?:\\.\\d+)?)',                                                    // 6 숫자
    '(:=|:-|<-|->|<=|>=|!=|==|[←→≥≤≠∧∨¬∪∩∘∈∉⊆⊂∅=+\\-*\\/<>])'               // 7 연산자
  ].join('|'), 'gm');
  const escHTML = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  function tokenizeCode(text, pseudo) {
    let out = '', last = 0, m;
    CODE_RE.lastIndex = 0;
    while ((m = CODE_RE.exec(text))) {
      if (m[0] === '') { CODE_RE.lastIndex++; continue; }
      out += escHTML(text.slice(last, m.index));
      if (m[1]) out += '<span class="code-comment">' + escHTML(m[1]) + '</span>';
      else if (m[2]) out += '<span class="code-string">' + escHTML(m[2]) + '</span>';
      else if (m[3]) out += '<span class="code-property">' + escHTML(m[3]) + '</span>';
      else if (m[4]) {
        const w = m[4];
        // 의사코드 줄 맨 앞의 영어 동사(Deduplicate, Sort …)도 제어어로 본다(줄 번호 '19: ' 뒤 포함)
        const lead = pseudo && /^[A-Z][a-z]+$/.test(w) && /^\s*(\d+:\s*)?$/.test(text.slice(text.lastIndexOf('\n', m.index - 1) + 1, m.index));
        const kw = CODE_KEYWORDS.has(w) || (/^[A-Z]{2,}$/.test(w) && !m[5]) || lead;
        if (kw) out += '<span class="code-keyword">' + w + '</span>' + (m[5] || '');
        else if (m[5]) out += '<span class="code-function">' + w + '</span>' + m[5];
        else out += w;
      }
      else if (m[6]) out += '<span class="code-number">' + m[6] + '</span>';
      else if (m[7]) out += '<span class="code-operator">' + escHTML(m[7]) + '</span>';
      last = CODE_RE.lastIndex;
    }
    return out + escHTML(text.slice(last));
  }
  function colorizeCode(root) {
    if (!root || root.dataset.colored) return;   // 멱등
    root.dataset.colored = '1';
    const pseudo = root.classList.contains('pseudocode-line');
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => (n.parentElement.closest('[class^="code-"], [class*=" code-"], .katex, .katex-display')
        || (n.nodeValue.indexOf('$') >= 0 && !n.parentElement.closest('pre, code')) || !/[A-Za-z0-9:=←→≥≤≠∧∨∪∩∘∈∅+\-*\/<>"']/.test(n.nodeValue))
        ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(n => {
      const html = tokenizeCode(n.nodeValue, pseudo);
      if (html === escHTML(n.nodeValue)) return;
      const t = document.createElement('template');
      t.innerHTML = html;
      n.parentNode.replaceChild(t.content, n);
    });
  }
  const colorizePseudocode = colorizeCode;
  $$('pre').forEach(pre => { if (!pre.closest('svg')) colorizeCode(pre); });

  function initPseudocodeWalkthrough(containerEl) {
    if (!containerEl) return;
    const lines      = $$('.pseudocode-line', containerEl);
    lines.forEach(colorizePseudocode);
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

  /* ── 쪽 배치: 요약 위치를 모든 쪽에서 같게, 고급 쪽의 단서 칸에 용어 정리 ─────────
     1) 단원 첫 쪽(단원 도입 + 첫 화면)도 다른 쪽처럼 요약(.summary)이 화면 맨 아래에 오도록
        첫 화면의 min-height를 "창 높이 - 단원 위에서 첫 화면까지의 거리"로 맞춘다.
     2) 고급 쪽(수식 블록·유도·의사코드·코드 칸이 있거나 용어가 4개 이상인 쪽, 표지 난이도 '고급'인 강의의 모든 쪽,
        data-level="advanced")은 노트 칸의 용어 툴팁으로 단서 칸 아래에 '용어 정리'를 만든다.
        앞 쪽에서 나온 용어도 다시 적는다. 쪽 높이를 넘지 않는 만큼만 넣는다. data-level="basic"이면 넣지 않는다. */
  function initPageLayout() {
    const firstScreens = $$('.module-header + .screen.cornell');
    const navHeight = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 48;
    const courseAdvanced = $$('.course-cover-meta-item').some(e => e.textContent.trim() === '고급');

    function allowedHeight(screen) {
      if (firstScreens.includes(screen)) {
        const mod = screen.closest('.module');
        return window.innerHeight - (screen.getBoundingClientRect().top - mod.getBoundingClientRect().top);
      }
      return window.innerHeight - navHeight();
    }
    function termsOf(notes) {
      const seen = new Set(), out = [];
      $$('.term[data-definition]', notes).forEach(t => {
        const d = t.dataset.definition.trim();
        const k = d.search(/[:：]\s/);
        const name = (k > 0 ? d.slice(0, k) : t.textContent).trim();
        const def = (k > 0 ? d.slice(k + 1) : d).trim();
        const key = name.replace(/\s+/g, '');
        if (!name || seen.has(key)) return;
        seen.add(key);
        out.push([name, def]);
      });
      return out;
    }
    function isAdvanced(screen, notes) {
      const lv = screen.dataset.level;
      if (lv === 'basic') return false;
      if (lv === 'advanced' || courseAdvanced) return true;
      if ($('.katex-display, .math-derivation, .pseudocode-translation, pre', notes)) return true;
      return termsOf(notes).length >= 4;
    }
    let lastKey = '';
    function layout(force) {
      const key = window.innerWidth + 'x' + window.innerHeight;
      if (force !== true && key === lastKey) return;   // 크기가 그대로면 다시 짜지 않는다(깜빡임 방지)
      lastKey = key;
      $$('.cue-terms[data-auto]').forEach(e => e.remove());
      firstScreens.forEach(s => { s.style.minHeight = ''; });
      if (window.innerWidth < 1200) return;   // 한 단으로 접힌 화면은 높이 제한이 없다
      firstScreens.forEach(s => { s.style.minHeight = Math.max(0, Math.floor(allowedHeight(s))) + 'px'; });
      $$('.screen.cornell').forEach(screen => {
        const cue = $(':scope > .cue', screen), notes = $(':scope > .notes', screen);
        if (!cue || !notes || !isAdvanced(screen, notes)) return;
        const listed = new Set($$('dt', cue).map(d => d.textContent.replace(/\s+/g, '')));
        const terms = termsOf(notes).filter(([n]) => !listed.has(n.replace(/\s+/g, '')));
        if (!terms.length) return;
        const box = document.createElement('div');
        box.className = 'cue-terms';
        box.dataset.auto = '1';
        box.innerHTML = '<span class="cue-label">용어 정리</span><dl></dl>';
        const dl = $('dl', box);
        cue.appendChild(box);
        const limit = allowedHeight(screen) + 0.5;
        let n = 0;
        for (const [name, def] of terms) {
          const dt = document.createElement('dt'), dd = document.createElement('dd');
          dt.textContent = name; dd.textContent = def;
          dl.append(dt, dd);
          if (screen.getBoundingClientRect().height > limit) { dt.remove(); dd.remove(); break; }
          n++;
        }
        if (!n) box.remove();
      });
    }
    let timer = null;
    const relayout = () => { clearTimeout(timer); timer = setTimeout(layout, 120); };
    // KaTeX 렌더링(DOMContentLoaded + 100ms) 뒤에, 글꼴이 준비되면 다시
    const first = () => setTimeout(() => layout(true), 250);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', first);
    else first();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => setTimeout(() => layout(true), 300));
    window.addEventListener('resize', relayout);
  }
  initPageLayout();

})();
