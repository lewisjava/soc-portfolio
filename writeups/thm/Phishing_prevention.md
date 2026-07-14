---
title: Phishing - Prevention
platform: TryHackMe
difficulty: easy
date: 2026-07-14
tags: [Phishing, Tools]
summary: A write up of tactics and tools used in the prevention of successful phishing emails.
---

# Prevention
"An ounce of prevention is worth a pound of cure"

## Sender policy framework

### SPF
"Sender policy framework is sued to authenticate the sender of an email, With an SPF record in place, Internet Service Providers can verify that a mail server is authorized to send email for a specific domain, An SPF record is a DNS TCT record containing a list of the IP addresses that are allowed to send email on behalf of you domain" - Dmarcian.

Essentialy the PSF framework is designed to detect the forging of sender addresses during the deliver of emails.

![SPF](/static/images/spf.png)
Following the worflow above when an email is sent the receiving mail server checks the domains SPF record to verify whether the sending server is authorized to send messages on behalf of that domain. based on the result there are three outcomes.

1. Pass, neutral, None = Accept
2. SoftFail, PermError = Flag (mark as suspicious but allow)
3. Fail, TempError = Reject

the syntax of an SPF record is as follows = v=spf1 ip4: 0.0.0.0 include:_spf.google.com

- v=spf1 = Start of the record
- ip4: = specifies which IP can send mail
- Include: = specifies which domain can send mail
- -all = Non-authorized mails will be rejected.

SPF falls under the MITRE D3FEND tactic of harderning specifically the technique Transfer Agent Authentication (D3-TAAN) as it's used to validate server components of messaging infrastructure are authorized to send a particular message.

### SPF tools
SPF Surveyor is a tool from Dmarcian that enables a visual look at DNS records and ensures that records use correct syntax.

Another tool is the Google Admin ToolBox MessageHeader which allows the analysis of delivery details using an email's full header, this shows record results, including spf. 

## DomainKeys Identified Mail (DKIM)

### DKIM
DKIM is defined as "DKIM stands for DomainKeys Identified Mial and is used for the authentication of an email that's being sent. Like SPF, DKIM is an open standard for email authentication that is used for DMARC aignment. A DKIM record exists in the DNS, but it is more complex than PSF. DKIM's advantage is that it can survive forwarding, which makes it superior to SPF and a foundation for securing your email."

It is essential an email security standard designed to make sure messages aren't altered in transit between the sending and recipient servers.

![dkim](/static/images/dkim.png)

An example DKIM record would be as follows: v=DKIM1; k=rsa; p=<public_key>

- v=DKIM1 - specifies the version of DKIM being used
- k=rsa - The key type, RSA encryption algo is standard
- p= - This is the public key that will be matched to the private ey to verify.

Again this is another form of Transfer Agent Authentication (D3-TAAN) as it verifies email servers using a cryptographic signature but it also employs Message Authentication (D3-MAN) as it uses public keys for digital signatures to prevent impersonation.

### Tools
Dmarcian offers two tools for DKIM, a DKIM record Checker and a DKIM record validator.

## Domain-Based Message Authentication, Reporting, and Conformance
### DMARC
"DMARC, an open source standard, uses a concept called alignment to tie the result of two other open source standards, SPF and DKIM, to the content of an email"

Essentialy DMARC is a technical standard that helps protect email senders and recipients from spam, spoofing, and phishing. DMARC ensures the sender's domain matches the domains verified by SPF and DKIM, if this fails DMARC instructs the recipiient server on how to handle the email based on a policy specified in the record.

Example DMARC record: v=DMARC1; p=quarantine; rua=mailto:postmaster@website.com

- v=DMAR1 - The version of DMARC
- p=quarantine - the DMAR policy (in this instance quarantine = move to the spam folder)
- rua=mailto:postmaster@website.com - aggregate reports will be sent to the email specified

DMARC since it checks both SPF and DKIM is another technique that falls under the MITRE D3FEND categories of Transfer agent authentication (D3-TAAN) and message harderning (D3-MH)

### Tools
Another tool offered by Dmarcian is domain checker which inspects DMARC, SPF, an DKIM records. Below is an example results of microsoft.com ran through this tool
![dmarc](/static/images/dmarc.png)

## Secure/Multipurpose Internet Mail Extensions
### S/MIME
S/MIME is a standard protocol for sending digitally signed and encrypted messages, it is based on public key cryptography. the two main components and security features of S/MIME are:

Digital signature - This offers authentication, non-repudiation and data integrity
Encryption - Which offers confidentiality

![smime](/static/images/smime.png)

Unlike the aforementioned protocols, S/MIME falls entirely under the MITRE D3FEND technique of message harderning (D3-MH) as it both uses digital signatures to prove an email came from the correct sender and ensures the text was not changed in transit which is a technique of Message Authentication (D3-MAN) and also scrambles the email contents so only the person with the correct private key can read it which is a technique of Message Encryption (D3-MENCR)

## How orgs prevent phishing
### Tools
Beyond just message authentication, harderning and encryption, organisations eploy a variety mordern solutions to enhance email secuirty and reduce phishing risks

|Solution|how it works|MITRE D3FEND technique|
|--------|------------|----------------------|
|Email filtering|provides filtering based on IP and domain reputation allowing for blocking or quarantining|D3-EF|
|Secure email gateways|Scan messages to detect impersonation attempts, spoofing, and other phishing techniques that other filters may miss|D3-EF, D3-SRA, D3-SMRA,D3-MAN & D3-ER|
|Link Rewriting|Replaces suspicious or unknown URLs with safe, redirected ones, giving the system time to scan and verify the link|D3-CNE, D3-CNS, D3-UA & D3-URA|
|Sandboxing|Isolates and tests suspicious links or attachments in a secure,virtual environment to check for malicious behaviour.|D3-EFA, D3-ABPI, D3-HBPI|

### User-facing Tools and training
Even with the techincal defences above set in place attackers will still find a way for phishing emails to reach users, this is where one of the most important preventitive measures come in place and that is teaching people awareness of phishing emails via visual cues and education this includes:

- Trust and warning indicators: Mordern email platforms display visual cues to help users undersand if a message is safe.
- Phishing reporting: Easy, in-maile reporting options
- User awareness training: Train employees on identifying phishing attempts, social engineering tactics, and safe email practices.
- Phishing simulation exercises: Run controlled phishing campaings to test and reinforce employee training.

## Conclusion
In conclusion phishing is one of the most common and effective technique for an attacker due to this a wide range of tools, techniques and training procedures have been developed and are at the disposal of security specialists, buisnesses and employees to counteract and defend against such attacks.

However even with all these in place phishing still remains the most effective technique for attackers so remain vigilant.

---

- **Phishing - prevention**
- **TryHackMe**
- **Easy**
- **2026-07-14**
- **Phishing, Tools**
- **A guide to the tools, techniques and procedures to preventing phishing emails from success**
