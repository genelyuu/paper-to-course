#!/usr/bin/env python3
"""scaffold.py: 강의의 공통 레이아웃(머리·꼬리·코넬 쪽)을 references/templates/의 틀로 찍어 낸다.

레이아웃은 손으로 쓰지 않는다. 모듈 작성자는 쪽마다 .notes 안의 본문만 채운다.
  머리(header) : references/_base.html (내비·사이드바) + templates/nav.html (단원별 점·목차 줄)
  꼬리(footer) : references/_footer.html
  단원         : templates/module.html (단원 머리말 + 쪽들)
  코넬 쪽      : templates/screen.html (.cue | .notes / .summary)
  단서 칸      : templates/cue-callout.html (학습 목표·배경 지식·핵심 정리), templates/cue-questions.html (핵심 질문)
  확인 문제    : templates/quiz.html, templates/quiz-question.html (쪽당 최대 2문항)

사용법
  python3 -I scaffold.py init    <course-dir> <spec.json> [--force]   자산 복사 + _base.html + 모듈 뼈대
  python3 -I scaffold.py base    <course-dir> <spec.json>             _base.html만 다시 만든다(제목·색·목차가 바뀔 때)
  python3 -I scaffold.py modules <course-dir> <spec.json> [--force]   모듈 뼈대만 만든다(있는 파일은 --force 없이는 두지 않는다)
  python3 -I scaffold.py todo    <course-dir>                          남은 "[작성 필요: …]" 자리를 보여 준다(0개여야 빌드)

spec.json 형식은 templates/course.example.json을 본다. 빠진 글은 "[작성 필요: …]"로 채워 눈에 띄게 남긴다.
파일을 쓰기 전에 spec 전체를 검사하고, 틀린 곳이 있으면 하나도 쓰지 않고 멈춘다.
  - quiz[].options는 2~5개, quiz[].answer는 1~선택지 수의 정수(빠지면 data-correct와 정답 해설 앞 기호에 빈자리를 남긴다).
  - quiz_per_page는 1 또는 2(기본 2), 또는 쪽마다 문항 수를 적은 목록(각 1~2, 합 = 문항 수).
  - corner_style은 "outline" 또는 "filled". 기본은 확인 문제·개념 체크가 outline, 나머지 코너는 filled
    (interactive-elements.md "코너 이름표"). 확인 문제 쪽은 모듈 키 quiz_corner_style로 바꾼다.

필드별 이스케이프 규칙
  일반 글(HTML 아님)  : title(강의 제목), nav_tooltip, corner
      → 모두 이스케이프한다. "&", "<", ">"는 문자 그대로 보인다(속성에서는 '"'·"'"도).
  인라인 HTML         : 모듈 title·label·subtitle, objectives, screens[].heading·paper_ref·questions·summary,
                        takeaways, quiz_titles, quiz_summaries, quiz_cues, quiz[].q·options
      → <i class="mi">, <sub>, $…$ 등을 그대로 쓴다. 엔티티가 아닌 "&"는 "&amp;"로, 태그를 열지 않는 "<"
        (뒤가 영문자·"/"·"!"가 아닌 것, 예: "a < b", "<보기>")는 "&lt;"로 바꾼다. 이미 쓴 엔티티는 그대로 둔다.
        "<" 뒤에 영문자가 오는 글(예: 수식 "$a<b$")은 태그로 읽히므로 "&lt;"나 "\\lt"로 쓴다.
  HTML 그대로         : screens[].notes (아무것도 바꾸지 않는다)
  속성 안 HTML        : quiz[].right·wrong (main.js가 속성 값을 innerHTML로 넣는다) → 값 전체를 속성용으로 한 번 이스케이프
                        ("&"→"&amp;", "<"→"&lt;", '"'→"&quot;"). 글자 그대로의 "<보기>"는 값에 "&lt;보기&gt;"로 쓴다.
  내비 점의 data-tooltip·aria-label은 nav_tooltip(없으면 label, 없으면 title)에서 태그를 뺀 글이다.
  사이드바 글은 label(없으면 title)이다.
표준 라이브러리만 쓴다.
"""
import html, json, os, re, shutil, sys, textwrap

