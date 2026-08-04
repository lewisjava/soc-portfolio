---
title: Benign
platform: TryHackMe
difficulty: Medium
date: 2026-08-04
tags: [Triage, SIEM, challenge]
summary: Challenge room to investigate a compromised host
---

# Benign
DS One of the client’s indicated a potentially suspicious process execution indicating one of the hosts from the HR department was compromised. Some tools related to network information gathering / scheduled tasks were executed which confirmed the suspicion. Due to limited resources, we could only pull the process execution logs with Event ID: 4688 and ingested them into Splunk with the index win_eventlogs for further investigation.

About the Network Information

The network is divided into three logical segments. It will help in the investigation.

IT Department

    James
    Moin
    Katrina

HR department

    Haroon
    Chris
    Diana

Marketing department

    Bell
    Amelia
    Deepak

## Identify and Investigate an infected host

**How many logs are ingested from the month of March, 2022**
13959

**There seems to be an imposter account observed in the logs what is the name of that user**
The imposter username is Amel1a, impersonating Amelia by replacing the i with a 1
![benign1](/static/images/benign1.png)
This person is also responsible for running the command whoami.exe at 12:54:30 2022-03-05
![benign2](/static/images/bening2.png)

**Which user from the HR department was observed to be running scheduled tasks**
Searching the HR hosts and schtasks I created a table which displayed the usernames, PID and, process name and command line so I could scroll through the events and saw Chris.fort was the HR user running scheduled tasks, where I can also see an update.exe executable hidden in a temp folder scheduled too be ran on every bootup
![benign3](/static/images/benign3.png)

**Which user from the HR department executed a system process (LOLBIN) to download a payload from a file-sharing host**
Searching for the typical lolbin binaries and the HR hosts I can see that only one of the common commands was used in a singular event by Haroon to download a file called benign.exe from hxxtps://control[.]com/e4d11035 with a PID of 9912
![benign4](/static/images/benign4.png)

**To bypass the security controls, which system (lolbin) was used to download a payload from the internet**
This can be seen in the previous screenshot it was certutil.exe

**What was the date this binary was executed by the infected host**
searching for the process ID of the certutil binary command I can see the date it was executed wwhich was 2022-03-04 at 10:38:28 AM

**Which third-party site was accessed to download the malicious payload**
This can be seen in the previous screenshots it is controlc.com

**What is the name of the file that was saved on the host machine from the C2 server during the post-exploitation phase**
seen in previous screenshots this is the executable benign.exe

**The suspicious file downloaded from the c2 server contained malicious content, what is the pattern**
After travelling to the website form where the download was from I can see the contents of the malicious file 
![benign5](/static/images/benign5.png)

**What is the url the compromised host connected to**
the url the compromised host connects to is the one it downloaded the malicious file from. controlc/e4d11035

---


- **Benign**
- **TryHackMe**
- **Medium**
- **2026-08-04**
- **Triage, SIEM, challenge**
- **A write up investigating a compromised host using splunk**
