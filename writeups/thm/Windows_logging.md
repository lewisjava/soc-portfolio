---
title: Windows Logging for SOC
platform: TryHackMe
difficulty: easy
date: 2026-07-22
tags: [Windows security]
summary: A write up of windows logging, what to look for, how to interpret them and what malicious action they indicate
---

# Windows Logging for SOC
With Windows being almost universally the most popular OS system for users it has a target on it's back by threat actors with over 90% (VikingCloud.com, Cybersecurity statistics - 2026) of all ransomware and malware attacks globally targeting Windows. With this understanding Windows logs becomes an essential skill for SOC analysts.

Windows comes with logging capabilities that are stored in binary format in C:\Windows\System32\winevt\Logs and are read with the built in Event Viewer

## Security Log: Authentication
Security event logs tend to bring the most value, with two of the most important being Successful Logon (4624) and Failed Logon (4625):

|Event ID|Purpose|Limitations|
|--------|-------|-----------|
|4624 (Successful logon)|Detect suspicious RDP/network logins and ID the attack starting point|Noisy, hundreds of logon events per minute on loaded servers|
|4625 (Failed Logon)|Detect brute force, password spraying, or vulnerability scanning|Inconsistent, the logs have lots of caveats that may lead to wrong interpretation of events|

Brute force example:
1. Filter for 4625 event ID
2. Look for events with logon type 3 and 10 (Network and RDP logins)
3. Every event here is worth attention but main red flegs include: Many attempted users like admin, helpdesk and cctv (password spraying). many login failures on a single account usually administrator (indicates brute force), workstation name does not match a corporate pattern (eg kali instead of WRK1-PC-06), source IP is not expected.

RDP logons example:
1. Filter for 4624
2. Look for events with logon type 10 (RDP)
3. Red flags are either a preceding brute force or a suspicious source IP / hostname
4. if malicious find out what happened next (e.g. 0x5D6AC, Logon ID is a unique session identifier save for later)

### Exercises

**Which IP performed a brute force of the THM-PC**
Filtering for event id 4625 and the computer THM-PC gives all unsuccessful login attempts related to that host pc where I can inspect the individual logs for more information which provides the source IP attempting to login/brute-force.
![4625](/static/images/4625.png)

**which user has been breached as a result of the attack**
Looking at the Account name being targeted I can see that it is the administrator account that has been breached**
![4624](/static/images/4624.png)

