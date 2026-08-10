---
title: Boogeyman two
platform: TryHackMe
difficulty: Medium
date: 2026-08-06
tags: [Triage, challenge]
summary: Analyse the new tacticcs, techniuqes and procedures of the threat group named boogeyman
---

# Boogeyman two

Artefacts:
    Copy of the email.
    Memory dump of the victim's workstation.

Tools:
Volatility - Open-source framewrk for extracting digital artefacts from volatile memory samples
```
vol -f memorydump.raw <plugin>
```

Olevba - a tool for analysing and extracting VBA macros from Microsoft office documents (part of the oletools suite)
```
olevba document.doc
```


## Spear phishing human resources
Scenario:
Maxine, a Human Resource Specialist working for Quick Logistics LLC, received an application from one of the open positions in the company. Unbeknownst to her, the attached resume was malicious and compromised her workstation.

**What email was used to send the phishing email**
The email used to send the phishing email was westaylor23@outlook.com
![boogeyman2.1](/static/images/boogeyman2.1.png)

**What is the email of the victim employee**
This can be seen in the previous screenshot, the victims email is: maxine.beck@quicklogisticsorg.onmicrosoft.com

**what is the name of the attached malicious document**
resume_wesleyTaylor.doc
![boogeyman2.2](/static/images/boogeyman2.2.png)

**What is the md5 hash of the malicious document**
Downloading the doc from the email and running md5sum against it gives the md5 hash
![boogeyman2.3](/static/images/boogeyman2.3.png)

**What URL is used to download the stage 2 payload base on the documents macro**
Running the olevba tool against the doc gives all the IOCs including the URL needed.
![boogeyman2.4](/static/images/boogeyman2.4.png)

**what is the name of the process that executed the newly downloaded stage 2 payload**
seen in the previous screenshot: wscript.exe

**What is the full path of the malicious stage 2 payload**
The full path of the malicious stage 2 payload is: C:\ProgramData\update.js
![boogeyman2.5](/static/images/boogeyman2.5.png)

**What is the PID of the process that executed the stage 2 payload**
Here I moved to the volatility framework tool to find the PID, first I had to look at applicable plugins for what I was finding and came across a few plugins in the documentation: windows.pslist, windows.psscan and windows.malfind. 
Running windows.pslist gave me the PID 4260 as well as it's PPID which was 1124. PID 4260 was also the PPID for a binary called updater.exe
![boogeyman2.6](/static/images/boogeyman2.6.png)

**What is the PPID of the process that executed the stage 2 payload**
This is covered in the last question it is 1124, for a process called WINWORD.EXE

**What url is used to download the malicious binary executed by the stage 2 payload**
https://files.boogeymanisback.lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe

**What is the PID of the malicious process used to establish the C2 connection**
6216 is the PID of the update.exe process seen in the previous screenshot

**What is the full path of the malicious process used to establish the C2 connection**
Reading the documentation again I came across a plugin that would display the command line for me: windows.cmdline. This did end up showing me the full path
![boogeyman2.7](/static/images/boogeyman2.7.png)

**What is the IP address and port of the C2 connections initiated by the malicious binary**
Using the command windows.netscan shows the connections made, where I can see a connection was made by updater.exe too 128.199.95.189:8080
![boogeyman2.8](/static/images/boogeyman2.8.png)

**What is the full file path of the malicious email attachment based on the memory dump**
This was found alongside the full path of the malicious process used to establish the C2 connection during the windows.cmdline plugin
![boogeyman2.9](/static/images/boogeyman2.9.png)

**the attack implanted a scheduled task right after establishing the c2 callback. what is the full command used by the attacker to maintain persistence**
None of the plugins within the documentation for volatility could help me with this, instead I resorted to using the strings command against the file and grepping for schtasks which gave me the answer
![boogeyman2.10](/static/images/boogeyman2.10.png)

---

- **Boogeyman two**
- **TryHackMe**
- **Medium**
- **2026-08-06**
- **Triage, Challenge**
- **A write up for a phishing email compromise using volatile memory**
