---
title: Wireless Networking, Ethernet Standards and Cabling
date: 2026-06-06
tags: [networking, wireless, ethernet, cabling]
summary: Wireless standards, mobile networking, Ethernet standards, fibre types, copper cabling, connectors, and transceivers.
---

# Wireless Networking, Ethernet Standards and Cabling

## Wireless standards

Managed by the Institute of Electrical and Electronics Engineers (IEEE), under 802.11:

| Standard | Frequency | Speed |
|---|---|---|
| 802.11a | 5 GHz | 6–54 Mbit/s |
| 802.11b | 2.4 GHz | 1–11 Mbit/s |
| 802.11g | 2.4 GHz | 6–54 Mbit/s |
| 802.11n (Wi-Fi 4) | 2.4 & 5 GHz | 72–600 Mbit/s |
| 802.11ac (Wi-Fi 5) | 5 GHz | 433–6933 Mbit/s |
| 802.11ax (Wi-Fi 6 / 6E) | 2.4, 5 & 6 GHz | 574–9608 Mbit/s |
| 802.11be (Wi-Fi 7) | 2.4, 5 & 6 GHz | 1376–46120 Mbit/s |

## Mobile networking

- **4G / LTE** (Long Term Evolution) — 150 Mbit/s download
- **LTE Advanced** — 300 Mbit/s download
- **5G** — 10 Gb/s throughput goal, significant IoT impact

## Satellite networking

Non-terrestrial comms — high cost and complexity, and quite slow (100 Mbit/s down, 5 Mbit/s up). Used for remote sites. High latency (250ms up and down). High frequencies (2 GHz).

## Ethernet standards

Ethernet is the most popular networking technology in the world — universal. Many types of Ethernet exist, differing in speed, cabling, and connectors. Uses either twisted-pair copper or fibre. IEEE 802.3 standards make it universal.

Example standards:

- `1000BASE-T` — gigabit Ethernet, copper, 1 Gbit/s
- `10GBASE-T` — 10 gigabit Ethernet, copper, 10 Gbit/s
- `1000BASE-SX` — gigabit Ethernet, fibre, 1 Gbit/s

Reading the naming convention: number = speed, `BASE` = baseband (opposite of broadband), `T` = twisted-pair copper, `F` = fibre, `SX` = short-wavelength light (also fibre).

## Optical fibre

Transmission by light — very fast. No radiofrequency signal makes it difficult to monitor or tap. Used for long distances since the signal doesn't degrade over distance like RF does. Immune to radio interference.

Two types:

- **Multimode** — short-range comms up to 2km, inexpensive light source like an LED, very large core.
- **Singlemode** — up to 100km distance, uses an expensive light source like a laser, very small core that only allows a single mode of light.

**Fibre connectors:**

- **SC** (Subscriber Connector, aka square/standard connector) — most common. Pushes in then locks with a click, won't slip out.
- **LC** (Local Connector, aka Lucent/little connector) — slightly smaller than SC, also clicks in and locks.
- **ST** (Straight Tip) — uses a bayonet connector, push in and twist to lock.
- **MPO** (Multi-fibre Push On, aka MTP) — twelve fibres in a single connector, saves space and allows easier management. Also locks in like the SC connector.

## Copper cabling

The fundamental medium for network communications. Once cabling is installed it's very difficult to remove and rebuild — plan ahead. All wireless comms eventually need to connect to wired infrastructure.

- **Twisted-pair copper cabling** — two pairs with equal and opposite signals: transmit+/transmit- and receive+/receive-, hence the name.
- **Coaxial cable** — two or more forms share a common axis. RG-6 is used in TV/digital cable and high-speed internet over cable.
- **Twinax** — coax with two conductors, common on 10Gb Ethernet. Installed as part of SFP+ cables, shorter distance, low cost and low latency.

Cables don't have inherent speeds — they just support the signal. The signal encoding determines the transfer rate. Cable standards have categories for the speeds they support — for example, Cat 5 is the minimum that supports `1000BASE-T`.

**Copper connectors:**

- **RJ11** (Registered Jack Type 11) — 6-position, 2-conductor (6 notches but only two copper conductors inside). Used in telephone and DSL connections.
- **RJ45** — 8-position, 8-conductor. Used in typical Ethernet connections.

![RJ45 connector pinout](/static/images/notes/networking/rj45-connector.png)

- **F-connector** — coaxial cable used for cable modems, very outdated.
- **BNC connector** — another coax connector (Bayonet Neill-Concelman). Used with twinax and DS3 WAN links.

## Network transceivers

A transceiver provides a modular interface that plugs into a switch, allowing you to use any kind of media — on one switch you could use both copper and fibre just by plugging in the right transceiver.

Common transceiver types:

- **SFP** (Small Form-factor Pluggable) — commonly used to provide 1 Gbit/s fibre.
- **SFP+** (Enhanced SFP) — same as SFP but much faster, 10 Gbit/s.
- **QSFP** (Quad Channel SFP) — four channels of 1 Gbit/s. QSFP+ is four channels of SFP+.
