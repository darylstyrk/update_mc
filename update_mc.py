#!/usr/bin/env python3

import httpx
import hashlib
import os
import tempfile
from random import randint
from time import sleep

# Run sometime in the next hour to avoid a herd at Mojang.
sleep(randint(60, 3600))

# Go get a list of all versions and start cutting it up to the specific URL and hash we need.
versions = httpx.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
current = versions.json()["versions"][0]["url"]
target = httpx.get(current)
target_dl = target.json()["downloads"]["server"]["url"]
remote_sha1 = target.json()["downloads"]["server"]["sha1"]

# If it's a new install we create an empty file.
local_file = "/usr/local/bin/minecraft_server.jar"
if not os.path.exists(local_file):
    open(local_file, "w").close()

# Get the local hash to compare to the remote hash.
sha1 = hashlib.sha1()
with open(local_file, "rb") as f:
    while True:
        data = f.read(65536)
        if not data:
            break
        sha1.update(data)
local_sha1 = sha1.digest()

# Compare the remote hash to the local hash. If they're not the same we assume the remote has is
# newer and we replace the local version with the remote.
if remote_sha1 != local_sha1:
    remote_jar = httpx.get(target_dl)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(remote_jar.content)
    os.chmod(f.name, 0o755)
    os.replace(f.name, local_file)
