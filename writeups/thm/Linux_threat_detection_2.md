---
title: Linux threat detection two
platform: TryHackMe
difficulty: Medium
date: 2026-07-28
tags: [Linux Security, Threat Detection, Discovery]
summary: A write up of threat detection after Initial Access, commands ran, goals and how to detect them in logs.
---

# Linux Threat Detection Two


## Discovery
After Inital Access the Discovery commands used are usually always the same no matter what entry point is used, the only exception is when Discovery is skipped because the attackers already know their target or want to install a cryptominer and exit.

|Discovery goal|Commands|
|--------------|--------|
|OS and Filesystem Discovery|pwd, ls /, env, uname -a, lsb_release -a, hostname|
|User and Groups Discovery|id, whoami, w, last, cat /etc/sudoers, cat /etc/passwd|
|Process and Network Discovery|ps aux, top, ip a, ip r, arp -a, ss -tnlp, netstat -tnlp|
|Cloud or Sandbox Discovery|sytemd-detect-virt, lsmod, uptime, pgrep "<edr-or-sandbox>"|

After initial Discovery attackers may also utilize more focused commands to achieve their goals. This include stealing data like passwords and data, cryptocurrency miners query CPU and GPU info to optimize the mining and botnet scripts to scan the network for new victims.

|Attack Objectives|Typical commands|
|Find and steal credentials and other sensitive data (T10003)|History \| grep pass, find / -name .env, find /home -name id_rsa|
|Id how suitable the system is for crypto mining (T1496)|cat /proc/cpuinfo, lscpu \| grep Model, free -m, top, htop|
|scan the internal network for other future victims (T1046)|ping <ip>, for ip in 192.168.1{1..254} do nc -w 1 $ip 22 done|


Detecting Discover commands requires using auditd or other runtime monitoring tools. Configuring auditd to log the commands mentioned thus far, then hunt for Disocvery using a SIEM or ausearch. The challenge is deciding if the commands are legit or from an attacker. Getting context by building a process tree is essential.

### Exercises
The scenario is that the SIEM has triggered an alert about a spike in Discovery commands, the first thing seen is that the itsupport user launched the hostname command. Investigate on the VM and find out what happened

**What is the path of the script that initated the hostname command**
Since I have both the command and the username that ran it I can use the command "ausearch -i | grep hostname | grep itsupport" which gives me th PID and PPID of the commands being ran by this user, I can then use this to filter for the ppid using "ausearch --ppid 3771" which shows the cwd=/home/itupport, running ls on this directory will show the cript inside
![linuxdiscovery1](/static/images/linuxdiscovery1.png)

**What was the last discovery command ran by the script**
since the PID of the debug.sh script was 3771 I used "ausearch -ppid 3771" to look for all processes that were started by the script, looking through the last few commands shows the last discovery command ran.
![linuxdiscovery2](/static/images/linuxdiscovery2.png)

**Looking at the script content, what's the email of the script author**
Since I know the directory path of the script I can simply cat it to get the contents
![linuxdiscovery3](/static/images/linuxdiscovery3.png)

## Motivation for attacks
After Discovery the threat actor will reveal their motivation by installing specialized malware or taking actions uniue to some class of attack.

These means threat actors are very likely to perform Ingress tool transfer (T1105) by utilizing preinstalled commands such as:

- Wget: downloading a file from a website
- Curl: make a request to the webpage
- SSH: transfer a file via SCP or SFTP

Detecting ingress tool transfer is possible because these commands can be logged with auditd or by ssh login in the case of scp/sftp.

Beyond auth logs for ssh and auditd logs for commands, network traffic logs, file events and antivirus alerts will also help.

Network traffic:
- A download from an IP previously seen in cyber attacks
- A download from a suspicious or known malicaious domain
- A download from a public service known to host attack tools such as GitHub

File events:
- A newly-created file in the temp folders (/tmp or /var/tmp)
- A newly-created file named like exploit, shell.php or kF1pBsY5

