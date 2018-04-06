from collections import deque
from datetime import datetime as dt

## to Class IpBucks for the challenge
class IpBucks:

    def __init__(self, inac_prd, out_path):
    ## Fields:

        ## constant variables:
        ## path to sessionization.txt
        self.out_path = out_path
        ## inactivity period length
        self.inac_prd = inac_prd

        ## fields for all ips
        ## queue for bucks of ips by elapsed time
        self.ipList_que = deque([[]] + [[]] * inac_prd) # by seconds
        ## dictionary with session info of ips
        self.ip_dict = {} # 'ip': [ip, start_dt, lastest_dt, duration, count, No]

        ## fields specific to each read-in line of log.csv
        self.elap = 0 # now - then
        self.then = 0 # time from last update
        self.now = 0
        self.ip = 0
        self.ipListQue_ind = False # Buck index in ipListQue
        self.lineNo = 0 # Line No


    ## Methods:

    ## Update self.ipListQue_ind
    def ipListQue_find(self):
        if (self.ip not in self.ip_dict) or (self.ip_dict[self.ip] is None):
            self.ipListQue_ind = False
        else:
            self.ipListQue_ind = (self.then - self.ip_dict[self.ip][2]).seconds

    ## Update self.ip_dict[new ip]:
    ##     Cases: 1) ip not in dict; 2) dict[ip] is None; 3) dict[ip] is Not None
    def ipDict_update(self):
        if self.ipListQue_ind is not False: # already exists
            ## 'ip': [ip, start_dt, lastest_dt, duration, count, lineNo]
            self.ip_dict[self.ip][2] = self.now # update end
            self.ip_dict[self.ip][4] += 1
        else:
            ## 'ip': [ip, start_dt, lastest_dt, duration, count, lineNo]
            self.ip_dict[self.ip] = [self.ip, self.now, self.now, 0, 1, self.lineNo]

    ## Change the new ip between buckets self.ipList_que:
    ##     Cases: 1) ip not in que (not in dict || dict[ip] is None); 2) Buck 0; 3) Buck > 0
    ## self.ipListQue_ind: current ipListQue_ind
    def ipListQue_switch(self):
        if self.ipListQue_ind is 0: # already in Buck 0
            return 0
        elif self.ipListQue_ind is not False: # already exist in Buck non_zero
            self.ipList_que[self.ipListQue_ind].remove(self.ip)

        self.ipList_que[0].append(self.ip) # switch to Buck 0

    ## Handle the 1st line of data
    def bucks_update0(self):
        self.ipDict_update()
        self.ipListQue_switch()

        ## last operation for update of each data line
        self.then = self.now

    ## return a sorted list of ips in the ascending order of their first request time
    def ips_sort(self, ips):
        if len(ips) == 1:
            return ips
        else:
            return sorted(ips, key = lambda x: self.ip_dict[x][-1])

    ## Writing session info of ips in the last bucket, and set Nones in self.ip_dict
    def writing(self):
        with open(self.out_path, 'a+') as file:
            ips = self.ips_sort(self.ipList_que[-1]) # get ips in the last bucket
            logs = map(lambda z: self.out_form(ip=z), ips) # list of session info lists

            for x in logs:
                file.write(','.join(y for y in x) + '\n')

    ## Given ip: return session in required form, and set Nones in self.ip_dict
    def out_form(self, ip):
        ## 'ip': [ip, start_dt, lastest_dt, duration, count]
        ip_list = self.ip_dict[ip]

        ## Calculate duration
        ip_list[3] = str((ip_list[2] - ip_list[1]).seconds + 1) # inclusive

        ## Str(): start, end, count of web requests
        ip_list[1] = ip_list[1].isoformat(sep=" ")
        ip_list[2] = ip_list[2].isoformat(sep=" ")
        ip_list[4] = str(ip_list[4])
        self.ip_dict[ip] = None

        return ip_list[:5]

    ## Update ipList_que when 1 sec elapses: 1 pop, 1 appendleft
    def ipListQue_update(self):
        self.ipList_que.appendleft([])
        self.ipList_que.pop()


    ## Handle non-1st lines of data in log.csv
    def bucks_updateN(self, N):

        if N >= self.inac_prd + 1:
            ## write all the info in self.ip_dict, and set Nones
            self.finish()

            ## reinitialize self.ipList_que
            self.ipList_que = deque([[]] + [[]] * self.inac_prd)

            ## ip: self.ip_dict[ip] is None, and ip not existing in ipListQue
            self.ipListQue_ind = False
            self.ipDict_update()
            self.ipListQue_switch()

            ## last operation for update of each data line
            self.then = self.now

        elif N == 0:
            self.ipDict_update()
            self.ipListQue_switch()

            ## last operation for update of each data line
            self.then = self.now

        elif N == 1:
            if len(self.ipList_que[-1]) != 0:
                ## writing info of ips in the last bucket, and set Nones in self.ip_dict
                self.writing()

            ## 1 popright, 1 appendleft
            self.ipListQue_update()

            ## (not existing in ipListQue) or (ip': None in dict)
            if (self.ipListQue_ind is False) or (self.ipListQue_ind == (self.inac_prd)):
                self.ipListQue_ind = False
            else:
                self.ipListQue_ind += 1

            self.bucks_updateN(N = 0)

            ## last operation for update of each data line
            self.then = self.now

        else:
            ## update self.ipListQue_ind;
            if (self.ipListQue_ind is False) or ((self.ipListQue_ind + self.elap - 1) >= self.inac_prd):
                self.ipListQue_ind = False
            else:
                self.ipListQue_ind += 1

            ## writing the last bucket
            if (self.ipList_que[-1] is not None) or (len(self.ipList_que[-1]) != 0):
                ## writng ips in the last bucket, and set Nones in self.ip_dict
                self.writing()

            ## 1 popright, 1 appendleft
            self.ipListQue_update()

            self.bucks_updateN(N = N - 1)

    ## Update instance of IpBucks before the last of data is finished
    def update(self, input_list, lineNo):
        [self.ip, self.now] = input_list
        self.lineNo = lineNo
        self.ipListQue_find()
        ## elap cannot be calculated for Case: then == 0

        if self.then == 0:
            self.bucks_update0()

        else:
            self.elap = (self.now - self.then).seconds
            self.bucks_updateN(self.elap)

    ## Writing all remaining session info in instance of IpBucks after the last of data is finished
    def finish(self):

        ## write all the info in self.ip_dict
        with open(self.out_path, 'a+') as file:
            ## process and sort the Non_none records, and set them to Nones
            names = self.ips_sort( list(filter(lambda x: self.ip_dict[x] is not None, self.ip_dict.keys())) )
            logs = map(lambda y: self.out_form(y), names)

            ## write to output file
            for x in logs:
                file.write(','.join(y for y in x) + '\n')



