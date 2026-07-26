---
title: Snort Cheatsheet
date: 2026-07-26
tags: [snort, ids, ips, rules, command-line]
summary: Snort command-line modes, PCAP processing syntax, and a full rule header and rule options breakdown.
---

# Snort Cheatsheet

## Global Commands

```
Snort -V
Snort -version
```
- Example: confirming the installed Snort version before relying on syntax that may differ across releases.

```
Snort -q
```
- Example: suppressing the version banner — useful when piping output into another tool or script where the banner would just add noise.

```
Snort -i eth0
```
- Example: pointing Snort at a specific network interface on a multi-interface system, rather than relying on whatever the default happens to be.

## Sniffer Mode

```
Snort -v
```
- Example: basic verbose packet sniffing — a quick first check that Snort is seeing traffic at all before building anything more complex.

```
Snort -e
```
- Example: displaying link-layer (Ethernet) headers alongside each packet — useful when MAC-address-level detail matters, e.g. investigating ARP spoofing.

```
Snort -d
```
- Example: displaying the actual data payload of each packet, not just headers — needed when the content of traffic matters, not just where it's going.

```
Snort -X
```
- Example: displaying full packet details in hex — the most granular view available, useful for confirming exactly what bytes are on the wire rather than trusting a higher-level summary.

```
Snort -eX
```
- Example: combining link-layer headers and full hex output in one pass, rather than running two separate captures to see both.

```
Snort -v -n 10
```
- Example: capturing a fixed sample of 10 packets rather than an open-ended stream — useful for a quick sanity check without flooding the terminal.

## Logger Mode

- Default log path: `/var/log/snort`

```
Snort -v -l /home/username/Desktop
```
- Example: redirecting logs to an alternative path — useful when the default log directory isn't writable or logs need to be kept somewhere specific for a case.

```
Snort -v -K ASCII
```
- Example: logging in plain ASCII rather than Snort's default binary format, making the log directly readable in a text editor without needing Snort itself to parse it back.

```
Snort -v -r snort.log
```
- Example: reading back a previously captured log file for offline review, rather than capturing live traffic.

```
Snort -v -r snort.log -n 10
```
- Example: reading only the first 10 packets from a saved log — useful for a quick look at a large capture without loading all of it at once.

```
Snort -v -r snort.log tcp
Snort -v -r snort.log 'udp and port 53'
```
- Example: applying a Berkeley Packet Filter (BPF) when reading back a log, narrowing review to just TCP traffic, or specifically DNS (UDP/53) traffic, rather than scrolling through everything captured.

## IDS/IPS Mode

```
Snort -c /etc/snort/snort.conf
```
- Example: running Snort with a full configuration file, enabling rule sets and settings rather than relying on command-line flags alone.

```
Snort -c /etc/snort/snort.conf -T
```
- Example: testing a configuration file for syntax errors before deploying it — catching a broken rule or misconfiguration ahead of time rather than after Snort fails to start.

```
Snort -c /etc/snort/snort.conf -N
```
- Example: running with logging disabled — useful when only alerting matters for a specific test, and log volume needs to stay minimal.

```
Snort -c /etc/snort/snort.conf -D
```
- Example: running Snort as a background daemon rather than tying up an active terminal session — the way it would typically run in production.

```
Snort -c /etc/snort/snort.conf -v -A none
```
- Example: verbose mode with no alert output — useful for confirming Snort is processing traffic correctly before layering alerting on top.

```
Snort -c /etc/snort/snort.conf -v -A console
Snort -c /etc/snort/snort.conf -v -A cmg
```
- Example: two different console alert output styles — useful during active testing and rule development, where alerts need to be visible immediately rather than only written to a file.

```
Snort -c /etc/snort/snort.conf -v -A fast
Snort -c /etc/snort/snort.conf -v -A full
```
- Example: two different file-based alert output formats — `fast` gives a condensed one-line-per-alert summary suited to quick review, `full` gives complete packet detail suited to deeper investigation later.

```
Snort -c /etc/snort/rules/local.rules -v -A console
```
- Example: running against a specific rules file directly, without a full configuration file — useful when testing a small, specific set of custom rules rather than an entire production ruleset.

## PCAP Processing

```
Snort -c /etc/snort/snort.conf -q -r file.pcap -A console
```
- Example: running Snort's detection engine against a single previously captured PCAP file, rather than live traffic — the core workflow for retroactively checking whether a historical capture contains anything matching current detection rules.

```
Snort -c /etc/snort/snort.conf -q --pcap-list="file1.pcap file2.pcap" -A console
```
- Example: processing several named PCAP files in one run, rather than running Snort separately against each one.

```
Snort -c /etc/snort/snort.conf -q --pcap-dir=/home/pcap-folder -A console
```
- Example: processing every PCAP file in a folder automatically — useful when a whole collection of captures needs the same rule set applied without listing each filename individually.

```
Snort -c /etc/snort/snort.conf -q --pcap-list="file1.pcap file2.pcap" -A console --pcap-show
```
- Example: same as processing multiple named files, but also printing which specific file each alert came from — useful when triaging results across a batch, to know exactly which capture is worth investigating further.

---

# Snort Rule Breakdown

A Snort rule has two logical parts: the **Rule Header** (network-based information — action, protocol, source/destination IP and port, direction) and **Rule Options** (packet-based investigation details — message, reference, flow, content).

## Rule Header

| Field | Example value | Meaning |
|---|---|---|
| Action | `alert` | Tells Snort what to do on a rule match |
| Protocol | `tcp` | Protocol to analyse — supports TCP, UDP, ICMP, IP |
| Source IP | `$EXTERNAL_NET` | Source IP address(es) |
| Source Port | `any` | Source port(s) |
| Direction | `->` | Direction operator — identifies the orientation of traffic |
| Destination IP | `$HOME_NET` | Destination IP address(es) |
| Destination Port | `$HTTP_PORTS` | Destination port(s) |

## Rule Options

| Category | Field | Keyword | Meaning |
|---|---|---|---|
| General Rule Options | Message | `msg` | Display message shown on a rule match |
| General Rule Options | Reference | `reference` | Additional information or reference for the rule (e.g. a CVE) |
| General Rule Options | Rule ID | `sid` | Unique rule number |
| General Rule Options | Revision info | `rev` | Revision information for the rule |
| Non-Payload Detection Options | Flow | `flow` | TCP stream direction |
| Payload Detection Options | Nocase | `nocase` | Disables case sensitivity to widen the content match |
| Payload Detection Options | Content | `content` | Filters the payload data, looking for an exact match |
| Payload Detection Options | Fast-pattern | `fast-pattern` | Prioritises the content search to speed up payload matching — required when using multiple `content` options |
| Post-Detection Options | Session | `session` | Extracts user data from TCP sessions |

## Example rule — Directory Traversal Attempt detection

```
alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (
msg:"Directory Traversal Attempt!";
flow:established;
nocase; content:"HTTP"; fast_pattern; content:"| 2E 2E 2F|"; content:"/..";
session:all;
reference:CVE,XXX;
sid:100001; rev:1;)
```
- Example: an alert rule watching for a classic directory traversal pattern — `2E 2E 2F` in hex is `../`, and the rule looks for that sequence following an HTTP request, regardless of letter case, to catch an attacker attempting to escape a web root and read arbitrary files on the server.

Source: [TryHackMe Snort room](https://tryhackme.com/room/snort)
