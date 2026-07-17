---
title: SOC Level 1 — Alert Triage, Reporting and Metrics
platform: TryHackMe
difficulty: easy
date: 2026-06-28
tags: [SOC Level 1, Alert Triage, SOC Metrics]
summary: The full lifecycle of an L1 alert — from event to triage to escalation — plus the metrics a SOC uses to measure whether it's actually working.
---

# SOC Level 1 — Alert Triage, Reporting and Metrics

## Events and alerts

Before anything, an **event** must occur — this can range from a user logon to a process launch to a file download. That event gets logged by the system, OS, or firewall, and the logs get sent to a SIEM or an EDR.

An **alert** occurs when a specific event, or sequence of events, requires attention. Alerts are what save an analyst from sifting through thousands of raw logs.

Alert management platforms include:

- **SIEM** — Security Information and Event Manager
- **EDR** — Endpoint Detection and Response
- **SOAR** — Security Orchestration, Automation, and Response (for bigger SOC teams)
- **ITSM** — IT Service Management, a ticketing system

![Alert management platforms](/static/images/writeups/soc-level-1-alert-triage-and-metrics/alert-management-platforms.png)

The L1 analyst is the first line of defence, dealing with the majority of incoming alerts.

## Alert properties

![Alert properties breakdown](/static/images/writeups/soc-level-1-alert-triage-and-metrics/alert-properties.png)

| # | Property | Description | Examples |
|---|---|---|---|
| 1 | Alert Time | Alert creation time — usually a few minutes after the actual event | Alert 15:35, Event 15:32 |
| 2 | Alert Name | A summary based on the detection rule's name | Unusual Login Location, Windows RDP Bruteforce |
| 3 | Alert Severity | Urgency, initially set by detection engineers, adjustable by analysts | 🟢 Low, 🟡 Medium, 🟠 High, 🔴 Critical |
| 4 | Alert Status | Whether someone is working the alert or triage is complete | New, In Progress, Closed |
| 5 | Alert Verdict | Whether the alert is a real threat or noise | True Positive, False Positive |
| 6 | Alert Assignee | The analyst reviewing the alert | — |
| 7 | Alert Description | The rule's logic, why the activity could indicate an attack, and optionally how to triage it | — |
| 8 | Alert Fields | Analyst comments and the specific values that triggered the alert | Affected hostname, entered command line |

## Alert prioritisation

Alerts don't get worked in the order they arrive. The most common approach:

1. **Filter the alerts** — take only new, unseen, unresolved alerts. Don't duplicate work already claimed by a teammate.
2. **Sort by severity** — critical first, then high, medium, low. Detection engineers design rules so critical alerts are far more likely to be real, high-impact threats.
3. **Sort by time** — oldest first. If two alerts both concern breaches, the older one likely has an attacker already further into the attack chain.

## Alert triage process

Once an alert is chosen, triage begins — a process-heavy sequence where every step matters.

![Alert triage flow](/static/images/writeups/soc-level-1-alert-triage-and-metrics/alert-triage-flow.png)

**Initial steps:**

1. Assign the alert to yourself.
2. Move it into "in progress."
3. Familiarise yourself with its name, description, and key indicators.
4. Begin the investigation stage.

**Investigation** — the most complex step, applying technical knowledge to assess legitimacy across SIEM and EDR logs:

1. Understand who is under threat — the affected user, hostname, cloud resource, network, or website.
2. Note the action described in the alert — a suspicious login, malware, or phishing.
3. Review surrounding events for suspicious activity shortly before or after the alert.
4. Use threat intel platforms or other resources to verify assumptions.
5. Move to final actions.

**Final actions:**

1. Decide if the alert is malicious (true positive) or not (false positive).
2. Prepare a detailed comment explaining the analysis steps and verdict reasoning, then close the case.

## Reporting

Before closing or passing an alert to L2, it often needs a full report rather than a short comment — especially for true positives.

