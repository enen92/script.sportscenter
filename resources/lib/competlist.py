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

def start(sportname):
	window = dialog_compet('DialogCompetList.xml',addonpath,'Default',str(sportname))
	window.doModal()
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
	
class dialog_compet(xbmcgui.WindowXML):
    

	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = eval(args[3])[0]
		self.is_library = eval(args[3])[1]
		#self.fanart = eval(args[3])[2]
		if not self.is_library:
			self.ignored_leagues = os.listdir(ignoredleaguesfolder)

	def onInit(self,):
		if not self.is_library:
			threading.Thread(name='watcher', target=self.watcher).start()
		self.addleagues()
		
	def watcher(self,):
		while not xbmc.abortRequested:
			ignored_leagues = os.listdir(ignoredleaguesfolder)
			fav_leagues = os.listdir(favleaguesfolder)
			if self.ignored_leagues != ignored_leagues:
				self.ignored_leagues = ignored_leagues
				self.getControl(983).reset()
				self.getControl(981).reset()
				self.getControl(984).reset()
				self.getControl(982).reset()
				self.getControl(980).reset()
				self.addleagues()
			xbmc.sleep(200)
	
	def addleagues(self,):
		#set top bar info
		self.getControl(333).setLabel('Competition List - '+urllib.unquote(self.sport))
		
		fanart = os.path.join(addonpath,'fanart.jpg')
	
		self.getControl(907).setImage(fanart)
		
		#Def das vistas
		xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
		xbmc.executebuiltin("ClearProperty(listview,Home)")
		xbmc.executebuiltin("ClearProperty(panelview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(clearview,Home)")
		xbmc.executebuiltin("ClearProperty(infoview,Home)")
		xbmc.sleep(200)
		
		self.preferred_view = settings.getSetting('view_type_leaguelist')

		if self.preferred_view == '' or self.preferred_view == 'listview':
			self.preferred_view = 'listview'
			self.preferred_label = 'League ListView'
			self.controler = 983
		
		elif self.preferred_view == 'bannerview':
			self.preferred_label = 'League BannerView'
			self.controler = 981
			
		elif self.preferred_view == 'panelview':
			self.preferred_label = 'League PanelView'
			self.controler = 984
			
		elif self.preferred_view == 'clearview':
			self.preferred_label = 'League ClearArtView'
			self.controler = 982
			
		elif self.preferred_view == 'infoview':
			self.preferred_label = 'League InfoView'
			self.controler = 980
		
		if not self.is_library: #Current season information
			try: all_leagues = thesportsdb.Search(tsdbkey).search_all_leagues(None,self.sport,None)["countrys"]
			except: all_leagues = []
		else: #internal library information
			try:
				all_leagues = sc_database.Retriever().get_all_leagues(self.sport,None)
			except: all_leagues = []
			
		#print all_leagues
		self.list_listitems = []
		
		if all_leagues:
		
			for league in all_leagues:
				leagueItem = xbmcgui.ListItem(thesportsdb.Leagues().get_name(league), iconImage = thesportsdb.Leagues().get_badge(league))
				league_id = thesportsdb.Leagues().get_id(league)
				leagueItem.setProperty('league_id', league_id)
				leagueItem.setProperty('year', thesportsdb.Leagues().get_formedyear(league))
				leagueItem.setProperty('sport', thesportsdb.Leagues().get_sport(league))
				leagueItem.setProperty('country', thesportsdb.Leagues().get_country(league))
				#manipulate languages here
				if settings.getSetting('addon-language') == '0':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_en(league))
				elif settings.getSetting('addon-language') == '1':	
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_de(league))
				elif settings.getSetting('addon-language') == '2':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_fr(league))
				elif settings.getSetting('addon-language') == '3':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_it(league))
				elif settings.getSetting('addon-language') == '4':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_cn(league))
				elif settings.getSetting('addon-language') == '5':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_jp(league))	
				elif settings.getSetting('addon-language') == '6':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_ru(league))
				elif settings.getSetting('addon-language') == '7':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_es(league))	
				elif settings.getSetting('addon-language') == '8':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_pt(league))
				elif settings.getSetting('addon-language') == '9':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_se(league))
				elif settings.getSetting('addon-language') == '10':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_nl(league))
				elif settings.getSetting('addon-language') == '11':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_hu(league))
				elif settings.getSetting('addon-language') == '12':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_no(league))
				elif settings.getSetting('addon-language') == '13':
					leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_pl(league))	
				
				fanart = thesportsdb.Leagues().get_fanart(league)
				if len(fanart) >= 1: leagueItem.setProperty('fanart', fanart[randint(0,len(fanart)-1)])
				else: leagueItem.setProperty('fanart', os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
				leagueItem.setProperty('badge', thesportsdb.Leagues().get_badge(league))
				leagueItem.setProperty('banner', thesportsdb.Leagues().get_banner(league))
				leagueItem.setProperty('clear', thesportsdb.Leagues().get_logo(league))
				leagueItem.setProperty('trophy', thesportsdb.Leagues().get_trophy(league))
				leagueItem.setProperty('league_object',str(league))
			
				if not self.is_library:
					if (league_id + '.txt') not in self.ignored_leagues:
						self.list_listitems.append(leagueItem)
				else: self.list_listitems.append(leagueItem)
			
		xbmc.sleep(200)	
		self.getControl(self.controler).addItems(self.list_listitems)
			
		number_of_leagues=len(self.list_listitems)
		self.getControl(334).setLabel(str(number_of_leagues) + ' '+'Leagues') #TODO string
		
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
			self.specific_id = self.getControl(container).getSelectedItem().getProperty('league_id')
			contextmenubuilder.start(['leaguelist-lib',self.specific_id])	
		else:
			self.set_info()
		
	def set_info(self):
		active_view_type = self.getControl(2).getLabel()
		if active_view_type == "League InfoView":
			self.controler = 980
			self.listControl = self.getControl(self.controler)
		if active_view_type == "League ListView":
			self.controler = 983
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "League BannerView":
			self.controler = 981
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "League ClearArtView":
			self.controler = 982
			self.listControl = self.getControl(self.controler)
		elif active_view_type == "League PanelView":
			self.controler = 984
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
			try: self.getControl(911).setImage(seleccionado.getProperty('fanart'))
			except: pass
			try: self.getControl(910).setImage(seleccionado.getProperty('trophy'))
			except: pass
			try: self.getControl(954).setImage(seleccionado.getProperty('trophy'))
			except: pass
			try: self.getControl(908).setImage(seleccionado.getProperty('clear'))
			except: pass
			try: self.getControl(938).setImage(seleccionado.getProperty('badge'))
			except: pass
			try: self.getControl(939).setImage(seleccionado.getProperty('badge'))
			except: pass
		return
				
	def onClick(self,controlId):
		print "clicou no control id",controlId
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
			league_object = seleccionado.getProperty('league_object')
			league_fanart = seleccionado.getProperty('fanart')
			try: league_id = thesportsdb.Leagues().get_id(eval(league_object))
			except: league_id = ''
			if not self.is_library:
				leagueview.start([league_object,self.sport,league_fanart,'plotview'])
			else:
				if league_id:
					seasonlist.start([self.sport,league_id,league_fanart])
			
