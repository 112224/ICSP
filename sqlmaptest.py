import os

print("asdfsadf")


with open("sqlmap_list.txt") as f:
    for line in f:
        print(line)
        os.system("python sqlmap\sqlmap.py " + line + ' --timeout=2')