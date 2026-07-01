---
title: Common Ports Cheatsheet
date: 2026-01-10
tags: [networking, ports, reference]
summary: Quick reference for the ports every SOC analyst should know cold.
---

# Common Ports Cheatsheet

> Sample note — replace with your own.

## Must-know ports

| Port | Protocol | Service |
|------|----------|---------|
| 21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 3389 | TCP | RDP |

## Why this matters for SOC work

When you see traffic on an unexpected port, that's a signal. RDP (3389) exposed to the internet is a common attack vector. Telnet (23) should almost never be in use — it's unencrypted.
