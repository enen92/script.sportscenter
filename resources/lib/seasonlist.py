#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import os
import urllib
from centerutils.common_variables import *
from centerutils.iofile import *
from centerutils.database import sc_database
from random import randint
import homemenu as home
import thesportsdb
import contextmenubuilder
import eventlist

def start(strlist):
	window = dialog_compet('DialogSeasonList.xml',addonpath,'Default',str(strlist))
	window.doModal()
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
	
class dialog_compet(xbmcgui.WindowXML):

	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = eval(args[3])[0]
		self.league_id = eval(args[3])[1]
		self.fanart = eval(args[3])[2]

	def onInit(self,):
		self.addseasons()
		
	
	def addseasons(self,):
		#set global fanart	
		self.getControl(907).setImage(addon_fanart) #common_variables
		
		#Def das vistas
		xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
		xbmc.executebuiltin("ClearProperty(listview,Home)")
		xbmc.sleep(200)
		
		self.preferred_view = settings.getSetting('view_type_seasonlist')

		if self.preferred_view == '' or self.preferred_view == 'listview':
			self.preferred_view = 'listview'
			self.preferred_label = 'Season: ListView'
			self.controler = 983
		
		season_list = []	
		if not self.league_id: #assume we want all seasons for a given sport
			events_list = sc_database.Retriever().get_all_events(self.sport,None,None,None)
			if events_list:
				for event in events_list:
					event_season = thesportsdb.Events().get_season(event)
					if event_season not in season_list: season_list.append(event_season)
		else:
			self.league = sc_database.Retriever().get_all_leagues(self.sport,self.league_id)
			if self.league: self.league = self.league[0]
			events_list = sc_database.Retriever().get_all_events(self.sport,None,self.league_id,None)
			if events_list:
				for event in events_list:
					event_season = thesportsdb.Events().get_season(event)
					if event_season not in season_list: season_list.append(event_season)
		
		
		self.list_listitems = []
		if season_list:
			if not self.league_id:
				sport_icon = os.path.join(addonpath,art,self.sport.lower() + '.png')
				sport_fanart = ''
				if settings.getSetting('season-background') != '0':
					if settings.getSetting('season-background') == '1':
						sport_fanart = os.path.join(addonpath,art,'sports',self.sport + '.jpg')
					elif settings.getSetting('season-background') == '2':
						sport_fanart = self.get_sport_fav_fanart(self.sport,'fans')
					elif settings.getSetting('season-background') == '3':
						sport_fanart = self.get_sport_fav_fanart(self.sport,'general')
					elif settings.getSetting('season-background') == '4':
						if settings.getSetting('season-custom') != '':
							sport_fanart = settings.getSetting('season-custom')
				for season in season_list:
					#manipulate strSeason return for better label presentation
					if len(season) == 4 and int(season) < 1900:
						i = 0
						start_year=''
						end_year=''
						for char in season:
							if i == 0 or i == 1: start_year = start_year + char
							else: end_year = end_year + char
							i+=1
						if int(start_year) > 30 and int(start_year) < 1900: start_year = '19'+start_year
						else: start_year = '20'+start_year
						if int(end_year) > 30 and int(end_year) < 1900: end_year = '19'+end_year
						else: end_year = '20'+end_year
						season_label = start_year + '/' + end_year
					else: season_label = season

					seasonItem = xbmcgui.ListItem(season_label, iconImage = sport_icon)
					seasonItem.setProperty('season_id', season)
					seasonItem.setProperty('league_id', '')
					seasonItem.setProperty('season_identifier', urllib.unquote(self.sport))
					if sport_fanart: seasonItem.setProperty('fanart',sport_fanart)
					seasonItem.setProperty('trophy',sport_icon)
					seasonItem.setProperty('badge',sport_icon)
					self.list_listitems.append(seasonItem)
			else:
				trophy = thesportsdb.Leagues().get_trophy(self.league)
				if self.fanart and self.fanart != 'null' and self.fanart != 'None':
					fanart = self.fanart
				else: 
					fanart_list = thesportsdb.Leagues().get_fanart(self.league)
					if fanart_list:
						fanart = fanart_list[randint(0,len(fanart_list)-1)]
					else:
						if settings.getSetting('season-background') != '0':
							if settings.getSetting('season-background') == '1':
								fanart = os.path.join(addonpath,art,'sports',self.sport + '.jpg')
							elif settings.getSetting('season-background') == '2':
								fanart = self.get_sport_fav_fanart(self.sport,'fans')
							elif settings.getSetting('season-background') == '3':
								fanart = self.get_sport_fav_fanart(self.sport,'general')
							elif settings.getSetting('season-background') == '4':
								if settings.getSetting('season-custom') != '':
									fanart = settings.getSetting('season-custom')
				badge = thesportsdb.Leagues().get_badge(self.league)
				league_name = thesportsdb.Leagues().get_name(self.league)
				for season in season_list:
					#manipulate strSeason return for better label presentation
					print "fuk season",season
					if len(season) == 4 and int(season) < 1900:
						i = 0
						start_year=''
						end_year=''
						for char in season:
							if i == 0 or i == 1: start_year = start_year + char
							else: end_year = end_year + char
							i+=1
						if int(start_year) > 30 and int(start_year) < 1900: start_year = '19'+start_year
						else: start_year = '20'+start_year
						if int(end_year) > 30 and int(end_year) < 1900: end_year = '19'+end_year
						else: end_year = '20'+end_year
						season_label = start_year + '/' + end_year
					else: season_label = season
					seasonItem = xbmcgui.ListItem(season_label, iconImage = trophy)
					seasonItem.setProperty('season_id', season)
					seasonItem.setProperty('league_id',self.league_id)
					seasonItem.setProperty('season_identifier', league_name)
					seasonItem.setProperty('fanart',fanart)
					seasonItem.setProperty('trophy',trophy)
					seasonItem.setProperty('badge',badge)
					self.list_listitems.append(seasonItem)

			
		xbmc.sleep(200)	
		self.getControl(self.controler).addItems(self.list_listitems)
			
		number_of_leagues=len(self.list_listitems)
		self.getControl(334).setLabel(str(number_of_leagues) + ' '+'Seasons') #TODO string
		
		#set top bar info
		if self.league_id: self.season_label = urllib.unquote(self.sport) + ' - ' + league_name
		else: self.season_label = urllib.unquote(self.sport)
		self.getControl(333).setLabel('Season List - ' + self.season_label)
		
		xbmc.executebuiltin("SetProperty("+self.preferred_view+",1,home)")
		self.getControl(2).setLabel(self.preferred_label)
		xbmc.sleep(100)
		#select 1st item
		self.setFocusId(self.controler)
		self.getControl(self.controler).selectItem(0)
		self.set_info()
		

	def get_sport_fav_fanart(self,sport,method):
		if sport.lower() == 'soccer' or sport.lower() == 'football': ficheiro = football_fav_file
		elif sport.lower() == 'basketball': ficheiro = basketball_fav_file
		elif sport.lower() == 'rugby': ficheiro = rugby_fav_file
		elif sport.lower() == 'american%20football': ficheiro = amfootball_fav_file
		elif sport.lower() == 'motorsport': ficheiro = motorsport_fav_file
		elif sport.lower() == 'ice%20hockey': ficheiro = icehockey_fav_file
		elif sport.lower() == 'baseball': ficheiro = baseball_fav_file
		elif sport.lower() == 'golf':	ficheiro = golf_fav_file
		if os.path.isfile(ficheiro):
			sport_info = eval(readfile(ficheiro))
			if method == 'fans':
				fanart = sport_info[4]
				if fanart: return fanart
				else:
					fanart = sport_info[5]
					if fanart: return fanart
					else: return ''
			elif method == 'general':
				fanart = sport_info[5]
				if fanart: return fanart
				else: return ''
		else: return ''
			
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.control_panel = xbmc.getCondVisibility("Control.HasFocus(2)")
			if self.control_panel:
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(self.controler)
			else: 
				self.close()
		else:
			self.set_info()
		
	def set_info(self):
		active_view_type = self.getControl(2).getLabel()
		if active_view_type == "Season: ListView":
			self.controler = 983
			self.listControl = self.getControl(self.controler)
		
		try:seleccionado=self.listControl.getSelectedItem()
		except:seleccionado = ''
	          
		if seleccionado:

			try: self.getControl(934).setLabel('[B]'+seleccionado.getLabel()+'[/B]')
			except:pass

			try: self.getControl(912).setImage(seleccionado.getProperty('fanart'))
			except: pass
			try: self.getControl(911).setImage(seleccionado.getProperty('fanart'))
			except: pass
			try: self.getControl(910).setImage(seleccionado.getProperty('trophy'))
			except: pass
			try: self.getControl(938).setImage(seleccionado.getProperty('badge'))
			except: pass
			try: self.getControl(939).setImage(seleccionado.getProperty('badge'))
			except: pass
		return
				
	def onClick(self,controlId):
		print "clicou no control id",controlId
		#se clicar no diferente tipo de view
		if controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "League ListView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(listview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("League InfoView")
				self.getControl(983).reset()
				self.getControl(980).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(infoview,1,home)")
				settings.setSetting('view_type_leaguelist','infoview')
				self.controler = 980
			elif active_view_type == "League InfoView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(infoview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("League BannerView")
				self.getControl(980).reset()
				self.getControl(981).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(bannerview,1,home)")
				settings.setSetting('view_type_leaguelist','bannerview')
				self.controler = 981
			elif active_view_type == "League BannerView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(bannerview,Home)")
				xbmc.sleep(200)
				self.getControl(981).reset()
				self.getControl(982).addItems(self.list_listitems)
				self.getControl(controlId).setLabel("League ClearArtView")
				xbmc.executebuiltin("SetProperty(clearview,1,home)")
				settings.setSetting('view_type_leaguelist','clearview')
				self.controler = 982
			elif active_view_type == "League ClearArtView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(clearview,Home)")
				xbmc.sleep(200)
				self.getControl(982).reset()
				self.getControl(984).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("League PanelView")
				xbmc.executebuiltin("SetProperty(panelview,1,home)")
				settings.setSetting('view_type_leaguelist','panelview')
				self.controler = 984
			elif active_view_type == "League PanelView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(panelview,Home)")
				xbmc.sleep(200)
				self.getControl(984).reset()
				self.getControl(983).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("League ListView")
				xbmc.executebuiltin("SetProperty(listview,1,home)")
				settings.setSetting('view_type_leaguelist','listview')
				self.controler = 983
		elif controlId == 983 or controlId == 980 or controlId == 981 or controlId == 982 or controlId == 984:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem()
			season_id = seleccionado.getProperty('season_id')
			league_id = seleccionado.getProperty('league_id')
			#usage start(sport,season,league,team)
			eventlist.start([self.sport,season_id,league_id,''])
			
