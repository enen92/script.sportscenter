# -*- coding: utf-8 -*-

import feedparser,re
from time import mktime
import datetime




def return_rsslist(url):
	rssobj = feedparser.parse(url)
	return_list = []
	now = datetime.datetime.now()
	datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
	if rssobj: 
		rssdict=rssobj["entries"]
		for entry in rssdict:
			title = entry['title']
			content = entry['summary_detail']['value']
			dateitem = entry['published_parsed']
			
			#manipulations on time
			dt = datetime.datetime.fromtimestamp(mktime(dateitem))
			day_difference = (dt - datenow).days
			print day_difference
			if day_difference == 0: feedday = 'Today ' + dt.strftime("%H:%M")
			elif day_difference == -1: feedday = 'Yesterday ' + dt.strftime("%H:%M")
			else: feedday = dt.strftime("%d-%m-%Y %H:%M")
			
			
			links = entry['links']
			img = ''
			for link in links:
				if 'image' in link['type']:
					img = link['href'].replace('150x150','768x576')
			#fix pt rss
			if not img:
				if "<div id=" in content:
					imgfilter = re.compile('src="(.+?)"').findall(content)
					if imgfilter: img = imgfilter[0].replace('143x81','400x225')
					contentfilter = re.compile('<div>(.+?)</div>').findall(content)
					if contentfilter: content = contentfilter[0]

					
					
					
			return_list.append([title,feedday,content,img])
	return return_list

