---
title: MITRE ATT&CK Framework
date: 2026-06-15
tags: [mitre, attack, ttp, threat-intel]
summary: The core building blocks of ATT&CK — tactics, techniques, sub-techniques, procedures — and who actually uses the framework day to day.
---

# MITRE ATT&CK Framework

ATT&CK is a model that attempts to systematically categorise adversary behaviour. The main components:

- **Tactics** — the *why*, the reason the adversary is performing an action.
- **Techniques** — *how* adversaries achieve tactical goals by performing an action.
- **Sub-techniques** — a more specific, lower-level description of adversarial behaviour.
- **Procedures** — the specific, in-the-wild implementation an adversary uses for a technique or sub-technique.

The [MITRE ATT&CK matrix](https://attack.mitre.org/matrices/) is a visual representation of all tactics and techniques in the framework. The [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) allows annotating and exploring matrices.

## Worked example

- **Tactic** — an attacker wants to perform reconnaissance on their target. This is the attacker's goal.
- **Technique** — they use Active Scanning to achieve that goal.
- **Sub-technique** — Active Scanning comprises three specific methods: Scanning IP Blocks, Vulnerability Scanning, or Wordlist Scanning.

## Why ATT&CK matters

It provides a standard, consistent language for describing adversary behaviour.

**Threat intelligence and defence:** ATT&CK bridges the gap between threat intelligence and defensive operations. A threat report might describe *what* an attacker did without explaining *how* to turn that into usable detection logic. By mapping threat activity to TTPs, defenders can translate intelligence into real detection logic, queries, and playbooks.

## Who uses ATT&CK

- **Cyber threat intelligence** — collects and analyses info to improve an org's security posture, mapping observed threat actor behaviour to ATT&CK TTPs to create actionable profiles across the industry.
- **SOC analysts** — investigate and triage security threats, linking activity to tactics and techniques to provide detailed context for alerts and prioritise incidents.
- **Detection engineers** — design and improve detection systems, mapping SIEM/EDR rules to ATT&CK to ensure better detection coverage.
- **Incident responders** — respond to and investigate incidents, mapping incident timelines to MITRE tactics and techniques to better visualise the attack.
