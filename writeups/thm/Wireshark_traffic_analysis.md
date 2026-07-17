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
|`(tcp.flags.syn == 1) and (tcp.flags.ack == 1)`|SYN and ACK are set, rest of the bits not important|
|tcp.flags == 4|Only RST flag|
|tcp.flags.reset == 1|RST flag set, rest of the bits not important|
tcp.flags == 20|Only RST and ACK flags|
|`(tcp.flags.reset == 1) and (tcp.flags.ack == 1)`|RST and ACK are set, rest of the bits not important|
|tcp.flags == 1|Only FIN flag is set|
|tcp.flags.fin == 1|FIN flag is set, rest of the bits not important|

`tcp.flags.syn==1 and tcp.flags.ack==0` and tcp.window_size > 1024 - TCP connect scan display filter
`tcp.flags.syn==1 and tcp.flags.ack==0` and tcp.window_size <= 1024 - TCP SYN scan display filter
`icmp.type==3 and icmp.code==3` - UDP scan patterns display filter
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
|`((arp)) && (arp.opcode == 1)) && (arp.src.hw_mac == target-mac-address)`|Possible ARP flooding from detection|

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

## DNS and ICMP
Traffic tunnerling/port forwarding is transferring data through scure tunnels that provide anonymity and traffic security making it highly valuable in orgs, but this same data encryption allows attackers to bypass security using the standad protocols like ICMP and DNS

### ICMP
ICMP anomalies usually occur after a malware execution or vulnerability execution as ICMP packets can transfer an addiotional data payload meaning attackers use this section to exfil data and establish C2 connections. IOC's usually include large volumes of ICMP traffic or anomalous packet sizes.

|Wireshark filter|Description|
|----------------|-----------|
|icmp|Global search|
|data.len > 64 and icmp|Searches for ICMP packets with a packet length greater than 64|

### DNS
Usually used to translate and convert IP domains to IP addresses attackers exploit this protocol for data exfil and C2 activites since it is commonly used and trusted it gets ignored by security protocols. Like ICMP, DNS anomalies occur post malware execution where the DNS queries to a C2 server. These queries tend to be longer than default DNS queries and contain commands instead of subdomain addresses.

|Wireshark filter|Description|
|dns|global search|
|dns contains "dnscat"| used to search for anomalous and non regular names in DNS addresses or subdomain addresses|
|dns.qry.name.len > 15 and !mdns|Used to search for DNS queries longer than default length|
!mdns disables local link device queries

### Exercises
**Which protocol is sued in ICMP tunnelling**
Using the aforementiond filter managd to narrow down to the anomalous packets however finding out what protocol they were using required me to follow Chris Greers youtube tutorial which taught reading packet payloads, and within packet 42 there is "enSSH" suggesting the attacker is using ICMP to exfil data, further along more ICMP packets contain the diffie hellman exchange to suggesting established connection.
![ssh](/static/images/ssh.png)

**What is the suspicious main domain address that receives anomalous DNS queries**
By adding the aforementioned display filter and then adding names to the column it only takes a quic search across the packets to come across a long truncated name that also contains "dataexfil" making it the suspicious domain address
![dataexfil](/static/images/dataexfil.png)


## FTP
|wireshark filter|Description|
|----------------|-----------|
|ftp|global search|
|ftp.response.code == 211|system status|
|ftp.response.code == 212|Directory status|
|ftp.response.code == 213|File status|
|ftp.response.code == 220|Service ready|
|ftp.response.code == 227|Entering passive mode|
|ftp.response.code == 228|Long passive mode|
|ftp.response.code == 230|User login|
|ftp.response.code == 231|User logout|
|ftp.response.code == 331|Valid username|
|ftp.response.code == 430|Invalid username or pass|
|ftp.response.code == 530|No login, invalid password|
|ftp.request.command == USER|username|
|ftp.request.command == "PASS"|Password|
|ftp.request.arg == "password"|Password|
|ftp.response.code == 530|Bruteforce search|
|ftp.response.code == 530 and gtp.response.arg contains "username"|Bruteforce signal|
|ftp.request.command == "PASS" and ftp.request.arg == "password"|password spray signal"

### Exercises
**how many incorrect login attempts are there**
this simply requires looking at the response code 530 which is the response to incorrec login attempts which returns 737 packets
![530](/static/images/530.png)

**What is the size of the file accessed by the "ftp"account**
Using the response code 213 and looking at the arg gives us the size of the file accessed which is 39424
![213](/static/images/213.png)

**the adversary uploaded a document to the ftp server what is the filename**
simply filtering for ftp and looking through the info section finds the name resume.doc pretty quickly.
![ftp](/static/images/ftp.png)

**the adversary tried to assign special flags to change the executing permissions what are they**
Executing permissions involves the chmod command and if you know you're looking for this it makes it easy to find and the perms have been set using CHMOD 777
![chmod](/static/images/chmod.png)

## HTTP
As a result of being the backbone of web traffic and unencrypted it's a must to know in network traffic analysis and is often used in the following attacks:
- Phishing pages (T1566)
- Web attacks (T1190)
- Data exfil (TA0010)
- C2 (TA0011)

