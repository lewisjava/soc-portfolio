---
title: Pyramid of pain
date: 2026-07-09
tags: [Framework, conceptual]
summary: An understanding of how to apply the Pyramid Of Pain framework to cybersecurity concepts
---

# Pyramid of Pain

The pyramid of pain is a conceptual framework created by David J. Bianco that ranks threat indicators based on how difficult and costly it i for an attacker to change them when detected helping security teams prioritize threat intelligence and maximize operational disruption. The levels to the pyramid of pain are ranked as such
1. Trivial
2. Easy
3. Simple
4. Annoying
5. Challenging
6. Tough!

### Trivial
Hash values - Digital fingerprints of files such as MD5, SHA-256
This is considered trivial as changinge a single byte in the code or recompiling generates a completely new hash

### Easy
IP Addresses - Numeric identifiers for internet locations
This is considered easy as attackers frequently rotate through VPNs, proxies or cloud infrastructure

### Simple
Domain names - Web addresses used by attackers for command and control or phishing
Considered simple because although it costs a time and money to register a domain, attackers often use automated generators or dynamic DNS to switch them

### Annoying
Network and host artifacts - Traces left on systems or networks such as specific reg keys, mutexes or unsual user-agent strings.
Considered annoying as attackers have to modify their underlying code or alter howthey interact with a victims machine.

### Challenging
Tools - The software, scripts, or RATs used to carry out the attack
Considered challening as developing o acquiring new proprietary tooling takes significant time, skill and resources.

### Tough!
Tactics, techniques and procedures - the adversary's overall behavioural patern and methodology.
Considered tough as it represents the attackers habits and srategic aroach, having to alter these means retraining operators and entirely rethinking their attack strategies.

---
- **Pyramid of pain**
- **2026/07/09**
- **Conceptual, Framework**
- **An overview of the pyramid of pain framework**
