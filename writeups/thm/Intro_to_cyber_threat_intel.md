---
title: Intro to Cyber Threat Intel
platform: TryHackMe
difficulty: easy
date: 2026-07-31
tags: [Threat analysis, Threat intelligence]
summary: An introductory write up into cyber threat intelligence and related topics
---

# Intro to threat intel
This room seeks to translate the sometimes abstract discipline of CTI into everyday tasks: enriching indicators, triagine alerts and turning raw data into the stories that matter.

- Understand what threat intelligence is and why it matters to SOC analysts
- Know about the threat intelligence lifecyle and the indicators to look for
- Familiarise with intelligence sharing using feeds and platforms

## Cyber threat inelligence
CTI seeks to answer three essential questions:
1. Who, or what, is on the other end of this aler indicatior
2. What was their behaviour in the past
3. How does mmy org respons and what should I do abut it

### From data to usable intelligence
Information security literature disinguishes data, information and intelligence. the below table shows how they are distinguished
|Layer|definition|Alert-queue example|SOC L1 action|
|-----|----------|-------------------|-------------|
|Data|An unprocessed observable|45.155.205.3: :445|Capture the artefact|
|Information|Data plus factual annotation|IP registered to Hetzner, first seen 2023-07-14|Record attributes|
|Intelligence|Analysed information that answers so-what|IP belongs to the current BumbleBee C2;block immediately|Escalate or suppress|

In the above table the goal of the L1 is to enrich artefacts until they qualify as intel, this push is enacted through enrichment; a rapid and methodical lookup of public, commercial and internal srouces that shed light on origin, behaviour and relevance.

During that ascent from data to intel, three more labels are of importance:
- Indicator of comproimse (IOC): Evidence of a breach such as a C2 address in logs.
- Indicator of Attack (IOA): A malicious action, such as PowerShell launching an unknown service, is underway.
- Tactics, Techniques and Procedures: an adversart's detailed methodologies expressed in mitre att&ck IDs and descriptions

### Indicator Types essential to first-line triage
Knowing what kind of indicator the alert supplies and knowing where to look is important
|Indicator|example|First resources|Associated IO or TTP|
|---------|-------|---------------|--------------------|
|IPv4/6|45.155.205.3|WHOIS / VirusTotal / shodan banner scan|IOA: repeated SSH failures / TTP:T1110.003 Password guessing|
|Domain / FQDN|malicious-updates[.]net|WHOIS age / RiskIQ or securitytrails passive-DNS / urlscan.io|IOA:surge of DNS queries to a 24-hour-old domain|
|URL|hxxp://malicious-updates[.]net/login|URLhause reputation / urlscan.io beahviour graph / any.run dynamic run (network off)|IOA: browser POST to /gateway.php with payload|
|file hash| e99a18c428...|VirusTotal static & dynamic / Hybrid-analysis / MalShare corpus|TTP:T1055 process injection into regsrvr32.exe|
|E-mail address|billing@evil-corp.com|MXToolbox header analysis / have i been pwned|IOA: SPF failure plus recent domain registration|
|Local artefact|HKCU/Software/run/updated.exe|Sigma rules / EDR prevalence query / Vendor knowledge base|TTP:T1060.001 Registry Run Keys|

### Sources of Cyber threat intelligence

- Internal telemetry: SIEM Logs, EDR detections, phishing-mailbox submissions provide the highest immediate relevance
- Commercial services: Vendor premium feeds, paid sandboxes, and closed-source analytics. These provide high fidelity, but may have export and sharing limits based on licensing
- OSINT: AbuselPDB, URLhause, public blogs with IOCs and academic research. Before applying, information from these sources will need to by cross-confirmed.
- Communities and ISACs:Sector-specific lists marked with labels and rich context (e.g., FS-ISAC)

### Threat intelligence classifications
threat intell is geared towards understanding the relationship between your operational environment and your adversary, with this in mind threat intell can be broken down into the following classifications

- Strategic intel: High-level intel that looks into the orgs threat landscape and maps out the risk areas based on trends, patterns and emerging threats that may impact buisness decisions. An example is an annual ransomware trends report predicitng a shit to data-wiping extortion in healthcare.

- Tactical intel:Assesments of adversaries behaviours through analysis of tactics, techniques and procedures. This can be in the form of Advirosy notes, such as detailing new T1059.005 (Visual basic) abuse in malspa.

- Operational intel: Cmpaign-specific details about the motives and intent to perform an attack. This is useful for understanding the critical assets available in the org (people, processes and tech)that may be targeted.

- Technical intel: Atomic indicators and artefact such as IPs and hashes related to an attack

## CTI lifecycle
Cyber threat intelligence follows a six-phase intelligence lifecycle

1. planning and direction - defining the mission
such as what assets to protect, what business risks there are to not protecting, what available con
trols are their (firewalls, EDRs etc.), what goals (such as using threat-feed indicators to block or alter on suspect IP addresses at the firewall or detect known malicious file hashes at the EDR layer)
2. Collection - Assembling raw material from sources and gathering artefacts relevant to the mission such as sources (commercial feeds, open-soucre projects, MISP, vendor threat repots etc.)
3. Processing - Normalising and correlating the raw feed data.
4. Analysis - Turning information into judgement
5. dissemination - Getting intelligence to the right consumers; Examples include providing firewall CSV to fireall team, yara rule set to Endpoint team, Indicators objects with full tags to CTI platform and written summary to management to show report of the mission and ROI.
6. Feedback - Measuring and refining the cycle; 

Once intel is gathered they are responsible for sharing and updating other analysts on new findings about attack techniuqes, one format in which threat intel can be found is stuctured threat inforation expression (STIX) a JSON schema developed to describe and specify threat indicators, relationships and context in a machine-readable format.

## CTI standards & frameworks

- MITRE ATT&CK: matrix that matches tactics, techniques and procedures of an adversary to a tag
    - Match behaviour in the alert to a tactic/techniuqe pair.
    - Write the ID in your triage note: "Observed T1071.001 (Web based C2) against FINANCE_WRkSTATION-00
    - Hand the note to a Level 2 or incident response

- MITRE D3END: catalogues how to respond to attacks, each entry maps to defensive tactics, example:
    - Your proxy raises a T1048.003 DNS tunnel alert
    - Search D3FEND for the matching defensive technique: D3-NTDN DNS-request analysis. the page lists practical control: block extensive TXT records and alert on uncommon query entropy
    - Add the most feasible control to your "next actions" field, supplies mitigation on top of diagnosis

- Cyber Kill chain: Breaks down adversary actions into steps, help identify stage-specific activities occured when investigating an attack

- CVEs, CVSS and the NVD:
    - CVE (Common vulnerabilities and exposures): Provides a catalogue number for discovered vulnerabilities, CVE-2023-4863
    - CVSS (Commone vulnerability scoring system): a 0-10 severity scale with temporal and environmental modifiers for vulnerabilities
    - NVD( National vulnerability data): the canonical repository that links CVE numbers to CVSS scores, exploits and affected products

- Sharing and processing intel:
    - STIX: a structured JSON schema for describing threat information
    - TAXII: the Trusted Automated eXchange of Indicator Information is a set of secure APIs used to exchange threat intelligence in near real-time for detection, prevention and mitigation threats. Supports two sharing moddels: Collection which enrues threat intel is collected and hosted by a producer and channel which publishes threat intel to users from a central server.



---

- **Intro to threat intelligence**
- **TryHackMe**
- **Easy**
- **2026-07-21**
- **Threat intelligence**
- **A introductory write up into cyber threat intelligence, it's life cycle and sources**
