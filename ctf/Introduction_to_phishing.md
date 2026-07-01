---
title: Introduction to Phishing
platform: TryHackMe
difficulty: easy
date: 2026-01-20
tags: [SOC simulator]
summary: Monitor and analyze real-time alerts
---

# Your Title Here

Introduction to Phishing

## A section heading

Analyze and investigate realistic phishing alerts from a SIEM


## Code blocks


## Tables

## Lists

- First alert was a false positive triggered by an email containing a link that would
Direct the user to a website, the email was from another user within the company and the link
claimed to take the recipient to an onboarding video. During investigation the link was 
tested on the VM and took me to a non-malicious website, looking through splunk I found
through various emails that the recipient was intended to recive an onboarding video.
Therefore I came to the conclusion the email was legit.
- The second alert came from a more suspicious email that claimed to be from amazon
claiming the recipient MUST click the link and update their delivery address to receive a parcel.
Looking at the email their are several attack indicators, firstly the email is spoofed and misspelled,
Secondly the link within the email address when scanned by virustotal is shown to be a malicious link.
Therefore after investigation the alert was classified as a true positive but does not need
escalating as the email was blocked.
- Third point

---

## Frontmatter field reference

The block between the `---` lines at the top is the "frontmatter". Fields:

- **title** — Introduction to Phshing
- **platform** — TryHackme
- **difficulty** — Easy
- **date** — 2026-05-27.
- **tags**
- **summary** — Introduction to phishing and triage.
