---
title: Windows Event Logs — TryHackMe
platform: TryHackMe
difficulty: easy
date: 2026-01-15
tags: [windows, event-logs, soc, blue-team]
summary: Walking through Windows Event Log analysis — understanding key Event IDs and using Event Viewer and wevtutil to investigate suspicious activity.
---

# Windows Event Logs

> Windows Event logs and how to understand them

## Room overview

This room covers Windows Event Logs and how SOC analysts use them to detect malicious activity. Event logs are one of the most important data sources in any investigation.

## Key Event IDs to know

| Event ID | Meaning |
|----------|---------|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4688 | Process creation |
| 4720 | User account created |
| 7045 | New service installed |

## Tools used

- **Event Viewer** — the built-in GUI for browsing logs
- **wevtutil** — command-line tool for querying logs
- **PowerShell** — `Get-WinEvent` for filtering and automation

## Example: finding failed logons

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} | Select-Object TimeCreated, Message
```

This pulls all failed logon events. A burst of these from one source followed by a `4624` (success) is a classic **brute force** pattern.

## What I learned

Event logs tell a story. The skill isn't memorising every ID — it's knowing which ones matter for a given attack and being able to correlate them across a timeline.

## Takeaway

Event ID 4688 with command-line logging enabled is gold for detecting malicious process execution. Always check whether it's enabled in an environment.
