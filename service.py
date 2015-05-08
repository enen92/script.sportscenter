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

from resources.lib.centerutils.common_variables import *
from resources.lib.centerutils.onscreenutils import *
import threading
import xbmc
import socket
import json
import datetime
import time

#Watcher class checks all files feeded to the player and tries to match it with livescores information from thesportsdb
class watcher:
	def __init__(self,):
		self.t1 = datetime.datetime(1970, 1, 1)
		self.videowatcher()

	def videowatcher(self,):
		#TODO proper service handling (xbmc.Monitor())
		while 1:
			do_check = False
			#Check time interval between checks
			t2 = datetime.datetime.now()
			interval = int(settings.getSetting("videowatcher"))
			update = (abs(t2 - self.t1).seconds)/60 > interval

			if xbmc.getCondVisibility('Player.HasMedia'):
				#get the playing file and compare it with the value stored in the hidden setting
				playingfile = xbmc.Player().getPlayingFile()
				if settings.getSetting('last_played_channel') != playingfile: do_check = True
			
				#check if playing file is PVR or a regular video
			
				if xbmc.getCondVisibility('Pvr.IsPlayingTv') or xbmc.getCondVisibility('Pvr.IsPlayingRadio'):
					#get program title and plot
					active_players = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.GetActivePlayers","params":[]}')
					try: playerid = json.loads(active_players)['result'][0]['playerid']
					except: playerid = ''
					if playerid:
						curr_item = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "plot", "streamdetails"], "playerid":'+str(playerid)+' }, "id": 1 }')
						try: ch_plot = json.loads(curr_item)['result']['item']['plot']	# plot of the channel program being played
						except: ch_plot = ''
						try: ch_title = json.loads(curr_item)['result']['item']['title']	# title of the channel program being played
						except: ch_title = ''
						if ch_title and ch_title != settings.getSetting('last_played_programtitle'): do_check = True
				else:
					#TODO
					ch_title = 'coiso'
					ch_plot = 'coiso'
				
			#Update and match with playing file
			if do_check:
				update_and_match_livescores(ch_title,ch_plot,False)
				settings.setSetting('last_played_channel',playingfile)
				settings.setSetting('last_played_programtitle',ch_title)	
			xbmc.sleep(200)
		
		
		
		
#Service startup
if settings.getSetting('enable-onscreenservice') == 'true':
	video_watcher = threading.Thread(name='videowatcherthread', target=watcher).start()
	







