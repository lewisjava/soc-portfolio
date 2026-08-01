---
title: IP and Domain threat intel
platform: TryHackMe
difficulty: Medium
date: 2026-08-01
tags: [Threat Intel, IPs, Domains]
summary: A write up on enriching IP and domain insights with open source threat intelligence
---

# IP and Domain threat intel
Security operations runbooks revolve around the process: verify -> enrich -> decide. IP and domain enrichment revolves around artefacts such as geolocation, ASNs, open-service footprints and DNS records to decide if an indicator is malicious or not.

## Domain Enrichment

1. Resolving DNS names: using tools like nslookup or dnscherker.org a domains name can be resolved to an IPv4/6 address which can then be investigated to see if it is tied to a known APT infrastructure.

2. TXT records: these records provide a lot of info about a domainn such as it's mail security settings to the tools it uses. Empty TXT records are a red flag, records may also contain suspicious SPF records or a faked DKIM signature.

3. WHOIS/RDAP: two usefull tools for domain enrichment. They reveal information such as the registrart, registration, expiry datas and the domains age. Mordern infrastructure rarely stays online for more than a few months.

Attack techniqiues using DNS:

- CDN abuse: attackers routre malicious traffic through legitimate CDNs like cloudflare. If an A record points to a CDN range, the IP itself won't tell much.
- Typosquatting (T1583.001): where attackers register look-alike or misspelled domain names to trick users.
- IDN attacks(T1583.001): Very similar to typosquatting where attackers use the fact that domain names allow non-ASCII characters like Cyrillic or Greek which have letters that look identical to latin ones. When in doubt use punycoder and convert the domain to it's punycod representation (xn-- form)

### Exercises
Context: given a domain indicator purematrixa[.]com with the goal of enriching it. The alert from the SIEM was raised on june 1, 2026

**Which CDN does the purematrixa[.]com use**
Using nslookup I can see that the domain uses Cloudflare.
![ipthreatintel](/static/images/ipthreatintel.png)

**According to the how old was the domain when the siem raised the alert**
Looking at the WHOIR record and comparing the created date to the alert date I can see the domain is only 4 days old which is indicative of a suspicious domain.
![ipthreatintel1](/static/images/ipthreatintel1.png)

## IP enrichment
Most SIEM or EDR alerts contain at least one IP. An IP that could belong to a compromised router, a shared CDN edge or a cloud service used by thousands of tenants. Without enrichment there is a risk of blocking legitimate infrastructure or ignoring a real orld C2 server. The simples enrichment available is to query the IP adress in AbusePDB and VirusToal.


### Autonomous Systems
an AS is a collection of IP prefixes unser a single orgs control (such as cloudflare, AWS, vodafone, etc). Each AS is assigned a unique ASN. Looking at the ASN helps analysts assess the likely role of an IP, for example:

- Residential ASNs: Alerts on these may indicate VPN usage or a comproised consumer devices. Example: AS124888 (Vodafone)
- Server Hostings: The most risky role, as it is often used by adversaries to dsitribute malware. Example: AS215439 (PLAY2GO)
- Cloud/CDN ASNs: Used by both legit services and adversaries, needs deeper analysis. Example: AS16509 (Amazon AWS)

### Geolocation (GeoIP)
Geolocation enrichment complements ASN lookup and is useful during the investigation of anomalous logins. Tools like ipinfo.io and iplocation.net provide approximate country. Geolocation lookup helps with:

- User logon analysis: If a UK-based employee logs on from the Netherlands, it might indicate an intrusion
- Network analysis: If you monitor a local European company, any traffic to, for exmaple, Vietnam is suspicious.

### Exercise
An alert pointing to 2[.]58[.]56[.]50, a potential C2 server adress.

**What country does the malicious IP resolve to**
Looking at the IP in virustotal I can see the IP resolves to Netherlands. it also has 8 security vendors flagging it as malicious which is likely enough to say the IP needs to be blocked.
![ipthreatintel2](/static/images/ipthreatintel2.png)

**Looking at the VirusTotal comments, what C2 server is hosted behind the IP**
Looking at the comments we can see one user commment that this is a Remcos server, doing further research shows that Remcos is a remote access trojan (S0332) a top ten malware variant of 2021.
![ipthreatintel3](/static/images/ipthreatintel3.png)

**What ANS does the IP belong too**
Looking the IP up in gbp.tools shows the ANS belongs to 1337 services GmbH which is an internet hosting and content network based in Germany
![ipthreatintel4](/static/images/ipthreatintel4.png)
Further research of this ASN shows that the ASN is under control of cyber criminals according to threatfox
![ipthreatintel5](/static/images/ipthreatintel5.png)

