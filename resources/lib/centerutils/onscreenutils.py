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

from common_variables import *
from iofile import *
from database import sc_scrapper
import thesportsdb
import os
import difflib
import time
import datetime
import json
import socket
import threading


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


#This function updates and saves the information about livescores and livematches to the userdata
#usage: highpriority-title,lowpriority-plot,mode is True False and depends if we want to enable loading on the onscreen dialog or not
def update_and_match_livescores(ch_title,ch_plot,mode):
	#variable init
	home_dict = {}
	away_dict = {}
	event_league_id = ''
	#
	if mode == True:
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		save(loading_onscreenlock,'')
	#remove all files
	if os.path.isfile(onscreen_livescores): os.remove(onscreen_livescores)
	if os.path.isfile(onscreen_playingmatch): os.remove(onscreen_playingmatch)
	teams = os.listdir(onscreen_userdata_teams)
	for ficheiro in teams:
		if os.path.isfile(os.path.join(onscreen_userdata_teams,ficheiro)): os.remove(os.path.join(onscreen_userdata_teams,ficheiro))
	leagues = os.listdir(onscreen_userdata_leagues)
	for ficheiro in leagues:
		if os.path.isfile(os.path.join(onscreen_userdata_leagues,ficheiro)): os.remove(os.path.join(onscreen_userdata_leagues,ficheiro))
	#update livescores and teams txt files
	livescores_list = []
	livescores = thesportsdb.LiveScores(tsdbkey).latestsoccer()["teams"]
	if livescores:
		livescores = livescores["Match"]
	if livescores:
		for event in livescores:
			try:	timestring = thesportsdb.Livematch().get_time(event)
			except: timestring = ''
			if timestring and 'finished' not in timestring.lower() and timestring.lower() != 'postponed' and timestring.lower() != 'not started':
				try:
					event_home_id = thesportsdb.Livematch().get_home_id(event)
					event_away_id = thesportsdb.Livematch().get_away_id(event)
				except:
					event_home_id = ''
					event_away_id = ''
				if event_home_id and event_home_id != '{}' and event_away_id and event_away_id != '{}':
					print event_home_id,event_away_id
					if event_home_id:
						ficheiro = os.path.join(onscreen_userdata_teams,str(event_home_id)+'.txt')
						if not os.path.exists(ficheiro):
							home_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_home_id)["teams"][0]
							#define keyword array for home team
							hometeam_name = thesportsdb.Teams().get_name(home_dict)
							hometeam_alternative = thesportsdb.Teams().get_alternativename(home_dict)
							team_keywords = []
							if hometeam_name and hometeam_name != 'None': team_keywords.append(hometeam_name)
							if hometeam_alternative and hometeam_alternative != 'None': team_keywords.append(hometeam_alternative)
							event['homekeywords'] = team_keywords
							save(ficheiro,str(home_dict))
					if event_away_id:
						ficheiro = os.path.join(onscreen_userdata_teams,str(event_away_id)+'.txt')
						if not os.path.exists(ficheiro):
							away_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_away_id)["teams"][0]
							#define keyword array for home team
							awayteam_name = thesportsdb.Teams().get_name(away_dict)
							awayteam_alternative = thesportsdb.Teams().get_alternativename(away_dict)
							team_keywords = []
							if awayteam_name and awayteam_name != 'None': team_keywords.append(awayteam_name)
							if awayteam_alternative and awayteam_alternative != 'None': team_keywords.append(awayteam_alternative)
							event['awaykeywords'] = team_keywords
							save(ficheiro,str(away_dict))	
					livescores_list.append(event)
				#TODO proper league determination - need  @ zag feature request
				if home_dict and away_dict:
					home_league_id = thesportsdb.Teams().get_league_id(home_dict)
					away_league_id = thesportsdb.Teams().get_league_id(away_dict)
					if home_league_id == away_league_id:
						event_league_id = home_league_id
						event['league_id'] = event_league_id
		#Save livescores
		if livescores_list:
			save(onscreen_livescores,str(livescores_list))
		#Match match being watched
		match_patterns_title = sc_scrapper.Parser().from_string_get_home_and_away_teams(ch_title,'short')
		match_patterns_plot = sc_scrapper.Parser().from_string_get_home_and_away_teams(ch_plot,'full')
		#print match_patterns_title,match_patterns_plot
		
		#the idea is to have a percentage of similarity for every home and away entry in the match patterns list. Then sum both and add it to the empty dictionary. The comparison is only made for len > 3 to avoid comparing rubish. Every home and away teams will be a key in the dictionary and their value will be the assigned event. Later we sort the dictionary keys is descending order and grab the higher value. If the value exceeds a X value we assume we found the match we are watching.
		
		probability_dictionary = {}
		if livescores_list:
			for event in livescores_list:
				
				#Title
				ratio = 0.0
				if match_patterns_title:
					for hometeam,awayteam in match_patterns_title:
						for keyword in event['homekeywords']:
							if len(hometeam) > 3:
								ratio += difflib.SequenceMatcher(None, hometeam.lower(), keyword.lower() ).ratio()
						for keyword in  event['awaykeywords']:
							if len(awayteam) > 3:
								ratio += difflib.SequenceMatcher(None, awayteam.lower(),keyword.lower()).ratio()
						if ratio > 0.0: probability_dictionary[ratio] = event
					
				#Plot	
				
				if match_patterns_plot:
					for hometeam,awayteam in match_patterns_plot:
						for keyword in event['homekeywords']:
							if len(hometeam) > 3:
								ratio += difflib.SequenceMatcher(None, hometeam.lower(), keyword.lower()).ratio()
						for keyword in event['awaykeywords']:
							if len(awayteam) > 3:
								ratio += difflib.SequenceMatcher(None, awayteam.lower(),keyword.lower() ).ratio()
						if ratio>0.0: probability_dictionary[ratio] = event	
					
			#for key in probability_dictionary:
				#print key
				#print thesportsdb.Livematch().get_home_name(probability_dictionary[key])
			
		if probability_dictionary:
			if len(probability_dictionary.keys()) >= 1:
				ratios = []
				for key in sorted(probability_dictionary.keys()):
					ratios.append(key)
				
				key = max(ratios)	
				hometeam_id = thesportsdb.Livematch().get_home_id(probability_dictionary[key])
				awayteam_id = thesportsdb.Livematch().get_away_id(probability_dictionary[key])
				if 'league_id' in probability_dictionary[key].keys():
					league_id = probability_dictionary[key]['league_id']
				else:
					league_id = ''
				videofile = settings.getSetting('last_played_channel')
				txt = { 'hometeamid':hometeam_id,'awayteamid':awayteam_id,'league_id':league_id,'videofile':videofile }
				save(onscreen_playingmatch,str(txt))

		if mode == True:
			xbmc.executebuiltin("ClearProperty(loading,Home)")
			try:os.remove(loading_onscreenlock)
			except:pass
	return	
