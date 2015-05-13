# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from centerutils.common_variables import *

def view_images(image_array):
	window = dialog_viewimage('DialogFullscreenimage.xml',addonpath,'Default',image_array)
	window.doModal()

class dialog_viewimage(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.image_array = eval(args[3])

	def onInit(self):
		if self.image_array:
			self.actual_img = self.image_array[0]
			self.getControl(901).setImage(os.path.join(addonpath,art,'black.jpg'))
			self.getControl(900).setImage(self.actual_img)
		
	def onAction(self,action):
		if action.getId() == 92 or action == 'PreviousMenu':
			self.close()
		elif action.getId() == 2:
			#set next image
			self.i = 0
			for i in xrange(0,len(self.image_array)-1):
				if self.image_array[i] == self.actual_img:
					self.i=i+1
					break
			#case
			if self.i > len(self.image_array)-1:
				self.actual_img = self.image_array[0]
				self.i = 0
			else:
				self.actual_img = self.image_array[self.i]
			self.getControl(900).setImage(self.actual_img)

		elif action.getId() == 1:
			#set next image
			for i in xrange(0,len(self.image_array)):
				if self.image_array[i] == self.actual_img:
					self.i=i-1
					break
			#case
			if self.i >= 0:
				self.actual_img = self.image_array[self.i]
			else:
				self.actual_img = self.image_array[len(self.image_array)-1]
				self.i = len(self.image_array)-1
			self.getControl(900).setImage(self.actual_img)
					
			
