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

#TODO wait for @zag

def search(tipo,keyword):
	if not tipo:
		dialog = xbmcgui.Dialog()
		options = ["Teams","Players","Events"]
		options_translate = ["teams","players","events"]
		ret = dialog.select("Search option", options)
	else:
		selected = tipo
		search_parameter = keyword
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
					pass
		elif selected == 'players':
			players_list = thesportsdb.Search(tsdbkey).searchplayers(None,search_parameter)["players"]
			if not players_list:
				mensagemok('SportsCenter','No results!')
			else:
				if len(players_list) == 1:
					player_id = thesportsdb.Players().get_id(players_list[0])
					playerview.start([player_id,'plotview'])
				else:
					pass
		elif selected == 'events':
			event_list = thesportsdb.Search(tsdbkey).searchevents(search_parameter,None)["events"]
			if not event_list:
				mensagemok('SportsCenter','No results!')
			else:
				if len(event_list) == 1:
					event_id = thesportsdb.Events().get_id(event_list[0])
					#teamview.teamdetails(team_id)
				else:
					pass
	return
				
