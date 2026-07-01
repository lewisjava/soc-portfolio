# GitHub Repo Setup Guide

Your GitHub repo serves two purposes: it's the source for your PythonAnywhere site, AND it's a portfolio piece itself. Recruiters look at GitHub. A well-organised, regularly-updated repo signals competence before they even read a word.

---

## One-time setup

### 1. Create the repo on GitHub
- Go to https://github.com/new
- Name it `soc-portfolio` (or `soc-analyst-portfolio`)
- Make it **Public** (the whole point is visibility)
- Don't initialise with a README — you already have one

### 2. Push this project up
From inside the project folder on your machine:
```bash
git init
git add .
git commit -m "Initial commit: SOC portfolio site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/soc-portfolio.git
git push -u origin main
```

---

## Recommended folder structure

This is already built for you, but here's what each folder is for:

```
soc-portfolio/
├── writeups/
│   ├── thm/             ← TryHackMe room write-ups
│   ├── letsdefend/      ← LetsDefend investigation reports
│   ├── blueteamlabs/    ← Blue Team Labs challenges
│   └── home-lab/        ← Your home lab projects & detections
├── ctf/                 ← CTF walkthroughs (picoCTF, etc.)
├── notes/
│   ├── networking/      ← Subnetting, protocols, ports
│   ├── linux/           ← Commands, permissions, log locations
│   ├── windows/         ← Event IDs, registry, PowerShell
│   ├── security/        ← Crypto, attacks, frameworks
│   ├── siem/            ← Splunk SPL, Sentinel KQL
│   └── threat-intel/    ← IOC enrichment, MITRE ATT&CK
├── certs/               ← One file per certification
├── tools/               ← Cheatsheets for tools you use
├── about.md             ← Your bio
└── app.py               ← The Flask site (don't touch unless customising)
```

---

## Daily workflow

Every time you finish a lab or learn something worth noting:

```bash
# 1. Create a new markdown file (copy CONTENT_TEMPLATE.md as a starting point)
cp CONTENT_TEMPLATE.md writeups/thm/my-new-room.md

# 2. Write your content, then commit
git add .
git commit -m "Add write-up: My New Room"
git push

# 3. If your site is live on PythonAnywhere, pull + reload there
```

**Commit often.** A GitHub contribution graph that's green every day during your study period is itself a portfolio signal — it shows discipline and consistency to anyone reviewing your profile.

---

## Naming convention for files

Use lowercase with hyphens, descriptive but short:
- `writeups/thm/windows-event-logs.md` ✓
- `writeups/thm/Windows Event Logs!!!.md` ✗

The filename becomes the URL slug, so keep it clean.

---

## Pro tip: pin this repo

On your GitHub profile, click "Customize your pins" and pin `soc-portfolio` so it's the first thing visitors see. Also add the live PythonAnywhere URL to the repo's "About" section (the gear icon on the repo homepage) and to your GitHub bio.

---

## What makes this portfolio strong

1. **Consistency** — regular commits over months beats a burst of activity
2. **Depth** — a few detailed write-ups beat many shallow ones
3. **Range** — show networking, Linux, Windows, SIEM, and IR, not just one area
4. **Real work** — home lab projects and detection rules stand out more than just lab completions
5. **Communication** — clear write-ups prove you can document an investigation, which is core SOC work
