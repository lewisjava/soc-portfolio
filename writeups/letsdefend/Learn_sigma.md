---
title: Learn sigma
platform: LetsDefend
difficulty: easy
date: 2026-07-23
tags: [Detection rules]
summary: A LetsDefend challenge that explains sigma rules
---

# Sigma rules
Sigma rules standardize how analysts define threat detection logic, allowing teams to write a rule once and translate it to multiple platforms like Splunk, Elastic, or microsoft sentinel.

Sigma rules consist of four primary sections:
1. Header: for metadata like title, ID, author and tags mapped to frameworks like MITRE
2. Log source: spcifes the data source such as firewall, windows event log, process creation
3. Detection: The boolean logic, selections and filters used to spot anomalous behaviour.
4. Condition: Determines when the rule triggers based on the detection data

Sigma rules are used for three main reasons:
1. Platform portability
2. Community sharing
3. Efficiency


## Exercises
In this LetsDefend challenge the organisation in the scenario has detected a ransomware infection which searches for valuable files, such as sensitive documents and config files, encrypts them using a strong encryption algorithm to ransom them. The investigation done shows the ransomware used the Windows utility bitsadmin.exe to download malicious payloads or communicate with it's c2 server. 

A sigma rule has been pre written and the task is to review it and answer the questions to understand the different rule secetions (selection,condition,fields,tags,logsource) work together to detect malicious activity

**Which executable file was specifically targeted by ths sigma rule**
Since I knew the name of the exe used thanks to the challenge description I was able to locate the executable name in the rule which then allowed me to understand which section of the rule correlates to file targeting which is "selection_img:"
![sigma1](/static/images/sigma1.png)

**Which command-line option is used to indicate a file transfer in this rule**
Finding this was rather easy "/transfer" is the command line option
![sigma2](/static/images/sigma2.png)

**What logical expression in the condition field combined the criteria to trigger this rule**
I assumed the answer would be what's found in the "condition" field which it was the rule requires selection_img field and one of selection_cmd or all of selection_cli_* for the rule to trigger
![sigma3](/static/images/sigma3.png)

**What specific field did this rule capture that shows the command being executed**
The answer to this question is found under the fields section and it is CommandLine
![sigma4](/static/images/sigma4.png)

**which single att&ck tactic tag is listed first in this rule**
Mitre isn't specifically mentioned in any of the fields but since I have experience looking at the framework I recognised the tactic name and found the answer pretty quickly
![sigma5](/static/images/sigma5.png)

**what is the primary category of events that this sigma rule was written to monitor**
Since I have experience looking at Windows Event Viewer I was able to identify what is meant by category of events in the question and it is process_creation (4688 / 1)
![sigma6](/static/images/sigma6.png)

**what specific command-line argument did this rule look for to ID http-based downloads**
To do this the rule contains the argument "CommandLine|contains: 'http'" to id any command entered that may be attempting to curl or wget from the web
![sigma7](/static/images/sigma7.png)

**which command-line option must be present to create a new transfer using bitsadmin**
Looking in the selection_cli_1 section i can see that it looks for command line commands that contain either /create or /addfile, for this question the answer is /create
![sigma8](/static/images/sigma8.png)

## Conclusion
To conclude sigma rules are a vendor agnostic, open-source text signatures written in yaml that standardises syntax to streamline workloads, with a clear and easy to follow workflow that makes writing new rules easy and portable.

---

- **Sigma rules**
- **LetsDefend**
- **easy**
- **2026-07-23**
- **Detection rules**
- **A write up of sigma rules, what they are, why the exist and how they are written**
