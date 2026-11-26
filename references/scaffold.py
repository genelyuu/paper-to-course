#!/usr/bin/env python3
"""scaffold.py: 강의의 공통 레이아웃(머리·꼬리·코넬 쪽)을 references/templates/의 틀로 찍어 낸다.

레이아웃은 손으로 쓰지 않는다. 모듈 작성자는 쪽마다 .notes 안의 본문만 채운다.
  머리(header) : references/_base.html (내비·사이드바) + templates/nav.html (단원별 점·목차 줄)
  꼬리(footer) : references/_footer.html
  단원         : templates/module.html (단원 머리말 + 쪽들)
  코넬 쪽      : templates/screen.html (.cue | .notes / .summary)
  단서 칸      : templates/cue-callout.html (학습 목표·배경 지식·핵심 정리), templates/cue-questions.html (핵심 질문)
  확인 문제    : templates/quiz.html, templates/quiz-question.html (쪽당 2문항)

사용법
  python3 -I scaffold.py init    <course-dir> <spec.json> [--force]   자산 복사 + _base.html + 모듈 뼈대
  python3 -I scaffold.py base    <course-dir> <spec.json>             _base.html만 다시 만든다(제목·색·목차가 바뀔 때)
  python3 -I scaffold.py modules <course-dir> <spec.json> [--force]   모듈 뼈대만 만든다(있는 파일은 --force 없이는 두지 않는다)
  python3 -I scaffold.py todo    <course-dir>                          남은 "[작성 필요: …]" 자리를 보여 준다(0개여야 빌드)

spec.json 형식은 templates/course.example.json을 본다. 빠진 글은 "[작성 필요: …]"로 채워 눈에 띄게 남긴다.
표준 라이브러리만 쓴다.
"""
import html, json, os, re, shutil, sys, textwrap

REF = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(REF, 'templates')
TODO = '[작성 필요: {}]'
CIRCLED = '①②③④⑤'
ACCENTS = {  # 교과 색 프리셋: accent / hover / light / muted (design-system.md "교과 색 프리셋")
    'blue':   ('#1F6FB2', '#185A92', '#E8F1FA', '#6FA3D3'),
    'green':  ('#1B7A50', '#145F3E', '#E6F4EC', '#6BB592'),
    'purple': ('#6B4FA8', '#563F88', '#F0ECF8', '#A08ECB'),
    'orange': ('#B85C0F', '#964A0B', '#FCEFE3', '#E0A06A'),
}
COPY = ['styles.css', 'main.js', '_footer.html', 'build.sh', 'build.py']


def tpl(name):
    with open(os.path.join(TPL, name), encoding='utf-8') as f:
        return f.read()


def render(t, **kw):
    out = re.sub(r'\{\{(\w+)\}\}', lambda m: str(kw[m.group(1)]), t)
    return out


def nav_templates():
    lines = [l for l in tpl('nav.html').splitlines() if l.strip() and not l.lstrip().startswith('<!--')]
    return lines[0], lines[1]


def attr(s):
    return html.escape(s, quote=True)


def todo(what):
    return TODO.format(what)


def indent(block, n):
    pad = ' ' * n
    block = textwrap.dedent(block.strip('\n'))
    return '\n'.join(pad + l if l.strip() else l for l in block.splitlines())


# ── 머리(header) ─────────────────────────────────────────
def make_base(spec):
    base = tpl_ref('_base.html')
    acc = ACCENTS[spec.get('accent', 'blue')]
    dot, item = nav_templates()
    mods = spec['modules']
    dots = '\n        '.join(render(dot, id=i, num=i + 1, label=m.get('label', m['title'])) for i, m in enumerate(mods))
    items = '\n      '.join(render(item, id=i, num=i + 1, label=m.get('label', m['title'])) for i, m in enumerate(mods))
    for k, v in (('COURSE_TITLE', spec['title']), ('ACCENT_COLOR', acc[0]), ('ACCENT_HOVER', acc[1]),
                 ('ACCENT_LIGHT', acc[2]), ('ACCENT_MUTED', acc[3]), ('NAV_DOTS', dots), ('SIDEBAR_ITEMS', items)):
        base = base.replace(k, v)
    long = [m.get('label', m['title']) for m in mods if len(m.get('label', m['title'])) > 14]
    if long:
        print('경고: 사이드바 라벨이 14자를 넘는다(잘릴 수 있음, "label"로 줄여 쓴다):', ', '.join(long))
    return base


def tpl_ref(name):
    with open(os.path.join(REF, name), encoding='utf-8') as f:
        return f.read()


# ── 단서 칸 ─────────────────────────────────────────────
def callout(variant, title, body_html):
    return render(tpl('cue-callout.html'), variant=variant, title=title, body=indent(body_html, 12))


