from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os
import pandas as pd


ROOT = "http://ssms.dongguk.edu"


def search_tag(path, folder, visited, queue):
    visited.add(path)
    try:
        path_name = path.replace('/', '_')
        path_name = path_name.replace('?', '_')
        with open(f"{folder} ahref{path_name}.txt", "w", encoding='UTF-8') as f:  # ,기준으로 text, url
            f.write("text, url 순\n\n")
            absolute_path = ROOT + path
            print("absolute_path :", absolute_path)

            ###########################################
            session = requests.session()
            res = session.get(absolute_path, timeout=4)        #기존에서 session.get으로 로그인 상태 유지한채 받는거로 바꿈
            soup = BeautifulSoup(res.content, "html.parser")
            ###############################################

            hreflist = []
            formlist = []
            inputlist=[]

            attr = ['img', 'i']
            for link in soup.find_all('a'):
                text, url = link.text.strip(), link.get('href')
                if url is None:
                    url = "None"
                if url in ('#', '/'):
                    continue  # http://ssms.dongguk.edu/# == http://ssms.dongguk.edu/ 이어서 그냥 거름
                # 이미지 url 도 그냥 박아버리는 거 같은데, 의도한건지 확인 바람.
                for li in attr:
                    if link.find(li) is None:
                        continue
                    else:
                        if li == 'img':
                            text += " img button : "
                            if link.find(li).get('src') is None:
                                text += "None"
                            else:
                                text += link.find(li).get('src')
                        else:
                            text += " Class : "
                            if isinstance(link.find(li).get('class'), list):
                                text += ' '.join(link.find(li).get('class'))
                            else:
                                if link.find(li).get('class') is None:
                                    text += "None"
                                else:
                                    text += link.find(li).get('class')
                tmplist = (text, url)
                hreflist.append(tmplist)
                if url.startswith('javascript') or url.startswith('mailto'):
                    continue
                if url.startswith('http') and not url.startswith(ROOT): # http로 시작하는데 https://facebook.com 날리는 거고
                    continue
                elif url.startswith(ROOT): # http로 시작하는데, https://stackoverflow.com/telnet
                    url = url.replace(ROOT, '') # /telnet 변환
                print("url :", url)
                queue.append(url)
                f.write(text)
                f.write(", ")
                f.write(url)
                f.write("\n")

        with open(f"{folder}form{path_name}.txt", "w", encoding='UTF-8') as f: # method, action순
            f.write("method, action 순\n\n")
            for link in soup.find_all('form'):
                method = link.get('method')
                action = None
                if method is None:
                    method = "None"
                    action = link.get('action')
                if action is None:
                    action = "None"
                tmplist = (method, action)
                formlist.append(tmplist)
                f.write(action)
                f.write(", ")
                f.write(method)
                f.write("\n")

        with open(f"{folder}input{path_name}.txt", "w", encoding='UTF-8') as f: # text,type,placeholder 순
            f.write("text, type, placeholder 순\n\n")
            for link in soup.find_all('input'):
                text, type, placeholder = link.text.strip(), link.get('type'), link.get('placeholder')

                if not type:
                    type = "None"
                if not placeholder:
                    placeholder = "None"

                tmplist = (text, type,placeholder)
                inputlist.append(tmplist)
                f.write(text)
                f.write(", ")
                f.write(type)
                f.write(", ")
                f.write(placeholder)

                f.write("\n")
    except:
        print(traceback.format_exc().splitlines()[-1])


def main():
    curdir=os.getcwd()
    logintypes=['/student', '/mentor']#, 'instructor' ,'assistant']
    for folder in logintypes:
        directory = curdir + folder
        if not os.path.exists(directory):
            os.makedirs(directory)

    loginfo=[]
    stdvalues = {
        'loginType': 'student',        #student, mentor,instructor,assistant
        'loginId': '2018113581',       #학생, 멘토, 교수, 조교 4가지 logintype
        'loginPwd': 'caps1234'
    }
    mtrvalues={
        'loginType': 'mentor',
        'loginId': 'juno',
        'loginPwd': 'theori1234'
    }
    loginfo.append(stdvalues)
    loginfo.append(mtrvalues)

    for login in loginfo:
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
                search_tag(u, folder, visited, queue)


if __name__ == "__main__":
    main()
