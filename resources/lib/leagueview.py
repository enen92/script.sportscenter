import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib
import thesportsdb
import datetime
from random import randint
from centerutils.common_variables import *
from centerutils.youtube import *
from centerutils.rssparser import *
from centerutils.datemanipulation import *
import competlist as competlist
import teamview as teamview
import soccermatchdetails as soccermatchdetails
import eventdetails as eventdetails

def start(data_list):
	window = dialog_league('DialogLeague.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_league(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.league = eval(eval(args[3])[0])
		self.sport = eval(args[3])[1]
		self.league_fanart = eval(args[3])[2]
		self.mode = eval(args[3])[3]
		if type(self.league) != dict:
			self.league = thesportsdb.Lookups(tsdbkey).lookupleague(self.league)["leagues"][0]

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
		
		if self.sport == 'soccer' or self.sport == 'football':	
			menu.append(('League Tables','tables'))
		if self.sport == 'soccer' or self.sport == 'football':	
			menu.append(('Fixtures','fixtures'))
		menu.append(('Teams','teams'))
		menu.append(('Latest Events','lastmatch'))
		menu.append(('Next Events','nextmatch'))

		self.getControl(983).reset()	   
		for entry,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			self.getControl(983).addItem(menu_entry)
			
		#set league fanart
		if not self.league_fanart:
			self.league_fanartlist = thesportsdb.Leagues().get_fanart(self.league)
			if self.league_fanartlist:
				self.league_fanart = self.league_fanartlist[randint(0,len(self.league_fanartlist)-1)]
			else: self.league_fanart = None
		self.getControl(912).setImage(self.league_fanart)
		self.getControl(429).setImage(self.league_fanart)
			
		if self.mode:
			mode = self.mode
		else:
			mode = settings.getSetting('view_type_league')
		if mode == 'plotview':
			self.setplotview()
		elif mode == 'badgeview':
			self.setbadgeview()
		elif mode == 'jerseyview':
			self.setjerseyview()
		elif mode == 'bannerview':
			self.setbannerview()
		elif mode == 'newsview':
			self.setnewsview()
		elif mode == 'tablesview':
			self.settablesview()
		elif mode == 'nextmatchview':
			self.setnextmatchview()
		elif mode == 'lastmatchview':
			self.setlastmatchview()
		elif mode == 'fixturesview':
			self.setfixturesview()
		elif mode == 'videosview':
			self.setvideosview()
		else:
			self.setplotview()
			
			
			
	def setleagueinfo(self):
		
		#set league badge
		self.league_badge = thesportsdb.Leagues().get_badge(self.league)
		self.getControl(934).setImage(os.path.join(self.league_badge))
		
		#set league plot
		if settings.getSetting('addon-language') == '0':
			self.league_plot = thesportsdb.Leagues().get_plot_en(self.league)
		elif settings.getSetting('addon-language') == '1':	
			self.league_plot = thesportsdb.Leagues().get_plot_de(self.league)
		elif settings.getSetting('addon-language') == '2':
			self.league_plot = thesportsdb.Leagues().get_plot_fr(self.league)
		elif settings.getSetting('addon-language') == '3':
			self.league_plot = thesportsdb.Leagues().get_plot_it(self.league)
		elif settings.getSetting('addon-language') == '4':
			self.league_plot = thesportsdb.Leagues().get_plot_cn(self.league)
		elif settings.getSetting('addon-language') == '5':
			self.league_plot = thesportsdb.Leagues().get_plot_jp(self.league)
		elif settings.getSetting('addon-language') == '6':
			self.league_plot = thesportsdb.Leagues().get_plot_ru(self.league)
		elif settings.getSetting('addon-language') == '7':
			self.league_plot = thesportsdb.Leagues().get_plot_es(self.league)
		elif settings.getSetting('addon-language') == '8':
			self.league_plot = thesportsdb.Leagues().get_plot_pt(self.league)
		elif settings.getSetting('addon-language') == '9':
			self.league_plot = thesportsdb.Leagues().get_plot_se(self.league)
		elif settings.getSetting('addon-language') == '10':
			self.league_plot = thesportsdb.Leagues().get_plot_nl(self.league)
		elif settings.getSetting('addon-language') == '11':
			self.league_plot = thesportsdb.Leagues().get_plot_hu(self.league)
		elif settings.getSetting('addon-language') == '12':
			self.league_plot = thesportsdb.Leagues().get_plot_no(self.league)
		elif settings.getSetting('addon-language') == '13':
			self.league_plot = thesportsdb.Leagues().get_plot_pl(self.league)
		
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
			
		teams_list = thesportsdb.Lookups(tsdbkey).lookup_all_teams(self.league_id)["teams"]
		team_number = len(teams_list)
		#set team number on top bar
		self.getControl(334).setLabel(str(team_number)+' Teams')
		
		#this is the controller for plotview
		
		table_check = False
		if self.sport == 'soccer' or self.sport == 'football':
			table_list = thesportsdb.Lookups(tsdbkey).lookup_leaguetables(self.league_id,None)["table"]
			if table_list:
				table_check = True
				for team in table_list:
					team_id = thesportsdb.Tables().get_id(team)
					team_points = thesportsdb.Tables().get_points(team)
					for teamfull in teams_list:
						if thesportsdb.Teams().get_id(teamfull) == team_id:
							if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(teamfull)
							else: team_name = thesportsdb.Teams().get_alternativefirst(teamfull)
							team_badge = thesportsdb.Teams().get_badge(teamfull)
							team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(teamfull)
							if team_fanart_general_list:
								team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
							else: team_fanart = self.league_fanart
							teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
							teamitem.setProperty('team_name',team_name)
							teamitem.setProperty('team_name_short',team_name)
							teamitem.setProperty('team_logo',team_badge)
							teamitem.setProperty('team_fanart',team_fanart)
							teamitem.setProperty('team_id',team_id)
							teamitem.setProperty('team_points',team_points)
							self.getControl(980).addItem(teamitem)
				
							
		if self.sport != 'soccer' or self.sport == 'football' or not table_check:
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
				teamitem.setProperty('team_name_long',team_name)
				teamitem.setProperty('team_banner',team_banner)
				teamitem.setProperty('team_logo',team_badge)
				teamitem.setProperty('team_jersey',team_jersey)
				teamitem.setProperty('team_fanart',team_fanart)
				teamitem.setProperty('team_id',team_id)
				self.getControl(980).addItem(teamitem)
			if self.sport == 'golf': self.getControl(336).setLabel('[COLOR labelheader]Golfers[/COLOR]')			
			else: self.getControl(336).setLabel('[COLOR labelheader]Teams[/COLOR]')
			self.getControl(335).setVisible(False)

		
		for team in teams_list:
			if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team)
			else: team_name = thesportsdb.Teams().get_alternativefirst(team)
			team_badge = thesportsdb.Teams().get_badge(team)
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
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(plotview,1,home)")
		settings.setSetting("view_type_league",'plotview')
		self.mode = ''

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
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(badgeview,1,home)")
		settings.setSetting("view_type_league",'badgeview')
		self.mode = ''

		self.getControl(2).setLabel("League: BadgeView")
		
	def setjerseyview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(jerseyview,1,home)")
		settings.setSetting("view_type_league",'jerseyview')
		self.mode = ''

		self.getControl(2).setLabel("League: JerseyView")
		
	def setbannerview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(bannerview,1,home)")
		settings.setSetting("view_type_league",'bannerview')
		self.mode = ''

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
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("SetProperty(newsview,1,home)")
		settings.setSetting("view_type_league",'newsview')
		self.mode = ''

		self.getControl(2).setLabel("League: NewsView")
		
	def settablesview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#tables stuff
		teams_list = thesportsdb.Lookups(tsdbkey).lookup_all_teams(self.league_id)["teams"]
		table_list = thesportsdb.Lookups(tsdbkey).lookup_leaguetables(self.league_id,None)["table"]
		pos=0
		if table_list:
			for team in table_list:
				pos += 1
				team_id = thesportsdb.Tables().get_id(team)
				team_points = thesportsdb.Tables().get_points(team)
				team_played = thesportsdb.Tables().get_totalplayed(team)
				team_wins = thesportsdb.Tables().get_wins(team)
				team_lost = thesportsdb.Tables().get_loss(team)
				team_draws = thesportsdb.Tables().get_draws(team)
				team_gs = thesportsdb.Tables().get_goalsscored(team)
				team_gc = thesportsdb.Tables().get_goalssuffered(team)
				team_gd = thesportsdb.Tables().get_goalsdifference(team)
				for teamfull in teams_list:
					if thesportsdb.Teams().get_id(teamfull) == team_id:
						if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(teamfull)
						else: team_name = thesportsdb.Teams().get_alternativefirst(teamfull)
						team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(teamfull)
						if team_fanart_general_list:
							team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
						else: team_fanart = self.league_fanart
						team_badge = thesportsdb.Teams().get_badge(teamfull)
						teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
						teamitem.setProperty('team_name',team_name)
						teamitem.setProperty('team_fanart',team_fanart)
						teamitem.setProperty('team_played',team_played)
						teamitem.setProperty('team_wins',team_wins)
						teamitem.setProperty('team_draws',team_draws)
						teamitem.setProperty('team_losts',team_lost)
						teamitem.setProperty('team_gs',team_gs)
						teamitem.setProperty('team_gc',team_gc)
						teamitem.setProperty('team_gd',team_gd)
						teamitem.setProperty('position',str(pos)+' -')
						teamitem.setProperty('team_logo',team_badge)
						teamitem.setProperty('team_id',team_id)
						teamitem.setProperty('team_points',team_points)
						self.getControl(990).addItem(teamitem)
						
		#		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(tablesview,1,home)")
		settings.setSetting("view_type_league",'tablesview')
		self.mode = ''

		self.getControl(2).setLabel("League: TablesView")
	
		
			
	def setnextmatchview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#next matches stuff
		event_next_list = thesportsdb.Schedules(tsdbkey).eventsnextleague(self.league_id)["events"]
		league_teams = thesportsdb.Lookups(tsdbkey).lookup_all_teams(self.league_id)["teams"]		
		
		if event_next_list:
			for event in event_next_list:
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				event_fanart = thesportsdb.Events().get_fanart(event)
				
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
					home_team_dict = None
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == home_team_id:
							home_team_dict = team
							break 
					if not home_team_dict: home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: team_name = home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = None
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == away_team_id:
							away_team_dict = team
							break 
					if not away_team_dict: away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
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
				else:
					if event_fanart and event_fanart != 'None' and event_fanart != 'null':
						game.setProperty('StadiumThumb',event_fanart)
					
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
				
				# date + time + timedelay
				event_fullstring = event_timestring + timedelay
				game.setProperty('date',event_fullstring)
				if event_race: 
					game.setProperty('EventName',event_name) 
				if event_round and event_round != '0': game.setProperty('round',round_label)
				self.getControl(987).addItem(game)
				
				
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(nextmatchview,1,home)")
		settings.setSetting("view_type_league",'nextmatchview')
		self.mode = ''

		self.getControl(2).setLabel("League: NextMatchView")

	def setlastmatchview(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#last matches stuff
		event_last_list = thesportsdb.Schedules(tsdbkey).eventspastleague(self.league_id)["events"]
		league_teams = thesportsdb.Lookups(tsdbkey).lookup_all_teams(self.league_id)["teams"]
		if event_last_list:
			for event in event_last_list:

				
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				event_id = thesportsdb.Events().get_eventid(event)
				event_fanart = thesportsdb.Events().get_fanart(event)
				event_sport = thesportsdb.Events().get_sport(event)
				
				event_datetime = thesportsdb.Events().get_datetime_object(event)
				if event_datetime:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(event_datetime)
					event_datetime=db_time.astimezone(my_location)
				
				if event_sport.lower() == 'motorsport' or event_sport.lower() == 'golf':
					if event_sport.lower() == 'motorsport':
						home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					elif event_sport.lower() == 'golf':
						home_team_logo = os.path.join(addonpath,art,'golf.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''
				else:
					home_team_dict = None
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == home_team_id:
							home_team_dict = team
							break
					#make the lookup only if we can't match the team
					if not home_team_dict: home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = None
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == away_team_id:
							away_team_dict = team
							break
					#make the request only if we can't match the team
					if not away_team_dict: away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					event_round = thesportsdb.Events().get_round(event)
					if event_round:
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
				if event_sport.lower() != 'golf' and event_sport.lower() != 'motorsport':
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
						game.setProperty('StadiumThumb',event_fanart)
				# date + time + timedelay
				event_fullstring = event_timestring + timedelay
				game.setProperty('date',event_fullstring)
				self.getControl(988).addItem(game)
				
		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(lastmatchview,1,home)")
		settings.setSetting("view_type_league",'lastmatchview')
		self.mode = ''

		self.getControl(2).setLabel("League: LastMatchView")
		
	def setfixturesview(self,roundnum = None):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#last matches stuff
		self.roundnum = roundnum
		if not roundnum:
			event_last_list = thesportsdb.Schedules(tsdbkey).eventspastleague(self.league_id)["events"]
			event_next_list = thesportsdb.Schedules(tsdbkey).eventsnextleague(self.league_id)["events"]
			if event_next_list:
				if event_last_list:
					roundlast = thesportsdb.Events().get_round(event_last_list[0])
					roundnext = thesportsdb.Events().get_round(event_next_list[0])
					if roundlast == roundnext: self.roundnum = roundlast
					else: self.roundnum = roundnext
				else:
					self.roundnum = thesportsdb.Events().get_round(event_next_list[0])	
			else:
				#set round as last list
				if event_last_list:
					self.roundnum = thesportsdb.Events().get_round(event_last_list[0])
				else: sys.exit(0) #TODO close progress
				
		else: pass # roundnum is already defined
		
		event_list = thesportsdb.Schedules(tsdbkey).eventsround(self.league_id,self.roundnum,None)["events"]
		items_to_add = []
		
		league_teams = thesportsdb.Lookups(tsdbkey).lookup_all_teams(self.league_id)["teams"]
		if event_list:
			for event in event_list:
				#init result and versus
				event_result_present = ''
				event_vs_present = ''
				#
				
				event_datetime = thesportsdb.Events().get_datetime_object(event)
				if event_datetime:
					#datetime object conversion goes here
					db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(event_datetime)
					my_timezone= settings.getSetting('timezone')
					my_location=pytz.timezone(pytz.all_timezones[int(my_timezone)])
					event_datetime=db_time.astimezone(my_location)
				
				
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				event_id = thesportsdb.Events().get_eventid(event)

				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''
				else:
					home_team_dict = None
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == home_team_id:
							home_team_dict = team
							break
					#make the lookup only if we can't match the team
					if not home_team_dict: home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = None
					for team in league_teams:
						if thesportsdb.Teams().get_id(team) == away_team_id:
							away_team_dict = team
							break
					#make the request only if we can't match the team
					if not away_team_dict: away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
					
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					#check if result is None-None and if so define vs instead of result
					if result == 'None-None': event_vs_present = 'vs'
					else: event_result_present = result
				
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
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				if not event_race:
					game.setProperty('HomeTeamLong',home_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('StadiumThumb',stadium_fanart)
					game.setProperty('AwayTeamLong',away_team_name)
					game.setProperty('event_result',event_result_present)
					game.setProperty('event_vs',event_vs_present)
					game.setProperty('event_id',event_id)
				else:
					game.setProperty('EventName',event_name)
				# date + time + timedelay
				game.setProperty('date',event_timestring)
				items_to_add.append(game)
		
		if items_to_add:	
			self.getControl(991).reset()
			self.getControl(9025).setLabel("[B]Round "+str(self.roundnum)+"[/B]")
			self.getControl(991).addItems(items_to_add)
				
		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(fixturesview,1,home)")
		settings.setSetting("view_type_league",'fixturesview')
		self.mode = ''

		self.getControl(2).setLabel("League: FixturesView")
		
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
		xbmc.executebuiltin("ClearProperty(tablesview,Home)")
		xbmc.executebuiltin("ClearProperty(nextview,Home)")
		xbmc.executebuiltin("ClearProperty(fixturesview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(jerseyview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(videosview,1,home)")
		settings.setSetting("view_type_league",'videosview')
		self.mode = ''

		self.getControl(2).setLabel("League: VideosView")			
		
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.control_panel = xbmc.getCondVisibility("Control.HasFocus(2)")
			if self.control_panel:
				xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				self.setFocusId(983)
			else:
				self.close()
		else:
			checkjersey = xbmc.getCondVisibility("Control.HasFocus(981)")
			checkbadge = xbmc.getCondVisibility("Control.HasFocus(985)")
			checkplot = xbmc.getCondVisibility("Control.HasFocus(980)")
			checkbanner = xbmc.getCondVisibility("Control.HasFocus(984)")
			checklastmatch = xbmc.getCondVisibility("Control.HasFocus(988)")
			checknextmatch = xbmc.getCondVisibility("Control.HasFocus(987)")
			checktables = xbmc.getCondVisibility("Control.HasFocus(990)")
			checkfixtures = xbmc.getCondVisibility("Control.HasFocus(991)")
			
			if checkbadge or checkplot or checkbanner or checklastmatch or checknextmatch or checkjersey or checktables or checkfixtures:
				if checkbadge:
					fanart = self.getControl(985).getSelectedItem().getProperty('team_fanart')
				elif checktables:
					fanart = self.getControl(990).getSelectedItem().getProperty('team_fanart')
				elif checkplot:
					fanart = self.getControl(980).getSelectedItem().getProperty('team_fanart')
				elif checkbanner:
					fanart = self.getControl(984).getSelectedItem().getProperty('team_fanart')
				elif checkjersey:
					fanart = self.getControl(981).getSelectedItem().getProperty('team_fanart')
				elif checkfixtures:
					fanart = self.getControl(991).getSelectedItem().getProperty('StadiumThumb')
					if not fanart or fanart == 'None': fanart = self.league_fanart
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
			elif seleccionado == 'tables':
				self.settablesview()
			elif seleccionado == 'fixtures':
				self.setfixturesview()
			
					
		elif controlId == 980 or controlId == 984 or controlId == 985 or controlId == 981 or controlId == 990:
			team = self.getControl(controlId).getSelectedItem().getProperty('team_id')
			team_fanart = self.getControl(controlId).getSelectedItem().getProperty('team_fanart')
			teamview.start([team,self.sport,team_fanart,'plotview'])
		


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
			
		elif controlId == 988 or controlId == 991:
			event_id = self.getControl(controlId).getSelectedItem().getProperty('event_id')
			if self.sport.lower() == 'soccer' or self.sport.lower() == 'football':
				soccermatchdetails.start([False,event_id])
			else:
				eventdetails.start([event_id])
			
		elif controlId == 9024: #previous round
			if self.roundnum and self.roundnum != '0':
				try:
					int(self.roundnum)-1
					Proceed = True
				except: Proceed = False
				if Proceed:
					self.setfixturesview(int(self.roundnum)-1)
			
		elif controlId == 9026: #next round
			if self.roundnum and self.roundnum != '0':
				try:
					int(self.roundnum)+1
					Proceed = True
				except: Proceed = False
				if Proceed:
					self.setfixturesview(int(self.roundnum)+1)
			
	
		
