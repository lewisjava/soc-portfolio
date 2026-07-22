---
title: Web security essentials
platform: TryHackMe
difficulty: easy
date: 2026-07-22
tags: [Web security]
summary: A write up of how the web works with common website security risks
---

# Web security
As SaaS rose and applications could be run through web browsers accessibility, faster updates and better compatibiltiy rose but so did the opportunities for attackers. Web applications are amongst the most common entry points for attackers accounting for more than 40% of all data breaches with up to 75% of all cyber attacks and information security incidents specifically targeting web apps - Crowdstrike, global threat report, 2026.

- Equifax, 2017: 150 million americans has their customer data compromised due to an Apache vulnerability.
- Capital one, 2019: over 100 million customers sensitive personal and financial information exposed due to a misconfigured web application firewall.

Web apps function through a request-response cycle which attackers try to abuse by overwhelming servers with requests, bypassing access controls or even tricking the server into executing harmful commands.

Components of a web service:
- Application: code, images, style and icons
- Web server: hosts the application, listens for requests and returns responses
- Host machine: the underlying os that runs the web server and app

## Protecting the web

Protecting the application:
- Secure code: avoiding insecure functions, ensure proper handling of errors and remove sensitive information
- Input validation & Sanitization: validate and sanitize user input to prevent injection attacks.
- Access control: Restrict access based on user roles.

Protecting the web server:
- Logging: Keep detailed record of all web requests with acess logs.
- WAF: Filter and block harmfull traffic based on defined rules
- CDN: Reduce direct exposure to your server and use integrated WAFs

Protecting the host machine:
- Least priviledge: Use low-privilege users for services
- System hardening: Disable unnecessary services and close unused ports
- ANtivirus: add endpoint-level protection that blocks known malware

|CDN Benefit|Description|
|-----------|-----------|
|IP masking|Hides the origin server IP address making it harder to target|
|DDoS protection|CDNs can absorb a large ammount of traffic making DoS attacks less effective|
|Enforced HTTPS|Encrypted comms via TLS is enforced by default by most CDNs|
|Integrated WAF|Many CDNS integrate web application firewalls|

WAF types:
- Cloud-based: sits in front of the web server, easy to deploy with great scalability.
- Host-based: Software deployed directly on the web server and offers control for each app
- Network-based: A physical or virtual appliance situated on the network perimeter, more suited for enterprise environments

## Conclusion
In conclusion web applications are everywhere and are constantly growing, making them a constant target to attacks and due to this there are many tools to help protect against them

---

- **Web security - fundamentals**
- **TryHackMe**
- **Easy**
- **2026-07-22**
- **tags**
- **summary**
