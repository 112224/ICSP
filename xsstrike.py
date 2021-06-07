import os

with open(r"C:\dev\cmder\git\ICSP\xss_list.txt") as f:
    for line in f:
        print(line)
        os.system(r"python C:\dev\cmder\git\ICSP\XSStrike\xsstrike.py "+ line)


