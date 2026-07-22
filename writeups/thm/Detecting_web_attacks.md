---
title: Detecting web attacks
platform: TryHackMe
difficulty: easy
date: 2026-07-22
tags: [Web security]
summary: A write up of the methods and tools used to detect web attacks
---

# Detecting web attacks
With web attacks being among the most common ways for attackers to gain entry into a system learning how to detecting and defend against them is essential in cyber security roles.


## Client-side attacks
This kind of attack relys on abusing weaknesses in user behaviour on the user's device, exploting vulnerabilties in browsers or tricking the user into performing unsafe actions. Unfortunately due to this tools used by SOC analysts such as server-side logs and network traffic captures offer little to no visibility into what occurs inside a user's browers making it difficult or even impossible without additional browser side security controls or endpoint monitoring to detect.

Common client-side attacks:
- XSS: The most common client-side attack where attackers run malicious scripts in trusted websites hat execute in the users browser
- Cross-site Request forgery (CSFR): In this attack the browser is tricked into sending unauthorized requests on behalf of the trusted user
- Clickjacking: Attackers overlay invisible elements on top of legitimate content making users believe they are interacting with something else

## Server-side attacks
server side attacks rely on exploiting vulnerabilities within a web server, the apps code or the backend that supports a website or web app. Attackers attempt to exploit server logic, misconfigs, input handling togain access.

Unlike client-side attacks, server-side attacks leave a trail of evidence known as indicators of compromise.

Common server-side attacks:
- Brute-force: brute forcing username and password combos in a short time to gain access
- SQL injection: using string concatenation to inject sql queries and commands to attack the database behind the website. MOVEit, 2023 - SQLi vulnerability was exploited affecting over 2'700 orgs including U.S. gov agencies, the BBC and British airways
- Command injectin: An attacker takes advantage of a wbesite that takes user input and passes it to the system without checking it allowing them to sneak in commands that the server will run.

## Log-Based detection
Logs are used in all areas of cyber security and it's no different with web apps. Every requests sent to a web server cna leave evidence in its access and error logs.

Access log format:

|Log field|Example indicator|
|---------|-----------------|
|Client IP|A known malicious or outsie of the expected geo range|
|Timestamp and requested page|Requests made at unusual hours or repeated in a short period of time|
|Status code|Repeated 404 responses indicating a page could not be found|
|Response size|Significantly smaller or larger than normal response sizes|
|Referrer|Referring pages that don't fit normal site nav|
|User-Agent|Outdated browser versions or common attack tools: sqlmap/wpcan etc|

### Exercises
**What is the attacker's user-agent while performing the directory fuzz**
Looking in the logs the attempt of directory fuzzing can be seen by the rapid succession of GET requests to the web server with many providing 404's meaning the attacker is goign through a list sequentially.
![ffuf](/static/images/ffuf.png)

**What is the name of the page on which the attacker performs a brute-force attack**
The name of the page is the same name of one of the pages the attacker got a 200 reponse when performing the directory fuzz which is login.php, the user-agent also shows they're using Hydra to perform the bruteforce
![hydra](/static/images/hydra.png)

**What is the complete, decoded SQLi payload the attacker uses on the /changeusername.php form**
First this requires going through the logs and finding the POST request from the attacker
![sqli](/static/images/sqli.png)
Then moving this code into cyber chef to decode it which shows the sqli code they injected to dump the database
![cyberchefsqli](/static/images/cyberchefsqli.png)

## Network-based detection
Network traffic analysis allows for examination of raw data exchanged between client and server allowing for packet analysis using tools like wireshark.

**What password does the attacker successfully ID in the brute-force attack**
Filtering for http.response.code == 302 shows successful logins where we can find the packet that contains the successful login and the password by following the stream.
![httpstream](/static/images/httpstream.png)

**What is the flag the attacker found in the database using the SQLi**
following the stream of the SQLi injection shows the flag
![httpstreamflag](/static/images/httpstreamflag.png)

## WAF
WAFs are the first line of defences for websites and web apps. They are the gatekeepers for web apps that inspect packet requests with the abilitiy to decrypt TLS traffic and filter it before it reaches the server.

|Rule type|Decsription|Example|
|---------|----------|-------|
|Block commmon attack patterns|Blocks known malicious payloads and indicators|Block malicious user-agents:sqlmap|
|Deny known malicious sources|Uses IP rep, threat intel, or geo-blocing to stop risky traffic|Block IPs from recent botnet campaigns|
|Custom-built rules|Tailored to specific applications needs|Allow only GET/POST requests to /login|
|Rate-limiting and abuse prevention|Limite user frequency to prevent abuse|Limit login attmepts to 5 per minute per IP|

Example custom rule: if User-agent CONTAINS "sqlmap" THEN block

## Conclusion
To conclude web attacks can be performed commonly on client and server side and are detected through various methods and tools including log analysis, network analysis and using web application firewalls with custom rules. By correlating across sources alerts can be transformed into approaches to defend and respond to web attacks

---

- **Detecting web attacks**.
- **TryHackMe**
- **Easy**
- **2026-07-22**
- **Web Security**
- **A write up of the common web attacks and methods and tools used to detect them** 

