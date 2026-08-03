---
title: Living off the land attacks
platform: TryHackMe
difficulty: easy
date: 2026-07-30
tags: [Malware Concepts, LOTL]
summary: A write up of how to detect and analyse living off the land attacks
---

# Living off the land
Living off the land attacks are where attackers do not rely on custom malware or malicious executables but instead use trusted system tools already present on the machine.

## Common LOL tools and techniques
Threat actors use lol techniques because built-in tools are already trusted, widely available and often allowed by default controls so malicious activity can blend among normal ops.

Common tools use:
- Powershell: used for in-memory scripting, remote downloads and automation
- WMIC/WMI: used to run commands locally or on remote hosts and to query system state
- Certuitl: used to fetch files and encode or decode payloads
- Mshta: used to run HTA (HTM, Jscript or VBScript code) content or an inline script delivered by a document or link
- Rundll32: used to invoke DLL exports or trigger URL handlers
- Scheduled tasks (schtasks): used to run code at logon or on a schedule for persistence

Living off the land methods are not exclusive to windows either and Linux is also still targeted with attacks. Public collections document common patterns for both platforms, LOLBAS for windows and GFTObin for Unix. Knowing which tools are most likely to be misused and the goals behind those uses helps defenders tune logging, capture full command lines and process trees and prioritise alerts.

Measured to reduce attack surface and improve response:
- Apply layered defensive controls that combine endpoint, network and identity protections (defence in depth)
- Implement application control policies such as AppLocker or Windows Defender Application control to define which scripts and executables are permitted to run
- Enforce/use the principles of least privilege by ensuring only admins can access or use system management utilities
- Configure network rules and DNS filters to block or redirect connections to domains and IPs known for malicious activity
- Maintain clear containment playbooks that outline the steps for isolating compromised systems and revoking exposed credentials
- Regularly review and update access perms, logging coverage, and control lists to adapt to new attack methods.

## Real world examples

- APT29 (Nobelium) - Powershell and WMI for Persistence and Execution
Used fileless techniques that combine PowerShell with WMI event subscriptions to persist and execute code without dropping obvious binaries on disk. A WMI event subscription was created to run a PowerShell payload stored in WMI. The payload was read, decrypted and executed from WMI properties leaving minimal on-disk artefacts (T1546.003)

- BlackCat (ALPHV) Ransomware - Built-in tools for Lateral movement
Used Powershell for scripting and defence disabling, PsExec from sysinternals suite for remote execution and lateral movement, and certuitl to fetch or decode payloads on hosts.

- Cobalt Strike loaders: QakBot and Iced ID
Multiple incident reports note that loades such as QakBot, IcedID and others have been used to stage and deliver Cobalt Strike beacons and attackers often use signed Windows binaries like rundll32.exe and mshtr.exe to exeucte or bootstrap those payload in memory making execution appear to invlve legit processes.

## Detecting LOL activity

1. Powershell
attacers use PowerShell because it can run scripts directly into memory without creating files, automate many ssytem actions, interact with the network and bypass execution policies.

Example detection
```
index=wineventlog OR index=sysmon (EventCode=4688 OR EventCode=1 OR EventCode=4104)
(CommandLine="*powershell*IEX*" OR CommandLine="*powershell*-EncodedCommand*" OR CommandLine="*powershell*-Exec Bypass*" OR CommandLine="*Invoke-WebRequest*" OR CommandLine="*DownloadString*" OR CommandLine="*Invoke-RestMethod*")
| stats count values(Host) as hosts values(User) as users values(ParentImage) as parents by CommandLine
```

2. WMIC
Windows managemtn instrumentation command-line lets admins query and manage local or remote windows systems because of this it is commonly used by threat actors to execute commands remotely through starting processes.

Example detection
``` 
index=sysmon OR index=wineventlog (EventCode=1 OR EventCode=4688)
(CommandLine="*\\wmic.exe*process call create*" OR CommandLine="*wmic /node:* process call create*" OR CommandLine="*wmic*process get Name,CommandLine*")
| stats count values(Host) as hosts values(User) as users values(ParentImage) as parents by CommandLine
```

3. Certutil
A tool used for managing certificates and encoding or decoding data. Used by attackers because it is signed by microsfot and common in admin workflows. It can place files without using curl or similar software and bypasses some simple blocking rules.

Example detection:
```
index=sysmon OR index=wineventlog (EventCode=1 OR EventCode=4688 OR EventCode=4663)
(Image="*\\certutil.exe" OR CommandLine="*certutil*")
(CommandLine="* -urlcache * -f *" OR CommandLine="* -decode *" OR CommandLine="* -encode *")
| stats count values(Host) as hosts values(User) as users values(ParentImage) as parents by CommandLine
```
4. MSHTA
MSHTA runs HTML application files which can tonain VBcript or JavaScript code

Example alert:
```
index=sysmon (EventCode=1 OR EventCode=4688) Image="*\\mshta.exe" (CommandLine="*http*://*" OR CommandLine="*javascript:*" OR CommandLine="*.hta")
\| stats count by host, user, ParentImage, CommandLine
```
5. Rundll32
Rundll32 executes specific exported functions from DLL files.

Example alert:
```
index=sysmon (EventCode=1 OR EventCode=4688 OR EventCode=7) Image="*\\rundll32.exe" (CommandLine="*\\Users\\Public\\*" OR CommandLine="*url.dll,FileProtocolHandler*" OR CommandLine="*\\Windows\\Temp\\*")
\| stats count by host, user, ParentImage, CommandLine
```

6. Scheduled tasks (schtasks)
Task scheduler is a built-in windows automation letting adminds run programs or scripts at specific times, because of this it shows up in normal system logs and are often allowed by polcy making it a valuable mechanism for both legit ops and attacker persistence.

attackers create or modify tasks to achieve persistence across reboots, to run code at user logon or on a regulare cadence.

Example alert:
```
index=wineventlog EventCode=4698 OR EventCode=4699 OR index=sysmon (EventCode=1 OR EventCode=4688) (CommandLine="*schtasks* /Create*" OR CommandLine="*schtasks* /Run*" OR Image="*\\taskeng.exe" OR EventCode=4698)
| stats count by host, user, EventCode, TaskName, CommandLine
```

## Conclusion
To conclude this writeup demonstrates how attackers do not need custom malware or scripts but isntead can repurpose trusted Windows utilities to carry out malicious activity without introducing new binaries. By testing and analysisng each command safely it can be observed how legit admin tools such as PowerShell, WMIC, certutil, Mshta, Rundll32 and Scheduled Tasks can be abused for execution.

Key Takeaways:

> Most built-in windows tools are abused in living off the land attacks

> PowerShell can be used to enable fileless, in-memory and automated execution

> WMIC can be used to support remote process creation and system recon

> Certutil can be used to download, ecnode or decode malicious payloads

> Mshta and Rundll32 can be used to run scripts or DLL-based payloads

> Peristence mechanisms can be created and triggered through Scheduled tasks.

> Apply defensive techniques such as enhanced logging, behavioural detecion and execution control to limit LOL activity

---

- **Living off the land attacks**
- **TryHackMe**
- **Medium**
- **2026-07-20**
- **Malware Concepts, Living off the land**
- **A write up of living off the land attacks, tools and techniques used and how to detect them**
