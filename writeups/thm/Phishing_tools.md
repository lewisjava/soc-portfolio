---
title: Phishing - Tools
platform: TryHackMe
difficulty: easy
date: 2026-07-13
tags: [Phishing, Tools]
summary: A guide to using the tools that allow deeper analysis of Phishing emails.
---

# Phishing Tools

Write your content in standard markdown below. Everything here gets rendered.

## Artefacts
When analysing emails the initial goal is to discover and collect artifacts that will help determine it's legitimacy and intent. The artifacts are the foundation for deeper investigations such as reputation checks, threat intelligence lookups and behavioural analysis. Artifacts can be found in both the header and the body and both require analysis

Header artifacts:
- Sender email address
- Sender IP address
- Email subject line
- Recipient email address
- Reply-to email address
- Dat and time

Body analysis:
- URLs and hyperlinks
- Attachment name(s)
- Attachment hash

## Header Analysis
By manually extracting header data by viewing the source code the senders IP, address and Reply-to information can be found. However Messageheader, a tool part of the Google Admin Toolbox analyses the header by simply pasting the full header into the tool and in response it will return the key details such as senders IP, routing path and potential misconfigurations
![MessageHeader Tool](/static/images/messageheader.png)

There are other great tools such as Message Header Analyzer and more.

Analysing deeper using the information provided, the IP returned can be used to perform a Reputation analysis, by simply entering the IP (or URLs) into a tool called IPinfo it will provide information such as geographics location and associated orgs to the IP.

There are other tools such as URLScan.io and Talos IP & Domain reputation centre which is a Cisco threat intelligence tool that assesses the reputation of IP's, domains and networks.

![Talos](/static/images/talos.png)

## Body Analysis
After analysis of the header the natural next step is analysis of the body where the true intent of a phishing email is often reveealed. This is where the malicious payload is often devlivered via hyperlinks designed o lure uses to phishing sites or as attachments intended to compromise the target system. During analysis the links can be extracted manually from the visible email content or by examining the underlying HTML and raw source to uncover hidden or obfuscated URLs.

### Links/URLs (T1566.002)
You can manually assess the destination of a link by coppying it's address, pasting it and then looking over the resulting link. But another effective way would be to use a tool such as URL extraction tool or cyberchef which both have the functionality of parsing all embedded links which saves time and reduces the risk of missing hidden/obfuscated URLs.
![URl extractor](/static/images/linkextraction.png) This falls under the MITRE D3FEND technique URL reputation analysis D3-URA and URL analysis D3-UA under the Detect Tactic

|MITRE D3FEND technique|ID|Tactic|
|----------------------|--|------|
|URL analysis|D3-URA|Detect|
|URL reputation analysis|D3-UA|Detect|

### Attachments (T1566.001)
When attempting to analyse attatchments it is essential this is done in an controlled and isolated environment such as a lab machine or sandbox to reduce the risk of accidental execution. Once downloaded tools like sha256sum can be used to generate a hash value for further analysis. The hash value tcan then be uploaded to other tools like the very valuable VirusTotal which is a widely used tool that checks the reputation of files, URLs, IPs and domains using data from security vendors.
![Virus Total](/static/images/virustotal.png). This falls under the MITRE D3FEND technique D3-FHRA file hash reputation analysis

|MITRE D3FEND technique|ID|Tactic|
|----------------------|--|------|
|File Hash reputation analysis|D3-FHRA|Detect|
|File Hashing|D3-FH|Detect|

### Malware Sandboxes
One of the best tools at a SOC analysts disposal is the use of malware sandboxex where you can upload a file to be analyzed in a controled environment. This allows for the safe observation of the behaviour of the malicious file in action without any risk to systems. By doing an analyst can observe the URLs it attempts to contact, any payloads it downloads and any other IOCs (Indicators of compromise)

For example one very popular tool is ANY.RUN, an interactive malware sandbox, it provides a hands-on experience that allows an anlysts to interact with the environment, monitor processes, view network activity and anlyze system changes as they take place.
![anyrun](/static/images/anyrun.png)

|MITRE D3FEND technique|ID|Tactic|
|----------------------|--|------|
|Dynamic analysis|D3-DA|Detect|

## PhishTool
PhishTool is a platform that streamlines phishing investigations, it is able to autmoate much of the manual work involved in analysis, this helps SOC analysts triage user-reported messaged to threat intelligence analysts collecting indicators or a researcher investigating phishing kit. It combines threat intelligence OSINT, email metadata and automated analysis workflows.

![PhishTool one](/static/images/phishtool1.png)
After uploading an email to phish tool, it will present many valuable artifacts and on th right side it will show the rendered and raw HTML as well as the message source.

![PhishTool two](/static/images/phishtool2.png)
PhishTool offers tabs that allows for ease of analysis of various components of the email from auth results, transmission paths and URL analysis.

![phishtool three](/static/images/phishtool3.png)
One of PhishTool's key features is it's seamless integration with VirusTotal allowing for reputation and detection results without ever having to leave the tool.

![Phishtool four](/static/images/phishtool4.png)
Finally PhishTool allows for formal documentation of findings that includes marking the email as malicious or not and key artifacts such as addresses, IPs and embeddeed URLs to be flagged. These get added to investigation notes and Resolved.

### Conclusion
In conclusion Phishing analysis of emails is a rigorous that requires analysis of various elements for many different artifacts, IOCs and more. This process has been shown to be significantly streamlines by the use of various tools that should be at the disposale of any analysts due to their effeective nature that has been demonstrated clearly within this write up.

---

- **Phishing - Tools**
- **TryHackMe**
- **Easy**
- **2026-07-13**
- **Phishing, Tools**
- **A look and breakdown of usefull tools for phishing email analysis**
