---
title: SOAR
date: 2026-07-09
tags: [SOAR, Tools, SOC]
summary: A brief summary/guid to the Security, Orchestration, Automation and Response tool.
---

# SOAR


## What is SOAR

SOAR is a tool that allows SOCs to overcome so challenges they face, these include;alert fatigue, too many disconnected tools, manual processes and talent shortage. SOAR achieves this through it's three main capablities; Orchestration, automation and response.

Orhestration - When investigationg an alert you typical have to switch between multiple security tools, SIEM, threat intelligence patforms, IAM tool, Ticketing systems etc and this can be a slow process. Orchestration solves this by coordinating al these tools together inside SOOAR alongside a defined workflow for investiagtion known as a Playbook.

Automation - The coordination of multiple tools alongside a playbook can also be automated, automation significantly speeds up the process of investigation and decreases the risk of alert fatigue.

Response - The response can also be automated and following a Playbook SOAR has the capability to respond automatically to certain threats.

## Building a playbook
Since phishing continues to remain the most common attack vector used in breaches I will use that as an example for this playbook demonstration.

1. Suspeceted email is received
2. Create investigation ticket
3. Check does the eail contain urls or attachments? if no notif users and end, if yes continue
Branch A 
4. a. Check: does it contain attatchments? if yes continue
5. a. compute hash of attatchment
6. a. Submit hash to VirusTotal
7. a. is hash malicious? if yes delete emails (step 9) if no got to manual analysis of email in a sandbox (step 8)
Branch B
4. b. Check: does it contain URLs? if yes proceed.
5. b. send URL to virusTotal
6. b. Is the URL malicious? if yes go to delete emails (step 9) if no go to manual analysis of emal in a sandbox (step 8)

8. Manual analysis of email in a sandbox - performed when neither hash or ulr comes back as confirmed malicious via automated lookup, since VirusTotal misses can still be malicious.
9. Delete emails, reached via malicious hash/URL or malicious results from sandbox analysis
10. Ticket update with IOC's

## CVE patching
SOAR is also incredibly usefull for automation a large part of CVE patching, sinc CVE patches are released very frequently it would take up a large amoun of SOC resources to continusly apply these patches or else face a backlog and end up with lots of vulnerabilites But by developing a playbook with SOAR this can be mitigated.

---

- **SOAR**
- **2026-07-09**
- **SOAR,tools,automation**
- **A brief summary of the SOAR tool and its uses within an SOC**
