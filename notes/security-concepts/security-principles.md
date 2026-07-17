---
title: Security Principles
date: 2026-06-26
tags: [cia-triad, security-models, zero-trust, defense-in-depth]
summary: The CIA triad and beyond, classic security models (Bell-LaPadula, Biba, Clark-Wilson), defence in depth, and zero trust vs trust-but-verify.
---

# Security Principles

## The CIA triad

- **Confidentiality** — ensuring everything is encrypted and secure, so no one unauthorised can access it.
- **Integrity** — ensuring data is what it's supposed to be (hashing, etc.).
- **Availability** — ensuring data/systems are always available when needed, preventing DoS/DDoS.

## Beyond CIA

Two more elements worth adding: **Authenticity** (ensuring nothing is fake or counterfeit — that data really is from the claimed source) and **Non-repudiation** (the original source of something cannot deny they are the direct source of a particular document/file/data).

In 1998, Donn Parker proposed the **Parkerian Hexad**: Availability, Utility, Integrity, Authenticity, Confidentiality, Possession.

Of these, two aren't covered by CIA: **Utility** (the usefulness of information — e.g. a user loses a decryption key to their laptop; the information is still there but currently useless) and **Possession** (protecting information from unauthorised taking, copying, or controlling).

## DAD

**Disclosure, Alteration, Destruction/Denial** — a framework detailing three ways a system can be attacked, essentially the inverse of CIA:

- **Disclosure** — the opposite of confidentiality; private information disclosed to the public.
- **Alteration** — the opposite of integrity; data has been tampered with or altered.
- **Destruction/Denial** — the opposite of availability; data is destroyed or a service is shut down.

## Security models

Security models ensure a system achieves the functions of the CIA triad.

**Bell-LaPadula Model** — aims to achieve confidentiality via three rules:

- *Simple security property* — no read up: a subject at a lower security level cannot read an object at a higher level.
- *Star security property* — no write down: a subject at a higher security level cannot write to an object at a lower level.
- *Discretionary-security property* — uses an access matrix to allow read/write operations.

Limitation: not designed to handle file sharing.

**Biba Model** — aims to achieve integrity via two rules:

- *Simple integrity property* — no read down: a higher-integrity subject should not read from a lower-integrity object.
- *Star integrity property* — no write up: a lower-integrity subject should not write to a higher-integrity object.

Limitation: cannot handle internal threats.

**Clark-Wilson Model** — aims to achieve integrity through:

- **Constrained Data Item (CDI)** — the data type whose integrity is being preserved.
- **Unconstrained Data Item (UDI)** — all data beyond CDI, such as user/system input.
- **Transformation Procedures (TPs)** — programmed operations (read/write) that maintain CDI integrity.
- **Integrity Verification Procedures (IVPs)** — procedures that check and ensure CDI validity.

Other models exist too: Brewer and Nash, Goguen-Meseguer, Sutherland, Graham-Denning.

## Defence in depth

Creating a security system composed of various systems and layers — also known as multi-level security.

## ISO/IEC 19249

Lists five architectural and five design principles for secure systems.

**Architectural principles:**

- **Domain separation** — related components grouped as a single entity with common security attributes (e.g. x86 privilege rings: OS kernel runs in ring 0, user-mode apps in ring 3).
- **Layering** — each OSI layer provides specific services to the layer above, making it possible to impose security policies and validate correct operation.
- **Encapsulation** — hiding low-level implementation and preventing direct manipulation of an object's data, exposing only specific methods (mirrors OOP design).
- **Redundancy** — ensures availability and integrity, e.g. dual power supplies, RAID 5 configurations.
- **Virtualisation** — sharing a single set of hardware among multiple operating systems, providing sandboxing that improves security boundaries.

**Design principles:**

- **Least privilege** — give the absolute minimum privilege required for someone to complete their task.
- **Attack surface minimisation** — reducing vulnerabilities, e.g. hardening a Linux system by disabling unnecessary services.
- **Centralised parameter validation** — validating input centrally to prevent exploitation via invalid input.
- **Centralised security services** — e.g. a centralised authentication server.
- **Preparing for error and exception handling** — systems should fail safe (e.g. a crashed firewall should block all traffic, not allow all), and error messages shouldn't leak confidential information.

## Zero trust vs trust but verify

**Trust but Verify** — always verify, even when you trust an entity. Verifying requires proper logging, then reviewing logs to confirm normal behaviour. In practice, it's not feasible to verify everything manually, which is why automated mechanisms (proxies, IDS, IPS) are needed.

**Zero Trust** — treats trust itself as a vulnerability and works to eliminate it: "never trust, always verify." Every entity is considered adversarial until proven otherwise, regardless of location or ownership. Authentication and authorisation are required before accessing any resource, containing the damage of any breach.

**Microsegmentation** is one implementation of Zero Trust — a network segment can be as small as a single host, and communication between segments requires authentication and access control checks.
