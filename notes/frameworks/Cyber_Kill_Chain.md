---
title: Cyber Kill Chain
date: 2026-07-10
tags: [Framework]
summary: The Cyber Kill Chain framework developed by Lockheed Martin
---

# Cyber Kill Chain
This guide will cover the 7 phases of the Cyber Kill Chain.
1. Reconnaissance
2. Weaponization
3. Delivery
4. Exploitation
5. Installation
6. Command and control (C2)
7. Actions on objectives.

### Reconnaissance
This is the research and planning phase of the attack, this incudes trying to understand infrastructure details, employee data, buisness processes and exposed technologies. This phase is often passive and undetected.

- Passive recon: involves having no direct interaction with the target, this may include WHOIS looups, social media scraping or revewing breach data.
- Active recon: This does involve direct contact and includes activites such as social engineering, port scanning, banner grabbing or probing for opern services.

OSINT (Open source intelligence) allows adversaries to gather insights about their targets through publicly aailable info. Some sources where OSINT data can be collected from include:
- Search Engines
- Print and online media
- Social media accounts
- Online forums and blogs
- Online public record databases
- WHOIS and technical data

One example of OSINT would be email harvesting which is the process of obtaining email addresses from public, paid or free services which could then be used for phishing or social engineering attacks.[TheHarvester](https://github.com/laramies/theHarvester)
[OSINT](HTTPS://osintframewor.com/)

### Weaponization
After recon the aim now is to turn the data from recon into actionable attack tools such as malware and exploits into a payload.

Some examples include:
- Creating an infected Microsoft office document containing a malicious macros or VBA scripts.
- Create a malicious payload, implant it on USB drives, then distribute them in public
- Set up C2 infrastructure for executing commands on the victim's machien or deliver more payloads

### Delivery
Delivery is when choosing the method for transmitting the payload onto the target environment.


Some examples include:
- Phishing email: after performing recon and determining the attack target, the malicious actor could craft a email that would target a specific person (spear phishing) or multiple within the company.
- USB drops: This offers a physical medium of deliver into public spaces like coffee shops, car parks or on the street.
- Watering hole attack: a targeted attack designed to aim at a specific group of people by compromising the website they are usually visiting, redirecting them to a malicious website of the attacker's choice or creation

### Exploitation
This is the moment the attacker's code executes and takes advantage of a known vulnerability.

some exampl techniques include:
- Malicious macro execution: This could be a phishing email that would execute ransomware when the victim opens it
- Zero-day exploits: Where the attacker leverages an unknown and unpatched fla in a system, leaving no opportunity for detection at the beginning.
- Known CVEs: The attacker can choose to exploit an unpatched public vulnerablity found on the target environment

Signs to look out for include: Unexpected process spawns, registry changes or new services created and suspicous command-line arguments found in the system logs.

### Installation
Once an attacker initally gains access they will want to set up what i known as a persistent backdoor, this allows them to regain access if they were to be detected or if they got detected and removed

Some methods for acheiving persistence are as follows:
- Installing a web shell on the webserver. due to web shell simplicity and formatting it is difficult to detect and might be classified as benign.
- Installing a backdoor on the victims machine such as using meterpreter to set up a shell on the victims machine.
- Creating or modifying Windows services. Known as technique T1543.003 in the MITRE ATT&CK frameworke an attacker can create or modify the Windows services to execute the malicous scripts or payloads regularly as a part of the persistence using the tools like ssc.exe and Reg to modify service configs. Further to this the attacker can also masquerade the malicious payload by using a service name that is known to be related to the OS or a legitimate software.
- Adding the entry to the "run keys" for the malicious payload in the Registry or start up folder which will force the payload to execute each time the user logs in to the computer

In this phase it is very likely the attacker will also use the Timestomping technique to avoid detection which allows them to modify file's timestamps, including to modify, access, create and change times.

### Command and control
Once a malicious attacker gets persistence their likely next step is to open up the C2 channel through the malware to control and manipulate the victim. This is known as C&C/C2 Beeaconing a type of malicious communication between a C&C server and the malware on the infected host and this communication is consistent. 

After estabilshing the connection between the external server and the compromised endpoint the attacker then has full control of the victim's machine.

The most comomon C2 channels used by adversaries include:
- HTTP on port 80 and HTTPS on port 443. This type of beaconing blends the malicious traffic with the legit traffic helping the attacker evade firewalls.
- DNS, where the infected machine makes constant DNS requests to the DNS server that belongs to the attacker. This type of C2 communication is also known as DNS tunneling.

### Actions on objectives
After going through the six phases the malicious actor will attempt to take the actions of their original objectives, some these could be;
- Collect the credentials from users.
- Perform privilege escalation
- Internal reconnaissance
- Lateral movement through the company's environment
- Collect and exfiltrate sensitive data.
- Deleting the backups and shadow copies
- Overwrite or corrupt data

and much much more.


---


- **Cyber kill chain**
- **2026/07/10**
- **framework**
- **The 7 phases of the cyber kill chain by Lockheed Martin**
