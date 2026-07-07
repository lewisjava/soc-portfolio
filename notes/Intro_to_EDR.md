---
title: Introduction to EDR
platform: TryHackMe
difficulty: easy
date: 2026-07-07
tags: [Security Solutions, EDS, Introduction]
summary: An introduction to Endpoint Detection and Response Systems
---

# Introduction to EDR



## EndPoint Detection Systems

Endpoint Detection and Response is a security solution that is designed to monitor, detect and respond to threats at te endpoint level, as a SOC analyst it is required to understand how EDR works since orgs routinely use this solution for protecting their endpoints.


## What is an EDR

In computing an endpoint is any physical device connect to a network or a digital location where an API receives requests. Most modern businees's core functions rely on the use of these digital devices and cyber threats reflect this so to protect these devices EDR's are deployed.

EDR'S have three main features: Visibility, detection,  response. 

# visibility
The ability to analyse an activitydepends upon the available visibility o the activity. What makes EDR's unique is the level of visibility it provides. EDR's collect data from the endpoints including process modifications, registry modifications, file and foler modifications, user actions and much more. Then it presents this data in a easy to read format. 

# Detection
EDR detection capabilites incorporate signature-based detectsions aswell as behaviour-based detections, such as unexpected user activites. With mordern machine learning capabilities it is capable of detecting any devation from standard baseline user activities and flags it. EDR's can aso detect fileless malware and allows users to feed custom IOC's for threat detection.

# Response
EDR also allows for analysts to take action on detected threats. The actions can be taken at any endpoint within the EDR. This includes isolation of endpoints, terminate processes, quarantine files and even connect to a host remotely and execute actions independently all within the EDR console.

## How EDR's work

# Agents
EDR's give the level of visibility they do by delploying 'agents' on the endpoints. Agents are the eyes and ears of the EDR, they sit on endpoints and monitor all the activite and this infomation is sent to the central EDR console.  

# Console
Once the console receives the data sent by the agents it correlates and analyzes it through complex logic and machine learning algos, the threat intelligence info is mached with the collected data and the console acting like a brain connects the dots and forms an alert. After an alert is formed it is up to the SOC analyst to acknowledge the alert and prioritize it.

# Telemetry
When agents collect data this data is also known as telemetry and is the black box of an endpoint, collected telemtry is used to make the judgements between malicious and regular activity, the more telemtry collected the better the decision making capability.

| Telemetry | What it is |
|----------|----------|
| Process executions and terminations  | helps identify suspicious child-parent and process relationsships, sus executable, malware payloads, etc  |
| Network conections  | helps identify any connection to a C2 server, unusual port usage, data exfiltration or lateral movement  |
| CLI activity| captures all commands executed on endpoints in CMD, powershell, etc. helps ID malicious command execution, obfuscated powershell script executions|
|Files and folder modifications |threat actors modify files and folder during data staging, ransomware executions ad maicious file dropping. |
|Registry modifications | the registry is a goldmine of infor about configurations in windows with many modifications that occur during malicious activity, EDR monitors all of it.|


## Detection and Response

# Detection

|Detection | What it does | example|
|----------|--------------|--------|
|Behavioural detection | instead of just matching signatures with known threats, this monitors behaviour patterns| winword.exe spawning a powershell.exe will be flagged by the EDR due to beahvour, wor documents spawning a powershell is an unusual parent-child realtionship|
|anomaly detection|machine learning allows EDR to understand baseline behaviour and any devation from this will be flagged|on one of the endpoints a process modifie an auto-start registry key which is not common behaviour on the endpoint|
|IOC matching|EDR will flag any activity that matches any known IOC|A user downloads a file that drops an executable that is sued in a specific attack, the hash of this executable will get matched and instantly flagged by the edr|
|MITRE ATT&CK Mapping|any flagged activity is also mapped with the MITRE tactic and technique providing usefull info for analysts|if the EDR flags the creation of a scheduled task it will map the following: Tactic = persistence & technuiqe = scheduled task/job|

# Response
The natural step after detection is response and EDR offers both automated and manual responses.

|Response|What it does|
|--------|------------|
|Isolate host|During any malicious activity on an endpoint you can isolate it from the network throuh the edr|
|Terminate process|Since some hosts run the core buisness operations isolation is not viable, instead you can terminate the process and neutralize the malicious activity|
|Quarantine|If a file comes into an enpoint, it can be quarantined enrusing the file is moved to an isolated location and cannot be executed|
|Remote access|Allows for remote access to the shell of any endpoint, this is done when the EDR's built in response is not enough|



- **Introduction to EDR**
- **TryHackMe**
- **Easy**
- **2026-07-07**
- **Security solutions, EDR, SOC**
- **A brief introduction to Endpoint detection and response systems**
