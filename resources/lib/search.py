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

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib
import thesportsdb
import teamview
import playerview
from centerutils.common_variables import *
import eventdetails
import soccermatchdetails

dialog = xbmcgui.Dialog()

def search(tipo,keyword):
	if not tipo:
		options = ["Teams","Players","Events"]
		options_translate = ["teams","players","events"]
		ret = dialog.select("Search option", options)
	else:
		selected = tipo
		search_parameter = urllib.quote(keyword)
		ret = 1
	if ret > -1:
		if not tipo:
			selected = options_translate[ret]
			keyb = xbmc.Keyboard('', 'Enter search keyword')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search_parameter = urllib.quote(keyb.getText())
				
		else: pass
		
		if selected == 'teams':
			team_list = thesportsdb.Search(tsdbkey).searchteams(search_parameter)["teams"]
			if not team_list:
				mensagemok('SportsCenter','No results!')
			else:
				if len(team_list) == 1:
					team_id = thesportsdb.Teams().get_id(team_list[0])
					teamview.teamdetails(team_id)
				else:
					team_names = []
					team_ids = []
					for team in team_list:
						team_id = thesportsdb.Teams().get_id(team)
						team_name = thesportsdb.Teams().get_name(team)
						team_names.append(team_name)
						team_ids.append(team_id)
					ret = dialog.select("Select team", team_names)
					teamview.teamdetails(team_ids[ret])
		elif selected == 'players':
			players_list = thesportsdb.Search(tsdbkey).searchplayers(None,search_parameter)["player"]
			if not players_list:
				mensagemok('SportsCenter','No results!')
			else:
				if len(players_list) == 1:
					player_id = thesportsdb.Players().get_id(players_list[0])
					playerview.start([player_id,'plotview'])
				else:
					player_names = []
					player_ids = []
					for player in players_list:
						player_id = thesportsdb.Players().get_id(player)
						player_name = thesportsdb.Players().get_name(player)
						player_names.append(player_name)
						player_ids.append(player_id)
					ret = dialog.select("Select player", player_names)
					playerview.start([player_ids[ret],'plotview'])
		elif selected == 'events':
			event_list = thesportsdb.Search(tsdbkey).searchevents(search_parameter,None)["event"]
			if not event_list:
				mensagemok('SportsCenter','No results!')
			else:
				if len(event_list) == 1:
					event_id = thesportsdb.Events().get_eventid(event_list[0])
					event_sport = thesportsdb.Events().get_sport(event_list[0])
					if event_sport.lower() == 'soccer' or event_sport.lower() == 'football':
						soccermatchdetails.start([False,event_id])
					else:
						eventdetails.start([event_id])
				else:
					event_ids = []
					event_names = []
					event_sports = []
					for event in event_list:
						event_id = thesportsdb.Events().get_eventid(event)
						event_name = thesportsdb.Events().get_eventtitle(event)
						event_sport = thesportsdb.Events().get_sport(event)
						event_ids.append(event_id)
						event_names.append(event_name)
						event_sports.append(event_sport)
					ret = dialog.select("Select event", event_names)
					sport = event_sports[ret]
					if sport.lower() == 'soccer' or sport.lower() == 'football':
						soccermatchdetails.start([False,event_ids[ret]])
					else:
						eventdetails.start([event_ids[ret]])
	return
				