REF = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(REF, 'templates')
TODO = '[작성 필요: {}]'
CIRCLED = '①②③④⑤'
LETTERS = 'abcde'
ACCENTS = {  # 교과 색 프리셋: accent / hover / light / muted (design-system.md "교과 색 프리셋")
    'blue':   ('#1F6FB2', '#185A92', '#E8F1FA', '#6FA3D3'),
    'green':  ('#1B7A50', '#145F3E', '#E6F4EC', '#6BB592'),
    'purple': ('#6B4FA8', '#563F88', '#F0ECF8', '#A08ECB'),
    'orange': ('#B85C0F', '#964A0B', '#FCEFE3', '#E0A06A'),
}
OUTLINE_CORNERS = ('확인 문제', '개념 체크')  # interactive-elements.md: 이 둘은 테두리만(outline)
CORNER_STYLES = ('outline', 'filled')
QUIZ_PER_PAGE = 2  # 기본값이자 상한(쪽 맞춤 규칙: 한 페이지 최대 2문항)
COPY = ['styles.css', 'main.js', '_footer.html', 'build.sh', 'build.py']


def tpl(name):
    with open(os.path.join(TPL, name), encoding='utf-8') as f:
        return f.read()


def tpl_ref(name):
    with open(os.path.join(REF, name), encoding='utf-8') as f:
        return f.read()


def render(t, **kw):
    return re.sub(r'\{\{(\w+)\}\}', lambda m: str(kw[m.group(1)]), t)


def nav_templates():
    lines = [l for l in tpl('nav.html').splitlines() if l.strip() and not l.lstrip().startswith('<!--')]
    return lines[0], lines[1]


# ── 이스케이프(규칙은 맨 위 설명) ──────────────────────────
_BARE_AMP = re.compile(r'&(?!(?:[A-Za-z][A-Za-z0-9]*|#[0-9]+|#[xX][0-9A-Fa-f]+);)')
_TAG = re.compile(r'</?[A-Za-z][^<>]*>|<!--.*?-->', re.S)


def text(s):
    """일반 글 → 글 자리(text node)."""
    return html.escape(str(s), quote=False)


def attr(s):
    """일반 글 → 속성 값."""
    return html.escape(str(s), quote=True)


def inline(s):
    """인라인 HTML → 글 자리. 태그와 엔티티는 두고, 홀로 선 '&'와 태그가 아닌 '<'만 바꾼다."""
    s = _BARE_AMP.sub('&amp;', str(s))
    s = re.sub(r'<(?![A-Za-z/!])([^<>]*)>', r'&lt;\1&gt;', s)  # "<보기>" → "&lt;보기&gt;"
    return re.sub(r'<(?![A-Za-z/!])', '&lt;', s)


def plain(s):
    """인라인 HTML → 태그를 뺀 일반 글(엔티티는 풀어 둔다)."""
    return html.unescape(_TAG.sub('', inline(s)))


def todo(what):
    return TODO.format(what)


def indent(block, n):
    pad = ' ' * n
    block = textwrap.dedent(block.strip('\n'))
    return '\n'.join(pad + l if l.strip() else l for l in block.splitlines())


# ── 검사(파일을 쓰기 전에 spec 전체) ───────────────────────
def module_name(i, m):
    return '%02d-%s' % (i, m.get('slug', 'module%d' % i)) if isinstance(m, dict) else '%02d' % i


def quiz_groups(m):
    """확인 문제를 쪽마다 나눈 문항 수 목록."""
    n = len(m.get('quiz') or [])
    per = m.get('quiz_per_page', QUIZ_PER_PAGE)
    if isinstance(per, list):
        return per
    return [min(per, n - c) for c in range(0, n, per)]


