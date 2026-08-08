---
title: Investigating Windows 2.0
platform: TryHackMe
difficulty: Medium
date: 2026-08-08
tags: [Triage, Challenge]
summary: A write investigating an infected host using loki logs and yara rules
---

# Investigating Windows 2.0



## Exercises

**What registry key contains the same command that is executed within a scheduled task**
This is HKCU/Environment/UserIntMprLogonScript and it falls under the mitre Technique T1037.001 
![windows](/static/images/windows.png)

**What analysis tool will immediately close if/when you attempt to launch it**
Since the scheduled task will appear as a process in the process monitor attempting to launch the sysinternals suit tools procmon and procexp, procexp failes to launch and instantly shuts down.

**What is the full WQL Query associated with this script**
This question requires using the loki logs provided, and since the question tells us it uses a WQL query I can use the find function and look for the common WQL queries 
![windows1](/static/images/windows1.png)

**What is the script language**
going to the file location found from the registry key in question one, inside their is a fill called WMIbackdoor. With WMI using WQL query I assume this to be the script in question. Editing it with powershell shows the code inside is VBscript
![windows2](/static/images/windows2.png)

**What is the name of the other script**
Going back to the loki logs, just underneath the previous script shows another script with the name LaunchBeaconingBackdoor
![windows3](/static/images/windows3.png)

**What is the name of the software company visible within the script**
Looking through the comments within the script there is a software company inside called MotoBit software
![windows4](/static/images/windows4.png)

**What 2 websites are associated with this software company**
This can be seen in the previous screenshot there is a .com and .cz address associated with the company 

**search online for the name of the script from Q5 and one of the websites from the previous answer, what attack script comes up**
this is WMIbackdoor.ps1
![windows5](/static/images/windows5.png)

**What is the location of this file within the local machine**
C:\TMP

**Which two processes open and close very quickly every few minutes**
mim.exe and powershell.exe. The mim.exe is scheduled to run through the registry key every 5 minutes, and powershell.exe is scheduled to run every 2
1[windows6](/static/images/windows6.png)

**What is the parent process of these two tasks**
Searching for these processes in procmon, grabbing their parent PID and filtering for that brings up the process svchost.exe, a process likely masquerading as the legitimate svchost.exe

**What is the first operation for the first of the two processes**
Filtering for mim.exe in procmon shows the first process for this binary is, process start.
![windows7](/static/images/windows7.png)

**Inspect the properties for the 1st occurrence of this process, in the event tab what are the 4 pieces of information displayed**
Looking inside the 4 pieces of information are:
- Parent PID
- command line
- Current directory
- Environment
![windows8](/static/images/windows8.png)


**Inspect the disk operations, what is the name of the unusual process**
There is a process running with the name no process

**Run loki, inspect the output, what is the name of the module after init**
![windows10](/static/images/windows10.png)

**Regarding the 2nd warning, what is the name of the eventFilter**
For the second warning the event filter name is ProcessStartTrigger
![windows11](/static/images/windows11.png)

**For the 4th warning, what is the class name**
The class name for the 4th warning is \_FilterToConsumerBinding
![windows12](/static/images/windows12.png)

**What binary alert has the following 4d5a900... as FIRST_BYTES**
nbtscan.exe
![windows13](/static/images/windows13.png)

**According to the results, what is the description listed for reason 1**
The reason for the binary alert is Known Bad / Dual use classics
![windows14](/static/images/windows14.png)

**Which binary alert is marked as APT cloaked**
The yara rule matches a binary called p.exe as a binary cloaked as psexec
![windows15](/static/images/windows15.png)

**What are the matches**
str1:psexecsvc.exe : str2:Sysinternals PsExec
![windows16](/static/images/windows16.png)

**Which binary alert is associated with somethingwindows.dmp**
This is the schtasks-backdoor.ps1 binary 
![windows17](/static/images/windows17.png)

**Which binary is encrypted that is similar to a trojan**
xcmd.exe is the encrypted binary that is also used for Derusbi Trojan
![windows19](/static/images/windows18.png)

**There is a binary that can masquerade itself as a legitimate core Windows Process/image, what is the full path of this binary**
Looking through the loki logs and filtering for svchost.exe since this has been used to launch the malware I find the binary not where it is supposed to be sat in users\public.
![windows19](/static/images/windows19.png)

**What is the full path location for the legit version**
C:\Windows\System32

**What is the description listed for reason 1**
Stuff running where it normally shouldn't
![windows20](/static/images/windows20.png)

**there is a file in the same folder location that is labelled as a hacktool, what is the name of the file**
the file labelled as a hacktool is called en-US.js
![windows21](/static/images/windows21.png)

**What is the name of the yara rule MATCH**
This can be seen in the previous screen shot: CACTUSTORCH

**Which binary didn't show in the loki results**
from the C:\TMP folder searching for the files, the only one that showed no results was mim.exe
![windows22](/static/images/windows22.png)

**Complete the yar rule file located within the Tools folder on the desktop. what are the 3 strings to complete the rule in order to detect the binary loki didn't hit on**
Looking inside the template yar file it shows that it is after 3 strings and only gives a few characters for those strings.
![windows23](/static/images/windows23.png)

for this i Use the strings and findstr function in windows cmd to find what I am looking for. With findstr I can use dots to represent any character and use "\" to escape the dot for the literal dots shown.  "." = ?  "\." = .
![windows24](/static/images/windows24.png)

Adding them in complete the yara rule and it looks like this.
![windows226](/static/images/windows226.png)

---
- **Windows Investigation 2.0**
- **TryHackMe**
- **Medium**
- **2026-08-08**
- **Triage, logs, challenge**
- **A write up of a malicious infection using loki logs and yara rules**
