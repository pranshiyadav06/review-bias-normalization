#csv fields are as follows
#Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text

#json fields are as follows
#{"reviewerID": "AO94DHGC771SJ", "asin": "0528881469", "reviewerName": "amazdnu", "helpful": [0, 0], "reviewText": ", "overall": 5.0, "summary": "Gotta have GPS!", "unixReviewTime": 1370131200, "reviewTime": "06 2, 2013"}

import sys

w=open(sys.argv[2],'w')
w.write('Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text\n')

import json
import csv

data=open(sys.argv[1],'r').readlines()
for line in data:
	j=json.loads(line)
	str1=','+j["asin"]+','+j["reviewerID"]+',,,,'+str(j["overall"])+',,"'+j["summary"].replace('"',' ')+'","'+j["reviewText"].replace('"',' ')+'"\n'
	w.write(str1)