def validate(spec):
    errs = []
    if not isinstance(spec, dict):
        return ['spec 맨 위는 객체({…})여야 한다.']
    if not isinstance(spec.get('title'), str) or not spec['title'].strip():
        errs.append('강의 제목(title)이 없다.')
    if spec.get('accent', 'blue') not in ACCENTS:
        errs.append('교과 색(accent) %r은 쓸 수 없다. %s 중 하나를 쓴다.' % (spec.get('accent'), '·'.join(ACCENTS)))
    mods = spec.get('modules')
    if not isinstance(mods, list) or not mods:
        errs.append('모듈 목록(modules)이 비었다.')
        return errs
    for i, m in enumerate(mods):
        where = '모듈 %s' % module_name(i, m)
        if not isinstance(m, dict):
            errs.append('%s: 모듈은 객체({…})여야 한다.' % where)
            continue
        if not isinstance(m.get('title'), str) or not m['title'].strip():
            errs.append('%s: 단원 제목(title)이 없다.' % where)
        for k in ('label', 'nav_tooltip'):
            if k in m and not isinstance(m[k], str):
                errs.append('%s: %s는 문자열이어야 한다.' % (where, k))
        for s_i, s in enumerate(m.get('screens') or []):
            if not isinstance(s, dict):
                errs.append('%s 화면 %d: 화면은 객체({…})여야 한다.' % (where, s_i + 1))
            elif 'corner_style' in s and s['corner_style'] not in CORNER_STYLES:
                errs.append('%s 화면 %d: corner_style %r은 쓸 수 없다. "outline" 또는 "filled"를 쓴다.'
                            % (where, s_i + 1, s['corner_style']))
        if 'quiz_corner_style' in m and m['quiz_corner_style'] not in CORNER_STYLES:
            errs.append('%s: quiz_corner_style %r은 쓸 수 없다. "outline" 또는 "filled"를 쓴다.' % (where, m['quiz_corner_style']))
        quiz = m.get('quiz') or []
        if not isinstance(quiz, list):
            errs.append('%s: quiz는 목록이어야 한다.' % where)
            continue
        for k, q in enumerate(quiz, 1):
            qw = '%s 확인 문제 %d번' % (where, k)
            if not isinstance(q, dict):
                errs.append('%s: 문항은 객체({…})여야 한다.' % qw)
                continue
            opts = q.get('options')
            n_opts = 5
            if opts is not None:
                if not isinstance(opts, list) or not all(isinstance(o, str) for o in opts):
                    errs.append('%s: 선택지(options)는 문자열 목록이어야 한다.' % qw)
                elif not 2 <= len(opts) <= 5:
                    errs.append('%s: 선택지(options)는 2~5개여야 한다(지금 %d개).' % (qw, len(opts)))
                else:
                    n_opts = len(opts)
            if 'answer' in q:
                a = q['answer']
                if isinstance(a, bool) or not isinstance(a, int):
                    errs.append('%s: 정답 번호(answer)는 정수여야 한다(지금 %r).' % (qw, a))
                elif not 1 <= a <= n_opts:
                    errs.append('%s: 정답 번호(answer) %d가 선택지 범위 1~%d를 벗어난다.' % (qw, a, n_opts))
            for key in ('right', 'wrong', 'q'):
                if key in q and not isinstance(q[key], str):
                    errs.append('%s: %s는 문자열이어야 한다.' % (qw, key))
        per = m.get('quiz_per_page', QUIZ_PER_PAGE)
        if isinstance(per, list):
            if not all(isinstance(x, int) and not isinstance(x, bool) and 1 <= x <= QUIZ_PER_PAGE for x in per):
                errs.append('%s: quiz_per_page 목록의 값은 1~%d이어야 한다(지금 %r).' % (where, QUIZ_PER_PAGE, per))
            elif sum(per) != len(quiz):
                errs.append('%s: quiz_per_page 합 %d가 문항 수 %d와 다르다.' % (where, sum(per), len(quiz)))
        elif isinstance(per, bool) or not isinstance(per, int) or not 1 <= per <= QUIZ_PER_PAGE:
            errs.append('%s: quiz_per_page는 1~%d이어야 한다(지금 %r).' % (where, QUIZ_PER_PAGE, per))
    return errs


# ── 머리(header) ─────────────────────────────────────────
def nav_label(m):
    return m.get('label', m['title'])


def nav_tooltip(m):
    return m['nav_tooltip'] if 'nav_tooltip' in m else plain(nav_label(m))


def make_base(spec):
    base = tpl_ref('_base.html')
    acc = ACCENTS[spec.get('accent', 'blue')]
    dot, item = nav_templates()
    mods = spec['modules']
    dots = '\n        '.join(render(dot, id=i, num=i + 1, tooltip=attr(nav_tooltip(m))) for i, m in enumerate(mods))
    items = '\n      '.join(render(item, id=i, num=i + 1, label=inline(nav_label(m))) for i, m in enumerate(mods))
    subst = {'COURSE_TITLE': text(spec['title']), 'ACCENT_COLOR': acc[0], 'ACCENT_HOVER': acc[1],
             'ACCENT_LIGHT': acc[2], 'ACCENT_MUTED': acc[3], 'NAV_DOTS': dots, 'SIDEBAR_ITEMS': items}
    base = re.sub('|'.join(subst), lambda mo: subst[mo.group(0)], base)  # 한 번에 바꿔 값 속 낱말을 다시 바꾸지 않는다
    long = [plain(nav_label(m)) for m in mods if len(plain(nav_label(m))) > 14]
    if long:
        print('경고: 사이드바 라벨이 14자를 넘는다(잘릴 수 있음, "label"로 줄여 쓴다):', ', '.join(long))
    return base


