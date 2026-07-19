---
title: NetworkMiner
platform: TryHackMe
difficulty: easy
date: 2026-07-19
tags: [NetworkMiner, Tools, Network Analysis]
summary: A brief introduction into the network analysis tool Network Miner
---

# NetWork Miner

Network miner is a tool that is often used in conjuction with Wireshark and while wireshark is a deep level packet analysis tool, NetworkMiner is used to get a quick overview of what is happening on the network as it network forensics analysis tool that, instead of showing raw data, automatically extracts files, images and messages for the analyst making finding sensitive data very easy. 

## Tool overview 1 exercises

**What is the total number of frames**
By going to the case panel right clicking on the case we can bring up the metadata which shows the total number of frames which is 460.
![networkminermetadata](/static/images/networkminermetadata.png)

**How many IP addresses use the same MAC address with host 145.253.2.203**
This simply requires sorting the hosts section under mac addresses then looking inside the host, then inside the mac address to see which and how many IP addresses use the same MAC which is 2.
![mac](/static/images/mac.png)

**how many packets were sent from host 65.208.228.223**
This is found easily by expanding the specific host and looking for the sent field where it states 72 packets were sent.
![packets](/static/images/packets.png)

**what is the name of the webserver banner under host 65.208.228.223**
The answer sits under the host details within the host section and the answer is apache
![banner](/static/images/banner.png)

**What is the extracted username and hash password for the user logged onto 02694W-WIN10 host**
The answer to both here sit under the credentials tab the user is #B/administrator and the NTLM hash is just underneath.
![credentials](/static/images/credentials.png)

## Tool overiew 2 exercises
**What is the linux distro mentioned in the file in frame number 63602**
This required going to the riles tab and filtering for the specific frame and looking inside the file for this frame which showed the distro mentioned was centos
![centos](/static/images/centos.png)

**What name and surname are mentioned in the file associated with frame 76469**
Same as above this file contains the name Ned Flanders
![nedflanders](/static/images/nedflanders.png)

**What is the source address of the image "ads.bmp.2E5F0FD9[1].bmp**
This required searching for the file above which then would provide the details associated with the file.
![bmp](/static/images/bmp.png)

**What is the frame number of the possible TLS anomaly**
This requires going into the anomalies tab and looking for any mention of a TLS anomaly of which there are two but the specific answer is 36255

**Which email sent an email with the subject starting with "You have more..."**
This requires going into the messages tab and filtering with the above starting subject doing thdoing this shows the platform used was facebook
![facebook](/static/images/facebook.png)

**What is the email address of Branson Matheson**
Like above searching for the name in the filter will show all details associated with the keyword, in this case being the username. in this cans eht email is branson@sandsite.org
![sandsite](/static/images/sandsite.png)

## Exercises
**What is the full OS name of the host 131.151.37.122**
Under the host address and under os windows tab the full name windows - windows NT 4 is dounfd
![windowsnt](/static/images/windowsnt.png)

**invetigate the hosts 131.151.37.122 and 131.151.32.91 how many bytes were sent by the client through port 1065**
By expanding the host 131.151.37.122 and expanding the sessions tab within there port 1065 can be found as well as the bytes sent through by the client which is 192
![1065](/static/images/1065.png)

**Investigate the coms between 131.151.37.122 and 131.151.32.21 how many bytes were sent by the server through port 143**
Same as above but instead of looking at the bytes by the client this time it's sent by the server on a different port which sent 20769.
![server](/static/images/server.png)

**What is the sequence number of frame 9**
This requires using version 1.6 of Networkminer and going into the frames tab, expanding frame 9 and expanding the TCP section which gives the sequence number 2ad77400
![frame9](/static/images/frame9.png)

**How many different content types are detected**
This requires going to the parameter tab and searching the keyword "Content_Type" and looking at how many different types there are, in this pcap there are two text/plain and multipart/mixed
![contenttype](/static/images/contenttype.png)

**What is the USB products brand name**
By investigating the files with the keyword USB we can look at all files related to usbs and one html doc contains the landing page for downloading the drivers for the usb where the brand ASIX can be found.
![asix](/static/images/asix.png)

**what is the name of the phone model**
After searching for phone in the keyword filter nothing appears but going through the images there is a pciture which contains the name of the model for the phone which is a lumia 535
![lumia](/static/images/lumia.png)

**what is the source IP of the fish image**
Searching for fish as a keyword in the files tab returns a file called crazy fish double clicking on it returns some data where the source IP can also be located which is 50.22.95.9
![fish](/static/images/fish.png)

**What is the password for the username homer.pwned.se@gmx.com**
Theres over 300 entries in the credentials tab which would make it take a while to sift through looking for the right one but by clicking on the username tab we can sort it alphabetically which makes finding the homer username easy and then the password is spring2015
![spring2015](/static/images/spring2015.png)

**What is the DNS query of the frame 62001**
Going over to the DNS tab and filtering for 62001 brings back two queries for this specific frame which is pop.gmx.com.
![popgmx](/static/images/popgmx.com)

## Conclusion
In conclusion this tool is great to get an overview of the network traffic before delving deeper with more in depth tools like wireshark and txpdump.

---
- **NetworkMiner**
- **TryHackMe**
- **Easy**
- **2026-07-19**
- **NetworkMiner, Tools, Network analysis**
- **A demonstration of the use of NetworkMiner through various activities**
