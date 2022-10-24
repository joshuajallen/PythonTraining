# https://realpython.com/installing-python/
# https://docs.python.org/3/library/functions.html#open
# https://docs.python.org/3/library/os.path.html
# https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html

# shortcuts

# CRTL + P - paramter info
# CTRL + space - autofill/completions
# CTRL + Q  - documentation
# SHIFT + ALT + E - execute code
# CTRL + S - save
# Ctrl+Alt+Shift+L - format code


# !/usr/bin/env python3

import requests
import shutil
import psutil
import os
import datetime
import csv
import pandas as pd
import re
import subprocess

from matplotlib import axes

os.getcwd()

os.system('cd C:\\Users\\328576\\source\\python\\training')
# requests.get("https://www.bbc.co.uk/")
# sys.path.insert(1, 'C:/Users/328576/source/python/pyText')

# check disk usage

du = shutil.disk_usage("/")
print(du)

# total free disk space
print(du.free / du.total * 100)

# cpu usage
psutil.cpu_percent(0.1)
psutil.cpu_percent(0.5)


def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20


use = psutil.cpu_percent(0.1)


def check_cpu_usage():
    return use < 75


if not check_disk_usage("/") or not check_cpu_usage():
    print("ERROR")

else:
    print("Everything working ")

print(os.getcwd())
file = open("application_test.csv")
file.read()
file.close()

path = "application_test.csv"
os.path.exists(path)
os.path.getsize(path)
datetime.datetime.fromtimestamp(os.path.getmtime(path))
os.path.abspath(path)
os.mkdir("newdir")
os.listdir()

# working with csv

f = open("application_test.csv")
file = csv.reader(f)
data = pd.read_csv(path)

# regular expressions

re.findall(pattern="Cash", string=str(data['NAME_CONTRACT_TYPE']))
result = re.search(r"text", "mytext", re.IGNORECASE)
print(result)

result = re.findall(r"text|test", "mytext and test", re.IGNORECASE)
print(result)

# managing data and processes

name = input("Enter your name: ")
print(name)
