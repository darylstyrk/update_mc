#!/usr/bin/env python3

import httpx
import hashlib
import os
import tempfile
from random import randint
from time import sleep

sleep(randint(60, 3600))

versions = httpx.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
current = versions.json()["versions"][0]["url"]
target = httpx.get(current)
target_dl = target.json()["downloads"]["server"]["url"]
remote_sha1 = target.json()["downloads"]["server"]["sha1"]

local_file = "/usr/local/bin/minecraft_server.jar"
if not os.path.exists(local_file):
    open(local_file, "w").close()

sha1 = hashlib.sha1()
with open(local_file, "rb") as f:
    while True:
        data = f.read(65536)
        if not data:
            break
        sha1.update(data)
local_sha1 = sha1.digest()

if remote_sha1 != local_sha1:
    remote_jar = httpx.get(target_dl)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(remote_jar.content)
    os.chmod(f.name, 0o755)
    os.replace(f.name, local_file)