### Exercises
**From which domain was the Elastic agent downloaded**
First I used ausearch -i -x curl which showed a download from dropbox for a helper.sh script but nothing related to Elastic, after this I used -x wget which showed a download releated to Elastic .
![linuxdiscovery4](/static/images/linuxdiscovery4.png)

**What is the full path to the downloaded helper.sh script**
since I already searched for the curl command before I got the answer for this question in advance
![linuxdiscovery5](/static/images/linuxdiscovery5.png)

**Which of the downloaded is more likely to be malicious**
Since Elastic is a known program and the helper program is a a script that is very likely to run commands this makes the program downloaded with curl much more likely to be malicious. I also did some extra research for this answer and learned about LOTL (living of the land) and curl appears to be a popular tool used in offensive security for version hunting, file upload attacks, WAF evasion and TLS recon. (infosecwriteups.com curl is more than a downloader its a weapon)

## Dota3: First actions
Dota3 malware analysis:
This scenario follows CounterCraft and SANS reports about Dota3 a simple but well known malware.

the inital access from this malware starts as so:
- A botnet of more than 2000 distinct IPs across 94 countries scans the internet for systems with open SSH
- The botnet brute-forces the systems, mainly targeting the root user and trying the top 1000 weak passwords
- If the password was guessed, one of the botnet hosts accesses the victim via SSH and continues the attack

Discovery:
After gaining access the threat actor automates Discovery by running multiple commands in quick succession.

### Exercises

**Which IP address managed to brute-force the exposed SSH**
using grep accepted on the auth log shows which IP accessed the exposed ssh
![linuxdiscovery6](/static/images/linuxdiscovery6.png)

**which command did the attacker use to list the last logged-in users**
the last command is used to show the last logged-in users so searching the audit logs for use of this command should show up when/if it was executed, which in this case it did.
![linuxdiscovery7](/static/images/linuxdiscovery7.png)

**which three EDR processes did the attacker look for with egrep**
Using ausearch -i | grep egrep | grep proctitle allows me too look at egrep processes and spot any that standout, one in particular egrepped for known EDR names in this instance.
![linuxdiscovery8](/static/images/linuxdiscovery8.png)

## Dota3: Miner setupp
Continuing the chain, the threat actors install a cryptominer and supplementary malware, with SSH access they upload tools via SCP. after transferring tools the attaackers unpack them into a hidden folder under /tmp. Finally the threat actors execute two binaries from the archive, the first is a customised network scanner and the second is an XMRig cryptominer.

Detecting the attack:
- Auditd logs: creation of untrusted, hidden files and folder in the /tmp directory
- Auditd logs: creation of files named like known malware
- Auditd logs: Usage of commands often observed in attacks such as nohup
- Network traffic: SSH port scan of the network
- EDR solution: The XMrig cryptominer binary is blocked by most EDRs

### Exercises
**What is the name of the malicious archive that was transferred via SCP**
For this I used a command to look at any /tmp events and used grep proctitle to simplify the output where I could see suspicious commands taking place on a suspicious file
![linuxdiscovery9](/static/images/linuxdiscovery9.png)

**what was the full command line of the cryptominer launch**
grepping for tmp and proctitle shows the full command line of the cryptominer launch
![linuxdiscovery10](/static/image/linuxdiscovery10.png)

**Which IP address range did the attacker scan for an exposed SSH**
grepping for nohup, a typical command used by attackers to keep a process running, shows a bash was used to scan an ip range
![linuxdiscovery11](/static/images/linuxdiscovery11.png)

## Conclusion
To conclude this room covers the step taken by an attacker after Inital Access, from Discovery commands to final impact, including using a real world example and how to detect the using Linux logs.

Key takeaways:

> Hack and forget attacks are usually automated and performed at scale by botnets

> In Linux, all attack stages mostly rely on prebuilt commands like ls, cat, wget and ssh

> The best approach is using auditd and process tree analysis

---

- **Linux threat detection two**
- **TryHackMe**
- **Medium**
- **2026-07-28**
- **Linux Security, Logs, Discovery**
- **A write up of what takes place after Inital Access in a Linux machine and how to detect it with logs and process tree analysis**
