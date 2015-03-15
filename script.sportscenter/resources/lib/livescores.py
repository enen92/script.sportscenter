import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib
import thesportsdb
import datetime
from random import randint
from centerutils.common_variables import *
from centerutils.datemanipulation import *
import competlist as competlist
import teamview as teamview

def start(data_list):
	window = dialog_livescores('DialogLivescores.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_livescores(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		#self.league = eval(eval(args[3])[0])
		#self.sport = eval(args[3])[1]

	def onInit(self):	
	
		#self.livescores = thesportsdb.LiveScores().latestsoccer()["teams"]["Match"][0]
		#print self.livescores
		#print len(self.livescores)
			
		#self.setFocusId(983)
		#self.getControl(983).selectItem(0)
		#self.fill_calendar(menu[0][1])
		#self.fill_calendar('2015-03-17')
		self.fill_livescores()
		
	def fill_livescores(self):
		items_to_add = []
		self.livescores = thesportsdb.LiveScores().latestsoccer()["teams"]["Match"]
		if self.livescores:
			for event in self.livescores:
				try:
					event_home_id = thesportsdb.Livematch().get_home_id(event)
					event_away_id = thesportsdb.Livematch().get_away_id(event)
					event_identifier = event_home_id + event_away_id
					game = xbmcgui.ListItem(event_identifier)
					#get home and away dicts
					home_team_dict = thesportsdb.Lookups().lookupteam(event_home_id)["teams"][0]
					away_team_dict = thesportsdb.Lookups().lookupteam(event_away_id)["teams"][0]
					#set hometeamname
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
					else: team_name = home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
					if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
					else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
					#logos
					home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
					away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
					#current_score
					home_goals = thesportsdb.Livematch().get_homegoals_number(event)
					away_goals = thesportsdb.Livematch().get_homegoals_number(event)
					result = '%s-%s' % (home_goals,away_goals)
					#league info
					competition = thesportsdb.Livematch().get_league(event)
					#roundnum = thesportsdb.Livematch().get_round(event)
					#if roundnum and roudnum != 'None':
					#	competition = competition + ' - Round ' + roundnum
					print "start to append data"
					if ' ' in home_team_name:
						if len(home_team_name) > 12: game.setProperty('HomeTeamLong',home_team_name)
						else: game.setProperty('HomeTeamShort',home_team_name)
					else: game.setProperty('HomeTeamShort',home_team_name)
					game.setProperty('HomeTeamLogo',home_team_logo)
					if ' ' in away_team_name:
						if len(away_team_name) > 12: game.setProperty('AwayTeamLong',away_team_name)
						else: game.setProperty('AwayTeamShort',away_team_name)
					else: game.setProperty('AwayTeamShort',away_team_name)
					game.setProperty('AwayTeamLogo',away_team_logo)
					game.setProperty('result',result)
					game.setProperty('competition',competition)
					self.getControl(987).addItem(game)
				except: pass
				#num_items = self.getControl(987).size()
				#for i in xrange(1,num_items):
				#	self.getControl(987).getListItem(0).getControl(333)
				#self.getControl(333).setPercent(100)
				
				
				
		

	def fill_calendar(self,datestring):
		#self.getControl(92).setImage(os.path.join(addonpath,art,'loadingsports',self.sport+'.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.getControl(987).reset()
		#next matches stuff
		#event_next_list = thesportsdb.Schedules().eventsnextleague("4328")["events"]
		event_next_list = thesportsdb.Schedules().eventsday(datestring,None,None)["events"][0:3]
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
					if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
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
		if controlId == 983:
			listControl = self.getControl(controlId)
			selected_date=listControl.getSelectedItem().getProperty('entry_date')
			self.fill_calendar(selected_date)
	
		
