---
title: SSH Key Authentication
date: 2026-06-08
tags: [ssh, authentication, key-based-auth]
summary: How SSH key pairs and fingerprint verification work, key generation, and correct private key permissions.
---

# SSH Key Authentication

When connecting, an SSH client confirms whether it recognises the server's public key fingerprint. **ED25519** is a public-key algorithm used for digital signature generation and verification, and a common modern alternative to RSA for SSH keys.

SSH keys default to RSA, but the algorithm can be chosen. `ssh-keygen` is the program used to generate key pairs:

```shell-session
ssh-keygen
[...]
-t dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa
Specifies the type of key to create.
```

## Key protection and usage

Private keys can be protected with a passphrase.

Permissions must be set correctly to use a private key — otherwise the client will ignore the file with a warning. Only the owner should be able to read or write to the private key (`600` or stricter):

```shell-session
ssh -i privateKeyFileName user@host
```

This specifies a key for the standard Linux OpenSSH client.

## Detection relevance

Recognising legitimate SSH key-based authentication patterns matters for a SOC analyst — an unexpected key added to a user's `authorized_keys` file, or SSH key usage from an unfamiliar source, is a persistence indicator worth investigating. Weak passphrase-protected private keys can also be brute-forced offline if an attacker gains access to the key file itself, similar to password cracking against a hash.
