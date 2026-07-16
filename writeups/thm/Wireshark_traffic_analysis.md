---
title: Wireshark - Traffic analysis
platform: TryHackMe
difficulty: Medium
date: 2026-07-16
tags: [Wireshark, traffic analysis]
summary: Using wireshark to correlate packet-level info to detect anomalies and malicious activities
---

# Wireshark - Traffic analysis
This writeup will over investigating packet-level details by using wireshark to detect anomalies and odd situations for a given case.

## Nmap scans
### Nmap basics
Nmap maps networks and it has three common Nmap scan types:
- TCP connect scans
- SYN scans 
- UDP scans

TCP filters
|Wireshark filter|description|
|----------------|-----------|
|TCP   UDP|Global search|
|tcp.flags == 2|only SYN flag|
|tcp.flags.syn == 1|SYN flag set, rest of bits not important|
|tcp.flags == 16|Only ACK flag|
|tcp.flags.ack == 1|ACK flag set, rest of bits not important|
|tcp.flags == 18|Only SYN, ACK flags|
|(tcp.flags.syn == 1) and (tcp.flags.ack == 1)|SYN and ACK are set, rest of the bits not important|
|tcp.flags == 4|Only RST flag|
|tcp.flags.reset == 1|RST flag set, rest of the bits not important|
tcp.flags == 20|Only RST and ACK flags|
|(tcp.flags.reset == 1) and (tcp.flags.ack == 1)|RST and ACK are set, rest of the bits not important|
|tcp.flags == 1|Only FIN flag is set|
|tcp.flags.fin == 1|FIN flag is set, rest of the bits not important|

tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size > 1024 = TCP connect scan display filter
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size <= 1024 = TCP SYN scan display filter
icmp.type==3 and icmp.code==3 = UDP scan patterns display filter
### Exercise
**What is the total number of the TCP connect scans?**
The first challenge simply asks for the amount of packets that are TCP connect scans, using the aforementioned TCP connect scan display filter should give the answer
![tcpconnect](/static/images/tcpconnect.png)
As seen in the screenshot this display filter gives back a thousand packets (which is the correct answer). This is also an example display filter that will be bookmarked for further use as it's a usefull filter for finding TCP connection patterns.

**Which scan type is used to scan the TCP port 80**
By putting in "tcp.port == 80" it will return all connections at this port all then that's needed is to see the pattern to know which scan was used.
![port80](/static/images/port80.png)
Looking at the results in the screnshot is SYN -> SYN, ACK -> ACK -> RST, ACK. Meaning the full three-way handshake is complete making this a TCP connect scan.

**How many UDP close port messages are there**
This is a simple challenge since all it requires is that we filter for ICMP since this protocol gives the response when a UDP port is closed
![udp port closed](/static/images/udppostclosed.png)
as seen in the screenshot above this returns 1083 packets which is the correct answer for the challenge.

**Which UDP port in the 55-70 port range is open?**
Using the "in" syntax from the previous writeup provides an easy way to get port numbers within a range so applying "udp.port in {55 .. 70} gives back only a full open connection to port 68.
![port68](/static/images/port68.png)

## ARP poisoning and man in the middle
ARP poisoning/Adversary in the middle (T1557.002) is an attack that allows attackers to position themselves between the communication of two or more networked devices. This is done by sending malicious ARP pacets to the default gateway to manipulate/jam the network.

|Wireshark filter|Description|
|----------------|-----------|
|arp|Global search|
|arp.opcode == 1|ARP requests|
|arp.opcode == 2|ARP responses|
|arp.dst.hw_mac==00:00:00:00:00:00|ARP scanning|
|arp.duplicate-address-detected or arp.duplicate-address-frame|Possible ARP poisoning detection|
|((arp)) && (arp.opcode == 1)) && (arp.src.hw_mac == target-mac-address)|Possible ARP flooding from detection|

A suspicious situations means having two different ARP responses conflict for a particular IP address which will then be flagged by wireshark, figuring out which of thw two is legit and which isn't is the analysts job.

### Exercise

