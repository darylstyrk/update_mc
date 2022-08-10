#!/usr/bin/env python3

import requests
import hashlib

versions = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
current = versions.json()["versions"][0]["url"]
target = requests.get(current)
target_dl = target.json()["downloads"]["server"]["url"]
remote_sha1 = target.json()["downloads"]["server"]["sha1"]

BUF_SIZE = 65536

sha1 = hashlib.sha1()
with open("/usr/local/bin/minecraft_server.jar", "rb") as local_sha1:
    while True:
        data = local_sha1.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)
local_sha1 = sha1.hexdigest()

if remote_sha1 != local_sha1:
    remote_jar = requests.get(target_dl, allow_redirects=True)
    with open("/usr/local/bin/minecraft_server.jar", "wb") as file:
        file.write(remote_jar.content)
