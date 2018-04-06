# Data-Incubator-2018
## Table of Contents
1. Coding Language and Modules
2. Approach: Ideas, Applied Data Structures and Self-defined Class

## 1. Coding Language and Dependencies
### Coding Language
The .py files were written in Python 3.6.3

### Modules
* Module `datetime` was imported to process the date and time.
* Module `cvs` was imported to read and write to a .csv file.
* Module `os.path` was imported to return the absolute path of `sessionization.py`.

## 2. Approach: Ideas, Applied Data Structures and Self-defined Class

### Ideas and Applied Data Structures
The code reads in and processes the data from log.csv line by line. When 1 line from log.csv is read in, the fields, `ip`, `date` and `time`, will be stored in a list for further process. `date` and `time` will be combined as one string 'date time', and will be translated into a datetime object by module `datetime`. 

A dictionary object is applied to track all the unexpired sessions, with the ip as the key and a list `[ ip, session_start, latest_request_time, duration, # of web requests]` as the corresponding value. This is intended to save time in tracking and updating unexpired sessions.

A queue object is applied to group unexpired sessions by their elapsed time. Each element in the queue, if not empty, is a list of ips, each of which corresponds to an unexpired session in the dictionary object mentioned above. For ips from one list element in this queue, their corresponding unexpired sessions have the same latest_request_time, and the element index in the queue equals to the amount of time, in seconds, for which the sessions have stayed inactive since their last web request. For instance, the last requests by the ips in the 0th element list were made at the current time given by the latest line of data that is read in from log.csv.

Assuming the length of the inactivity period is n seconds, then the queue has n + 1 list elements. The rightmost list element contains the ips whose last requests in their unexpired sessions were made n seconds ago, so the sessions of these ips will end first. This makes it easy to find sessions that are about to end and to track sessions of different time elapses.

The structure of the queue is easy to maintain because, every time the sessions in the rightmost element end, the queue will pop the rightmost element and insert an empty list in the left end.

### Self-defined Class
Class IpBucks (short for " Ip Buckets") is defined in `BuckClass.py` to help facilitate the process of solving this challenge. Its attributes and built-in methods will take care of the most of the process for users, such as implementing and updating the dictionary and the queue mentioned above. Actually, all we just need to do is implement an instance of class IpBucks in the beginning, call `.update()` for each line from log.csv and call `.finish()` after the last line in log.csv is processed.
