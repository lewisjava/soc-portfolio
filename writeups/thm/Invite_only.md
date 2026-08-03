---
title: Invite Only
platform: TryHackMe
difficulty: easy
date: 2026-08-01
tags: [Threat analysis, Challenge]
summary: Extract insight from a set of flagged artefacts, and distil the information into usable threat intel.
---

# Invite only
You are an SOC analyst on the SOC team at Managed Server Provider TrySecureMe. Today, you are supporting an L3 analyst in investigating flagged IPs, hashes, URLs, or domains as part of IR activities. One of the L1 analysts flagged two suspicious findings early in the morning and escalated them. Your task is to analyse these findings further and distil the information into usable threat intelligence.

Flagged IP: 101[.]99[.]76[.]120
Flagged SHA256 hash: 5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f

We recently purchased a new threat intelligence search application called TryDetectThis2.0. You can use this application to gather information on the indicators above


## Exercises

**What is the name of the file identified with the flagged SHA256 hash**
Using the AV vendor tool I found the name is syshelper.exe
![inviteonly1](/static/images/inviteonly1.png)


**What is the file type associated with the flagged SHA256 hash**
In the screenshot above just under the name we can see the file typs is win32 exe.


**What are the execution parents of the flagged hash?**
Moving down to execution parents there are two, with their respective hashes which will be noted for later use
![inviteonly2](/static/images/inviteonly2.png)

**What is the name of the file being dropped**
Scrolling to the dropped file section we can see the executable aclient.exe and it's hash that will also be noted down.
![inviteonly3](/static/images/inviteonly3.png)

**research the second hash in question 3 and list the four malicious files dropped**
putting the new hash into the AV vendor tool and going to the relations tab I can see the malicious exe drops 20 files, 4 of which have been marked as malicious.
![inviteonly4](/static/images/inviteonly4.png)
![inviteonly5](/static/images/inviteonly5.png)

**Anayse the files related to the flagged IP, what is the family that links these files**
Putting the IP into the AV vendor tool and going to the community tab I can see users have commented information related to the IP, specifically that the family is AsyncRAT
![inviteonly6](/static/images/inviteonly6.png)

**What is the original report where these flagged indicators are mentioned** 
In the previous screenshot one of the commenters uses a refrence which is actually the title of the original report: from trust to threat hijacked discord invites used for multi stage malware delivery

**Which tool did the attackers use to steal cookies from the google chrome browser** 
Reading the report I learn the attackers use a tool called ChromeKatz to steal cookies from new Chromium broswer versions
![inviteonly7](/static/images/inviteonly7.png)

**Which phishing technique did the attackers use**
Reading the report shows the attackers use a phishing technique called clickfix where the user lands onto the phishing website which displays a fake website prompting the user to verify, clicking verify copies a malicious powershell script to the users clipboard silently, after which clickfix technique takes place whereby the website pretends to not work and required manual verification that asks the user to press windowd + r (opening the run dialog box) press crnt + v (pasting the malicious code into the run dialog box) and "press enter to verify" which will then run the malicious powershell code.
![inviteonly8.png](/static/images/inviteonly8.png)

**What is the name of the platform that was used to redirect a user to malicious servers** 
The platform used was discord, where the threat actors used fake verification bots to redirect users to a malicious website


---

- **Invite Only**
- **TryHackMe**
- **Easy**
- **2026-08-01**
- **Threat analysis, challenge**
- **A challenge scenario turning artefacts into threat intelligence using enrichment**
