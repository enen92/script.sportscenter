#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from centerutils.common_variables import *
from random import randint
import homemenu as home
import thesportsdb

def start(sportname):
	window = dialog_compet('DialogCompetList.xml',addonpath,'Default',sportname)
	window.doModal()
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
	
class dialog_compet(xbmcgui.WindowXMLDialog):
    

	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = args[3]
		

	def onInit(self,):
		fanart = os.path.join(addonpath,'fanart.jpg')
	
		self.getControl(912).setImage(fanart)
		try: all_leagues = thesportsdb.Search().search_all_leagues(None,self.sport,None)["countrys"]
		except: all_leagues = {}
		self.list_listitems = []
		
		for league in all_leagues:
			stream = xbmcgui.ListItem(thesportsdb.Leagues().get_name(league), iconImage = thesportsdb.Leagues().get_badge(league))
			stream.setProperty('year', thesportsdb.Leagues().get_formedyear(league))
			stream.setProperty('sport', thesportsdb.Leagues().get_sport(league))
			stream.setProperty('country', thesportsdb.Leagues().get_country(league))
			stream.setProperty('plot', thesportsdb.Leagues().get_plot_en(league))
			fanart = thesportsdb.Leagues().get_fanart(league)
			if len(fanart) >= 1: stream.setProperty('fanart', fanart[randint(0,len(fanart)-1)])
			else: stream.setProperty('fanart', os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
			stream.setProperty('badge', thesportsdb.Leagues().get_badge(league))
			stream.setProperty('banner', thesportsdb.Leagues().get_banner(league))
			stream.setProperty('clear', thesportsdb.Leagues().get_logo(league))
			stream.setProperty('trophy', thesportsdb.Leagues().get_trophy(league))
			self.list_listitems.append(stream)
			
		#xbmc.sleep(200)	
		self.getControl(983).addItems(self.list_listitems)
		
		#Def das vistas
		#self.setFocusId(980)
		xbmc.executebuiltin("ClearProperty(panelview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(clearview,Home)")
		xbmc.executebuiltin("ClearProperty(infoview,Home)")
		xbmc.executebuiltin("SetProperty(listview,1,home)")

		self.getControl(2).setLabel("League ListView")
		xbmc.sleep(100)
		#select 1st item
		self.setFocusId(983)
		self.getControl(983).selectItem(0)
		self.set_info()
			
	def onAction(self,action):
		self.control_panel = xbmc.getCondVisibility("IsEmpty(Window(home).Property(MediaMenu))")
		if action == 92:
			if not self.control_panel: 
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(980)
			else: 
				self.close()
				home.start(self.sport)		
		else:
			self.set_info()
		
	def set_info(self):
		active_view_type = self.getControl(2).getLabel()
		if active_view_type == "League InfoView":
			listControl = self.getControl(980)
		if active_view_type == "League ListView":
			listControl = self.getControl(983)
		elif active_view_type == "League BannerView":
			listControl = self.getControl(981)
		elif active_view_type == "League ClearArtView":
			listControl = self.getControl(982)
		elif active_view_type == "League PanelView":
			listControl = self.getControl(984)
		seleccionado=listControl.getSelectedItem()
		print "select",seleccionado
		print "seleccionado image",seleccionado.getProperty('fanart')
		          
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
			elif active_view_type == "League InfoView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(infoview,Home)")
				xbmc.sleep(200)
				self.getControl(controlId).setLabel("League BannerView")
				self.getControl(980).reset()
				self.getControl(981).addItems(self.list_listitems)
				xbmc.executebuiltin("SetProperty(bannerview,1,home)")
			elif active_view_type == "League BannerView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(bannerview,Home)")
				xbmc.sleep(200)
				self.getControl(981).reset()
				self.getControl(982).addItems(self.list_listitems)
				self.getControl(controlId).setLabel("League ClearArtView")
				xbmc.executebuiltin("SetProperty(clearview,1,home)")
			elif active_view_type == "League ClearArtView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(clearview,Home)")
				xbmc.sleep(200)
				self.getControl(982).reset()
				self.getControl(984).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("League PanelView")
				xbmc.executebuiltin("SetProperty(panelview,1,home)")
			elif active_view_type == "League PanelView":
				xbmc.sleep(200)
				xbmc.executebuiltin("ClearProperty(panelview,Home)")
				xbmc.sleep(200)
				self.getControl(984).reset()
				self.getControl(983).addItems(self.list_listitems)
				xbmc.executebuiltin("XBMC.Container.Refresh")
				self.getControl(controlId).setLabel("League ListView")
				xbmc.executebuiltin("SetProperty(listview,1,home)")
