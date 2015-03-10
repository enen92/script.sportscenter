# -*- coding: utf-8 -*-

""" 
Download tools
"""
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,tarfile,os,sys,re

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'

def Downloader(url,dest):
	urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url:_pbhook(nb,bs,fs))
		
def _pbhook(numblocks, blocksize, filesize):
	try:
		percent = int((int(numblocks)*int(blocksize)*100)/int(filesize))
	except:
		percent = 100
	return percent

	
def extract(self,file_tar,destination):
	dp = xbmcgui.DialogProgress()
	dp.create(translate(40000),translate(40044))
	tar = tarfile.open(file_tar)
	tar.extractall(destination)
	dp.update(100)
	tar.close()
	dp.close()
		
def remove(self,file_):
	dp = xbmcgui.DialogProgress()
	dp.create(translate(40000),translate(40045))
	os.remove(file_)
	dp.update(100)
	dp.close()
