import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re
import thesportsdb
from centerutils.common_variables import *
import competlist as competlist

def start(data_list):
	window = dialog_stadium('DialogStadium.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_stadium(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.team = eval(args[3])

	def onInit(self):
		self.stadium_name = thesportsdb.Teams().get_stadium(self.team)
		self.stadium_thumb = thesportsdb.Teams().get_stadium_thumb(self.team)
		print self.stadium_thumb
		self.stadium_plot = thesportsdb.Teams().get_stadium_plot(self.team)
		self.stadium_location = thesportsdb.Teams().get_stadium_location(self.team)
		self.stadium_capacity = thesportsdb.Teams().get_stadium_capacity(self.team)
		
		self.getControl(3).setImage(self.stadium_thumb)
		self.getControl(1).setLabel(self.stadium_name)
		self.getControl(6).setText(self.stadium_plot)
		self.getControl(4).setLabel('[COLOR labelheader]Location:[CR][/COLOR]'+self.stadium_location)
		self.getControl(5).setLabel('[COLOR labelheader]Capacity:[CR][/COLOR]'+self.stadium_capacity)
		

		
		#self.league_id = thesportsdb.Leagues().get_id(self.league)
		

			
	def onClick(self,controlId):
	
		print controlId
	
		if controlId == 983:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem().getProperty('entryid')
			if seleccionado == 'news':
				self.setnewsview()
			elif seleccionado == 'teams':
				if settings.getSetting('view_type_league') == 'bannerview':
					self.setbadgeview()
				elif settings.getSetting('view_type_league')=='badgeview':
					self.setbannerview()
				else:
					self.setbadgeview()
			elif seleccionado == 'home':
					self.setplotview()
			elif seleccionado == 'nextmatch':
					self.setnextmatchview()
			elif seleccionado == 'lastmatch':
					self.setlastmatchview()
			elif seleccionado == 'videos':
					self.setvideosview()

	
		