def ol(items):
    return '<ol>\n' + '\n'.join('  <li>%s</li>' % x for x in items) + '\n</ol>'


def questions(items):
    items = items or [todo('핵심 질문')]
    return render(tpl('cue-questions.html'), items='\n'.join('          <li>%s</li>' % q for q in items))


# ── 코넬 쪽 ─────────────────────────────────────────────
def screen(page, cue_parts, heading, notes_html, summary, corner=None, paper_ref=None, dense=False, level=None):
    classes = ' dense' if dense else ''
    attrs = ' data-level="%s"' % level if level else ''
    return render(tpl('screen.html'), page=page, label=re.sub(r'<[^>]+>', '', heading), classes=classes, attrs=attrs,
                  cue='\n'.join(p.rstrip('\n') for p in cue_parts),
                  corner='<span class="corner-tag">%s</span>' % corner if corner else '',
                  heading=heading,
                  paper_ref='<span class="paper-ref">%s</span>' % paper_ref if paper_ref else '',
                  notes=indent(notes_html, 8), summary=summary or todo('요약 한 문장'))


def quiz_block(qid, items, start):
    qs = []
    for k, q in enumerate(items):
        n = q.get('answer')
        opts = q.get('options') or [todo('선택지')] * 5
        texts = [o if o[:1] in CIRCLED else '%s %s' % (CIRCLED[j], o) for j, o in enumerate(opts)]
        row = ' row' if all(len(t) <= 10 for t in texts) else ''
        right = q.get('right', todo('정답 해설'))
        wrong = q.get('wrong', todo('오답 해설'))
        if n and '|' not in right:
            right = '%s | %s' % (CIRCLED[n - 1], right)
        if not wrong.startswith('|'):
            wrong = '| ' + wrong
        options = '\n'.join(
            '              <button class="quiz-option" data-value="option-%s" onclick="selectOption(this)">'
            '<div class="quiz-option-radio"></div><span>%s</span></button>' % ('abcde'[j], t) for j, t in enumerate(texts))
        qs.append(render(tpl('quiz-question.html'), correct='option-%s' % 'abcde'[(n or 1) - 1],
                         right=attr(right), wrong=attr(wrong), qnum=start + k,
                         question=q.get('q', todo('발문')), row=row, options=options))
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
                            corner=s.get('corner'), paper_ref=s.get('paper_ref'),
                            dense=s.get('dense', False), level=s.get('level')))
        page += 1
    quiz = m.get('quiz') or []
    for c in range(0, len(quiz), 2):
        k = c // 2
        if k == 0:
            cue = [callout('callout-accent', '핵심 정리', ol(m.get('takeaways') or [todo('요점')]))]
        else:
            qc = m.get('quiz_cues') or []
            cue = [questions(qc[k - 1] if len(qc) >= k else None)]
        titles = m.get('quiz_titles') or []
        sums = m.get('quiz_summaries') or []
        pages.append(screen(page, cue, titles[k] if k < len(titles) else todo('확인 문제 제목'),
                            quiz_block('quiz-m%d%s' % (i, '' if k == 0 else '-%d' % (k + 1)), quiz[c:c + 2], c + 1),
                            sums[k] if k < len(sums) else None, corner='확인 문제'))
        page += 1
    return render(tpl('module.html'), id=i, num=i + 1, title=m['title'],
                  subtitle=m.get('subtitle', todo('부제')), screens=''.join(pages).rstrip('\n') + '\n')


def module_path(d, i, m):
    return os.path.join(d, 'modules', '%02d-%s.html' % (i, m.get('slug', 'module%d' % i)))


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
    with open(os.path.join(d, '_base.html'), 'w', encoding='utf-8') as f:
        f.write(make_base(spec))
    print('_base.html 작성')


def cmd_modules(d, spec, force):
    os.makedirs(os.path.join(d, 'modules'), exist_ok=True)
    for i, m in enumerate(spec['modules']):
        p = module_path(d, i, m)
        if os.path.exists(p) and not force:
            print('건너뜀(이미 있음):', os.path.relpath(p, d))
            continue
        with open(p, 'w', encoding='utf-8') as f:
            f.write(make_module(i, m))
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


def main(argv):
    if len(argv) < 3 or argv[1] not in ('init', 'base', 'modules', 'todo'):
        sys.exit(__doc__)
    cmd, d = argv[1], argv[2]
    if cmd == 'todo':
        sys.exit(cmd_todo(d))
    spec = json.load(open(argv[3], encoding='utf-8'))
    force = '--force' in argv
    {'init': lambda: cmd_init(d, spec, force), 'base': lambda: cmd_base(d, spec),
     'modules': lambda: cmd_modules(d, spec, force)}[cmd]()


if __name__ == '__main__':
    main(sys.argv)
