---
title: Networking Devices and Functions
date: 2026-05-31
tags: [networking, devices, infrastructure]
summary: Core networking hardware — routers, switches, firewalls, load balancers, proxies — and the key network functions that tie them together.
---

# Networking Devices and Functions

## Devices

**Router** — the most common device, routes traffic from one IP subnet to another. An OSI layer 3 device (a switch is the layer 2 equivalent). Connects diverse networks, LAN to WAN. Can use copper, fibre, and more.

**Switch** — operates at the MAC layer, using MAC addresses to send data from one device to another. Comes with many ports and features, such as PoE (Power over Ethernet).

**Firewall** — filters traffic by port number or application and allows management of allowed ports and apps. Firewalls also encrypt traffic via VPN between sites, creating a tunnel between firewalls. Can also act as a layer 3 device using dynamic routing and network address translation (NAT).

**IDS / IPS** — Intrusion Detection System and Intrusion Prevention System. Although often integrated into next-gen firewalls, they can be standalone devices. An IPS both detects and prevents intrusions, while an IDS only detects and alerts.

**Load balancer** — distributes load across multiple servers to prevent a single server from being overloaded and crashing. Also identifies outages on servers and takes them out of rotation. Load balancers also provide encryption/decryption (taking that load off the servers), cache data for faster response, and use prioritisation (Quality of Service).

**Proxy** — sits between the user and the external network. Receives the user's requests and performs them on their behalf, receives the response on their behalf, verifies the response is safe before it enters the network, and sends it back to the user. Also useful for caching, access control, URL filtering, and content scanning.

**NAS vs SAN** — Network Attached Storage connects to a shared storage device across the network (file-level access). Storage Area Network looks and feels like a local storage device (block-level access) — very efficient reading and writing.

**Access point** — a bridge that extends the wired network onto the wireless network. This is a layer 2 device.

**Wireless LAN controller** — a hub for all access points across a network, providing centralised management. Allows deployment of new APs, performance and security management, configuring and deploying updates to all APs, and reporting on AP usage. Usually a proprietary system.

## Functions

**CDN (Content Delivery Network)** — a network designed to get data from one place to another using geographically distributed caching servers, so users get data from the closest server to them rather than from the original server, which could be across the globe.

**VPN (Virtual Private Network)** — secures private data traversing a public network. Also known as a concentrator or head-end. Encrypts and decrypts data in real time, often integrated into the firewall.

**QoS (Quality of Service)** — a configuration that shapes traffic and packets, controlling bandwidth usage and data rates to prioritise important applications over less important ones.

**TTL (Time to Live)** — prevents an infinite loop. All tasks are given a time to live after which they stop, after a certain number of iterations/hops. For example, a packet caught in a loop will be deleted after a certain number of hops. Routing loops can also occur — if Router A thinks the next hop is Router B and Router B thinks the next hop is Router A, this creates an infinite loop.

**DNS (Domain Name System)** — resolves an IP address from a fully qualified domain name, for example `www.professormesser.com` = `172.67.41.114`. This system allows you to reach an IP address using a domain name instead of the raw address.
