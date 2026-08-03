---
title: Linux Logging for SOC
platform: TryHackMe
difficulty: easy
date: 2026-07-27
tags: [Linux Security, logs]
summary: A write up exploring key linux logs and how to use them in investigations
---

# Linux Logging
Linux has long been a leader in servers and embedded systems and is now becoming more widespread as an OS especially with the growth of cloud adoption, because of this investigating linux machines becomes more and more likely either from on-premises servers or from cloud-native containerized workloads. This write up covers the most common Linux logs sent to a SIEM and how to view them directly on-host

> Most logs in linux are stored in /var/log
## Text Logs
Linux stores most events into plain text files meaning they can be read via any text editor, however they are also less structured without event codes or formatting rules. Because of this filtering logs is essential.

example filter: car /var/log/syslog | grep CRON (views only cronjob logs, grep -v CRON will exclude all cronjob logs)

Discovering Logs also requires understanding what you're looking for by using keywords.

Example discover: grep -R -E "auth|login|session" var/log (search for potential logins across all logs)

### Exercises 
**Which time server domain did the VM contact to sync its time**
Since NTP (Network time protocol) is responsible for time sync I simply grepped for ntp in the syslogs which gave me the server
![linuxlogging1](/static/images/linxulogging1.png)

**What is the Kernel message from Yamma**
I just grepped for yama in the syslogs for this one.
![linuxlogging1](/static/images/linxulogging2.png)

## Auth logs
The two most usefull logs to monitor are /var/log/auth.log or /var/log/secure. This log contains auth events, user management events, launched sudo commands and much more.

Loging and logoff events:
- cat /var/log/auth.log | grep -E 'session opened|session closed' (finds local and remote logins as well as cron and sudo logins)

- cat /var/log/auth.log | grep "sshd" | grep -E 'Accepted|failed' (ssh-specific events)


This log also contains misc events:

- cat var/log/auth.log | grep -E '(passwrd|useradd|usermod|userdel)\[' (searches for passwords, new users, user modificiations and deleted users)

- cat /var/log/auth.log | grep -E 'COMMAND=' (searches for commands launched with sudo)

### Exercises
**Which IP addres failed to log in on multiple users via SSH**
using grep Failed in the auth logs found all the failed log in attempts from 10.14.94.82
![linuxlogging3](/static/images/linxulogging3.png)

**Which user was created and added to the sudo group**
grepping for usermod in the auth.log logs shows users who were modified including being added to groups
![linuxlogging4](/static/images/linxulogging4.png)

## Common linux logs
Generic System logs:
- /var/log/kern.log: Kernel messages and errors, useful for more advanced investigations
- /var/log/syslog: A consolidated stream of various Linux events
- /var/log/dpkg.log: Package manager logs on Debian-based systems
- /var/log/dnf.log: Package manager logs on RHEL-based systems

App-specific logs:
usefull for investigating specific apps like database logs for queries, mail logs for phishing, container logs for anomalies and web server logs to know which pages were opened when and by who.

example: cat /var/log/nginx/access.log (web requests to a web server)

Bash history:
Records each command ran after pressing enter, however can be hidden quite easily.

example: cat /home/ubuntu/.bash_history 

### Exercises
**What version of unzip was installed on the system**
Using grep in the dpkg.log for unzip showed me which version was installed
![linuxlogging5](/static/images/linxulogging5.png)

**What is the flag you see in of of the users bash history**
Firstly I researched the find command as the other users bash history was hidden to me, with find I was able to find the path for the root users path history and used sudo cat to print it out and give me the flag.
![linuxlogging6](/static/images/linxulogging6.png)

## Runtime Monitoring
None of the logs covered thus far answer questions of what programs where launched by who or who deleted what, this is because linux does not log process creation, file changes or netwrok-related events.

OS's rely on system calls to work, any time a person opens a file, creates a process, accesses a camera or request any other OS service a specific system call is made. One example is using whoami which make a system call to execve to execute the whoami. All modern EDRs and logging tools rely on system calls, they monitor them and log the details in human readable format. This is done because attackers simply cannot bypass system calls, all defenders have to do is choose which system calls to log and monitor. 

## Auditd
The Audit Deamon is a built-in auditing solution often used for runtime monitoring using rulesets to monitor high risk evetns.

logs can be viewed in real time in /var/log/audit/audit.log or ausearch command.

example: ausearch -i -k proc_wget (shows a log a single wget command) 

This command will show the following:
- pid= and ppid=: process id and parent process id, helpful for linking events and building a process tree
- auid=: audit user, the account originally used to log in, whether locally or remotely
- uid=: the user who ran the command, this can differ from auid if user was switched
- tty=: session identifier. helps distinguish events when multiple people work on the same linux server
- exe=: absolute path to the executed binary, often used to build SOC detection rules.
-key=: optional tag specified by engineers in auditd rules that is useul to filter the events

example: ausearch -i -k file_sshconf (looks at file events matching the file_sshconf key
SOC teams also set up rules to monitor changes in critical files and directories such as SSH config files, cronjob definitions or system settings.

SOC teams often rely on alternatives to auditd since it is hard to read and ingest into SIEM, such alternatives include:

- Sysmon for linux.
- Falco
- Osquery
- EDRs

All the above tools work on monitoring system calls.

### Exercises
**When was the secret.thm file opened for the first time**
Using ausearch -i -k file_thmsecret showed me all the relevant logs related to the file and one of th events was a cat event showing this was opened.
![linuxlogging7](/static/images/linxulogging7.png)

**What is the original file name downloaded from Github via wget**
using ausearch -i -k proc_wget | grep github gives me all wget events with the keyword github
![linuxlogging8](/static/images/linxulogging8.png)

**Which network range was scanned using the downloaded tool**
Since there is no key for this event I had to just use ausearch -i | grep naabu to look for any events with the tools name
![linuxlogging9](/static/images/linxulogging9.png)

## Conclusion
In conclusion the use of Linux is growing consistenly thus making it a growing target for attacks and bad actors making understanding logs and how to find them an essential tool to trace and investigate a variety of threats.

Key Takeaways:
> Linux logging can be chaotic, but it often stores enough details to detect a threat

> Logs are kept in /var/log/ folder

> The top three log sources for SOC are auth.log, app-specific logs and runtime logs

> Bash history is unreliable for SOC, ue auditd or an alternative solution

---

- **Linux Logging for SOC** 
- **TryHackMe**
- **Easy**
- **2026-07-27**
- **Linux Security, Logging**
- **A write up of linux logs and how to search them**
