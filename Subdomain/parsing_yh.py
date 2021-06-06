from urllib.request import urlopen
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os
import json


def refine_str(dirty):
    clean = dirty.replace('"', '')
    clean = clean.replace("'", '')
    clean = clean.replace(',', '')
    return clean


# herf tag 를 만나면 => q에 추가
# path => 현재 url
def search_tag(visited, soup, root, queue, get_ret):
    # 페이지 안에 herf 로 다른 페이지 이동이 있을 경우
    attr = ['img']
    for link in soup.find_all('a'):
        url = link.get('href')
        attr_flag = False
        if '?' in url:
            get_ret.append(url)
            url, para = url.split('?')
        if not url:
            continue
        if url in visited:
            continue
        if url in ('#', '/'):
            continue  # http://ssms.dongguk.edu/# == http://ssms.dongguk.edu/ 이어서 그냥 거름
        for li in attr:
            if link.find(li):
                attr_flag = True
                break

        if attr_flag or url.startswith('javascript') or url.startswith('mailto'):
            continue
        if url.startswith('http') and not url.startswith(root):  # http로 시작하는데 https://facebook.com 날리는 거고
            continue
        elif url.startswith(root):  # http로 시작하는데, https://stackoverflow.com/telnet
            url = url.replace(root, '')  # /telnet 변환
        # print("url :", url)
        if url not in visited:
            visited.add(url)
            queue.append(url)


def search_ele(path, soup, ret):
    # method, action 순
    # form 을 찾아서 method 확인 => 입력받는 곳이 없으면 sql or xss 의 대상 아님
    for link in soup.find_all('form'):
        method = link.get('method')
        action = link.get('action')
        req_params = []
        flag = False
        # input type 의 태그
        for wp in link.find_all('input'):
            # form 의 자식들
            c_id, c_type, c_name = wp.get('id'), wp.get('type'), wp.get('name')
            # method 는 못찾았지만, submit 이 있을 때
            if c_type == 'submit':
                # if the type is 'submit' then flag = True
                flag = True
                continue
            req_params.append((c_id, c_type, c_name))

        # select type 의 태그
        sel_params = []
        for wp in link.find_all('select'):
            c_id, c_type, c_name = wp.get('id'), wp.get('type'), wp.get('name')
            c_opts = []
            for opt in wp.find_all('option'):
                c_opts.append(opt.get('value'))
            sel_params.append([c_id, c_type, c_name, c_opts])

        # submit 은 있고, form 에 method 가 없다면
        if not method and flag:
            # 이 form 을 이용하여 통신을 하는 함수가 적어도 하나 존재(통신을 가정)
            # script 중 해당 form 의 id를 이용하는 부분의 +- N글자 만큼을 읽어옴
            # 해당 부분에서 method 와 url 탐색 ( 1번 이상 의도적으로 숨겨놓은 경우 => 찾지 못함 )
            tmp = soup.find_all('script')
            tmp = str(tmp)
            js_idx = tmp.find(link.get('id'))
            if js_idx != -1:
                n = len(tmp)
                st = js_idx - 150 if js_idx - 150 > 0 else 0
                ed = js_idx + 150 if js_idx + 150 < n else n
                tmp = tmp[st: ed]
                tmp = tmp.split()
                for i in range(len(tmp)):
                    if tmp[i] == 'url:':
                        action = tmp[i + 1]
                    elif tmp[i] == 'url':
                        action = tmp[i + 2]
                    elif tmp[i] == 'type:':
                        method = tmp[i + 1]
                    elif tmp[i] == 'type':
                        method = tmp[i + 2]
            else:
                continue
        elif not method and not flag:
            continue
        # method 가 form 안에 있는 경우는 별도 지정 없이 바로 추가
        # print([path, method, action,req_params, sel_params])
        method = refine_str(method)
        if action:
            action = refine_str(action)
        ret.append([path, method, action, req_params, sel_params])

        '''# text,type,placeholder 순
        for link in soup.find_all('input'):
            text, type, placeholder = link.text.strip(), link.get('type'), link.get('placeholder')
            if not type:
                type = "None"
            if not placeholder:
                placeholder = "None"
            tmplist = (text, type, placeholder)
            inputlist.append(tmplist)'''