**what was the logon ID of the malicious RDP logon**
For this part I could have just filtered for the event ID 4624 and the hostname of the PC and go through each of the successful logins and look for the one that matches the host IP but this would take a bit of time, instead I googled how I could filter further for logon types or by IPs which showed me how to filter for both using the xml tab and custom queries where i used \*[EventData[Data[@Name='LogonType']='10' to look for RDP logons. 
After grabbing the logon ID as shown in the screenshot below, this is now used as the pivot for the rest of the investigation, the whole RDP session can be traced via this logon ID.
![logonid](/static/images/logonid.png)

## Security Log: User management

|Event ID|Description|Malicious Usage|
|--------|-----------|---------------|
|4270 / 4722 / 4738|User account was created / enabled / changed|Attackers might create a abackdoor account or even enable an old one to avoid detection|
|4725 /4726|A user account was disabled / created|Threat actors may disable privileged SOC accounts to slow down their actions|
|4723 / 4724|A user changed their password / User's password was reset|Threat actors, with enough perms, might reset the password and then access the required user|
|4732 / 4733|A user was added to / removed from a security group|Attackers often add their backdoor accounts to privileged groups like "Administrator"|

Backdoored Users example:
1. Filter for 4720 / 4732 event IDs
2. Manually review every event, red flags are:
    - No one from it department can confirm the action
    - Changes were made during non-working hours
    - The subjects users name is unknown or unexpected
    - The target user's name does not follow a usual naming pattern
3. If confirmed the action was malicious, find out login details
    - Copy logon ID 
    - Find the corresponding login event with the same Logon ID
### Exercises
**Which user was created by the attacker soon after the RDP login**
First I filtered by event ID 4720 and this only returned only one event which made it rather easy to find, however if a large amount of events were to have returned I would have used the find function and used the Logon ID to look for account creation events relevent to that logon ID.
![4720](/static/images/4720.png)

**Which two privileged groups was the backdoor user added to?**
With the logon ID looking for events related to this user was very easy simply using it on the find function and filtering for event 4732 allowed me to easily find the groups the user was added too
![4732](/static/images/4732.png)

## Sysmon: Process monitoring
Security show who is breached, syslogs show how. Sysmon is a free tool from Microsoft sysinternals suit that allows for advanced monitoring in addition to the deault system logs.

Sysmon event ID 1:
- Process info: context of launched process, including its PID, path and command line
- Parent info: context of the parent process, helpful to vuild a process tree or attack chain
- Binary info: Process hash, sig, and PE metadata
- User context:A user running the process and logon ID

Process launch:
1. Open sysmon logs and filter for event ID 1
2. Review the fields from process and binary info groups, red flags are:
    - Image is in an uncommon directory like C:\Temp
    - Process is suspiciously named like aa.exe
    - Process hash matches as malware on VirusTotal
3. Review the fields from the parent process group, red flags are:
    - Parent matches red flags from step 2
    - Parent is not expected such as notepad launching some CMD commands
4. if in doubt go up process tree until confident in verdict.
5. trace the attack chain by filtering all security and sysmon events with the same Logon ID.

### Exercises
**Which web browser does Sarah use to browse the web**
Sorting the logs ny time and looking at the first process create log showed Google Chrome as the first process created when this user logged on which was their web browser.
![1](/static/images/1.png)

**Which file did sarah download from the browser**
Looking at event ID 15 file stream created with this username shows what they downloaded with the browser
![15](/static/images/15.png)

**Which URL was the file downloaded from**
one of the event ID 15's also contains the hosturl after filtering for this event ID with this username and going through them I came across the event which contained it 
![hosturl](/static/images/hosturl.png)

## Syslog: Files and network

event id's:
- 11 / 13 = file create / Registry Value set: Detect files dropped by malware or its changes to the registry
- 3 / 22 = Network connection / DNS query: Detect traffic from untrusted processes or to known malicious destinations

Although process creation events provide enough context to detect common breach scenarios, additonal logs are used to reconstruct full attack cain and ensure nothing is missed.

Process activites:
1. Copy THE PID from the event in ID 1
2. Search for other Sysmon events with the same PID
3. Red flags for network connection events are:
    - Connection to external IPs on port 80 or on non-standard ports like 4444
    - Connection to known malicious IPs (e.g. by checking on VirusTotal)
    - DNS queries to suspicious domains
4. Red flags for file and registry changes are
    - Files dropped to staging directories like C:\Temp
    - Dropped file is a script
    - Created files or registry keys are used for persistence

### Exercises
**Which file was created by the downloaded malware to persist on the host**
First i sorted by event ID and found the process created by the downloaded file and got the process ID which was 1460. I then used this in the find function until I landed on event ID 11 file created
![parentid](/static/images/parentid.png)

**What is the Command & Control server malware connected to**
The process ID also had an event 3 ID logged for network connections meaning the malware established the connection and is likely to the C2 server.
![3](static/images/3.png)

**which domain does the malicious IP correspond to**
putting the ip into virustotal shows the domains it resolves too, it also shows that the ip has been flagged as malicious
![syslog](/static/images/syslog.png)

## PowerShell: Loggin Commands
Powershell is logged using the PowerShell history file since syslog does not log the commands ran in it, it only logs when the processes was created.

Located: C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt

### Exercises
**Which powershell command was executed first**
Opening the powershell history file and looking at the first line shows the first executed command
![consolehistory](/static/images/consolehistory.png)

**When did the Administrator run the first PS command**
Right clicking the file and clicking the properties option and looking at when the file was first created gives the answer which is may 18, 2025

## Conclusion
To conclude logs are essential to understanding what is happening on a Windows device and by using built in tools like Event Viewer and Syslog allows an analysts to not just understand what happened but how it happened.

Key Takeaways
> 4624 and 4625 Event IDs are key
> Group logs by Logon ID and Process ID to view attack chain
> Learn sysmon
> Read powershell logs
---
- **Windows Logging for SOC**
- **TryHackMe**
- **Easy**
- **2026/07/22**
- **Windows Security**
- **A write up of the logs, event IDs and tools used in windows logging and how to understand them**
