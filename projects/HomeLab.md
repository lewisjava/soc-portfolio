o---
title: Enterprise Security Homelab
status: in-progress
date: 2026-08-05
tags: [siem, home-lab, Wazuh]
tech: [Security Onion, Sysmon, VirtualBox, Atomic red team]
github: https://github.com/LewisJava/home-siem
summary: A virtualised enterprise environment built to simulate IT infrastructure, security monitoring and defensive operations, progressing from Active Directory administration to SIEM detection engineering and attack simulation.

---

# Enterprise Security HomeLab

## Overview

What is this project, and why did you build it? What does it demonstrate about your skills?

## Architecture
ENTERPRISE SECURITY HOMELAB

[Short description]

┌───────────────────────────────────────┐
│         ARCHITECTURE DIAGRAM          │
└───────────────────────────────────────┘

Environment
├── Windows Server 2022 / DC01
├── Windows Endpoint
├── Ubuntu / Wazuh
├── Kali Linux
└── VirtualBox Host-only LAN

Objectives:
- Build a realistic Windows enterprise environment
- Implement Active Directory
- Centralise endpoint telemetry
- Monitor Windows activity with Wazuh/Sysmon
- Simulate adversary behaviour
- Develop and validate detections

## Build process
### Windows server/Domain controller
To start the build I went around and downloaded the relevent ISOs (Windows host, Windows server, Kali Linux) to emulate an organisational environment
![homelab!](/static/images/homelab1.png)
![homelab2](/static/images/homelab2.png)
![homelab3](/static/images/homelab3.png)

After installation was network configuration
![homelab4](/static/images/homelab4.png)

Then AD
![homelab5](/static/images/homelab5.png)

Finally promote the DC
![homelab6](/static/images/homelab6.png)

After rebooting the machine I can see the server has official been set as the domain controller by the new name.
![homelab7](/static/images/homelab7.png)

From here I can now manage network security, authenticate user logins and enfoorce rules for computers on a business network by using Microsoft Active Directory. But first I decided to make sure everything was working correctly by using a few commands in powershell
```
Get-ADDomain
```
Which returns my corp.lab.local domain

```
dcdiag /q
```
Which only returned no serious errors, and a failure for IPv6 as I had not disabled it yet
![homelab9](/static/images/homelab9.png)

```
Get-Service awds,kdc,netlogon,dns
```
which all returned running.

### Active Directory design
The next step on the server now was to build the directory structure using Active Directory Users and Computers.

Here I created OUs that mirror real orgs:
corp.lab.local
│
└── HQ
    ├── IT
    ├── Finance
    ├── HR
    ├── Sales
    ├── Workstations
    ├── Servers
    └── Groups
I choose this structure as it represents what some orgs may look like, allowing me to create users within the groups and apply appropriate and realistic GPOs for the OUs, as well as security policies and controls (Higher for IT and lower for HR, finance, sales etc.)
![homelab10](/static/images/homelab10.png)
![homelab11](/static/images/homelab11.png)
![homelab12](/static/images/homelab12.png)

### Windows/Host machine
Next is to install the host machine.
![homelab5](/static/images/homelab5.png)
![homelab13](/static/images/homelab13.png)
![homelab14](/static/images/homelab14.png)

For the on-prem active directory I had to set up a domain controller and a workstation, create/disable users, reset passwords, manage group memberships, push a GPO, and log into a domain-joined client. 

### SIEM
The next installation in my home lab was a SIEM, for this I chose Wazuh because of it's lower RAM requirements.
![homelab15](/static/images/homelab15.png)
![homelab16](/static/images/homelab16.png)

The next was to update the netplan for the Wazuh host
Before:
![homelab17](/static/images/homelab17.png)
After:
![homelab18](/static/images/homelab18.png)

After installing and setting up Wazuh I went to the dashboard to ensure the set up was done properly using the login details it provided after installation
![homelab19](/static/images/homelab19.png)

From here I can deploy my Domain Controller and windows Endpoint machine here as agents. After installing the Wazuh packages on the endpoints and configuring them they both appeared in my SIEM
![homelab20](/static/images/homelab20.png)

### Attack simulation
Next in my home lab project is setting up the attack simulator using the Atomic Red team tool. First I had to make sure Microsoft Defender would ignore anything coming from Atomic red team or it would quarantine them before they ran stopping alerts from generating.
![homelab22](/static/images/homelab22.png)

Next I installed AtomicRedTeam and set up a snapshot to rollback to after every test.

![homelab23](/static/images/homelab23.png)

Next step is to run the atomic red team test command and check to see if it logs on wazuh!
![homelab24](/static/images/homelab24.png)

### Helpdesk
The next thing I installed a helpdesk machine to communicate with the endpoint. Using another Ubuntu server I pointed it's DNS to the DC to resolve AD names, downloaded the LAMP stack (Linux, Apache, MySQL, and PHP).
![helpdesk1](/static/images/helpdesk1.png)

Confirmation Apache is serving PHP properly via endpoint browser. info.php will be removed after since it exposes environment detail
![helpdesk2](/static/images/helpdesk2.png)

Database layer:
![helpdesk3](/static/images/helpdesk3.png)

Final install with osticket displayed on endpoint
![helpdesk4](/static/images/helpdesk4.png)

Agent login
![helpdesk5](/static/images/helpdesk5.png)

Created departments with relevant Help Topics
![helpdesk6](/static/images/helpdesk6.png)

Ticket created and generated on agent side
![helpdesk7](/static/images/helpdesk7.png)



## Detections / results

After getting both endpoints connected to Wazuh I downloaded Sysmon loggin from windows and downladed a config for it from github (SwiftOnSecurity) and started feeding the Syslog events into Wazuh where they started to appear after I successfully set it all up
![homelab21](/static/images/homelab21.png)

And below it can be seen on the wazuh dashboard!!
![homelab25](/static/images/homelab25.png)

The next step now is to set up and write I wazuh rule so that this process spawns an alert!
![homelab27](/static/images/homelab27.png)

And the rule successfully firing and alerting on the dashboard
![homelab28](/static/images/homelab28.png)


## What I learned
From start to finish I learned a lot.

1. Installing and configuring the endpoints, both the work station and DC were rather easy to set up and configure as there is plenty of offical Microsoft documentation to follow.

2. Setting up the network was the next step, manually assigning the IPv4 address to the machines and the subnet mask so that they can communicate to each other across a host only network. Later on I stumbled into an issue when I tried to download the wazuh packages as it was failing even though I could ping the DNS forwarder and nslookup the packages from the endpoints, it was until trying many fixes that I realised the NAT had not been set up on both machines so they could not download it.

3. After getting the endpoints added to the wazuh manager I had a real issue when I rolled back the Wazuh server where the keys on the manager and keys on the endpoints did not match so a fresh install had to be done on both. Troubleshooting issues like this was a task I seriously underestimated to be challening when setting things up, one such issue was a wazuh agent (the workstation endpoint) would not fail to start so I had to get the -Tail of the ossec.log to see why, it turns out it failed to start due to an error reading the xml file as I had faile to close a line properly using <\>.

4. Getting the security system up and running was not a hassle, getting wazuh set up and the agents deployed was rather easy following instruction, documentation and resources.
---

- **in-progress** — `complete`, `in-progress`, or `planned`. Shows as a coloured badge.
- **Wazuh, windows server 2022, VirtualBox** — comma-separated list in brackets, e.g. `[Splunk, Sysmon, VirtualBox]`. Shows as tags, separate from `tags`.
- **github** — link to the project's repo, if you have one. Shows as a button on the project page.
- Everything else (title, date, tags, summary) works the same as write-ups and notes.
