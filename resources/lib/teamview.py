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
import urllib,re,datetime,os
import thesportsdb,feedparser
from random import randint
from centerutils.common_variables import *
from centerutils.youtube import *
from centerutils.rssparser import *
from centerutils.datemanipulation import *
from centerutils.sc_instagram import *
from centerutils.sc_player import *
from centerutils import instagramviewer
import competlist as competlist
import soccermatchdetails as soccermatchdetails
import eventdetails as eventdetails
import stadium as stadium
import tweetbuild as tweetbuild
import imageviewer as imageviewer
import playerview as playerview


def teamdetails(team_id):
	window = dialog_teamdetails('DialogTeamInfo.xml',addonpath,'Default',team_id)
	window.doModal()

class dialog_teamdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.team_id = str(eval(args[3])[0])
		self.mode = str(eval(args[3])[1])
		
		self.event_last_list = thesportsdb.Schedules(tsdbkey).eventslast(self.team_id)['results']
		self.event_next_list = thesportsdb.Schedules(tsdbkey).eventsnext(self.team_id)['events']

	def onInit(self):
		self.team = thesportsdb.Lookups(tsdbkey).lookupteam(self.team_id)['teams'][0]
		if settings.getSetting('team-naming')=='0': self.team_name = thesportsdb.Teams().get_name(self.team)
		else: self.team_name = thesportsdb.Teams().get_alternativefirst(self.team)		
		self.team_badge = thesportsdb.Teams().get_badge(self.team)
		self.team_fanartlist = thesportsdb.Teams().get_fanart_list(self.team) 
		self.team_fanart = thesportsdb.Teams().get_fanart_general1(self.team)
		self.team_stadiumfanart = thesportsdb.Teams().get_stadium_thumb(self.team)
		self.team_clear = thesportsdb.Teams().get_logo(self.team)
		self.team_jersey = thesportsdb.Teams().get_team_jersey(self.team)
		self.founded = thesportsdb.Teams().get_formedyear(self.team)
		self.twitter = thesportsdb.Teams().get_team_twitter(self.team)
		
		if settings.getSetting('addon-language') == '0':
			self.plot = thesportsdb.Teams().get_plot_en(self.team)
		elif settings.getSetting('addon-language') == '1':
			self.plot = thesportsdb.Teams().get_plot_de(self.team)
		elif settings.getSetting('addon-language') == '2':
			self.plot = thesportsdb.Teams().get_plot_fr(self.team)
		elif settings.getSetting('addon-language') == '3':
			self.plot = thesportsdb.Teams().get_plot_it(self.team)
		elif settings.getSetting('addon-language') == '4':
			self.plot = thesportsdb.Teams().get_plot_cn(self.team)
		elif settings.getSetting('addon-language') == '5':
			self.plot = thesportsdb.Teams().get_plot_jp(self.team)
		elif settings.getSetting('addon-language') == '6':
			self.plot = thesportsdb.Teams().get_plot_ru(self.team)
		elif settings.getSetting('addon-language') == '7':
			self.plot = thesportsdb.Teams().get_plot_es(self.team)
		elif settings.getSetting('addon-language') == '8':
			self.plot = thesportsdb.Teams().get_plot_pt(self.team)
		elif settings.getSetting('addon-language') == '9':
			self.plot = thesportsdb.Teams().get_plot_se(self.team)
		elif settings.getSetting('addon-language') == '10':
			self.plot = thesportsdb.Teams().get_plot_nl(self.team)
		elif settings.getSetting('addon-language') == '11':
			self.plot = thesportsdb.Teams().get_plot_hu(self.team)
		elif settings.getSetting('addon-language') == '12':
			self.plot = thesportsdb.Teams().get_plot_no(self.team)
		elif settings.getSetting('addon-language') == '13':
			self.plot = thesportsdb.Teams().get_plot_pl(self.team)
		
		
		self.sport = thesportsdb.Teams().get_sport(self.team)
		self.manager = thesportsdb.Teams().get_manager(self.team)
		self.stadium_name = thesportsdb.Teams().get_stadium(self.team)
		self.location = thesportsdb.Teams().get_stadium_location(self.team)
		self.league = thesportsdb.Teams().get_league(self.team)
		self.likes = thesportsdb.Teams().get_likes(self.team)
		self.league_id = thesportsdb.Teams().get_league_id(self.team)
		self.youtube = thesportsdb.Teams().get_team_youtube(self.team)
		self.instagram = thesportsdb.Teams().get_team_instagram(self.team)
		#get league table data
		table_list = thesportsdb.Lookups(tsdbkey).lookup_leaguetables(self.league_id,None)["table"]
		self.position = 0
		#detect position
		dict_to_order = {}
		if table_list:
			for team in table_list:
				self.position += 1
				if self.team_id == thesportsdb.Tables().get_id(team): break

			if self.position != 0:
				self.getControl(309).setLabel('[B]'+get_position_string(self.position)+'[/B]')
		
		if self.likes == 'None': self.likes = '0'
		
		self.getControl(1).setLabel(self.team_name)
		if self.team_badge and self.team_badge != 'None':
			self.getControl(2).setImage(self.team_badge)
		if self.team_fanart and self.team_fanart != 'None':
			self.getControl(3).setImage(self.team_fanart)
		if self.team_stadiumfanart and self.team_stadiumfanart != 'None':
			self.getControl(4).setImage(self.team_stadiumfanart)
		if self.team_clear and self.team_clear != 'None':
			self.getControl(5).setImage(self.team_clear)
		if self.team_jersey and self.team_jersey != 'None':
			self.getControl(6).setImage(self.team_jersey)
		self.getControl(7).setLabel('[COLOR labelheader]Founded:[CR][/COLOR]'+self.founded)
		self.getControl(430).setText(self.plot)
		self.getControl(8).setLabel('[COLOR labelheader]Sport:[CR][/COLOR]'+self.sport)
		self.getControl(9).setLabel('[COLOR labelheader]Manager:[CR][/COLOR]'+self.manager)
		self.getControl(10).setLabel('[COLOR labelheader]Stadium:[CR][/COLOR]'+self.stadium_name)
		self.getControl(11).setLabel('[COLOR labelheader]Location:[CR][/COLOR]'+self.location)
		self.getControl(12).setLabel('[COLOR labelheader]League:[CR][/COLOR]'+self.league)
		
		self.getControl(18).setImage(os.path.join(addonpath,'resources','img','like.png'))
		self.getControl(19).setLabel(str(self.likes)+' Users')
		
		#set next match information
		if self.event_next_list:
			self.nextevent = self.event_next_list[0]
			if self.sport.lower() != 'motorsport':
				self.hometeam = thesportsdb.Events().get_hometeamid(self.nextevent)
				self.awayteam = thesportsdb.Events().get_awayteamid(self.nextevent)
				self.home_away = ''
				if self.team_id == self.hometeam:
					self.home_away = 'HOME'
					self.searchid = thesportsdb.Events().get_awayteamid(self.nextevent)
				else:
					self.home_away = 'AWAY'
					self.searchid = thesportsdb.Events().get_hometeamid(self.nextevent)
				self.getControl(41).setLabel(self.home_away)
				try:
					self.nexteam = thesportsdb.Lookups(tsdbkey).lookupteam(self.searchid)['teams'][0]
					self.nextlogo = thesportsdb.Teams().get_badge(self.nexteam)
					self.getControl(40).setImage(self.nextlogo)
				except: pass
			else:
				self.getControl(40).setImage(os.path.join(addonpath,art,'raceflag.png'))
				self.location = thesportsdb.Events().get_racelocation(self.nextevent)
				if self.location and self.location != 'None' and self.location != 'null':
					self.getControl(46).setLabel(self.location)
				self.getControl(44).setVisible(False)
			#datestuff is independent from the sport
			try:
				#date
				self.nextdate = thesportsdb.Events().get_datetime_object(self.nextevent)
				if self.nextdate:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(self.nextdate)
					self.nextdate=db_time.astimezone(my_location)
				#next date
				#day difference is calculated here
				if self.nextdate:
					now = datetime.datetime.now()
					datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
					datenow =  pytz.timezone(str(pytz.timezone(str(my_location)))).localize(datenow)
					day_difference = abs(self.nextdate - datenow).days
					if day_difference == 0:
						string = 'Today'
					elif day_difference == 1:
						string = 'Tomorrow'
					else:
						string = 'In ' + str(day_difference) + ' days'
				else: string = ''
				self.getControl(42).setLabel(string)

				if self.nextdate:
					fmt = "%H:%M"
					self.event_time = self.nextdate.strftime(fmt)
					self.getControl(45).setLabel(self.event_time)
			except: pass


		
		i = 0
		controlinicial = 30
		winnumber = 0
		if self.event_last_list and self.event_last_list != 'None':
			for event in self.event_last_list:
				awayteam = thesportsdb.Events().get_awayteamid(event)
				hometeam = thesportsdb.Events().get_hometeamid(event)
				awayscore = thesportsdb.Events().get_awayscore(event)
				homescore = thesportsdb.Events().get_homescore(event)
				if hometeam == self.team_id:
					if int(homescore) > int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greensquare.png'))
						self.getControl(controlinicial+i+1).setLabel('W')
						winnumber += 1
					elif int(homescore) < int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','redsquare.png'))
						self.getControl(controlinicial+i+1).setLabel('L')
					else:
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greysquare.png'))
						self.getControl(controlinicial+i+1).setLabel('D')
				else:
					if int(homescore) > int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','redsquare.png'))
						self.getControl(controlinicial+i+1).setLabel('L')
					elif int(homescore) < int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greensquare.png'))
						self.getControl(controlinicial+i+1).setLabel('W')
						winnumber += 1
					else:
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greysquare.png'))
						self.getControl(controlinicial+i+1).setLabel('D')
				i += 2
			winpercentage = float(winnumber)/5*100 
			self.getControl(43).setLabel(str(int(winpercentage))+'% WINS')
			self.getControl(44).setPercent(int(winpercentage))

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
		
		
		#check if twitter,youtube and instagram exists
		xbmc.executebuiltin("ClearProperty(hasteam_instagram,Home)")
		xbmc.executebuiltin("ClearProperty(hasteam_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(hasteam_twitter,Home)")
		if self.youtube and self.youtube != 'None': xbmc.executebuiltin("SetProperty(hasteam_youtube,1,home)")
		if self.instagram and self.instagram != 'None': xbmc.executebuiltin("SetProperty(hasteam_instagram,1,home)")
		if self.twitter and self.twitter != 'None': xbmc.executebuiltin("SetProperty(hasteam_twitter,1,home)")

	def setvideosview(self,):
		ytuser = self.youtube.split('/')[-1]
		if ytuser:
			xbmc.executebuiltin("ClearProperty(focusteam_instagram,Home)")
			xbmc.executebuiltin("ClearProperty(focusteam_plot,Home)")
			xbmc.executebuiltin("ClearProperty(focusteam_events,Home)")
			xbmc.executebuiltin("ClearProperty(focusteam_players,Home)")
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			video_list = return_youtubevideos(ytuser)
			self.getControl(989).reset()
			for video_name,video_id,video_thumb in video_list:
				video = xbmcgui.ListItem(video_name)
				video.setProperty('thumb',video_thumb)
				video.setProperty('video_id',video_id)
				self.getControl(989).addItem(video)
			xbmc.executebuiltin( "Dialog.Close(busydialog)" )
			xbmc.executebuiltin("SetProperty(focusteam_youtube,1,home)")
			
	def setimagesview(self,):
		xbmc.executebuiltin("ClearProperty(focusteam_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_plot,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_events,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_players,Home)")
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
		xbmc.executebuiltin("SetProperty(focusteam_instagram,1,home)")
		
	def setplayersview(self,):
		xbmc.executebuiltin("ClearProperty(focusteam_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_plot,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_events,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_instagram,Home)")
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		self.players = thesportsdb.Lookups(tsdbkey).lookup_all_players(self.team_id)['player']
		if self.players:
			for player in self.players:
				player_name = thesportsdb.Players().get_name(player)
				player_thumb = thesportsdb.Players().get_face_first(player)
				player_id = thesportsdb.Players().get_id(player)
				playeritem = xbmcgui.ListItem(player_name)
				if player_thumb:
					playeritem.setProperty('thumb',player_thumb)
				else:
					playeritem.setProperty('thumb',os.path.join(addonpath,art,'noface.png'))
				playeritem.setProperty('player_id',player_id)
				self.getControl(987).addItem(playeritem)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
		xbmc.executebuiltin("SetProperty(focusteam_players,1,home)")
		
	def setplotview(self,):
		xbmc.executebuiltin("ClearProperty(focusteam_instagram,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_events,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_players,Home)")
		xbmc.sleep(100)
		xbmc.executebuiltin("SetProperty(focusteam_plot,1,home)")
		return
		
	def seteventsview(self,):
		xbmc.executebuiltin("ClearProperty(focusteam_youtube,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_plot,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_players,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_events,Home)")
		xbmc.executebuiltin("ClearProperty(focusteam_instagram,Home)")
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		next_events = ''
		if self.event_next_list and self.event_next_list != 'None':
			for event in self.event_next_list:
				if self.sport.lower() != 'motorsport':
					home = thesportsdb.Events().get_hometeamname(event)
					away = thesportsdb.Events().get_awayteamname(event)
					event_title = home + ' vs ' + away + '\n'
					next_events = next_events + event_title
				else:
					evntx = thesportsdb.Events().get_eventtitle(event)
					event_title = evntx + '\n'
					next_events = next_events + event_title
			self.getControl(471).setText(next_events)
		last_events = ''
		if self.event_last_list and self.event_last_list != 'None':
			for event in self.event_last_list:
				if self.sport.lower() != 'motorsport':
					home = thesportsdb.Events().get_hometeamname(event)
					away = thesportsdb.Events().get_awayteamname(event)
					homescore = str(thesportsdb.Events().get_homescore(event))
					awayscore = str(thesportsdb.Events().get_awayscore(event))
					event_title = home + ' '+homescore + '-' + awayscore + ' ' + away + '\n'
					last_events = last_events + event_title
				else:
					evntx = thesportsdb.Events().get_eventtitle(event)
					event_title = evntx + '\n'
					last_events = last_events + event_title
			self.getControl(470).setText(last_events)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
		xbmc.executebuiltin("SetProperty(focusteam_events,1,home)")

	def onClick(self,controlId):
		if controlId == 210:
			stadium.start(self.team)
			
		elif controlId == 213:
			twitter_name = thesportsdb.Teams().get_team_twitter(self.team)
			if twitter_name: 
				twitter_name = twitter_name.split('/')[-1]
				tweetbuild.tweets(['user',twitter_name])
				
		elif controlId == 216:
			imageviewer.view_images(str(self.team_fanartlist))
		
		elif controlId == 214:
			self.setvideosview()
			
		elif controlId == 209:
			self.setplotview()
			
		elif controlId == 215:
			self.setimagesview()
			
		elif controlId == 212:
			self.setplayersview()
			
		elif controlId == 211:
			self.seteventsview()
		
		elif controlId == 987:
			player_id = self.getControl(987).getSelectedItem().getProperty('player_id')
			playerview.start([player_id,'plotview'])
			
		elif controlId == 985:
			image_std = self.getControl(985).getSelectedItem().getProperty('fullscreen')
			image_description = self.getControl(985).getSelectedItem().getLabel()
			instagramviewer.start(str([image_std,image_description]))
			
		elif controlId == 989:
			youtube_id = self.getControl(989).getSelectedItem().getProperty('video_id')
			player = SCPlayer(function="RunScript(script.sportscenter,,/teamdetails/"+str(self.team_id)+"/videoview)")
			self.close()
			player.play('plugin://plugin.video.youtube/play/?video_id='+youtube_id)
			while player.isPlaying():
				xbmc.sleep(200)
			



