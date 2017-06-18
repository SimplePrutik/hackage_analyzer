import requests
import urllib.request
import json
import re
import os

r = requests.get("https://hackage.haskell.org/packages/.json")
packages = json.loads(r.text)

nodes = open ('nodes.csv','w')
edges = open ('edges.csv','w')

nodes.write('Id,Label\n')
edges.write('Source,Target\n')

ids = {}
index = 1
for pkg in packages:
    ids[pkg['packageName']] = index
    nodes.write(str(index) + ',' + pkg['packageName'] + '\n')
    index = index + 1



with open('dependencies.log', 'r') as openfileobject:
    for line in openfileobject:
        item = line
        item = re.sub(re.compile('(-(?:\d+\.)*\d+\/)') , "" ,item)
        items = re.findall('\S+', item)
        for i in range(1,len(items) - 1):
            try:
                edges.write(str(ids[items[0]]) + ',' + str(ids[items[i]]) + '\n')
            except:
                print(items[0], items[i], 'Error')

