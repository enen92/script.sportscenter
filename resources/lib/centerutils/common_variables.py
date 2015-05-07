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

""" 
   	
"""
    
import xbmc
import xbmcplugin
import xbmcvfs
import xbmcgui 
import xbmcaddon
import os
import pytzimp

addon_id = 'script.sportscenter'
tsdbkey = '5261590715995'
art = os.path.join("resources","img")
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
version = settings.getAddonInfo('version')
profilepath= xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
MainURL = 'http'
addon_icon = settings.getAddonInfo('icon')
addon_fanart = os.path.join(addonpath,'fanart.jpg')
dialog = xbmcgui.Dialog()

#Timezones
my_timezone = settings.getSetting('timezone')
my_location = pytzimp.timezone(pytzimp.all_timezones[int(my_timezone)])
tsdbtimezone = 'Atlantic/Azores'

#Internal database variables
sc_database = os.path.join(profilepath,'sc_database.sql')
database_userdata = os.path.join(profilepath,'database')
if not os.path.isdir(database_userdata): xbmcvfs.mkdir(database_userdata)

football_library = os.path.join(database_userdata,'football.txt')
if os.path.exists(football_library):
	haslibrary_football = True
else:
	haslibrary_football = False
basketball_library = os.path.join(database_userdata,'basketball.txt')
if os.path.exists(basketball_library):
	haslibrary_basketball = True
else:
	haslibrary_basketball = False
icehockey_library = os.path.join(database_userdata,'icehockey.txt')
if os.path.exists(icehockey_library):
	haslibrary_icehockey = True
else:
	haslibrary_icehockey = True
baseball_library = os.path.join(database_userdata,'baseball.txt')
if os.path.exists(baseball_library):
	haslibrary_baseball = True
else:
	haslibrary_baseball = False
motorsport_library = os.path.join(database_userdata,'motorsport.txt')
if os.path.exists(motorsport_library):
	haslibrary_motorsport = True
else:
	haslibrary_motorsport = False
rugby_library = os.path.join(database_userdata,'rugby.txt')
if os.path.exists(rugby_library):
	haslibrary_rugby = True
else:
	haslibrary_rugby = False
golf_library = os.path.join(database_userdata,'golf.txt')
if os.path.exists(golf_library):
	haslibrary_golf = True
else:
	haslibrary_golf = False
amfootball_library = os.path.join(database_userdata,'amfootball.txt')
if os.path.exists(amfootball_library):
	haslibrary_amfootball = True
else:
	haslibrary_amfootball = False
	
#onscreen variables	
onscreen_userdata = os.path.join(profilepath,'onscreen')
if not os.path.isdir(onscreen_userdata): xbmcvfs.mkdir(onscreen_userdata)
onscreen_userdata_teams = os.path.join(profilepath,'onscreen','teams')
if not os.path.isdir(onscreen_userdata_teams): xbmcvfs.mkdir(onscreen_userdata_teams)
onscreen_userdata_leagues = os.path.join(profilepath,'onscreen','leagues')
if not os.path.isdir(onscreen_userdata_leagues): xbmcvfs.mkdir(onscreen_userdata_leagues)
onscreen_livescores = os.path.join(profilepath,'onscreen','livescores.txt')
onscreen_playingmatch = os.path.join(profilepath,'onscreen','playingmatch.txt')

#Wizzard variables
football_file = os.path.join(profilepath,'football.txt')
football_fav_file = os.path.join(profilepath,'football_fav.txt')
basketball_file = os.path.join(profilepath,'basketball.txt')
basketball_fav_file = os.path.join(profilepath,'basketball_fav.txt')
rugby_file = os.path.join(profilepath,'rugby.txt')
rugby_fav_file = os.path.join(profilepath,'rugby_fav.txt')
amfootball_file = os.path.join(profilepath,'amfootball.txt')
amfootball_fav_file = os.path.join(profilepath,'amfootball_fav.txt')
icehockey_file = os.path.join(profilepath,'icehockey.txt')
icehockey_fav_file = os.path.join(profilepath,'icehockey_fav.txt')
baseball_file = os.path.join(profilepath,'baseball.txt')
baseball_fav_file = os.path.join(profilepath,'baseball_fav.txt')
golf_file = os.path.join(profilepath,'golf.txt')
golf_fav_file = os.path.join(profilepath,'golf_fav.txt')
motorsport_file = os.path.join(profilepath,'motorsport.txt')
motorsport_fav_file = os.path.join(profilepath,'motorsport_fav.txt')
sport_fav_file = os.path.join(profilepath,'sport_fav.txt')
favlogos = os.path.join(profilepath,'favlogos')
contextfolder = os.path.join(profilepath,'user_settings')
ignoredleaguesfolder = os.path.join(contextfolder,'ignoredleagues')
favleaguesfolder = os.path.join(contextfolder,'favleagues')
ignoreleaguecalendar = os.path.join(contextfolder,'igncalendar')
ignoreleaguelivescores = os.path.join(contextfolder,'ignlivescores')
if not os.path.isdir(contextfolder): xbmcvfs.mkdir(contextfolder)
if not os.path.isdir(ignoredleaguesfolder): xbmcvfs.mkdir(ignoredleaguesfolder)
if not os.path.isdir(favleaguesfolder): xbmcvfs.mkdir(favleaguesfolder)
if not os.path.isdir(ignoreleaguecalendar): xbmcvfs.mkdir(ignoreleaguecalendar)
if not os.path.isdir(ignoreleaguelivescores): xbmcvfs.mkdir(ignoreleaguelivescores)

def translate(text):
      return settings.getLocalizedString(text).encode('utf-8')

