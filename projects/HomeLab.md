---
title: Home SIEM Deployment — With Wazuh
status: in-progress
date: 2026-08-05
tags: [siem, home-lab, Wazuh]
tech: [Security Onion, Sysmon, VirtualBox, Atomic red team]
github: https://github.com/LewisJava/home-siem
summary: 
---

# Home SIEM Deployment — Security Onion

## Overview

What is this project, and why did you build it? What does it demonstrate about your skills?

## Architecture

Describe the setup — VMs, network layout, what talks to what. A diagram image is ideal here:

![Architecture diagram](/static/images/projects/home-siem/architecture.png)

## Build process
### Windows server/Domain controller
To start the build I went around and downloaded the relevent ISOs (Windows host, Windows server, Kali Linux) to emulate an organisational environment
![homelab!](/static/images/homelab1.png)

After getting the ISO's the next step was to get everything installed starting with Windows Server which required a manual install as VM's easy install feature creates an unattended answer file that fails to match the image index inside the windows server ISO
![homelab2](/static/images/homelab2.png)

After the install the windows server was set up and ready to be configured

![homelab3](/static/images/homelab3.png)

The first thing was to configure the network and make the domain controller's DNS point to itself.

![homelab4](/static/images/homelab4.png)

After this point I went back and installed the GUI version as this made the next steps much easier, as the next step was to install active directory domain services and DNS.
![homelab5](/static/images/homelab5.png)

The next and final step was to promote the Domain controller
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

The next step on the server now was to build the directory structure using Active Directory Users and Computers.

Here I created OUs that mirror real orgs - HQ > Departments > IT / Finance / HR / Sales plus workstations, Servers and Groups and added users to them.
![homelab10](/static/images/homelab10.png)

I also created security groups and added the relevant users to their security groups
![homelab11](/static/images/homelab11.png)

Then I created specific group policies for the specific groups such as allowing audit process creation for helpdesk staff, password/lockout policy for security.
![homelab12](/static/images/homelab12.png)

### Windows/Host machine
Next is to install the host machine.
![homelab5](/static/images/homelab5.png)


After the machine was successfully installed, I then set to getting it joined to the network as a client, setting it's IP, subnetmask, and setting it's DNS to the domain controllers IP
![homelab13](/static/images/homelab13.png)

Next I wanted to add the workstation to the domain and it was at this point I realised I was on the home edition so had to download the Enterprise edition and repeat the steps up to this point. Either way once here I got the endpoint set up installed and joined to the domain.
![homelab14](/static/images/homelab14.png)

For the on-prem active directory I had to set up a domain controller and a workstation, create/disable users, reset passwords, manage group memberships, push a GPO, and log into a domain-joined client. 

### SIEM
The next installation in my home lab was a SIEM, for this I chose Wazuh because of it's lower RAM requirements.
![homelab15](/static/images/homelab15.png)

The next step was to install Wazuh onto the Ubuntu host
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

## Detections / results

After getting both endpoints connected to Wazuh I downloaded Sysmon loggin from windows and downladed a config for it from github (SwiftOnSecurity) and started feeding the Syslog events into Wazuh where they started to appear after I successfully set it all up
![homelab21](/static/images/homelab21.png)


## What I learned
From start to finish I learned a lot.

1. Installing and configuring the endpoints, both the work station and DC were rather easy to set up and configure as there is plenty of offical Microsoft documentation to follow.

2. Setting up the network was the next step, manually assigning the IPv4 address to the machines and the subnet mask so that they can communicate to each other across a host only network. Later on I stumbled into an issue when I tried to download the wazuh packages as it was failing even though I could ping the DNS forwarder and nslookup the packages from the endpoints, it was until trying many fixes that I realised the NAT had not been set up on both machines so they could not download it.


---

## Frontmatter field reference (delete this section before publishing)

- **status** — `complete`, `in-progress`, or `planned`. Shows as a coloured badge.
- **tech** — comma-separated list in brackets, e.g. `[Splunk, Sysmon, VirtualBox]`. Shows as tags, separate from `tags`.
- **github** — link to the project's repo, if you have one. Shows as a button on the project page.
- Everything else (title, date, tags, summary) works the same as write-ups and notes.
