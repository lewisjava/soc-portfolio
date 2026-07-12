---
title: Phishing - Emails in action
platform: TryHackMe
difficulty: easy
date: 2026-07-12
tags: [Phishing]
summary: Examination of real phishing emails.
---

# Emails in action
By analysing real world examples of phishing attempts you can learn to understand and identify the techniques and procedures used and be able to discrimante between legitimate routine emails and malicious ones such as a credential harvesting attempt.


## Email one
In this example the email is designed to mimic an official transaction receipt from PayPal. The attackers leveraged a spoofed email addresses to impersonate trusted services and used a URL shortening services to obfuscate the final destination of the malicious link.
![Email one header](/static/images/email1header.png)

Looking at the screen shot above there are three common techniques used that stand out:
1. Attention grabbing subject line, the fake transaction evokes that sense of urgency that makes the recipient make mistakes and act hastily.
2. The from address where the sender details do not match the actual address. Service@paypal.com vs noreply...@sultanbogor.com
3. The to address is an unusual email recipient address and not a normal Yahoo domain.

![Email one body](/static/images/email1body.png)
Looking at the screenshot above, after inspecting the email we can see everything as usual for an email impersonating paypal and there is also a HTML button for canceling the order which needs to be inspected. 

![Email one button](/static/images/email1button.png)
Inspecting the button reveals it is actuall a redirecting link which when used in a tool such as WhereGoes the destination can be inspected without actually visiting it.


|Technique used|MITRE refrence|Mitre Tactic|
|--------------|--------------|------|
|Email spoofing|T1684.002|Stealth
|URL shortening|T1608.005|Resource development|
|Branded HTML|T1684.001|Stealth

## Email two
This next email mimics a formal shipping notification to attempt to trick recipents into a sense of urgency utilising social engineering against them. Through analysis of the email the use of spoofed addresses, link manipulation and tracking pixels is used to compromise victims of the attack.

![Email 2 headeer](/static/images/email2header.png)
Looking at the screenshot above of the second example email the first thing that stands out is the subject line, it uses a fake tracking number that mimics the syntax of a regular tracking number in order to create a sense of urgency and replicate a legitimate email. Secondly the from address has the display name as Distribution Cnter but the actual sender address is contact@beginpro.club. Finally the hyperlink in the email matches the subject line but there is no idea where it goes until the source code is inspected.

![Email 2 body](/static/images/email2body.png)
In the above screenshot the source can be inspected and the href for the tracking button can be seen as well as the src. the src is a tracking pixel, a very very small image that gets loaded into an email and will send lots of information including the recipients IP address back to the senders server and is why most email providers block images in emails.


|Technique used|MITRE Refrence|MITRE Tactic|
|--------------|--------------|------------|
|Email spoofing|T1684.002|Stealth|
|Pixel tracking (Phishing for information)|T1598.003|Reconnaissance|
|Link manipulation|T1566.002|Inital access|

## Email three
This email is different from the other too as it is part of a phishing campaing that utilized a multi-stage redirection chain to harvest user details. It demonstrates how attackers leverage reputations of professional document-sharing services such as adobe, one drive, microsoft etc. to create a deceptive path that leads the victim to a draudulent login portal.

![Email 3 header](/static/images/email3header.png)
Looking at the example email above it can be seen that the email was intially sent on Thursday the 15th of July 2021 and within the email there is claims of an expiration date that occurs only 8 days from when the email is received, this is an attempt at creating urgency a social engineering technique that has been used in all 3 emails so far and that's because it is very common. Finally there is a download document here button.

![Email 3 body](/static/images/email3body.png)
Looking deeper into the email when the link is clicked it redirects to a landing page that mimics a leigitmate OneDrive share and interacting with the buttons on this page further redirects to a second site impersonating Adobe. If carefully inspecting these sites it becomes apparent that the URLs are suspicious and the provided directions on the page are nonsensical. However these pages act as credential harvesting portals a common technique known as web portal capture, a credential access and collection tactic used by attackers to steal information. In this example the user will attempt to login using their outlook details to use the tools however, even when entering correct details, they will be presented with a generic error message as the tool is not legit and the details they entered have now been sent to the attackers server.

|Technique used|MITRE Refrence|MITRE Tactic|
|--------------|--------------|------------|
|Artifical urgency|T1684|Inital Stealth|
|Brand impersonation|T1684.001|Stealth|
|Link redirection|T1204.001|Excution|
|Credential harvesting|T1056.003|Credential Access/Collection|

---

- **Phishing - Emails in action**
- **TryHackMe**
- **Easy**
- **2026-07-12**
- **Phishing**
- **A deconstruction and analysis of three example phishing emails**
