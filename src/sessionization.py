## import Libraries:
from datetime import datetime as dt
import csv
import BuckClass  ## defined in './BuckClass.py'
import os.path



## main function:

## Read in inactivity_period.txt
# file = open('../input/inactivity_period.txt', 'r')
# file = open(os.path.join(os.path.dirname(__file__), os.pardir, '/input/inactivity_period.txt'))
cdir = os.path.dirname(__file__)
file = open(cdir + '/../input/inactivity_period.txt')
inac_prd = int(file.read()) ## seconds in integer

## Establish sessionization.txt:
## out_path = '../output/sessionization.txt'
out_path = cdir + '/../output/sessionization.txt'
file = open(out_path, 'w')
file.close()

## Initialize an instance of IpBucks
ipBucks = BuckClass.IpBucks(inac_prd, out_path)

##################################################################
## Open and read in log.csv
file = open(cdir + '/../input/log.csv', 'r')
reader = csv.reader(file, delimiter = ',')

## Get header and move to 1st line of data
header = next(reader)

## Get index for: 'ip', 'date', 'time': don't need 'cik', 'accession', 'extention' as duplicates count
ind_ip, ind_date, ind_time = list(map(lambda x: header.index(x), ['ip', 'date', 'time']))

## Initialize input_list: holds [ip_str, date_str, time_str] from each data line:
input_list = []

for row in reader:
    ## input_list = [ip_str, date_str, time_str]
    input_list = list(map(lambda x: row[x], [ind_ip, ind_date, ind_time]))

    ## Process: input_list = [ip_str, datetime_dt]
    input_list = [input_list[0], dt.strptime(' '.join(input_list[1:]), '%Y-%m-%d %H:%M:%S')]

    ## Update ipBucks
    ipBucks.update(input_list)

## Already finished last line of data
# ipBucks.finish()





