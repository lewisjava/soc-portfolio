---
title: Boogeyman three
platform: TryHackMe
difficulty: Medium
date: 2026-008-07
tags: [Triage, SIEM, challenge]
summary: The boogeyman emerges from the darkness again.
---

# Boogeyman three
Analyse the new tactics, techniques and procedures of the threat group Boogeyman

Tools: Elastic ELK

## The Chaos inside
Using an inital email access, the threat actor aims to expand the impact by targeting the CEO, Evan Hutchinson. After opening the email nothing happened but van still reported the phishing email to the security team. Upon investigating the workstation of the CEO the team discovered the email attachment in the downloads folder of the victim (ProjectFinancialSummary_Q3.pdf) there was also a observed file inside the ISO payload with the exact same name. It is presumed the incident occured between august 29 and auagust 30, 2023.

**What is the PID of the process that executed the inital stage 1 payload**
Turning KQL off for this and searching for .html or .pdf, will show all results relating to the pdf file, where I can see a lol bin technique mshta.exe is used to execute the stage 1 payload with the process ID 6392, parent process id 2940 and occured at 23:51:15
![boogeyman3.1](/static/images/boogeyman3.1.png)

**The stage 1 payload attempted to implant a file to another location, what is the full command-line value of this execution**
pivoting from the process ID 6392 and using that as the parent PID I can see 5 results with this process ID as the parent, one of which where xcopy is used to implant the file to another location with the name review.dat. the process ID is 3832 and it occured at 23:51:16
![boogeyman3.2](/static/images/boogeyman3.2.png)

**The implanted file was eventually used and executed by the stage 1 payload. what is the full command-line value of this execution**
Using the same search query for the last question the next event after is when the file is executed. with a process ID 3680 and it occured at 23:51:16
![boogeyman3.3](/static/images/boogeyman3.3.png)

**The stage 1 payload established a persistence mechanism. what is the name of the scheduled task created by the malicious script**
This is the next command executed by mshta and it establishes a persistence mechanism to run at the same time every day and the name of the scheduled task is "Review. the process ID of the scheduled task is 6204 and it occured at 23:51:16

**The execution of the implanted file inside the machine has initiated a potential C2 connection, what is the IP and port used by this connection**
Since I have the timeline of the events I simply filtered for event.code:3 and set the time to be less than 23:55:00.000 which will bring up the connection events just after the execution of the payload
![boogeyman3.4](/static/images/boogeyman3.4.png)

**The attacker has discovered that the current access is a local administrator. what is the name of the process used by the attacker to execute a UAC bypass** 
Searching for events with review.dat returns just under 40 events, looking near to the time frame of the execution there are some discovery commands such as whoami and some user enumeration, after these the binary spawns fodhelper.exe, after researching this process is used as a UAC bypass as the file runs with high integrity privileges without showing a standard UAC confirmation prompt to the user.
![boogeyman3.5](/static/images/boogeyman3.5.png)

**Having a high privilege machine access, the attacker attempted to dump the credentials inside the machine. What is the github link used by the attacker to download a tool for credential dumping**
For this I queried for the process.name: powershell.exe with either invoke-webrequest or iew. Two commands used to download tools from the web, using this showed me that the user has downloaded a few tools, the one closest to our timeline for now is mimkatz
![boogeyman3.6](/static/images/boogeyman3.6.png)

**After successfully dumping the credentials inside the machine, the attacker used the credentials to gain access to another machien. What is the username and hash of the new credential pair**
Knowing the name of the binary used I filtered for mimkatz.exe and found the name and hash of the credential pair
![boogeyman3.7](/static/images/boogeyman3.7.png)

**Using the new credentials, the attacker attempted to enumerate accessible file shares. What is the name of the file accessed by the attacker from a remote share**
Filtering for the use of powershell.exe and cat I can see what files the user accessed in this case it was a file called IT_Automation.ps1 at 30th aug, 00:19:52
![boogeyman3.8](/static/images/boogeyman3.8.png)

**After getting the contents of the remote file, the attcker used the new credentials to move laterally, what is the new set of credentials discovered by the attacker**
Filtering for powershell commands ran around this time period I come across the powershell command that the attacker uses to move laterally as well as the credentials to do.

**What is the hostname of the attacker's lab machine for its lateral movement attempt**
This can be seen in the previous screenshots powershell command, WKSTN-1327

**Using the malicious command executed by the attacker from the first machine what is the parent process name of the malicious command executed on the second compromised machine**
Filtering for thew processes created around the same time and on the new host I can see the parent process name of the malicious command is wsmprovhost.exe
![boogeyman3.10](/static/images/boogeyman3.10.png)

**The attacker then dumped the hashes in this second machine. what is the username and hash of the newly dumped credentials**
Since I know the tool used I simply looked for the use of that tool filtered to this specific machine where I can see the credentials dumped.
![boogeyman3.11](/static/images/boogeyman3.11.png)

**After gaining access to the domain controller, the attacker attempted to dump the hashes via a DCSync attack, Aside from the administrator account, what account did the attacker dump**
From the domain controller the attacker dumped another account called backupda
![boogeyman3.12](/static/images/boogeyman3.12.png)

**After dumping the hashes, the attacker attempted to download another remote file to execute ransomware, What is the link used by the attacker to download the ransomware binary**
From the administrator account I filtered for Invoke, a command used by powershell to start binaries or download them depending on what comes after in the cmdlet, there I found a download from github for randomboogey.exe
![boogeyman3.13](/static/images/boogeyman3.13.png)
---

- **Boogeyman three**
- **TryHackMe**
- **Medium**
- **2026-08-07**
- **Triage, SIEM, Challenge**
- **A write up following a full chain of attack from inital access to actions on objectives**
