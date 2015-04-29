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
from random import randint
import homemenu as home
import thesportsdb
import leagueview as leagueview
import seasonlist as seasonlist
import contextmenubuilder
import eventlist

def start(sportname):
	window = dialog_compet('DialogTeamList.xml',addonpath,'Default',str(sportname))
	window.doModal()
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
	
class dialog_compet(xbmcgui.WindowXML):
    

	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = eval(args[3])[0]

	def onInit(self,):
		self.addteams()
		
	def addteams(self,):
		#set top bar info
		self.getControl(333).setLabel('Teams List - '+urllib.unquote(self.sport))
		
		fanart = os.path.join(addonpath,'fanart.jpg')
		self.getControl(907).setImage(fanart)
		
		#Def das vistas
		xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
		xbmc.executebuiltin("ClearProperty(listview,Home)")
		xbmc.executebuiltin("ClearProperty(panelview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(clearview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.sleep(200)
		
		self.preferred_view = settings.getSetting('view_type_teamlist')

		if self.preferred_view == '' or self.preferred_view == 'listview':
			self.preferred_view = 'listview'
			self.preferred_label = 'Team: ListView'
			self.controler = 983
		
		elif self.preferred_view == 'bannerview':
			self.preferred_label = 'Team: BannerView'
			self.controler = 981
			
		elif self.preferred_view == 'panelview':
			self.preferred_label = 'Team: PanelView'
			self.controler = 984
			
		elif self.preferred_view == 'clearview':
			self.preferred_label = 'Team: ClearArtView'
			self.controler = 982
			
		elif self.preferred_view == 'badgeview':
			self.preferred_label = 'Team: BadgeView'
			self.controler = 980

		elif self.preferred_view == 'jerseyview':
			self.preferred_label = 'Team: JerseyView'
			self.controler = 985
		
		try:
			all_teams = sc_database.Retriever().get_all_teams(self.sport,None,None)
		except: all_teams = []
			
		#print all_leagues
		self.list_listitems = []
		
		if all_teams:
		
			for team in all_teams:
				#get name according to convention
				if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
				else: team_name = thesportsdb.Teams().get_alternativefirst(team)	
				
				teamItem = xbmcgui.ListItem(team_name, iconImage = thesportsdb.Teams().get_badge(team))
				team_id = thesportsdb.Teams().get_id(team)
				teamItem.setProperty('team_id', team_id)
				teamItem.setProperty('year', thesportsdb.Teams().get_formedyear(team))
				teamItem.setProperty('sport', thesportsdb.Teams().get_sport(team))
				teamItem.setProperty('country', thesportsdb.Teams().get_country(team))
				teamItem.setProperty('league_id', thesportsdb.Teams().get_league_id(team))
				#manipulate languages here
				if settings.getSetting('addon-language') == '0':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_en(team))
				elif settings.getSetting('addon-language') == '1':	
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_de(team))
				elif settings.getSetting('addon-language') == '2':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_fr(team))
				elif settings.getSetting('addon-language') == '3':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_it(team))
				elif settings.getSetting('addon-language') == '4':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_cn(team))
				elif settings.getSetting('addon-language') == '5':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_jp(team))	
				elif settings.getSetting('addon-language') == '6':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_ru(team))
				elif settings.getSetting('addon-language') == '7':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_es(team))	
				elif settings.getSetting('addon-language') == '8':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_pt(team))
				elif settings.getSetting('addon-language') == '9':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_se(team))
				elif settings.getSetting('addon-language') == '10':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_nl(team))
				elif settings.getSetting('addon-language') == '11':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_hu(team))
				elif settings.getSetting('addon-language') == '12':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_no(team))
				elif settings.getSetting('addon-language') == '13':
					teamItem.setProperty('plot', thesportsdb.Teams().get_plot_pl(team))	
				
				fanart = thesportsdb.Teams().get_fanart_general_list(team)
				if len(fanart) >= 1: teamItem.setProperty('fanart', fanart[randint(0,len(fanart)-1)])
				else: teamItem.setProperty('fanart',os.path.join(addonpath,art,'sports',self.sport + '.jpg'))
				player_fanart = thesportsdb.Teams().get_fanart_player(team)
				if not player_fanart:
					fan_fanart = thesportsdb.Teams().get_fanart_fans(team)
					if not fan_fanart: player_fanart = fanart
					else: player_fanart = fan_fanart

				teamItem.setProperty('badge', thesportsdb.Teams().get_badge(team))
				teamItem.setProperty('jersey', thesportsdb.Teams().get_team_jersey(team))
				teamItem.setProperty('banner', thesportsdb.Teams().get_banner(team))
				teamItem.setProperty('player_fanart', player_fanart)
				teamItem.setProperty('clear', thesportsdb.Teams().get_logo(team))
				teamItem.setProperty('team_object',str(team))
				self.list_listitems.append(teamItem)
			
			
		xbmc.sleep(200)	
		self.getControl(self.controler).addItems(self.list_listitems)
			
		number_of_teams=len(self.list_listitems)
		self.getControl(334).setLabel(str(number_of_teams) + ' '+'Teams') #TODO string
		
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
			elif xbmc.getCondVisibility("Control.HasFocus(985)"): container = 985
			self.specific_id = self.getControl(container).getSelectedItem().getProperty('team_id')
			contextmenubuilder.start(['teamlist-lib',self.specific_id])	
		else:
			self.set_info()
		
	def set_info(self):
		active_view_type = self.getControl(2).getLabel()
		if active_view_type == "Team: BadgeView":
			self.controler = 980
			self.listControl = self.getControl(self.controler)
		if active_view_type == "Team: ListView":
			self.controler = 983
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "Team: BannerView":
			self.controler = 981
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "Team: ClearArtView":
			self.controler = 982
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "Team: PanelView":
			self.controler = 984
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "Team: JerseyView":
			self.controler = 985
			self.listControl = self.getControl(self.controler)
		
		try:seleccionado=self.listControl.getSelectedItem()
		except:seleccionado = ''
	          
		if seleccionado:

			try: self.getControl(934).setLabel('[B]'+seleccionado.getLabel()+'[/B]')
			except:pass
			try: self.getControl(935).setLabel(seleccionado.getProperty('year'))
			except: pass
			try: self.getControl(936).setLabel(seleccionado.getProperty('country'))
			except: pass
			try: self.getControl(937).setText(seleccionado.getProperty('plot'))
			except: pass
			try: self.getControl(912).setImage(seleccionado.getProperty('fanart'))
			except: pass
			try: self.getControl(911).setImage(seleccionado.getProperty('player_fanart'))
			except: pass
			try: self.getControl(954).setImage(seleccionado.getProperty('player_fanart'))
			except: pass
			try: self.getControl(910).setImage(seleccionado.getProperty('jersey'))
			except: pass
			try: self.getControl(953).setImage(seleccionado.getProperty('badge'))
			except: pass
			try: self.getControl(908).setImage(seleccionado.getProperty('clear'))
			except: pass
			try: self.getControl(938).setImage(seleccionado.getProperty('badge'))
			except: pass
			try: self.getControl(939).setImage(seleccionado.getProperty('badge'))
			except: pass
		return
				
	def onClick(self,controlId):
		#se clicar no diferente tipo de view
		if controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "Team: ListView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(listview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("Team: BadgeView")
				self.getControl(983).reset()
				self.getControl(980).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(badgeview,1,home)")
				settings.setSetting('view_type_teamlist','badgeview')
				self.controler = 980
			elif active_view_type == "Team: BadgeView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(badgeview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("Team: JerseyView")
				self.getControl(980).reset()
				self.getControl(985).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(jerseyview,1,home)")
				settings.setSetting('view_type_teamlist','jerseyview')
				self.controler = 985
			elif active_view_type == "Team: JerseyView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("Team: BannerView")
				self.getControl(980).reset()
				self.getControl(981).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(bannerview,1,home)")
				settings.setSetting('view_type_teamlist','bannerview')
				self.controler = 981				
			elif active_view_type == "Team: BannerView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(bannerview,Home)")
				xbmc.sleep(200)
				self.getControl(981).reset()
				self.getControl(982).addItems(self.list_listitems)
				self.getControl(controlId).setLabel("Team: ClearArtView")
				xbmc.executebuiltin("SetProperty(clearview,1,home)")
				settings.setSetting('view_type_teamlist','clearview')
				self.controler = 982
			elif active_view_type == "Team: ClearArtView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(clearview,Home)")
				xbmc.sleep(200)
				self.getControl(982).reset()
				self.getControl(984).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("Team: PanelView")
				xbmc.executebuiltin("SetProperty(panelview,1,home)")
				settings.setSetting('view_type_teamlist','panelview')
				self.controler = 984
			elif active_view_type == "Team: PanelView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(panelview,Home)")
				xbmc.sleep(200)
				self.getControl(984).reset()
				self.getControl(983).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("Team: ListView")
				xbmc.executebuiltin("SetProperty(listview,1,home)")
				settings.setSetting('view_type_teamlist','listview')
				self.controler = 983
		elif controlId == 983 or controlId == 980 or controlId == 981 or controlId == 982 or controlId == 984:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem()
			team_id = seleccionado.getProperty('team_id')
			league_id = seleccionado.getProperty('league_id')
			if self.sport != 'motorsport':
				eventlist.start([self.sport,"","",team_id])
			else:
				eventlist.start([self.sport,"",league_id,""])
			
