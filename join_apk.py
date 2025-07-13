# -*- coding: utf-8 -*-
import os, base64

parts = ["lucienx_part1.txt","lucienx_part2.txt",
         "lucienx_part3.txt","lucienx_part4.txt"]

def fix_pad(s):
    s = s.strip().replace("\n","").replace(" ","")
    return s + "="*((4 - len(s)%4)%4)

with open("LucienX_app.apk","wb") as out:
    for p in parts:
        if os.path.exists(p):
            data = open(p).read()
            out.write(base64.b64decode(fix_pad(data)))
print("ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ LucienX_app.apk created successfully.")





