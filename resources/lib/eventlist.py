#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import os
import threading
import urllib
from centerutils.common_variables import *
from centerutils.database import sc_database
from centerutils import pytzimp
from random import randint
from centerutils.datemanipulation import *
import homemenu as home
import thesportsdb
import leagueview as leagueview
import seasonlist as seasonlist
import contextmenubuilder

def start(arguments):
	window = dialog_eventlist('DialogEventList.xml',addonpath,'Default',str(arguments))
	window.doModal()
	
class dialog_eventlist(xbmcgui.WindowXML):
    
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = eval(args[3])[0]
		self.league = eval(args[3])[2]
		self.season = eval(args[3])[1]
		self.team = eval(args[3])[3]

	def onInit(self,):
		self.addevents()
		#pass
		
	def addevents(self,):
		#set top bar info
		self.getControl(333).setLabel('Event List - '+urllib.unquote(self.sport))
		
		fanart = os.path.join(addonpath,'fanart.jpg')
	
		self.getControl(907).setImage(fanart)
		
		#Def das vistas
		xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
		xbmc.executebuiltin("ClearProperty(posterview,Home)")
		#xbmc.executebuiltin("ClearProperty(panelview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(biglist,Home)")
		xbmc.executebuiltin("ClearProperty(infoview,Home)")
		xbmc.sleep(200)
		
		self.preferred_view = settings.getSetting('view_type_eventlist')

		if self.preferred_view == '' or self.preferred_view == 'infoview':
			self.preferred_view = 'infoview'
			self.preferred_label = 'EventList: InfoView'
			self.controler = 980
			
		elif self.preferred_view == 'biglist':
			self.preferred_view = 'biglist'
			self.preferred_label = 'EventList: BigList'
			self.controler = 982
			
		elif self.preferred_view == 'bannerview':
			self.preferred_view = 'bannerview'
			self.preferred_label = "EventList: BannerView"
			self.controler = 983
			
		elif self.preferred_view == 'posterview':
			self.preferred_view = 'posterview'
			self.preferred_label = "EventList: PosterView"
			self.controler = 984
		
		#grab all events
		all_events = sc_database.Retriever().get_all_events(self.sport,self.season,self.league,self.team)
			
		self.list_listitems = []
		
		if all_events:
		
			for event in all_events:
				#init result and versus
				event_result_present = ''
				event_vs_present = ''
				isRace = False

				event_datetime = thesportsdb.Events().get_datetime_object(event)
				if event_datetime:
					#datetime object conversion goes here
					db_time = pytzimp.timezone(str(pytzimp.timezone(tsdbtimezone))).localize(event_datetime)
					my_timezone= settings.getSetting('timezone')
					my_location=pytzimp.timezone(pytzimp.all_timezones[int(my_timezone)])
					event_datetime=db_time.astimezone(my_location)
				
				#Define event year for listitem property
				event_year = ''
				if event_datetime:
					event_year = str(event_datetime.year)
					
			
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				event_id = thesportsdb.Events().get_eventid(event)
				event_banner = thesportsdb.Events().get_banner(event)
				event_fanart = thesportsdb.Events().get_fanart(event)
				event_thumb = thesportsdb.Events().get_thumb(event)
				event_poster = thesportsdb.Events().get_poster(event)
				event_sport = thesportsdb.Events().get_sport(event)
				event_season = thesportsdb.Events().get_season(event)
				event_label = ''
				
				#plot
				event_plot = thesportsdb.Events().get_plot(event)
				if not event_plot or event_plot == 'None' or event_plot == 'null' or settings.getSetting('hide-results') == 'true':
					event_plot = ''
					
				#season
				if len(event_season) == 4 and event_season != 'None' and event_season != 'null':
					if int(event_season) < 1900:
						i = 0
						start_year=''
						end_year=''
						for char in event_season:
							if i == 0 or i == 1: start_year = start_year + char
							else: end_year = end_year + char
							i+=1
						if int(start_year) > 30 and int(start_year) < 1900: start_year = '19'+start_year
						else: start_year = '20'+start_year
						if int(end_year) > 30 and int(end_year) < 1900: end_year = '19'+end_year
						else: end_year = '20'+end_year
						season_label = start_year + '/' + end_year
					else: season_label = event_season
				else: season_label = event_season
				
				print "fucking season library",season_label
					
				#round
				event_round = thesportsdb.Events().get_round(event)
				if not event_round or event_round == 'null' or event_round == 'None' or event_round == '0':
					event_round = 'Round: N/A'
				else:
					event_round = 'Round: '+str(event_round)
				
				#League related data
				event_leagueid = thesportsdb.Events().get_leagueid(event)
				event_league_dict = sc_database.Retriever().get_all_leagues(event_sport,event_leagueid)[0]
				event_league_name = thesportsdb.Leagues().get_name(event)
				event_league_trophy = thesportsdb.Leagues().get_trophy(event_league_dict)
				
				if not event_league_trophy or event_league_trophy == 'None' or event_league_trophy == 'null':
					event_league_trophy = ''
					
					
				#Properties dependent on the kind of event				
				if event_race and event_race != 'null':
					isRace = True
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''
					event_label = event_name
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = sc_database.Retriever().get_all_teams(None,None,home_team_id)[0]
					#make the lookup only if we can't match the team
					if not home_team_dict: home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = sc_database.Retriever().get_all_teams(None,None,away_team_id)[0]
					#make the request only if we can't match the team
					if not away_team_dict: away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					#check if result is None-None and if so define vs instead of result 
					if result == 'None-None' or result == 'null-null' or settings.getSetting('hide-results') == 'true': event_vs_present = 'vs'
					else: event_result_present = result
					event_label = home_team_name + ' ' + event_vs_present + event_result_present + ' ' + away_team_name
				
				#Set event fanart here
				if not event_fanart or event_fanart == 'None' or event_fanart == 'null':
					if settings.getSetting('event-fanart-priority') != '4':
						if settings.getSetting('event-fanart-priority') == '0':
							if not isRace:
								stadiumfanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
								if stadiumfanart:
									event_fanart = stadiumfanart
							else:
								league_fanartlist = thesportsdb.Leagues().get_fanart(event_league_dict)
								if league_fanartlist:
									event_fanart = league_fanartlist[randint(0,len(league_fanartlist)-1)]

						elif settings.getSetting('event-fanart-priority') == '1':
							#hometeamfanart
							if not isRace:
								available_fanarts = []
								playerfan = thesportsdb.Teams().get_fanart_player(home_team_dict)
								if playerfan and playerfan != 'None' and playerfan != 'null':
									available_fanarts.append(playerfan)
								fanfan = thesportsdb.Teams().get_fanart_fans(home_team_dict)
								if fanfan and fanfan != 'None' and fanfan != 'null':
									available_fanarts.append(fanfan)
								if available_fanarts:
									event_fanart = available_fanarts[randint(0,len(available_fanarts)-1)]
								
							else:
								league_fanartlist = thesportsdb.Leagues().get_fanart(event_league_dict)
								if league_fanartlist:
									event_fanart = league_fanartlist[randint(0,len(league_fanartlist)-1)]

						elif settings.getSetting('event-fanart-priority') == '2':
							league_fanartlist = thesportsdb.Leagues().get_fanart(event_league_dict)
							if league_fanartlist:
								event_fanart = league_fanartlist[randint(0,len(league_fanartlist)-1)]
								
				#thumb check is done here
				if not event_thumb or event_thumb == 'None' or event_thumb == 'null':
					event_thumb = event_fanart
					
				#poster check is done here
				if not event_poster or event_poster == 'None' or event_poster == 'null':
					event_poster = event_fanart
					
				
				if event_datetime:
					try:
						day = str(event_datetime.day)
						month = get_month_long(event_datetime.month)
						year = str(event_datetime.year)
						extensiveday = '%s %s %s' % (day,month,year)
						event_timestring = extensiveday
					except: event_timestring = ''
				else: event_timestring = ''
								
				game = xbmcgui.ListItem(event_label)
				game.setProperty('HomeTeamLogo',home_team_logo)
				game.setProperty('fanart',event_fanart)
				game.setProperty('event_thumb',event_thumb)
				game.setProperty('event_poster',event_poster)
				game.setProperty('event_plot',event_plot)
				game.setProperty('event_league_name',event_league_name)
				game.setProperty('event_league_trophy',event_league_trophy)
				game.setProperty('event_timestring',event_timestring)
				game.setProperty('event_round',event_round)
				game.setProperty('event_season',season_label)
				game.setProperty('event_id',event_id)


				if event_year:
					game.setProperty('event_year',event_year)
				#banner
				if event_banner and event_banner != 'None' and event_banner != 'null':
					game.setProperty('banner',event_banner)
				if not event_race or event_race == 'null':
					if ' ' in home_team_name:
						if len(home_team_name) > 12: game.setProperty('HomeTeamLong',home_team_name)
						else: game.setProperty('HomeTeamShort',home_team_name)
					else: game.setProperty('HomeTeamShort',home_team_name)
					if ' ' in away_team_name:
						if len(away_team_name) > 12: game.setProperty('AwayTeamLong',away_team_name)
						else: game.setProperty('AwayTeamShort',away_team_name)
					else: game.setProperty('AwayTeamShort',away_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					
					game.setProperty('event_result',event_result_present)
					game.setProperty('event_vs',event_vs_present)
				else:
					game.setProperty('EventName',event_name)
				# date + time + timedelay
				game.setProperty('date',event_timestring)
				self.list_listitems.append(game)
		
		xbmc.sleep(200)	
		self.getControl(self.controler).addItems(self.list_listitems)
			
		number_of_events=len(self.list_listitems)
		self.getControl(334).setLabel(str(number_of_events) + ' '+'Events') #TODO string
		
		xbmc.executebuiltin("SetProperty("+self.preferred_view+",1,home)")
		self.getControl(2).setLabel(self.preferred_label)
		xbmc.sleep(100)

		#select 1st item
		self.setFocusId(self.controler)
		self.getControl(self.controler).selectItem(0)
		self.set_info()
		
		
			
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.control_panel = xbmc.getCondVisibility("Control.HasFocus(2)")
			if self.control_panel:
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(self.controler)
			else: 
				self.close()
				#home.start(self.sport)
		elif action.getId() == 117: #contextmenu
			if xbmc.getCondVisibility("Control.HasFocus(983)"): container = 983
			elif xbmc.getCondVisibility("Control.HasFocus(981)"): container = 981
			elif xbmc.getCondVisibility("Control.HasFocus(984)"): container = 984
			elif xbmc.getCondVisibility("Control.HasFocus(982)"): container = 982
			elif xbmc.getCondVisibility("Control.HasFocus(980)"): container = 980
			self.specific_id = self.getControl(container).getSelectedItem().getProperty('event_id')
			contextmenubuilder.start(['eventlist',self.specific_id])	
		else:
			self.set_info()
		
	def set_info(self):
		active_view_type = self.getControl(2).getLabel()
		if active_view_type == "EventList: InfoView":
			self.controler = 980
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "EventList: BigList":
			self.controler = 982
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "EventList: BannerView":
			self.controler = 983
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "EventList: PosterView":
			self.controler = 984
			self.listControl = self.getControl(self.controler)
		
		try:seleccionado=self.listControl.getSelectedItem()
		except:seleccionado = ''
	          
		if seleccionado:
			try: self.getControl(934).setLabel('[B]'+seleccionado.getLabel()+'[/B]')
			except:pass
			try: self.getControl(935).setLabel(seleccionado.getProperty('event_timestring'))
			except: pass
			try: self.getControl(936).setLabel(seleccionado.getProperty('event_league_name'))
			except: pass
			try: self.getControl(958).setLabel('[COLOR labelheader]League:[/COLOR][CR]' + seleccionado.getProperty('event_league_name'))
			except: pass
			try: self.getControl(937).setLabel(seleccionado.getProperty('event_season') + ' ' + seleccionado.getProperty('event_round'))
			except: pass
			try: self.getControl(959).setLabel('[COLOR labelheader]Season & Round:[/COLOR][CR]' + seleccionado.getProperty('event_season') + ' ' + seleccionado.getProperty('event_round'))
			except: pass
			try: self.getControl(960).setLabel('[COLOR labelheader]Event date:[/COLOR][CR]' + seleccionado.getProperty('event_timestring'))
			except: pass
			try: self.getControl(938).setText(seleccionado.getProperty('event_plot'))
			except: pass
			try: self.getControl(70).setText(seleccionado.getProperty('event_plot'))
			except: pass
			try: self.getControl(912).setImage(seleccionado.getProperty('fanart'))
			except: pass
			try: self.getControl(911).setImage(seleccionado.getProperty('event_thumb'))
			except: pass
			try: self.getControl(913).setImage(seleccionado.getProperty('event_thumb'))
			except: pass
			try: self.getControl(956).setImage(seleccionado.getProperty('event_poster'))
			except: pass
			try: self.getControl(957).setImage(seleccionado.getProperty('event_poster'))
			except: pass
			try: self.getControl(910).setImage(seleccionado.getProperty('event_league_trophy'))
			except: pass
			try: self.getControl(954).setImage(seleccionado.getProperty('event_league_trophy'))
			except: pass
		return
				
	def onClick(self,controlId):
		if controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "EventList: InfoView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(infoview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("EventList: BigList")
				self.getControl(982).reset()
				self.getControl(982).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(biglist,1,home)")
				settings.setSetting('view_type_eventlist','biglist')
				self.controler = 982
			elif active_view_type == "EventList: BigList":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(biglist,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("EventList: PosterView")
				self.getControl(984).reset()
				self.getControl(984).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(posterview,1,home)")
				settings.setSetting('view_type_eventlist','posterview')
				self.controler = 984
			elif active_view_type == "EventList: PosterView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(posterview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("EventList: BannerView")
				self.getControl(983).reset()
				self.getControl(983).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(bannerview,1,home)")
				settings.setSetting('view_type_eventlist','bannerview')
				self.controler = 983
			elif active_view_type == "EventList: BannerView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(bannerview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("EventList: InfoView")
				self.getControl(980).reset()
				self.getControl(980).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(infoview,1,home)")
				settings.setSetting('view_type_eventlist','infoview')
				self.controler = 980

		elif controlId == 980 or controlId == 982:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem()
			league_object = seleccionado.getProperty('league_object')
			league_fanart = seleccionado.getProperty('fanart')
			try: league_id = thesportsdb.Leagues().get_id(eval(league_object))
			except: league_id = ''
			if not self.is_library:
				leagueview.start([league_object,self.sport,league_fanart])
			else:
				if league_id:
					seasonlist.start([self.sport,league_id,league_fanart])
			
