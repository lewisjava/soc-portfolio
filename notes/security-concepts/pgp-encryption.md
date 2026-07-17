---
title: PGP Encryption
date: 2026-06-08
tags: [cryptography, pgp, gpg, email-security]
summary: Pretty Good Privacy — how it protects email confidentiality and integrity, and the core GPG commands for key generation and message decryption.
---

# PGP Encryption

Pretty Good Privacy (PGP) is commonly used, especially in email, to protect both the confidentiality and integrity of a message.

## Generating a key

```shell-session
gpg --full-gen-key
```

```shell-session
Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection? 9
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)
Key does not expire at all
Is this correct? (y/N) y
```

As with SSH keys, PGP/GPG private keys can be protected with a passphrase.

## Working with keys and messages

```shell-session
gpg --import backup.key                       # import a key from a backup file
gpg --decrypt confidential_message.gpg         # decrypt a message
```

See the [GnuPG manual](https://www.gnupg.org/gph/de/manual/r1023.html) for the full reference.
