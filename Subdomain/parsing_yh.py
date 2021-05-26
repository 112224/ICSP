from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os
import pandas as pd


# herf tag를 만나면 => q에 추가
# path => 현재 url
def search_tag(path):
    visited.add(path)
    try:
        absolute_path = ROOT + path
        res = session.get(absolute_path, timeout=4)  # 기존에서 session.get으로 로그인 상태 유지한채 받는거로 바꿈
        soup = BeautifulSoup(res.content, "html.parser")
        formlist = []
        inputlist = []

        # 페이지 안에 herf 로 다른 페이지 이동이 있을 경우
        attr = ['img', 'i']
        for link in soup.find_all('a'):
            url = link.get('href')
            if not url:
                continue
            if url in ('#', '/'):
                continue  # http://ssms.dongguk.edu/# == http://ssms.dongguk.edu/ 이어서 그냥 거름
            for li in attr:
                if not link.find(li):
                    continue
            if url.startswith('javascript') or url.startswith('mailto'):
                continue
            if url.startswith('http') and not url.startswith(ROOT):  # http로 시작하는데 https://facebook.com 날리는 거고
                continue
            elif url.startswith(ROOT):  # http로 시작하는데, https://stackoverflow.com/telnet
                url = url.replace(ROOT, '')  # /telnet 변환
            print("url :", url)
            queue.append(url)

        # method, action순
        # form을 찾아서 method 확인 => 입력받는 곳이 없으면 sql or xss의 대상 아님
        for link in soup.find_all('form'):
            method = link.get('method')
            action = link.get('action')
            if not method:
                flag = False
                for wp in li.find_all('input'):
                    # form 의 자식들
                    c_id, c_type, c_name = wp.get('id'), wp.get('type'), wp.get('name')
                    if c_type == 'submit':
                        flag = True
                print()
                for wp in li.find_all('select'):
                    print(wp.get('id'), wp.get('type'), wp.get('name'))
                    for opt in wp.find_all('option'):
                        print(opt.get('value'))
            else:

            if action:

            tmplist = (method, action)
            formlist.append(tmplist)

        # text,type,placeholder 순
        for link in soup.find_all('input'):
            text, type, placeholder = link.text.strip(), link.get('type'), link.get('placeholder')
            if not type:
                type = "None"
            if not placeholder:
                placeholder = "None"
            tmplist = (text, type, placeholder)
            inputlist.append(tmplist)
    except:
        print(traceback.format_exc().splitlines()[-1])


if __name__ == "__main__":

    curdir = os.getcwd()
    logintypes = ['/student', '/mentor']  # , 'instructor' ,'assistant']
    for folder in logintypes:
        directory = curdir + folder
        if not os.path.exists(directory):
            os.makedirs(directory)

    loginfo = []
    # 사용자 입력을 받거나, 파일을 읽어오는 방식으로 변경
    # ex) 옵션을 줘서 읽어올 파일이 있으면 읽어오고 아닐 경우 입력을 받는 방식
    stdvalues = {
        'loginType': 'student',  # student, mentor,instructor,assistant
        'loginId': '2018113581',  # 학생, 멘토, 교수, 조교 4가지 logintype
        'loginPwd': 'caps1234'
    }
    mtrvalues = {
        'loginType': 'mentor',
        'loginId': 'juno',
        'loginPwd': 'theori1234'
    }
    loginfo.append(stdvalues)
    loginfo.append(mtrvalues)

for login in loginfo:

    ROOT = "http://ssms.dongguk.edu"
    visited = set()
    queue = deque([""])
    login_url = 'http://ssms.dongguk.edu/mbrmgt/DGU121'
    session = requests.session()
    res = session.post(login_url, data=login)
    res.raise_for_status()
    folder = login.get('loginType') + '/'
    while queue:
        u = queue.popleft()
        if u not in visited:
            search_tag(u)