**What is the number of ARP requests crafted by the attacker?"**
First this requires identification of the attacker but this is made easy in the example packet capture as there is a MAC address that is making many ARP requests.
![arp requests](/static/images/arprequests.png)
By searching for all packets containing the attackers MAC address as the src and using arp.opcode == 1 all ARP requests are returned giving the value 284

**What is the number of HTTP packets received by the attacker**
Here instead the attackers MAC addressed is flipped to the dst instead of the src and the protocol search is filtered for HTTP and this returns 90 which is the answer.
![ARP http](/static/images/arphttp.png)

**What is the number of sniffed username and password entries** 
For this I filtered for the dst mac address for the attacker and the HTTP POST requests which returned only 10 packets then I manually read these that contained the strings uname and pass and it turns out the attacker gained 6 usernames and passwords
![HTTP post](/static/images/httppost.png)

**What is the password of the client client986**
The password of this client is in the previous screenshot and is clientnothere!

**What is the comment provided by the client354**
One of the HTTP POST requests was named comment.php and showed up in my previous display filter and was therefore easy to find.
![commentphp](/static/images/commentphp.png)

## Identifying hosts: DHCP,NetBIOS and Kerberos
When investigating a compromise or malware IDing hosts on the network beyong IP and MAC address is kessential.

### DHCP
|wiresharkfilter|Description|
|---------------|-----------|
|dhcp|global search|
|dhcp.option.dhcp == 3|DHCP Request|
|dhcp.option.dhcp == 5|DHCP ACK|
|dhcp.option.dhcp == 6|DCHP NAK|
|dhcp.option.hostname contains "Keyword|Searches for the hostname within the keyword|
|dhcp.option."option 50/51/61/15" contains "keyword"|Searches for a specific word within any of the aforemetioned options|

### NetBios
The tech responsible for allowing applications on different hosts to communicate with one antoher.

|Wireshark filter|description|
|----------------|-----------|
|nbns|Global search|
|nbns.name contains "keyword" : such as "name", "ttl" and "ip address details"|nbns options|

### Kerberos
The default authentication service for Microsoft windows domains.

|Wireshark filter|Description|
|kerberos|global search|
|kerberos.CNameString contains "keyword"|User account search|
|(Kerbero.CName string contains "$")|Hostname information the values that end with $ are hostnames those without are usernames|
|kerberos.pvno == 5|protocol version|
|Kerberos.realm contains ".org"|domain name for the generated ticket|
|kerberos.nameString == "krbtg"|Service and domain name for the generated ticket|

### Exercises
**What is the MAC address of the host "Galaxy A30"**
Applying the filter dhcp.option.hostname contains "galaxy" gives us the packets with this hostname and searching the packet for the MAC address reveals it for us.
![dhcp](/static/images/dhcp.png)

**How many NetBios Registration requests does the LIVALJM workstation have**
Initially searching the the nbns name for LIVALJM returns 40 packets but searching inside the registration packets I extracted the display filter specific for regitrations and applied it to the display filter which returned 16 packets which is the answer.
![nbns](/static/images/nbns.png)

**Which host requested the ip addres 172.16.13.85**
Using the expression filter table it allowed me to easily find and built the correct expression among the many dhcp options to find the answer
![dhcp](/static/images/displayfilterip.png)
![galaxya12](/static/images/galaxya12.png)
Which gave the answer galaxy-a12

**what is the ip address of the user u5**
Simply using the display filter kerberos.CNameString contains "u5" gives us the answer.
![cname](/static/images/cname.png)

**What is the hostname of the available host in the kerberos packets**
By applying the cname as a column all the kerberos packets will also have their appropriate hostnames next to them and this makes it very easy to find.
![Kerberos](/static/images/kerberos.png)

---

## Frontmatter field reference

The block between the `---` lines at the top is the "frontmatter". Fields:

- **title** — required. The display title.
- **platform** — optional. Shows as a badge (e.g. TryHackMe, LetsDefend).
- **difficulty** — optional. One of: easy, medium, hard. Shows as a coloured tag.
- **date** — optional but recommended. Format YYYY-MM-DD. Used for sorting.
- **tags** — optional. Comma-separated list in square brackets.
- **summary** — optional. One-sentence description shown on cards.

For **certs**, use `status: passed` / `studying` / `planned` and `org: CompTIA` instead of platform/difficulty.
