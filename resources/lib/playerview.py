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

import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,datetime
import thesportsdb,feedparser
from random import randint
from centerutils.common_variables import *
from centerutils.youtube import *
from centerutils.sc_instagram import *
from centerutils.rssparser import *
from centerutils.datemanipulation import *
from centerutils.sc_player import *
from centerutils import instagramviewer
import competlist as competlist
import soccermatchdetails as soccermatchdetails
import eventdetails as eventdetails
import stadium as stadium
import tweetbuild as tweetbuild
import imageviewer as imageviewer


def start(player_array):
	window = dialog_playerdetails('DialogPlayerInfo.xml',addonpath,'Default',str(player_array))
	window.doModal()

class dialog_playerdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.player_id = str(eval(args[3])[0])
		self.mode = str(eval(args[3])[1])

	def onInit(self):
		self.player = thesportsdb.Lookups(tsdbkey).lookupplayer(self.player_id)["players"][0]
		#Name
		self.playername = thesportsdb.Players().get_name(self.player)
		self.getControl(223).setLabel(self.playername)
		
		
		#thumb
		self.playerthumb = thesportsdb.Players().get_thumb(self.player)
		if self.playerthumb and self.playerthumb != 'None':
			self.getControl(4).setImage(self.playerthumb)
		#fanart
		self.playerfanart_list = thesportsdb.Players().get_fanart_list(self.player)
		if self.playerfanart_list:
			self.playerfanart = self.playerfanart_list[randint(0,len(self.playerfanart_list)-1)]
			self.getControl(3).setImage(self.playerfanart)
		
		#plot	
		if settings.getSetting('addon-language') == '0':
			self.plot = thesportsdb.Players().get_plot_en(self.player)
		elif settings.getSetting('addon-language') == '1':
			self.plot = thesportsdb.Players().get_plot_de(self.player)
		elif settings.getSetting('addon-language') == '2':
			self.plot = thesportsdb.Players().get_plot_fr(self.player)
		elif settings.getSetting('addon-language') == '3':
			self.plot = thesportsdb.Players().get_plot_it(self.player)
		elif settings.getSetting('addon-language') == '4':
			self.plot = thesportsdb.Players().get_plot_cn(self.player)
		elif settings.getSetting('addon-language') == '5':
			self.plot = thesportsdb.Players().get_plot_jp(self.player)
		elif settings.getSetting('addon-language') == '6':
			self.plot = thesportsdb.Players().get_plot_ru(self.player)
		elif settings.getSetting('addon-language') == '7':
			self.plot = thesportsdb.Players().get_plot_es(self.player)
		elif settings.getSetting('addon-language') == '8':
			self.plot = thesportsdb.Players().get_plot_pt(self.player)
		elif settings.getSetting('addon-language') == '9':
			self.plot = thesportsdb.Players().get_plot_se(self.player)
		elif settings.getSetting('addon-language') == '10':
			self.plot = thesportsdb.Players().get_plot_nl(self.player)
		elif settings.getSetting('addon-language') == '11':
			self.plot = thesportsdb.Players().get_plot_hu(self.player)
		elif settings.getSetting('addon-language') == '12':
			self.plot = thesportsdb.Players().get_plot_no(self.player)
		elif settings.getSetting('addon-language') == '13':
			self.plot = thesportsdb.Players().get_plot_pl(self.player)
		self.getControl(430).setText(self.plot)
		
		#likes
		self.likes = thesportsdb.Players().get_likes(self.player)
		self.getControl(18).setImage(os.path.join(addonpath,'resources','img','like.png'))
		self.getControl(19).setLabel(str(self.likes)+' Users')
		
		#Age
		self.age = thesportsdb.Players().get_borndate(self.player)
		if self.age:
			self.getControl(7).setLabel('[COLOR labelheader]Born:[CR][/COLOR]'+self.age)
		else:
			self.getControl(7).setLabel('[COLOR labelheader]Born:[CR][/COLOR]N/A')
			
		#born location
		self.location = thesportsdb.Players().get_bornlocation(self.player)
		if self.location:
			self.getControl(8).setLabel('[COLOR labelheader]Born location:[CR][/COLOR]'+self.location)
		else:
			self.getControl(8).setLabel('[COLOR labelheader]Born location:[CR][/COLOR]N/A')
			
		#nationality
		self.nationality = thesportsdb.Players().get_nationality(self.player)
		if self.nationality:
			self.getControl(9).setLabel('[COLOR labelheader]Country:[CR][/COLOR]'+self.nationality)
		else:
			self.getControl(9).setLabel('[COLOR labelheader]Country:[CR][/COLOR]N/A')
			
		#team
		self.team = thesportsdb.Players().get_teamname(self.player)
		if self.team:
			self.getControl(10).setLabel('[COLOR labelheader]Team:[CR][/COLOR]'+self.team)
		else:
			self.getControl(10).setLabel('[COLOR labelheader]Team:[CR][/COLOR]N/A')
		
		#position
		self.position = thesportsdb.Players().get_position(self.player)
		if self.position:
			self.getControl(11).setLabel('[COLOR labelheader]Position:[CR][/COLOR]'+self.position)
		else:
			self.getControl(11).setLabel('[COLOR labelheader]Position:[CR][/COLOR]N/A')
		
		#gender
		self.gender = thesportsdb.Players().get_gender(self.player)
		if self.gender:
			self.getControl(12).setLabel('[COLOR labelheader]Gender:[CR][/COLOR]'+self.gender)
		else:
			self.getControl(12).setLabel('[COLOR labelheader]Gender:[CR][/COLOR]N/A')
			
		#Value
		self.value = thesportsdb.Players().get_signedvalue(self.player)
		if self.value:
			self.getControl(13).setLabel('[COLOR labelheader]Value:[CR][/COLOR]'+self.value)
		else:
			self.getControl(13).setLabel('[COLOR labelheader]Value:[CR][/COLOR]N/A')
			
		#signed date
		self.signed_date = thesportsdb.Players().get_signeddate(self.player)
		if self.signed_date:
			self.getControl(14).setLabel('[COLOR labelheader]Signed date:[CR][/COLOR]'+self.signed_date)
		else:
			self.getControl(14).setLabel('[COLOR labelheader]Signed date:[CR][/COLOR]N/A')
		
		#wage
		self.wage = thesportsdb.Players().get_college(self.player)
		if self.wage:
			self.getControl(15).setLabel('[COLOR labelheader]Wage:[CR][/COLOR]'+self.wage)
		else:
			self.getControl(15).setLabel('[COLOR labelheader]Wage:[CR][/COLOR]N/A')	
		
		#height
		self.height = thesportsdb.Players().get_height(self.player)
		if self.height:
			self.getControl(16).setLabel('[COLOR labelheader]Height:[CR][/COLOR]'+self.height)
		else:
			self.getControl(16).setLabel('[COLOR labelheader]Height:[CR][/COLOR]N/A')
		
		#weight
		self.weight = thesportsdb.Players().get_weight(self.player)
		if self.weight:
			self.getControl(17).setLabel('[COLOR labelheader]Weight:[CR][/COLOR]'+self.weight)
		else:
			self.getControl(17).setLabel('[COLOR labelheader]Weight:[CR][/COLOR]N/A')
			
		#Twitter instagram youtube
		self.twitter = thesportsdb.Players().get_twitter(self.player)
		xbmc.executebuiltin("ClearProperty(has_twitter,Home)")
		if self.twitter and self.twitter != 'None': xbmc.executebuiltin("SetProperty(has_twitter,1,home)")
		
		self.youtube = thesportsdb.Players().get_youtube(self.player)
		xbmc.executebuiltin("ClearProperty(has_youtube,Home)")
		if self.youtube and self.youtube != 'None': xbmc.executebuiltin("SetProperty(has_youtube,1,home)")
		
		self.instagram = thesportsdb.Players().get_instagram(self.player)
		xbmc.executebuiltin("ClearProperty(has_instagram,Home)")
		if self.instagram and self.instagram != 'None': xbmc.executebuiltin("SetProperty(has_instagram,1,home)")
		
		if self.mode:
			mode = self.mode
		else:
			mode = 'plotview'
			
		if mode == 'plotview':
			xbmc.executebuiltin("SetProperty(focus_plot,1,home)")
			
		elif mode == 'videoview':
			self.setvideosview()
			
		elif mode == 'imagesview':
			self.setimagesview()
		
	def setimagesview(self,):
		xbmc.executebuiltin("ClearProperty(focus_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(focus_plot,Home)")
		instauser = self.instagram.split('/')[-1]
		if instauser:
			self.getControl(985).reset()
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			self.image_array = get_recent_instagram_images(instauser)
			for caption,thumb,fullscreen in self.image_array:
				image = xbmcgui.ListItem(caption.replace('\n',''))
				image.setProperty('thumb',thumb)
				image.setProperty('fullscreen',fullscreen)
				self.getControl(985).addItem(image)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
		xbmc.executebuiltin("SetProperty(focus_instagram,1,home)")
		
	def setvideosview(self,):
		ytuser = self.youtube.split('/')[-1]
		if ytuser:
			xbmc.executebuiltin("ClearProperty(focus_instagram,Home)")
			xbmc.executebuiltin("ClearProperty(focus_plot,Home)")
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			video_list = return_youtubevideos(ytuser)
			self.getControl(989).reset()
			for video_name,video_id,video_thumb in video_list:
				video = xbmcgui.ListItem(video_name)
				video.setProperty('thumb',video_thumb)
				video.setProperty('video_id',video_id)
				self.getControl(989).addItem(video)
			xbmc.executebuiltin( "Dialog.Close(busydialog)" )
			xbmc.executebuiltin("SetProperty(focus_youtube,1,home)")
			
		
	def onClick(self,controlId):
		if controlId == 211:
			twitter_name = thesportsdb.Players().get_twitter(self.player)
			if twitter_name: 
				twitter_name = twitter_name.split('/')[-1]
				tweetbuild.tweets(['user',twitter_name])
				
		elif controlId == 214:
			imageviewer.view_images(str(self.playerfanart_list))
			
		elif controlId == 210:
			xbmc.executebuiltin("ClearProperty(focus_instagram,Home)")
			xbmc.executebuiltin("ClearProperty(focus_youtube,Home)")
			xbmc.executebuiltin("SetProperty(focus_plot,1,home)")
			
		elif controlId == 212:
			self.setvideosview()
				
		elif controlId == 213:
			self.setimagesview()
			
		elif controlId == 989:
			youtube_id = self.getControl(989).getSelectedItem().getProperty('video_id')
			player = SCPlayer(function="RunScript(script.sportscenter,,/player/"+str(self.player_id)+"/videoview)")
			self.close()
			player.play('plugin://plugin.video.youtube/play/?video_id='+youtube_id)
			while player.isPlaying():
				xbmc.sleep(200)
			
		elif controlId == 985:
			image_std = self.getControl(985).getSelectedItem().getProperty('fullscreen')
			image_description = self.getControl(985).getSelectedItem().getLabel()
			instagramviewer.start(str([image_std,image_description]))
