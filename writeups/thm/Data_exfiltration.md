---
title: Data Exfiltration
platform: TryHackMe
difficulty: Medium
date: 2026-07-20
tags: [Network security]
summary: A write up to identifying and defending against data exfiltration
---

# Data exfiltration
Data exfiltration (TA0010) is one of the primary tactics for an attacker once they have breached a network. there are some common phases to data exfiltration:

- Discover/collection: Here the attacker locates sensitive files
- Staging/ compression: here the attack aggregates, compresses, encrypts or encodes files
- Exfiltration transports: Here the attacker transfers the files over network, removable media, cloud or covert channels
- C2 coordination: Here the attacker orchestrates transfer and confirms receipt

|techniques|Example|Indicators of attack|
|----------|-------|--------------------|
|Net-based|HTTP/S uploads to S3/Azure Blob/webmail, FTP/SFTP/SCP, DNS tunnelling, ICMP/covert protocols, custom TCP/UDP|Proxy/web gatewaylogs (large POSTs, uploads to cloud endpoints), firewall/NGFW flows (high bytes to a single IP/ASN) netflow (spikes/outbound flows), DNS logs (long hostnames, TXT queries|
|Host-based|Powershell/invoke-webrequest, rclone, awscli, curl/wget, archive creation, use of removable USBs, ADS/hiddens streams|Sysmon/EDR (Process create, network connect, file create events), Windows security (4663/4656 object access), auditd/shell history on Linux, and removable-media events.|
|cloud exfil|S3 PutObject / multipart upload, Azure Blob Uploads, goolge cloud storage objects, Drive/Sharepoint external sharing|CloudTrail / AzureActivity / GCP Audit, Cloud storage access logs, unusual service-account or IP activity|
|Convert & encoding|DNS tunnelling, base64 or chunked encoding, steganography into images/aduio, splitting files into many small requests|DNS logs, proxy logs with many small POSTs, correlation of intermittent uploads + suspicious process activity|
|Insider & collab tools|Slack/teams/dropbox/google drive uploads or sharing to external users. compromised accounts|Audit logs (share events, file downloads), and mail logs|
|General IoAs & triage signals|Large outbound volume to external IP's/domains, unknownk destination domains, suspicious processes/command lines, many file read events ollowed by an outbound connection. and multipart/streamed uploads|Correlate: Proxy/firewall/netflow, DNS, Sysmon/EDR (eventID 1/3/11), mail server logs|

Effective detection doesn't rely on single points of data but correlation across across host, network and cloud telemetry to understand who accesses what data, what was transferred, how it was staged and where it was sent.

## Detection: DNS tunnelling

Indicators of attack:
- Many DNS queries sent to a single domain, espeially when the count is high compared to baseline
- Long subdomain labels or full query names (> 60-100)
- High entropy or base32/64 like patterns in the query name
- Rare record types (TXT,NULL) or many large TXT responses
- Unusual response behaviour, frequent NXDOMAIN or large TCP/UDP fragments for DNS
- Queries at regular intervals (beaconing)

**What is the suspicious domain receiving the DNS traffic**
Using SPLUNK to look at the logs just by looking at the query field one domain stands out from the rest as being very suspicious as the other domains in these field are familiar domains. this however does not automatically make it malicious and warrants further investigation.
![query](/static/images/query.png)

**How many suspicious traffic/logs related to dns tunneling were observed**
This simply required filtering the source by dns and filtering for alerts that are equal to suspicious.
![315](/static/images/315.png)

**which local IP sent the maximium number of suspicious requests**
This requires looking at the source ip with the previous exerises filters still applied
![src](/static/images/src.png)

## Detection: exfil through FTP

Indicators of attack:
- USER and PASS commands
- STOR (upload) and RETR (download) commands: repeated or large transfers
- Large data connections to unusual external IPs, especially outside business hours
- Data channel openings on ephemeral ports paried with large payloads

**What is the name of the customer related file exfiltrated from the root account**
Using the display filter ftp.request.arg == "root" shows us all communications from this account from here it was easy to locate the name of the file customer_data.xlsx
![customerdata](/static/images/customerdata.png)

**which internal IP was found to sending the largest payload to an external IP**
By going into conversations and then into the IPv4 tab and sorting by bytes it showed that the internal ip sending the largest bytes outwards was 192.168.1.105
![wiresharkftp](/static/images/wiresharkftp.png)

**What is the hidden flag hidden inside the ftp stream transferring the CSV file to the suspicious IP**
By right clicking on the two ip's in the conversations tab used in the previous exercise I added bytes A -> B as a display filter which brought up the conversation between the two and showed the file that was exfiltrated and the hidden flag
![flag](/static/images/flag.png)

## Detection: exfil via HTTP

Indicators of attack:
- Unusually large HTTP POST requests to external/unexpected hosts.
- HTTP requests to domains with low rep / rarely seen in baseline traffic
- Frequent small reqeusts (beaconing) to the same host, followed by large uploads
- Chunked or multipart transfers where multiple requests compose a larger file

**Which internal compromised host was used to exfiltrate sensitive data**
Using wireshark and adding hosts as a column I was able to manually search and filter out common and known domains until one popped up that stood out from the rest, looking into the conversations one ip address sent a large POST request >600 bytes of data to this domain making this the compromised host - 192.168.1.103
![httpexfil](/static/images/httpexfil.png)

**What is the flag hidden in the exfiltrated data** 
from the conversation tab adding this conversation to the display filter and inspecting the packet shows the flag hidden within.
![httpflag](/static/images/httpflag.png)

## Detection: Data exfil via ICMP

Indicators of attack:
- ICMP packet volumes, a single host sending many ICMP echo requests to an external host
- Large frame.len or icmp.payload, pings with payloads much larger than typical >64
- ICMP type/code unusual values
- Regular timing, evenly spaced ICMP packets carrying similar sized packets
- Fragments with reassembly: multiple ICMP fragments with same src/dst pair.

**What is the flag found in the exfiltrated data through ICMP**
This one is easy it simply required sorting the data by length and looking at anything over normal ICMP packet length and inspecting the larger packets where the flag can be found.
![icmpflag](/static/images/icmpflag.png)

## Conclusion
In conclusion this write up covers the fundamentals behind what data exilftration is and why it's a critical threat, the attacker frameworks and methods they use to exfiltrate methods and the common attack techniques/indicators of attack and how to discover and detect data exfiltration on the network.

---

- **Data Exfiltration**
- **TryHackMe**
- **Medium**
- **2026-07-20**
- **Network Security**
- **A write up of the fundamentals, techniques and detection methods of data exfiltration**
