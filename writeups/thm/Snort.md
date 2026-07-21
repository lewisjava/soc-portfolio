---
title: Snort - Network Security
platform: TryHackMe
difficulty: Medium
date: 2026-07-21
tags: [Snort, Tools, Network security]
summary: A write up and overview of the network intrusion and prevention system Snort.
---

# Snort
Snort is an open source, rule-based Network intrusion detection and prevention system (NIDS/NIPS), snort works by useing a series of rules that helpp define malicious network activity and uses those rules to find packets that match against them and generate alerts for users.

|Snort commands|Description|
|--------------|-----------|
|snort -V|Shows instance version|
|snort -T|Tests config|
|snort -c|indentifies config file|
|snort -q|Quiet mode|

## Sniffer mode

|Sniffer mode parameters|Description|
|-v|Verbose, Displays the TCP/IP output|
|-d|Display the packet data|
|-e|Display the linklayer headers|
|-X|Display the full packet details in HEX|
|-i|Defines the specific network interface to listen/sniff|

example: sudo snort -v -i eth0

## Packet Logger mode

|Packet logger parameter|Description|
|-----------------------|-----------|
|-l|Logger mode, target log and alert output directory, default output folder is /var/log/snort|
|-K ASCII|Log pacets in ASII format|
|-r|Reading option:Review the logged events in snort|
|-n|Specifiy the number of packets to be processed or read|

### Exercises

**What is the source port used to connect to port 53**
After running snort in log mode and generating the log to the current working directory, using cd to get into the log folder and using ls I could see that the source port connected to 53 was 3009
![snortlog](/static/images/snortlog.png)

**Read the snort.log.1640048004" with snort, what is the IP ID of the 10th packet**
Uinsg the following snort -r snort.log.1640048004 -n 10 prints the first 10 packets making finding the 10th one very easy
![pid](/static/images/pid.png)

**Read the snort.log.1640048004" with snort, what is the referer of the 4th packet**
Using the same input as before but adding the parameter -X to give full packet details provides me with the refere of the packets where I can find the refer for the 4th packet
![referer](/static/images/referer.png)

**Read the same file with snort what is the ack number of the 8th packet**
Same input and output as before but looking for the ACK number which is 0x38AFFFF3
![ack](/static/images/ack.png)

**Read the same file with snort, what is the number of the TCP port 80 packets**
The answer for this one requires the use of Berkely packet filters to provide only tcp response 
![berkely](/static/images/berkely.png)

## IDS/IPS

|IDS/IPS parameter|Description|
|-----------------|-----------|
|-c|Defining the configuration file.|
|-T|Testing the configuration file|
|-N|Disable logging.|
|-D|Background mode|
|-A|Alert modes: Full, Console, cmg|

IPS mode and dropping packets: IPS mode is activated with the -Q --daq afpacket parameters
Snort IPS requires at least two interfaces to work:
snort -c /etc/snort/snort.conf -q -Q --daq afpacket -i eth0:eth1 -A console

### Exercises
**What is the number of detected HTTP GET methods**
after running the command sudo snort -c /etc/snort/snort.conf -A full -l . and then ran the traffic-generator scrip, this command will look at the traffic and compare it to the rule list in the config and then print the log to the current working directory. 
![get](/static/images/get.png)

## PCAP investigation
The benefit of using snort with pcap files is the ability to compare the pcap file against the ruleset.

|pcap parameter|Decription|
|--------------|----------|
|-r/ --pcap-single=|Read a single pcap|
|--pcap-list=""|Read pcaps provided in command (space seperated)|
|--pcap-show|Show pcap name on console during processing|

example: sudo snort -c /etc/snort/snort.conf -q -r icmp-test.pcap -A console -n 10
this compares the pcap against the config file, prints to the console and only the first 10 packets will be printed.

sudo snort -c /etc/snort/snort.conf -q --pcap-list="icmp-test.pcap http2.pcap" -A console -n 10 --pcap-show
Tests multiple pcaps the same way, uses pcap show to be able to know which pcap is generating which reports

### Exercises
**What is the number of generated alerts with mx-1.pcap**
First ran this pcap through snort using sudo snort -c /etc/snort/snort.conf -A full -l . -r mx-1.pcap which generated a report, this log was then ran through snort to read the report which showed 170 alerts.
![snortalert](/static/images/snortalert.png)

**How many TCP segments are Qued**
This data is provided without needing to read the log file and is provided straight from compaing the pcap file to the config file.
![tcpsegments](/static/images/tcpsegments.png)

