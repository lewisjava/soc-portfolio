---
title: ItsyBitsy
platform: TryHackMe
difficulty: Medium
date: 2026-08-03
tags: [Triage, SIEM, ELK, challenge]
summary: Put your ELK knowledge together and investigate an incident.
---

# ItsyBitsy


## Investigate a potential C2 communication alert
scenario - During normal SOC monitoring, Analyst John observed an alert on an ids solution indicating a potential C2 communication from a user Browne from the HR department. A suspicious file was accessed containing a malicious pattern thm:{ ________ }. A week-long HTTP connection logs have been pulled to investigate. Due to limited resources, only the connection logs could be pulled out and are ingested into the connection_logs index in Kibana.

Our task in this room will be to examine the network connection logs of this user, find the link and the content of the file, and answer the questions.  

**How many events were returned for the month of March 2022**
1482
![itsybitsy1](/static/images/itsybitsy1.png)

**What is the IP associated with the suspected user in the logs**
First things I did was to look at the IP connections, of which there were two, the one with minimal activity I assume to be the anomalous connection as it's not the one associated with the account 

**the user's machine used a legit windows binary to download a file from the C2 server. What is the name of the binary**
Filtering for the IP and with the method:GET I can see the download that took place and the binary used was bitsadmin

**The infected machine connected with a famous filesharing site in this period, which also acts as a C2 server used by the malware authors to communicate, what is the name of the filesharing site**
Expanding on the GET request I can see the file which the site was downloaded from is pastebin.com 
![itsybitsy3](/static/images/itsybitsy3.png)

**What is the full URL of the C2 to which the infected host is connected**
Looking at the URI i can see that the full name is pastebin.com/yT0Ah6a
![itsybitsy4](/static/images/itsybitsy4.png)

**A file was accessed on the filesharing site. what is the name of the fill accessed**
Following the full URL I can see what file was downloaded and it's called secret.txt
![itsybitsy5](/static/images/itsybitsy5.png)

**The file contains a secret code what is it**
This is answered in the previous screenshot

---

- **ItsyBitsy**
- **TryHackMe**
- **Medium**
- **2026-08-03**
- **Triage, SIEM, ELK, challenge**
- **A write up investigating a C2 alert using ELK**
