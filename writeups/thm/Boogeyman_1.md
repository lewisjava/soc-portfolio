---
title: Boogeyman 1
platform: TryHackMe
difficulty: Medium
date: 2026-08-05
tags: [Triage, challenge]
summary: A new threat actor emerges from the wild using the name Boogeyman
---

# BoogeyMan 1
Tasks are to analyse the Tactics, Techniques and Procedures executed by a threat group

Artefacts

For the investigation proper, provided with the following artefacts:

    Copy of the phishing email (dump.eml)
    Logs from Julianne's workstation (powershell.json)
    Packet capture from the same workstation (capture.pcapng)

## Email analysis
Targeted phishing email targeting the finance team

**What is the email address used to send the phishing email**
Attacker email: agriffin@bpakcaging.xyz (impersonating packaging company officer)
![boogeyman1](/static/images/boogeyman1.png)

**What is the email address of the victim**
julianne.westcott@hotmail.com (in previous screenshot.)


**What is the name of the third-party mail relay service used by the attacker based on the DKIM-signature and List-Unsubscribe headers**
elasticemail
![boogeyman2](/static/images/boogeyman2.png)

**What is the name of the file inside the encrypted attachment**
invoice_20230103.lnk
![boogeyman3](/static/images/boogeyman3.png)

**what is the name of the file inside the encrypted attachment**
Invoice2023!
![boogeyman4](/static/images/boogeyman4.png)

**Based on the resut of the lnkparse tool, what is the encoded payload found in the Command Line Arguments tool**
After running the tool the following encoded payload is shown in the command line.
![boogeyman5](/statice/images/boogeyman5.png)
Putting the encoded string into cyberchef shows it attempts to download a file from hxxp://files[.]bpackcaging[.]xyz/update, probably a binary with the name update.
![boogeyman6](/static/images/boogeman6.png)

## Endpoint security

**What are the domains used by the attacker for file hosting and C2**
Since I know their domains end with .xyz I catted the powershell.json logs, parsed them through jq, and then grepped for anything that returned .xyz which gave me their omains.
domain one: cdn.bpakcaging.xyz:8080
domain two: files.bpakcaging.xyz
![boogeyman7](/static/images/boogeyman7.png)

**What is the name of the enumeration tool downloaded by the attacker**
In the previous screenshot it can be seen two binaries are downloaded by the attacker and shortly after pwd is ran after the downloades. grepping for pwd showed me what the attacker was doing as well as the name of the tool used, which is seatbelt, which is the sb.exe binary downloaded.
![boogeyman8.png](/static/images/boogeyman8.png)

**What is the file accessed by the attacker using the downloaded sq3.exe binary**
tracing back the cd commands shows the attacker accessed a file called plum.sqlite
![boogeman9.png](/static/images/boogeyman9.png)

**What is the software that uses the file in Q3**
The software can be seen in the directory of the file and it is Windows sticky notes

**What is the name of the exfiltrated file**
since the malware prints pwd after every command I can work my way up the pwd chain and find the exfiltrated file name which is protected_data.kdbx, it also shows me the destination ip of 167[.]71[.]211[.]113
![boogeyman10](/static/images/boogeyman10.png)

**What type of file uses the .kdbx file extension**
Keepass, a password manager.

**What is the encoding used during the exfiltration attempt of the sensitive file**
This can be seen in the previous screenshot, the encoding used is hex

**What is the tool used for exfiltration**
Also seen in previous screenshot, the tool used is nslookup, a type of DNS exfiltration.

## Network traffic analysis

**What software is used by the attacker to host its presumed file payload server**
Since I have both the IP and domain with port from the previously. What I did here is look at HTTP and the destination IP of the attacker to see the downloads that were performed I then followed the TCP stream which showed me the attacker is using python to host it's file payload server
![boogeyman12](/static/images/boogeyman12.png)

**What HTTP method is used by the C2 for the output of the commands executed by the attacker**
Since I found the cdn domain and the port 8080 that it was using I can find the C2 traffic and see it is using POST commands from hxxp://cdn[.]bpakcaging[.]xyz:8080/27fe2489
![boogeyman13](/static/images/boogeyman13.png)

**What is the protocol used during the exfiltration activity**
Since the attacker is nslookup to exfiltrate the files the protocol used is DNS

**What is the password of the exfiltrated file**
For this I filtered in wireshark for http contains sq3.exe and found only 4 packets with binary code inside
![boogeyman14](/static/images/boogeyman14.png)
which after taking to cyberchef I managed to find the password
![boogeyman15](/static/images/boogeyman15.png)

**What is the credit card number stored inside the file**
For this I exported all DNS queries associated with the outbound IP the file was sent to, I then used tshark, to get the exfiltrated kdbx from the encoded data.
![boogeyman16](/static/images/boogeyman16.png)
After entering the masterkey the file opens and displays the credit card number
![boogeyman17](/static/images/boogeyman17.png)

---

- **BoogeyMan 1**
- **TryHackMe** 
- **Medium** 
- **2026-08-05**
- **Triage, SIEM**
- **A write up from inital access to data exfiltration**
