---
title: IP, Common Ports and Protocols
date: 2026-06-06
tags: [networking, ports, protocols, tcp, udp]
summary: An analogy for how IP/TCP/UDP encapsulation works, plus the ports and protocols a SOC analyst needs memorised.
---

# IP, Common Ports and Protocols

## Intro to IP

A useful analogy: think of it as a series of moving vans.

- The network topology is a road.
- The truck on the road is the IP address (layer 3).
- The boxes inside hold the data — TCP and UDP (layer 4).
- Inside the boxes are more things, like application information (layer 5).

This is called **encapsulation** — data sits inside data.

The IP delivery truck delivers from house address to house address (IP addresses). When it arrives at a house, the boxes need to be stored in the right rooms — this is done using port numbers.

![Encapsulation diagram — IP, TCP/UDP, and application data layered together](/static/images/notes/networking/ip-ports-diagram.png)

## Common ports

| Protocol | Description | Port |
|---|---|---|
| FTP | Transfers files | tcp/20, tcp/21 |
| SSH | Secure Shell | tcp/22 |
| SFTP | Secure FTP | tcp/22 |
| Telnet | Telecommunications network | tcp/23 |
| SMTP | Simple Mail Transfer Protocol | tcp/25 (plaintext), tcp/587 (TLS encrypted) |
| DNS | Domain Name System — converts names to IP addresses | udp/53 |
| DHCP | Dynamic Host Configuration Protocol | udp/67, udp/68 |
| TFTP | Trivial File Transfer Protocol | udp/69 |
| NTP | Network Time Protocol | udp/123 |
| SNMP | Simple Network Management Protocol | udp/161 |
| LDAP / LDAPS | Lightweight Directory Access Protocol — stores and retrieves info in a network directory | tcp/389 |
| SMB | Server Message Block — file and printer sharing across the network | tcp/445 |
| Syslog | Consolidated logging across diverse systems, usually used alongside a SIEM | udp/514 |
| MS-SQL | Microsoft's database protocol | tcp/1433 |
| RDP | Remote Desktop Protocol | tcp/3389 |
| SIP | Session Initiation Protocol, used for VoIP | tcp/5060, tcp/5061 |

SNMP traps are alerts and notifications sent from network devices. Databases use SQL (Structured Query Language) to query and retrieve data.

## Other useful protocols

**ICMP** — Internet Control Message Protocol. Used to send a message to a device to check if it's operational and get a response back — this is what the `ping` command does.

**GRE** — Generic Routing Encapsulation. Creates a tunnel between two endpoints, allowing encapsulation at one end and decapsulation at the other.

**VPN protocols** — allow encryption of data sent across tunnels. A concentrator (specialised cryptographic hardware) is sometimes used. A site-to-site VPN is always-on, with firewalls acting as the concentrators, ensuring data sent across the network to the other site is encrypted.

**IPsec** — IP security. Provides authentication and encryption at layer 3 for every packet. Two primary protocols: Authentication Header (AH) and Encapsulating Security Payload (ESP).

**IKE (Internet Key Exchange)** — allows two parties to agree on an encryption/decryption key without sending the key across the network. This builds a Security Association (SA) using Diffie-Hellman on udp/500 for phase 1; phase 2 builds the ESP tunnel.

**AH (Authentication Header)** — hashes the packet with a shared key, using MD5, SHA-1, or SHA-2. Adds the AH to the packet header.

**ESP (Encapsulating Security Payload)** — encrypts the packet using the same hashing protocols as AH, but also adds 3DES or AES for encryption, plus an integrity check value to ensure data was received properly.

## Network communications

- **Unicast** — one sends information to one other station (one-to-one).
- **Multicast** — one-to-many-of-many.
- **Anycast** — one-to-one-of-many.
- **Broadcast** — sends info to everyone. Used by routing updates and ARP requests.
