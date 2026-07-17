---
title: Designing the Cloud and Cloud Models
date: 2026-06-02
tags: [networking, cloud, vpc]
summary: How cloud environments virtualise physical network infrastructure, VPC concepts, and the three cloud service models.
---

# Designing the Cloud and Cloud Models

The cloud offers on-demand computing power that can scale up and down, even for individual applications.

## Virtual networks

Scenario: a server farm with 100 physical servers, all connected via switches and routers with redundancy. Migrating all 100 physical machines onto one large physical server in the cloud, then creating 100 virtual servers inside — what happens to the network? All the physical network devices can be replaced with virtual versions offering the same functionality, all managed from the hypervisor. This creates far more flexibility.

## VPC (Virtual Private Cloud)

A pool of resources created in a public cloud, all connected by a transit gateway. VPCs sit on different IP subnets and require a VPN to connect to the cloud.

A VPN offers site-to-site connectivity through the internet. But to make an instance or application available to anyone on the internet, you need a VPC Gateway (Internet Gateway).

A VPC NAT allows private cloud subnets to connect to and use external resources, but does not allow external resources to access the private cloud.

VPCs often come with additional security, including security groups and access lists — these act as a firewall for the cloud.

## Cloud models

- **Public** — available to anyone over the internet.
- **Private** — for internal use only; your own virtualised local data centre.
- **Hybrid** — a mix of both.

## Service models

- **SaaS** (Software as a Service) — no local install, everything is handled by the provider. Centralised management of data and apps. Google Mail and Office 365 are examples — just log in and use.
- **IaaS** (Infrastructure as a Service) — only the cloud hardware is provided; you install and manage your own software. You handle upgrades and security. Your data is still in the cloud, but you retain greater control over it.
- **PaaS** (Platform as a Service) — a middle ground: no servers, software maintenance, or HVAC to manage, but you still handle development.

![Cloud service models — SaaS, PaaS, IaaS responsibility split](/static/images/notes/networking/cloud-service-models.png)
