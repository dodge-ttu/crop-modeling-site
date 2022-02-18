#! /home/will/virt_envs/cpvenv/bin/python

import requests

with open('/home/will/crop-modeling-site/metload/met_load_key.txt') as f:
        met_key = f.read().splitlines()[0] # strip newlines

payload = {
        'met_key':met_key,
        }

r = requests.get('http://143.198.148.168:8000/metload/1295849198091283497812893972193748912379', params=payload)
