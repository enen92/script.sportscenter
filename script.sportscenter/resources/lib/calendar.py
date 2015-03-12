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
	window = dialog_league('DialogCalendar.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_league(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		#self.league = eval(eval(args[3])[0])
		#self.sport = eval(args[3])[1]

	def onInit(self):	
	
		#self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		
		#xbmc.executebuiltin("SetProperty(loading,1,home)")
		
		#self.league_id = thesportsdb.Leagues().get_id(self.league)
		#self.league_rss = thesportsdb.Leagues().get_rssurl(self.league)
		#self.league_youtube = thesportsdb.Leagues().get_youtube(self.league)
		
		self.getControl(911).setImage(addon_fanart)
		self.getControl(333).setLabel('Calendar View')
		
		
		#populate panel left
		menu = [('Today','2010-09-12'),('Tomorrow','2010-09-12'),('Friday','2010-09-12'),('Saturday','2010-09-12'),('Sunday','2010-09-12'),('Monday','2010-09-12'),('Tuesday','2010-09-12'),('Wednesday','2010-09-12'),('Thursday','2010-09-12'),('Friday','2010-09-12'),('Saturday','2010-09-12')]
	
		self.getControl(983).reset()	   
		for data_string,date in menu:
			menu_entry = xbmcgui.ListItem(data_string)
			menu_entry.setProperty('menu_entry', data_string)
			menu_entry.setProperty('entry_date', date)
			self.getControl(983).addItem(menu_entry)
			
		self.setnextmatchview()
		

	def setnextmatchview(self):
		#self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")	
		#next matches stuff
		event_next_list = thesportsdb.Schedules().eventsnextleague("4328")["events"]
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


		
#	def onAction(self,action):
#		if action == 92 or action == 'PreviousMenu':
#			#if not self.control_panel: 
#			if 2==1:
#				pass
				#xbmc.executebuiltin("ClearProperty(MediaMenu,Home)")
				#self.setFocusId(980)
#			else: 
				#pass
#				self.close()
				#competlist.start(self.sport)
#		else:
#			checkjersey = xbmc.getCondVisibility("Control.HasFocus(981)")
#			checkbadge = xbmc.getCondVisibility("Control.HasFocus(985)")
#			checkplot = xbmc.getCondVisibility("Control.HasFocus(980)")
#			checkbanner = xbmc.getCondVisibility("Control.HasFocus(984)")
#			checklastmatch = xbmc.getCondVisibility("Control.HasFocus(988)")
#			checknextmatch = xbmc.getCondVisibility("Control.HasFocus(987)")
#			
#			if checkbadge or checkplot or checkbanner or checklastmatch or checknextmatch or checkjersey:
#				if checkbadge:
#					fanart = self.getControl(985).getSelectedItem().getProperty('team_fanart')
#				elif checkplot:
#					fanart = self.getControl(980).getSelectedItem().getProperty('team_fanart')
#				elif checkbanner:
#					fanart = self.getControl(984).getSelectedItem().getProperty('team_fanart')
#				elif checkjersey:
#					fanart = self.getControl(981).getSelectedItem().getProperty('team_fanart')
#				elif checklastmatch:
#					fanart = self.getControl(988).getSelectedItem().getProperty('StadiumThumb')
#					if not fanart or fanart == 'None': fanart = self.league_fanart
#				elif checknextmatch:
#					fanart = self.getControl(987).getSelectedItem().getProperty('StadiumThumb')
#					if not fanart or fanart == 'None': fanart = self.league_fanart
#				self.getControl(912).setImage(fanart)
#			else: 
#				if self.league_fanart: self.getControl(912).setImage(self.league_fanart)

			
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
	
		
