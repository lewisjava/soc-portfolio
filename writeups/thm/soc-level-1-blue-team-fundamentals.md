---
title: SOC Level 1 — Blue Team Fundamentals
platform: TryHackMe
difficulty: easy
date: 2026-06-27
tags: [SOC Level 1, Blue Team, Fundamentals]
summary: The structure of a SOC's blue team, and the two attack surfaces every analyst needs to think about — humans and systems.
---

# SOC Level 1 — Blue Team Fundamentals

## Where the L1 analyst sits

SOC Level 1 is the junior analyst role — the first line of defence.

- **Red team** — offensive experts, penetration testers, and ethical hackers.
- **GRC team** — specialists managing policy and compliance.
- **Blue team** — defensive security experts.

Inside the SOC itself:

- **L1 analyst** — junior role, triages incoming alerts and passes escalations to L2.
- **L2 analyst** — investigates more advanced attacks.
- **Engineers** — experts in configuring security tools like EDR or SIEM.
- **Manager** — manages the team.

![SOC team structure](/static/images/writeups/soc-level-1-blue-team-fundamentals/soc-team-structure.png)

Beyond the SOC itself sits the **CIRT** (Cyber Incident Response Team) — the advanced team that handles what the blue team can't.

![CIRT position relative to the SOC](/static/images/writeups/soc-level-1-blue-team-fundamentals/cirt-team.png)

## Advancing a SOC career

Start as L1, practising alert handling. Try CTFs, stay current with cyber news, and consider certifications like TryHackMe's SAL1. Prepare for interviews, and understand the difference between working an internal SOC versus a Managed Security Service Provider (MSSP) before applying.

| Topic | Internal SOC | MSSP |
|---|---|---|
| Scenario example | Working within a bank, protecting its own systems | Working for a global MSSP protecting sixty customers across Europe |
| Working pace | Usually calmer shifts, less time pressure | Shifts often start with a queue of urgent alerts |
| Security tools | A few tools, but deep familiarity with them | Sixty diverse tools and platforms |
| Incident practice | Might see two major attacks a year | Deals with attacks and breaches weekly |

## Attack surface one: humans

Sometimes the easiest way to gain access isn't hours of enumeration looking for exploits — it's a phishing email.

| Attack Example | Attacker's Next Step |
|---|---|
| Breach the Google account of an HR manager | Steal and sell the entire employee database |
| Trick a wealthy individual into running malware | Hijack a web banking session from their PC |
| Breach an IT administrator's account | Access the heart of a large corporate network |
| Trick a government worker into sharing secrets | Use the information to simplify future attacks |

Social engineering exploits human psychology rather than technical flaws. For the tactic to succeed it needs to be:

- **Trustworthy** — the attacker appears legitimate so the victim trusts them.
- **Emotional** — the attack triggers urgency, fear, or curiosity.

Common vectors: **phishing** (stealing login credentials), **malware downloads** (tricking a user into installing malware), and **deepfakes** (impersonating someone within the company on a video call).

Defending against attacks on humans involves two key tasks: mitigation and detection.

![Defending against human-targeted attacks](/static/images/writeups/soc-level-1-blue-team-fundamentals/defending-humans.png)

## Attack surface two: systems

| Breached System | Attack Value |
|---|---|
| A student's personal laptop | Steal a Steam profile, add the PC to a botnet |
| A bank's senior IT administrator's laptop | Access internal banking systems |
| A law firm's mail server | Dump all mailboxes, blackmail the victim |
| A server at the heart of an industrial network | Encrypt the whole network with ransomware |
| A government website's management panel | Deface the website content |

The first goal is gaining access to the target system — what happens next depends on the attacker's motive.

**Human-led attacks** — the system owner is usually inadvertently the main cause, with 81% of breaches involving stolen or leaked passwords.

**Vulnerabilities** — every piece of software can have a security flaw. In 2024, over 40,000 vulnerabilities were published, with more than 300 used in major attacks. Once found, they need to be patched.

**Supply chain attacks** — a home PC connects to hundreds of apps, browsers, and pieces of software, each depending on thousands of libraries. Exploiting just one of these entry points can compromise everything and lead to further escalation.

**Misconfiguration** — a mistake in how a system was set up, often by the IT team, and these happen frequently.

![Example of a system misconfiguration](/static/images/writeups/soc-level-1-blue-team-fundamentals/misconfiguration-example.png)

Misconfigurations don't require a software update to fix — just a better setup. As an analyst, you'll often only spot them after a threat actor has already exploited one. In smaller companies you might also take a more proactive role:

- **Penetration testing** — hiring ethical hackers to simulate an attack and report on discovered flaws.
- **Vulnerability scans** — periodically running tools to detect default passwords or outdated software.
- **Configuration audits** — manually reviewing systems against best practices like CIS benchmarks.
