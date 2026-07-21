---
title: Snort - Network Security
platform: TryHackMe
difficulty: Medium
date: 2026-07-21
tags: [Snort, Tools, Network security]
summary: A write up and overview of the network intrusion and prevention system Snort.
---
# Snort - Network Security

Snort is an open-source, rule-based Network Intrusion Detection and Prevention System (NIDS/NIPS). Snort works by using a series of rules that help define malicious network activity, then uses those rules to find packets that match against them and generate alerts for users.

| Snort commands | Description            |
| -------------- | ---------------------- |
| snort -V       | Shows instance version |
| snort -T       | Tests config           |
| snort -c       | Identifies config file |
| snort -q       | Quiet mode             |

## Sniffer mode

| Sniffer mode parameters | Description                                     |
| ----------------------- | ----------------------------------------------- |
| -v                      | Verbose, displays the TCP/IP output             |
| -d                      | Display the packet data                         |
| -e                      | Display the link-layer headers                  |
| -X                      | Display the full packet details in HEX          |
| -i                      | Defines the specific network interface to sniff |

Example: `sudo snort -v -i eth0`

## Packet Logger mode

| Packet logger parameter | Description                                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| -l                      | Logger mode; target log and alert output directory. Default output folder is /var/log/snort  |
| -K ASCII                | Log packets in ASCII format                                                                   |
| -r                      | Reading option: review the logged events in Snort                                            |
| -n                      | Specify the number of packets to be processed or read                                        |

### Exercises

**What is the source port used to connect to port 53?**

After running Snort in logger mode and generating the log to the current working directory, I used `cd` to move into the log folder and `ls` to list its contents. The source port connected to port 53 was 3009.

