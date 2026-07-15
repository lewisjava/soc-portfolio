---
title: Network Analysis - Basics
platform: TryHackMe
difficulty: easy
date: 2026-07-15
tags: [Network traffic]
summary: A write up to the basics of network traffic analysis, capturing, inspecting and analysing.
---

# Network traffic analysis
Network traffic analysis (NTA) is a metho of monitoring network availability and activity to identify anomalies, including security and operational issues. It includes correlating several logs, deep packet inspection and network flow statistics with specified outlined goals.

## The purpose
![dns](/static/images/dns.png)
Taking a look at the example DNS logs above it can be seen there is multiple ND queries going to the same TLD, each time using a different sub domain. The DNS logs provide the following info;
- Query and querytype
- subdomain and top level domain: Tool like VirusTotal will verify if malicious
- Destination IP: Tool like VirusTotal will verify if malicious
- Host IP
- Timestamp

However this doesn't provide much information, therefore inspection of the DNS traffic and checking the content of the queries and replies will provide much more information.

![dnspacket](/static/images/dnspacket.png)
By examining one of the packets in the image above it can be seen that the content of a DNS reply contains C2 commands meaning what was taking place was DNS tunneling and Beaconing (TA0011, TA0010, T1572 & T1071.004). Without analysis of the network traffic this would never have been discovered.

## What can be analyses
The traffic that can be observed is everything within the TCP/IP model and what can be found in each layer of this model is as follows:

- Application: Application header + Data
- Transport: Transport header, Application Header + Data
- Internet: IP header, transports header, Application header + Data
- Link: Link header, IP header, transport header, Application header + Data

### Appliction
On the application layer the header info and the payload can be analysed, this information changes depending on which application layer protocol is used. Using HTTP as an example from firewall logs:
![application layer](/static/images/applicationlayer.png)
In this layer the GET request for a download can be seen and the response code 200 signifying it's success, and what can also be seen is the name of what was downloaded, it's size, but not what's inside.

### Transport
Going deeper into the transport layer where the application data and header are segmented and encapsulated. Using the firewall logs the TCP/UDP data can be analysed and this layer provides source and destination ports and the flags, these are valuable for detecting certain types of attacks such as session hijacking which can be detected by analyzing the sequence numbers included in the transport header. If the sequence numbers are suddenly far apart, further investigation is waarranted.
![transport layer](/static/images/transportlayer.png)
Looking at the example wireshark packet capture above the first 3 lines show a normal TCP 3-way handshake, line 4-5 show legit data transfer and line 6 shows a packet from another source trying to inject itself into the session as can be seen by the massive jump in the sequence number.

### Internet
When the transport layer sends down a segment the internet layer adds it's header. The fields most logged here are the source and destination IP and the time to live. If you wanted to detect fragmentation attacks this will not suffice however, what will need to be inspected is the fragment offset and total length fields as well. A fragmentation attack has many variations, one attack can create tiny fragments to evade IDS or mess up the reassembly of fragmetns by using overlapping byte ranges.
![fragmentation](/static/images/fragmentation.png)
In the above example the attacker is attempting mess up reassembly by using overlapping byte rangesas the offset in line 3 overlaps with the one in line 2 meaning the complete packet can be reassembled in one way or the other.

### Link
Finally once the internet layer finishes encapsulation the IP packet is sent to the link layer. Here the link layer adds it's own header containing addressing information. Most logs will display the source and destination MAC address but for attacks like ARP poisoning or spoofing this will not suffice. Instead full packet analysis and context is required, for example in the logs what can't be seen is when the MAC address appears from multiple interfaces or when many ARP packets are sent out with conflicting MAC addresses.
![ARP poisoning](/static/images/arp.png)
In the example packet capture above it's demonstrated clearly the details of an ARP poisoning attack, the host with IP 192.168.1.200 is replying to each ARP request with the same MAC.

## Sources and flows
An organistation typically has some predetermined network flows and sources and sometimes it is more helpfull to focus on these. these sources and flows can be grouped into two categories:

Sources
1. Intermediary
2. Endpoint

Flows
1. North-south: traffic that exits or enters the LAN and passes the firewall
2. East-west Traffic that stays within the LAN

### Sources
**Intermediary**
These are devices through which traffic passes this includes firewalls, switches, web proxies, IDS/IPS, routers, access points, wireless LAN controllers etc. The infrastructure of Internet Service Providers is also included.

The traffic from these devices comes from routing protocols (EIGRP, OSPR, BGP), management protocols (SNMP, PING), logging protocols (SYSLOG) and other protocols (ARP,STP,DHCP)

**Endpoint sources**
These are the devices from which traffic originates and take the bulk of the network bandwidth. These are devices such as servers, hosts, IoT devices, printers, lab machines, cloud resources, mobile phones, tables and many more.

### Flows
**North-South traffic**
This is the traffic that is most closely monitored since it travels from the LAN to the WAN and vice versa. The most well known services in this category include HTTPS, DNS, SSH, VPN, SMTP, RDP and mure. These protocols have two streams Ingress (Inbound) and egress (Outbound). This traffic must pass the firewall in one way or another so configuring firewall rules and logging properly are key.

**East-west traffic**
This traffic stays within the orgs LAN, so is monitored less. However it's still important to monitore in the event the network is compromised the attacker will exploit services internally to move laterally in the network (TA0008). There are many services within this category that includes: Directory authentication and ID services, File shares and print services, Router switching and infrastructure services, application communication, backup and replication, monitoring and management and more.

## Observing network traffic
Network traffic analysis is built on combining multile sources of info, analysing them, finding patterns and using the results to inform actions. The main sources of information are:
- Logs
- Full Packet Capture
- Network Statistics

### Logs
Logs are the entry point. Each system and protcol in the network has a way of logging information, for example Microsoft implements Windows Event Logs. However the data logged by protocols and system is up to the vendor and includes what they deem useful such as source/destination IPs.
![Network log](/static/images/networklog.png)
In the above example log. There is the logs of authentication on a linux host using the Syslog format

### Full packet capture
When logs don't provide enough information full packet capture is required, there are two ways of doing this:
- Network tap
- Port mirroring

A network tap is a physical device placed inline in the network and copies all the network traffic without affecting performance. Port mirroring is a software alternative such as an IDS, packet capture box or other systems.

Depending on what is used there is considerations to take place. THe placement of the TAP or configuring of the mirror in the right place to capture the right traffic. Full packet capture requires sufficent storage. Finally if mirroring this can impact performance is large amounts of traffic pass through the mirrored port.

Tools are reuiqred for analysis of packet captures, the most commoon are wiresharl, TCPdump and IPS/IDS like snort, suricata and zeek

### Network statistics
Another way of finding anomalies is through gathering metadata of the data flowing through the network. An example would be counting the number of DNS requests a host sends out. Two example protocols cover this function: NetFlow and IPFIX

- NetFlow: Cisco tool that is good for detecting C2 traffic, data exfiltraion and lateral movement
- IPFIX: Considered the successor to NetFlow: Includes vendors beyond Cisco, similar features to NetFlow but more flexiblity in which field to capture.

## Conclusion
Network analysis is fundamental to understanding what is occuring within a network and required mutliple sources of information from logs, packets and network statistics to get an understanding of what is taking place and if their is any suspicious or malicious activity taking place.

---
- **Network Analysis - Basics**
- **2026-07-15**
- **Network analysis**
- **An understanding of the basics to network analysis**
