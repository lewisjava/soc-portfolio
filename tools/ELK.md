---
title: ELK
platform: TryHackMe
date: 2026-07-08
tags: [ELK, tool, SIEM]
summary: A guide to using Elastic Stack
---

# Elastick stack guide
Orignally developed to store, search and visualize large amounts of data orgs can now use it to monitor application performance and perform searches on large datasets, these features made it popular in security.

## Basic components

Elastic search - full-text search and analytics engine for JSON-formatted docs. Stores analyzes and correlates data and supports RESTful API for interacting with it

Logstach - data processing engine. Takes data from different sources, filters it, normalizes it and sends it t the destination which could be Kibana or a listening port. Logstach is configured into three parts.
- Input: where the user defines the source from which data is being ingested
- Filter: where the user specifies the filer options to normalize the logs ingested
- Output: where the user wants the filtered data sent. can be kibana interace, Elasticsearch data base or even a fil.

Beats - host-agents known as data-shippers that ship/transfer data fr the endpoints to Elasticsearch.

Kibana - Web based visualization tool that works with Elasticsearch to analyze, investigate and visualize data streams in real time. allows users to create multiple visualizations and dashboards for easy visibility.

## Search bar
Uses KQL (Kibana Query Language) to search logs in Elasticsearch.
with KQL searches can be performed with free text or field-based searches

Free text - allows for log searches based on text only meaning a simple search of the term "security" will return all the documents that contain this term. KQL also allows wildcards to match parts of a word. allows the use of logical operators AND/OR/NOT

Field-based: in field based searches a field is provided and then a value with a colon as a seperator "field: value", for example "sourceIP : 238.163.231.224 AND UserName : Admin"

---
- **ELK**
- **2026/07/08**
- **ELK, SIEM, LOGS**
- **A brief description of Elastic**
