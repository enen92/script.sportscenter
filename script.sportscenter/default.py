# Copyright (C) 2009-2013 Malte Loepmann (maloep@googlemail.com)
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.


# I have built this script from scratch but you will find some lines or ideas that are taken 
# from other xbmc scripts. Some basic ideas are taken from Redsandros "Arcade Browser" and I often 
# had a look at Nuka1195's "Apple Movie Trailers" script while implementing this one. Thanks for your work!

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys
from resources.lib import homemenu as home
from resources.lib.centerutils.common_variables import *



print sys.argv
def get_params():
	try:
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
				splitparams={}
				splitparams=pairsofparams[i].split('=')
				if (len(splitparams))==2:
					param[splitparams[0]]=splitparams[1]
	except: pass                     
	return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
regexs=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

try:
    regexs=params["regexs"]
except:
    pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)


if mode==None or url==None or len(url)<1:
	print ""
	skin = xbmc.getSkinDir()
	if skin == 'skin.aeon.nox.5':# or skin == 'skin.mimic' or skin == 'skin.confluence':
		home.start(None)
	else:
		#mensagemok('Sports Center', 'Only available for Confluence,Aeon Nox and Mimic')
		mensagemok('Sports Center', 'Only available for Aeon Nox 5 and Helix for now...')
		sys.exit(0)

elif mode==1:
	calendar()
	
	
try:		
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
except: sys.exit(0)
