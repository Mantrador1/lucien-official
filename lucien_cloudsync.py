# -*- coding: utf-8 -*-
import os
import time
import hashlib
from webdav3.client import Client

# WebDAV Config
options = {
    'webdav_hostname': "https://webdav.pcloud.com",
    'webdav_login':    "fotoniomail@gmail.com",
    'webdav_password': "LucienBot2025"
}

client = Client(options)
target_folder = "/Lucien_Uploads"
local_folder = "C:/lucien_proxy/uploads"

# ÃƒÅ½Ã¢â‚¬ÂÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¿ ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ cloud ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â½ ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÂÃ‚ÂÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹
if not client.check(target_folder):
    client.mkdir(target_folder)

def file_checksum(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

uploaded = {}

while True:
    try:
        for filename in os.listdir(local_folder):
            full_path = os.path.join(local_folder, filename)
            if not os.path.isfile(full_path):
                continue

            checksum = file_checksum(full_path)
            if uploaded.get(filename) == checksum:
                continue  # skip if same

            remote_path = f"{target_folder}/{filename}"
            client.upload_sync(remote_path=remote_path, local_path=full_path)
            uploaded[filename] = checksum
            print(f"ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Synced: {filename}")

    except Exception as e:
        print(f"ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Error: {str(e)}")

    time.sleep(900)  # ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Âµ 15 ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â€šÂ¬ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¬





