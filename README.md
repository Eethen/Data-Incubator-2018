# Data-Incubator-2018
# Table of Contents
1. Coding Language and Dependencies
2. Approach: Ideas, Applied Data Structures and Self-defined Class
3.

# 1. Coding Language and Dependencies
## Coding Language
The sessionization.py was written in Python 3.6.3

## Dpendencies
* Module `datetime` was imported to process the date and time. The code is `from datetime import datetime as dt` in `sessionization.py`.
* Module `cvs` was imported to read and write to a .csv file. The code is `import cvs` in `sessionization.py`.
* Module `os.path` was imported to return the absolute path of `sessionization.py`.

# Approach: Ideas, Applied Data Structures and Self-defined Class

## Ideas and Applied Data Structures:
The code reads in and processes the data in log.csv line by line. When 1 line from log.csv is read in, the features, `ip`, `date` and `time`, will be stored in a list for further process as multiple requests of one document within 1 session should not count just as 1; `date` and `time` will combined and process into a datetime object by module `datetime`. 

A dictionary is applied to store information of unexpired sessions for each ip, with ip as keys and a list `[ ip, session_start, latest_request_time, duration, # of web requests]` as values. This is intended to save time in searching and reading.

A queue is applied to group unexpired sessions by their elapsed time. One of its elements is a list of ips who have expired sessions stored in the dictionary mentioned above. That is, ips from one list element in this queue share one latest_request_time for their unexpired sessions. The index of the list elements correspond to how much time it has elapsed since their latest requests. For instance, sessions of ips in element list 0 have their latest requests time as the current time. 

Assuming the inactivity period is n, then the queue has n + 1 list elements; that is, the rightmost element contains ips where n seconds has elapsed since the last request in their sessions, so sessions of the ips in this group will end first. This makes it easy to check for sessions that should end and to track sessions of different time elapses.

The structure of the queue is easy to maintain because every time the sessions in the rightmost element end, the queue will pop the rightmost element and insert an empty list in the left end.

## Class:

