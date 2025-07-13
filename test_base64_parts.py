# -*- coding: utf-8 -*-
import base64

parts = [
    "lucienx_part1.txt",
    "lucienx_part2.txt",
    "lucienx_part3.txt",
    "lucienx_part4.txt"
]

def is_valid_base64(s):
    s = s.strip().replace("\n", "").replace(" ", "")
    missing_padding = len(s) % 4
    if missing_padding:
        s += "=" * (4 - missing_padding)
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception as e:
        return False

for part in parts:
    with open(part, "r") as f:
        data = f.read()
        valid = is_valid_base64(data)
        print(f"{part}: {'ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ OK' if valid else 'ÃƒÂ¢Ã‚ÂÃ…â€™ INVALID'}")





