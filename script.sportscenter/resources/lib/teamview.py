import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,datetime
import thesportsdb,feedparser
from random import randint
from centerutils.common_variables import *
from centerutils.youtube import *
from centerutils.rssparser import *
from centerutils.datemanipulation import *
import competlist as competlist
import stadium as stadium
import tweetbuild as tweetbuild


def teamdetails(team_id):
	window = dialog_teamdetails('DialogTeamInfo.xml',addonpath,'Default',team_id)
	window.doModal()

class dialog_teamdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.team_id = str(args[3])
		self.event_last_list = thesportsdb.Schedules().eventslast(self.team_id)['results']
		self.event_next_list = thesportsdb.Schedules().eventsnext(self.team_id)['events']

	def onInit(self):
		self.team = thesportsdb.Lookups().lookupteam(self.team_id)['teams'][0]
		self.team_name = thesportsdb.Teams().get_name(self.team)
		self.team_badge = thesportsdb.Teams().get_badge(self.team)
		self.team_fanart = thesportsdb.Teams().get_fanart_general1(self.team)
		self.team_stadiumfanart = thesportsdb.Teams().get_stadium_thumb(self.team)
		self.team_clear = thesportsdb.Teams().get_logo(self.team)
		self.team_jersey = thesportsdb.Teams().get_team_jersey(self.team)
		self.founded = thesportsdb.Teams().get_formedyear(self.team)
		self.plot = thesportsdb.Teams().get_plot_en(self.team)
		self.sport = thesportsdb.Teams().get_sport(self.team)
		self.manager = thesportsdb.Teams().get_manager(self.team)
		self.stadium_name = thesportsdb.Teams().get_stadium(self.team)
		self.location = thesportsdb.Teams().get_stadium_location(self.team)
		self.league = thesportsdb.Teams().get_league(self.team)
		self.likes = thesportsdb.Teams().get_likes(self.team)
		if self.likes == 'None': self.likes = '0'
		
		self.getControl(1).setLabel(self.team_name)
		self.getControl(2).setImage(self.team_badge)
		self.getControl(3).setImage(self.team_fanart)
		self.getControl(4).setImage(self.team_stadiumfanart)
		self.getControl(5).setImage(self.team_clear)
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
		
		#Next match information
		if self.event_next_list:
			self.nextevent = self.event_next_list[0]
			self.hometeam = thesportsdb.Events().get_hometeamname(self.nextevent)
			self.awayteam = thesportsdb.Events().get_awayteamname(self.nextevent)
			self.home_away = ''
			if self.team_name == self.hometeam:
				self.home_away = 'HOME'
				self.searchid = thesportsdb.Events().get_awayteamid(self.nextevent)
			else:
				self.home_away = 'AWAY'
				self.searchid = thesportsdb.Events().get_hometeamid(self.nextevent)
			self.getControl(41).setLabel(self.home_away)
			self.nexteam = thesportsdb.Lookups().lookupteam(self.searchid)['teams'][0]
			self.nextlogo = thesportsdb.Teams().get_badge(self.nexteam)
			self.getControl(40).setImage(self.nextlogo)
			self.nextdate = thesportsdb.Events().get_eventdate(self.nextevent).split('-')
			if len(self.nextdate) == 3:
				now = datetime.datetime.now()
				datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
				eventdate = datetime.datetime(int(self.nextdate[0]), int(self.nextdate[1]), int(self.nextdate[2]))
				day_difference = abs(eventdate - datenow).days
				if day_difference == 0:
					string = 'Today'
				elif day_difference == 1:
					string = 'Tomorrow'
				else:
					string = 'In ' + str(day_difference) + ' days'
				
				self.getControl(42).setLabel(string)


		
		i = 0
		controlinicial = 30
		winnumber = 0
		for event in reversed(self.event_last_list):
			awayteam = thesportsdb.Events().get_awayteamname(event)
			hometeam = thesportsdb.Events().get_hometeamname(event)
			awayscore = thesportsdb.Events().get_awayscore(event)
			homescore = thesportsdb.Events().get_homescore(event)
			if hometeam == self.team_name:
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
			
		
			
		#self.getControl(13).setImage(os.path.join((addonpath,art,'redsquare.png'))
		
	def onClick(self,controlId):
		if controlId == 210:
			stadium.start(self.team)
		elif controlId == 211:
			twitter_name = thesportsdb.Teams().get_team_twitter(self.team)
			if twitter_name: 
				twitter_name = twitter_name.split('/')[-1]
				tweetbuild.tweets(twitter_name)



