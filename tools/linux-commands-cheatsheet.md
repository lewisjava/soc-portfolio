---
title: Linux Commands Cheatsheet
date: 2026-01-11
tags: [linux, commands, reference]
summary: Quick reference for the Linux commands every SOC analyst will use.
---

# Linux Commands Cheatsheet

> The most common commands for traversing and investigating Linux systems.

## Must-know commands

| Command | What it does | Example |
|------|----------|---------|
| grep | Searches for specific strings | grep -ri "malicious_ip" /var/log |
| tail -f | Monitor logs in real time | tail -f /var/log/auth.log |
| find | Locate files modified in the last 24 hours (good for finding web shells) | find /var/www -mtime -1 |
| awk | Analyses logs to count unique IP addresses or specific columns | awk '{print $1}' access.log \| sort \| uniq -c |
| sed | Extract specific line ranges from files without opening | sed -n '5,10p' file.txt |
| strings | Extract human readable data from binaries to find hidden URLs/IPs | strings /tmp/susp_bin |
| ss -tulpn | Displays all listening ports and the PIDs owning them | ss -tulpn |
| netstat -pant | Displays active network connections associated with PIDs | netstat -pant |
| tcpdump | Capture network traffic for Wireshark analysis | tcpdump -i eth0 -w capture.pcap |

## Why this matters for SOC

These are some of the most common commands used for traversing and investigating Linux systems.
