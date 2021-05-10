from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback


def search_tag(path):
    visited.add(path)

    try:
        path_name = path.replace('/', '_')
        path_name = path_name.replace('?', '_')
        with open(f"ahref{path_name}.txt", "w", encoding='UTF-8') as f:  # ,기준으로 text, url

            # http://ssms.dongguk.edu/
            # https://stackoverflow.com/ or https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
            # ssms 사이트 자체에는 form 이 없어서 옆의 사이트들로도 테스트
            absolute_path = ROOT + path
            print("absolute_path :", absolute_path)
            html = urlopen(absolute_path, timeout=4)  # ssms가 현재 down상태인데 site가 down인 경우를 위해서 except 구문추가
            soup = BeautifulSoup(html, "html.parser")
            hreflist = []
            formlist = []

            attr = ['img', 'i']
            for link in soup.find_all('a'):
                text, url = link.text.strip(), link.get('href')
                if url is None:
                    url = "None"
                if url in ('#', '/'):
                    continue  # http://ssms.dongguk.edu/# == http://ssms.dongguk.edu/ 이어서 그냥 거름
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

        with open(f"form{path_name}.txt", "w", encoding='UTF-8') as f: # method, action, input type, input placeholder 순
            for link in soup.find_all('form'):
                method = link.get('method')
                action = None
                if method is None:
                    method = "None"
                    action = link.get('action')
                if action is None:
                    action = "None"
                # if link.find('input')!=None: t=link.find('input').get('type')       #for 문으로 findall(form) 추가해줘야함
                # if t==None :t="None"
                # ph=link.find('input').get('placeholder')
                # if ph==None :ph="None"
                else:
                    t = "None"
                    ph = "None"
                tmplist = (method, action)
                # tmplist.append(t)   #input type = t
                # tmplist.append(ph)  #input placeholder ph
                formlist.append(tmplist)
                cnt = 1
                for i in tmplist:
                    f.write(i)
                    if cnt % 4 == 0:
                        f.write("\n")
                    else:
                        f.write(',')
                    cnt += 1
    except:
        print(traceback.format_exc().splitlines()[-1])


if __name__ == "__main__":
    ROOT = "http://ssms.dongguk.edu"
    visited = set()
    queue = deque([""])
    while queue:
        u = queue.popleft()
        if u not in visited:
            search_tag(u)
