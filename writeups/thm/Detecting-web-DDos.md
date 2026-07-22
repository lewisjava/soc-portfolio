---
title: Detecting web DDoS
platform: TryHackMe
difficulty: easy
date: 2026-07-22
tags: [Web security]
summary: A write up of web DDoS attacks methods and how to identify them using analysis and tools.
---

# Detecting web DDoS
Denial-of-service attacks (TA0814) come in many forms and attack the Acceessibility in the CIA triad aiming to disrupt or completely block access to a website or web service.

DoS attacks do this by overwhelming a website or app so that they can't be used. DoS attacks can be launched at different layers of th OSI model but since this is focusing on web security the focus will be on layer 7.

Types of Dos attacks:
|Attack type|Description|
|-----------|-----------|
|Slowloris|Sneding many partial HTTP requests to tie up server resources|
|HTTP flood|Sending a large number of HTTP requests to overwhelm the server|
|Cache Bypass|Bypassing CDN edge servers and forcing the origin server to respond|
|Oversized Query|Forcing the server to process large,resource-intensive requests|
|Login/Form abuse|Overloading the auth logic with login attempts or password resets|
|Faulty Input Validation Abuse|Exploting poorly designed input handling|

- Anonymous Sudan, 2023: Notorious hacktivist group known for using DDoS attacks, launched an attack against microsoft causing Azure, OneDrive and Outlook outages by using HTTP flooding and Slowloris o overwhelm web servers.

## Log Analysis

|Indicator|Example|Description|
|---------|-------|-----------|
|High Request rate|10.10.10.100 -> 1000 GET /login|Resource heavy page login is flooded with requests to overwhelm auth processes|
|Odd User-agents|curl/7.6.88 -> /index|Attackers spoof outdated or unusual user-agents to blend in or bypass filters, user-agents with tools is a red flag for automated attacks|
|Geographic anomalies|IP address origins dotted around the world|Legit traffic typically comes from a few regions where real users are located, globally distributed botnets utilize IP addresses from around the world|
|Burst Timestamps|50 requests in 1 second -> /search|A sudden spike of requests packed into the same second creates an unnatural traffic pattern that points to automation|
|Server Errors(5xx)|A significant spike of 503 service unavailable errors|A sudden surge of server error responses indicates resources are maxed out and the service is struggling under attack traffic|
|Logic Abuse|GET /products?limit=999999|Crafted queries to overload the server forcing it to load huge amounts of information and slowing it down for everyone|

Attackers typically focus on endpoints that consume the most server resources per reqeusts or the most critical endpoints:
- /login
- /search
- /api
- /register or /signup
- /contact or /feedback
- /cart or /checkout

### Exercises
The exercise provides access.log on a machine to investigate, it only takes scrolling through the logs without any commands to see there is a flood of get requests coming from a user-agent with the name curl suggesting this is the attacker.

**What is the attackers IP address**
Looking at the ip associated with the requests and user-agent shows the ip is 203.12.23.195
![dos](/static/images/dos.png)

**What page is repeatedly targeted by the attacker's requests**
/login

**After the attack, what error code do legitimate users receive**
scrolling down to the requests taken place after the attack shows users get a server error 503

## Leveraging SIEMs
Since DoS attacks generate huge amounts of traffic these can easily be viewed on any SIEM dashboard where a visual distribution of traffic can be seen, a DoS attack would show a very heavy spike in traffic.

### Exercises
**What was the most frequently requested uri**
Since this data is all sorted by splunk it is very easy to find by looking in the uri fields where I can see /search is the most requested uri
![uri](/static/images/uri.png)

**Which clientip made the most requests to the target uri**
All I had to do was add the uri to the display filter and then go to the clientip field and look at the top one which was 203.0.113.7
![clientip](/static/images/clientip.png)

**How many IP addresses were part of the botnet that attacked your website**
This requires looking at the number next to clientip in the interesting fields bar on the left in the previous screenshot to see the amount of IPs involved in the botnet which is 60.

**which useragent was most commonly used by the attacking traffic**
Navigating to the user agent interesting field with the pevious display filter applied shows the top user agents involved with the number 1 being java/1.8.0_181
![useragentsplunk](/static/images/useragentsplunk.png)

**use the timechart command to visualize the requests. what is the peak number of requests made per second during the attack**
at first I attempted to visualise the data using the command timechart span=1 count(\_raw) however this showed me the total amount so i had to head over to the splunk documentation to find out the syntax required to acheive my goal. This is where I found out I could set the span to 1 second with span=1s which showed the peak requests per second was 207.
![peak](/static/images/peak.png)

**Which legit clientip received the first 503 response post-attack**
This simply required adding the server response 503 to the display filter and looking at the first ip not involved in the attack.
![503](/static/images/503.png)

## Defence
### Application level Defense
Secure development practices.
A scure site requires secure code, search field and forms must validate input so they can't be abused.

One way to stop automated traffic is to require a challenge before granting access such as the well known CAPTCHA.

### Network and Infrastructure Defences
Content delivery networks help manage server load by caching and serving content from the edge servers closets to users reducing latency and allowing the origin server to only handle a fraction of requests. CDNs beyond absorbing traffic also provide analysts with visbility including visuals and diagnostics of website traffic.

WAFs (typically integrated into CDNs) shield servers and inspect incoming traffic to either allow, challenge or block requests when compared to a set of rules.

Mordern defence solutions are sometimes required for large scale mitigation one of the most well known services for this CloudFlare.

## Conclusion
To conclude there are many types of DoS attacks with many different motives behind them, as well as how to identify them in logs or SIEMs using a a hands-on splunk exercise, and how CDNs and WAFs defend websites against DoS attacks.

---

- **Detecting web DoS**
- **TryHackMe**
- **Easy**
- **2026-7-22**
- **Web Security**
- **A write up of DoS attacks, how to identify them in logs and what tools defend against them**
