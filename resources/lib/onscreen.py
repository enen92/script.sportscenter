import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,os,sys
import thesportsdb
from centerutils.common_variables import *
from centerutils.iofile import *

dialog = xbmcgui.Dialog()

def start(data_list):
	window = dialog_libconfig('DialogOnScreen.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_libconfig(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.home_team_logo = os.path.join(addonpath,art,'benfica.png')
		self.away_team_logo = os.path.join(addonpath,art,'juventus.png')
		self.league_logo = os.path.join(addonpath,art,'premier.png')

	def onInit(self):
		self.set_menu()
		
		
	def set_menu(self,):
		
		menu = []
		
		if settings.getSetting('enable-matchdetails') == 'true':
			menu.append(('Match Details',os.path.join(addonpath,art,'details.png'),'matchdetails'))
			
		if settings.getSetting('enable-homedetails') == 'true':
			menu.append(('Home Team Details',os.path.join(addonpath,art,'details.png'),'homedetails'))
			
		if settings.getSetting('enable-awaydetails') == 'true':
			menu.append(('Away Team Details',os.path.join(addonpath,art,'details.png'),'awaydetails'))
			
		if settings.getSetting('enable-hometwitter') == 'true':
			menu.append(('Home Team Twitter',os.path.join(addonpath,art,'twitter.png'),'hometwitter'))
			
		if settings.getSetting('enable-awaytwitter') == 'true':
			menu.append(('Away Team Twitter',os.path.join(addonpath,art,'twitter.png'),'awaytwitter'))
			
		if settings.getSetting('enable-matchtwitter') == 'true':
			menu.append(('Match Twitter #',os.path.join(addonpath,art,'twitter.png'),'matchtwitter'))
			
		if settings.getSetting('enable-leaguetables') == 'true':
			menu.append(('League Tables',os.path.join(addonpath,art,'stats.png'),'leaguetables'))
		
		if settings.getSetting('enable-livescores') == 'true':
			menu.append(('LiveScores',os.path.join(addonpath,art,'onair.png'),'livescores'))
		
		
		for entry,thumb,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			menu_entry.setProperty('thumb',thumb)
			if entry_id == 'homedetails' or entry_id == 'hometwitter':
				menu_entry.setProperty('subthumb',self.home_team_logo)
			elif entry_id == 'awaydetails' or entry_id == 'awaytwitter':
				menu_entry.setProperty('subthumb',self.away_team_logo)
			elif entry_id == 'matchtwitter' or entry_id == 'matchdetails' or entry_id == 'livescores':
				menu_entry.setProperty('subthumb',os.path.join(addonpath,art,'soccer.png'))
			elif entry_id == 'leaguetables':
				menu_entry.setProperty('subthumb',self.league_logo)
			self.getControl(983).addItem(menu_entry)
		
		return

	def onClick(self,controlId):	
		if controlId == 983:
			entry_id = self.getControl(controlId).getSelectedItem().getProperty('entryid')
			if entry_id == 'livescores':
				import livescores as livescores
				livescores.start(None)
			
			elif entry_id == 'leaguetables':
				import tables as tables
				tables.start('4328')
			
			elif entry_id == 'hometwitter':
				import tweetbuild as tweetbuild
				tweetbuild.tweets(['user','sl_benfica'])
			
			elif entry_id == 'matchtwitter':
				import tweetbuild as tweetbuild
				keyb = xbmc.Keyboard('#', 'Please write the hashtag to assign to this match')
				keyb.doModal()
				if (keyb.isConfirmed()):
					hashtag = keyb.getText()
					tweetbuild.tweets(['hash',hashtag])
				#assign hash to match

			

	
		
