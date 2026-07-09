---
title: Introduction to Phishing — SOC Simulator
platform: TryHackMe
difficulty: easy
date: 2026-05-27
tags: [SOC simulator, phishing, triage]
summary: My first SOC triage — monitoring and analysing real-time phishing alerts in the TryHackMe SOC simulator.
---

# Introduction to Phishing — SOC Simulator

My first SOC triage: analysing and investigating realistic phishing alerts from a SIEM in TryHackMe's SOC simulator.

## Alert 1 — False positive

The first alert was a false positive triggered by an email containing a link that would direct the user to a website. The email was from another user within the company and the link claimed to take the recipient to an onboarding video.

During investigation the link was tested in the VM and led to a non-malicious website. Looking through Splunk, I found through various emails that the recipient was indeed intended to receive an onboarding video.

**Verdict:** the email was legitimate — false positive.

## Alert 2 — True positive

The second alert came from a more suspicious email that claimed to be from Amazon, claiming the recipient MUST click the link and update their delivery address to receive a parcel.

Looking at the email there are several attack indicators:

- The sender address is spoofed and misspelled
- The link within the email, when scanned with VirusTotal, is shown to be malicious

**Verdict:** true positive — but it did not need escalating, as the email was blocked before reaching the user.

## Feedback / lessons learned

Need to improve my reporting — include the 5 W's (who, what, when, where, why) in every investigation summary.

---

[View the public summary of this investigation on TryHackMe →](https://tryhackme.com/soc-sim/public-summary/1da5fb6457c9957da637d0341611f99c217f6b3f0eadba6079a53f5f36a2f611de3df097d74d7a91b53d62017b6427d3)
