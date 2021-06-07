import os

print("asdfsadf")


with open("C:\dev\cmder\git\ICSP\sqlmap_list.txt") as f:
    for line in f:
        print(line)
        os.system("python C:\dev\cmder\git\ICSP\sqlmap\sqlmap.py "+ line+' --timeout=2')