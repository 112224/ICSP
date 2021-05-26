from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os


soup = BeautifulSoup(urlopen('http://ssms.dongguk.edu/mbrmgt/DGU101'), "html.parser")

print('1. ', soup.title)
print('2. ', soup.title.name)
print('3. ', soup.title.string)
print('4. ', soup.title.parent.name)
print('5. ', soup.p)

print('7. ', soup.find_all('input'), '\n\n')
val = soup.find_all('form')
print('8. ', val)

ans = []
print('!!!!!!!test\n\n\n')
if val:
    for li in val:
        res = li.get('method')
        ans.append(res)
        if not res:
            # input이랑 select는 처리 radio는 어떻게 하지..?
            # radio
            print(li.find_all('input'))
            print(li.find_all('select'))
            for wp in li.find_all('input'):
                print(wp.get('id'), wp.get('type'), wp.get('name'))
            print()
            for wp in li.find_all('select'):
                print(wp.get('id'), wp.get('type'), wp.get('name'))
                for opt in wp.find_all('option'):
                    print(opt.get('value'))


#print(ans)
