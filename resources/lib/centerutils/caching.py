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

from common_variables import *
from downloadtools import *
import os
import xbmcvfs
import threading
from random import randint

#caching variables
_caching_art_folder_ = os.path.join(profilepath,'art')
_caching_leagues_ = os.path.join(profilepath,'leagues')
_caching_teams_ = os.path.join(profilepath,'teams')
_caching_latest_match_ = os.path.join(profilepath,'latestmatch')
_caching_next_match_ = os.path.join(profilepath,'nextmatch')
_caching_livescores_ = os.path.join(profilepath,'livescores')

#Mkdir
if not os.path.isdir(_caching_art_folder_): xbmcvfs.mkdir(_caching_art_folder_)
if not os.path.isdir(_caching_leagues_): xbmcvfs.mkdir(_caching_leagues_)
if not os.path.isdir(_caching_teams_): xbmcvfs.mkdir(_caching_teams_)
if not os.path.isdir(_caching_latest_match_): xbmcvfs.mkdir(_caching_latest_match_)
if not os.path.isdir(_caching_livescores_): xbmcvfs.mkdir(_caching_livescores_)

#functions

def cache_image(url):
	ficheiro = os.path.join(profilepath,_caching_art_folder_,url.split('/')[-1])
	#print url,ficheiro
	if settings.getSetting("enable-caching") == 'true':
		if url and url != 'None':
			if os.path.exists(ficheiro):
				return ficheiro
			else:
				#t1 = threading.Thread('teste', target=Downloader , args=(url,ficheiro,))
				return url
				
		else: return ''
	else: return ficheiro
	
#5-4-1
#4-2-2-2
