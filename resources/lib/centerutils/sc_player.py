#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
 Author: enen92 

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
"""

import xbmc

class SCPlayer(xbmc.Player):
	def __init__(self,function):
		print("Player has been created")
		self.function = function
            
	def onPlayBackStarted(self):
		pass
                              
	def onPlayBackStopped(self):
		print("player stopped")
		xbmc.executebuiltin(self.function)
		return

	def onPlayBackEnded(self):              
		self.onPlayBackStopped()
		print("playbackended")


