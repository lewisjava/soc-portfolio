---
title: Windows threat detection - Initial Access
platform: TryHackMe
difficulty: Medium
date: 2026-07-24
tags: [Windows Security]
summary: A write up of using windows logging to detect Initial Access.
---

# Windows threat detection - Inital access

There are two groups of initial access:
1. Exposed services
2. User-driven

Exposed services:
Every organisation requires services to operate such as SMTP, RDP, HTTP but every service introduces risks and vectors for attack. Examples include:
- T1133: External remote services, where threat actors will look for exposed RDP/VNC/SSH with weakpasswords to get remote access
- T1190: Exploit public-facing applications, where threat actors will look for misconfigured or vulnrable websites and apps

User-drivern:
This requires the help of the End user unknowinly helps the threat actor gain access by clicking malicious links, launching phishing attachments, using pirated software, plugging in unknown USB devices etc. This is the more common point of entry since the end user/humans are the weakest link in cyber security and with windows being the most popular OS for user workstations. This includes examples like:
- T1566: Phishing
- T1091: Removable media

## Inital Access via RDP
RDP is a very common method of attack for inital access with Censys Search suggesting there are over 5 million RDP enabled machines, with many under threat actors control.

|Step of attack|Detection opportunity|
|--------------|---------------------|
|1. Network scan by botnet which detects exposed RDP port|N/A|
|2. RDP brute force|1. Open logs filter for failed logins 4625 2. filter for logon types 3 and 10 3. filter for logins from external IPs|
|3. Inital Access via RDP| 1. Switch event filter to 4624 2. Check the account under which the logon was made, this is the account used for inital access|
|4. Further malicious actions| 1. Filter for logon type 10 2. Copy Logon ID field 4. Open Sysmonlogs and search events with Logon ID, this will show processes started by threat actor|

### Exercises

**Which user seems to be the most actively brute-forced by botnets?**
I was able to guess the answer for this as administrator before looking at the logs as I assumed this would be the most likely target anyway, but to understand what this would look like in the logs and develop the skill of using the logs I filtered for the answer anyway. Filtering for event ID 4625 and sorting by date and time I can see a burst of attempted login attemps each a second apart indiciative of a brute-force event, looking inside one of the events shows the accound name: ADMINISTRATOR
![rdp](/static/images/rdp.png)

**which IP managed to breach the host Via RDP**
For this exercise the challenge wants me to filter for 4624 events and find the event that matches the targeted user and the logon type as 10, after finding the event that matches both these requirements the source ip field will show me the IP that managed to breach the host via RDP
![rdp1](/static/images/rdp1.png)

**Can you get the real workstation name of the threat actor**
With the IP address I was able to search the other logon types, including logon type 3, which would then give me the threat actors hostname. At first I used nslookup on the IP which gave me the DNS of the attacker which I realised wasn't what the question was after.
![rdp2](/static/images/rdp3.png)

## Inital access via phishing
This is the much more common method of gaining inital access since it is harder to mitigate than just simply blocking RDP access. HoxHunt phishing trends report, 2025 - shows phishing attacks have increased 41x since the release of ChatGPT in 2022. This challenge has me look at two phishing techniques: Binary attachments and LNK attachments.

- Binary attachments: With binary attachments threat actors do two things
    1. Attempt to use unknown file extensions like .com .scr or .cpl since people are more aware of not clicking .exe files.
    2. Abuse windows feature that hides known file extensions by default so invoice.pdf.exe actually looks like invoice.pdf in the files.

- LNK attachments: With LNK attachments threat actors attempt to hide powershell, visual basics and BAT scripts over binaries, hiding them behing LNK shortcuts to trick end users.

Sysmon is very usefull for detecting this type of initiall access:
1. Sysmon event ID 1: Web browser launched
2. Sysmon event ID 11: A file (usually archived) is downloaded
3. Sysmon event ID 11: User may unarchive files to some folder
4. Sysmon event ID 1: The user double-clicks the unarchived file

### Exercises
**Which file did the user download via the web browser**
Using Sylog evenID 11 makes looking for suspicious downloads pretty easy when you know how to ID suspect downloads as I can also use the find feature to look for suspicious file extensions such as archive extensions which was .zip in this case
![phishingia](/static/images/phishingia.png)

**In which folder did the user unarchive the suspicious file?**
Since I had the name of the file I cleared my filters and used the file name in the find function until I landed on an event ID 15 event.
![phishingia1](/static/images/phishingia1.png)

**what is the process ID of the launched phishing malware**
Since I have the process ID for the file unarchive I can use this in the search file as it will be the parent ID in event for the launched phishing malware
![phishingia2](/static/images/phishingia2.png)

**Which malicious domain did the malware try to connect to**
Same as last exercise I just used the process ID of the launched malware event to search for theevent 22 ID event dns query
![phishingia3](/static/images/phishingia3.png)

## Inital Access via USB
Infected USB drives, despite cloud services, are stil are real method of initial access and occurs by pluggin in an infected USB into a device. The USB can belong to the threat actor and make its way to the victim or the USB may be the victims and it ended up infected by plugging it into someone elses print service that is infected with a worm. USB access also passes firewalls like phishing.

Detecting inital access by USB is very similar to phishing since it starts with a user running malicious binary via a graphical interface like explorer.exe

### Exercises
**Which USB file was launched by the user**
Filtering for event ID 1 in the syslogs and using "E:\" in the find function allowed me to discover the USB launch event quickly
![usb1](/static/images/usb1.png)

**Which suspicious file did the malware drop to the disk**
Using the process ID from the event found in the previous exercise I can use this to find any events related to the USB launch. I also could have filtered for event ID 11 and used the USBs name in the find function to find the event due to the "Image:" tag in the event.
![usb2](/static/images/usb2.png)

**To which other USB did the malware propagate**
Again using the process ID I'm able to discover all events related to the process launch and found another event 11 ID where the target file system was another USB drive.
![usb3](/static/images/usb3.png)

## Conclusion
To conclude this room covered the most common ways of gaining initial access and how to discover them in the event logs.

Takeaways:
> The two most common methods are exposed services and user-driven
> Inital Access via RDP can be easily detected using default auth logs (4624/25)
> User-driven attacks are best detected by process execution events
> Each initial access method has unique features that will be learnt through practice

---

- **Windows security - Intial access**
- **TryHackMe**
- **Medium**
- **2026-07-24**
- **Windows Security**
- **A write up initial access methods used against windows OS and how to discover them in logs**