# ── 단서 칸 ─────────────────────────────────────────────
def callout(variant, title, body_html):
    return render(tpl('cue-callout.html'), variant=variant, title=title, body=indent(body_html, 12))


def ol(items):
    return '<ol>\n' + '\n'.join('  <li>%s</li>' % inline(x) for x in items) + '\n</ol>'


def questions(items):
    items = [inline(q) for q in items] if items else [todo('핵심 질문')]
    return render(tpl('cue-questions.html'), items='\n'.join('          <li>%s</li>' % q for q in items))


# ── 코넬 쪽 ─────────────────────────────────────────────
def corner_tag(name, style=None):
    if not name:
        return ''
    style = style or ('outline' if name in OUTLINE_CORNERS else 'filled')
    return '<span class="corner-tag%s">%s</span>' % (' outline' if style == 'outline' else '', text(name))


def screen(page, cue_parts, heading, notes_html, summary, corner=None, corner_style=None, paper_ref=None,
           dense=False, level=None):
    """heading·summary·paper_ref는 인라인 HTML, notes_html은 HTML 그대로."""
    classes = ' dense' if dense else ''
    attrs = ' data-level="%s"' % attr(level) if level else ''
    return render(tpl('screen.html'), page=page, label=plain(heading).replace('--', '-'), classes=classes, attrs=attrs,
                  cue='\n'.join(p.rstrip('\n') for p in cue_parts),
                  corner=corner_tag(corner, corner_style),
                  heading=inline(heading),
                  paper_ref='<span class="paper-ref">%s</span>' % inline(paper_ref) if paper_ref else '',
                  notes=indent(notes_html, 8), summary=inline(summary) if summary else todo('요약 한 문장'))


def quiz_block(qid, items, start):
    qs = []
    for k, q in enumerate(items):
        n = q.get('answer')  # validate()가 1..len(options)를 보장한다
        opts = [inline(o) for o in q.get('options') or [todo('선택지')] * 5]
        texts = [o if o[:1] in CIRCLED else '%s %s' % (CIRCLED[j], o) for j, o in enumerate(opts)]
        row = ' row' if all(len(plain(t)) <= 10 for t in texts) else ''
        right = q.get('right', todo('정답 해설'))  # 속성 안 HTML: attr()이 한 번 이스케이프한다
        wrong = q.get('wrong', todo('오답 해설'))
        if '|' not in right:
            right = '%s | %s' % (CIRCLED[n - 1] if n else todo('정답 기호'), right)
        if not wrong.startswith('|'):
            wrong = '| ' + wrong
        options = '\n'.join(
            '              <button class="quiz-option" data-value="option-%s" onclick="selectOption(this)">'
            '<div class="quiz-option-radio"></div><span>%s</span></button>' % (LETTERS[j], t) for j, t in enumerate(texts))
        correct = 'option-%s' % LETTERS[n - 1] if n else todo('정답 번호')
        qs.append(render(tpl('quiz-question.html'), correct=correct,
                         right=attr(right), wrong=attr(wrong), qnum=start + k,
                         question=inline(q['q']) if 'q' in q else todo('발문'), row=row, options=options))
    return render(tpl('quiz.html'), quiz_id=qid, questions=''.join(qs).rstrip('\n'))


