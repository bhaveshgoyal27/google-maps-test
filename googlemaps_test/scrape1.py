import requests
from bs4 import BeautifulSoup
import json

re=requests.get("https://api.covid19india.org/data.json").text
print(re[0])
r = json.loads(re)
a=r["cases_time_series"]
i=a[-1]
print("total confirmed: {}\n total dead: {}\n total recoverd: {}".format(i["totalconfirmed"],i["totaldeceased"],i["totalrecovered"]))
b=r["statewise"]
b.pop(0)
d=dict()
for i in b:
    d[i["state"]]=[i["active"],i["confirmed"],i["deaths"],i["recovered"]]
for i in d:
    print(i,d[i])


re=requests.get("https://api.covid19india.org/state_district_wise.json").text
r=json.loads(re)

    