**What two tags does BGP.Tools attribuet to the ASN**
BGP.tools provides the two tags: Server Hosting and Tor services

## Service exposure
Knowing what services are expoed on an IP is useful from two angles:
1. When looking at a victim's public IP to try and figure out how the attacker got in
2. When looking up the attacker's IP, if it runs outdated services or has RDP exposed the host was likely compromised and is being use as a jump point by attackers

### Shodan Recon
Shodan is a powerful recon tool for IP address analysis. Shodan provides detailed info about open ports, running services and system configs:
- Open ports: the first fingerprint of exposure.
- Service banners: These provide hints on service versions. an old version usually means a vulnerable version.

### Censys search
censys.io an alternative to Shodan for blue teams as it shows exposed services even on non-standard ports and provides some advanced search capabilities.

### TLS certs
IPs that expose HTTPS services bring in a new indicator. Tools such as crt.sh to look at TLS certificate infomation is a gold mine for enrichment. there are alternative such as Censys or SSL shopper also. Key fields to look out for are:
- Issuer: A newly self-signed cert is a strong indicator that the website is worth investigating
- Validity: Newly-create and long-lived certs can also indicate malware infrastructure
- Subject: For self-certs, this can point to a program behing the HTTPS (e.g, Pfsense)

### Exercise
This time the goal is to perform a investigation of 64[.]89[.]160[.]44
It is a clearly malicious IP but the CTI team wants to get more context on the IP's role.

**What remote access service is exposed**
Looking at the censys report we can see there are 9 services open, one of which being rdp (3389)
![ipthreatintel6](/static/images/ipthreatintel6.png)

**How many ports have been identified as open on the server**
this was answered in the previous question and screenshot: 9

**One of the exposed services leak an active C2 server, What is the name of that C2**
The two exposed services that stand out are the "unknown" ones, looking at port 1000 shows a TCP connection to AsyncRAT, which when looking up is a malicious remote access trojan that connects to a C2 server using an encrypted TCP connection
![ipthreatintel7](/static/images/ipthreatintel7.png)

**For how many days is the C2 servers cert valid**
Looking up the c2 server shows the cert is vali for 3935 days
![ipthreatintel8](/static/images/ipthreatintel8.png)

## VPN detection
The goal of a login alert where the location is the same, same country, same city and same user agent, all that's off is it's outside working hours. The goal is to answer the question is this a real user or someone behind a VPN.

IP2proxy and Spur are two essential resources for labeling VPN, proxy and tor exit nodes. 

### SOC workflow

1. Investigate the domain.
    - Does it look legit? Does it remind you of typosquatting
    - What is its rep? is it a known malicious domain?
    - When was it registered? if it's new, that's suspicious
    - Resolve the domain to IP and investigate the IP
2. Investigate the IP
    - Is it a CDN range? if yes, no need to investigate further
    - What is its rep? use virusTotal and AbuseIPDB
    - Where is it located? is it a VPN node? how does it match the alert?
    - What AS type does it belong to? how does it match the alert?

## Challenge
An APT group has just struck your company and the IR team is working through it. The task is to gather everything there is on a malicious domain and ID the infrastructure the malware relies on. the domain is raytracingengine[.]com

**What IP does the domain resolve to**
Using NSlookup resolved the domain name to an IPv4 address
![ipthreatintel9](/static/images/ipthreatintel9.png)

**What cloud provider did the attacker use**
Continuing with NSlookup I can see the ASN is google suggesting the provider is google cloud
![ipthreatintel10](/static/images/ipthreatintel10.png)

**What country is the malicious server located in**
This can be seen in the previous screenshot: United States

**When was the malicious domain created**
Moving over to WHOIS i can use the important date sections to get the creationd date of the domain.
![ipthreatintel11](/static/images/ipthreatintel11.png)

**According to the exposed service what is the attackers servers OS**
Resolving the name to an IP and putting it into Censys I can see one of the exposed services is ssh a service typical used in Linux systems, the OS field also says it is Canonical linux.
![ipthreatintel12](/static/images/ipthreatintel12.png)

## Conclusion
This writeup covered how to turn a raw IP or domain into something an analysts can actually act on. Using tools such as WHOIS/RDAP for ownership and domain age, ASN lookups for who owns the network and what else lives there, TLS certs and other indicators to help during alert triage.


---
- **IP and Domain Threat Intel**
- **TryHackMe**
- **Medium**
- **2026-08-01**
- **Threat analysis, Domains, IPs**
- **A write up of how to turn raw IPs and Domains into threat intelligence**
