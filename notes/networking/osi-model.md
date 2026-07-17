---
title: The OSI Model
date: 2026-05-31
tags: [networking, osi, fundamentals]
summary: The seven layers of the OSI model and what each is responsible for.
---

# The OSI Model

The OSI model stands for Open Systems Interconnection reference model. It has 7 layers.

Physical (1) → Data Link (2) → Network (3) → Transport (4) → Session (5) → Presentation (6) → Application (7)

An easy way to remember this is with the acronym: **P**lease **D**o **N**ot **T**each **S**tupid **P**eople **A**cronyms.

## The layers

**Physical layer** — uses hardware: cables, signals, connectors. There are no protocols here. When a problem occurs at this layer it may be interference on a wireless network, a faulty cable, or hardware failure.

**Data Link layer** — aka the MAC address layer or the switching layer, the foundation of communication. Each network card has a MAC address, and this is a destination for data.

**Network layer** — aka the routing layer. This is the layer where routers route traffic, using the Internet Protocol. It fragments frames to traverse different networks. Problems here relate to IP addresses and subnetting.

**Transport layer** — the "post office" layer. Uses TCP and UDP. Parcels large data into smaller pieces and reassembles them at the destination.

**Session layer** — communication management layer. Allows communications to start, stop, or restart, using control and tunneling protocols.

**Presentation layer** — character encoding. Translates data into a readable format for human eyes — the step just prior to a human actually seeing the data.

**Application layer** — the final layer, the one we actually see on our screen, whether that's emails, video, HTTP, FTP, DNS, or POP3.
