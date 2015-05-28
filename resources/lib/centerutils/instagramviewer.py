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

import xbmc
import xbmcgui
from common_variables import *

def start(data_list):
	window = dialog_instagram('DialogInstagram.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_instagram(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.image = eval(args[3])[0]
		self.label = eval(args[3])[1]

	def onInit(self):
		self.getControl(3).setImage(self.image)
		self.getControl(6).setText(self.label)
