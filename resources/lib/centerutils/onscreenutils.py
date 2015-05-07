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
import thesportsdb
import os

#This function updates and saves the information about livescores and livematches to the userdata
#usage: highpriority-title,lowpriority-plot,mode is True False and depends on which we want to enable loading on the onscreen dialog or not
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
	print "CONA: vou pedir os livescores"
	livescores = thesportsdb.LiveScores(tsdbkey).latestsoccer()["teams"]["Match"]
	if livescores:
		print "existe livescores"
		for event in livescores:
			timestring = thesportsdb.Livematch().get_time(event)
			if 'finished' not in timestring.lower() and timestring.lower() != 'postponed':# and timestring.lower() != 'not started':
				livescores_list.append(event)
				event_home_id = thesportsdb.Livematch().get_home_id(event)
				event_away_id = thesportsdb.Livematch().get_away_id(event)
				if event_home_id:
					ficheiro = os.path.join(onscreen_userdata_teams,str(event_home_id)+'.txt')
					if not os.path.exists(ficheiro):
						home_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_home_id)["teams"][0]
						save(ficheiro,str(home_dict))
				if event_away_id:
					ficheiro = os.path.join(onscreen_userdata_teams,str(event_away_id)+'.txt')
					if not os.path.exists(ficheiro):
						away_dict = thesportsdb.Lookups(tsdbkey).lookupteam(event_away_id)["teams"][0]
						save(ficheiro,str(away_dict))
			#TODO save leagues
		#Save livescores
		if livescores_list:
			save(onscreen_livescores,str(livescores_list))
		#Match match being watched
						
	return	
