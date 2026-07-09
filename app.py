import os
import re
from flask import Flask, render_template, abort, url_for, request
from pathlib import Path

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE = {
    'name': 'SOC Portfolio',
    'tagline': 'Tier 1 SOC Analyst in Training',
    'github': 'https://github.com/LewisJava',
    'tryhackme': 'https://tryhackme.com/p/LewisJava',
    'email': 'lewis2101@proton.me',
}

CONTENT_ROOT = Path(__file__).parent

# Domain-based note categories. Key = folder under notes/, value = (label, accent colour)
NOTE_CATEGORIES = {
    'networking':           ('Networking', '#22d3ee'),
    'linux-os':             ('Linux & OS', '#a78bfa'),
    'windows':              ('Windows', '#60a5fa'),
    'security-concepts':    ('Security Concepts', '#fbbf24'),
    'detection-monitoring': ('Detection & Monitoring', '#4ade80'),
    'threat-intel':         ('Threat Intelligence', '#fb923c'),
    'ir-forensics':         ('IR & Forensics', '#f472b6'),
    'frameworks':           ('frameworks', '#c4b5fd'),
}

WRITEUP_PLATFORMS = {
    'thm': 'TryHackMe',
    'letsdefend': 'LetsDefend',
    'blueteamlabs': 'Blue Team Labs',
    'home-lab': 'Home Lab',
}

PIPE_TOKEN = '\x00PIPE\x00'

# ── MARKDOWN PARSER ───────────────────────────────────────────────────────────
def parse_markdown(text):
    """Minimal markdown -> HTML. Headings, bold, italic, code blocks, inline
    code, links, images, lists, blockquotes, tables (with \\| escaping),
    horizontal rules, ==highlights==."""

    def replace_code_block(m):
        lang = m.group(1) or ''
        code = m.group(2).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="lang-{lang}">{code}</code></pre>'
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)

    lines = text.split('\n')
    html = []
    in_list = False
    in_blockquote = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Table: header row with pipes followed by a separator row
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:|-]+\|[\s:|-]*$', lines[i+1]) and '-' in lines[i+1]:
            if in_list: html.append('</ul>'); in_list = False
            html.append('<table><thead><tr>')
            for cell in split_table_row(line):
                html.append(f'<th>{inline(cell)}</th>')
            html.append('</tr></thead><tbody>')
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                html.append('<tr>')
                for cell in split_table_row(lines[i]):
                    html.append(f'<td>{inline(cell)}</td>')
                html.append('</tr>')
                i += 1
            html.append('</tbody></table>')
            continue

        # Blockquote
        if line.startswith('> '):
            if not in_blockquote:
                html.append('<blockquote>')
                in_blockquote = True
            html.append(f'<p>{inline(line[2:])}</p>')
            i += 1; continue
        elif in_blockquote:
            html.append('</blockquote>')
            in_blockquote = False

        # Horizontal rule
        if re.match(r'^-{3,}$', line.strip()) or re.match(r'^_{3,}$', line.strip()):
            if in_list: html.append('</ul>'); in_list = False
            html.append('<hr>')
            i += 1; continue

        # Headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            if in_list: html.append('</ul>'); in_list = False
            level = len(m.group(1))
            content = inline(m.group(2))
            slug = heading_slug(m.group(2))
            html.append(f'<h{level} id="{slug}">{content}</h{level}>')
            i += 1; continue

        # Unordered list
        if re.match(r'^[-*+]\s+', line):
            if not in_list: html.append('<ul>'); in_list = True
            html.append(f'<li>{inline(line[2:].strip())}</li>')
            i += 1; continue
        elif in_list and line.strip() == '':
            html.append('</ul>')
            in_list = False
        elif in_list:
            html.append('</ul>')
            in_list = False

        # Empty line
        if line.strip() == '':
            html.append('')
            i += 1; continue

        # Paragraph
        if not line.startswith('<'):
            html.append(f'<p>{inline(line)}</p>')
        else:
            html.append(line)

        i += 1

    if in_list: html.append('</ul>')
    if in_blockquote: html.append('</blockquote>')
    return '\n'.join(html)


