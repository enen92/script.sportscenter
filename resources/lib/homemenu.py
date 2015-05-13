import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import os,time,urllib
from centerutils.common_variables import *
from centerutils.iofile import *
from centerutils.datemanipulation import *
from centerutils.database import sc_database
import competlist as competlist
import teamview as teamview
import seasonlist as seasonlist
import teamlist as teamlist
import eventlist as eventlist
import libconfig as libconfig
from wizzard import wizzard


def start(focus_sport):
	if not focus_sport: focus_sport = 'soccer'
	window = dialog_home('DialogMainMenu.xml',addonpath,'Default',focus_sport)
	window.doModal()
	
class dialog_home(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = args[3]
		self.has_diff_submenu = ""
		
		#note simple hack to avoid flickering and set the submenu when launching the plugin
		self.initfanart = False
		self.initsubmenu = False 

	def onInit(self):
		self.focused_sport = 'soccer'
		table = []
		if settings.getSetting('enable-football') == 'true':
			table.append(('Football','soccer.png','soccer'))
		if settings.getSetting('enable-rugby') == 'true':
			table.append(('Rugby','rugby.png','rugby'))
		if settings.getSetting('enable-motorsport') == 'true':
			table.append(('MotorSport','motorsport.png','motorsport'))
		if settings.getSetting('enable-basketball') == 'true':
			table.append(('Basketball','basketball.png','basketball'))
		if settings.getSetting('enable-amfootball') == 'true':
			table.append(('AM Football','americanfootball.png','american%20football'))
		if settings.getSetting('enable-icehockey') == 'true':
			table.append(('Ice Hockey','ice%20hockey.png','ice%20hockey'))
		if settings.getSetting('enable-baseball') == 'true':
			table.append(('Baseball','baseball.png','baseball'))
		if settings.getSetting('enable-golf') == 'true':
			table.append(('Golf','golf.png','golf'))
			   
		for sport,img,sport_name in table:
			item = xbmcgui.ListItem(sport, iconImage = os.path.join(addonpath,art,img))
			item.setProperty('sport_clearlogo', os.path.join(addonpath,art,img))
			item.setProperty('sport_name', sport_name)
			self.getControl(980).addItem(item)
		
		self.getControl(912).setImage(os.path.join(addonpath,'fanart.jpg'))
		
		
		
		#set top panel visible false before running the wizzard
		self.getControl(501).setVisible(False)
		self.getControl(502).setVisible(False)
		wizzard()
		
		self.setFocusId(980)
		
		i=0
		for sport,img,sport_name in table:
			if sport_name == self.sport:
				index = i
			else: i+=1
		try:self.getControl(980).selectItem(index)
		except: self.getControl(980).selectItem(1)
		xbmc.sleep(200)
		
		self.set_fanart()
		self.set_favourite_data()
		self.set_submenu()

	
	def set_favourite_data(self):
		
		if os.path.exists(sport_fav_file):
			#Set top panel visible
			self.getControl(501).setVisible(True)
			self.getControl(502).setVisible(True)
			
			
			self.focused_sport = ''
			self.favourite_sport = readfile(sport_fav_file)
			#check if wraplist has focus
			if xbmc.getCondVisibility("Control.HasFocus(980)"):
				self.focused_sport = self.getControl(980).getSelectedItem().getProperty('sport_name')
				#assign self.sport variable to current focused sport. This parameter will be passed when calling dialog team
				self.sport = self.focused_sport
				#check if a file of favourite team of the selected sport exists
				if self.focused_sport.lower() == 'soccer' or self.focused_sport.lower() == 'football':
					if not os.path.isfile(football_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'basketball':
					if not os.path.isfile(basketball_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'rugby':
					if not os.path.isfile(rugby_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'american%20football':
					if not os.path.isfile(amfootball_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'motorsport':
					if not os.path.isfile(motorsport_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'ice%20hockey':
					if not os.path.isfile(icehockey_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'baseball':
					if not os.path.isfile(baseball_fav_file): self.focused_sport = self.favourite_sport
				elif self.focused_sport.lower() == 'golf':
					if not os.path.isfile(golf_fav_file): self.focused_sport = self.favourite_sport				
			else: self.focused_sport = self.favourite_sport
				
		#Set data accordingly
		if self.focused_sport:
		
			#initialize variables
			favourite_team_name = ''
			favourite_team_id = ''
			favourite_logo = ''
			
			
			if self.focused_sport.lower() == 'soccer' or self.focused_sport.lower() == 'football':	
				if os.path.isfile(football_fav_file):
					sport_data = eval(readfile(football_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('football-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('football-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
						
			elif self.focused_sport.lower() == 'basketball':
				if os.path.isfile(basketball_fav_file):
					sport_data = eval(readfile(basketball_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('basketball-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('basketball-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
			
			elif self.focused_sport.lower() == 'rugby':
				if os.path.isfile(rugby_fav_file):
					sport_data = eval(readfile(rugby_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('rugby-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('rugby-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
					
			elif self.focused_sport.lower() == 'american%20football':
				if os.path.isfile(amfootball_fav_file):
					sport_data = eval(readfile(amfootball_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('amfootball-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('amfootball-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)

				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
					
			elif self.focused_sport.lower() == 'motorsport':
				if os.path.isfile(motorsport_fav_file):
					sport_data = eval(readfile(motorsport_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('motorsport-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('motorsport-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
					
			elif self.focused_sport.lower() == 'ice%20hockey':
				if os.path.isfile(icehockey_fav_file):
					sport_data = eval(readfile(icehockey_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3].lower()
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('icehockey-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('icehockey-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
					
			elif self.focused_sport.lower() == 'baseball':
				if os.path.isfile(baseball_fav_file):
					sport_data = eval(readfile(baseball_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('baseball-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('baseball-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
					
			elif self.focused_sport.lower() == 'golf':
				if os.path.isfile(golf_fav_file):
					sport_data = eval(readfile(golf_fav_file))
					favourite_team_name = sport_data[1]
					favourite_team_id = sport_data[0]
					favourite_logo = sport_data[2]
					favourite_team_sport = sport_data[3]
					favourite_team_fan_fanart = sport_data[4]
					favourite_team_logo_fanart = sport_data[5]
					if os.path.exists(os.path.join(favlogos,favourite_logo.split('/')[-1])):
						favourite_logo = os.path.join(favlogos,favourite_logo.split('/')[-1])
					#set fan fanart or logo fanart for favourite teams
					now_focused = self.getControl(980).getSelectedItem().getProperty('sport_name').lower()
					if settings.getSetting('golf-background') == '2':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_fan_fanart and favourite_team_fan_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])):
									favourite_team_fan_fanart = os.path.join(favlogos,favourite_team_fan_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_fan_fanart)
						
					elif settings.getSetting('golf-background') == '3':
						if now_focused.lower() == self.focused_sport.lower():
							if favourite_team_logo_fanart and favourite_team_logo_fanart != 'None':
								if os.path.isfile(os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])):
									favourite_team_logo_fanart = os.path.join(favlogos,favourite_team_logo_fanart.split('/')[-1])
								self.getControl(913).setImage(favourite_team_logo_fanart)
				if xbmc.getCondVisibility("Control.HasFocus(980)"):
					self.current_focus = self.getControl(980).getSelectedItem().getProperty('sport_name')
					if self.current_focus.lower() != self.focused_sport.lower():
						setting_sport = get_sport_setting(self.current_focus)
						if setting_sport:
							setting_sport = setting_sport + "-background"
							if str(settings.getSetting(setting_sport)) != '1' and str(settings.getSetting(setting_sport)) != '4':
								self.getControl(913).setImage(addon_fanart)
				

			#set favourite info
			if favourite_team_name:
				self.getControl(983).reset()
				item = xbmcgui.ListItem(favourite_team_name)
				if ' ' in favourite_team_name:
					if len(favourite_team_name) > 12: item.setProperty('favourite_name_long', '[B]'+favourite_team_name+'[/B]')
					else: item.setProperty('favourite_name_short', '[B]'+favourite_team_name+'[/B]')			
				else:
					item.setProperty('favourite_name_short', '[B]'+favourite_team_name+'[/B]')
				if favourite_logo: item.setProperty('favourite_logo', favourite_logo)
				if favourite_team_id: item.setProperty('favourite_id',favourite_team_id)
				if favourite_team_sport: item.setProperty('favourite_team_sport',favourite_team_sport)
				if settings.getSetting('username') != '': item.setProperty('username',settings.getSetting('username'))
				self.getControl(983).addItem(item)		
		return
		
	def set_fanart(self):
		#here the addon only sets the custom addon sport fanart or any custom fanart defined on the addon settings
		if xbmc.getCondVisibility("Control.HasFocus(980)"):
			sport = self.getControl(980).getSelectedItem().getProperty('sport_name')
			if sport != self.sport or not self.initfanart:
				self.initfanart = True
				self.sport = sport
			
				if self.sport == 'soccer' or self.sport == 'football':
					if settings.getSetting('football-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','soccer.jpg'))
					elif settings.getSetting('football-background') == '4':
						football_custom = settings.getSetting('football-custom')
						if football_custom != '':
							self.getControl(913).setImage(football_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('football-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'basketball':
					if settings.getSetting('basketball-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','basketball.jpg'))
					elif settings.getSetting('basketball-background') == '4':
						basketball_custom = settings.getSetting('basketball-custom')
						if basketball_custom != '':
							self.getControl(913).setImage(basketball_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('basketball-background') == '0':self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'rugby':
					if settings.getSetting('rugby-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','rugby.jpg'))
					elif settings.getSetting('rugby-background') == '4':
						rugby_custom = settings.getSetting('rugby-custom')
						if rugby_custom != '':
							self.getControl(913).setImage(rugby_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('rugby-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'american%20football':
					if settings.getSetting('amfootball-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','american%20football.jpg'))
					elif settings.getSetting('amfootball-background') == '4':
						amfootball_custom = settings.getSetting('amfootball-custom')
						if amfootball_custom != '':
							self.getControl(913).setImage(amfootball_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('amfootball-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'motorsport':
					if settings.getSetting('motorsport-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','motorsport.jpg'))
					elif settings.getSetting('motorsport-background') == '4':
						motorsport_custom = settings.getSetting('motorsport-custom')
						if motorsport_custom != '':
							self.getControl(913).setImage(motorsport_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('motorsport-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'ice%20hockey':
					if settings.getSetting('icehockey-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','ice%20hockey.jpg'))
					elif settings.getSetting('icehockey-background') == '4':
						icehockey_custom = settings.getSetting('icehockey-custom')
						if icehockey_custom != '':
							self.getControl(913).setImage(icehockey_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('icehockey-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'baseball':
					if settings.getSetting('baseball-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','baseball.jpg'))
					elif settings.getSetting('baseball-background') == '4':
						baseball_custom = settings.getSetting('baseball-custom')
						if baseball_custom != '':
							self.getControl(913).setImage(baseball_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('baseball-background') == '0': self.getControl(913).setImage(addon_fanart)
				
				elif self.sport == 'golf':
					if settings.getSetting('golf-background') == '1':
						self.getControl(913).setImage(os.path.join(addonpath,art,'sports','golf.jpg'))
					elif settings.getSetting('golf-background') == '4':
						golf_custom = settings.getSetting('golf-custom')
						if golf_custom != '':
							self.getControl(913).setImage(golf_custom)
						else: self.getControl(913).setImage(addon_fanart)
					elif settings.getSetting('golf-background') == '0': self.getControl(913).setImage(addon_fanart)
		return

	def set_submenu(self):
		#menu entries
		has_library = [('Leagues','leagues'),('Seasons','seasons'),('Teams','teams'),('Events','events'),('Configure','configure')]
		no_library = [('Configure','configure')]
		#
		sport = self.getControl(980).getSelectedItem().getProperty('sport_name')
		if sport != self.sport or not self.initsubmenu:
			self.sport = sport
			self.initsubmenu = True
			if self.sport == 'soccer' or self.sport == 'football':
				library = haslibrary_football
			elif self.sport == 'basketball':
				library = haslibrary_basketball
			elif self.sport == 'rugby':
				library = haslibrary_rugby
			elif self.sport == 'american%20football':
				library = haslibrary_amfootball
			elif self.sport == 'motorsport':
				library = haslibrary_motorsport
			elif self.sport == 'ice%20hockey':
				library = os.path.exists(icehockey_library)
			elif self.sport == 'baseball':
				library = haslibrary_baseball
			elif self.sport == 'golf':
				library = haslibrary_golf
			if library:
				if self.has_diff_submenu == 'has_library': #self.has_diff_submenu can only have 'has_library' or 'no_library' as values
					pass
				else:
					self.getControl(9010).reset()
					for menu_label,menu_key in has_library:
						menu_item = xbmcgui.ListItem(menu_label)
						menu_item.setProperty('menu_key',menu_key)
						self.getControl(9010).addItem(menu_item)
					self.has_diff_submenu == 'has_library'
			else:
				if self.has_diff_submenu == 'no_library':
					pass
				else:
					self.getControl(9010).reset()
					for menu_label,menu_key in no_library:
						menu_item = xbmcgui.ListItem(menu_label)
						menu_item.setProperty('menu_key',menu_key)
						self.getControl(9010).addItem(menu_item)
					self.has_diff_submenu == 'no_library'
		
		
		
		
		return
			
	def onClick(self,controlId):
		if controlId == 980:
			listControl = self.getControl(980)
			seleccionado=listControl.getSelectedItem()
			#usage -> competlist.start(['sport','True for library False for Current Season'])
			if self.sport == 'soccer' or self.sport == 'football':
				library = settings.getSetting('football-home-item')
			elif self.sport == 'basketball':
				library = settings.getSetting('basketball-home-item')
			elif self.sport == 'rugby':
				library = settings.getSetting('rugby-home-item')
			elif self.sport == 'american%20football':
				library = settings.getSetting('amfootball-home-item')
			elif self.sport == 'motorsport':
				library = settings.getSetting('motorsport-home-item')
			elif self.sport == 'ice%20hockey':
				library = settings.getSetting('icehockey-home-item')
			elif self.sport == 'baseball':
				library = settings.getSetting('baseball-home-item')
			elif self.sport == 'golf':
				library = settings.getSetting('golf-home-item')
			if library == '0':
				competlist.start([seleccionado.getProperty('sport_name'),False])
			else:
				competlist.start([self.sport,True])
		elif controlId == 983:
			self.team_id = self.getControl(983).getSelectedItem().getProperty('favourite_id')
			self.favteam_sport = urllib.quote(self.getControl(983).getSelectedItem().getProperty('favourite_team_sport').lower())
			teamview.start([self.team_id,self.favteam_sport,'','plotview'])
		elif controlId == 9024:
			from resources.lib import livescores as livescores
			livescores.start(None)
		elif controlId == 9023:
			from resources.lib import calendar as calendar
			calendar.start(None)
		elif controlId == 9022:
			settings.openSettings()
		elif controlId == 9010:
			key = self.getControl(9010).getSelectedItem().getProperty('menu_key')
			if key == 'leagues':
				#usage -> competlist.start(['sport','True for library False for Current Season'])
				competlist.start([self.sport,True])
			elif key == 'seasons':
				#usage -> seasonlist.start(['sport','None for all seasons league id for seasons of a league',fanart = none to get a new one])
				seasonlist.start([self.sport,'',''])
			elif key == 'teams':
				teamlist.start([self.sport])
			elif key == 'events':
				#usage start(sport,season,league,team)
				eventlist.start([self.sport,'','',''])
			elif key == 'configure':
				libconfig.start([self.sport])

			
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.close()
		else:
			if xbmc.getCondVisibility("Control.HasFocus(980)"):
				self.set_submenu()
				self.set_fanart()
				self.set_favourite_data()
