# SOC Portfolio

A clean, dark-themed portfolio site for storing SOC analyst write-ups, CTF walkthroughs, study notes, tool cheatsheets, and certifications. Built with Flask. You write content as markdown files — the site renders them automatically. No database, no build step.

---

## How it works

Every piece of content is a **markdown file** in a content folder. Drop a `.md` file into the right folder, refresh the site, and it appears. That's the whole workflow.

```
writeups/thm/my-room.md                    → Write-ups → TryHackMe
ctf/picoctf-challenge.md                   → CTF
notes/detection-monitoring/edr-basics.md   → Notes → Detection & Monitoring
certs/security-plus.md                     → Certs
tools/spl-cheatsheet.md                    → Tools (quick-reference cheatsheets)
```

### Note categories (domain-based)

| Folder | Shows as |
|--------|----------|
| `notes/networking/` | Networking |
| `notes/linux-os/` | Linux & OS |
| `notes/windows/` | Windows |
| `notes/security-concepts/` | Security Concepts |
| `notes/detection-monitoring/` | Detection & Monitoring — SIEM, EDR, IDS/IPS, Sysmon |
| `notes/threat-intel/` | Threat Intelligence |
| `notes/ir-forensics/` | IR & Forensics |

**Notes vs Tools:** Notes are things you studied and understand, organised by SOC domain. Tools is quick-reference cheatsheets you look up mid-task (command references, syntax guides). A SIEM *concept* note goes in Detection & Monitoring; an SPL *syntax cheatsheet* goes in Tools.

### Built-in features

- **Search** — `/search/` scans every document (titles, tags, and full text)
- **Auto table of contents** — articles with 3+ sections get a TOC automatically
- **Reading time** — calculated per article
- **Escaped pipes in tables** — use `\|` inside a table cell to show a literal pipe

Each file starts with a **frontmatter** block (between `---` lines) defining the title, tags, difficulty, date, and summary. See `CONTENT_TEMPLATE.md` for the full reference — copy it as a starting point for every new entry.

---

## Run it locally

```bash
# 1. Install Flask
pip install -r requirements.txt

# 2. Run
python app.py

# 3. Open http://127.0.0.1:5000
```

---

## Deploy to PythonAnywhere (free)

PythonAnywhere gives you free Flask hosting at `yourusername.pythonanywhere.com`.

### Step 1 — Create an account
Sign up at https://www.pythonanywhere.com (free "Beginner" tier is enough).

### Step 2 — Upload your project
Two options:

**Option A — via GitHub (recommended):**
Open a Bash console on PythonAnywhere and run:
```bash
git clone https://github.com/YOUR_USERNAME/soc-portfolio.git
```

**Option B — via upload:**
Use the "Files" tab to upload the project as a zip, then unzip in a Bash console:
```bash
unzip soc-portfolio.zip
```

### Step 3 — Install Flask
In a PythonAnywhere Bash console:
```bash
cd soc-portfolio
pip install --user -r requirements.txt
```

### Step 4 — Create the web app
1. Go to the **Web** tab → "Add a new web app"
2. Choose **Manual configuration** (not the Flask quickstart)
3. Pick **Python 3.10** (or latest available)

### Step 5 — Point it at your code
In the **Web** tab, find the "Code" section:
- **Source code:** `/home/YOUR_USERNAME/soc-portfolio`
- **WSGI configuration file:** click the link to edit it

Delete everything in that WSGI file and replace it with:
```python
import sys
project_home = '/home/YOUR_USERNAME/soc-portfolio'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from app import app as application
```
(Replace `YOUR_USERNAME` with your actual username. This is also saved in `wsgi_pythonanywhere.py` for reference.)

### Step 6 — Reload
Click the big green **Reload** button on the Web tab. Visit `yourusername.pythonanywhere.com`.

### Updating content later
When you add new write-ups, push them to GitHub, then in a PythonAnywhere Bash console:
```bash
cd soc-portfolio && git pull
```
Then hit **Reload** on the Web tab. Done.

---

## Customising

Open `app.py` and edit the `SITE` dictionary at the top:
```python
SITE = {
    'name': 'SOC Portfolio',
    'tagline': 'Tier 1 SOC Analyst in Training',
    'github': 'https://github.com/YOUR_USERNAME/soc-portfolio',
    'linkedin': 'https://linkedin.com/in/YOUR_USERNAME',
    'tryhackme': 'https://tryhackme.com/p/YOUR_USERNAME',
    'email': 'your@email.com',
}
```

Edit `about.md` to write your bio. Colours and styling live in `static/css/style.css` (CSS variables at the top control the whole theme).

---

## Removing the sample content

The repo ships with example files so the site isn't empty. Delete these once you've added your own:
- `writeups/thm/example-windows-event-logs.md`
- `notes/networking/example-ports-cheatsheet.md`

---

## What the markdown parser supports

Headings, **bold**, *italic*, `inline code`, fenced code blocks, tables, blockquotes, unordered lists, links, images, horizontal rules, and `==highlights==`. It's a lightweight custom parser — no external markdown library needed, which keeps the PythonAnywhere setup dead simple.
