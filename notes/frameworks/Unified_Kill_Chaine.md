---
title: Unified Kill Chain
date: 2026-07-10
tags: [Framekwork]
summary: A complementary cyber security kill chain framework
---

# Unified kill chain

The unified kill chain is an 18 step framework that is used to complement Lockheed Martins kill chain and MITRE's ATT&CK framework.

The 18 steps are as follows:

1. Recon - Researching, identifying and slecting targets using active or passive recone.
2. Weaponization - Prepatory activities aimed at setting up the infrastructure required for the attack.
3. Delivery - Techniques resulting in the transmission of a weaponized object to the target environment
4. Social engineering - Techniques aimed at the manipulation of people to perform unsafe actions
5. Exploitaion - Techniques to exploit vulnerabilties.
6. Persistence - Any access, action or change to a system that gives an attacker persistent presence on the system.
7. Defence evasion - Techniques an attacker may specifically use for evading detection and other defences
8. C2 - Techniques that allow attackers to communicate with controlled systems within a target network
9. Pivoting - tunneling traffic through a controlled system to other systems that are not directly accessible
10. Discover - Techniques that allow an attacker to gain knowledge about a system and its network environment.
11. Privilege Escalation - The result of techniques that provide an attacker with higher perms on a system/network
12. Execution - Techniques that result in execution of attacker-controlled code on a local or remote system
13. Credential Access - Techniques resulting in the access of, or control over, system, service or domain credentials
14. lateral movement - Tehcniques that enable an adversay to horizontally access and control other remote systems
15. Collection - Techniques used to ID and gather data from a target network prior to exfiltration.
16. Exfiltration - Techniques that result or aid in an attacker removing data from a target network.
17. Impact - Techniques aimed at manipulating, interrupting or destroying the target system or data.
18. Objectives - Socio-technical objectives of an attack that are intended to achieve a strategic goal

These can be split up into three main goals of an attacker: In, through and out.

## In
The inital goal of any attacker is to gain access and gain a foothold in their target system and they will employ numerous tactics to do so. In this phase the first 9 steps of the kill chain are used.

### Recon (MITRE Tactic TA0043)
This phase of the UKC covers techniques that an attacker would emply to gain information about the target system using either passive or active recon and the information gathered here sets the stage fr the rest of the attack and kill chain.

Information gathered from this phase includes:
- Discovering what systems and services are running on the target
- Finding contact lists or lists of employees that can be impersonated
- Looking for credentials that may be of use later in later stages such as pivoting.

### Weaponization
This phase of the UKC describes the adversay setting up the necessary infrastructure to perform the attack, this could be setting up a C2 server a system capable of catching reverse shells and elivering payloads.

### Social engineering (MITRE Tactic TA0001)
This phase described techniques that an adversay can employ to manipulate employees to perform actions that will aid in the adversaries attack. This could include:
- Getting a user to open a malicious attachment in a phishing emil.
- Impersonating a web page and having the user enter their credentials.
- Calling or visiting the target and impersonating a user

### Exploitation (MITRE Tactic TA0002)
This phase describes how an atacker takes advantage of weaknesses or vulnerabilites present in a system. for example:
- Uploading and executing a reverse shell to a web application
- Interfering with an automated script on the system to execute code
- Abusing a web application vulnerabilit to execute code on the system it is running on

### Persistence (Mitre Tactic TA0003)
This phase details the techniques an adversary uses to maintain access to a system they have gained an intial foothold on, for exmaple:
- Creating a service on the target system that will allow the attacker to regain access.
- Adding the target system to a C2 server where commands can be executed remotely at any tie
- Leaving other forms of backdoors that execute when certain actions occur

### Defence evasion (Mitre Tactic 0005)
One of the more valuable phases of the UKC this is used to understand the techniques used to evade defensive measured put in place in the system or network, for example:
- Web application firewalls
- Network firewalls
- Anti-virus systems
- IDS

This phase is valuable when analysing an attack as it helps form a response better and gives the defensive team info on how they can better improve their defence systems for the future.

### C2 (MITRE Tactic TA0011)
The C2 phase combines the efforts made during the weaponization stage to establish comms between the adversary and target system once done the adversary can establish command and control of a target system and execute their objectives such as:
- Execute commands
- Steal data, credentials and other sensitive information
- Use the controlled server to pivot to other systems on the network

### Pivoting (MITRE Tactic TA0008)
Pivoting is the technique used to reach other systems within a network that are not otherwise accessible (for example they are not exposed to the internet), there are often many systems in a network that are not directly reachable and often contain valuable data.

Normal paragraph text. You can use **bold**, *italic*, `inline code`, and [links](https://example.com).

## Through
Through goals follow on from a foothold being estabilshed.

### Pivoting (MITRE TACTIC TA0008)
Pivoting is also continued here where once the attacker has gained access they will use their inital access and turn the system into a staging site and as a tunnel between their command operations and the victims network. Furhter to this the system would also be used as the distribution point for all malware and backdoors at later stages

### Disovery (MITRE Tactic TA0007)
In this stage the attacker will be uncovering information about the system and the network it is connected to, the knoweldge base would be built from the active user accounts, permissions granted, apps and software in use, web browser activity, files, directories, network shares and system configs.

### Privilege Escalation (MITRE Tactic TA0004)
Following on from and using the info gathered during Discovery, the attacker will attempt to gain more prominent permissions within the pivot system by exploiting vulnerabilities and misconfigs found and will attempt to access the usual accounts:
- SYSTEM/ROOT
- Local administrator
- A user account with Admin-like access
- A user account with specific access or functions

### Execution (MITRE Tactic TA0002)
Having gained sufficient privileges the attacker during this stage will attempt to deploy their malicious code using the pivot system as their host. Remote trojans, C2 scripts, malicious links and scheduled tasks are deployed and created to facilitate a recurring presence on the system and uphold their persistence

### Credential access (MITRE Tactic TA0006)
This stage usually wors hand in hand with privilege escalation, the attacker would attempt to steal account names and passwords through various methods including keylogging and credential dumping.

### Lateral movement (MITRE Tactic TA0008)
With the credentials and elevated priviledges the attacker can now move through the network and jump onto other targeted systems with much more ease to attempt to achieve their primary objective. the stealthier the technique used the better.

## Out (Action on Objectives)
The out goal is the final phases of the malicious actors attac on the environment, where they now have critical asset access and can fulfil their attac goals which are usually geared toward comrpomising the CIA triad.

### Collection (MITRE Tactic TA0009)
After all the hunting foor access and assets the attacker will be gathering all the valuable data of interest, which in turn compromises the confidentiality of the data and would lead to the next state of attack, Exfiltration. The main targets being drives, browsers, audio, video and email.

### Exfiltration (MITRE Tactic TA0010)
To elevate their compromise the attcker will steal the data, packaged using encryption measures and compressed to avoid detection. The C2 channeel and tunnel deployed earlier will be used here.

### Impact (MITRE Tactic TA0040)
If the attacker wanted to also compromise the integrity and the availability of the data assets then they would also manipulate, interrupt and/or destroy these assets. The goal would be maximum disruption to the business and operational processes and may involve removing account access, disk wipes and data encryption.

---


- **Unified Kill Chain**
- **2026/07/10**
- **Framework**
- **A guide to the Unified kill chain framework**
