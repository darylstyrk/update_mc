#!/usr/bin/env python3

import httpx
import hashlib
import os

versions = httpx.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
current = versions.json()["versions"][0]["url"]
target = httpx.get(current)
target_dl = target.json()["downloads"]["server"]["url"]
remote_sha1 = target.json()["downloads"]["server"]["sha1"]

if not os.path.exists('/usr/local/bin/minecraft_server.jar'):
    os.mknod('/usr/local/bin/minecraft_server.jar')

sha1 = hashlib.sha1()
with open("/usr/local/bin/minecraft_server.jar", "rb") as local_sha1:
    while True:
        data = local_sha1.read(65536)
        if not data:
            break
        sha1.update(data)
local_sha1 = sha1.hexdigest()

if remote_sha1 != local_sha1:
    remote_jar = httpx.get(target_dl)
    with open("/usr/local/bin/minecraft_server.jar", "wb") as file:
        file.write(remote_jar.content)
