---
title: Common commands Cheatsheet
date: 2026-01-11
tags: [linux, commands, reference]
summary: Quick reference for the linux commands every SOC analyst will use.
---

# Common commands Cheatsheet

> List of most common commamds.

## Must-know ports

| command | what it does | example |
|------|----------|---------|
| grep | searches for specific strings | grep -ri "malisious_ip" /var/log |
| tail -f | monitor logs in real time | tail -f /var/log/auth.log |
| find | locate files modifid in the last 24 hours (good for finding web shells | find /var/www -mtime -1 |
| awk  | analyses logs to count unique IP addresses or specific colums | awk '{print $1}' access.log 'pipe'  sort 'pipe' uniq -c |
| sed | extract specific line ranges from files without opening | sed -n '5,10p' file.txt |
| strings | extract human readable data from binaries to find hidden urls/IP's | strings /tmp/susp_bin |
| ss -tulpn | displayes all listening ports and the PID's owning them  | ss -tulpn |
| netstat -pant  | displays active network connections associated with PIDS  | netstat -pant |
|tcpdump   | capture network traffic for wireshark analysis  |tcpdump -i eth0 -w capture.pcap |
## Why this matters for SOC

These are some of the most common commands used for traversing and investigating linux systems