# ── 단원 ───────────────────────────────────────────────
def make_module(i, m):
    prereq = m.get('prereq', i == 0)
    pages, page = [], 1
    for s_i, s in enumerate(m.get('screens') or [{}]):
        cue = []
        if s_i == 0:
            cue.append(callout('callout-info', '학습 목표',
                               '<p>이 모듈을 학습하면 다음을 할 수 있다.</p>\n' + ol(m.get('objectives') or [todo('학습 목표 ~할 수 있다.')])))
        elif prereq and s.get('background', True):
            cue.append(callout('callout-info', '배경 지식',
                               '<p>이 화면은 논문의 주장이 아니라 논문을 읽기 위해 먼저 알아 둘 배경이다.</p>'))
        if s.get('questions') or s_i > 0:
            cue.append(questions(s.get('questions')))
        notes = s.get('notes') or '<p>%s</p>' % todo('본문')
        pages.append(screen(page, cue, s.get('heading', todo('화면 제목')), notes, s.get('summary'),
                            corner=s.get('corner'), corner_style=s.get('corner_style'), paper_ref=s.get('paper_ref'),
                            dense=s.get('dense', False), level=s.get('level')))
        page += 1
    quiz = m.get('quiz') or []
    titles = m.get('quiz_titles') or []
    sums = m.get('quiz_summaries') or []
    qc = m.get('quiz_cues') or []
    c = 0
    for k, size in enumerate(quiz_groups(m)):
        if k == 0:
            cue = [callout('callout-accent', '핵심 정리', ol(m.get('takeaways') or [todo('요점')]))]
        else:
            cue = [questions(qc[k - 1] if len(qc) >= k else None)]
        pages.append(screen(page, cue, titles[k] if k < len(titles) else todo('확인 문제 제목'),
                            quiz_block('quiz-m%d%s' % (i, '' if k == 0 else '-%d' % (k + 1)), quiz[c:c + size], c + 1),
                            sums[k] if k < len(sums) else None, corner='확인 문제',
                            corner_style=m.get('quiz_corner_style')))
        c += size
        page += 1
    return render(tpl('module.html'), id=i, num=i + 1, title=inline(m['title']),
                  subtitle=inline(m['subtitle']) if 'subtitle' in m else todo('부제'),
                  screens=''.join(pages).rstrip('\n') + '\n')


def module_path(d, i, m):
    return os.path.join(d, 'modules', '%s.html' % module_name(i, m))


# ── 명령 ───────────────────────────────────────────────
def cmd_init(d, spec, force):
    os.makedirs(os.path.join(d, 'modules'), exist_ok=True)
    for f in COPY:
        if force or not os.path.exists(os.path.join(d, f)):
            shutil.copy2(os.path.join(REF, f), os.path.join(d, f))
    if not os.path.exists(os.path.join(d, 'vendor')):
        shutil.copytree(os.path.join(REF, 'vendor'), os.path.join(d, 'vendor'),
                        ignore=shutil.ignore_patterns('make-vendor.sh', 'rename-font.py', 'ksx-unicodes.py'))
    cmd_base(d, spec)
    cmd_modules(d, spec, force)


def cmd_base(d, spec):
    out = make_base(spec)
    with open(os.path.join(d, '_base.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print('_base.html 작성')


def cmd_modules(d, spec, force):
    os.makedirs(os.path.join(d, 'modules'), exist_ok=True)
    for i, m in enumerate(spec['modules']):
        p = module_path(d, i, m)
        if os.path.exists(p) and not force:
            print('건너뜀(이미 있음):', os.path.relpath(p, d))
            continue
        out = make_module(i, m)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(out)
        print('작성:', os.path.relpath(p, d))


def cmd_todo(d):
    n = 0
    for root, _, files in os.walk(d):
        if 'vendor' in root.split(os.sep):
            continue
        for fn in sorted(files):
            if not fn.endswith('.html') or fn == 'index.html':
                continue
            p = os.path.join(root, fn)
            for ln, line in enumerate(open(p, encoding='utf-8'), 1):
                for t in re.findall(r'\[작성 필요: [^\]]*\]', line):
                    print('%s:%d %s' % (os.path.relpath(p, d), ln, t)); n += 1
    print('남은 자리 %d개' % n)
    return 1 if n else 0


def load_spec(path):
    try:
        with open(path, encoding='utf-8') as f:
            spec = json.load(f)
    except OSError as e:
        sys.exit('spec 파일을 열 수 없다: %s (%s)' % (path, e.strerror))
    except json.JSONDecodeError as e:
        sys.exit('spec 파일의 JSON이 틀렸다: %s %d행 %d열 (%s)' % (path, e.lineno, e.colno, e.msg))
    errs = validate(spec)
    if errs:
        sys.exit('spec 오류 %d건, 파일을 쓰지 않았다(%s):\n  ' % (len(errs), path) + '\n  '.join(errs))
    return spec


def main(argv):
    if len(argv) < 3 or argv[1] not in ('init', 'base', 'modules', 'todo') or (argv[1] != 'todo' and len(argv) < 4):
        sys.exit(__doc__)
    cmd, d = argv[1], argv[2]
    if cmd == 'todo':
        sys.exit(cmd_todo(d))
    spec = load_spec(argv[3])
    force = '--force' in argv
    {'init': lambda: cmd_init(d, spec, force), 'base': lambda: cmd_base(d, spec),
     'modules': lambda: cmd_modules(d, spec, force)}[cmd]()


if __name__ == '__main__':
    main(sys.argv)