def start(data_list):
	window = dialog_team('DialogTeam.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_team(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.team_id = eval(args[3])[0]
		self.sport = eval(args[3])[1]
		self.team = thesportsdb.Lookups().lookupteam(self.team_id)['teams'][0]
		

	def onInit(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		#self.league_id = thesportsdb.Leagues().get_id(self.league)
		
		self.getControl(911).setImage(os.path.join(addonpath,art,"sports",self.sport + '.jpg'))
		
		#set team badge
		self.team_badge = thesportsdb.Teams().get_badge(self.team)
		if self.team_badge: self.getControl(934).setImage(self.team_badge)
		
		self.getControl(983).reset()
		#populate panel left
		menu = [('Home','home'),('Team Details','details'),('News','news'),('Tweets','tweets'),('Videos','videos'),('Players','players'),('Stadium','stadium'),('Fixtures','nextmatch'),('Results','lastmatch')]
			   
		for entry,entry_id in menu:
			menu_entry = xbmcgui.ListItem(entry)
			menu_entry.setProperty('menu_entry', entry)
			menu_entry.setProperty('entryid', entry_id)
			self.getControl(983).addItem(menu_entry)
			
		#set team fanart
		self.team_fanartlist = thesportsdb.Teams().get_fanart_general_list(self.team)
		if self.team_fanartlist:
			self.team_fanart = self.team_fanartlist[randint(0,len(self.team_fanartlist)-1)]
			self.getControl(912).setImage(self.team_fanart)
		else: self.team_fanart = os.path.join(addonpath,art,'sports',self.sport+'.jpg')

		self.player_fanart = thesportsdb.Teams().get_fanart_player(self.team)
		if self.player_fanart:
			self.getControl(429).setImage(self.player_fanart)
		else:
			self.getControl(429).setImage(self.team_fanart)

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
		
		self.getControl(980).reset()
		self.getControl(984).reset()
		self.getControl(985).reset()
			
		teams_list = thesportsdb.Lookups().lookup_all_teams(self.league_id)["teams"]
		for team in teams_list:
			team_name = thesportsdb.Teams().get_name(team)
			team_badge = thesportsdb.Teams().get_badge(team)
			team_banner = thesportsdb.Teams().get_banner(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = ''
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_name',team_name)
			teamitem.setProperty('team_banner',team_banner)
			teamitem.setProperty('team_logo',team_badge)
			teamitem.setProperty('team_fanart',team_fanart)
			self.getControl(980).addItem(teamitem)
			
		for team in teams_list:
			team_name = thesportsdb.Teams().get_name(team)
			team_banner = thesportsdb.Teams().get_banner(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = ''
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_banner',team_banner)
			teamitem.setProperty('team_fanart',team_fanart)
			self.getControl(984).addItem(teamitem)
			
		for team in teams_list:
			team_name = thesportsdb.Teams().get_name(team)
			team_badge = thesportsdb.Teams().get_badge(team)
			team_fanart_general_list = thesportsdb.Teams().get_fanart_general_list(team)
			if team_fanart_general_list:
				team_fanart = team_fanart_general_list[randint(0,len(team_fanart_general_list)-1)]
			else: team_fanart = ''
			teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
			teamitem.setProperty('team_badge',team_badge)
			teamitem.setProperty('team_fanart',team_fanart)
			self.getControl(985).addItem(teamitem)
		return
		
	def setplotview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		#self.setleagueinfo()
		
		#set team plot
		#set league plot
		self.team_plot = thesportsdb.Teams().get_plot_en(self.team)
		self.getControl(430).setText(self.team_plot)
		
		#set team formed year
		self.team_formedyear = thesportsdb.Teams().get_formedyear(self.team)
		self.getControl(428).setLabel('[COLOR labelheader]Established:[CR][/COLOR]' + self.team_formedyear)
		
		#set team name
		self.team_name = thesportsdb.Teams().get_name(self.team)
		self.getControl(427).setLabel('[COLOR labelheader]Team Name:[CR][/COLOR]' + self.team_name)
		#		
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(bannerview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
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
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(badgeview,1,home)")
		settings.setSetting("view_type_league",'badgeview')

		self.getControl(2).setLabel("League: PlotView")
		
	def setbannerview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.setleagueinfo()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		xbmc.executebuiltin("ClearProperty(lastmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(plotview,Home)")
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(nextmatchview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("ClearProperty(videosview,Home)")
		xbmc.executebuiltin("SetProperty(bannerview,1,home)")
		settings.setSetting("view_type_league",'bannerview')

		self.getControl(2).setLabel("League: BannerView")
			
		
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
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("SetProperty(newsview,1,home)")
		settings.setSetting("view_type_league",'newsview')

		self.getControl(2).setLabel("League: LastMatchView")	
		try:self.getControl(986).selectItem(0)
		except:pass
			
	def setnextmatchview(self):
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#next matches stuff
		event_next_list = thesportsdb.Schedules().eventsnext(self.team_id)['events']
		self.getControl(987).reset()
		if event_next_list:
			for event in event_next_list:
				event_date = thesportsdb.Events().get_eventdate(event)
				event_date_parsed = event_date.split('-')
				if event_date_parsed:
					now = datetime.datetime.now()
					datenow = datetime.datetime(int(now.year), int(now.month), int(now.day))
					eventdate = datetime.datetime(int(event_date_parsed[0]), int(event_date_parsed[1]), int(event_date_parsed[2]))
					day_difference = abs(eventdate - datenow).days
					if day_difference == 0: presented_date='Today'
					elif day_difference == 1: presented_date='Tomorrow'
					else: presented_date = event_date_parsed[2] + '-' + get_month_short(event_date_parsed[1]) +'   '+str(day_difference)+' days'
				else: presented_date = event_date_parsed[2] + '-' + get_month_short(event_date_parsed[1])
				event_fullname = thesportsdb.Events().get_eventtitle(event)
				event_race = thesportsdb.Events().get_racelocation(event)
				if event_race:
					home_team_logo = os.path.join(addonpath,art,'raceflag.png')
					event_name = thesportsdb.Events().get_eventtitle(event)
					event_round = ''		
				else:
					home_team_id = thesportsdb.Events().get_hometeamid(event)
					home_team_dict = thesportsdb.Lookups().lookupteam(home_team_id)["teams"][0]
					home_team_name = thesportsdb.Events().get_hometeamname(event)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups().lookupteam(away_team_id)["teams"][0]
					away_team_name = thesportsdb.Events().get_awayteamname(event)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					event_round = thesportsdb.Events().get_round(event)
					if event_round:
						round_label = 'Round ' + str(event_round)
				
					if len(home_team_name) > 8: 
						if xbmc.getSkinDir() == 'skin.aeon.nox.5': home_team_name = home_team_name.replace(' ','[CR]')
						else: pass
					if len(away_team_name) > 8: 
						if xbmc.getSkinDir() == 'skin.aeon.nox.5': away_team_name = away_team_name.replace(' ','[CR]')
						else: pass
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				if not event_race:
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('StadiumThumb',stadium_fanart)
					game.setProperty('vs','VS')
				game.setProperty('date',presented_date)
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
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(nextmatchview,1,home)")
		settings.setSetting("view_type_league",'nextmatchview')

		self.getControl(2).setLabel("League: LastMatchView")

	def setlastmatchview(self):	
		self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		i = 0
		controlinicial = 30
		winnumber = 0
		
		#last matches stuff
		event_last_list = thesportsdb.Schedules().eventslast(self.team_id)['results']
		if event_last_list:
			for event in event_last_list:
				awayteam = thesportsdb.Events().get_awayteamname(event)
				hometeam = thesportsdb.Events().get_hometeamname(event)
				awayscore = thesportsdb.Events().get_awayscore(event)
				homescore = thesportsdb.Events().get_homescore(event)
				if hometeam == self.team_name:
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
					home_team_name = thesportsdb.Events().get_hometeamname(event)
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
					away_team_id = thesportsdb.Events().get_awayteamid(event)
					away_team_dict = thesportsdb.Lookups().lookupteam(away_team_id)["teams"][0]
					away_team_name = thesportsdb.Events().get_awayteamname(event)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					home_score = thesportsdb.Events().get_homescore(event)
					away_score = thesportsdb.Events().get_awayscore(event)
					result = str(home_score) + '-' + str(away_score)
					event_round = thesportsdb.Events().get_round(event)
					if event_round:
						round_label = 'Round ' + str(event_round)
				
					if len(home_team_name) > 8: 
						if xbmc.getSkinDir() == 'skin.aeon.nox.5': home_team_name = home_team_name.replace(' ','[CR]')
						else: pass
					if len(away_team_name) > 8: 
						if xbmc.getSkinDir() == 'skin.aeon.nox.5': away_team_name = away_team_name.replace(' ','[CR]')
						else: pass
				
				game = xbmcgui.ListItem(event_fullname)
				game.setProperty('HomeTeamLogo',home_team_logo)
				if not event_race:
					game.setProperty('HomeTeam',home_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('StadiumThumb',stadium_fanart)
					game.setProperty('AwayTeam',away_team_name)
					game.setProperty('match_result',result)
					if event_round: game.setProperty('round',round_label)
				else:
					game.setProperty('EventName',event_name) 
				game.setProperty('date',event_date)
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
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
		xbmc.executebuiltin("ClearProperty(newsview,Home)")
		xbmc.executebuiltin("SetProperty(lastmatchview,1,home)")
		settings.setSetting("view_type_league",'lastmatchview')

		self.getControl(2).setLabel("League: LastMatchView")
		
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
		xbmc.executebuiltin("ClearProperty(badgeview,Home)")
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
			checkbadge = xbmc.getCondVisibility("Control.HasFocus(985)")
			checkplot = xbmc.getCondVisibility("Control.HasFocus(980)")
			checkbanner = xbmc.getCondVisibility("Control.HasFocus(984)")
			checklastmatch = xbmc.getCondVisibility("Control.HasFocus(988)")
			checknextmatch = xbmc.getCondVisibility("Control.HasFocus(987)")
			if checkbadge or checkplot or checkbanner or checklastmatch or checknextmatch:
				if checkbadge:
					fanart = self.getControl(985).getSelectedItem().getProperty('team_fanart')
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
			else: 
				self.getControl(912).setImage(self.team_fanart)


			
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
			elif seleccionado == 'stadium':
				stadium.start(self.team)	
			elif seleccionado == 'details':
				teamdetails(self.team_id)
			elif seleccionado == 'tweets':
				twitter_name = thesportsdb.Teams().get_team_twitter(self.team)
				if twitter_name: 
					twitter_name = twitter_name.split('/')[-1]
					tweetbuild.tweets(twitter_name)
				else: pass
					
					

		elif controlId == 2:
			active_view_type = self.getControl(controlId).getLabel()
			if active_view_type == "League: PlotView":
				self.setvideosview()
			elif active_view_type == "League: VideosView":
				self.setbannerview()
			elif active_view_type == "League: BannerView":
				self.setbadgeview()	
			elif active_view_type == "League: BadgeView":
				self.newsview()
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
			
	
		
