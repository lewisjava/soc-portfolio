---
title: Log consolidation and parsing
date: 2026-08-10
tags: [Logs]
summary: Commands to consolidate and parse logs
---

# Log consolidation and parsing.

1. Uses awk and sed to normalize the log entries to the desired format. in this example date and time 
```
# Process nginx access log
awk -F'[][]' '{print "[" $2 "]", "--- /var/log/gitlab/nginx/access.log ---", "\"" $0 "\""}' /var/log/gitlab/nginx/access.log  | sed "s/ +0000//g" > /tmp/parsed_consolidated.log
```

2. Use grep to filter specific entries
```
grep "34.253.159.159" /tmp/parsed_consolidated.log > /tmp/filtered_consolidated.log
```

3. Use sort to sort all the log entries by date and time
```
sort /tmp/parsed_consolidated.log > /tmp/sort_parsed_consolidated.log
```

4. Use uniq to remove duplicate entries.
```
uniq /tmp/sort_parsed_consolidated.log > /tmp/uniq_sort_parsed_consolidated.log
```


---
