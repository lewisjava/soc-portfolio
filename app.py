import os
import re
from datetime import datetime
from flask import Flask, render_template, abort, url_for
from pathlib import Path

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE = {
    'name': 'SOC Portfolio',
    'tagline': 'Tier 1 SOC Analyst in Training',
    'github': 'https://github.com/YOUR_USERNAME/soc-portfolio',
    'linkedin': 'https://linkedin.com/in/YOUR_USERNAME',
    'tryhackme': 'https://tryhackme.com/p/YOUR_USERNAME',
    'email': 'your@email.com',
}

CONTENT_ROOT = Path(__file__).parent

# ── MARKDOWN PARSER ───────────────────────────────────────────────────────────
def parse_markdown(text):
    """Minimal markdown → HTML. Handles headings, bold, italic,
    code blocks, inline code, links, lists, blockquotes, horizontal rules."""

    # Fenced code blocks
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

        # Table detection: current line has pipes, next line is a separator
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:|-]+\|[\s:|-]*$', lines[i+1]) and '-' in lines[i+1]:
            if in_list: html.append('</ul>'); in_list = False
            header_cells = [c.strip() for c in line.strip().strip('|').split('|')]
            html.append('<table><thead><tr>')
            for cell in header_cells:
                html.append(f'<th>{inline(cell)}</th>')
            html.append('</tr></thead><tbody>')
            i += 2  # skip header and separator
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row_cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                html.append('<tr>')
                for cell in row_cells:
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
            slug = re.sub(r'[^\w\s-]', '', m.group(2).lower()).strip().replace(' ', '-')
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


def inline(text):
    """Process inline markdown: bold, italic, inline code, links, images."""
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    # Images (before links)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    # Badge-style highlights: ==text==
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    return text


# ── FRONTMATTER ───────────────────────────────────────────────────────────────
def parse_frontmatter(text):
    """Extract YAML-style frontmatter between --- delimiters."""
    meta = {'title': 'Untitled', 'date': '', 'tags': [], 'difficulty': '', 'platform': '', 'summary': ''}
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
    """Load a markdown file, parse frontmatter and content."""
    try:
        text = path.read_text(encoding='utf-8')
        meta, content = parse_frontmatter(text)
        meta['html'] = parse_markdown(content)
        meta['slug'] = path.stem
        meta['raw'] = content
        if not meta.get('title') or meta['title'] == 'Untitled':
            # Try to infer title from first heading
            m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            if m:
                meta['title'] = m.group(1)
        return meta
    except Exception:
        return None


def load_section(folder, subdir=''):
    """Load all markdown files from a section folder."""
    base = CONTENT_ROOT / folder
    if subdir:
        base = base / subdir
    if not base.exists():
        return []
    items = []
    for f in sorted(base.glob('*.md'), reverse=True):
        doc = load_md(f)
        if doc:
            doc['section'] = folder
            doc['subdir'] = subdir
            items.append(doc)
    return items


# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    recent_writeups = []
    for sub in ['thm', 'letsdefend', 'blueteamlabs', 'home-lab']:
        recent_writeups += load_section('writeups', sub)
    recent_writeups.sort(key=lambda x: x.get('date', ''), reverse=True)

    recent_ctf = load_section('ctf')
    certs = load_section('certs')
    return render_template('index.html',
        site=SITE,
        recent_writeups=recent_writeups[:6],
        recent_ctf=recent_ctf[:4],
        certs=certs,
        total_writeups=len(recent_writeups),
        total_ctf=len(recent_ctf),
    )


@app.route('/writeups/')
def writeups():
    platforms = {}
    labels = {'thm': 'TryHackMe', 'letsdefend': 'LetsDefend', 'blueteamlabs': 'Blue Team Labs', 'home-lab': 'Home Lab'}
    for sub in ['thm', 'letsdefend', 'blueteamlabs', 'home-lab']:
        items = load_section('writeups', sub)
        if items:
            platforms[labels.get(sub, sub)] = items
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
    labels = {
        'networking': 'Networking', 'linux': 'Linux & OS',
        'windows': 'Windows', 'security': 'Security Concepts',
        'siem': 'SIEM & Tools', 'threat-intel': 'Threat Intel'
    }
    for sub in labels:
        items = load_section('notes', sub)
        if items:
            sections[labels[sub]] = {'docs': items, 'key': sub}
    return render_template('notes.html', site=SITE, sections=sections)


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


@app.route('/about/')
def about():
    path = CONTENT_ROOT / 'about.md'
    doc = load_md(path) if path.exists() else {'html': '<p>About page coming soon.</p>', 'title': 'About'}
    return render_template('about.html', site=SITE, doc=doc)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', site=SITE), 404


if __name__ == '__main__':
    app.run(debug=True)