def split_table_row(line):
    """Split a table row on unescaped pipes. \\| inside a cell is preserved."""
    protected = line.replace('\\|', PIPE_TOKEN)
    cells = [c.strip() for c in protected.strip().strip('|').split('|')]
    return [c.replace(PIPE_TOKEN, '|') for c in cells]


def heading_slug(text):
    return re.sub(r'[^\w\s-]', '', text.lower()).strip().replace(' ', '-')


def inline(text):
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    return text


def extract_toc(content):
    """Extract h2 headings for a table of contents. Only shown if 3+ headings."""
    headings = re.findall(r'^##\s+(.*)', content, re.MULTILINE)
    if len(headings) < 3:
        return []
    return [{'text': h, 'slug': heading_slug(h)} for h in headings]


def reading_time(content):
    words = len(re.findall(r'\w+', content))
    return max(1, round(words / 200))


# ── FRONTMATTER & LOADING ─────────────────────────────────────────────────────
def parse_frontmatter(text):
    meta = {'title': 'Untitled', 'date': '', 'tags': [], 'difficulty': '', 'platform': '', 'summary': '', 'status': '', 'org': ''}
    if not text.startswith('---'):
        return meta, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return meta, text
    fm_block = parts[1].strip()
    content = parts[2].strip()
    for line in fm_block.split('\n'):
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        key = key.strip()
        val = val.strip()
        if key == 'tags':
            meta['tags'] = [t.strip().strip('"\'') for t in val.strip('[]').split(',') if t.strip()]
        else:
            meta[key] = val.strip('"\'')
    return meta, content


def load_md(path):
    try:
        text = path.read_text(encoding='utf-8')
        meta, content = parse_frontmatter(text)
        meta['html'] = parse_markdown(content)
        meta['slug'] = path.stem
        meta['raw'] = content
        meta['toc'] = extract_toc(content)
        meta['reading_time'] = reading_time(content)
        if not meta.get('title') or meta['title'] == 'Untitled':
            m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            if m:
                meta['title'] = m.group(1)
        return meta
    except Exception:
        return None


def load_section(folder, subdir=''):
    base = CONTENT_ROOT / folder
    if subdir:
        base = base / subdir
    if not base.exists():
        return []
    items = []
    for f in base.glob('*.md'):
        doc = load_md(f)
        if doc:
            doc['section'] = folder
            doc['subdir'] = subdir
            items.append(doc)
    items.sort(key=lambda x: x.get('date', ''), reverse=True)
    return items


def all_documents():
    """Every document on the site with its URL — used by search."""
    docs = []
    for sub in WRITEUP_PLATFORMS:
        for d in load_section('writeups', sub):
            d['url'] = url_for('writeup', platform=sub, slug=d['slug'])
            d['kind'] = f"Write-up · {WRITEUP_PLATFORMS[sub]}"
            docs.append(d)
    for d in load_section('ctf'):
        d['url'] = url_for('ctf_detail', slug=d['slug'])
        d['kind'] = 'CTF'
        docs.append(d)
    for sub, (label, _) in NOTE_CATEGORIES.items():
        for d in load_section('notes', sub):
            d['url'] = url_for('note', category=sub, slug=d['slug'])
            d['kind'] = f"Note · {label}"
            docs.append(d)
    for d in load_section('tools'):
        d['url'] = url_for('tool_detail', slug=d['slug'])
        d['kind'] = 'Tool / Cheatsheet'
        docs.append(d)
    return docs


# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    recent_writeups = []
    for sub in WRITEUP_PLATFORMS:
        recent_writeups += load_section('writeups', sub)
    recent_writeups.sort(key=lambda x: x.get('date', ''), reverse=True)

    recent_notes = []
    for sub in NOTE_CATEGORIES:
        for d in load_section('notes', sub):
            d['cat_label'] = NOTE_CATEGORIES[sub][0]
            d['cat_key'] = sub
            recent_notes.append(d)
    recent_notes.sort(key=lambda x: x.get('date', ''), reverse=True)

    recent_ctf = load_section('ctf')
    certs = load_section('certs')
    tools_count = len(load_section('tools'))
    notes_count = len(recent_notes)

    return render_template('index.html',
        site=SITE,
        recent_writeups=recent_writeups[:6],
        recent_notes=recent_notes[:5],
        recent_ctf=recent_ctf[:4],
        certs=certs,
        total_writeups=len(recent_writeups),
        total_ctf=len(recent_ctf),
        notes_count=notes_count,
        tools_count=tools_count,
    )