|wireshark filter|Description|
|----------------|-----------|
|http and http2|Global search for either http or http2|
|http.reqeuest.method == "GET"/"POST"|search for either http get or post requests
|http.response.code == 200/301/302/etc.|Search for the http response codes|
|http.user_agent contains "nmap|Searches for the browser and operating system id to a web server app|
|http.request.uri contains "admin"|Points the requested resource from the server|
|http.request.uri contains "admin"|complete URI information|
|http.server contains "apache"|Server service name|
|http.host contains "keyword"|searches for the hostname of the server|
|http.host == "keyword"|Searched for the hostname|
|http.connection == "Keep-Alive"|Connection status|
|data-text-lines contains "keyword"|Searches cleartext data provided by the server|

The user-agent field specifically is great place for spotting anomalies in traffic so certain things may stand out in this field:
- Different user agent info from the same host in a short time notice
- Non-standard and custom user agent info
- Masquerading names such as Mozlilla for Mozilla
- Audit tools such as nmap,nikto,wfuzz and sqlmap in the user agent field: Bookmarked display filter for this (http.user_agent contains "sqlmap") or (http.user_agent contains "Nmap") or (http.user_agent contains "Wfuzz") or (http.user_agent contains "Nikto")
- Payload data in the user agent field

Investigations start with prior research on threats and anomalies that are going to be hunted one of the exercises requires investigating the log4j vulnerability, this attack starts with a POST requests and contains cleartext patterns "jndi:ldap" and Exploit.class".

|Wireshark filter|Description|
|----------------|-----------|
|http.request.method == "POST"|Will search for the attack start in log4j|
|(ip contains "jndi") or ( ip contains "Exploit") or (frame contains "jndi") or ( frame contains "Exploit") or (http.user_agent contains "$") or (http.user_agent contains "==")|Searches for the known cleartext patterns|

### Exercises
**Investiagte the user agents. What is the number of anomalous user-agent types**
By adding user agents into the column field this makes it very easy to tally up the how many user agent types there are of which there are 6.
![useragent](/static/images/useragent.png)

**what is the packet number with a subtle spelling difference in the user agent field**
since the user-agent was added to the column this makes it easy to see which has the subtle spelling difference as it stands out when compared to the legitimate user agent it is trying to imitate. Mozlila vs Mozilla
![mozilla](/static/images/mozilla.png)

**locate the Log4j attack starting phase what is the packet number?**
using the http.request.method == "POST" alongside having user-agent in the column filter and loking for the jndi:ldap user agent allowed me to find this packet pretty quickly and it is number 444
![log4j](/static/images/log4j.png)

**Locate the starting attack and decode the base64 command, what is the ip address contacted by the adversary**
Looking inside the starting point POST command we can see the base64 code
![useragentbase64](/static/images/useragentbase64.png)
Adding this into cyberchef we can decode it and get the ip address for the answer which is 62[.]210[.]130[.]250
![cyberchef](/static/images/cyberchef.png)

## HTTPS
The encrypted version of HTTP so requires the encryption/decryption key pairs in the form of an encryption log file to read.

|Wireshark filter|description|
|----------------|-----------|
|http.request|lists all requests|
|tls|global tls search|
|tls.handshake.type == 1|TLS client request|
|tls.handshake.type == 2|TLS Server response|
|ssdp|Local simple service disvoery protocol|

HTTPS also has it's own version of the tcp-three way handshake, the first two steps are in order "Client hello", "Server hello".

- Client Hello: (http.request or tls.handshake.type == 1) and !(ssdp) 
- Server Hello: (http.request or tls.handshake.type == 2) and !(ssdp)
### Exercise
**What is the frame number of the client hello message sent to accounts.google.com**
This one was done by using the tls.handshake.type == 1 and adding the server name field found within the first packet to the display filter field and adjusting the name to search for the account I am after.
![servername](/static/images/servername.png)

**Decrypt the traffic with the Keylogsfile.txt file. what is the number of HTTP2 packets**
adding the file to the master pre-shared option within the tls prefrences decrypts the traffic and simply applying the http2 display filter will return the amount of packets
![tls](/static/images/tls.png)

**go to frame 322. what is the authority header of the HTTP2 packet**
this is found within the 322 packet
![http2](/static/images/http2.png)

**Investigate the decrypted packets and find the flag**
By using export to objects and exporting to http we get the flag FLAG{THM-PACKETMASTER}
![packetmaster](/static/images/packetmaster.png)

## Conclusion
In conclusion this room covered how to detect anomalies and investigate events of interest at the packet level across various protocols.

---

- **Wireshark - Traffic analysis** — required. The display title.
- **TryHackme** — optional. Shows as a badge (e.g. TryHackMe, LetsDefend).
- **Medium** — optional. One of: easy, medium, hard. Shows as a coloured tag.
- **2026-07-17** — optional but recommended. Format YYYY-MM-DD. Used for sorting.
- **Wireshark, Network analysis** — optional. Comma-separated list in square brackets.
- **Using wireshark to detect anomalies and investigate events of interest** — optional. One-sentence description shown on cards.

For **certs**, use `status: passed` / `studying` / `planned` and `org: CompTIA` instead of platform/difficulty.
