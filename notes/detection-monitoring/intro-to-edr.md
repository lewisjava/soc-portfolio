---
title: Introduction to EDR
platform: TryHackMe
difficulty: easy
date: 2026-07-07
tags: [Security Solutions, EDR, Detection]
summary: An introduction to Endpoint Detection and Response systems
---

# Introduction to EDR

## Endpoint Detection and Response

Endpoint Detection and Response is a security solution that is designed to monitor, detect and respond to threats at the endpoint level. As a SOC analyst it is required to understand how EDR works since orgs routinely use this solution for protecting their endpoints.

## What is an EDR

In computing, an endpoint is any physical device connected to a network or a digital location where an API receives requests. Most modern businesses' core functions rely on the use of these digital devices and cyber threats reflect this, so to protect these devices EDRs are deployed.

EDRs have three main features: visibility, detection, response.

### Visibility

The ability to analyse an activity depends upon the available visibility of the activity. What makes EDRs unique is the level of visibility they provide. EDRs collect data from the endpoints including process modifications, registry modifications, file and folder modifications, user actions and much more. Then it presents this data in an easy to read format.

### Detection

EDR detection capabilities incorporate signature-based detections as well as behaviour-based detections, such as unexpected user activities. With modern machine learning capabilities it is capable of detecting any deviation from standard baseline user activities and flags it. EDRs can also detect fileless malware and allow users to feed custom IOCs for threat detection.

### Response

EDR also allows analysts to take action on detected threats. The actions can be taken at any endpoint within the EDR. This includes isolation of endpoints, terminating processes, quarantining files and even connecting to a host remotely and executing actions independently, all within the EDR console.

## How EDRs work

### Agents

EDRs give the level of visibility they do by deploying 'agents' on the endpoints. Agents are the eyes and ears of the EDR — they sit on endpoints and monitor all the activity, and this information is sent to the central EDR console.

### Console

Once the console receives the data sent by the agents it correlates and analyzes it through complex logic and machine learning algorithms. The threat intelligence info is matched with the collected data and the console, acting like a brain, connects the dots and forms an alert. After an alert is formed it is up to the SOC analyst to acknowledge the alert and prioritize it.

### Telemetry

When agents collect data, this data is also known as telemetry and is the black box of an endpoint. Collected telemetry is used to make the judgements between malicious and regular activity — the more telemetry collected, the better the decision making capability.

| Telemetry | What it is |
|----------|----------|
| Process executions and terminations | Helps identify suspicious child-parent process relationships, suspicious executables, malware payloads, etc |
| Network connections | Helps identify any connection to a C2 server, unusual port usage, data exfiltration or lateral movement |
| CLI activity | Captures all commands executed on endpoints in CMD, PowerShell, etc. Helps ID malicious command execution, obfuscated PowerShell script executions |
| File and folder modifications | Threat actors modify files and folders during data staging, ransomware executions and malicious file dropping |
| Registry modifications | The registry is a goldmine of info about configurations in Windows, with many modifications that occur during malicious activity — EDR monitors all of it |

## Detection and Response in practice

### Detection

| Detection | What it does | Example |
|----------|--------------|--------|
| Behavioural detection | Instead of just matching signatures with known threats, this monitors behaviour patterns | winword.exe spawning powershell.exe will be flagged by the EDR due to behaviour — Word documents spawning PowerShell is an unusual parent-child relationship |
| Anomaly detection | Machine learning allows EDR to understand baseline behaviour and any deviation from this will be flagged | On one of the endpoints a process modified an auto-start registry key, which is not common behaviour on the endpoint |
| IOC matching | EDR will flag any activity that matches any known IOC | A user downloads a file that drops an executable used in a specific attack — the hash of this executable will get matched and instantly flagged by the EDR |
| MITRE ATT&CK mapping | Any flagged activity is also mapped to the MITRE tactic and technique, providing useful info for analysts | If the EDR flags the creation of a scheduled task it will map: Tactic = Persistence, Technique = Scheduled Task/Job |

### Response

The natural step after detection is response, and EDR offers both automated and manual responses.

| Response | What it does |
|--------|------------|
| Isolate host | During any malicious activity on an endpoint you can isolate it from the network through the EDR |
| Terminate process | Since some hosts run core business operations, isolation is not always viable — instead you can terminate the process and neutralize the malicious activity |
| Quarantine | If a file comes onto an endpoint, it can be quarantined, ensuring the file is moved to an isolated location and cannot be executed |
| Remote access | Allows remote access to the shell of any endpoint — this is done when the EDR's built-in response is not enough |