**How many HTTP response headers are extracted**
This is found under the HTTP inspect stream after the pcap file is read and the number is 3
![httpresponse](/static/images/httpresponse.png)

**run the file against the second configuration file, what is the number of alerts**
Running the file against the second config file using the command sudo snort -c /etc/snort/snortv2.conf -A full -l . -r mx-1.pcap returns 68 alerts
![snortv2](/static/images/snortv2.png)

**Investigate mx-2.pcap what is the number of the generated alerts**
running the previous used commands against the second pcap returns 340 alerts
![pcap2](/static/images/pcap2.png)

**What is the number of detected TCP packets**
Heading to the stream statistics section and reading the tracked number provides 82 showing 82 tcp packets were detected.
![tracked](/static/images/tracked.png)

**investigate both mx-2 and mx-3.pcap what is the total generated alerts**
This requires adding --pcap-list to the command to scan both pcaps at the same time and aggregate the data of the two sources. Doing this shows there is 1020 alerts between the two.
![pcaplist](/static/images/pcaplist.png)

## Snort rule structure
Snort rule structure is essential to blue/purple teamers for designing new snort rules. the format is as follows

1. Action: alert, drop, reject
2. protocol: TCP, UDP, ICMP
3. Source ip: ANY
4. Source port: ANY
5. Direction: <>
6. Destination ip: ANY
7. Destination ip: ANY
8. Options: msg, reference, sid, rev

- Example rule that will generate an alert for each ICMP packet processed by snort:
- alert icmp any any <> any any (msg:"ICMP Packet found"; reference:CVE-XXXX;sid:1000001: rev:1;)
- sid = rule ID (<100 =  reserved rules, 100-999,999 = rules came with the build, >1,000,000 = rules created by user
- rev = revision information, this option allows analysts to access revision information for each rule.
- <> = Bi directional flow
- -> = source to destination flow
- msg = the message that will appear with an alert, should be appropriate to the rule

### content rule/payload options

payload data it matches specific payload data by ASCII, HEX or both. example:
- ASCII mode - alert tcp any any <> any 80 (msg: "GET request found"; content:"GET";sid: 100001;rev:1;) this rule creates an alert for each HTTP packet containing the keywor GET, this rule is case sensitive adding "Nocase" to the options header fixes this, adding "Fast_pattern" to the options headerwould prioritise content search to speed up the payload search operation.

### Non-payload options

a- ID: allows for filtering the IP ID field: alert tcp any any <> any any (msg: "ID TEST";id:123456; sid: 100001;rev:1;)
- flags: filtering for tcp flags in the options header: alert tcp any any <> any any (msg:"FLAG TEST";flags:S; sid:100001;rev:1;)
- Dsize: filtering the packet by payload size: dsize:min<>max;, dize:>100, dsize<100. done in the options header
- Sameip Filtering the source and destination IP addresses for duplication, add "sameip" to options header

rule editing is done by editing the loal.rules rile: sudo gedit /etc/snort/rules/local.rules

### Exercises
**Write a rule to filter IP ID "35369" and run it against task9.pcap, what is the request name of the detected packet**
After creating the rule and using cat to read the alert I can see the reuqest was a timestamp request
![snortrule](/static/images/snortrule.png)

**Create a rule to filter packets with Syn flag and run it against the pcap file, what is the number of detected packets**

![synalert](/static/image/synalert.png)
After writing the appropriate rule and running it against the pcap file I ran the grep command for the msg option I wrote and piped it through cd -l to get the amount of times it appeared which was 1.

**Write a rule to filter packets with Push-Ack flags and run it against the same pcap file. what is th number of detected packers**
After writing the appropriate rule and running it against the pcap file I then ran grep against the msg option i wrote and piped it through wc -l to get the amount of times it appeared which was 216
![flagalert](/static/images/flagalert.png)

**Create a rule to filter UDP packets with the same source and destination IP and run it against the same pcap file, what is the number of packets**
Same procedure as the last two but with a different rule
![udpalert](/static/images/udpaler.png)

## Conclusion
In conclusion Snort is an incredibly versatile tool capable of operating as a sniffer, IPS/IDS and more. In this writeup I demonstrate the basic fundamentals of the tool as well as the capability of writing local.rules and using them against pcap files and reading the outputs to gather data.


---

- **Snort**
- **TryHackMe**
- **Medium**
- **2026-07-21**
- **Medium**
- **A write up of snort, what it is and does and the creation and use of rules**
