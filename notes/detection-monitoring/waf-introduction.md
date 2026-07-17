---
title: WAF Introduction
date: 2026-06-21
tags: [waf, owasp, detection-evasion]
summary: How web application firewalls work, signature vs behavioural detection, and their real-world limitations against logic-based attacks.
---

# WAF Introduction

A Web Application Firewall (WAF) is, at its core, a firewall that inspects HTTP/S traffic. Like regular firewalls, it comes in many types, from stateless to next-gen. WAFs speak HTTP fluently, so they can parse methods, headers, cookies, query strings, and POST bodies to enforce policies against threats such as SQL injection, XSS, and file injection.

A WAF strives to protect against the OWASP Top 10 web application security vulnerabilities. Beyond regular firewalls, a WAF understands attacks that target web applications specifically — for example, recognising `?id=1' OR '1'='1'` as a SQL injection probe, or `<img src=x onerror=alert(1)>` as a browser-executable XSS vector.

## Deployment models

| Model | Description | Common Examples |
|---|---|---|
| Cloud-based (Reverse Proxy) | Traffic routed through vendor infrastructure (e.g. via DNS). WAF terminates TLS. | Cloudflare, AWS WAF, Akamai, Imperva Cloud |
| Network Appliance | Physical or virtual in-line device, often paired with a load balancer. | F5 Advanced WAF, Fortinet WAF, Barracuda WAF |
| Host-based (Embedded) | A module within the web server (e.g. Apache/Nginx). | ModSecurity + OWASP Core Rule Set (CRS) |

## Fingerprinting a WAF

Understanding how a WAF can be identified helps an analyst understand attacker reconnaissance behaviour, which shows up in logs.

**Passive header inspection** — a `curl -I` request against the target might reveal common cloud WAF headers:

- `server: cloudflare` for Cloudflare
- `X-Sucuri-ID` for Sucuri
- `X-CDN: Imperva` for Incapsula/Imperva
- `Akamai-Origin-Hop: 2` for Akamai
- `X-F5-Application: ASM` for F5 Advanced WAF

**Behavioural analysis** — sending a request that looks malicious to provoke a diagnostic response:

- `' OR 1=1--` should trigger a SQLi signature
- `<script>alert(1)</script>` matches an XSS signature
- `../../../../etc/passwd` activates an LFI signature

| Response | Likely Meaning |
|---|---|
| `403 Forbidden`, blank page | Classic WAF block |
| `406 Not Acceptable` | Common in ModSecurity CRS |
| Custom "Access Denied" HTML page | Vendor-specific (Fortinet, Barracuda, etc.) |
| Delayed response (>500ms) | WAF inspection overhead |
| No change from normal | Possibly no WAF present |

**Automated fingerprinting** — tools like WAFW00F issue a baseline probe, analyse the response/headers/status codes, and escalate with a controlled set of test requests if results are inconclusive.

## Signature-based vs behavioural detection

A signature-based WAF says: "I know what a knife looks like." A behavioural WAF says: "I know how a benign use of a knife looks, and how someone holding it maliciously moves." Both can be fooled by mimicry.

Attackers evade signature matching through:

- **Encoding** — e.g. `' OR 1=1--` encoded as `%27%20OR%201%3D1--`
- **Case variation** — `UNION SELECT` written as `unIOn sElEcT`
- **Comment insertion** — inserting comments to break up a matched pattern
- **Alternative syntax** — e.g. `1' AND SLEEP(10)--` rewritten as `1' AND IF(1=1, SLEEP(10), 1)--`

| Signature-based | Advantages | Disadvantages |
|---|---|---|
| | Low false positives when tuned | Blind to obfuscation (encoding, comments) |
| | Easy to write and understand | Can't detect zero-day attacks |
| | High performance | Requires constant updates |

| Behavioural | Advantages | Disadvantages |
|---|---|---|
| | Catches unknown (zero-day) attacks | High false positives (e.g. blocks legitimate long forms) |
| | Harder to bypass with simple encoding | Requires a training/learning period |
| | Adapts to application logic over time | Computationally expensive |

Most commercial WAFs are hybrid, using both approaches.

## Anatomy of a real rule

The following is from the OWASP Core Rule Set v3.3.7:

```apacheconf
SecRule REQUEST_BASENAME "@detectSQLi" \
    "id:942101,\
    phase:2,\
    block,\
    capture,\
    t:none,t:utf8toUnicode,t:urlDecodeUni,t:removeNulls,\
    msg:'SQL Injection Attack Detected via libinjection',\
    logdata:'Matched Data: %{TX.0} found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    tag:'attack-sqli',\
    tag:'OWASP_CRS',\
    tag:'PCI/6.5.2',\
    severity:'CRITICAL'"
```

- `SecRule REQUEST_BASENAME "@detectSQLi"` — the trigger. `REQUEST_BASENAME` refers to the filename/endpoint in the URL path. `@detectSQLi` calls libinjection, which tokenises input like a real SQL parser rather than matching raw strings.
- `id:942101` / `phase:2` / `block` / `capture` — rule identity (part of CRS's numbering scheme), when it runs (request body processing), the action taken, and that the matched payload is saved for logging.
- `t:none`, `t:utf8toUnicode`, `t:urlDecodeUni`, `t:removeNulls` — input normalisation before detection runs, handling encoding tricks and null-byte termination attempts.
- `msg` / `logdata` — human-readable alert and rich forensic detail (the exact matched payload, which variable was inspected, its full value) that shows up in logs and the SIEM.
- `tag:'PCI/6.5.2'` — links the rule to a PCI DSS compliance requirement; `tag:'attack-sqli'` and `tag:'OWASP_CRS'` are operational hooks used for correlation and reporting, not just labels.

## Limitations

A WAF only works as well as its rules, and it doesn't understand application logic:

- **IDOR (Insecure Direct Object Reference)** — changing `GET /api/user/123` to `.../124` uses no special characters or malicious payloads, so nothing triggers a block.
- **Authorisation bypass** — a user accessing `/admin` without admin rights looks like a completely benign URL to a WAF.
- **Race conditions and replay attacks** — involve no malicious syntax for a WAF to detect.

In short: WAFs filter *syntax*, not *intent*. They can't fix broken access controls. Encrypted traffic is a blind spot unless it's decrypted for inspection, client-side attacks fly under the radar since WAFs inspect server-bound traffic, and poorly configured WAF rules can themselves introduce new attack surfaces (e.g. RCE via badly-escaped dynamic rule construction, or DoS via expensive regex on large payloads).
