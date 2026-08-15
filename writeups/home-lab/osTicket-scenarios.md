---
title: osTicket Scenarios
platform: Home Lab
difficulty:
date: 2026-08-14
tags: [Home Lab, Support analyst, osTicket]
summary: A sample of common tickets and their workflow.
---

# osTicket scenarios

## T-10001 - Account locked out after password change
For this scenario I set the lockout threshold in the domain GPO to 5 to trigger an event lockout for one of my created users (Mitch)
![homelabticket1](/static/images/homelabticket1.png)

User then creates a ticket explaining that they are locked out of their account
![homelabticket2](/static/images/homelabticket2.png)

After investigating the security logs on the domain controller I can verify that the user is in fact logged out
![homelabticket3](/static/images/homelabticket3.png)

After this I respond to the user, give them a temporary log in password after resetting their password as well as forcing a password change when logging back into the account
![homelabticket4](/static/images/homelabticket5.png)
![homelabticket6](/static/images/homelabticket6.png)

After confirming the user is logged in successfully and has regained access to their account I can document the incident and close the ticket.
![homelabticket7](/static/images/homelabticket7.png)
![homelabticket8](/static/images/homelabticket8.png)


## T-1002 - New starter setup / provisioning
New starter requiring an account set up and adding to the right OU, Security groups and relevant GPOs applied.

Ticket from line manager
![homelabticket9](/static/images/homelabticket9.png)

User is created and then added to their relevant security group
![Homelabticket10](/static/images/homelabticket10.png)

Login to the new users account and ensure everything is set up properly and that the GPO applies.
![homelabticket11](/static/images/homelabticket11.png)

New user account is set up and ready.

## T-1003 VPN won't connect

---

- **osTicket scenarios**
- **Home Lab**
- **2026-08-14**
- **Support analyst, ticketing, IT**
- **A write up demonstrating ticket workflow in an enterprise environment**