def main(input_url, is_login, login_url, id, pw):
    ans = []
    get_ans = []
    loginfo = [{}]
    # 사용자 입력을 받거나, 파일을 읽어오는 방식으로 변경
    # ex) 옵션을 줘서 읽어올 파일이 있으면 읽어오고 아닐 경우 입력을 받는 방식

    for login in loginfo:
        root = input_url
        visited = set()
        queue = deque([""])
        res = None
        if login:
            login_url = login_url
            session = requests.session()
            res = session.post(login_url, data=login)
            res.raise_for_status()
            cookie_val = res.cookies
            print(cookie_val)
        ret = []
        get_ret = []
        cnt=0
 
        while queue:
            cnt+=1
  
            u = queue.popleft()
            '''if u not in visited or not once:
                visited.add(u)'''
            try:
                absolute_path = root + u
                if res:
                    res = session.get(absolute_path, timeout=4) 
                    soup = BeautifulSoup(res.content, "html.parser")

                else:
                    page_response = requests.get(absolute_path, timeout=4)
                    soup = BeautifulSoup(page_response.content, 'html.parser')
                search_tag(visited, soup, root, queue, get_ret)
                # val = soup.find_all('form')
                # print(val)
                search_ele(absolute_path, soup, ret)
            except:
                print(traceback.format_exc().splitlines()[-1])

        print('complete the task!!')
        for ele in ret:
            print(ele)
        ans.append(ret)
        get_ans.append(get_ret)

    type_filter = ['radio', 'checkbox']
    # fname = input_url[8:] if input_url[:8] == 'https://' else input_url[7:]
    # with open(f"sql_{fname}.txt", "w+", encoding='UTF-8') as f:
    with open(f"sqlmap_list.txt", "w+", encoding='UTF-8') as f, open (f"xss_list.txt", "w+", encoding='UTF-8') as f2:
        url_check = set()
        for get_ret in get_ans:
            ## 작성요망
        for ret in ans:
            for path, method, action, req_params, sel_params in ret:
                for_data = []
                for_para = []
                add_str = ''
                checked = set()
                if action:
                    if action.startswith(root):
                        action = action.replace(root,'')
                    action = root + action
                else:
                    continue
                # 파라미터가 없는 경우 => injection 불가라고 생각하여 넣음
                if len(req_params):
                    if method == 'post' or method == 'POST':
                        for cid, ctype, cname in req_params:
                            if not cname:
                                continue
                            if cname in checked:
                                continue
                            checked.add(cname)
                            if ctype not in type_filter:
                                # 얘는 정리 쉬움 ','.join(map(str,for_para))
                                for_para.append(cname)
                            if ctype == 'checkbox':
                                for_data.append(f'{cname}=True')
                                continue
                            # 얘는 default 값이 필요 형태는 '&'.join(map(str,for_data)
                            else:
                                for_data.append(f'{cname}=1')
                        for cid, ctype, cname, copts in sel_params:
                            for_data.append(f'{cname}={copts[0]}')
                else:
                    continue
                if method == 'post' or method == 'POST':
                    sql_add_str = ' --data="' + '&'.join(map(str, for_data)) + '" -p ' + ','.join(map(str, for_para))
                    xss_add_str = ' --data="' + '&'.join(map(str, for_data))
                if method == 'get' or method == 'GET':
                    if action in url_check:
                        continue
                    url_check.add(action)
                f.write(action + sql_add_str + '\n')
                f2.write(action + xss_add_str + '\n')
                # print(path, method, action, req_params, sel_params, '\n')

        # df.to_csv(f'{root}.csv', index=False)
    print(cnt)


if __name__ == "__main__":
    main("http://192.168.56.107/", False, None, None, None)