| Purpose | Why it matters |
|---|---|
| Provide context for escalation | Saves L2 analysts time and helps them quickly understand what happened |
| Save findings for the record | Raw logs are only stored 3–12 months, but alerts are kept indefinitely, so context needs to live in the alert itself |
| Improve investigation skills | If you can't explain it simply, you don't understand it well enough — writing reports sharpens L1 skills |

**Report format — the 5 W's:**

- **Who** — which user logged in, ran the command, or downloaded the file
- **What** — the exact action or event sequence
- **When** — when the suspicious activity started and ended
- **Where** — which device, IP, or website was involved
- **Why** — the most important W — the reasoning behind the final verdict

![Report format structure](/static/images/writeups/soc-level-1-alert-triage-and-metrics/report-format.png)

**Escalation guide** — generally escalate to L2 when:

- The alert indicates a major cyberattack requiring deeper investigation or DFIR.
- Remediation actions are required (malware removal, host isolation, password reset).
- Communication with customers, partners, management, or law enforcement is needed.
- You don't fully understand the alert and need help from a more senior analyst.

## SOC communication

Reports should be straightforward and logical, but critical or unusual scenarios can complicate this. Ideally the team has its own crisis communication procedures.

![Communication case examples](/static/images/writeups/soc-level-1-alert-triage-and-metrics/communication-cases.png)

- **Urgent alert, L2 unavailable for 30 minutes** — know your emergency contacts. Try L2, then L3, then your manager.
- **Slack/Teams account compromise needs user validation** — never contact the user through the potentially breached channel; use an alternative method like a phone call.
- **Overwhelming volume of alerts, some critical** — prioritise per the standard workflow, but inform your L2 of the situation.
- **You realise days later you misclassified an alert** — reach out to L2 immediately. Threat actors can stay silent for weeks before causing impact.
- **SIEM logs aren't parsing or searching correctly** — don't skip the alert. Investigate what you can and flag the tooling issue to L2 or an engineer.

## SOC metrics and objectives

The efficiency of a SOC can be measured, most commonly via:

- **MTTD** — Mean Time to Detect: average time to identify a security threat or issue.
- **MTTA** — Mean Time to Acknowledge: average time between the initial alert and the analyst starting triage.
- **MTTR** — Mean Time to Respond: average time between the initial alert and actually stopping the breach from spreading.

## Core metrics

| Metric | Formula | Measures |
|---|---|---|
| Alerts Count | Total alerts received | Overall SOC analyst load |
| False Positive Rate | False positives ÷ total alerts | Level of noise in alerts |
| Alert Escalation Rate | Escalated alerts ÷ total alerts | Experience level of L1 analysts |
| Threat Detection Rate | Detected threats ÷ total threats | Reliability of the team |

Rough healthy targets: 5–30 alerts per L1 analyst per day. False positive rate above 80% signals a real noise problem needing remediation. Alert escalation rate should ideally stay below 50%. Threat detection rate should always aim for 100%.

## SLA metrics

An alert alone doesn't stop a breach — timely reception, triage, and response do. These are usually agreed with management under a Service Level Agreement (SLA).

![SLA metric targets](/static/images/writeups/soc-level-1-alert-triage-and-metrics/sla-metrics.png)

| Metric | Common Target | Description |
|---|---|---|
| Team Availability | 24/7 | Working schedule — 8/5 or full 24/7 coverage |
| Mean Time to Detect | 5 minutes | Average time between the attack and its detection |
| Mean Time to Acknowledge | 10 minutes | Average time for L1 to start triage on a new alert |
| Mean Time to Respond | 60 minutes | Average time to actually stop the breach spreading |

## Improving metrics

| Issue | Recommendations |
|---|---|
| False Positive Rate over 80% | Exclude trusted activity (e.g. system updates) from detection rules; consider automating triage for the most common alert types |
| MTTD over 30 minutes | Ask engineers to tune detection rules to run faster or more frequently; check SIEM logs are ingesting in real time |
| MTTA over 30 minutes | Ensure analysts are notified in real time on new alerts; distribute the queue evenly across the shift |
| MTTR over 4 hours | As L1, escalate to L2 as quickly as possible; make sure the team has documented playbooks for common attack scenarios |
