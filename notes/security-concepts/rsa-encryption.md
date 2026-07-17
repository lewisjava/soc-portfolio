---
title: RSA Encryption
date: 2026-06-08
tags: [cryptography, rsa, asymmetric, public-key]
summary: How RSA's factoring problem underpins asymmetric encryption, worked through with a numerical example.
---

# RSA Encryption

RSA is based on factoring a large number, which requires a massive amount of processing power to reverse without the private key.

## The algorithm, worked through

1. Bob chooses two prime numbers: *p* = 157 and *q* = 199. He calculates *n* = *p* × *q* = 31243.
2. With φ(*n*) = *n* − *p* − *q* + 1 = 31243 − 157 − 199 + 1 = 30888, Bob selects *e* = 163 such that *e* is relatively prime to φ(*n*). He also selects *d* = 379, where *e* × *d* ≡ 1 mod φ(*n*) — i.e. 163 × 379 = 61777, and 61777 mod 30888 = 1. The **public key** is (*n*, *e*) = (31243, 163). The **private key** is (*n*, *d*) = (31243, 379).
3. To encrypt a value *x* = 13, Alice calculates *y* = x^e mod n = 13^163 mod 31243 = 16341, and sends *y*.
4. Bob decrypts by calculating *x* = y^d mod n = 16341^379 mod 31243 = 13 — recovering the original value Alice sent.

## Key variables to know

- *p* and *q* — large prime numbers
- *n* — the product of *p* and *q*
- The **public key** is (*n*, *e*)
- The **private key** is (*n*, *d*)
- *m* — the original message (plaintext)
- *c* — the encrypted message (ciphertext)
