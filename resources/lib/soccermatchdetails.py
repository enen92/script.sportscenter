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
import thesportsdb
import datetime
import re
from centerutils.common_variables import *
from centerutils.datemanipulation import *

			


def start(data_list):
	window = dialog_matchdetails('DialogSoccerMatchdetails.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_matchdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.params = eval(args[3])

	def onInit(self):
		self.is_live = self.params[0]
		if self.is_live == False:
			self.event_id = self.params[1]
			self.event_details(self.event_id)
		else:
			self.event_string = self.params[1]
			#event is live
			event_list = self.event_string.split('###')
			self.home_team = event_list[0]
			self.away_team = event_list[1]
			self.livescores = thesportsdb.LiveScores(tsdbkey).latestsoccer()["teams"]["Match"]
			for match in self.livescores:
				home_team = thesportsdb.Livematch().get_home_name(match)
				away_team = thesportsdb.Livematch().get_away_name(match)
				if home_team == self.home_team and away_team == self.away_team:
					self.live_dict = match
					self.event_details(match)
					break
			
	def event_lineup(self,event_dict,home_away):
		xbmc.executebuiltin("ClearProperty(detail,Home)")
		xbmc.executebuiltin("ClearProperty(lineup,Home)")
		
		try: 
			for control in self._controlimage:
				self.getControl(control).setImage('transpar.png')
		except: pass
		
		try:
			for control in self._controltextbox:
				self.getControl(control).setText('')
		except: pass
		

		self.event_dict = event_dict
		#check wether we are trying to find the home or away team
		self.home_away = home_away
		if self.home_away == "home":
			self.jersey = self.hometeam_jersey
			self.badge = self.hometeam_badge
			self.team_name = self.hometeam_name
			if self.is_live == False:
				self.coach = thesportsdb.Teams().get_manager(self.hometeam_dict)
				self.formation = thesportsdb.Events().get_homeformation(self.event_dict)
				self.goalkeeper = thesportsdb.Events().get_homegoalkeeper(self.event_dict)
				self.defenders_raw = thesportsdb.Events().get_homedefense(self.event_dict)
				self.midfielders_raw = thesportsdb.Events().get_homemidfielders(self.event_dict)
				self.forwarders_raw = thesportsdb.Events().get_homeforward(self.event_dict)
				self.subs_raw = thesportsdb.Events().get_homesubs(self.event_dict)
			else:
				self.coach = thesportsdb.Livematch().get_homecoach(self.event_dict).replace(';','')
				self.formation = thesportsdb.Livematch().get_homeformation(self.event_dict)
				self.goalkeeper = thesportsdb.Livematch().get_homegoalkeeper(self.event_dict)
				self.defenders_raw = thesportsdb.Livematch().get_homedefense(self.event_dict)
				self.midfielders_raw = thesportsdb.Livematch().get_homemidfield(self.event_dict)
				self.forwarders_raw = thesportsdb.Livematch().get_homeforward(self.event_dict)
				self.subs_raw = thesportsdb.Livematch().get_home_sublineup(self.event_dict)
			#set button label to call away team lineup
			self.getControl(9027).setLabel('Away Team Lineup')
		
		elif self.home_away == "away":
			self.jersey = self.awayteam_jersey
			self.badge = self.awayteam_badge
			self.team_name = self.awayteam_name
			if self.is_live == False:
				self.coach = thesportsdb.Teams().get_manager(self.awayteam_dict)
				self.formation = thesportsdb.Events().get_awayformation(self.event_dict)
				self.goalkeeper = thesportsdb.Events().get_awaygoalkeeper(self.event_dict)
				self.defenders_raw = thesportsdb.Events().get_awaydefense(self.event_dict)
				self.midfielders_raw = thesportsdb.Events().get_awaymidfielders(self.event_dict)
				self.forwarders_raw = thesportsdb.Events().get_awayforward(self.event_dict)
				self.subs_raw = thesportsdb.Events().get_awaysubs(self.event_dict)
			else:
				self.formation = thesportsdb.Livematch().get_awayformation(self.event_dict)
				self.goalkeeper = thesportsdb.Livematch().get_away_goalkeeper(self.event_dict)
				self.defenders_raw = thesportsdb.Livematch().get_awaydefense(self.event_dict)
				self.midfielders_raw = thesportsdb.Livematch().get_awaymidfielder(self.event_dict)
				self.forwarders_raw = thesportsdb.Livematch().get_awayforward(self.event_dict)
				self.subs_raw = thesportsdb.Livematch().get_away_sublineup(self.event_dict)
				self.coach = thesportsdb.Livematch().get_awaycoach(self.event_dict).replace(';','')		
			
			#set button label to call home team lineup
			self.getControl(9027).setLabel('Home Team Lineup')
		
			
		#set team info
		if self.formation != {}:
			self.getControl(309).setText('[B]%s[/B]' % (self.formation))
		self.getControl(310).setText('[B]%s[/B]' % (self.team_name))
		self.getControl(306).setImage(self.badge)
		self.getControl(311).setText('[COLOR labelheader][B]Coach:[/B][/COLOR] %s' %(self.coach))
	
		#Prepare the data
		
		self.defenders = []
		self.midfielders = []
		self.forwarders = []
		self.subs = []
		
		if self.goalkeeper != {}:
			for player in self.goalkeeper.split(';'):
				if player == '': pass
				else:
					if player.startswith(' '): player = player[1:]
					self.goalkeeper = player
		else: self.goalkeeper = ''
		
		if self.defenders_raw != {}:
			for player in self.defenders_raw.split(';'):
				if player == '': pass
				else:
					if player.startswith(' '): player = player[1:]
					self.defenders.append(player)
		
		if self.midfielders_raw != {}:	
			for player in self.midfielders_raw.split(';'):
				if player == '': pass
				else:
					if player.startswith(' '): player = player[1:]
					self.midfielders.append(player)
		
		if self.forwarders_raw != {}:
			for player in self.forwarders_raw.split(';'):
				if player == '': pass
				else:
					if player.startswith(' '): player = player[1:]
					self.forwarders.append(player)
		
		if self.subs_raw != {}:
			for player in self.subs_raw.split(';'):
				if player == '': pass
				else:
					if player.startswith(' '): player = player[1:]
					self.subs.append(player)
				
		#set lineup and subs info
		lineup = str(self.goalkeeper) + '[CR]'
		if self.defenders:
			for player in self.defenders:
				lineup = lineup + player + '[CR]'
		if self.midfielders:
			for player in self.midfielders:
				lineup = lineup + player + '[CR]'
		if self.forwarders:
			for player in self.forwarders:
				lineup = lineup + player + '[CR]'
		
		subs = ''
		if self.subs:
			for player in self.subs:
				subs = subs + player + '[CR]'

		self.getControl(32150).setText(lineup)
		self.getControl(32151).setText(subs)
		
		#set goalkeeper
		self.getControl(32000).setImage(self.jersey)
		self.getControl(32001).setText(str(self.goalkeeper))
		
		self._controlimage = []
		self._controltextbox = []
		
		#formation management 
		if self.formation == '4-4-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
		
		elif self.formation == '4-3-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[3])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[1])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self._controlimage.append(32054)
			self.getControl(32055).setText(self.midfielders[0])
			self._controltextbox.append(32055)
			self.getControl(32056).setImage(self.jersey)
			self._controlimage.append(32056)
			self.getControl(32057).setText(self.midfielders[1])
			self._controltextbox.append(32057)
			self.getControl(32058).setImage(self.jersey)
			self._controlimage.append(32058)
			self.getControl(32059).setText(self.midfielders[2])
			self._controltextbox.append(32059)
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self._controlimage.append(32066)
			self.getControl(32067).setText(self.forwarders[2])
			self._controltextbox.append(32067)
			self.getControl(32068).setImage(self.jersey)
			self._controlimage.append(32068)
			self.getControl(32069).setText(self.forwarders[1])
			self._controltextbox.append(32069)
			self.getControl(32070).setImage(self.jersey)
			self._controlimage.append(32070)
			self.getControl(32071).setText(self.forwarders[0])
			self._controltextbox.append(32071)
			
		elif self.formation == '4-2-3-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32082).setImage(self.jersey)
			self._controlimage.append(32082)
			self.getControl(32083).setText(self.midfielders[0])
			self._controltextbox.append(32083)
			self.getControl(32084).setImage(self.jersey)
			self._controlimage.append(32084)
			self.getControl(32085).setText(self.midfielders[1])
			self._controltextbox.append(32085)
			self.getControl(32086).setImage(self.jersey)
			self._controlimage.append(32086)
			self.getControl(32087).setText(self.midfielders[2])
			self._controltextbox.append(32087)
			self.getControl(32088).setImage(self.jersey)
			self._controlimage.append(32088)
			self.getControl(32089).setText(self.midfielders[3])
			self._controltextbox.append(32089)
			self.getControl(32090).setImage(self.jersey)
			self._controlimage.append(32090)
			self.getControl(32091).setText(self.midfielders[4])
			self._controltextbox.append(32091)			
			#forwarders
			self.getControl(32060).setImage(self.jersey)
			self._controlimage.append(32060)
			self.getControl(32061).setText(self.forwarders[0])
			self._controltextbox.append(32061)
			
		elif self.formation == '4-1-2-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32092).setImage(self.jersey)
			self._controlimage.append(32092)
			self.getControl(32093).setText(self.midfielders[0])
			self._controltextbox.append(32093)
			self.getControl(32094).setImage(self.jersey)
			self._controlimage.append(32094)
			self.getControl(32095).setText(self.midfielders[1])
			self._controltextbox.append(32095)
			self.getControl(32096).setImage(self.jersey)
			self._controlimage.append(32096)
			self.getControl(32097).setText(self.midfielders[2])
			self._controltextbox.append(32097)
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self._controlimage.append(32066)
			self.getControl(32067).setText(self.forwarders[0])
			self._controltextbox.append(32067)
			self.getControl(32068).setImage(self.jersey)
			self._controlimage.append(32068)
			self.getControl(32069).setText(self.forwarders[1])
			self._controltextbox.append(32069)
			self.getControl(32070).setImage(self.jersey)
			self._controlimage.append(32070)
			self.getControl(32071).setText(self.forwarders[2])
			self._controltextbox.append(32071)
			
		elif self.formation == '4-1-4-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32098).setImage(self.jersey)
			self._controlimage.append(32098)
			self.getControl(32099).setText(self.midfielders[0])
			self._controltextbox.append(32099)
			self.getControl(32100).setImage(self.jersey)
			self._controlimage.append(32100)
			self.getControl(32101).setText(self.midfielders[1])
			self._controltextbox.append(32101)
			self.getControl(32102).setImage(self.jersey)
			self._controlimage.append(32102)
			self.getControl(32103).setText(self.midfielders[2])
			self._controltextbox.append(32103)
			self.getControl(32104).setImage(self.jersey)
			self._controlimage.append(32104)
			self.getControl(32105).setText(self.midfielders[3])
			self._controltextbox.append(32105)
			self.getControl(32106).setImage(self.jersey)
			self._controlimage.append(32106)
			self.getControl(32107).setText(self.midfielders[4])
			self._controltextbox.append(32107)
			#forwarders
			self.getControl(32060).setImage(self.jersey)
			self._controlimage.append(32060)
			self.getControl(32061).setText(self.forwarders[0])
			self._controltextbox.append(32061)
			
		elif self.formation == '4-4-1-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			self.getControl(32108).setImage(self.jersey)
			self._controlimage.append(32108)
			self.getControl(32109).setText(self.midfielders[4])
			self._controltextbox.append(32109)
			#forwarders
			self.getControl(32110).setImage(self.jersey)
			self._controlimage.append(32110)
			self.getControl(32111).setText(self.forwarders[0])
			self._controltextbox.append(32111)
			
		elif self.formation == '5-3-2':
			#defense
			self.getControl(32002).setImage(self.jersey)
			self._controlimage.append(32002)
			self.getControl(32003).setText(self.defenders[0])
			self._controltextbox.append(32003)
			self.getControl(32004).setImage(self.jersey)
			self._controlimage.append(32004)
			self.getControl(32005).setText(self.defenders[1])
			self._controltextbox.append(32005)
			self.getControl(32006).setImage(self.jersey)
			self._controlimage.append(32006)
			self.getControl(32007).setText(self.defenders[2])
			self._controltextbox.append(32007)
			self.getControl(32008).setImage(self.jersey)
			self._controlimage.append(32008)
			self.getControl(32009).setText(self.defenders[3])
			self._controltextbox.append(32009)
			self.getControl(32010).setImage(self.jersey)
			self._controlimage.append(32010)
			self.getControl(32011).setText(self.defenders[4])
			self._controltextbox.append(32011)
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self._controlimage.append(32054)
			self.getControl(32055).setText(self.midfielders[0])
			self._controltextbox.append(32055)
			self.getControl(32056).setImage(self.jersey)
			self._controlimage.append(32056)
			self.getControl(32057).setText(self.midfielders[1])
			self._controltextbox.append(32057)
			self.getControl(32058).setImage(self.jersey)
			self._controlimage.append(32058)
			self.getControl(32059).setText(self.midfielders[2])
			self._controltextbox.append(32059)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
			
		elif self.formation == '3-5-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielders
			self.getControl(32036).setImage(self.jersey)
			self._controlimage.append(32036)
			self.getControl(32037).setText(self.midfielders[0])
			self._controltextbox.append(32037)
			self.getControl(32038).setImage(self.jersey)
			self._controlimage.append(32038)
			self.getControl(32039).setText(self.midfielders[1])
			self._controltextbox.append(32039)
			self.getControl(32040).setImage(self.jersey)
			self._controlimage.append(32040)
			self.getControl(32041).setText(self.midfielders[2])
			self._controltextbox.append(32041)
			self.getControl(32042).setImage(self.jersey)
			self._controlimage.append(32042)
			self.getControl(32043).setText(self.midfielders[3])
			self._controltextbox.append(32043)
			self.getControl(32044).setImage(self.jersey)
			self._controlimage.append(32044)
			self.getControl(32045).setText(self.midfielders[4])
			self._controltextbox.append(32045)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
			
		elif self.formation == '3-4-2-1':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			self.getControl(32112).setImage(self.jersey)
			self._controlimage.append(32112)
			self.getControl(32113).setText(self.midfielders[4])
			self._controltextbox.append(32113)
			self.getControl(32114).setImage(self.jersey)
			self._controlimage.append(32114)
			self.getControl(32115).setText(self.midfielders[5])
			self._controltextbox.append(32115)
			#forwarders
			self.getControl(32116).setImage(self.jersey)
			self._controlimage.append(32116)
			self.getControl(32117).setText(self.forwarders[0])
			self._controltextbox.append(32117)
		
		elif self.formation == '3-4-1-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			self.getControl(32118).setImage(self.jersey)
			self._controlimage.append(32118)
			self.getControl(32119).setText(self.midfielders[0])
			self._controltextbox.append(32119)
			#forwarders
			self.getControl(32120).setImage(self.jersey)
			self._controlimage.append(32120)
			self.getControl(32121).setText(self.forwarders[0])
			self._controltextbox.append(32121)
			self.getControl(32122).setImage(self.jersey)
			self._controlimage.append(32122)
			self.getControl(32123).setText(self.forwarders[1])
			self._controltextbox.append(32123)
			
		elif self.formation == '3-5-1-1':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielder
			self.getControl(32036).setImage(self.jersey)
			self._controlimage.append(32036)
			self.getControl(32037).setText(self.midfielders[0])
			self._controltextbox.append(32037)
			self.getControl(32038).setImage(self.jersey)
			self._controlimage.append(32038)
			self.getControl(32039).setText(self.midfielders[1])
			self._controltextbox.append(32039)
			self.getControl(32040).setImage(self.jersey)
			self._controlimage.append(32040)
			self.getControl(32041).setText(self.midfielders[2])
			self._controltextbox.append(32041)
			self.getControl(32042).setImage(self.jersey)
			self._controlimage.append(32042)
			self.getControl(32043).setText(self.midfielders[3])
			self._controltextbox.append(32043)
			self.getControl(32044).setImage(self.jersey)
			self._controlimage.append(32044)
			self.getControl(32045).setText(self.midfielders[4])
			self._controltextbox.append(32045)
			#forwarders
			self.getControl(32108).setImage(self.jersey)
			self._controlimage.append(32108)
			self.getControl(32109).setText(self.forwarders[0])
			self._controltextbox.append(32109)
			self.getControl(32110).setImage(self.jersey)
			self._controlimage.append(32110)
			self.getControl(32111).setText(self.forwarders[1])
			self._controltextbox.append(32111)
			
		elif self.formation == '4-3-2-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self._controlimage.append(32054)
			self.getControl(32055).setText(self.midfielders[0])
			self._controltextbox.append(32055)
			self.getControl(32056).setImage(self.jersey)
			self._controlimage.append(32056)
			self.getControl(32057).setText(self.midfielders[1])
			self._controltextbox.append(32057)
			self.getControl(32058).setImage(self.jersey)
			self._controlimage.append(32058)
			self.getControl(32059).setText(self.midfielders[2])
			self._controltextbox.append(32059)
			#forwarders
			self.getControl(32112).setImage(self.jersey)
			self._controlimage.append(32112)
			self.getControl(32113).setText(self.midfielders[3])
			self._controltextbox.append(32113)
			self.getControl(32114).setImage(self.jersey)
			self._controlimage.append(32114)
			self.getControl(32115).setText(self.midfielders[4])
			self._controltextbox.append(32115)
			self.getControl(32116).setImage(self.jersey)
			self._controlimage.append(32116)
			self.getControl(32117).setText(self.forwarders[0])
			self._controltextbox.append(32117)
			
		elif self.formation == '4-5-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielder
			self.getControl(32036).setImage(self.jersey)
			self._controlimage.append(32036)
			self.getControl(32037).setText(self.midfielders[0])
			self._controltextbox.append(32037)
			self.getControl(32038).setImage(self.jersey)
			self._controlimage.append(32038)
			self.getControl(32039).setText(self.midfielders[1])
			self._controltextbox.append(32039)
			self.getControl(32040).setImage(self.jersey)
			self._controlimage.append(32040)
			self.getControl(32041).setText(self.midfielders[2])
			self._controltextbox.append(32041)
			self.getControl(32042).setImage(self.jersey)
			self._controlimage.append(32042)
			self.getControl(32043).setText(self.midfielders[3])
			self._controltextbox.append(32043)
			self.getControl(32044).setImage(self.jersey)
			self._controlimage.append(32044)
			self.getControl(32045).setText(self.midfielders[4])
			self._controltextbox.append(32045)
			#forwarders
			self.getControl(32124).setImage(self.jersey)
			self._controlimage.append(32124)
			self.getControl(32125).setText(self.forwarders[0])
			self._controltextbox.append(32125)
			
		elif self.formation == '3-4-3':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self._controlimage.append(32066)
			self.getControl(32067).setText(self.forwarders[0])
			self._controltextbox.append(32067)
			self.getControl(32068).setImage(self.jersey)
			self._controlimage.append(32068)
			self.getControl(32069).setText(self.forwarders[1])
			self._controltextbox.append(32069)
			self.getControl(32070).setImage(self.jersey)
			self._controlimage.append(32070)
			self.getControl(32071).setText(self.forwarders[2])
			self._controltextbox.append(32071)
			
		elif self.formation == '4-3-1-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32123)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32125)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32127)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32129)
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self._controlimage.append(32054)
			self.getControl(32055).setText(self.midfielders[0])
			self._controltextbox.append(32155)
			self.getControl(32056).setImage(self.jersey)
			self._controlimage.append(32056)
			self.getControl(32057).setText(self.midfielders[1])
			self._controltextbox.append(32157)
			self.getControl(32058).setImage(self.jersey)
			self._controlimage.append(32058)
			self.getControl(32059).setText(self.midfielders[2])
			self._controltextbox.append(32159)
			self.getControl(32118).setImage(self.jersey)
			self._controlimage.append(32118)
			self.getControl(32119).setText(self.midfielders[3])
			self._controltextbox.append(32119)
			#forwarders
			self.getControl(32120).setImage(self.jersey)
			self._controlimage.append(32120)
			self.getControl(32121).setText(self.forwarders[0])
			self._controltextbox.append(32121)
			self.getControl(32122).setImage(self.jersey)
			self._controlimage.append(32122)
			self.getControl(32123).setText(self.forwarders[1])
			self._controltextbox.append(32123)
			
		elif self.formation == '4-2-1-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32126).setImage(self.jersey)
			self._controlimage.append(32126)
			self.getControl(32127).setText(self.midfielders[0])
			self._controltextbox.append(32127)
			self.getControl(32128).setImage(self.jersey)
			self._controlimage.append(32128)
			self.getControl(32129).setText(self.midfielders[1])
			self._controltextbox.append(32129)
			self.getControl(32130).setImage(self.jersey)
			self._controlimage.append(32130)
			self.getControl(32131).setText(self.midfielders[2])
			self._controltextbox.append(32131)
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self._controlimage.append(32066)
			self.getControl(32067).setText(self.forwarders[0])
			self._controltextbox.append(32067)
			self.getControl(32068).setImage(self.jersey)
			self._controlimage.append(32068)
			self.getControl(32069).setText(self.forwarders[1])
			self._controltextbox.append(32069)
			self.getControl(32070).setImage(self.jersey)
			self._controlimage.append(32070)
			self.getControl(32071).setText(self.forwarders[2])
			self._controltextbox.append(32071)
			
		elif self.formation == '4-1-3-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32132).setImage(self.jersey)
			self._controlimage.append(32132)
			self.getControl(32133).setText(self.midfielders[0])
			self._controltextbox.append(32133)
			self.getControl(32134).setImage(self.jersey)
			self._controlimage.append(32134)
			self.getControl(32135).setText(self.midfielders[1])
			self._controltextbox.append(32135)
			self.getControl(32136).setImage(self.jersey)
			self._controlimage.append(32136)
			self.getControl(32137).setText(self.midfielders[2])
			self._controltextbox.append(32137)
			self.getControl(32138).setImage(self.jersey)
			self._controlimage.append(32138)
			self.getControl(32139).setText(self.midfielders[3])
			self._controltextbox.append(32139)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
			
		elif self.formation == '4-1-2-1-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			#midfielders
			self.getControl(32132).setImage(self.jersey)
			self._controlimage.append(32132)
			self.getControl(32133).setText(self.midfielders[0])
			self._controltextbox.append(32133)
			self.getControl(32142).setImage(self.jersey)
			self._controlimage.append(32142)
			self.getControl(32143).setText(self.midfielders[1])
			self._controltextbox.append(32143)
			self.getControl(32144).setImage(self.jersey)
			self._controlimage.append(32144)
			self.getControl(32145).setText(self.midfielders[2])
			self._controltextbox.append(32145)
			self.getControl(32140).setImage(self.jersey)
			self._controlimage.append(32140)
			self.getControl(32141).setText(self.midfielders[3])
			self._controltextbox.append(32141)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
			
		elif self.formation == '3-1-3-1-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self._controlimage.append(32030)
			self.getControl(32031).setText(self.defenders[0])
			self._controltextbox.append(32031)
			self.getControl(32032).setImage(self.jersey)
			self._controlimage.append(32032)
			self.getControl(32033).setText(self.defenders[1])
			self._controltextbox.append(32033)
			self.getControl(32034).setImage(self.jersey)
			self._controlimage.append(32034)
			self.getControl(32035).setText(self.defenders[2])
			self._controltextbox.append(32035)
			#midfielders
			self.getControl(32202).setImage(self.jersey)
			self._controlimage.append(32202)
			self.getControl(32203).setText(self.defenders[3])
			self._controltextbox.append(32203)
			self.getControl(32140).setImage(self.jersey)
			self._controlimage.append(32140)
			self.getControl(32141).setText(self.midfielders[3])
			self._controltextbox.append(32141)
			self.getControl(32146).setImage(self.jersey)
			self._controlimage.append(32146)
			self.getControl(32147).setText(self.midfielders[0])
			self._controltextbox.append(32147)
			self.getControl(32148).setImage(self.jersey)
			self._controlimage.append(32148)
			self.getControl(32149).setText(self.midfielders[1])
			self._controltextbox.append(32149)
			self.getControl(32200).setImage(self.jersey)
			self._controlimage.append(32200)
			self.getControl(32201).setText(self.midfielders[2])
			self._controltextbox.append(32201)
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self._controlimage.append(32062)
			self.getControl(32063).setText(self.forwarders[0])
			self._controltextbox.append(32063)
			self.getControl(32064).setImage(self.jersey)
			self._controlimage.append(32064)
			self.getControl(32065).setText(self.forwarders[1])
			self._controltextbox.append(32065)
			
		elif self.formation == '5-4-1':
			#defense
			self.getControl(32002).setImage(self.jersey)
			self._controlimage.append(32002)
			self.getControl(32003).setText(self.defenders[0])
			self._controltextbox.append(32003)
			self.getControl(32004).setImage(self.jersey)
			self._controlimage.append(32004)
			self.getControl(32005).setText(self.defenders[1])
			self._controltextbox.append(32005)
			self.getControl(32006).setImage(self.jersey)
			self._controlimage.append(32006)
			self.getControl(32007).setText(self.defenders[2])
			self._controltextbox.append(32007)
			self.getControl(32008).setImage(self.jersey)
			self._controlimage.append(32008)
			self.getControl(32009).setText(self.defenders[3])
			self._controltextbox.append(32009)
			self.getControl(32010).setImage(self.jersey)
			self._controlimage.append(32010)
			self.getControl(32011).setText(self.defenders[4])
			self._controltextbox.append(32011)
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self._controlimage.append(32046)
			self.getControl(32047).setText(self.midfielders[0])
			self._controltextbox.append(32047)
			self.getControl(32048).setImage(self.jersey)
			self._controlimage.append(32048)
			self.getControl(32049).setText(self.midfielders[1])
			self._controltextbox.append(32049)
			self.getControl(32050).setImage(self.jersey)
			self._controlimage.append(32050)
			self.getControl(32051).setText(self.midfielders[2])
			self._controltextbox.append(32051)
			self.getControl(32052).setImage(self.jersey)
			self._controlimage.append(32052)
			self.getControl(32053).setText(self.midfielders[3])
			self._controltextbox.append(32053)
			#forwarders
			self.getControl(32116).setImage(self.jersey)
			self._controlimage.append(32116)
			self.getControl(32117).setText(self.forwarders[0])
			self._controltextbox.append(32117)
			
		elif self.formation == '4-2-2-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self._controlimage.append(32022)
			self.getControl(32023).setText(self.defenders[0])
			self._controltextbox.append(32023)
			self.getControl(32024).setImage(self.jersey)
			self._controlimage.append(32024)
			self.getControl(32025).setText(self.defenders[1])
			self._controltextbox.append(32025)
			self.getControl(32026).setImage(self.jersey)
			self._controlimage.append(32026)
			self.getControl(32027).setText(self.defenders[2])
			self._controltextbox.append(32027)
			self.getControl(32028).setImage(self.jersey)
			self._controlimage.append(32028)
			self.getControl(32029).setText(self.defenders[3])
			self._controltextbox.append(32029)
			
			
		xbmc.executebuiltin("SetProperty(lineup,1,home)")
		xbmc.sleep(200)
		self.setFocusId(9027)
		
					
	def event_details(self,event):
		xbmc.executebuiltin("ClearProperty(lineup,Home)")
		xbmc.executebuiltin("ClearProperty(detail,Home)")
		if type(event) == dict:
			#in this case we are passing the dictionary itself
			self.event_dict = event
		else:
			self.event_dict = thesportsdb.Lookups(tsdbkey).lookupevent(event)["events"]
			if self.event_dict and self.event_dict != 'None':
				self.event_dict = self.event_dict[0]
				
		
		if self.is_live == False:
			self.hometeam_id = thesportsdb.Events().get_hometeamid(self.event_dict)
			self.awayteam_id = thesportsdb.Events().get_awayteamid(self.event_dict)
		else:
			self.hometeam_id = thesportsdb.Livematch().get_home_id(self.event_dict)
			self.awayteam_id = thesportsdb.Livematch().get_away_id(self.event_dict)
			
		self.hometeam_dict = thesportsdb.Lookups(tsdbkey).lookupteam(self.hometeam_id)["teams"][0]
		self.awayteam_dict = thesportsdb.Lookups(tsdbkey).lookupteam(self.awayteam_id)["teams"][0]
		
			
		#Get both teams badge and jersey
		self.hometeam_badge = thesportsdb.Teams().get_badge(self.hometeam_dict)
		self.awayteam_badge = thesportsdb.Teams().get_badge(self.awayteam_dict)
		self.hometeam_jersey = thesportsdb.Teams().get_team_jersey(self.hometeam_dict)
		self.awayteam_jersey = thesportsdb.Teams().get_team_jersey(self.awayteam_dict)
			
		#Set badge and jersey (if it exists)
		if self.hometeam_jersey and self.hometeam_jersey != 'None':
			self.getControl(777).setImage(self.hometeam_badge)
			self.getControl(779).setImage(self.hometeam_jersey)
		else:
			self.getControl(778).setImage(self.hometeam_badge)
			
		if self.awayteam_jersey and self.awayteam_jersey != 'None':
			self.getControl(780).setImage(self.awayteam_badge)
			self.getControl(782).setImage(self.awayteam_jersey)
		else:
			self.getControl(781).setImage(self.awayteam_badge)
				
		#Set team name
		if settings.getSetting('team-naming')=='0': self.hometeam_name = thesportsdb.Teams().get_name(self.hometeam_dict)
		else: self.hometeam_name = thesportsdb.Teams().get_alternativefirst(self.hometeam_dict)
		if settings.getSetting('team-naming')=='0': self.awayteam_name = thesportsdb.Teams().get_name(self.awayteam_dict)
		else: self.awayteam_name = thesportsdb.Teams().get_alternativefirst(self.awayteam_dict)
		self.getControl(784).setText('[B]%s[/B]' % (self.hometeam_name))
		self.getControl(785).setText('[B]%s[/B]' % (self.awayteam_name))
			
		#event stadium and spectactors
		self.stadium = thesportsdb.Teams().get_stadium(self.hometeam_dict)
		self.getControl(792).setLabel('[B]%s[/B]' % (self.stadium))
		if self.is_live == False: self.spectators = thesportsdb.Events().get_spectators(self.event_dict)
		else: self.spectators = thesportsdb.Livematch().get_spectators(self.event_dict)
		if self.spectators != '0' and str(self.spectators) != '{}':
			try:
				i = 0
				spectators = ''
				lenght = len(self.spectators)
				for letter in reversed(self.spectators):
					i += 1
					if (float(i)/3).is_integer():	
						if lenght != i: spectators = ',' + letter + spectators
						else: spectators = letter + spectators
					else: spectators = letter + spectators
				self.getControl(793).setLabel('[B]Spectators[/B]: %s' % (spectators))
			except:
				self.getControl(793).setLabel('[B]Spectators[/B]: %s' % (self.spectators))
			
		#event progress time
		if self.is_live == False:
			self.getControl(789).setLabel("[B]90'[/B]")
			self.getControl(790).setPercent(100)
			self.getControl(791).setImage(os.path.join(addonpath,art,'notlive.png'))
		else:
			self.timestring = thesportsdb.Livematch().get_time(self.event_dict)
			present = False
			if self.timestring.lower() == 'halftime':
				present = True
				self.time = 45
				self.statusimg = os.path.join(addonpath,art,'half.png')
			elif self.timestring.lower() == 'finished': 
				present = True
				self.time = 90
				self.statusimg = os.path.join(addonpath,art,'notlive.png')
			else:
				try: 
					self.time = int(self.timestring.replace("'",""))
					present = True
					self.statusimg = os.path.join(addonpath,art,'live.png')
				except: present = False
			if present:
				self.getControl(789).setLabel("[B]"+str(self.time)+"'"+"[/B]")
				self.getControl(790).setPercent(int(float(self.time)/90*100))
				self.getControl(791).setImage(self.statusimg)
			
		#set date
		if self.is_live == False: self.date = thesportsdb.Events().get_date(self.event_dict)
		else: self.date = thesportsdb.Livematch().get_date(self.event_dict)
		try:
			if self.date and self.date != 'None':
				date_vector = self.date.split('/')
				if len(date_vector) == 3:
					day = date_vector[0]
					if len(date_vector[2]) == 2:
						year = '20'+date_vector[2]
					month = get_month_long(date_vector[1])
					self.getControl(788).setLabel('[B]%s %s %s[/B]' % (day,month,year))
		except: self.getControl(788).setLabel('[B]%s[/B]' % (self.date))
			
		#set event competition and round(if available)
		if self.is_live == False:
			self.competition = thesportsdb.Events().get_league(self.event_dict)
			try: self.round = thesportsdb.Events().get_round(self.event_dict)
			except: self.round = ''
		else:
			self.competition = thesportsdb.Livematch().get_league(self.event_dict)
			try: self.round = thesportsdb.Livematch().get_round(self.event_dict)
			except: self.round = ''
		if self.round and self.round != 'None': self.title = '[B]' + self.competition + ' - Round ' + str(self.round) + '[/B]'
		else: self.title = '[B]'+self.competition+'[/B]'
		self.getControl(787).setLabel(self.title)
			
		#set result
		if self.is_live == False:
			self.home_scored = thesportsdb.Events().get_homescore(self.event_dict)
			self.away_scored = thesportsdb.Events().get_awayscore(self.event_dict)
		else:
			self.home_scored = thesportsdb.Livematch().get_homegoals_number(self.event_dict)
			self.away_scored = thesportsdb.Livematch().get_awaygoals_number(self.event_dict)
		self.result = '[B]%s-%s[/B]' % (str(self.home_scored),str(self.away_scored))
		self.getControl(783).setLabel(self.result)
			
		#check number of shots
		if self.is_live == False:
			self.home_shots = thesportsdb.Events().get_homeshots(self.event_dict)
			self.away_shots = thesportsdb.Events().get_awayshots(self.event_dict)
		else:
			self.home_shots = 'None'
			self.away_shots = 'None'
		if (self.home_shots and self.home_shots != 'None') and (self.away_shots and self.away_shots != 'None'):
			self.getControl(794).setLabel('[B]Shots[/B]')
			self.getControl(795).setLabel('[B]%s[/B]' %(str(self.home_shots)))
			self.getControl(796).setLabel('[B]%s[/B]' %(str(self.away_shots)))
			
		#fill home team match details
		self.home_details = {}
			
		if self.is_live == False: 
			try: self.home_goaldetails = thesportsdb.Events().get_homegoaldetails(self.event_dict).split(';')
			except: self.home_goaldetails = []
		else: 
			try: self.home_goaldetails = str(thesportsdb.Livematch().get_homegoals_detail(self.event_dict)).split(';')
			except: self.home_goaldetails = []
		if self.home_goaldetails:
			for goal in self.home_goaldetails:
				homegoaldetails = re.compile("(\d+).+?\:(.*)").findall(goal)
				if homegoaldetails:
					for minute,player in homegoaldetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'goal.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'goal.png'),player)]
							
		if self.is_live == False: 
			try: self.home_yellowcards = thesportsdb.Events().get_homeyellowcards(self.event_dict).split(';')
			except: self.home_yellowcards = []
		else: 
			try: self.home_yellowcards = str(thesportsdb.Livematch().get_homeyellowcards(self.event_dict)).split(';')
			except: self.home_yellowcards = []
		
		if self.home_yellowcards:
			for yellow in self.home_yellowcards:
				homeyellowdetails = re.compile("(\d+).+?\:(.*)").findall(yellow)
				if homeyellowdetails:
					for minute,player in homeyellowdetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'yellowcard2.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'yellowcard2.png'),player)]
							
		if self.is_live == False: 
			try: self.home_redcards = thesportsdb.Events().get_homeredcards(self.event_dict).split(';')
			except: self.home_redcards = []
		else: 
			try: self.home_redcards = str(thesportsdb.Livematch().get_homeredcards(self.event_dict)).split(';')
			except: self.home_redcards = []
		if self.home_redcards:
			for red in self.home_redcards:
				homereddetails = re.compile("(\d+).+?\:(.*)").findall(red)
				if homereddetails:
					for minute,player in homereddetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'redcard2.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'redcard2.png'),player)]
			
		self.home_details_listitems = []			
		for key in reversed(sorted(self.home_details.keys())):
			for detail in self.home_details[key]:
				detail_img = detail[0]
				detail_player = detail[1]
					
				detail_item = xbmcgui.ListItem(str(key))
				detail_item.setProperty('minute',"[B]%s': [/B]" % (str(key)))
				detail_item.setProperty('detail_img',detail_img)
				detail_item.setProperty('player',detail_player)
				self.home_details_listitems.append(detail_item)
					
		self.getControl(987).addItems(self.home_details_listitems)
			
		#fill away team match details
		self.away_details = {}
			
		if self.is_live == False:
			try: self.away_goaldetails = thesportsdb.Events().get_awaygoaldetails(self.event_dict).split(';')
			except: self.away_goaldetails = []
		else: 
			try: self.away_goaldetails = str(thesportsdb.Livematch().get_away_goaldetails(self.event_dict)).split(';')
			except: self.away_goaldetails = []
		if self.away_goaldetails:
			for goal in self.away_goaldetails:
				awaygoaldetails = re.compile("(\d+).+?\:(.*)").findall(goal)
				if awaygoaldetails:
					for minute,player in awaygoaldetails:
						if int(minute) in self.away_details.keys():
							self.away_details[int(minute)].append((os.path.join(addonpath,art,'goal.png'),player))
						else:
							self.away_details[int(minute)] = [(os.path.join(addonpath,art,'goal.png'),player)]
							
		if self.is_live == False: 
			try: self.away_yellowcards = thesportsdb.Events().get_awayyellowcards(self.event_dict).split(';')
			except: self.away_yellowcards = []
		else: 
			try: self.away_yellowcards = str(thesportsdb.Livematch().get_awayyellow(self.event_dict)).split(';')
			except: self.away_yellowcards = []
		if self.away_yellowcards:
			for yellow in self.away_yellowcards:
				awayyellowdetails = re.compile("(\d+).+?\:(.*)").findall(yellow)
				if awayyellowdetails:
					for minute,player in awayyellowdetails:
						if int(minute) in self.away_details.keys():
							if player != '&nbsp':
								self.away_details[int(minute)].append((os.path.join(addonpath,art,'yellowcard2.png'),player))
						else:
							if player != '&nbsp':
								self.away_details[int(minute)] = [(os.path.join(addonpath,art,'yellowcard2.png'),player)]
							
		if self.is_live == False:
			try: self.away_redcards = thesportsdb.Events().get_awayredcards(self.event_dict).split(';')
			except: self.away_redcards = []
		else:
			try: self.away_redcards = str(thesportsdb.Livematch().get_away_redcards(self.event_dict)).split(';')
			except: self.away_redcards = []
		if self.away_redcards:
			for red in self.away_redcards:
				awayreddetails = re.compile("(\d+).+?\:(.*)").findall(red)
				if awayreddetails:
					for minute,player in awayreddetails:
						if int(minute) in self.away_details.keys():
							if player != '&nbsp':
								self.away_details[int(minute)].append((os.path.join(addonpath,art,'redcard2.png'),player))
						else:
							if player != '&nbsp':
								self.away_details[int(minute)] = [(os.path.join(addonpath,art,'redcard2.png'),player)]
			
		self.away_details_listitems = []			
		for key in reversed(sorted(self.away_details.keys())):
			for detail in self.away_details[key]:
				detail_img = detail[0]
				detail_player = detail[1]
					
				detail_item = xbmcgui.ListItem(str(key))
				detail_item.setProperty('minute',"[B]%s': [/B]" % (str(key)))
				detail_item.setProperty('detail_img',detail_img)
				detail_item.setProperty('player',detail_player)
				self.away_details_listitems.append(detail_item)
					
		self.getControl(988).addItems(self.away_details_listitems)
		xbmc.executebuiltin("SetProperty(detail,1,home)")
		xbmc.sleep(200)
		self.setFocusId(9022)
					

	def onClick(self,controlId):

		if controlId == 9022:
			self.event_lineup(self.event_dict,"home")
			
		elif controlId == 9023:
			self.event_lineup(self.event_dict,"away")
			
		elif controlId == 9024:
			#stadium
			import stadium as stadium
			stadium_hometeam = thesportsdb.Teams().get_stadium(self.hometeam_dict)
			if stadium_hometeam == self.stadium:
				stadium.start(self.hometeam_dict)
				
		elif controlId == 9025:
			import eventdetails as eventdetails
			eventdetails.start([self.event_id])			
			
		elif controlId == 9027:
			if self.home_away == 'home':
				self.event_lineup(self.event_dict,"away")
			elif self.home_away == 'away':
				self.event_lineup(self.event_dict,"home")
			
		elif controlId == 9028:
			if self.is_live == False:
				self.event_details(self.event_id)
			else:
				self.event_details(self.live_dict)
			
	
		
