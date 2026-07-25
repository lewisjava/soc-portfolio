---
title: Windows theat detection - Persistence and C2
platform: TryHackMe
difficulty: Medium
date: 2026-07-25
tags: [Windows Security]
summary: A write up of the methods and reasons of maintaining control of a machine post breach and how to detect them
---

# Windows threat detection - Persistence and C2
## Command and control (C2)
Command and control consists of techniques that adversaries use to communicate with systems under their control within a victim network - TA0011

In an RDP breach an attacker can type whatever commands they want into the RDP session but as soon as this session is closed the attacker can no longer enter commands, so what they do as soon as they breach is set up a C2. In the cases of attachments or links these usually set up the C2 or once ran will download the C2 and hide it in the files an example of this would be what happened during the PAT29 phishing campaign.
### Exercises

**Where did the attackers hide the C2 malware**
Since I know the name of the malicious zip called URGENT.ZIP to start this task I can simply use the find feature to find the starting point of the attack chain. This attack chain starts with an event ID 15 where the user uses chrome to download URGENT!.zip at 8:13PM
![c21](/static/images/C21.png)

Continuing to use the find function to search for "urgent" and events that pop up finds more event ID 11s, 2 specifically that shows explorer creating a new folder called URGENT and a new file inside that folder showing URGENT.LNK showing the user extracted the .zip and also showing the malicious file at 8:14
![c22](/static/images/c22.png)

Shortly after a new powershell process is started at 8:14, likely due to the user clicking the malicious LNK file looking inside the event shows the commands executed which contains Invoke-WebRequest a highly suspicious command to be executed, it also shows the answer to the question as to where the attacker is attempting to hide the C2 malware in APPDATA as update.exe this is two attacker techniques at once Ingress tool transer (T1105) and Masquerading as it's attempting to hide as a simple update executable (T1036).
![C23](/static/images/c23.png)

The powershell process ID is now I a pivot point I can use to search for anything with the parentProccessId that matches the powershells PID, searching with the PID 3140 shows a file creation (which will give the full directory of where the attackers hid the malware) a Network connection spawned by powershell and DNS query spawned by powershell. The answer for the exercise is in the screenshot below.
![c24](/static/images/c24.png)

**What is the domain of the command and control server**
Continuing in the attack chain the room asks to find the command and control server, since I have the name of the downloaded tool update.exe I can pivot and use that as in the find function which brings up two key events, event ID 3 network connection and event ID 22 DNS query. the network connection shows the source ip and hostname used is the victim machine showing an outbound connection. The DNS query event shows that the process that ran it was update.exe in the image field and that the QueryName is route.m365officesync.workers.dev at 8:14 where the C2 connection has been established. Another technique can also be seen here where the C2 server is hosted on a legit cloud platform .workers.dev which is Cloudflares Workers domain allowing this query to blend in with legit traffic (T1102)![c25](/static/images/c25.png)

## Persistence
The tactic of maintaining a reliable, long-term access to a target that can survive reboots and password changes is called Peristence(TA0003). Once a threat actor breaches a host through a vulnerability they will not rely on that same vulnerability to get back in and assume it will be patched, instead they may:
- Create an additional hidden vulnerability in the breached device such as a backdoor or a webshell
- Create a new user (T1136), make it admi (T1098) and use it for further RDP logins.

The second one is done by using very specific commands:
- net user "username" "password" /add (this creates the user through CMD)
- New-LocalUser "username" -Password [PASSWORD] \(this creates a user through powershell)

- net localgroup Administrators "username" /add (this adds a user to admin group through CMD)
- Add-LocalGroupMember "Administrators" -Member "username" (this adds a user to admin group through powershell)

Detecting backdoor users:
Filter for event ID 4720 and look at who created the account (can this person confirm the account creation), what is the source IP and time of the creator's login (Is it expected?), what other events did the creator perform during their session. Look at what groups, if any, the new user was added to using even ID 4732. Look at if any accounts passwords were reset with event ID 4724.

