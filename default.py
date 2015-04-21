# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
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



import xbmcplugin
import xbmcgui
import xbmc 
import xbmcaddon
import os
import sys
from resources.lib import homemenu as home
from resources.lib.centerutils.common_variables import *



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
	try:
		if skin == 'skin.aeon.nox.5':# or skin == 'skin.mimic' or skin == 'skin.confluence':
			home.start(None)
			#from resources.lib import tables as tables
			#tables.start(None)
		else:
			mensagemok('Sports Center', 'Only available for Aeon Nox 5 and Helix for now...')
			sys.exit(0)
	except: pass
	
		#Dialog test
		#from resources.lib import calendar as calendar
		#calendar.start(None)
		#from resources.lib import livescores as livescores
		#livescores.start(None)
		#from resources.lib import matchdetails as matchdetails
		#matchdetails.start([False,'441709'])
		#matchdetails.start_linup(None)
		#except:
		#mensagemok('Sports Center', 'Only available for Confluence,Aeon Nox and Mimic')
			

elif mode==1:
	calendar()
	
	
try:		
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
except: sys.exit(0)
