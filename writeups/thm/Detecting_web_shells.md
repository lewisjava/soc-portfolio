---
title: Detecting web shells
platform: TryHackMe
difficulty: easy
date: 2026-07-22
tags: [Web security]
summary: A write up of the tools and methods used to detect web shells
---

# Detecting web shells
Web shells are a common technique (T1505.003) used by attackers to gina a foothold on target systems and maintain persistence. Web shells provide remote access, enabling various actions later in the attack chain making knowing how to detect them an essential skill for any security professional. For an attacker to upload and execute a web shell they must first exploit a file upload vulnerability. miconfig or have prior access to the system.

Examples:

- Hafnium (G0125) a likely state-sponsored cyber espionage group uploaded .aspx web shells to Windows Exchange servers in directories such as \inetpub\wwwroot\aspnet_client\. Once deployed Hafnium continues on to execute commands, perform recon, dump credentials and further establish persistence through new user account.

- Conti (S0575) is a Ransomware-as-a-service used by threat actors that abused a similar vulnerability in Microsoft Exchange allowing them to upload an aspnetclient_log.aspx file to the same directorry as Hafnium. Within minutes of the web shell upload, they upload a backup web shell and map out the network's computers, domain, controllers and domain admins.

## Log-Based Detection
Since web shells rely on the abuse of web servers, web server logs will naturally be the first place to find evidence of compromise.
- Repeated GET requests in quick succession, probing for a valid place to upload a shell
- POSTS requests to a valid upload location following the repeated GET requests
- Repeated GET or POSTS requests to the same file could indicate web shell interaction

|Requests method|Possible abuse case|
|---------------|-------------------|
|GET|Used for recon or interacting with a web shell|
|POST|Upload or interact with web shell|
|PUT|Upload a web shell|
|DELETE|Cleanup methods|
|OPTIONS|Recon|
|HEAD|Detect files|

Suspicious user-agents and IP addresess are indicators of attack as well as query strings (example.php?query=somequery) especially ones that contain keywords like cmd= or exec=. A missing refer could also ptentially indicate web shell activity.

Auditd is a native linux utility that tracks adn records events which allows allows rules to be created for it. By combining web access and error logs with auditd more insight will be provided to confirm if a file was created, modified or executed by which user and process.

SIEM platforms also offer centralized log collection and correlation, the creation of targeted queries to uncover malicious activity and allows for easier searching and analysis of logs.

## Beyond logs

### File system analysis
Since attackers have to upload their web shell it has to be stored somewhere. Analyzing web server files becomes essential in identifying uploaded web shells or locating filed modified to include a web shell payload.

Common web server directories where web shells are uploaded:
- Apache: /var/www/html/
- Nginx: /usr/share/nginx/html/

commands like find can be used to search for recently modified scripts:
- find /var/www -type f -name "\*.php" -newerct "2025-07-01" ! -newerct "2025-08-01"

Grep can also be used to track down suspicious functions like eval( within fies:
grep -r "eval(" wp-content

### Network traffic analysis
Inspecting packet payloads allows deeper analysis than log analysis provides and also has the same indicators as log analysis:
- Unusual HTTP methods and requests patterns
- Suspicious user-agents and IP addresses
- Encoded payloads
- Malicious code or commands in Request bodies
- Unexpected protocols or ports
- Unexpected Resource usage
- Web server rocesses spawning command line tools

## Investigation
In this investigation I've been provided the access and error logs for an apache server and tasked to find evidence of a web shell.

**Which IP address likely belongs to the attacker**
I start the investigation by using grep .php access.logs to look for any evidence of .php extensions in the file which would be suspicious and it returns shadyshell.php in the /wordpress/wp-content/uploads directory, it also includes the attackers ip.
![webshellphp](/static/images/webshellphp.png)

**what is the first directory the attacker successfully identifies**
This is answered in the previous question and is /wordpress

**What is the name of the .php file the attacker uses to upload to the web shell?**
Also answered with the first questions command but is located higher up in the response where upload_form.php is found and likely to be the .php file the attacker used to upload the web shell.
![uploadform](/static/images/uploadform.png)

**what is the first command run by the attacker**
using the command grep shadyshell access.logs shows all the interactions the attacker has with the web shell where the command whoami can be seen as the first one ran
![whoami](/static/images/whoami.png)

**after gaining access via the web shell, the attacker uses a command to download a second file onto the server what is the name of this file**
This is answered in the previous question but i also used the command grep cmd= access.logs to see all the commands executed by the attacker where it can be seen they use wget to download linpese.sh

**the attacker has hidden a secret within the web shell. Use cat to investigate the web shell code and find the flag** 
this requires to navigating where the shadyshell web shell is uploaded and using cat on the .php file to read the output
![webshellflag](/static/images/webshellflag.png)


## In conclusion
In this writeup I covered how to detect web shells through log, file system, network and behavioural analysis using a combination of native OS utilites and specialized security tools. By working through log samples and a simulated attack scenario I demonstrated how web shells behave and how to uncover them using real world indicators.

---
- **Web shell detection**
- **TryHackMe**
- **Easy**
- **2026-07-22**
- **Web security**
- **A write up of how web shells work and how to detect them using log, network and behaviora analysis**
