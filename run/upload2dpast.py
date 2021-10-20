# -*- coding: utf-8 -*-

import glob
import os
import requests
import pyperclip as pc

FILE = "/tmp/kama*.txt"
for file in glob.glob(FILE):
    with open(file, "r") as f:
        cont = f.readlines()
    data = {"content": ''.join(cont), "syntax": "json", "expiry_days": 10}
    headers = {"User-Agent": "My Python Project"}
    r = requests.post("https://dpaste.com/api/", data=data, headers=headers)
    if r.status_code == 200:
        rtext = r.text.replace("\n", "")+ ".txt"
        print(f"dpaste URL:\n {rtext}")
        pc.copy(rtext)
    else:
        print(f"dpaste error: {r.status_code}")
