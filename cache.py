#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import urllib
from lxml import html
import shutil
import os

requests.utils.default_user_agent = lambda: "Dashboard Scrapper (no website exists, martin.urbanec@wikimedia.cz, https://meta.wikimedia.org/wiki/User:Martin_Urbanec)"

base = "https://outreachdashboard.wmflabs.org/campaigns/"

campaigns = [
	'studenti',
	'seniori',
	'knihovny',
]

# Clean data
if os.path.isdir('/data/project/urbanecmbot/mark-students/public/data'):
	shutil.rmtree('/data/project/urbanecmbot/mark-students/public/data')
	os.mkdir('/data/project/urbanecmbot/mark-students/public/data')
else:
	os.mkdir('/data/project/urbanecmbot/mark-students/public/data')

# Regenerate files campaign-users.txt in public iface
fcss = open('/data/project/urbanecmbot/mark-students/public/data/stylesheet.css', 'w')
fcss.write('@charset "utf-8";\n\n')
rules = []
for campaign in campaigns:
	url = base + campaign + '/users'
	r = requests.get(url)
	tree = html.fromstring(r.content)
	users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
	f = open('/data/project/urbanecmbot/mark-students/public/data/' + campaign + '-users.txt', 'w')
	for user in users:
		f.write(user.encode('latin1') + '\n')
		rules.append("a[href$='wiki/Wikipedista:" + urllib.quote_plus(user.encode('latin1').replace(' ', '_')) + "']")
		rules.append("a[href$='Wikipedista:" + urllib.quote_plus(user.encode('latin1').replace(' ', '_')) + "&action=edit&redlink=1']")
		rules.append("a[href$='wiki/Wikipedistka:" + urllib.quote_plus(user.encode('latin1').replace(' ', '_')) + "']")
		rules.append("a[href$='Wikipedistka:" + urllib.quote_plus(user.encode('latin1').replace(' ', '_')) + "&action=edit&redlink=1']")
	f.close()
	fcss.write(",\n".join(rules))
	fcss.write("\n{ color: green !important; font-weight: bold !important; }\n\n")
	rules = []
