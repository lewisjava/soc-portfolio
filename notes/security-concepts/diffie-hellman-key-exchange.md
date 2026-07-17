---
title: Diffie-Hellman Key Exchange
date: 2026-06-08
tags: [cryptography, key-exchange, asymmetric]
summary: How two parties establish a shared secret over an insecure channel without ever transmitting the secret itself, worked through numerically.
---

# Diffie-Hellman Key Exchange

Key exchange aims to establish a shared secret between two parties.

Consider a scenario: Alice and Bob want to talk securely. They want to establish a shared key for symmetric cryptography but don't want to use asymmetric cryptography for the exchange itself — this is where Diffie-Hellman comes in.

Alice and Bob each generate secrets independently — call these A and B. They also share some public common material, C. Two assumptions: combined secrets are practically impossible to separate, and the order in which they're combined doesn't matter.

Alice and Bob combine their secrets with the common material to form AC and BC, send these to each other, then combine the received part with their own secret to arrive at two identical keys — both end up with ABC. This shared key can then be used to communicate.

## Worked example

(Note: `()` denotes "to the power of" below.)

1. Alice and Bob agree on **public variables**: a large prime number *p* and a generator *g*, where 0 < *g* < *p*. These are disclosed publicly over the channel. For simplicity (though insecurely small in practice): *p* = 29, *g* = 3.
2. Each chooses a **private integer**. Alice chooses *a* = 13, Bob chooses *b* = 15. Neither value is disclosed.
3. Each calculates their **public key**: Alice computes *A* = g(a) mod p = 3(13) mod 29 = 19. Bob computes *B* = g(b) mod p = 3(15) mod 29 = 26.
4. They exchange public keys — Bob receives Alice's *A* = 19, Alice receives Bob's *B* = 26. This step is the **key exchange**.
5. Each calculates the **shared secret** using the received public key and their own private key. Alice computes B(a) mod p = 26(13) mod 29 = 10. Bob computes A(b) mod p = 19(15) mod 29 = 10. Both arrive at the same result — g(ab) mod p = 10 — the shared secret key, without either the secret or the shared key ever being transmitted directly.
