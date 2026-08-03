---
title: Alert triage with Elastic
platform: TryHackMe
difficulty: Medium
date: 2026-08-02
tags: [Triage, SIEM, Elastic]
summary: A writeup investigating alerts with Elastic by analyzing logs and spotting threats.
---

# Alert triage with Elastic

## Investigating web attacks
Scenario:
![elastic1](/static/images/elastic1.png)

1. Query the client IP and http request method

```
_index:weblogs and client.ip:203.0.113.55 and http.request.method:POST
```
![elastic2](/static/images/elastic2.png)

After querying and adding the relevant fields to the columns we can see from the user agent and the POST requests are automated and related to the ProxyLogon vulnerability.

Scenario two: Same IP different alert
![elastic3](/static/images/elastic3.png)
this alert comes just seven minutes after the first. The trigger field includes cmd= a hallmark of web shell activity

1. query the GET requests and the file name
```
_index:weblogs and client.ip:203.0.113.55 and http.request.method:GET and errorEE.aspx
```
![elastic4](/static/images/elastic4.png)
Here we can see clearly the commands being run using the web shell in the url.path field of the table.

### Exercises

**How many POST requests did the IP address 203.0.1113.55 make to proxylogon.ecp**
there were 3 POST requests made by this IP
![elastic5](/static/images/elastic5.png)

**Which user.agent paired with the IP made the POST requests**
This can be seen in the screenshot above it was python-requests/2.25.1

**How many logs contain the cmd= query parameter in the url.path field**
the logs contain 20 cmd= query parameters
![elastic6](static/images/elastic6.png)

**Which command was run utilizing errorEE.aspx on jul 20, 2025 @ 04:45:50.000**
the command ran was hostname.
![elastic7](/static/images/elastic7.png)


## Uncovering Account Activity
Scenario:
![elastic8](/static/images/elastic8.png)

1. Focus on events that occurred on or after the specified time in the alert.
```
@timestamp >= "2025-07-20T05:11:22" and winlog.event_id:4624 and host.name:winserv2019.some.corp and winlog.event_data.TargetUserName:Administrator
```

![elastic9](/static/images/elastic9.png)
This shows a successful login to the account via RDP from the IP address in the alert 

2. Validate with sysmon logs:
```
@timestamp >= "2025-07-20T05:11:22" and winlog.event_id:1 and user.name:Administrator
```

![elastic10](/static/images/elastic10.png)
With the sysmon logs it can be seen the attacker started a process chain that matches the windows session initialization.

Scenario two:
![elastic11](/static/images/elastic11.png)
The same user has now created an account

1. Investigate the account creation
```
@timestamp >= "2025-07-20T05:13:10.000" and winlog.channel:Security and winlog.task:User Account Management
```
### Exercises

**What is the winlog.record_id of the administrator 4624 logon event**
The successful login occured at 05:11:22.545 and the record_id is 17166
![elastic12](/static/images/elastic12.png)

**What is the process.id of the sysmon 1 event that occured on jul 20,2025 @ 05:11:27.996**
The PID is 964 and it is for sihost.exe
![elastic13](/static/images/elastic13.png)

**What is the winlog.event_id for the new user account being created**
Windows account creation event ID is 4720 


**What is the name of the new user account**
The new user account created was svc_backup at 05:13:10.009
![elastic15](/static/images/elastic15.png)

## Exposing Command Execution
Scenario:
![elastic14](/static/images/elastic14.png)
Suspicious command-line usage from the same Administrator account:
1. Identify the child processes launched by cmd.exe
2. Find out who launched cmd.exe and why
3. Look for commands like 'net' used to add users to groups
4. use Sysmon and Windows security logs to confirm malicious behaviour.

Query to highlight sysmon events on or after stated time:
```
@timestamp >= "2025-07-20T05:13:15" and process.parent.name:cmd.exe and user.name:Administrator
```



### Exercises

**What command does the attacker use to add the new account to the Remote Desktop User group**
Using the first query mentioned above I can see that the Administrator account is adding adding their persistence account to higher privilege groups @ 05:13:22.
![elastic16](/static/images/elastic16.png)


**What is the winlog.record_id of the 4732 Security event when the attacker adds the user to the Administrator group**
![elastic17](/static/images/elastic17.png)

**What powershell command did the attacker run on jul 20, 2025 @ 05:16:14.628**
The answer for this required me finding the powershell process ID and then using that as a parent ID to see all the commands ran, where the attacker used 'net group "Domain Admins" /domain
![elastic](/static/images/elastic18.png)

**What is the name of the archive that the attacker creates using the rar.exe executable**
At 05:17:55 the attacker creates an archive called finance_it_archive.rar
![elastic](/static/images/elastic19.png)

---

- **Alert triage with Elastic**
- **TryHackMe**
- **Medium**
- **2026-08-03**
- **Triage, SIEM, Elastic**
- **A write up covering three different alerts and how to triage them using elastic**
