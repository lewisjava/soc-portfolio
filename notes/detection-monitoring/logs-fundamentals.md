---
title: Logs Fundamentals
date: 2026-06-19
tags: [logs, windows-event-ids, detection]
summary: Why logs matter for detection and forensics, the main log types, and the Windows Event IDs a SOC analyst needs memorised cold.
---

# Logs Fundamentals

Attackers are generally clever and creative, and part of that is knowing how to leave few traces on the victim's side to avoid detection — but a few traces are often just enough to piece everything together.

Logs contain most of these traces, since logs are the digital footprint left behind by any activity.

## Use cases of logs

| Use Case | Description |
|---|---|
| Security Events Monitoring | Logs help detect anomalous behaviour when real-time monitoring is used. |
| Incident Investigation and Forensics | Logs are traces of every kind of activity, offering detailed information on what happened during an incident. Used for root cause analysis. |
| Troubleshooting | Logs record errors in systems and applications, helping diagnose and fix issues. |
| Performance Monitoring | Logs provide valuable insight into application performance. |
| Auditing and Compliance | Logs make it easier to establish a trail of different kinds of activity for compliance purposes. |

## Types of logs

Logs are segregated into categories, since they're too numerous and overwhelming to sift through if aggregated together.

| Log Type | Usage | Example |
|---|---|---|
| System Logs | Troubleshooting running OS issues | Startup/shutdown events, driver loading, system errors, hardware events |
| Security Logs | Detecting and investigating incidents | Authentication events, authorisation events, policy changes, account changes, abnormal activity |
| Application Logs | Events specific to an application | User interaction, application changes, updates, application errors |
| Audit Logs | System changes and user events, useful for compliance | Data access, system changes, user activity, policy enforcement |
| Network Logs | Outgoing and incoming traffic | Incoming/outgoing traffic, connection logs, firewall logs |
| Access Logs | Access to different resources | Web server access, database access, application access, API access |

## Windows Event IDs

Windows has an application called Event Viewer which aggregates all logs and displays them with a GUI. Each log entry comes with an Event ID.

| Event ID | Description |
|---|---|
| 4624 | A user account successfully logged in |
| 4625 | A user account failed to log in |
| 4634 | A user account successfully logged off |
| 4720 | A user account was created |
| 4722 | A user account was enabled |
| 4724 | An attempt was made to reset an account's password |
| 4725 | A user account was disabled |
| 4726 | A user account was deleted |

Event Viewer can be searched by Event ID to find specific logs related to that event type.
