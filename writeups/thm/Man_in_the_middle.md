---
title: Man in the middle
platform: TryHackMe
difficulty: easy
date: 2026-07-20
tags: [Network security]
summary: A write up of the man in the middle attack and how to detect/defend against it.
---

# Man in the middle
In man in the middle attacks (T1557), attackers position themselves between legitimate communicaiont endpoints to intercept, modify or redirect traffic. Detecting these attacks requires a multi-layered approach combining network monitoring, certificate validation and behavioral anaysis. This normally involves two key steps:

- Interception: the attacker sits themsleves into a communication stream, often by eploiting weaknesses in network protocols or by using techniques like ARP, DNS or IP spoofing
- Manipulation/Decryption: the attacker tries to access or modify the communicaion, decrypting encoded data or injecting jarmful content, such as altered website responses or fake login forms.

Common types of MITM attacks:
- Packet sniffing
- Session hijacking
- SSL stripping
- DNS spoofing
- IP spoofing
- Rogue Wi-Fi access point

Real world examples:
- Equifax, 2017: suffered a majore breach due to a MITM attack exposing sensitive data of over 100 million users
- Code injections by ISPs and state actors intercepting search traffic via SSL spoofing


## Detecting ARP spoofing

Indicators of attack:
- Duplicate MAC-to-IP mappings: Multiple MAC addresses claiming the same IP address indicates impersonation
- Unsolicited ARP replies: High volume of ARP replies without matching requests
- Abnormal ARP traffic volume: A large number of ARP packets in short intervals
- Unusual traffic routing: Traffic rerouted through the attacker's MAC
- Gateway redirection patterns: multiple destination MACs for the same gateway IP
- ARP probe/ reply loops: Many ARP requests with "who has 192.168.1.x tell 192.168.1.y" patterns

### Exercises
**How many ARP packets from the gateway MAC address were observed**
Since the IP for the gateway is provided I only needed to find the mac address associated with this IP and then filter for that mac addresses and for ARP protocol which shows 10 packets
![arpmitm](/static/images/arpmitm.png)

**What mac address was used by the attacke to impersonate the gateway**
Since we know the IP address and the MAC address associated with the IP, looking in the logs with the gateway IP there can be a switch from the legit MAC address to the fake one.
![macmitm](/static/images/macmitm.png)

**How many gratuitous ARP replies were observed for 192.168.10.1**
Using the same filter is before scrolling through the packets shows there are two gratuitous ARP replies

**How many unique MAC addresses claimed the same IP**
Since there is the legit mac address and the attackers there are two MAC addresses claiming the IP

**How many arp spoofing packets were observed in total from the attacker**
By adding the attackers MAC address as the source as a new display filter with the gateway IP shows all the ARP spoofing packets sent which is 14 with the gratuitous replies.
![arpspoofing](/static/images/arpspoofing.png)

## DNS spoofing

Indicators of attack:
- Multiple DNS responses for the same query: a legitimate resover and a forged responder reply to the same query
- DNS response from an unexpected source: A DNS reply arrives from an IP address that does not match any configured resolver
- Suspiciously short TTL values: attackers use low TTLs to keep poisoned entries short lived and reassert control
- Unsolicited DNS responses: A DNS repy appears without a corresponding DNS request from the victim

### Exercises
**How many DNS responses were observed for the domain corp-login.acme-corp.local**
This simply required filtering for responses where the response were corp-login.acme-corp.local which returned 211 packets

**How many DNS requests were observed from the IPs other than 8.8.8.8**
By going into the conversations tab and looking into the IPv4 tab there is only 2 packets send by one other IP indicating this IP sent 2 DNS requests
![dnsmitm](/static/images/dnsmitm.png)

**What IP did the attacker's forged DNS response return for the domain**
Adding the conversation found inthe conversation too the display filter displays the two packets where we can see the attackers forged IP
![forgeddns](/static/images/forgeddns.png)

## SSL stripping

Indicators of attack:
- Inital requests vs response: The users initial requests will be for HTTPS but the subsequent packets are in HTTP because the attacker has relayed it.
- Redirects/Link rewriting: Monitoring for redirects, HTTP status codes 301/302 that persisently direct an HTTPS request to an HTTP resource
- Certificate errors: Inital TLS/SSL handshake may fail or display a self-signed cert.

**how many POST requests were observed for the domain corp-login.acme-corp.local**
Filtering for posts requests and for the host corp-login.acme-corp.local shows only 1 

**What's the password of the victim found in the plaintext after successful SSL stripping**
Looking inside the above POST request shows the victims password
![sslstripping](/static/images/sslstripping.png)

## Conclusion
Looking at the timeline in the exercises the attack goes as follows:
- ARP spoofing: attacker sends unsolicited ARP is-at caiming gateway IP
- DNS spoofing: victim dns queries for corp-login.acme-corp.local, attacker responds with forged dns response 192.168.10.55
- SSL stripping: The victim initiates connection to resolved IP via HTTP to attacker and credentials are sent in cleartext

---
- **Man-in-the-middle**
- **TryHackMe**
- **Easy**
- **2026-07-20**
- **Network Security**
- **A write up of the man-in-the-middle attack with example**
