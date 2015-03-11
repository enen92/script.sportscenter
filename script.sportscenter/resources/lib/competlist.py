#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from centerutils.common_variables import *
from random import randint
import homemenu as home
import thesportsdb
import leagueview as leagueview

def start(sportname):
	window = dialog_compet('DialogCompetList.xml',addonpath,'Default',sportname)
	window.doModal()
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
	
class dialog_compet(xbmcgui.WindowXML):
    

	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = args[3]
		

	def onInit(self,):
		#set top bar info
		self.getControl(333).setLabel('Competition List - '+self.sport)
		
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
			
		try: all_leagues = thesportsdb.Search().search_all_leagues(None,self.sport,None)["countrys"]
		except: all_leagues = {}
		self.list_listitems = []
		number_of_leagues=len(all_leagues)
		self.getControl(334).setLabel(str(number_of_leagues) + ' Leagues')
		
		for league in all_leagues:
			leagueItem = xbmcgui.ListItem(thesportsdb.Leagues().get_name(league), iconImage = thesportsdb.Leagues().get_badge(league))
			leagueItem.setProperty('year', thesportsdb.Leagues().get_formedyear(league))
			leagueItem.setProperty('sport', thesportsdb.Leagues().get_sport(league))
			leagueItem.setProperty('country', thesportsdb.Leagues().get_country(league))
			leagueItem.setProperty('plot', thesportsdb.Leagues().get_plot_en(league))
			fanart = thesportsdb.Leagues().get_fanart(league)
			if len(fanart) >= 1: leagueItem.setProperty('fanart', fanart[randint(0,len(fanart)-1)])
			else: leagueItem.setProperty('fanart', os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
			leagueItem.setProperty('badge', thesportsdb.Leagues().get_badge(league))
			leagueItem.setProperty('banner', thesportsdb.Leagues().get_banner(league))
			leagueItem.setProperty('clear', thesportsdb.Leagues().get_logo(league))
			leagueItem.setProperty('trophy', thesportsdb.Leagues().get_trophy(league))
			leagueItem.setProperty('league_object',str(league))
			self.list_listitems.append(leagueItem)
			
		xbmc.sleep(200)	
		self.getControl(self.controler).addItems(self.list_listitems)
			
		
		xbmc.executebuiltin("SetProperty("+self.preferred_view+",1,home)")
		self.getControl(2).setLabel(self.preferred_label)
		xbmc.sleep(100)
		#select 1st item
		self.setFocusId(self.controler)
		self.getControl(self.controler).selectItem(0)
		self.set_info()
		
		
			
	def onAction(self,action):
		if action.getId() == 92:
			self.control_panel = xbmc.getCondVisibility("!IsEmpty(Window(home).Property(MediaMenu))")
			if self.control_panel:
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(self.controler)
			else: 
				self.close()
				#home.start(self.sport)		
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
		seleccionado=self.listControl.getSelectedItem()
	          
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
			try: self.getControl(908).setImage(seleccionado.getProperty('clear'))
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
			league_object = seleccionado.getProperty('league_object')
			#self.close()
			leagueview.start([league_object,self.sport])
			
