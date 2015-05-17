import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,os,sys,json
import thesportsdb
from centerutils.common_variables import *
from centerutils.iofile import *
from centerutils.onscreenutils import *
import soccermatchdetails
import teamview
import tweetbuild as tweetbuild
import tables as tables

dialog = xbmcgui.Dialog()

def start(data_list):
	window = dialog_libconfig('DialogOnScreen.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_libconfig(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		#variables initialization
		self.league_logo = os.path.join(addonpath,art,'premier.png')
		self.hometeambadge = ''
		self.awayteambadge = ''
		self.hometwitter = ''
		self.awaytwitter = ''
		self.league_id = ''
		self.league_badge = ''
		self.hometeam_id = ''
		self.awayteam_id = ''

	def onInit(self):
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		has_media = False
		if os.path.exists(onscreen_playingmatch):
			match = eval(readfile(onscreen_playingmatch))
			self.hometeam_id = match['hometeamid']
			self.awayteam_id = match['awayteamid']
			self.playingfile = match['videofile']
			self.league_id = match['league_id']
			if xbmc.getCondVisibility('Player.HasMedia'):
				has_media = True
				if xbmc.Player().getPlayingFile() == self.playingfile:
					self.hometeambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.hometeam_id) + '.txt' ))))
					self.awayteambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.awayteam_id) + '.txt' ))))
				else:
					if xbmc.getCondVisibility('Pvr.IsPlayingTv') or xbmc.getCondVisibility('Pvr.IsPlayingRadio'):
						#get program title and plot
						active_players = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.GetActivePlayers","params":[]}')
						try: playerid = json.loads(active_players)['result'][0]['playerid']
						except: playerid = ''
						if playerid:
							curr_item = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "plot", "streamdetails"], "playerid":'+str(playerid)+' }, "id": 1 }')
							try: ch_plot = json.loads(curr_item)['result']['item']['plot']	# plot of the channel program being played
							except: ch_plot = ''
							try: ch_title = json.loads(curr_item)['result']['item']['title']	# title of the channel program being played
							except: ch_title = ''
							if ch_title and ch_title != settings.getSetting('last_played_programtitle'): do_check = True
					else:
						#TODO
						ch_title = 'coiso'
						ch_plot = 'coiso'
					update_and_match_livescores(ch_title,ch_plot,True)
			else:
				has_media = False	
		else:
			if xbmc.getCondVisibility('Player.HasMedia'):
				has_media = True
				if xbmc.Player().getPlayingFile() == settings.getSetting('last_played_channel'):
					if self.hometeam_id and self.awayteam_id:
						self.hometeambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.hometeam_id) + '.txt' ))))
						self.awayteambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.awayteam_id) + '.txt' ))))
				else:
					if xbmc.getCondVisibility('Pvr.IsPlayingTv') or xbmc.getCondVisibility('Pvr.IsPlayingRadio'):
						#get program title and plot
						active_players = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":1,"method":"Player.GetActivePlayers","params":[]}')
						try: playerid = json.loads(active_players)['result'][0]['playerid']
						except: playerid = ''
						if playerid:
							curr_item = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "plot", "streamdetails"], "playerid":'+str(playerid)+' }, "id": 1 }')
							try: ch_plot = json.loads(curr_item)['result']['item']['plot']	# plot of the channel program being played
							except: ch_plot = ''
							try: ch_title = json.loads(curr_item)['result']['item']['title']	# title of the channel program being played
							except: ch_title = ''
							if ch_title and ch_title != settings.getSetting('last_played_programtitle'): do_check = True
					else:
						#TODO
						ch_title = 'coiso'
						ch_plot = 'coiso'
					update_and_match_livescores(ch_title,ch_plot,True)
			else:
				has_media = False
		while os.path.exists(loading_onscreenlock):
			xbmc.sleep(200)
		self.set_menu()
		
		
	def set_menu(self,):
		
		menu = []
		
		if os.path.exists(onscreen_playingmatch):
			self.hometeambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.hometeam_id) + '.txt' ))))
			self.awayteambadge = thesportsdb.Teams().get_badge(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.awayteam_id) + '.txt' ))))
			self.hometwitter = thesportsdb.Teams().get_team_twitter(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.hometeam_id) + '.txt' ))))
			self.awaytwitter = thesportsdb.Teams().get_team_twitter(eval(readfile(os.path.join(onscreen_userdata_teams,str(self.awayteam_id) + '.txt' ))))
			if self.league_id and self.league_id != 'None':
				league_dict = thesportsdb.Lookups(tsdbkey).lookupleague(self.league_id)["leagues"][0]
				self.league_badge = thesportsdb.Leagues().get_badge(league_dict)
		
		if settings.getSetting('enable-matchdetails') == 'true' and self.hometeambadge and self.awayteambadge:
			menu.append(('Match Details',os.path.join(addonpath,art,'details.png'),'matchdetails'))
			
		if settings.getSetting('enable-homedetails') == 'true' and self.hometeambadge:
			menu.append(('Home Team Details',os.path.join(addonpath,art,'details.png'),'homedetails'))
			
		if settings.getSetting('enable-awaydetails') == 'true' and self.awayteambadge:
			menu.append(('Away Team Details',os.path.join(addonpath,art,'details.png'),'awaydetails'))
			
		if settings.getSetting('enable-hometwitter') == 'true' and self.hometwitter:
			menu.append(('Home Team Twitter',os.path.join(addonpath,art,'twitter.png'),'hometwitter'))
			
		if settings.getSetting('enable-awaytwitter') == 'true' and self.awaytwitter:
			menu.append(('Away Team Twitter',os.path.join(addonpath,art,'twitter.png'),'awaytwitter'))
			
		if settings.getSetting('enable-matchtwitter') == 'true':
			menu.append(('Match Twitter #',os.path.join(addonpath,art,'twitter.png'),'matchtwitter'))
			
		if settings.getSetting('enable-leaguetables') == 'true' and self.league_badge:
			menu.append(('League Tables',os.path.join(addonpath,art,'stats.png'),'leaguetables'))
		
		if settings.getSetting('enable-livescores') == 'true':
			menu.append(('LiveScores',os.path.join(addonpath,art,'onair.png'),'livescores'))
		
		
		for entry,thumb,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			menu_entry.setProperty('thumb',thumb)
			if entry_id == 'homedetails' or entry_id == 'hometwitter':
				menu_entry.setProperty('subthumb',self.hometeambadge)
			elif entry_id == 'awaydetails' or entry_id == 'awaytwitter':
				menu_entry.setProperty('subthumb',self.awayteambadge)
			elif entry_id == 'matchtwitter' or entry_id == 'matchdetails' or entry_id == 'livescores':
				menu_entry.setProperty('subthumb',os.path.join(addonpath,art,'soccer.png'))
			elif entry_id == 'leaguetables':
				if self.league_badge:
					menu_entry.setProperty('subthumb',self.league_badge)
			self.getControl(983).addItem(menu_entry)
		
		return

	def get_info_from_txt(self,):
		if os.path.exists(onscreen_playingmatch):
			matchinfo = eval(readfile(onscreen_playingmatch))
			hometeamid = matchinfo['hometeamid']
			awayteamid = matchinfo['awayteamid']
			leagueid = matchinfo['league_id']
			if 'matchtwitter' in matchinfo.keys():
				matchtwitter = matchinfo['matchtwitter']
			else:
				matchtwitter = ''
			return hometeamid,awayteamid,leagueid,matchtwitter

	def onClick(self,controlId):	
		if controlId == 983:
			entry_id = self.getControl(controlId).getSelectedItem().getProperty('entryid')
			if entry_id == 'livescores':
				import livescores as livescores
				livescores.start(None)
			
			elif entry_id == 'leaguetables':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					tables.start(leagueid)
			
			elif entry_id == 'matchtwitter':
				keyb = xbmc.Keyboard('#', 'Please write the hashtag to assign to this match')
				keyb.doModal()
				if (keyb.isConfirmed()):
					hashtag = keyb.getText()
					tweetbuild.tweets(['hash',hashtag])

			elif entry_id == 'matchdetails':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					event_list = thesportsdb.LiveScores(tsdbkey).latestsoccer()["teams"]["Match"]
					if event_list:
						for event in event_list:
							home_event_id = thesportsdb.Livematch().get_home_id(event)
							away_event_id = thesportsdb.Livematch().get_away_id(event)
							if home_event_id == hometeamid and away_event_id == awayteamid:
								home_event_name = thesportsdb.Livematch().get_home_name(event)
								away_event_name = thesportsdb.Livematch().get_away_name(event)
								event_string = home_event_name + '###' + away_event_name
								soccermatchdetails.start([True,event_string])
			
			elif entry_id == 'homedetails':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					teamview.teamdetails(hometeamid)
			
			elif entry_id == 'awaydetails':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					teamview.teamdetails(awayteamid)
					
			elif entry_id == 'hometwitter':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					teamdict = thesportsdb.Lookups(tsdbkey).lookupteam(hometeamid)["teams"][0]
					hometwitter = thesportsdb.Teams().get_team_twitter(teamdict)
					if hometwitter:
						twitter_name = hometwitter.split('/')[-1]
						tweetbuild.tweets(['user',twitter_name])
						
			elif entry_id == 'awaytwitter':
				if os.path.exists(onscreen_playingmatch):
					hometeamid,awayteamid,leagueid,matchtwitter = self.get_info_from_txt()
					teamdict = thesportsdb.Lookups(tsdbkey).lookupteam(awayteamid)["teams"][0]
					awaytwitter = thesportsdb.Teams().get_team_twitter(teamdict)
					if awaytwitter:
						twitter_name = awaytwitter.split('/')[-1]
						tweetbuild.tweets(['user',twitter_name])
						
			
			

	
		
