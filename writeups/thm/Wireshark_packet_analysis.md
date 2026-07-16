---
title: Wireshark - Packet Analysis
platform: TryHackMe
difficulty: easy
date: 2026-07-16
tags: [Network Analysis, Tools, Wireshark]
summary: A walkthrough of using Wireshark for packet analysis
---

# Wireshark
Wireshark is an open network protcol analyzer that allows its users to capture and interactively browse the traffic running on a computer network making it the ideal tool for packet capture analysis.

## Statistics
The statistics tab provides multiple statistics options that allows users see the scope of the traffic, available protocols, endpoints and conversations as well as some protocol specific details like DHCP, DNS and HTTP/2

### Resolved addresses
Within the statistics tab is an option for resolved addresses that helps analyse IP addresses and DNS names by providing the list of the resolved addresses and their hostnames. This means identifying accesses resources can be done by using this menu shown below.
![Resolved addresses](/static/images/resolvedaddresses.png)

### Protocol Hierachy
Another option under the statistics tab is Protcol Hierarchy which breaks down all available protocols from the capture file and formats them into a tree based on packet counters and percentages. This allows for easy viewing of the usage of the ports and services which makes it easy to see events of interest.
![protocol hierarchy](/static/images/protocolhierarchy.png)

### Conversations
The conversations option under statistics represents traffic between two specific endpoints and provides the list of conversations in five forms: Ethernet, IPV4/6, TCP and UDP.
![conversations](/static/images/conversations.png)

### EndPoints
The endpoints option is quite similar to conversations with the only difference being that it provides unique information for a single information field. This allows for identification for unique endpoints in the capture file.
![endpoints](/static/images/endpoints.png)

### IPv4 and IPv6
The statistics menu contains two stastistics options for IPv4 and IPv6 that allows narrowing the stastics on packets containing a specific IP version. 

IPv4:
![IPv4](/static/images/ipv4.png)

IPv6:
![IPv6](/static/images/ipv6.png)

### DNS
The DNS option breaks down all DNS packets from the capture file and formats it into a tree view based on packet counters and percentages of the DNS protocol.
![DNS](/static/images/dnswireshark.png)

### HTTP
The HTTP is very simialr to the DNS option in that it breaks the findings down into a tree view based on packet counters and percentages of the HTTP protocol.
![http](/static/images/httppacketcount.png)

## Packet Filtering
### Principles
There are two types of filters in Wireshark;

- Capture filters: used to save only a specific part of the traffic. is set before capturing traffic and not changeable during the capture
- Display filters: Used to investigate packets by reducing the number of visible packets in wireshark and is changeable during the capture.

Capture filter syntax:
- Scope: Host, net, port and portrange
- Direction: src, dst, src or dst, src and dst.
- Protocol: ether, wlan, ip, ip6, arp, rarp, tcp and udp.
- Example filter to capture port 80 traffic: tcp port 80.

Display filter syntax:
Display filters use c-like logical operators and comparison operators

|English|c-like|description|
|-------|------|-----------|
|and|&&|logical AND|
|not|!|logical NOT|
|or|\|\|| Logical OR|
|eq|==|Equal|
|ne|!=| Not Equal|
|gt|>|Greater than|
|lt|<|Less than|
|ge|>=|Greater than or equal too|
|le|<=|Less than or equal too|

Wireshark also comes with a display filters refrence table under the analyse tab
![display filters](/static/images/displayfilters.png)

These are used in the packet filter toolbar that has a few features:
- Packet filters are defined in lowercase
- Packet filters have an autocomplete feature
- Packet filters have a three-colour representation: green for valid, red for invalid and yelow for the filter will work but is unreliable.

## Protocol filters
### IP filters
These filters help analyse the traffic according to the IP level information (network layer of the OSI model). It filters information like IP addresses, version, TTL, type of srvice, flags and checksum values.

|Filter|Description|
|------|-----------|
|ip|Show all ip packets|
|ip.addr == 0.0.0.0|Show all packets containing IP addresses 0.0.0.0|
|ip.addr == 10.10.10.0/24|Shows all packets tontaining ip addresses from 10.10.10.0/24 subnet|
|ip.src == 0.0.0.0|Shows all packets from 0.0.0.0|
|ip.dst == 0.0.0.0|Shows all packets to 0.0.0.0|

### TCP and UDP filters
filters packets according to protcol level information (transport layer of the OSI model). Shows information such as source and destination ports, sequence number, acknowledgment number, windows size, timestamps, flags, length and protocol errors.

|Filter|Description|
|------|-----------|
|tcp.port == 80|Show all packets with port 80|
|tcp.srcport == 1234|Show all TCP packets originating from port 1234|
|tcp.dstport == 1234|Show all TCP packets sent to port 1234|

### HTTP and DNS (application level protocol filters)
Application level protocol filters analyse application level information from packets (application layer of the osi model). This includes application specific information like payload and linked data depending on the protocol type.

|Filter|Description|
|------|-----------|
|http|show all HTTP packets|
|http.response.code == 200|Show all packets with HTTP response code 200|
|http.request.method == "GET"|Show all HTTP GET requests|
|http.request.method == "POST"|Show all HTTP POST requests|
|dns|Show all DNS packets|
|dns.flags.response == 0| show all DNS requests|
|dns.flags.response == 1| Show all DNS responses|
|dns.qry.type == 1| Show all DNS "A" records|

Wire shark also comes with a built in option that stores all supported protocol structures and provides and easy-to-use expressions menu under the analyse tab -> Display filter expression.

## Advanced filtering

|Filter|Description|Example|
|------|-----------|-------|
|Contains|Search a value inside packets. simialr to the Find option by focusing on a specific field|http.server contains "Apache"|
|matches|Search a pattern of a regular expression|http.host matches "\.(php\|html)" lists all HTTP pacets where packets "host" fields match keywords .php or .html|
|in|Search a value or field inside of a specific scope/range|tcp.port in {80 443 8080}. list al TCP packets where packets "port" fields have values 80, 443 or 8080|
|upper|Convert a string value to uppercase|upper(http.server)contains "APACHE". Converts all HTTP packets "server" fields to uppcase and lists packets that contains the APACHE keyword|
|lower|Convert a string value to a lowercase|lower(http.server) contains "apache". Converts all HTTP packets "server" fields info to lowercase and list packets that contains "apache".|
|string|Converts a non string value to a string| string(frame.number) matches "[13579]$". convert all "frame number" field to string values and list frames end with odd values.|

Since there is many filter options and combinations wireshark comes with a bookmark feature on the display filter bar that allows for saving of user-created bookmarks to re-use common/complex filters with ease everytime with each new pcap file.


---

- **Wireshark - Packet analysis**
- **TryHackme**
- **Easy**
- **2026-07-16**
- **Network Analysis, wireshark, tools**
- **A walkthrough of using wiresahrk for packet analysis**
