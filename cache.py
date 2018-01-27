#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from lxml import html
import shutil
import os

base = "https://outreachdashboard.wmflabs.org/campaigns/"

campaigns = [
	'studenti',
	'seniori',
	'knihovny',
	'workshopy',
]

# Clean data
if os.path.isdir('public/data'):
	shutil.rmtree('public/data')
	os.mkdir('public/data')
else:
	os.mkdir('public/data')

# Regenerate files campaign-users.txt in public iface
for campaign in campaigns:
	url = base + campaign + '/users'
	r = requests.get(url)
	tree = html.fromstring(r.content)
	users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
	f = open('public/data/' + campaign + '-users.txt', 'w')
	for user in users:
		f.write(user.encode('latin1') + '\n')
	f.close()
