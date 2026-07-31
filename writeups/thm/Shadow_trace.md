---
title: Shadow Trace
platform: TryHackMe
difficulty: easy
date: 2026-07-31
tags: [Malware concepts, Challenge]
summary: Analyse a suspicious file, uncover hidden clues and trace the source of infection.
---

# Shadow trace
Task: analyse a file, collect anything to identify it, gather any potential IOCs, correlate and analyse the alerts for potential malicious beahciour.

## File analysis

**What architecture of the binary file windows-update.exe**
Looking at the file header I found the machine value was 8664 which represents the x64 64-bit target computer architecture.
![shadow](/static/images/shadow.png)

**What is the hash of the file windows-update.exe**
For this task I used the certutil command to get the sha 256-sum of the tool and I verified the results ussing the PE-bear tool
![shadow1](/static/images/shadow1.png)
![shadow2](/static/images/shadow2.png)

**Identify the URL within the file and use it as an IOC**
For this I used the PowerShell cmdlet Select-String to find any mentions of http inside the file and verified the results against the PE Bear tool
![shadow3](/static/images/shadow3.png)


**With the URL identified, can you spot a domain that can be used as an IOC?**
Using the same command as before but instead searching for the domain name rather than http produced results including "responses.tryhatme.com"
![shadow4](/static/images/shadow4.png)

**Input the decoded flag from the suspicious domain**
In the previous screenshot contains the base64 string tryhatme.com/VEhN..... throwing this into cyberchef provides the flag for this question.
![shadow5](/static/images/shadow5.png)

**What library related to socket communication is loaded by the binary**
Going to the import section of the tool PE bear and looking through the imports I came across the name WS2_32.dll which is the Windows Sockets 2.0 dynamic link library file which is the socket library the binary loaded.
![shadow6](/static/images/shadow6.png)

## Alert Analysis

**Can you identify the malicious URL from the trigger by the process powershell.exe**
Looking at the alert I can see that the url within the command has been encoded using base64, likely in an attempt to bypass basic string-based detection mechanisms. Putting the base64 string into cyberchef does provide the url.
![shadow7](/static/images/shadow7.png)
![shadow8](/static/images/shadow8.png)

**Can you identify the malicious URL from the alert triggered by chrome.exe**
Looking at the alert I can see that it is attempting to fetch from what looks like a bunch of decimal numbers, and then uses the command String.fromCharCode, so it looks like an attempt to obfuscate the URL using charcode and then decode it with the command and fetch a download from the decoded url. After pasting the charcode into cyberchef the URL is revealed.
![shadow9](/static/images/shadow9.png)
![shadow10](/static/images/shadow10.png)
---

- **Shadow trace**
- **TryHackMe**
- **Easy**
- **2026-07-31**
- **Malware Concepts, Challenge**
- **A write of a static malware analysis challenge with EDR alerts**
