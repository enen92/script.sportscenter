# -*- coding: utf-8 -*-

""" 
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,os

addon_id = 'script.sportscenter'
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


      
def translate(text):
      return settings.getLocalizedString(text).encode('utf-8')