@app.route('/writeups/')
def writeups():
    platforms = {}
    for sub, label in WRITEUP_PLATFORMS.items():
        items = load_section('writeups', sub)
        if items:
            platforms[label] = items
    return render_template('writeups.html', site=SITE, platforms=platforms)


@app.route('/writeups/<platform>/<slug>/')
def writeup(platform, slug):
    path = CONTENT_ROOT / 'writeups' / platform / f'{slug}.md'
    if not path.exists():
        abort(404)
    doc = load_md(path)
    return render_template('article.html', site=SITE, doc=doc, back_url=url_for('writeups'), back_label='← Write-ups')


@app.route('/ctf/')
def ctf():
    items = load_section('ctf')
    return render_template('ctf.html', site=SITE, items=items)


@app.route('/ctf/<slug>/')
def ctf_detail(slug):
    path = CONTENT_ROOT / 'ctf' / f'{slug}.md'
    if not path.exists():
        abort(404)
    doc = load_md(path)
    return render_template('article.html', site=SITE, doc=doc, back_url=url_for('ctf'), back_label='← CTF')


@app.route('/notes/')
def notes():
    sections = {}
    for sub, (label, color) in NOTE_CATEGORIES.items():
        items = load_section('notes', sub)
        if items:
            sections[label] = {'docs': items, 'key': sub, 'color': color}
    return render_template('notes.html', site=SITE, sections=sections, categories=NOTE_CATEGORIES)


@app.route('/notes/<category>/<slug>/')
def note(category, slug):
    path = CONTENT_ROOT / 'notes' / category / f'{slug}.md'
    if not path.exists():
        abort(404)
    doc = load_md(path)
    return render_template('article.html', site=SITE, doc=doc, back_url=url_for('notes'), back_label='← Notes')


@app.route('/tools/')
def tools():
    items = load_section('tools')
    return render_template('tools.html', site=SITE, items=items)


@app.route('/tools/<slug>/')
def tool_detail(slug):
    path = CONTENT_ROOT / 'tools' / f'{slug}.md'
    if not path.exists():
        abort(404)
    doc = load_md(path)
    return render_template('article.html', site=SITE, doc=doc, back_url=url_for('tools'), back_label='← Tools')


@app.route('/certs/')
def certs():
    items = load_section('certs')
    return render_template('certs.html', site=SITE, items=items)


@app.route('/search/')
def search():
    q = request.args.get('q', '').strip()
    results = []
    if q and len(q) >= 2:
        q_lower = q.lower()
        for doc in all_documents():
            haystack = ' '.join([
                doc.get('title', ''),
                doc.get('summary', ''),
                ' '.join(doc.get('tags', [])),
                doc.get('raw', ''),
            ]).lower()
            if q_lower in haystack:
                # Build a small snippet around the first match in the body
                idx = doc.get('raw', '').lower().find(q_lower)
                if idx >= 0:
                    start = max(0, idx - 60)
                    end = min(len(doc['raw']), idx + 90)
                    snippet = ('…' if start > 0 else '') + doc['raw'][start:end].replace('\n', ' ') + ('…' if end < len(doc['raw']) else '')
                else:
                    snippet = doc.get('summary', '')
                doc['snippet'] = snippet
                results.append(doc)
    return render_template('search.html', site=SITE, q=q, results=results)


@app.route('/about/')
def about():
    path = CONTENT_ROOT / 'about.md'
    doc = load_md(path) if path.exists() else {'html': '<p>About page coming soon.</p>', 'title': 'About', 'toc': [], 'reading_time': 1}
    return render_template('about.html', site=SITE, doc=doc)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', site=SITE), 404


if __name__ == '__main__':
    app.run(debug=True)
