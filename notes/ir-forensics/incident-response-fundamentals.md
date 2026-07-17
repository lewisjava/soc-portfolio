---
title: Incident Response Fundamentals
date: 2026-06-18
tags: [incident-response, sans, nist, picerl]
summary: True vs false positives, incident types, and the SANS PICERL framework for handling incidents end to end.
---

# Incident Response Fundamentals

Incident response handles an incident from start to end — from deploying security in several areas to prevent incidents, to fighting them and minimising their impact. It's a thorough guideline for the whole lifecycle.

## What are incidents

So many events run on a device that a massive volume of events and logs gets created — some of which point to bad things taking place. Security solutions digest these events into logs and surface the harmful activity.

Alerts raised by a security solution may be **false positives** (nothing is actually happening) or **true positives** (something bad is genuinely taking place).

**False positive example:** a security solution raises an alert on a high volume of data being transferred to an external IP. Investigation finds the system was undergoing a routine backup to cloud storage — a false positive.

**True positive example:** a security solution raises an alert on a phishing attempt against a user. Investigation confirms the email was genuinely malicious — a true positive.

True positives are also known as **incidents**. The next phase is assigning a severity level.

## Types of incidents

- **Malware infections** — the majority of incidents are associated with malware.
- **Security breaches** — an unauthorised person gains access to confidential data.
- **Data leaks** — confidential information exposed to unauthorised entities, sometimes used for reputational damage or extortion, sometimes accidental due to human error or misconfiguration.
- **Insider attacks** — incidents originating from within the organisation, e.g. disgruntled employees.
- **Denial of service** — an attack on availability, one of the three pillars of the CIA triad.

## The incident response process

Because incidents vary wildly depending on the actor, the organisation, and the circumstances, it makes sense to follow a framework. The two most common are **SANS** and **NIST**.

SANS offers various courses and certifications in cybersecurity; NIST develops standards and guidelines.

### SANS framework — PICERL

Six phases, remembered by the acronym PICERL:

1. **Preparation** — building resources to handle incidents: developing response teams, having a response plan, and deploying necessary security solutions.
2. **Identification** — looking for abnormal behaviour that may indicate an incident.
3. **Containment** — limiting the spread and impact of the incident.
4. **Eradication** — removing the root cause of the incident from the environment.
5. **Recovery** — restoring systems to normal operation.
6. **Lessons Learned** — reviewing what happened and improving the process for next time.
