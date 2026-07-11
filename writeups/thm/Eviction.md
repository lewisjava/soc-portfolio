---
title: Eviction
platform: TryHackMe
difficulty: easy
date: 2026-07-11
tags: [Framework, Challenge]
summary: Use the MITRE ATT&CK framework to understand the APT28 group
---

# Eviction
In this challenge we are an SOC analyst who has been sent an intelligence report that suggest there will be an attack orchestrated by the APT group APT28, we must use the MITRE ATT&CK framework to understand this adversary and properly defend.

## TTPS
### Recon and inital access
Since this is the starting point of attacks we'll use MITRE to understand how they will work at this stage of an attack.
![APT28 navigator](/static/images/APT281.png)
Looking at the navigator above, under both recon and initial access we can see that this group use spear phishing for both and that this will likely be how they start the attack.


### Resource development
If APT successfull during the recon and inital access phase where hey conduct initial credential phishing campaigns with embedded links to the attacker controled domains, they will then move onto resource development phase. In this phase we can assume they will work on email accounts out of their techniques in this stage where they will either replicate through removeable media where this group uses infected USBs to transmit through devices or through trusted relationships where they use the inital access emails as a social engineering angle.
![APT28 Resource development](/static/images/APT282.png)

### Execution
If the group makes it this far they always use the emails they have to attempt User execution through social engineering where the execution will be by Malicious File and/or Malicious link
![APT28 Execution](/static/images/APT283.png)


If they are successfull with this then the SOC must search for the relevant scripting interpreters looking at the MITRE map for APT28 group we can see they use either Powershell or Windows command shell
![APT28 Shells](/static/images/APT284.png)

### Peristence
Once any group gains a foothold they will seek to gain persistence, while the SOC looked over the scripting interpreter the SOC noticed obfuscated scripts that changed the registry editor, combinbing this information with their MITRE map we can see that they're likely editing the Registry run keys and that the SOC should track these.
![APT28 Persistence](/static/images/APT285.png)

### Defence Evasion
The SOC for this task identifies that the APT executes system binarie to evade defences, using the MITRE map that they use specifically the Rundll32
![APT28 Defence Evasion](/static/images/APT286.png)

### Discovery
The SOC for this task discovers that TCPdump has been used on of the compromised hosts, we can assume this is an attempt at discovery, by using MITRE we can map the technique and understand what specifically they're objective is here and why.
![APT28 Discovery](/static/images/APT287.png)

### Lateral movement
Since the group used TCPdump to network sniff, their next move is very predictable as we see in the task they acheive lateral movement via exploiting remote services, but which remote service should Sunny observe to ID APT activity traces. The answer to this is easy when consulting the MITRE map, where we can see the SMB/Windows Admin Shares.
![APT28 Lateral movement](/static/images/APT288.png)

### Collection
In this example the aim of the group is to steal intelectual propert from the buisnesses repositories, maeaning their goal for this phase is collection, but how? Agin by using the knowedlge of the MITRE batabase and knowledge of the adversary we can easily see that the the target repository will bethe sharepoint.
![APT28 Collection](/static/images/APT289.png)

## Conclusion
In conclusion this task demonstrates and also allowed me to develop the skills to use and navigate the mitre ATT&CK framework to map a known adversary group APT28 by understaning their TTP's it makes it much easier to predict and consequently defend against an adversay showcasing the power that knowledge of attacks and frameworks offer.


---
- **Eviction - A mitre att&ck challenge**
- **TryHackme**
- **Easy**
- **2026/07/11**
- **Framework, Challenge**
- **Using the mitre att&ck framework to map an attack from a known adversary**
