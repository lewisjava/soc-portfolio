---
title: File and hash threat intel
platform: TryHackMe
difficulty: easy
date: 2026-08-01
tags: [Threat analysis, hashes, files]
summary: A write up on enriching file and hash artefacts
---

# File and hash threat intel
SOC teams live inside alert quees adn triaging, every entry follows three essential steps:
1. Verify
2. Enrich
3. Decide

File and hash intelligence sits in the enrich phase.


## Filenames and Paths
When encoutering suspicious files getting as much context as possible is essenital. Human-readable strings, such as filepaths is one of the earilest heuristics available, while not able to prove maliciousness they can reveal attacker tradecraft patterns.

### File path analysis
These are great for revealing attacker behaviours:

- C:\ drive is a common target for persistence mechanism
- C:\Users\Public profile can enable cross-iuser access of detonated adversary tools
- C:\Users\Public\Public Downloads provides a high-traffic directory that would often evade strict monitoring

Adversaries may also utlise other malware staging patterns:

- C:\Windows\Temp\ for ephemeral payloads
- C:\ProgramData\ for stealth persistance

### Filename Heuristic indicators
Attackers have are also known to modify filenames to escape detection through implementing carious types of heuristic indicators, including:

- Double extensions - example.pdf.exe
- System binary impersonation - files such as scvhost.exe (defenders should include legitimate locations for system processes in an allowlists, rather than standalone filenames)
- High-entropy Strings - filenames such as jh8F21.exe suggest automated packing or polymorphic generations, used in a high-churn phishing operation
- Masquerading - filenames such as backup-2300.exe can blend with routine files.

### Exercises

**One of the files included in the CTI files folder on the Desktop shows on of the indicators mentioned. Can you identify the file name and the indicator**
Heading into the folder the first thing I did was check the box that shows file extensions and it instantly made the answer to the question stand out where one of the files had a double extension (T1036.007)
![cti1](/static/images/cti1.png)

## File Hash lookup
Next names can be tied back to the same binary through cryptographic fingerpirinting through a files hash.

When dealing with hashes:
- Store hashes in lowercase to avoid needless differences
- Hash what matters, if a binary resides in a ZIP file, hash both.
- Do not leave plain strings without the context of where and when you encountered them
- Any byte change will change the resulting hash

Analysis with virustotal:
With a file hash it can be searched on VirusTotal, with a few things work taking note of when submitted:

- Detection score: this represents a crowdsourced security verdict from various vendors displayed as a ratio, the higher the number the higher the confidence threat.
- Threat labels and categories: These are vendor-specific classifications of threats that help confimr their attribution across vendors
- Detection rules: These are the technical signatures used by AV engines to ID threats. yara rules, Heuristic patterns and behavioural triggers.
- Properties: The metadata of the files; file type, size and compilation timestamp
- Contained domains and IPs: This info covers the malware's network infrastructure.
- Contained files: this section details any files embedded or dropped during the malware's execution

cross-refrencing with malware bazaar an all-in-one database for malware collection and analysis.

### Exercises
**What is the SHA256 hash of the fie bl0gger**
using cerutil -hashfile bl0gger.exe sha256 gave me the file hash
![cti2](/static/images/cti2.png)

**What is the threat classification label used to id the malicious file**
Using the VMs equialent of VirusTotal I searched the file hash and got the classification label
![cti3](/static/images/cti3.png)

**Whehn was the file first submitted for analysis**
Shown on previous screenshot on right hand side - 2025-05-15 12:03:49

**Which vendor classified the Morse-Code-Analyzer file as non-malicious**
![cti4](/static/images/cti4.png)

**What MITRE technique has been flagged for persistence and privilege escalation for the morse-code-analyzer file**
![cti5](/static/images/cti5.png)

## Sandbox analysis
Hashes, strings and sections tell identity. But impact of malicious files is found by dynamic analysis of them. Sandbox analysis does three things.
- Confirm execution - if nothing happens, alert might be a decoy or malware is avoiding dynamic analysis
- Extract runtime IOCs - domains, mutexes, dropped payloads, feed hunts and detecions
- Map to ATT&CK - Most sandboxex auto-label behaviour with techniuqe IDs fast tracking reports.

Sanboxing tools

- Hybrid analysis
- Joe Sandbox

Sandboxing limitations:

- Sanbox evasion techniques: some payloads are designed to detect and evade sandboxes.
- Limited execution time and coverage: Most sandboxes terminate analysis after 2-5 minutes meaning multi-stage malware may not fully execute.
- Encrypted and obfuscated traffic: many sandboxes cannot decrypt SSL/TLS traffic leading to blind spots which may reuslt in HTTPS C2 traffic appearing with no payload visibility or the malware utlising DNS tunneling to hide data in DNS queries.
- Fileless and liveing off the land malware: some threats never touch disk, bypassing traditional sandbox analysis by employing powershell attacks and WMI persistence

### Threat intelligence challenge
Investigate a suspected file challenge.bin.sample

**what is the SHA256 of the file**
![cti6](/static/images/cti6.png)

**What family labels are asssigned to the file VirusTotal**
![cti7](/static/images/cti7.png)

**When was the first time the file was recorded in the wild**
![cti8](/static/images/cti8.png)

**Name the text file dropped during the execution of the malicious file**
![cti9](/static/images/cti9.png)

**What powershell command is observed to be executed**
![cti10](/static/images/cti10.png)

**What MITRE ATT&CK ID is associated with the actions of the command**
![cti11](/static/images/cti11.png)

## Conclusion
To conclude threat intelligence is integral to a SOC workflow that enriches unknown binaries encountered by threat alerts

Key Takeaways:

> Validate evidence before analysis: confirm you have the exact binaries and hashes

> Analyse filepaths and filenames for quick context: unusual storage locations, trusted software directories, and naming tricks highlight items that warrant deeper review.

> Generate hashes early to pivot into external or internal knowledge bases

> Observe runtime behaviour in a controlled environment to confirm intent, extract network and persistence indicators and map activity to recognised attack techniques

> Translate findings into a brief that lists indicators by type, summarises behaviour and provides proportionate recommendations supported by evidence

---

- **File and hash threat intel**
- **TryHackMe** — optional. Shows as a badge (e.g. TryHackMe, LetsDefend).
- **easy** — optional. One of: easy, medium, hard. Shows as a coloured tag.
- **2026-08-01** — optional but recommended. Format YYYY-MM-DD. Used for sorting.
- **Threat analysis, hashes, files** — optional. Comma-separated list in square brackets.
- **A write up of how to verify, enrich and decide whether a file is malicious through threat intelligence**