### Exercises
**How many times did the threat actor fail to log in to the Administrator**
The answer for this question is simlple to find just filter for event id 4625 and use the find function and search "Adiministrator", of the 6 events returned all of them are for Administrator. Inside one of the events also gives the source network address which can be used to search if a successfull login was made after filtering for 4624 events![persistence1](/static/images/persistence1.png)

**After the successful login, which backdoor user did the attacker create**
Filtering for the event ID 4720 and putting Administrator into the find function shows the attacker created an account name called support (T1136.001), which a legitimate backdoor malware called ServHelper (S0382) when creating a backdoor in order to blend in a a legitimate helpdesk account
![persistence2](/static/images/persistence2.png)

**which privileged group was the backdoor user added too**
Using the event ID 4732 and searching for "support" in the find function will show which group the user was added too which is BUILTIN/Adiministrators (T1098)
![persistence3](/static/images/persistence3.png)

## Persistence: Tasks and Services
This previous section covers persistence in the case of an attacker gaining inital access via RDP and goes on the assumption that the attacker will be able to RDP into the backdoored user. But if the attack started through phishing or USB using a backdoored user isn't a possibility. Instead threat actors need an actively running malware that maintains a connection to their C2 server, even after a system reebot.

Tasks and services:
Two common methods of using tasks and services to maintain persistence (of which there are hundreds):

- Create a windows Service (runs after OS startup): sc create "BadService" binpath= "C:\malware.exe" start= auto
this will create an sysmon 1 event launching sc.exe and a service creation event 4697 in security logs

- Create a scheduled Task (runs after OS startup): schtasks /create /tn "BadTask" /tr "C:\malware.exe" /sc onstart /ru System
this will create a sysmon 1 event ID launch of schtasks.exe and a scheduled task creation event ID 4698 in security logs

### Exercises
**Which Windows service was created to persist the Nessie malware**
Looking into the security logs and filtering for event 4697 and using the find function with the word "nessie" shows me that nessie created a new Windows service called data protection service to maintain Persistence (T1543.003)
which when looking into Services shows it starts up automatically and it has LocalSystem privileges.
![persistence4](/static/images/persistence4.png)

**Which scheduled task was created to persist the Troy malware**
Same methodology as before but instead filtering for tasks 4698. Which finds the task runs the malware on every startup.
![persistence5](/static/images/persistence5.png)

**what flag do you get after finding and running the Troy malware**
![persistence6](/static/images/persistence6.png)

## Persistence Run Keys and Startup
Services and scheduled tasks are typically run on system boot and required amin privileges to configure. However windows provides per-user persistence methods that are used by both legitimate tools and malware.

Two common examples are:
- Add malware to Startup Folder: copy C:\malware.exe %AppData%\Microsoft\Windows\Start Menu\Programs\Startup\malware.exe"
This will create a sysmon event ID 11 for new start up item.

- Add malware to Run keys: reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v BadKey /t REG_SZ /d "C:\malware.exe"
This will create a sysmon event ID 13 for new registry value

Both of these share the same MITRE ATT&ACK technique T1547.001

### Exercises 
**what is the parent process image of the Odin malware**
Searching for the odin malware with the event ID filter 1 shows the process creation parentimage for the odin malware is C:\Windows\explorer.exe
![persistence7](/static/images/persistence7.png)

**What is the last line that the odin malware outputs**
Using the process ID from the event in the previous screenshot I find another process creation event which shows that the malware spawned a powershell and executed a command.
![persistence8](/static/images/persistence8.png)

**What flag do you get after running the kitten malware**
![persistene9](/static/images/persistence9.png)

## Conclusion
Bad actors maintain persistence for many reasons, three examples are:
1. Add the host to a botnet
2. Spy on the victim as a part of a state-sponsored campaign
3. Use the victim as an entry point to the network.

This writeup covers C2, Persistence and impact, why attackers establish c2 and persistence, how they do it and how to detect them on Windows devices.

---

- **Windows threat detection - C2 and Persistence**
- **TryHackMe**
- **Medium**
- **2026-07-25**
- **Windows Security**
- **A write up on persistence and C2 methods and how to detect them on Windows machines**