def start(data_list):
	window = dialog_team('DialogTeam.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_team(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.team_id = eval(args[3])[0]
		self.sport = eval(args[3])[1]
		self.team_fanart = eval(args[3])[2]
		self.mode = eval(args[3])[3]
		self.team = thesportsdb.Lookups(tsdbkey).lookupteam(self.team_id)['teams'][0]
		self.event_next_list = thesportsdb.Schedules(tsdbkey).eventsnext(self.team_id)['events']
		

	def onInit(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		self.getControl(911).setImage(os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
		
		#set team badge
		self.team_badge = thesportsdb.Teams().get_badge(self.team)
		if self.team_badge: self.getControl(934).setImage(self.team_badge)
		
		self.getControl(983).reset()
		#populate panel left
					
		#set team fanart
		if not self.team_fanart:
			self.team_fanartlist = thesportsdb.Teams().get_fanart_general_list(self.team)
			if self.team_fanartlist:
				self.team_fanart = self.team_fanartlist[randint(0,len(self.team_fanartlist)-1)]
			else: self.team_fanart = os.path.join(addonpath,art,'sports',self.sport+'.jpg')
		self.getControl(912).setImage(self.team_fanart)

		self.player_fanart = thesportsdb.Teams().get_fanart_player(self.team)
		if self.player_fanart:
			self.getControl(429).setImage(self.player_fanart)
		else:
			self.getControl(429).setImage(self.team_fanart)
			
		self.team_stadium = thesportsdb.Teams().get_stadium(self.team)
		self.team_rss = thesportsdb.Teams().get_rssurl(self.team)
		self.team_youtube = thesportsdb.Teams().get_team_youtube(self.team)
		self.team_twitter = thesportsdb.Teams().get_team_twitter(self.team)
			
		#set team view menu
		menu = [('Home','home'),('Team Details','details')]
		
		if self.team_rss and self.team_rss != 'None':
			menu.append(('News','news'))
			
		if self.team_twitter and self.team_twitter != 'None':
			menu.append(('Tweets','tweets'))
			
		if self.team_youtube and self.team_youtube != 'None':
			menu.append(('Videos','videos'))
		
		if self.sport.lower() == 'motorsport':
			menu.append(('Racers','players'))
		elif self.sport.lower() == 'golf':
			menu.append(('Golfers','players'))
		else:	
			menu.append(('Players','players'))
	
		if self.team_stadium and self.team_stadium != 'None':
			menu.append(('Stadium','stadium'))
			
		if self.event_next_list and self.event_next_list != 'None':
			menu.append(('Fixtures','nextmatch'))
		
		menu.append(('Results','lastmatch'))
		
		self.getControl(983).reset()
			   
		for entry,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			self.getControl(983).addItem(menu_entry)
		
		#initialize view
		if self.mode and self.mode != 'None':
			mode = self.mode
		else:
			mode = settings.getSetting('view_type_team')
		
		if mode == 'plotview' or mode == '':
			self.setplotview()
		elif mode == 'playersview':
			self.setplayersview()
		elif mode == 'setnewsview':
			self.newsview()
		elif mode == 'nextmatchview':
			self.setnextmatchview()
		elif mode == 'lastmatchview':
			self.setlastmatchview()
		elif mode == 'videosview':
			self.setvideosview()
		else:
			self.setplotview()
			
	def setplotview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")

		
		#set team plot
		if settings.getSetting('addon-language') == '0':
			self.team_plot = thesportsdb.Teams().get_plot_en(self.team)
		elif settings.getSetting('addon-language') == '1':
			self.team_plot = thesportsdb.Teams().get_plot_de(self.team)
		elif settings.getSetting('addon-language') == '2':
			self.team_plot = thesportsdb.Teams().get_plot_fr(self.team)
		elif settings.getSetting('addon-language') == '3':
			self.team_plot = thesportsdb.Teams().get_plot_it(self.team)
		elif settings.getSetting('addon-language') == '4':
			self.team_plot = thesportsdb.Teams().get_plot_cn(self.team)
		elif settings.getSetting('addon-language') == '5':
			self.team_plot = thesportsdb.Teams().get_plot_jp(self.team)
		elif settings.getSetting('addon-language') == '6':
			self.team_plot = thesportsdb.Teams().get_plot_ru(self.team)
		elif settings.getSetting('addon-language') == '7':
			self.team_plot = thesportsdb.Teams().get_plot_es(self.team)
		elif settings.getSetting('addon-language') == '8':
			self.team_plot = thesportsdb.Teams().get_plot_pt(self.team)
		elif settings.getSetting('addon-language') == '9':
			self.team_plot = thesportsdb.Teams().get_plot_se(self.team)
		elif settings.getSetting('addon-language') == '10':
			self.team_plot = thesportsdb.Teams().get_plot_nl(self.team)
		elif settings.getSetting('addon-language') == '11':
			self.team_plot = thesportsdb.Teams().get_plot_hu(self.team)
		elif settings.getSetting('addon-language') == '12':
			self.team_plot = thesportsdb.Teams().get_plot_no(self.team)
		elif settings.getSetting('addon-language') == '13':
			self.team_plot = thesportsdb.Teams().get_plot_pl(self.team)
		
		self.getControl(430).setText(self.team_plot)
		
		#set team formed year
		self.team_formedyear = thesportsdb.Teams().get_formedyear(self.team)
		self.getControl(428).setLabel('[COLOR labelheader]Established:[CR][/COLOR]' + self.team_formedyear)
		
		#set team name
		if settings.getSetting('team-naming')=='0': self.team_name = thesportsdb.Teams().get_name(self.team)
		else: self.team_name = thesportsdb.Teams().get_alternativefirst(self.team)
		self.getControl(427).setLabel('[COLOR labelheader]Team Name:[CR][/COLOR]' + self.team_name)
		
		#set top bar info
		self.getControl(333).setLabel("Team View - "+self.team_name)
		
			
		#set next match information
		if self.event_next_list:
			self.nextevent = self.event_next_list[0]
			if self.sport.lower() != 'motorsport':
				self.hometeam = thesportsdb.Events().get_hometeamid(self.nextevent)
				self.awayteam = thesportsdb.Events().get_awayteamid(self.nextevent)
				self.home_away = ''
				if self.team_id == self.hometeam:
					self.home_away = 'HOME'
					self.searchid = thesportsdb.Events().get_awayteamid(self.nextevent)
				else:
					self.home_away = 'AWAY'
					self.searchid = thesportsdb.Events().get_hometeamid(self.nextevent)
				self.getControl(41).setLabel(self.home_away)
				try:
					self.nexteam = thesportsdb.Lookups(tsdbkey).lookupteam(self.searchid)['teams'][0]
					self.nextlogo = thesportsdb.Teams().get_badge(self.nexteam)
					self.getControl(40).setImage(self.nextlogo)
				except: pass
			else:
				self.getControl(40).setImage(os.path.join(addonpath,art,'raceflag.png'))
				self.location = thesportsdb.Events().get_racelocation(self.nextevent)
				if self.location and self.location != 'None' and self.location != 'null':
					self.getControl(45).setLabel(self.location)
			
			#datestuff is independent from the sport
			try:
				#date
				self.nextdate = thesportsdb.Events().get_datetime_object(self.nextevent)
				if self.nextdate:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(self.nextdate)
					self.nextdate=db_time.astimezone(my_location)
				#next date
				#day difference is calculated here
				if self.nextdate:
					now = datetime.datetime.now()
					datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
					datenow =  pytz.timezone(str(pytz.timezone(str(my_location)))).localize(datenow)
					day_difference = abs(self.nextdate - datenow).days
					if day_difference == 0:
						string = 'Today'
					elif day_difference == 1:
						string = 'Tomorrow'
					else:
						string = 'In ' + str(day_difference) + ' days'
				else: string = ''
				self.getControl(42).setLabel(string)

				if self.nextdate:
					fmt = "%H:%M"
					self.event_time = self.nextdate.strftime(fmt)
					self.getControl(43).setLabel(self.event_time)
			except: pass
			
		
		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(playersview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(plotview,1,home)")
		settings.setSetting("view_type_team",'plotview')
		self.mode = ''

		self.getControl(2).setLabel("Team: PlotView")
		#select first item only if mediamenu is not active
		if not xbmc.getCondVisibility("Control.HasFocus(2)"):
			self.setFocusId(983)
			self.getControl(983).selectItem(0)
		
	def setplayersview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		players = thesportsdb.Lookups(tsdbkey).lookup_all_players(self.team_id)['player']
		if players:
			number_players=len(players)
			
			#set player number top bar
			self.getControl(334).setLabel(str(number_players)+' '+'Players')
			
			for player in players:
				player_face = thesportsdb.Players().get_face(player)
				player_name = thesportsdb.Players().get_name(player)
				player_id = thesportsdb.Players().get_id(player)
				player_fanart_list = thesportsdb.Players().get_fanart_list(player)
				player_position = thesportsdb.Players().get_position(player)
				player_twitter = thesportsdb.Players().get_twitter(player)
				try:player_value = thesportsdb.Players().get_signedvalue(player).encode('utf-8').replace('&pound;','£')
				except:player_value = 'N/A'
				player_age = str(thesportsdb.Players().get_borndate(player))
				player_location = thesportsdb.Players().get_bornlocation(player)
				player_height = thesportsdb.Players().get_height(player)
				player_weight = thesportsdb.Players().get_weight(player)
				
				#player plot different languages
				if settings.getSetting('addon-language') == '0':
					player_plot = thesportsdb.Players().get_plot_en(player)
				elif settings.getSetting('addon-language') == '1':
					player_plot = thesportsdb.Players().get_plot_de(player)
				elif settings.getSetting('addon-language') == '2':
					player_plot = thesportsdb.Players().get_plot_fr(player)
				elif settings.getSetting('addon-language') == '3':
					player_plot = thesportsdb.Players().get_plot_it(player)
				elif settings.getSetting('addon-language') == '4':
					player_plot = thesportsdb.Players().get_plot_cn(player)
				elif settings.getSetting('addon-language') == '5':
					player_plot = thesportsdb.Players().get_plot_jp(player)
				elif settings.getSetting('addon-language') == '6':
					player_plot = thesportsdb.Players().get_plot_ru(player)
				elif settings.getSetting('addon-language') == '7':
					player_plot = thesportsdb.Players().get_plot_es(player)
				elif settings.getSetting('addon-language') == '8':
					player_plot = thesportsdb.Players().get_plot_pt(player)
				elif settings.getSetting('addon-language') == '9':
					player_plot = thesportsdb.Players().get_plot_se(player)
				elif settings.getSetting('addon-language') == '10':
					player_plot = thesportsdb.Players().get_plot_nl(player)
				elif settings.getSetting('addon-language') == '11':
					player_plot = thesportsdb.Players().get_plot_hu(player)
				elif settings.getSetting('addon-language') == '12':
					player_plot = thesportsdb.Players().get_plot_no(player)
				elif settings.getSetting('addon-language') == '13':
					player_plot = thesportsdb.Players().get_plot_pl(player)
				

				if player_fanart_list: player_fanart = player_fanart_list[randint(0,len(player_fanart_list))-1]
				else: player_fanart = ''
				playeritem = xbmcgui.ListItem(player_name)
				if player_face and player_face != 'None':
					playeritem.setProperty('player_cutout',player_face)
				else: playeritem.setProperty('player_cutout',os.path.join(addonpath,art,'noface.png'))
				playeritem.setProperty('player_fanart',player_fanart)
				playeritem.setProperty('player_name',player_name)
				playeritem.setProperty('player_position',player_position)
				playeritem.setProperty('player_value',player_value)
				playeritem.setProperty('player_age',player_age)
				playeritem.setProperty('player_id',player_id)
				playeritem.setProperty('player_location',player_location)
				playeritem.setProperty('player_height',player_height)
				playeritem.setProperty('player_weight',player_weight)
				playeritem.setProperty('player_plot',player_plot)
				playeritem.setProperty('player_fanartlist',str(player_fanart_list))
				playeritem.setProperty('player_twitter',player_twitter)							
				self.getControl(985).addItem(playeritem)


		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(playersview,1,home)")
		settings.setSetting("view_type_team",'playersview')
		self.mode=''

		self.getControl(2).setLabel("Team: PlayersView")
		
		#select first item only if mediamenu is not active
		if not xbmc.getCondVisibility("Control.HasFocus(2)"):
			self.setFocusId(985)
			self.getControl(985).selectItem(0)
		self.setplayerinfo()
		
	def setnewsview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		self.feedurl = thesportsdb.Teams().get_rssurl(self.team)
		rssitems = return_rsslist(self.feedurl)
		if rssitems:
			for title,date,content,img in rssitems:
				newsitem = xbmcgui.ListItem(title)
				newsitem.setProperty('content',content)
				newsitem.setProperty('news_img',img)
				newsitem.setProperty('date',date)
				newsitem.setProperty('title',title)
				self.getControl(986).addItem(newsitem)
			self.getControl(939).setImage(rssitems[0][3])
			self.getControl(937).setText(rssitems[0][2])
			self.getControl(938).setLabel(rssitems[0][0])
			
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(playersview,Home)")
		xbmc.executebuiltin("SetProperty(newsview,1,home)")
		settings.setSetting("view_type_team",'newsview')
		self.mode = ''

		self.getControl(2).setLabel("Team: NewsView")
		#select first item only if mediamenu is not active
		if not xbmc.getCondVisibility("Control.HasFocus(2)"):	
			try:self.getControl(986).selectItem(0)
			except:pass
			
	def setnextmatchview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#next matches stuff
		event_next_list = thesportsdb.Schedules(tsdbkey).eventsnext(self.team_id)['events']
		self.getControl(987).reset()
		if event_next_list:
			for event in event_next_list:
				event_datetime = thesportsdb.Events().get_datetime_object(event)
				event_fanart = thesportsdb.Events().get_fanart(event)
				if event_datetime:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(event_datetime)
					event_datetime=db_time.astimezone(my_location)
				
				if event_datetime:
					try:
						day = str(event_datetime.day)
						month = get_month_short(event_datetime.month)
						extensiveday = '%s %s' % (day,month)
						fmt = "%H:%M"
						extensivetime=event_datetime.strftime(fmt)
						event_timestring = extensiveday + ' - ' + extensivetime
					except: event_timestring = ''
				else: event_timestring = ''
				
				#day difference is calculated here
				if event_datetime:
					now = datetime.datetime.now()
					datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
					datenow =  pytz.timezone(str(pytz.timezone(str(my_location)))).localize(datenow)
					day_difference = abs(event_datetime - datenow).days
					if day_difference == 0:
						timedelay = '[COLOR white] (Today)[/COLOR]'
					elif day_difference == 1:
						timedelay = '[COLOR white] (Tomorrow)[/COLOR]'
					else:
						timedelay = '[COLOR white] (In ' + str(day_difference) + ' days)[/COLOR]'
				else: timedelay = ''
				presented_date = event_timestring + timedelay
				
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''		
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					event_round = thesportsdb.Events().get_round(event)
					if event_round and event_round != '0':
						round_label = 'Round ' + str(event_round)
				
				if event_fanart and event_fanart != 'None' and event_fanart != 'null':
					stadium_fanart = event_fanart
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				if not event_race:
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('StadiumThumb',stadium_fanart)
					game.setProperty('vs','VS')
				game.setProperty('date',presented_date)
				if event_race: 
					game.setProperty('EventName',event_name) 
					if event_fanart and event_fanart != 'None' and event_fanart != 'null':
						game.setProperty('StadiumThumb',stadium_fanart)
				if event_round and event_round != '0': game.setProperty('round',round_label)
				self.getControl(987).addItem(game)
				
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(playersview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(nextmatchview,1,home)")
		settings.setSetting("view_type_team",'nextmatchview')
		self.mode = ''

		self.getControl(2).setLabel("Team: NextMatchView")

	def setlastmatchview(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		i = 0
		controlinicial = 30
		winnumber = 0
		
		#last matches stuff
		event_last_list = thesportsdb.Schedules(tsdbkey).eventslast(self.team_id)['results']
		if event_last_list:
			for event in event_last_list:
				#compare team id's and not team name
				awayteam = thesportsdb.Events().get_awayteamid(event)
				hometeam = thesportsdb.Events().get_hometeamid(event)
				awayscore = thesportsdb.Events().get_awayscore(event)
				homescore = thesportsdb.Events().get_homescore(event)
				event_id = thesportsdb.Events().get_eventid(event)
				event_fanart = thesportsdb.Events().get_fanart(event)
				if hometeam == self.team_id:
					if int(homescore) > int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greensquare.png'))
						self.getControl(controlinicial+i+1).setLabel('W')
						winnumber += 1
					elif int(homescore) < int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','redsquare.png'))
						self.getControl(controlinicial+i+1).setLabel('L')
					else:
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greysquare.png'))
						self.getControl(controlinicial+i+1).setLabel('D')
				else:
					if int(homescore) > int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','redsquare.png'))
						self.getControl(controlinicial+i+1).setLabel('L')
					elif int(homescore) < int(awayscore):
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greensquare.png'))
						self.getControl(controlinicial+i+1).setLabel('W')
						winnumber += 1
					else:
						self.getControl(controlinicial+i).setImage(os.path.join(addonpath,'resources','img','greysquare.png'))
						self.getControl(controlinicial+i+1).setLabel('D')
				i += 2
				
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				event_datetime = thesportsdb.Events().get_datetime_object(event)
				if event_datetime:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(event_datetime)
					event_datetime=db_time.astimezone(my_location)
				
				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					event_round = thesportsdb.Events().get_round(event)
					if event_round and event_round != '0':
						round_label = 'Round ' + str(event_round)
				
				
				if event_datetime:
					try:
						day = str(event_datetime.day)
						month = get_month_long(event_datetime.month)
						year = str(event_datetime.year)
						extensiveday = '%s %s %s' % (day,month,year)
						fmt = "%H:%M"
						extensivetime=event_datetime.strftime(fmt)
						extensiveday = '%s %s %s' % (day,month,year)
						event_timestring = extensiveday + ' - ' + extensivetime
					except: event_timestring = ''
				else: event_timestring = ''
				
				#day difference is calculated here
				if event_datetime:
					now = datetime.datetime.now()
					datenow = datetime.datetime(int(now.year), int(now.month), int(now.day),int(now.hour),int(now.minute))
					datenow =  pytz.timezone(str(pytz.timezone(str(my_location)))).localize(datenow)
					day_difference = abs(event_datetime - datenow).days
					if day_difference == 0:
						timedelay = '[COLOR white] (Today)[/COLOR]'
					elif day_difference == 1:
						timedelay = '[COLOR white] (Yesterday)[/COLOR]'
					else:
						timedelay = '[COLOR white] (' + str(day_difference) + ' days ago)[/COLOR]'
				else: timedelay = ''
				
				if event_fanart and event_fanart != 'None' and event_fanart != 'null':
					stadium_fanart = event_fanart
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				game.setProperty('event_id',event_id)
				if not event_race:
					if ' ' in home_team_name:
						if len(home_team_name) > 12: game.setProperty('HomeTeamLong',home_team_name)
						else: game.setProperty('HomeTeamShort',home_team_name)
					else: game.setProperty('HomeTeamShort',home_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('StadiumThumb',stadium_fanart)
					if ' ' in away_team_name:
						if len(away_team_name) > 12: game.setProperty('AwayTeamLong',away_team_name)
						else: game.setProperty('AwayTeamShort',away_team_name)
					else: game.setProperty('AwayTeamShort',away_team_name)
					game.setProperty('match_result',result)
					if event_round and event_round != '0': game.setProperty('round',round_label)
				else:
					game.setProperty('EventName',event_name)
					if event_fanart and event_fanart != 'None' and event_fanart != 'null':
						game.setProperty('StadiumThumb',stadium_fanart)
				# date + time + timedelay
				event_fullstring = event_timestring + timedelay
				game.setProperty('date',event_fullstring)
				self.getControl(988).addItem(game)
		
		#Set percentage		
		winpercentage = float(winnumber)/5*100 
		self.getControl(43).setLabel(str(int(winpercentage))+'% WINS')
		self.getControl(44).setPercent(int(winpercentage))
		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(playersview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(lastmatchview,1,home)")
		settings.setSetting("view_type_team",'lastmatchview')
		self.mode = ''

		self.getControl(2).setLabel("Team: LastMatchView")
		
	def setvideosview(self):
	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.youtubeurl = thesportsdb.Teams().get_team_youtube(self.team)
		if self.youtubeurl:
			ytuser = self.youtubeurl.split('/')[-1]
		else: ytuser = None
		
			
		#videos stuff
		if ytuser:
			video_list = return_youtubevideos(ytuser)
			for video_name,video_id,video_thumb in video_list:
				video = xbmcgui.ListItem(video_name)
				video.setProperty('thumb',video_thumb)
				video.setProperty('video_id',video_id)
				self.getControl(989).addItem(video)
			
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")		
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(playersview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(videosview,1,home)")
		settings.setSetting("view_type_team",'videosview')
		self.mode = ''

		self.getControl(2).setLabel("Team: VideosView")	
		
	def setplayerinfo(self):
		fanart = self.getControl(985).getSelectedItem().getProperty('player_fanart')
		player_name = self.getControl(985).getSelectedItem().getProperty('player_name')
		player_position = self.getControl(985).getSelectedItem().getProperty('player_position')
		player_value = self.getControl(985).getSelectedItem().getProperty('player_value')
		try:
			player_datebirth = int(self.getControl(985).getSelectedItem().getProperty('player_age').split('-')[0])
			now_year = int(datetime.datetime.now().year)
			age = str(now_year - player_datebirth)
			player_age = age +' ('+str(player_datebirth)+')'
		except: player_age = 'N/A'
		player_location = self.getControl(985).getSelectedItem().getProperty('player_location')
		player_height = self.getControl(985).getSelectedItem().getProperty('player_height')
		player_weight = self.getControl(985).getSelectedItem().getProperty('player_weight')
		player_plot = self.getControl(985).getSelectedItem().getProperty('player_plot')
		if not fanart or fanart == 'None': fanart = self.team_fanart
		self.getControl(426).setImage(fanart)
		self.getControl(931).setLabel('[B]'+player_name+'[/B]')
		self.getControl(932).setLabel('[COLOR labelheader]Position:[CR][/COLOR]'+player_position)
		self.getControl(933).setLabel('[COLOR labelheader]Value:[CR][/COLOR]'+player_value)
		self.getControl(929).setLabel('[COLOR labelheader]Age:[CR][/COLOR]'+player_age)
		self.getControl(935).setLabel('[COLOR labelheader]Birth Place:[CR][/COLOR]'+player_location)
		self.getControl(936).setLabel('[COLOR labelheader]Height:[CR][/COLOR]'+player_height)
		self.getControl(927).setLabel('[COLOR labelheader]Weight:[CR][/COLOR]'+player_weight)
		self.getControl(928).setText(player_plot)
		return fanart
	
	def fanart_setter(self):
		checkplayers = xbmc.getCondVisibility("Control.HasFocus(985)")
		checkplot = xbmc.getCondVisibility("Control.HasFocus(980)")
		checkbanner = xbmc.getCondVisibility("Control.HasFocus(984)")
		checklastmatch = xbmc.getCondVisibility("Control.HasFocus(988)")
		checknextmatch = xbmc.getCondVisibility("Control.HasFocus(987)")
		if checkplayers or checkplot or checkbanner or checklastmatch or checknextmatch:
			if checkplayers:
				fanart = self.setplayerinfo()
			elif checkplot:
				fanart = self.getControl(980).getSelectedItem().getProperty('team_fanart')
			elif checkbanner:
				fanart = self.getControl(984).getSelectedItem().getProperty('team_fanart')
			elif checklastmatch:
				fanart = self.getControl(988).getSelectedItem().getProperty('StadiumThumb')
				if not fanart or fanart == 'None': fanart = self.team_fanart
			elif checknextmatch:
				fanart = self.getControl(987).getSelectedItem().getProperty('StadiumThumb')
				if not fanart or fanart == 'None': fanart = self.team_fanart
			self.getControl(912).setImage(fanart)
		#TODO check what window is open
		else: 
			self.getControl(912).setImage(self.team_fanart)
		return
				
		
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.control_panel = xbmc.getCondVisibility("Control.HasFocus(2)")
			if self.control_panel: 
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(983)
			else: 
				self.close()
		else:
			self.fanart_setter()


			
	def onClick(self,controlId):
	
		#print controlId
	
		if controlId == 983:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem().getProperty('entryid')
			if seleccionado == 'news':
				self.setnewsview()
			elif seleccionado == 'home':
				self.setplotview()
			elif seleccionado == 'nextmatch':
				self.setnextmatchview()
			elif seleccionado == 'lastmatch':
				self.setlastmatchview()
			elif seleccionado == 'videos':
				self.setvideosview()
			elif seleccionado == 'stadium':
				stadium.start(self.team)	
			elif seleccionado == 'details':
				teamdetails(str([self.team_id,'plotview']))
			elif seleccionado == 'players':
				self.setplayersview()
			elif seleccionado == 'tweets':
				twitter_name = thesportsdb.Teams().get_team_twitter(self.team)
				if twitter_name: 
					twitter_name = twitter_name.split('/')[-1]
					tweetbuild.tweets(['user',twitter_name])
				else: pass
					
					

		elif controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "Team: PlotView":
				self.setplayersview()
			elif active_view_type == "Team: VideosView":
				if self.team_rss and self.team_rss != 'None':
					self.setnewsview()
				else:
					self.setnextmatchview()
			elif active_view_type == "Team: PlayersView":
				if self.team_youtube and self.team_youtube != 'None':
					self.setvideosview()
				else:
					if self.team_rss and self.team_rss != 'None':
						self.setnewsview()
					else:
						self.setnextmatchview()
			elif active_view_type == "Team: NewsView":
				self.setnextmatchview()
			elif active_view_type == "Team: NextMatchView":
				self.setlastmatchview()
			elif active_view_type == "Team: LastMatchView":
				self.setplotview()
				
		elif controlId == 988:
			event_id = self.getControl(988).getSelectedItem().getProperty('event_id')
			self.fanart_setter()
			if self.sport.lower() == 'soccer' or self.sport.lower() == 'football':
				soccermatchdetails.start([False,event_id])
			else:
				eventdetails.start([event_id])
				
		elif controlId == 989:
			youtube_id = self.getControl(989).getSelectedItem().getProperty('video_id')
			xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+youtube_id+')')
			
		elif controlId == 986:
			news_content = self.getControl(986).getSelectedItem().getProperty('content')
			news_title = self.getControl(986).getSelectedItem().getProperty('title')
			news_image = self.getControl(986).getSelectedItem().getProperty('news_img')
			self.getControl(939).setImage(news_image)
			self.getControl(937).setText(news_content)
			self.getControl(938).setLabel(news_title)
			
		elif controlId == 985:
			player_id = self.getControl(985).getSelectedItem().getProperty('player_id')
			playerview.start([player_id,'plotview'])
	
