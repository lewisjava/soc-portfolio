---
title: Firewall Fundamentals
date: 2026-06-20
tags: [firewall, iptables, ufw]
summary: The four firewall types, rule anatomy, and practical Linux firewall commands using ufw.
---

# Firewall Fundamentals

The security guard of networks — making sure no one sneaks in who isn't permitted, or sneaks out with something they shouldn't. A firewall inspects a network or device's incoming and outgoing traffic.

## Types of firewalls

- **Stateless** — operates at layers 3 and 4 of the OSI model. Filters data based on predetermined rules without tracking the state of previous connections, so it processes packets quickly but doesn't verify the connection is legitimate.
- **Stateful** — goes beyond packet filtering, keeping track of previous connections in a state table. This adds a layer of security, since it can block or accept packets based on whether the connection has already been established.
- **Proxy** — operates at layer 7, able to inspect the actual content of packets.
- **Next-gen** — the most advanced, operating from layer 3 to layer 7. Offers deep packet inspection and other functionality.

## Rules in a firewall

A firewall rule's basic components:

- **Source address** — the IP address originating the traffic.
- **Destination address** — the IP address receiving the data.
- **Port** — the port number for the traffic.
- **Protocol** — the protocol used during communication.
- **Action** — the action taken when matching traffic is identified.
- **Direction** — whether the rule applies to incoming or outgoing traffic.

**Types of actions:**

| Action | Source | Destination | Protocol | Port | Direction |
|---|---|---|---|---|---|
| Allow | 192.168.1.0/24 | Any | TCP | 80 | Outbound |
| Deny | Any | 192.168.1.0/24 | TCP | 22 | Inbound |
| Forward | Any | 192.168.1.8 | TCP | 80 | Inbound |

- The **Allow** rule permits all outgoing traffic from the network on port 80.
- The **Deny** rule blocks all incoming traffic on port 22.
- The **Forward** rule forwards all incoming traffic on port 80 to the web server at 192.168.1.8.

Firewall rules are directional — inbound or outbound.

## Linux iptables firewall

**Netfilter** is the framework inside the Linux OS with firewall functionality, acting as the foundation for various firewall utilities such as `iptables`, `nftables`, and `firewalld`.

**ufw** (Uncomplicated Firewall) provides a beginner-friendly interface for easy rule creation:

```
sudo ufw status                                    # provides the status of the firewall
sudo ufw enable / disable                           # turns it on or off
sudo ufw default allow/deny outgoing/incoming        # sets the default policy for traffic
sudo ufw deny 22/tcp                                 # blocks all incoming SSH traffic
sudo ufw status numbered                             # lists all active rules
sudo ufw delete 2                                    # deletes rule 2 from the active rules list
```
