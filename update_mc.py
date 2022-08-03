#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 19:31:01 2022

@author: darylstyrk
"""

import requests

versions = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
current = versions.json()['versions'][0]['url']

target = requests.get(current)
target_dl = target.json()['downloads']['server']['url']

URL = target_dl

r = requests.get(URL, allow_redirects=True)

with open('/usr/local/bin/minecraft_server.jar', 'wb') as file:
    file.write(r.content)