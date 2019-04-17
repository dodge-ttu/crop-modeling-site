#! /home/will/virt_envs/cpvenv/bin/python

import requests

with open('/home/will/crop_mod_site/metload/met_load_key.txt') as f:
        met_key = f.read()

print('good choice')

payload = {
        met_key:met_key,
        }

requests.get('https://aerial-analytics.us/metload/1295849198091283497812893972193748912379', params=payload)

