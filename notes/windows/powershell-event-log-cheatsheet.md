---
title: PowerShell Event Log Investigation Cheatsheet
date: 2026-07-26
tags: [Windows Security, log analysis, powershell commands]
summary: Get-WinEvent syntax for filtering, hunting, correlating, and exporting Windows and Sysmon event logs during an investigation.
---

# PowerShell Event Log Investigation Cheatsheet

## Windows Event IDs — Security Log

| Event ID | Meaning |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4720 | User created or added |
| 4732 | Member added to a security-enabled local group |
| 1102 | Audit log was cleared — a strong anti-forensic indicator, worth hunting for whenever a timeline has an unexplained gap |

## Windows Event IDs — Sysmon

| Event ID | Meaning |
|---|---|
| 1 | Process Creation |
| 3 | Network Connection |
| 7 | Image Loaded |
| 8 | CreateRemoteThread — persistence operations, process migration |
| 11 | File Created |
| 12 / 13 / 14 | Registry Event |
| 13 | Registry Value Set |
| 15 | FileCreateStreamHash |
| 22 | DNS Event |

## Listing log providers with a keyword

```powershell
Get-WinEvent -ListProvider *PowerShell
```
- Example: confirming exactly which logging providers exist on a system before filtering against one — useful when a provider's exact name isn't known, since guessing wrong just returns an empty result with no indication why.

## Listing events for a specific provider

```powershell
(Get-WinEvent -ListProvider Microsoft-Windows-PowerShell).Events | Format-Table Id, Description
```
- Example: once a provider is confirmed to exist, this shows every Event ID it's capable of logging and what each one means — useful for scoping an investigation before writing a filter, targeting an ID that genuinely corresponds to the activity in question rather than guessing.

## Listing available logs containing a given keyword

```powershell
Get-WinEvent -ListLog * | findstr "kw"
```
- Example: tracking down the exact name of a log channel when only a rough idea of its name is known — e.g. searching "print" to find `Microsoft-Windows-PrintService/Admin` without already knowing its full, exact name.

## Listing all events on a specific log path

```powershell
Get-WinEvent -FilterHashtable @{logname="Microsoft-Windows-PrintService/Admin"} | fl -property *
```
- Example: pulling every entry from a specific Applications and Services log channel — the kind of specialised, component-specific log (PrintService, TaskScheduler, RemoteDesktopServices, etc.) that sits outside the classic System/Security/Application logs and needs its exact channel name to query directly.

## Finding process-related information using a keyword

```powershell
Get-WinEvent -Path .\file.evtx -FilterXPath '*/System/EventID=1' | Sort-Object TimeCreated | Where-Object {$_.Message -like "*kw*"} | fl
```
- Example: searching an offline `.evtx` file for every process-creation event whose message text mentions a specific keyword — e.g. a suspicious filename, hostname, or IP — without already knowing the exact process or timestamp to filter on.

## Filtering for network connections

```powershell
Get-WinEvent -Path .\Filtering.evtx -FilterXPath '*/System/EventID=3'
```
- Example: pulling every Sysmon network-connection event from an offline log, as a starting point for scanning for beaconing patterns, unexpected outbound IPs, or a specific process reaching out unexpectedly.

## Filtering for network connections — first occurrence only

```powershell
Get-WinEvent -Path .\Filtering.evtx -FilterXPath '*/System/EventID=3' -MaxEvents 1 -Oldest | fl -property *
```
- Example: finding the very first network connection in a whole capture — useful for establishing "patient zero" timing in an investigation, e.g. the moment C2 traffic first began, without scrolling through the entire log manually.

## Hunting for Metasploit events (default Meterpreter port 4444)

```powershell
Get-WinEvent -Path .\Filtering.evtx -FilterXPath '*/System/EventID=3 and */EventData/Data[@Name="DestinationPort"] and */EventData/Data=4444'
```
- Example: 4444 is Metasploit/Meterpreter's long-standing default handler port — a fast, targeted hunt for a specific known-bad indicator rather than reviewing every network connection by hand. The same pattern works for any other port of interest by swapping the number.

## Filtering by multiple Event IDs at once

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624,4625}
```
- Example: pulling both successful and failed logons together in one query to see the full authentication picture in chronological order, rather than running two separate filters and merging the results manually.

## Filtering by a specific time window

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625; StartTime='2026-01-21 20:58:00'; EndTime='2026-01-21 21:05:00'} 
```
- Example: narrowing to a tight window once a rough timestamp is already known from another artifact — the PowerShell-native equivalent of Procmon's time filter, without the exact-match trap that a plain "is" comparison can cause. Worth double-checking whether the log is displaying local time or UTC before setting Start/EndTime, since mismatched timezones are the most common reason a time-bounded query silently returns nothing.

## Counting and grouping events — spotting a brute-force pattern

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} | Group-Object {$_.Properties[19].Value} | Sort-Object Count -Descending | Select-Object Count, Name
```
- Example: rather than reading failed-logon events one at a time, grouping them by source IP (property index varies by event schema — worth checking with `.Properties` first) and sorting by count. A single IP responsible for hundreds of 4625s stands out immediately, rather than needing to be spotted by eye scrolling through a long list.

## Accessing structured event data directly, not just the Message text

```powershell
$event = Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 1
$event.Properties | ForEach-Object {$_.Value}
```
- Example: `.Message` is human-readable but fragile to filter against with `-like`, since exact wording can vary. `.Properties` gives the raw underlying data fields in order — more reliable for scripting a repeatable search than pattern-matching against rendered text.

## Querying a remote computer

```powershell
Get-WinEvent -ComputerName REMOTE-HOSTNAME -FilterHashtable @{LogName='Security'; ID=4624}
```
- Example: checking whether the same account or technique shows up on a second machine, without needing physical access or an RDP session — relevant when confirming whether lateral movement reached other hosts during an incident.

## Checking for log clearing (anti-forensics)

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=1102}
```
- Example: the first thing worth checking if a log looks suspiciously clean or short, or if a timeline has an unexplained gap — confirms whether nothing happened, or whether someone made it look that way.

## Combining multiple logs into one sorted timeline

```powershell
$security = Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624,4625,4720,4732}
$sysmon = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; ID=1,3,8}
$security + $sysmon | Sort-Object TimeCreated | Select-Object TimeCreated, Id, Message | Format-Table -Wrap
```
- Example: Security and Sysmon are two separate logs with independent, unrelated ID numbering — this pulls relevant events from both and interleaves them by actual time, giving one unified chronological view of an attack rather than switching between two separate windows and manually merging timestamps.

## Exporting query results for a report or write-up

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} | Select-Object TimeCreated, Id, Message | Export-Csv -Path C:\Evidence\failed_logons.csv -NoTypeInformation
```
- Example: turning a live query into a portable, shareable artifact — useful for attaching evidence to an incident report or keeping a permanent record outside the live log, which may eventually roll over and lose the original entries.
