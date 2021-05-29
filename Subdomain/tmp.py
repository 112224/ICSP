from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os
import re
p = re.compile(r'[\w\\]*')


soup = BeautifulSoup(urlopen('http://ssms.dongguk.edu/mbrmgt/DGU101'), "html.parser")

print('1. ', soup.title)
print('2. ', soup.title.name)
print('3. ', soup.title.string)
print('4. ', soup.title.parent.name)
print('5. ', soup.p)

#print('7. ', soup.find_all('input'), '\n\n')

#print('8. ', val)

print('!!!!!!!test\n\n\n')

'''val = soup.find_all('form')
for li in val:
    print('form id:', li.get('id'))
    res = li.get('method')
    if not res:
        tmp = soup.find_all('script')
        tmp = str(tmp)
        # input이랑 select는 처리 radio는 어떻게 하지..?
        # radio
        js_idx = tmp.find(li.get('id'))
        if js_idx != -1:
            n = len(tmp)
            st = js_idx - 150 if js_idx - 150 > 0 else 0
            ed = js_idx + 150 if js_idx + 150 < n else n
            tmp = tmp[st: ed]
            tmp = tmp.split()
            for i in range(len(tmp)):
                if tmp[i] == 'url:':
                    act = tmp[i+1]
                if tmp[i] == 'type:':
                    meth = tmp[i+1]
            print(tmp)
            print(act, meth)
        # print(li.find_all('input'))
        # print(li.find_all('select'))
        for wp in li.find_all('input'):
            print(wp.get('id'), wp.get('type'), wp.get('name'))
        print()
        for wp in li.find_all('select'):
            print(wp.get('id'), wp.get('type'), wp.get('name'))
            for opt in wp.find_all('option'):
                print(opt.get('value'))'''

path = 'http://ssms.dongguk.edu/mbrmgt/DGU121'
path = p.findall(path)
print(path)

#print(ans)
