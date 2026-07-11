---
title: Summit - Pyramid of Pain
platform: TryHackMe
difficulty: easy
date: 2026-01-20
tags: [Framework, challenge]
summary: Can you chase a simulated adversary up the Pyramid of Pain
---

# Summit

The scenario for this THM challenge is to work with an external pen tester in an interative purple-team scenario, the tester will attempt to eecute malware samples on a simulated internal user workstation while you need to configure the security tools to prevent the malware executing.


## First flag
The first challenge requires us to scan a sample malware called sample1.exe and try to see if we can find a potentiall rule we can implement to block it based on the results. 

What we get back are is the general information (including the file hashes) and the behavioural information which shows us that the exe reads the machine GUID from the reg, checks LSA protection, reads the computer name and checks supported languages. It connects to an unusual port which flags it as suspicious and then we can see that metasploit is detected.

since this is the first step in the challenge we simply create a rule to block the hash and it works, the pen tester simply recompiles sample1.exe into sample2.exe and it able to bypass this rule.
![Sample 1 - IOC hash](/static/images/sample1.png)

## Second flag
Running this EXE we get that exact same results as last time except it is also flagged as connecting to a suspicious IP, we can use this and add it into the firewall rules to block the IP. Further to this the sample scan provides us with network activity including HTTP requests and connections.

So by blocking the destination IP on the egress we stop the sample from connecting to it's C2 server.

The pen testers response to this is to sign up to a cloud service provider and get access to many public IP's
![Sample 1 - IOC IP](/static/image/sample2.png)
## Third flag
In this third sample we get more network activity, including DNS requests this time. By adding the domains to the DNS filter we stop the sample again from connecting to the C2 server much more solidly this time because no matter what IP address the domain has it will still get blocked causing the pen tester more issues. Their response to this it to purchase and register some new domain names and modify DNS records.
![Sample 3 - IOC DNS](/static/images/sample3.png)
## Fourth flag
In the fourth sample in the behavioural analysis we can see under the malicious category that the executable disables windows defender real-time monitoring and downloads executable files from the internet. Under the suspicious category it also makes changes to the registry which is an artifact we can use.

In the modification events it can be seen that the executable modifies a microsoft HKEY related to realtime monitoring. By adding the key effected to the rule builder we can block the actual behaviour of the malware, now the pentester has to develop new techniques used in their tools which costs a lot of time and money.
![sample 4 - IOC Registry edited](/static/images/sample4.png)
## Fifth flag.
The final sample simply gives logs which includes the dates, src and destination ips and ports and bytes sent for connections from the victim machine. Looking at it we can see there is a continous stream of 97 bytes to a destination which may singal that beaconing is taking place. all we have to do here is to block any ip (this prevents IP addresses work around) and any port where a size of 97 bytes leaves every 30 minutes and flag it as suspicious network behaviour. The pentester now has to develop a brand new tool and will have to train themselves on it, at this point the reward is no longer worth the effort.

Sample 5 - IOC C2 (Continous repeated outbound connection occuring every 30 minutes with exact same bytes ammount)
## Sixth and final flag
In this final flag we are simply shown the command log with this we are attacking the top of the pyramid of pain, the pentesters techniques and procedures.
from the commands we can see that the pentester is attempting to exfiltr8 all of the data thoughout the target machine. by simply adding the file used for exfiltration and it's path location in %temp% to the rules we block the penstesters goals directly, at this point no matter what tool they use or develop they will have to also develop a new set of techniques and procedures to achieve their goal.
![Sample 6 - IOC TTP'](/static/images/sample6.png)

## Conclusion
Throughout this demonstration we can see how much each of our actions disrupts the attackers goals from the minimal effect of blocking hashes to the maximum disruptive effectt of blocking their techniques and procedures rendering anything they attempt useless and requiring them, if they want to continue, to have to build their plan from the ground up. This demonstrates quite clearly where and how a defensive team focuses matters in disrupting and preventing malcious actors.

---

- **Summit**
- **TryHackMe**
- **Easy**
- **2026/07/11**
- **Framwork, Challenge**
- **Chase the adversary to the top of the pyramid of pain**
