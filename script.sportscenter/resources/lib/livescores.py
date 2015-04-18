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
import datetime
from centerutils.common_variables import *
from centerutils.datemanipulation import *
from centerutils.caching import *


def start(data_list):
	window = dialog_livescores('DialogLivescores.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_livescores(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)

	def onInit(self):
		#check if the panel has content to know if necessary to bring up loading controls
		self.getControl(92).setImage(os.path.join(addonpath,art,'busy.png'))
		number_of_items = self.getControl(987).size()
		if number_of_items <= 0:
			xbmc.executebuiltin("SetProperty(loading,1,home)")
			self.fill_livescores()
		
	def fill_livescores(self):
		items_to_add = []
		items_in_progress = []
		items_not_started = []
		items_finished = []
		try: self.livescores = thesportsdb.LiveScores().latestsoccer()["teams"]["Match"]
		except: self.livescores = None
		if self.livescores:
			self.getControl(93).setVisible(False)
			if type(self.livescores) == dict:
				self.livescores = [self.livescores]
			for event in reversed(self.livescores):
				try:
					event_home_id = thesportsdb.Livematch().get_home_id(event)
					event_away_id = thesportsdb.Livematch().get_away_id(event)
					event_identifier = event_home_id + event_away_id
					game = xbmcgui.ListItem(event_identifier)
					#get home and away dicts
					home_team_dict = thesportsdb.Lookups().lookupteam(event_home_id)["teams"][0]
					away_team_dict = thesportsdb.Lookups().lookupteam(event_away_id)["teams"][0]
					#set hometeamname
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: team_name = home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					#logos
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					#current_score
					home_goals = thesportsdb.Livematch().get_homegoals_number(event)
					away_goals = thesportsdb.Livematch().get_awaygoals_number(event)
					result = '%s-%s' % (home_goals,away_goals)
					#league info
					competition = thesportsdb.Livematch().get_league(event)
					#roundnum = thesportsdb.Livematch().get_round(event)
					#if roundnum and roudnum != 'None':
					#	competition = competition + ' - Round ' + roundnum
					#Game progress
					progress = thesportsdb.Livematch().get_time(event)
					if progress.lower() == 'finished':
						progress = "90'"
						status = 'finished'
					elif progress.lower() == 'halftime':
						progress = "45'"
						status = 'progress'
					elif progress.lower() == 'postponed':
						status = 'notstarted'
						progress = 'P'
					elif progress.lower() == 'waiting for penalty':
						progress = 'WP'
						status = 'progress'
					elif progress.lower() == 'penalty':
						progress = 'PEN'
						status = 'progress'
					elif progress.lower() == 'finished ap':
						progress = "90'"
						status = 'progress'
					elif progress.lower() == 'not started':
						progress = "0''"
						status = 'notstarted'
					else:status = 'progress'
					if ' ' in home_team_name:
						if len(home_team_name) > 12: game.setProperty('HomeTeamLong',home_team_name)
						else: game.setProperty('HomeTeamShort',home_team_name)
					else: game.setProperty('HomeTeamShort',home_team_name)
					#home_team_logo = cache_image(home_team_logo)
					game.setProperty('HomeTeamLogo',home_team_logo)
					if ' ' in away_team_name:
						if len(away_team_name) > 12: game.setProperty('AwayTeamLong',away_team_name)
						else: game.setProperty('AwayTeamShort',away_team_name)
					else: game.setProperty('AwayTeamShort',away_team_name)
					#set progress
					#xbmc.sleep(100)
					#print "away",away_team_logo,'teste', cache_image(away_team_logo)
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('result',result)
					game.setProperty('competition',competition)
					try:
						if int(home_goals) > 0:
							game.setProperty('home_scored','true')
							homegoaldetails = thesportsdb.Livematch().get_homegoals_detail(event)
							game.setProperty('home_goals',str(homegoaldetails).replace('"',''))
						if int(away_goals) > 0: 
							game.setProperty('away_scored','true')
							awaygoaldetails = thesportsdb.Livematch().get_away_goaldetails(event)
							game.setProperty('away_goals',str(awaygoaldetails).replace('"',''))
					except: pass
					#set progress here
					game.setProperty('minutes',progress)
					if progress.lower() == "45'":
						game.setProperty('is_live','half.png')
						game.setProperty("my_percent","50")
					elif progress.lower() == "0''":
						game.setProperty('is_live','half.png')
						game.setProperty("my_percent","0")
						game.setProperty('minutes',"0'")
					elif progress.lower() == 'p':
						game.setProperty('is_live','notlive.png')
						game.setProperty("my_percent","0")
					elif progress.lower() == 'wp':
						game.setProperty('is_live','half.png')
						game.setProperty("my_percent","100")
					elif progress.lower() == 'pen':
						game.setProperty('is_live','live.png')
						game.setProperty("my_percent","100")
					elif progress.lower() == 'finished ap':
						game.setProperty('is_live','notlive.png')
						game.setProperty("my_percent","100")
					else:
						if progress != "90'":
							game.setProperty('is_live','live.png')
							#try to set game percent according to playing time
							try:
								percent = str(int(int(progress.replace("'",""))/float(90)*100))
								game.setProperty("my_percent",percent)
							except: pass
						else:
							game.setProperty('is_live','notlive.png')
							game.setProperty("my_percent","100")
					
				
					if status == 'progress':
						print "este esta em progresso"
						items_in_progress.append(game)
					elif status == 'notstarted': 
						print "este nao comecou"
						items_not_started.append(game)
					elif status == 'finished':
						print "este acabou"
						items_finished.append(game)
					
				except: pass
			self.getControl(987).reset
			xbmc.executebuiltin("ClearProperty(loading,Home)")
			
			#iterate to all different lists to add the events by order of progress
			if items_in_progress:
				for item in items_in_progress: items_to_add.append(item)
			if items_finished:
				for item in items_finished: items_to_add.append(item)
			if items_not_started:
				for item in items_not_started: items_to_add.append(item)
			
			
			self.getControl(987).addItems(items_to_add)
			xbmc.sleep(300)
			self.setFocusId(987)
			self.getControl(987).selectItem(1)
		else:
			print "no matches"
			xbmc.executebuiltin("ClearProperty(loading,Home)")
			self.getControl(93).setLabel('No matches!')

			
	def onClick(self,controlId):
		if controlId == 983:
			listControl = self.getControl(controlId)
			selected_date=listControl.getSelectedItem().getProperty('entry_date')
			self.fill_calendar(selected_date)
	
		