![snortlog](https://lewisjava.pythonanywhere.com/static/images/snortlog.png)

**Read "snort.log.1640048004" with Snort. What is the IP ID of the 10th packet?**

Using `snort -r snort.log.1640048004 -n 10` prints the first 10 packets, making it easy to find the 10th.

![pid](https://lewisjava.pythonanywhere.com/static/images/pid.png)

**Read "snort.log.1640048004" with Snort. What is the referrer of the 4th packet?**

Using the same command as before but adding the `-X` parameter gives the full packet details, including the Referer header, which lets me read the referrer for the 4th packet.

![referer](https://lewisjava.pythonanywhere.com/static/images/referer.png)

**Read the same file with Snort. What is the ACK number of the 8th packet?**

Same command and output as before, this time reading off the ACK number, which is 0x38AFFFF3.

![ack](https://lewisjava.pythonanywhere.com/static/images/ack.png)

**Read the same file with Snort. What is the number of TCP port 80 packets?**

This one requires a Berkeley Packet Filter (BPF) to return only the TCP traffic on port 80.

![berkely](https://lewisjava.pythonanywhere.com/static/images/berkely.png)

## IDS/IPS

| IDS/IPS parameter | Description                     |
| ----------------- | ------------------------------- |
| -c                | Defines the configuration file  |
| -T                | Tests the configuration file    |
| -N                | Disable logging                 |
| -D                | Background mode                 |
| -A                | Alert modes: full, console, cmg |

IPS mode drops packets and is activated with the `-Q --daq afpacket` parameters. Snort IPS requires at least two interfaces to work:

```
snort -c /etc/snort/snort.conf -q -Q --daq afpacket -i eth0:eth1 -A console
```

### Exercises

**What is the number of detected HTTP GET methods?**

I ran `sudo snort -c /etc/snort/snort.conf -A full -l .` and then started the traffic-generator script. This command inspects the traffic, compares it against the ruleset in the config, and writes the log to the current working directory.

![get](https://lewisjava.pythonanywhere.com/static/images/get.png)

## PCAP investigation

The benefit of using Snort with PCAP files is the ability to compare the capture against the ruleset.

| PCAP parameter      | Description                                          |
| ------------------- | ---------------------------------------------------- |
| -r / --pcap-single= | Read a single PCAP                                   |
| --pcap-list=""      | Read PCAPs provided in the command (space separated) |
| --pcap-show         | Show the PCAP name on the console during processing  |

Example:

```
sudo snort -c /etc/snort/snort.conf -q -r icmp-test.pcap -A console -n 10
```

This compares the PCAP against the config file, prints to the console, and processes only the first 10 packets.

```
sudo snort -c /etc/snort/snort.conf -q --pcap-list="icmp-test.pcap http2.pcap" -A console -n 10 --pcap-show
```

This tests multiple PCAPs the same way, using `--pcap-show` to identify which PCAP is generating which output.

### Exercises

**What is the number of generated alerts with mx-1.pcap?**

I first ran the PCAP through Snort with `sudo snort -c /etc/snort/snort.conf -A full -l . -r mx-1.pcap`, which generated a report showing 170 alerts.

![snortalert](https://lewisjava.pythonanywhere.com/static/images/snortalert.png)

**How many TCP segments are queued?**

This value comes from the Stream (stream5) preprocessor statistics in Snort's shutdown summary, produced directly from comparing the PCAP against the config file — no need to read the log file separately.

![tcpsegments](https://lewisjava.pythonanywhere.com/static/images/tcpsegments.png)

**How many HTTP response headers are extracted?**

This is found in the HTTP Inspect statistics after the PCAP is read. The number is 3.

![httpresponse](https://lewisjava.pythonanywhere.com/static/images/httpresponse.png)

**Run the file against the second configuration file. What is the number of alerts?**

Running the file against the second config with `sudo snort -c /etc/snort/snortv2.conf -A full -l . -r mx-1.pcap` returns 68 alerts.

![snortv2](https://lewisjava.pythonanywhere.com/static/images/snortv2.png)

**Investigate mx-2.pcap. What is the number of generated alerts?**

Running the previously used commands against the second PCAP returns 340 alerts.

![pcap2](https://lewisjava.pythonanywhere.com/static/images/pcap2.png)

**What is the number of detected TCP packets?**

In the Stream preprocessor statistics section, the tracked TCP session count shows that 82 TCP packets were detected.

![tracked](https://lewisjava.pythonanywhere.com/static/images/tracked.png)

**Investigate both mx-2.pcap and mx-3.pcap. What is the total number of generated alerts?**

This requires adding `--pcap-list` to the command to scan both PCAPs at once and aggregate the data from the two sources. Doing this shows 1020 alerts between the two.

![pcaplist](https://lewisjava.pythonanywhere.com/static/images/pcaplist.png)

## Snort rule structure

Understanding Snort rule structure is essential for blue/purple teamers designing new rules. The header format is as follows:

1. **Action** — alert, drop, reject
2. **Protocol** — TCP, UDP, ICMP, IP
3. **Source IP** — e.g. any
4. **Source port** — e.g. any
5. **Direction** — `<>` or `->`
6. **Destination IP** — e.g. any
7. **Destination port** — e.g. any
8. **Options** — msg, reference, sid, rev, etc.

Example rule that generates an alert for each ICMP packet processed by Snort:

```
alert icmp any any <> any any (msg:"ICMP Packet found"; reference:CVE-XXXX; sid:1000001; rev:1;)
```

- **sid** = rule ID. sid < 100 is reserved for future use; sid 100–999,999 is used by rules distributed with Snort/the community ruleset; sid ≥ 1,000,000 is used for rules created by the user.
- **rev** = revision information. This option lets analysts track the revision of each rule.
- **`<>`** = bidirectional flow.
- **`->`** = source-to-destination flow.
- **msg** = the message that appears with an alert. It should be appropriate to the rule.

### Content rule / payload options

Payload options match specific payload data by ASCII, HEX, or both. Example:

```
alert tcp any any <> any 80 (msg:"GET request found"; content:"GET"; sid:1000001; rev:1;)
```

This rule creates an alert for each HTTP packet containing the keyword `GET`. It is case sensitive — adding `nocase` to the options fixes this. Adding `fast_pattern` prioritises the content search to speed up the payload search operation.

### Non-payload options

- **id** — filters the IP ID field:
  `alert tcp any any <> any any (msg:"ID TEST"; id:123456; sid:1000001; rev:1;)`
- **flags** — filters for TCP flags:
  `alert tcp any any <> any any (msg:"FLAG TEST"; flags:S; sid:1000001; rev:1;)`
- **dsize** — filters the packet by payload size: `dsize:min<>max;`, `dsize:>100`, `dsize:<100`.
- **sameip** — filters for matching source and destination IP addresses (duplication). Add `sameip` to the options.

Rule editing is done by editing the local.rules file: `sudo gedit /etc/snort/rules/local.rules`

### Exercises

**Write a rule to filter IP ID "35369" and run it against task9.pcap. What is the request name of the detected packet?**

After creating the rule and using `cat` to read the alert, I can see the request was a Timestamp request.

![snortrule](https://lewisjava.pythonanywhere.com/static/images/snortrule.png)

**Create a rule to filter packets with the SYN flag and run it against the PCAP file. What is the number of detected packets?**

After writing the appropriate rule and running it against the PCAP file, I ran `grep` for the msg option I wrote and piped it through `wc -l` to count how many times it appeared, which was 1.

![synalert](https://lewisjava.pythonanywhere.com/static/images/synalert.png)

**Write a rule to filter packets with the PSH-ACK flags and run it against the same PCAP file. What is the number of detected packets?**

After writing the appropriate rule and running it against the PCAP file, I ran `grep` against the msg option I wrote and piped it through `wc -l` to count how many times it appeared, which was 216.

![flagalert](https://lewisjava.pythonanywhere.com/static/images/flagalert.png)

**Create a rule to filter UDP packets with the same source and destination IP and run it against the same PCAP file. What is the number of packets?**

Same procedure as the last two, but with a rule using the `sameip` option on UDP traffic.

![udpalert](https://lewisjava.pythonanywhere.com/static/images/udpalert.png)

## Conclusion

Snort is an incredibly versatile tool, capable of operating as a sniffer, packet logger, and IDS/IPS. In this write-up I demonstrated the fundamentals of the tool, as well as writing local rules and running them against PCAP files to gather data from the outputs.
---

- **Snort**
- **TryHackMe**
- **Medium**
- **2026-07-21**
- **Medium**
- **A write up of snort, what it is and does and the creation and use of rules**
