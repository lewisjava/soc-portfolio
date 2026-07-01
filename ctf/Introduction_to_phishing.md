---
title: Introduction to Phishing
platform: TryHackMe
difficulty: easy
date: 2026-01-20
tags: [SOC simulator]
summary: Monitor and analyze real-time alerts
---

# Introduction to phishing

My first SOC triage

## Phishing emails and dodgy links.

Analyze and investigate realistic phishing alerts from a SIEM

## Alerts

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

## Feedback
Need to improve my reporting, include the 5 W's.

---

- **title** — Introduction to Phshing
- **platform** — TryHackme
- **difficulty** — Easy
- **date** — 2026-05-27.
- **summary** — Introduction to phishing and triage.
- **link** - https://tryhackme.com/soc-sim/public-summary/1da5fb6457c9957da637d0341611f99c217f6b3f0eadba6079a53f5f36a2f611de3df097d74d7a91b53d62017b6427d3
