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

#This function updates and saves the information about livescores and livematches to the userdata
#usage: highpriority-title,lowpriority-plot,mode is True False and depends if we want to enable loading on the onscreen dialog or not
def update_and_match_livescores(ch_title,ch_plot,mode):
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
				event_home_id = thesportsdb.Livematch().get_home_id(event)
				event_away_id = thesportsdb.Livematch().get_away_id(event)
				if event_home_id:
					ficheiro = os.path.join(onscreen_userdata_teams,str(event_home_id)+'.txt')
					if not os.path.exists(ficheiro):
						home_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_home_id)["teams"][0]
						#define keyword array for home team
						hometeam_name = thesportsdb.Teams().get_name(home_dict)
						hometeam_alternative = thesportsdb.Teams().get_alternativename(home_dict)
						team_keywords = ''
						if hometeam_name and hometeam_name != 'None': team_keywords = team_keywords + hometeam_name
						if hometeam_alternative and hometeam_alternative != 'None': team_keywords = team_keywords +';'+ hometeam_alternative
						event['homekeywords'] = team_keywords
						save(ficheiro,str(home_dict))
				if event_away_id:
					ficheiro = os.path.join(onscreen_userdata_teams,str(event_away_id)+'.txt')
					if not os.path.exists(ficheiro):
						away_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_away_id)["teams"][0]
						#define keyword array for home team
						awayteam_name = thesportsdb.Teams().get_name(away_dict)
						awayteam_alternative = thesportsdb.Teams().get_alternativename(away_dict)
						team_keywords = ''
						if awayteam_name and awayteam_name != 'None': team_keywords = team_keywords + awayteam_name
						if awayteam_alternative and awayteam_alternative != 'None': team_keywords = team_keywords +';'+ awayteam_alternative
						event['awaykeywords'] = team_keywords
						save(ficheiro,str(away_dict))	
				livescores_list.append(event)
			#TODO save leagues @ zag feature request
		#Save livescores
		if livescores_list:
			save(onscreen_livescores,str(livescores_list))
		#Match match being watched
		match_patterns_title = sc_scrapper.Parser().from_string_get_home_and_away_teams(ch_title,'short')
		match_patterns_plot = sc_scrapper.Parser().from_string_get_home_and_away_teams(ch_plot,'full')
		print match_patterns_title,match_patterns_plot
		
		#the idea is to have a percentage of similarity for every home and away entry in the match patterns list. Then sum both and add it to the empty dictionary. The comparison is only made for len > 3 to avoid comparing rubish. Every home and away teams will be a key in the dictionary and their value will be the assigned event. Later we sort the dictionary keys is descending order and grab the higher value. If the value exceeds a X value we assume we found the match we are watching.
		
		probability_dictionary = {}
		if livescores_list:
			for event in livescores_list:
				
				#Title
				
				if match_patterns_title:
					for hometeam,awayteam in match_patterns_title:
						if len(hometeam) > 3:
							ratio = difflib.SequenceMatcher(None, hometeam.lower(), event['homekeywords'].lower()).ratio()
						if len(awayteam) > 3:
							ratio = ratio + difflib.SequenceMatcher(None, awayteam.lower(), event['awaykeywords'].lower()).ratio()
					if ratio: probability_dictionary[ratio] = event
					
				#Plot	
				
				if match_patterns_plot:
					for hometeam,awayteam in match_patterns_plot:
						if len(hometeam) > 3:
							ratio = difflib.SequenceMatcher(None, hometeam.lower(), event['homekeywords'].lower()).ratio()
						if len(awayteam) > 3:
							ratio = ratio + difflib.SequenceMatcher(None, awayteam.lower(), event['awaykeywords'].lower()).ratio()
					if ratio: probability_dictionary[ratio] = event	
					
			print probability_dictionary
			
		if probability_dictionary:
			if len(probability_dictionary.keys()) >= 1:
				for key in sorted(probability_dictionary).keys():
					hometeam_id = thesportsdb.Livematch().get_home_id(probability_dictionary[key])
					awayteam_id = thesportsdb.Livematch().get_away_id(probability_dictionary[key])
					videofile = settings.getSetting('last_played_channel')
					txt = { 'hometeamid':hometeam_id,'awayteamid':awayteam_id,'videofile':videofile }
					save(onscreen_playingmatch,str(txt))
					break		
	return	
