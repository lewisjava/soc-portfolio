---
title: Phishing - Fundamentals
platform: TryHackMe
difficulty: easy
date: 2026-07-12
tags: [Phishing]
summary: A write up of the fundamentals to phishing
---

# Phishing

Phishing and it's many variants remains today one of the most common social engineering threats faced by organisations, with over 90% of all succesfull cyber attacks and data breaches starting with a phishing email. This makes understanding phishing a key area for SOC analysts.

## The Email address
Every investigation of a phishing email will start with the address. The anatomy of which is as afollows "username" "@" "domain.com", the username is the mailbox of the specific recepients mailbox on the email server, the @ symbol seperates the username from the domain name and the domain name specifies the mail server responsible for receiving the message.

example: lewis@companyname.com
The user would be lewis and the domain the user is in would be companyname

## Mail delivery
When mail is sent several protocols work to deliver the message to the recipient from the sender.

1. SMTP (simple mail transfer protocol): Sends emails
2. POP3 (post office protocol): Downloads emails to a device
3. IMAP (internet message access protocl): Syncs emails across devices.

## Email headers
This is where the contents of an email contains when it arives in an inbox, this is important when analyzing potentially malicious emails. An email consists of two parts:

1. Email header: Contains metadata about the message.
2. Email body: This part contains the actual message content, displayed either as plain text or HTML.
![Email header part 1](/static/images/emailheader1.png)
![Email header part 2](/static/images/emailheader2.png)

With the use of viewing message source in the example screenshots above we can get some useful data from the email header including such as the source ip address listed as X-Originating-Ip

## Email Body
This is where the message is contained. Emails are sent as text or formatted in HTML. HTML supports elements such as images, links and styling with most email clients showing the rendered content. An SOC analyst can also inspect the source to see how the message is structured allowing the to spot embedded elements and look for signs of phishing or malicious content.

![Body HTML](/static/images/bodyhtml.png)
In the above screenshot we can see the rendered HTML (which often gets blocked as can be seen) vs the raw HTML. by viewing the raw HTML you get a look at how the elements are structured and to be able to see links, images and other embedded content.

## Types of phishing
Now with the understanding of the system it can be understood how attackers abuse this system. There are many techniques used by attackers when it comes to malicious emails, all of these fall under the MITRE technique T1566

|Method|Description|
|------|-----------|
|Spam|Unsolicited bulk emails sent to a wide array of recipients.|
|Phishing|Emails that impersonae a trusted entity to trick recipients into revealing sensitive information.|
|Spear phishing|A targeted form of phishing that is aimed at a specific individual or organization using personalised information|
|Whaling|A type of spear phishing that targets higher leveled executives such as CEO/DFO to obtain sensitive data or financial access.|
|Smishing|Phishing attacks conducted through SMS/text messages targeting users on mobile devices|
|Vishing|Phishing attacks conduced through voice coils where attackers use social engineering over tthe phone|

In the above table we cover the common types of phishing used which falls under the STEALTH tactic in the mitre framework and utilises the social engineering techniques (T1684) phishing (T1566). Spear phishing also conains many sub techniques such as Spearphishing voice (T1566.004). 

Next are the common characteristics of phishing emails:

- Spoofed from address: This is where the senders email is spoofed to appear as a trusted entity (noreply@microsof.com) in this example we can see the email attempts to look like an official Microsoft email but is just missing the t of the end. If someone did not proofread the email address properly and skimmed it, this might trick them.
- Urgent subject or message: Sometimes an attacker will attempt to create a sense of urgency within the email imporing the reader to take immediate action evoking a sense of anxiety or panic that might cause the reader to not think properly and take immediate action, such an example might be "Your account will be locked unless you click this link and change your details"
- Brand impersonation: The email is designed to mimic legitimate orgs using their logos, branding, style of typing and embedding.
- Grammar and spelling issues: The message may also contain errors, though AI has made this issue much less common.
- Generic content: The message may lack any sort of personalization such as Dear Customer instead of your acutal name.
- Hidden or Shortened Links: Hyperlinks may dsiguise their true destination (Example link: bit.ly/secure-login), if this were a spearphishing attempt this would fall under the mitre sub-technique T1566.002.
- Malicious Attachments: Attachments are included and disguised as legitimate files (Example file: invoice.pdf.exe) If this were a spearphishing attempt this would fall under the mitre sub-technique T1566.001.

When dealing with links they should be defanged to prevent accidental clicking of them.

## Conclusion

Since phishing is the primary method used for intial access accounting for 15.44% of all incidents - D3 security, 2026, It is important to understand how emails work and how attackers abuse these systems and the techniques they use to do so.


---

- **Phishing - Fundamentals**
- **TryHackMe**
- **Easy**
- **2026-07-12**
- **Phishing**
- **Understanding the fundamentals behind emails and how they are abused**
