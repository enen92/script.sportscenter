import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib
import thesportsdb
from random import randint
from centerutils.common_variables import *
from centerutils.youtube import *
from centerutils.rssparser import *
from centerutils.datemanipulation import *
import competlist as competlist
import teamview as teamview

def start(data_list):
	window = dialog_league('DialogLeague.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_league(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.league = eval(eval(args[3])[0])
		self.sport = eval(args[3])[1]

	def onInit(self):	
	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		self.league_id = thesportsdb.Leagues().get_id(self.league)
		self.league_rss = thesportsdb.Leagues().get_rssurl(self.league)
		self.league_youtube = thesportsdb.Leagues().get_youtube(self.league)
		
		self.getControl(911).setImage(os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
		
		
		#populate panel left
		menu = [('Home','home')]
		if self.league_rss and self.league_rss != 'None':
			menu.append(('News','news'))
		
		if self.league_youtube and self.league_youtube !='None':
			menu.append(('Videos','videos'))
			
		menu.append(('League Tables(!)','tables'))
		menu.append(('Fixtures(!)','fixtures'))
		menu.append(('Teams','teams'))
		menu.append(('Latest Matches','lastmatch'))
		menu.append(('Next Matches','nextmatch'))

		self.getControl(983).reset()	   
		for entry,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			self.getControl(983).addItem(menu_entry)
			
		#set league fanart
		self.league_fanartlist = thesportsdb.Leagues().get_fanart(self.league)
		if self.league_fanartlist:
			self.league_fanart = self.league_fanartlist[randint(0,len(self.league_fanartlist)-1)]
			self.getControl(912).setImage(self.league_fanart)
			self.getControl(429).setImage(self.league_fanart)
		else: self.league_fanart = None
			
		self.setplotview()
		
	def setleagueinfo(self):
		
		#set league badge
		self.league_badge = thesportsdb.Leagues().get_badge(self.league)
		self.getControl(934).setImage(os.path.join(self.league_badge))
		
		#set league plot
		self.league_plot = thesportsdb.Leagues().get_plot_en(self.league)
		self.getControl(430).setText(self.league_plot)
		
		#set league formed year
		self.league_formedyear = thesportsdb.Leagues().get_formedyear(self.league)
		self.getControl(428).setLabel('[COLOR labelheader]Established:[CR][/COLOR]' + self.league_formedyear)
		
		#set league name
		self.league_name = thesportsdb.Leagues().get_name(self.league)
		self.getControl(427).setLabel('[COLOR labelheader]League:[CR][/COLOR]' + self.league_name)
		#Set top bar information
		self.getControl(333).setLabel('League View - ' + self.league_name)
		
		self.getControl(980).reset()
		self.getControl(981).reset()
		self.getControl(984).reset()
		self.getControl(985).reset()
			
		teams_list = thesportsdb.Lookups().lookup_all_teams(self.league_id)["teams"]
		team_number = len(teams_list)
		#set team number on top bar
		self.getControl(334).setLabel(str(team_number)+' Teams')
		
		for team in teams_list:
			if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
			else: team_name = thesportsdb.Teams().get_alternativefirst(team)
			team_id = thesportsdb.Teams().get_id(team)
			team_badge = thesportsdb.Teams().get_badge(team)
			team_banner = thesportsdb.Teams().get_banner(team)
			team_jersey = thesportsdb.Teams().get_team_jersey(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = self.league_fanart
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_name',team_name)
			teamitem.setProperty('team_banner',team_banner)
			teamitem.setProperty('team_logo',team_badge)
			teamitem.setProperty('team_jersey',team_jersey)
			teamitem.setProperty('team_fanart',team_fanart)
			teamitem.setProperty('team_id',team_id)
			self.getControl(980).addItem(teamitem)
			
		for team in teams_list:
			if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
			else: team_name = thesportsdb.Teams().get_alternativefirst(team)
			team_banner = thesportsdb.Teams().get_banner(team)
			team_jersey = thesportsdb.Teams().get_team_jersey(team)
			team_id = thesportsdb.Teams().get_id(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = self.league_fanart
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_banner',team_banner)
			teamitem.setProperty('team_fanart',team_fanart)
			teamitem.setProperty('team_jersey',team_jersey)
			teamitem.setProperty('team_id',team_id)
			self.getControl(984).addItem(teamitem)
			
		for team in teams_list:
			if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
			else: team_name = thesportsdb.Teams().get_alternativefirst(team)
			team_badge = thesportsdb.Teams().get_badge(team)
			team_jersey = thesportsdb.Teams().get_team_jersey(team)
			team_id = thesportsdb.Teams().get_id(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = self.league_fanart
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_badge',team_badge)
			teamitem.setProperty('team_fanart',team_fanart)
			teamitem.setProperty('team_jersey',team_jersey)
			teamitem.setProperty('team_id',team_id)
			self.getControl(985).addItem(teamitem)
			
		for team in teams_list:
			if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
			else: team_name = thesportsdb.Teams().get_alternativefirst(team)
			team_badge = thesportsdb.Teams().get_badge(team)
			team_id = thesportsdb.Teams().get_id(team)
			team_jersey = thesportsdb.Teams().get_team_jersey(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = self.league_fanart
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_badge',team_badge)
			teamitem.setProperty('team_fanart',team_fanart)
			teamitem.setProperty('team_jersey',team_jersey)
			teamitem.setProperty('team_id',team_id)
			self.getControl(981).addItem(teamitem)
		return
		
	def setplotview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(plotview,1,home)")
		settings.setSetting("view_type_league",'plotview')

		self.getControl(2).setLabel("League: PlotView")
		self.setFocusId(983)
		self.getControl(983).selectItem(0)
		
	def setbadgeview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(badgeview,1,home)")
		settings.setSetting("view_type_league",'badgeview')

		self.getControl(2).setLabel("League: BadgeView")
		
	def setjerseyview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(jerseyview,1,home)")
		settings.setSetting("view_type_league",'jerseyview')

		self.getControl(2).setLabel("League: JerseyView")
		
	def setbannerview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(bannerview,1,home)")
		settings.setSetting("view_type_league",'bannerview')

		self.getControl(2).setLabel("League: BannerView")
			
		
	def setnewsview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#news stuff
		self.feedurl = thesportsdb.Leagues().get_rssurl(self.league)
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
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("SetProperty(newsview,1,home)")
		settings.setSetting("view_type_league",'newsview')

		self.getControl(2).setLabel("League: NewsView")	
		
			
	def setnextmatchview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#next matches stuff
		event_next_list = thesportsdb.Schedules().eventsnextleague(self.league_id)["events"]
		if event_next_list:
			for event in event_next_list:
				event_date = thesportsdb.Events().get_eventdate(event)
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''		
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = thesportsdb.Lookups().lookupteam(home_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Events().get_name(home_team_dict)
					else: team_name = home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups().lookupteam(away_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					event_round = thesportsdb.Events().get_round(event)
					if event_round:
						round_label = 'Round ' + str(event_round)
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				if not event_race:
					if ' ' in home_team_name:
						if len(home_team_name) > 12: game.setProperty('HomeTeamLong',home_team_name)
						else: game.setProperty('HomeTeamShort',home_team_name)
					else: game.setProperty('HomeTeamShort',home_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					if ' ' in away_team_name:
						if len(away_team_name) > 12: game.setProperty('AwayTeamLong',away_team_name)
						else: game.setProperty('AwayTeamShort',away_team_name)
					else: game.setProperty('AwayTeamShort',away_team_name)
					game.setProperty('StadiumThumb',stadium_fanart)
					game.setProperty('vs','VS')
				game.setProperty('date',event_date)
				if event_race: 
					game.setProperty('EventName',event_name) 
				if event_round: game.setProperty('round',round_label)
				self.getControl(987).addItem(game)
				
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(nextmatchview,1,home)")
		settings.setSetting("view_type_league",'nextmatchview')

		self.getControl(2).setLabel("League: NextMatchView")

	def setlastmatchview(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#last matches stuff
		event_last_list = thesportsdb.Schedules().eventspastleague(self.league_id)["events"]
		if event_last_list:
			for event in event_last_list:

				event_date = thesportsdb.Events().get_eventdate(event)
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = thesportsdb.Lookups().lookupteam(home_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups().lookupteam(away_team_id)["teams"][0]
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					event_round = thesportsdb.Events().get_round(event)
					if event_round:
						round_label = 'Round ' + str(event_round)
				
			
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
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
					if event_round: game.setProperty('round',round_label)
				else:
					game.setProperty('EventName',event_name) 
				game.setProperty('date',event_date)
				self.getControl(988).addItem(game)
		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(lastmatchview,1,home)")
		settings.setSetting("view_type_league",'lastmatchview')

		self.getControl(2).setLabel("League: LastMatchView")
		
	def setvideosview(self):
	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
			
		self.youtubeurl = thesportsdb.Leagues().get_youtube(self.league)
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
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(videosview,1,home)")
		settings.setSetting("view_type_league",'videosview')

		self.getControl(2).setLabel("League: VideosView")			
		
	def onAction(self,action):
		if action == 92 or action == 'PreviousMenu':
			#if not self.control_panel: 
			if 2==1:
				pass
				#xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				#self.setFocusId(980)
			else: 
				#pass
				self.close()
				#competlist.start(self.sport)
		else:
			checkjersey = xbmc.getCondVisibility("Control.HasFocus(981)")
			checkbadge = xbmc.getCondVisibility("Control.HasFocus(985)")
			checkplot = xbmc.getCondVisibility("Control.HasFocus(980)")
			checkbanner = xbmc.getCondVisibility("Control.HasFocus(984)")
			checklastmatch = xbmc.getCondVisibility("Control.HasFocus(988)")
			checknextmatch = xbmc.getCondVisibility("Control.HasFocus(987)")
			
			if checkbadge or checkplot or checkbanner or checklastmatch or checknextmatch or checkjersey:
				if checkbadge:
					fanart = self.getControl(985).getSelectedItem().getProperty('team_fanart')
				elif checkplot:
					fanart = self.getControl(980).getSelectedItem().getProperty('team_fanart')
				elif checkbanner:
					fanart = self.getControl(984).getSelectedItem().getProperty('team_fanart')
				elif checkjersey:
					fanart = self.getControl(981).getSelectedItem().getProperty('team_fanart')
				elif checklastmatch:
					fanart = self.getControl(988).getSelectedItem().getProperty('StadiumThumb')
					if not fanart or fanart == 'None': fanart = self.league_fanart
				elif checknextmatch:
					fanart = self.getControl(987).getSelectedItem().getProperty('StadiumThumb')
					if not fanart or fanart == 'None': fanart = self.league_fanart
				self.getControl(912).setImage(fanart)
			else: 
				if self.league_fanart: self.getControl(912).setImage(self.league_fanart)

			
	def onClick(self,controlId):
	
		#print controlId
	
		if controlId == 983:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem().getProperty('entryid')
			if seleccionado == 'news':
				self.setnewsview()
			elif seleccionado == 'teams':
				if settings.getSetting('view_type_league') == 'bannerview':
					self.setbadgeview()
				elif settings.getSetting('view_type_league')=='badgeview':
					self.setjerseyview()
				elif settings.getSetting('view_type_league')=='jerseyview':
					self.setbannerview()
				else:
					self.setbadgeview()
			elif seleccionado == 'home':
					self.setplotview()
			elif seleccionado == 'nextmatch':
					self.setnextmatchview()
			elif seleccionado == 'lastmatch':
					self.setlastmatchview()
			elif seleccionado == 'videos':
					self.setvideosview()
					
		elif controlId == 980 or controlId == 984 or controlId == 985 or controlId == 981:
			self.team = self.getControl(controlId).getSelectedItem().getProperty('team_id')
			teamview.start([self.team,self.sport,'',''])
		


		elif controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "League: PlotView":
				self.setvideosview()
			elif active_view_type == "League: VideosView":
				self.setbannerview()
			elif active_view_type == "League: BannerView":
				self.setbadgeview()	
			elif active_view_type == "League: BadgeView":
				self.setjerseyview()
			elif active_view_type == "League: JerseyView":
				self.setnewsview()
			elif active_view_type == "League: NewsView":
				self.setnextmatchview()
			elif active_view_type == "League: NextMatchView":
				self.setlastmatchview()
			elif active_view_type == "League: LastMatchView":
				self.setplotview()
				
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
	
		
