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
import urllib
from random import randint
from centerutils.common_variables import *
from centerutils.datemanipulation import *
import imageviewer as imageviewer

def start(data_list):
	window = dialog_eventdetails('DialogEventdetails.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_eventdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.params = eval(args[3])

	def onInit(self):
		self.event_id = self.params[0]
		self.event_details(self.event_id)

				
	def event_details(self,event):
		self.is_plot = True
		self.event_dict = thesportsdb.Lookups(tsdbkey).lookupevent(event)["events"]
		if self.event_dict and self.event_dict != 'None':
			self.event_dict = self.event_dict[0]
		
		self.sport = thesportsdb.Events().get_sport(self.event_dict)
		
		#Get league information
		self.league_id = thesportsdb.Events().get_leagueid(self.event_dict)
		self.league_dict = thesportsdb.Lookups(tsdbkey).lookupleague(self.league_id)["leagues"][0]
		
		#Check if event has extended results & map
		self.results = thesportsdb.Events().get_result(self.event_dict)
		if self.results and self.results != 'None':
			xbmc.executebuiltin("SetProperty(has_results,1,home)")
			
		self.map = thesportsdb.Events().get_map(self.event_dict)
		
		
		if self.sport.lower() != 'motorsport' and self.sport.lower() != 'golf':
			#Set motorsport stuff visible false
			self.getControl(772).setVisible(False)
			self.getControl(773).setVisible(False)
			self.getControl(774).setVisible(False)
			
			if self.sport.lower() != 'golf':
				self.getControl(9024).setLabel('Stadium')
				xbmc.executebuiltin("SetProperty(has_map,1,home)")
			else:
				self.getControl(9024).setLabel('Map')
				if self.map and self.map != 'None':
					xbmc.executebuiltin("SetProperty(has_map,1,home)")
			
			
			#Teams dict
			self.hometeam_id = thesportsdb.Events().get_hometeamid(self.event_dict)
			self.awayteam_id = thesportsdb.Events().get_awayteamid(self.event_dict)
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
				if self.hometeam_badge and self.hometeam_badge != 'None':
					self.getControl(778).setImage(self.hometeam_badge)
			
			if self.awayteam_jersey and self.awayteam_jersey != 'None':
				self.getControl(780).setImage(self.awayteam_badge)
				self.getControl(782).setImage(self.awayteam_jersey)
			else:
				if self.awayteam_badge and self.awayteam_badge != 'None':
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
			self.spectators = thesportsdb.Events().get_spectators(self.event_dict)
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
			self.getControl(790).setPercent(100)
			self.getControl(791).setImage(os.path.join(addonpath,art,'notlive.png'))
			self.getControl(789).setLabel("[B]Fulltime[/B]")
			
			#set result
			self.home_scored = thesportsdb.Events().get_homescore(self.event_dict)
			self.away_scored = thesportsdb.Events().get_awayscore(self.event_dict)
			self.result = '[B]%s-%s[/B]' % (str(self.home_scored),str(self.away_scored))
			if 'none-none' in self.result.lower():
				self.result = 'vs'
			self.getControl(783).setLabel(self.result)
		else:
			#motorsport stuff
			self.getControl(790).setVisible(False)
			self.getControl(9024).setLabel('Map')
			if self.map and self.map != 'None':
				xbmc.executebuiltin("SetProperty(has_map,1,home)")
			
			if self.sport.lower() == 'motorsport':
				self.getControl(776).setImage(os.path.join(addonpath,art,'raceflag.png'))
			elif self.sport.lower() == 'golf':
				self.getControl(776).setImage(os.path.join(addonpath,art,'golf.png'))
			self.event_name = thesportsdb.Events().get_eventtitle(self.event_dict)
			self.getControl(775).setText(self.event_name)
			self.race_circuit = thesportsdb.Events().get_racecircuit(self.event_dict)
			try: self.getControl(772).setLabel('[COLOR labelheader]Race Circuit:[/COLOR][CR]' + self.race_circuit)
			except: pass
			self.race_location = thesportsdb.Events().get_racelocation(self.event_dict)
			try:self.getControl(773).setLabel('[COLOR labelheader]Race Location:[/COLOR][CR]' + self.race_location)
			except: pass
			self.race_country = thesportsdb.Events().get_racecountry(self.event_dict)
			try: self.getControl(774).setLabel('[COLOR labelheader]Race Country:[/COLOR][CR]' + self.race_country)
			except: pass
		
		
		#COMMON STUFF TO ALL SPORTS
			
		#set date
		self.date = thesportsdb.Events().get_date(self.event_dict)
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
		self.competition = thesportsdb.Events().get_league(self.event_dict)
		self.round = thesportsdb.Events().get_round(self.event_dict)

		if self.round and self.round != 'None' and self.round != '0' and self.round != 'null': self.title = '[B]' + self.competition + ' - Round ' + str(self.round) + '[/B]'
		else: self.title = '[B]'+self.competition+'[/B]'
		self.getControl(787).setLabel(self.title)
		
		#event thumb or fanart or poster
		self.thumb = thesportsdb.Events().get_thumb(self.event_dict)
		self.fanart = thesportsdb.Events().get_fanart(self.event_dict)
		    #priority given to thumb, then fanart, then fanartleague, then force sport
		if self.thumb and self.thumb != 'None' and self.thumb != 'null':		
			self.getControl(794).setImage(self.thumb)
		else:
			if self.fanart and self.fanart != 'None' and self.thumb != 'null':
				self.getControl(794).setImage(self.fanart)
			else:
				league_fanarts = thesportsdb.Leagues().get_fanart(self.league_dict)
				if league_fanarts:
					self.getControl(794).setImage(league_fanarts[randint(0,len(league_fanarts)-1)])
				else:
					self.getControl(794).setImage(os.path.join(addonpath,art,'sports',urllib.quote(self.sport.lower())+'.jpg'))
		
		#event plot
		self.plot = thesportsdb.Events().get_plot(self.event_dict)
		self.getControl(795).setText(self.plot)
		
					

	def onClick(self,controlId):

		if controlId == 9023:
			if self.is_plot:
				self.getControl(795).setText(self.results)
				self.getControl(9023).setLabel('Plot')
				self.is_plot = False
			else:
				self.getControl(795).setText(self.plot)
				self.getControl(9023).setLabel('Results')
				self.is_plot = True
			
		elif controlId == 9024:
			if self.sport.lower() == 'motorsport' or self.sport.lower() == 'golf':
				#map
				self.map = thesportsdb.Events().get_map(self.event_dict)
				imageviewer.view_images(str([self.map]))
			else:
				#stadium
				import stadium as stadium
				stadium_hometeam = thesportsdb.Teams().get_stadium(self.hometeam_dict)
				if stadium_hometeam == self.stadium:
					stadium.start(self.hometeam_dict)
			
			
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
			
	
		
