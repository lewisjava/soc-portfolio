---
title: Network Discovery
platform: TryHackMe
difficulty: Medium
date: 2026-07-19
tags: [Network Security]
summary: How attakers discover assets in a network and how to defend from it 
---

# Network discovery
An attacker can't attack something they can't see or know about so all attackers start by trying to discover an orgs assets that are open on the internet, this is called the attack surface. During the discovery phase the attacker will attempt to discover what assets can be accesses, IP addresses, ports, OS and services running on the assets and what versions. Defenders also do the exact same thing because you can't defend what you don't know or exists on the network.

## External vs Internal scanning
External scans usually target the public facing assets on the perimeter and are observeed by an external IP as the source and an internal IP as the destination, this indicates the attack is still in the reconnaissance phase (TA0043). In this case the defender might want to block the source IP but refrencing the pyramid of pain the attacker will likely just mask their IP and return again.

Internal scans is internal-to-internal where the source and destination IP are bouth private IP addresses within the network, this indicates the attacker has moved onto the discovery phase (TA0007). This kind of alert is high-severity since they are now within the network and requires elevation and incident response.

### Exercises
**Which fil contains logs that showcase internal scanning activity**
We are presented with 3 logs exported from a SIEM with only 1 being sanitized and the other 2 being very difficut to read, with this I had to step away from the task and learn how to use the cut command to get the information I needed for this task which when I tried I realised wasn't enough and I needed to also use the -d command to cut based on a delimiter, the command I ended up with and used on both the unsanitized files allowed me to cut and print the source and destination IP addresses where I found in log-session-2.csv that this is where the internal scan took place.
![cut](/static/images/cut.png)

**How many log entries are present for the internal IP performing internal scanning activity**
I initally used grep to get the ip and then pipe it throughn wc -l to give me the answer and this returned the answer 4552 which is actually double the answer as there is another column that contains the source ip for rule, so i had to switch and use cat and uniq -c while using cut for the specific column to give the exact answer.

![cat](/static/images/cat.png)

**What is the external IP address that is performing external scanning activity**
This one is pretty simple since the internal IP logs have already been discovered it just involves cutting for the source IP field in the other logs and the source IP will be returned.

![external](/static/images/external.png)

## Horizontal vs Vertical scanning
Once they attacker is aware of the hosts present on the network they'll then attempt to find out what ports are open on said hosts.

In horizontal scanning the attacker will scan a singular port across multiple IP points, this is done when an attacker has a specific vulnerability they have in mind to exploit such as using WannaCry ransomware against the SMBv1 vulnerability which requires port 445 open.

Vertical scanning is the opposite where an attacker will scan a singular adress for multiple ports, this is done to footprint a host and see what ports they have open, an attacker may do this if they have found a valuable target and are atttempting to discover if it has any vulnerability to exploit..This can be identified by the same source IP scanning the same destination IP multiple times for different ports.

### Exercises
**One of the log files contains evidence of a horizontal san, which IP range was scanned**
This one exercise required looking at which of the logs contained multiple destination source IP and using the previous cut and delimeter command it was pretty easy, the answer for this challenge requires also to format the answer to CIDR block notation which is 203.0.113.0/24
![cidr](/static/images/cidr.png)

**In the same log file, there is one IP address on which a vertical scan is perfomed, which IP address is this**
There is only one IP address in this same log file that shows up multiple times and entering that IP does give the answer.
![vertical](/static/images/vertical.png)

**On one of the IP addresses, only a few ports are scanned which hosts common services, what are they**
cutting for the destination IP and destination port gives the answer pretty quickly as the common ports 80, 445 and 3389 show up repeatedly.
![common](/static/images/common.png)

## Mechanics of scanning
The 3 most common types of scan are:
- Ping sweep: send a ping and receive an ICMP packet back, often blocked by security controls
- TCP SYN: Send a SYN request to the target if a SYN-ACK is sent back then the host and the port is open, stealthy scan that often blends with the rest of traffic
- UDP scan: send a UDP packet and get back an ICMP port unreachable reply if not open and get nothing back if it is maybe open, very unreliable.

### Exercises
**Which source IP performs a ping sweep attack across a whole subnet**
Using ELK makes finding the target IP for this attack easy since I an filter for network.protocol, in this case specifically ICMP and filter for the source address which gives the IP performing the ping sweep.
![icmp](/static/images/icmp.png)

**The zeek.conn.conn_state value shows the connection state. using the info provided by this value ID the typ of scan pefromed by 203.0.113.25**
Putting the field provided and source ip into the elastic field builder the zeek state returned is s0, I had to look up the book of zeek documentation to understand what this means and it means a connection was attempted but not established meaning the attacker sent a SYN packet and is performing a tcp syn scan.
![syn](/static/images/syn.png)

## Conclusion
In conclusion network discovery is a way for both attackers and defenders to understand what exists and what is open on a network aswell as the tools and methods to do so and the different types of scans as well as the difference between vertical,horizontal,external and internal.

---
- **Network Discovery**
- **TryHackMe**
- **Medium**
- **20-07-19**
- **Network traffic**
- **A write up of the methods, tools and reasons for network discovery**
