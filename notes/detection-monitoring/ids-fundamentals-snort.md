---
title: IDS Fundamentals — Snort
date: 2026-06-20
tags: [ids, snort, rules]
summary: Snort rule anatomy and the commands to create and run detection rules, including against PCAP files.
---

# IDS Fundamentals — Snort

Snort is the most popular IDS available.

`ls /etc/snort` lists all the files and folders present in Snort's main directory.

## Rule format

![Snort rule format breakdown](/static/images/notes/detection-monitoring/snort-rule-format.png)

- **Action** — specifies which action to take when the rule triggers. For example, `alert` when traffic matches the rule.
- **Protocol** — the protocol that matches this rule, e.g. `ICMP` when pinging a host.
- **Source IP** — the IP originating the traffic. Setting this to `any` detects traffic from any source IP.
- **Source port** — the port from which traffic originates. `any` detects traffic from any source port.
- **Destination IP** — the destination IP the matching traffic is heading to; it generates the alert. `$HOME_NET` is a variable defined in Snort's configuration file as the whole network's range.
- **Destination port** — the port the traffic would reach. `any` detects traffic to any port.
- **Rule metadata** — defined at the end of the rule in parentheses:
  - **Message (msg)** — describes what triggered the rule, e.g. "Ping Detected".
  - **Signature ID (sid)** — a unique identifier differentiating this rule from others.
  - **Rule revision (rev)** — the revision number, incremented every time the rule is modified, helping track changes.

## Rule creation

```
sudo nano /etc/snort/rules/local.rules
```

Paste in a rule, for example:

```
alert icmp any any -> 127.0.0.1 any (msg:"Loopback Ping Detected"; sid:10003; rev:1;)
```

Then start Snort to detect anything defined in the rule file:

```shell-session
sudo snort -q -l /var/log/snort -i lo -A alert_fast -c /etc/snort/snort.lua
```

Pinging the loopback address (`127.0.0.1`) will trigger the "Loopback Ping Detected" alert.

## Running Snort against PCAP files

```shell-session
sudo snort -q -l /var/log/snort -r Task.pcap -A alert_fast -c /etc/snort/snort.lua
```
