import os, operator, re

dic = open('dict.log', 'w')
data = open('dependencies.log', 'r')

count = 0

my_string = data.read().split()
my_dict = {}
for item in my_string:
    r = re.search('.*(-(?:\d+\.)*\d+\/)', item)
    if (r):
        item = item[:-(len(r.group(1)))]
    if item in my_dict:
        my_dict[item] += 1
    else:
        my_dict[item] = 1
my_dict = sorted(my_dict.items(), key=operator.itemgetter(1))
for key, value in my_dict:
    dic.write(key + ' ' + str(value) + '\n')

