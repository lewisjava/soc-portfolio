---
title: SOC Fundamentals
date: 2026-06-17
tags: [soc, fundamentals, people-process-technology]
summary: What a SOC actually is, the detect/respond split, and the People, Process, Technology model that underpins how one operates.
---

# SOC Fundamentals

A SOC (Security Operations Centre) is a dedicated facility operated by a specialised security team who continuously monitor an organisation's network and resources to identify suspicious activity, 24 hours a day, 7 days a week.

## Purpose and components

The main focus of the team is to keep **detection** and **response** intact.

### Detection

- **Detect vulnerabilities** — if the SOC can discover a vulnerability, they can fix it before it's exploited.
- **Detect unauthorised activity** — if someone has stolen an employee's credentials and logs in, they can cause serious damage. The SOC must be able to spot this — clues like geographical location can help.
- **Detect policy violations** — policies are set by the company via security policies and organisational units, so this varies from company to company.
- **Detect intrusions** — unauthorised access to systems and networks, such as exploitation of a web application.

### Response

Supports the incident response process.

## The three pillars of a SOC

**People, Process, and Technology** all coexist within a SOC environment.

### People

- **SOC Analyst (Level 1)** — anything detected by the security solution passes through this analyst first. They perform basic alert triage to determine if a detection is harmful.
- **SOC Analyst (Level 2)** — helps dive deeper into investigations and correlates data from multiple sources to perform proper analysis.
- **SOC Analyst (Level 3)** — very experienced. Critical severity detections reported by L1/L2 are often security incidents needing detailed responses, including containment, eradication, and recovery — this is where L3 comes in.
- **Security engineer** — while all analysts work on security solutions, engineers deploy and configure them.
- **Detection engineer** — independently creates security rules and the logic behind security solutions.
- **SOC manager** — manages the processes the SOC team follows, and is in contact with the org's CISO (Chief Information Security Officer).

### Process

- **Alert triage** — the basis of the SOC team's work. The first response to any alert is to triage it, focusing on analysing the specific alert by answering the 5 W's: Who? What? Where? When? Why?

![Alert triage — answering the 5 W's](/static/images/notes/detection-monitoring/5ws-alert-triage.png)

- **Reporting** — harmful alerts need to be escalated to higher-ups as tickets, assigned to the relevant people. The report should include the answers to all 5 W's along with a thorough analysis, ideally with screenshots.
- **Incident response and forensics** — if a reported detection is critical, these scenarios require a high-level team to initiate an incident response. Sometimes a detailed forensics activity also needs to be performed.

### Technology

- **SIEM** — a Security Information and Event Manager, a universal tool in SOC environments. Collects logs and has detection rules configured. It provides detections and correlates them with log sources and alerts when a match with any rule occurs. Provides only the *detection* capability in a SOC.
- **EDR** — Endpoint Detection and Response. Provides real-time and historical visibility of devices, operating at the endpoint level with extensive detection capabilities.
- **Firewall** — the most well-known tool, purely for network security. Acts as a barrier between internal and external networks and monitors traffic.
