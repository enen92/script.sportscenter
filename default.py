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
	param=[]
	try: paramstring=sys.argv[2]
	except: paramstring = ''
	if len(paramstring)>=2:
		params=sys.argv[2]
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=params.split('/')
		for parm in pairsofparams:
			if parm == '':
				pairsofparams.remove(parm)      
	return pairsofparams

try: params=get_params()
except: params = []

#Usage for external calls
#xbmc.executebuiltin("RunScript(script.sportscenter,,/teste1/teste2/teste3)")

if not params:
	home.start(None)
else:
	if params[0] == 'home':
		home.start(None)
	elif params[0] == 'calendar':
		from resources.lib import calendar as calendar
		calendar.start(None)
	elif params[0] == 'onscreen':
		from resources.lib import onscreen as onscreen
		onscreen.start(None)
	elif params[0] == 'league':
		sport = params[1]
		leagueid = params[2]
		try: mode = params[3]
		except: mode = 'plotview'
		from resources.lib import leagueview
		leagueview.start([leagueid,sport,'',mode])
	elif params[0] == 'team':
		sport = params[1]
		teamid = params[2]
		try: mode = params[3]
		except: mode = 'plotview'
		from resources.lib import teamview
		teamview.start([teamid,sport,'',mode])
	elif params[0] == 'player':
		player_id = params[1]
		try: mode = params[3]
		except: mode = 'plotview'
		from resources.lib import playerview as playerview
		playerview.start([player_id,mode])
		
	#TODO - Finish modes

try: xbmcplugin.endOfDirectory(int(sys.argv[1]))
except: sys.exit(0)
