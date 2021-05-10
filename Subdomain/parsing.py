from urllib.request import urlopen
from bs4 import BeautifulSoup


try:
    f= open("ahref.txt","w",encoding='UTF-8')    # ,기준으로 text, url

    URL="https://stackoverflow.com/" #https://stackoverflow.com/   or https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
    #ssms 사이트 자체에는 form 이 없어서 옆의 사이트들로도 테스트
    html = urlopen(URL,timeout=4)  #ssms가 현재 down상태인데 site가 down인 경우를 위해서 except 구문추가

    soup = BeautifulSoup(html, "html.parser") 

    hreflist=[]
    formlist=[]


    attr=['img','i']
    for link in soup.find_all('a'):     #a 찾기
        text,url=link.text.strip(), link.get('href')
        if(url==None) : url="None"
        if url=='#' : continue     #   http://ssms.dongguk.edu/# == http://ssms.dongguk.edu/ 이어서 그냥 거름
        for li in attr:
            if link.find(li) == None : continue
            else : 
                if(li=='img') : 
                    text+=" img button : "
                    if(link.find(li).get('src')==None) : text+="None"
                    else : text+=link.find(li).get('src')
                else : 
                    text+=" Class : "
                    if isinstance(link.find(li).get('class'),list):
                        text+=' '.join(link.find(li).get('class'))
                    else : 
                        if(link.find(li).get('class')==None) : text+="None"
                        else : text+=link.find(li).get('class')
        tmplist=[]
        tmplist.append(text)
        tmplist.append(url)
        hreflist.append(tmplist)

        f.write(text)         
        f.write(", ")
        f.write(url)
        f.write("\n")

    f= open("form.txt","w",encoding='UTF-8')    #method, action, input type, input placeholder 순
   
    # for link in soup.find_all('form'): 
    #    # print(link)
    #     for i in link.find_all('input'):
    #         print(i)
    #    # print(link.find('input'))


    for link in soup.find_all('form'): 
        method=link.get('method')
        if method==None :method="None"
        action=link.get('action')
        if action==None :action="None"
        #if link.find('input')!=None: t=link.find('input').get('type')       #for 문으로 findall(form) 추가해줘야함
        #if t==None :t="None"
        #ph=link.find('input').get('placeholder')
        #if ph==None :ph="None"
        # else : 
        #     t="None"
        #     ph="None"
        tmplist=[]
        tmplist.append(method)
        tmplist.append(action)
        #tmplist.append(t)   #input type = t
        #tmplist.append(ph)  #input placeholder ph
        formlist.append(tmplist)
        cnt = 1
        for i in tmplist:
            f.write(i)         
            if cnt%2==0 : f.write("\n")
            else : f.write(',')
            cnt+=1

except:
    print("connection fail")