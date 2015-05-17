import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib
import thesportsdb
import datetime
import os
import re
import threading
from random import randint
from centerutils.common_variables import *
from centerutils.datemanipulation import *
import competlist as competlist
import teamview as teamview
import contextmenubuilder
import tweetbuild


def start(data_list):
	window = dialog_calendar('DialogCalendar.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_calendar(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.date_string = eval(args[3])

	def onInit(self):	
	
		self.getControl(911).setImage(addon_fanart)
		self.getControl(333).setLabel('Calendar View')
		self.ignored_leagues = os.listdir(ignoredleaguesfolder)
		self.rmleaguescalendar = os.listdir(ignoreleaguecalendar)
		
		#Change background if custom is defined
		if settings.getSetting('calendar-background-type') == '1' and settings.getSetting('calendar-background-custom') != '':
			self.getControl(912).setImage(settings.getSetting('calendar-background-custom'))
		
		
		#Populate week days
		menu = []
		#grab datetime now and transform into a timezone object based on user timezone
		date_now = datetime.datetime.now()
		date_now_mytz = pytz.timezone(str(pytz.timezone(str(my_location)))).localize(date_now)
		#convert datetime timezone object to the timezone of the database
		date_now_tsdb = date_now_mytz.astimezone(my_location)
		menu.append(('Today, %s' % (date_now_mytz.day),'%s-%s-%s' % (str(date_now_tsdb.year),str(date_now_tsdb.month),str(date_now_tsdb.day))))

		for i in range(7): 
			date_now_mytz += datetime.timedelta(days=1)
			date_now_tsdb += datetime.timedelta(days=1)
			if i == 0: day_string ='%s, %s' % ('Tomorrow',date_now_mytz.day)
			else:
				day_string = '%s, %s' % (get_weekday(date_now_mytz.weekday()),date_now_mytz.day)
			date_string = '%s-%s-%s' % (str(date_now_tsdb.year),str(date_now_tsdb.month),str(date_now_tsdb.day))
			menu.append((day_string,date_string))
			
		self.getControl(983).reset()	   
		for data_string,date in menu:
			menu_entry = xbmcgui.ListItem(data_string)
			menu_entry.setProperty('menu_entry', data_string)
			menu_entry.setProperty('entry_date', date)
			self.getControl(983).addItem(menu_entry)
		
		#use this to direct navigation to a given date! -TODO
		threading.Thread(name='watcher', target=self.watcher).start()
		if not self.date_string:
			self.setFocusId(983)
			self.getControl(983).selectItem(0)
			self.date_string = menu[0][1]
			self.fill_calendar(self.date_string)
		

	def fill_calendar(self,datestring):
		self.getControl(93).setVisible(False)
		items_to_add = []
		self.getControl(94).setPercent(0)
		self.getControl(92).setImage(os.path.join(addonpath,art,'busy.png'))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.getControl(987).reset()
		#next matches stuff
		event_next_list = thesportsdb.Schedules(tsdbkey).eventsday(datestring,None,None)["events"]
		j = 0
		if event_next_list:
			total_events = len(event_next_list)
			for event in event_next_list:
				event_sport = thesportsdb.Events().get_sport(event)
				event_id = thesportsdb.Events().get_eventid(event)
				
				#check if event belongs to blocked sport strSport
				
				if event_sport == 'Soccer' and settings.getSetting('enable-football') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Basketball' and settings.getSetting('enable-basketball') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Ice Hockey' and settings.getSetting('enable-icehockey') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Baseball' and settings.getSetting('enable-baseball') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Motorsport' and settings.getSetting('enable-motorsport') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Rugby' and settings.getSetting('enable-rugby') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'Golf' and settings.getSetting('enable-golf') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				elif event_sport == 'American Football' and settings.getSetting('enable-amfootball') == 'false' and settings.getSetting('calendar-disabledsports') == 'true': pass
				else:
					#get league id and check if the league is not ignored
					league_id = thesportsdb.Events().get_leagueid(event)
					if ((league_id + '.txt') in self.ignored_leagues and settings.getSetting('calendar-disabledleagues') == 'true') or ((league_id + '.txt') in self.rmleaguescalendar): pass
					else:
						event_fullname = thesportsdb.Events().get_eventtitle(event)
						event_race = thesportsdb.Events().get_racelocation(event)
						event_league = thesportsdb.Events().get_league(event)
						event_sport = thesportsdb.Events().get_sport(event)
						
						if event_sport == 'Soccer': sport_logo = os.path.join(addonpath,art,'loadingsports','soccer.png')
						elif event_sport == 'Basketball': sport_logo = os.path.join(addonpath,art,'loadingsports','basketball.png')
						elif event_sport == 'Ice Hockey': sport_logo = os.path.join(addonpath,art,'loadingsports','ice%20hockey.png')
						elif event_sport == 'Baseball': sport_logo = os.path.join(addonpath,art,'loadingsports','baseball.png')
						elif event_sport == 'Motorsport': sport_logo = os.path.join(addonpath,art,'loadingsports','motorsport.png')
						elif event_sport == 'Rugby': sport_logo = os.path.join(addonpath,art,'loadingsports','rugby.png')
						elif event_sport == 'Golf': sport_logo = os.path.join(addonpath,art,'loadingsports','golf.png')
						elif event_sport == 'American Football': sport_logo = os.path.join(addonpath,art,'loadingsports','american%20football.png')
						
						fmt = "%y-%m-%d"
						fmt_time = "%H:%M"
						event_datetime = thesportsdb.Events().get_datetime_object(event)
						if event_datetime:
							#datetime object conversion goes here
							db_time = pytz.timezone(str(pytz.timezone(tsdbtimezone))).localize(event_datetime)
							event_datetime=db_time.astimezone(my_location)
							event_strtime = thesportsdb.Events().get_time(event)
							if event_strtime and event_strtime != 'null' and event_strtime != 'None':
								event_time = event_datetime.strftime(fmt_time)
								if len(str(event_datetime.minute)) == 1: event_minute = str(event_datetime.minute) + '0'
								else: event_minute = str(event_datetime.minute)
								event_order = int(str(event_datetime.hour) + str(event_minute))
							else:
								event_time = 'N/A'
								event_order = 30000
						else:
							event_time = 'N/A'
							event_order = 30000
						
						
						if event_race:
							home_team_logo = os.path.join(addonpath,art,'raceflag.png')
							event_name = thesportsdb.Events().get_eventtitle(event)
							event_round = ''		
						else:
							home_team_id = thesportsdb.Events().get_hometeamid(event)
							home_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(home_team_id)["teams"][0]
							if settings.getSetting('team-naming')=='0': home_team_name = thesportsdb.Teams().get_name(home_team_dict)
							else: team_name = home_team_name = thesportsdb.Teams().get_alternativefirst(home_team_dict)
							home_team_logo = thesportsdb.Teams().get_badge(home_team_dict)
							stadium_fanart = thesportsdb.Teams().get_stadium_thumb(home_team_dict)
							away_team_id = thesportsdb.Events().get_awayteamid(event)
							away_team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(away_team_id)["teams"][0]
							if settings.getSetting('team-naming')=='0': away_team_name = thesportsdb.Teams().get_name(away_team_dict)
							else: away_team_name = thesportsdb.Teams().get_alternativefirst(away_team_dict)
							away_team_logo = thesportsdb.Teams().get_badge(away_team_dict)
							event_round = thesportsdb.Events().get_round(event)
							if event_round and event_round != '0':
								round_label = ' - Round ' + str(event_round)
								event_league = event_league + round_label
				
						game = xbmcgui.ListItem(event_fullname)
						game.setProperty('HomeTeamLogo',home_team_logo)
						game.setProperty('league',event_league)
						game.setProperty('sport_logo',sport_logo)
						game.setProperty('sport',event_sport)
						game.setProperty('event_time',event_time)
						game.setProperty('event_order',str(event_order))
						game.setProperty('event_id',event_id)
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
						try: game.setProperty('date',event_datetime.strftime(fmt))
						except: pass
						if event_race: 
							game.setProperty('EventName',event_name)
						try:
							date_now_mytz = pytz.timezone(str(pytz.timezone(str(my_location)))).localize(datetime.datetime.now())
							if event_datetime > date_now_mytz:
								hour_diff = (event_datetime-date_now_mytz).seconds/3600
							else: hour_diff = ((date_now_mytz-event_datetime).seconds/3600)*(-1)
							if settings.getsetting('calendar-disabledpassed') == 'true' and hour_diff > int(settings.getSetting('calendar-disabledpassed-delay')): pass
							else: items_to_add.append(game)
						
						except:items_to_add.append(game)
						
						#try to set progress bar here
						#for the events presented
						j+=1
						self.getControl(94).setPercent(int(float(j)/total_events*100))
					#for the events not presented
					j+=1
					self.getControl(94).setPercent(int(float(j)/total_events*100))
		
		
			#order the items here by start time
			time_array = []
			items_to_add_processed = []
			for item in items_to_add:
				time_array.append(int(item.getProperty('event_order')))
		
			for timestmp in sorted(time_array):
				for item in items_to_add:
					itemorder = int(item.getProperty('event_order'))
					if itemorder == timestmp:
						items_to_add_processed.append(item)
						items_to_add.remove(item)
					
	
			if items_to_add_processed: self.getControl(987).addItems(items_to_add_processed)
			else:
				self.getControl(93).setVisible(True)
				self.getControl(93).setLabel('No events available!')
		else:
			self.getControl(93).setVisible(True)
			self.getControl(93).setLabel('No events available!')
									
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

	def watcher(self,):
		while not xbmc.abortRequested:
			rmleaguescalendar = os.listdir(ignoreleaguecalendar)
			if self.rmleaguescalendar != rmleaguescalendar:
				self.rmleaguescalendar = rmleaguescalendar
				self.fill_calendar(self.date_string)
			xbmc.sleep(200)

		
	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.close()

		elif action.getId() == 117: #contextmenu
			if xbmc.getCondVisibility("Control.HasFocus(987)"): container = 987
			self.specific_id = self.getControl(container).getSelectedItem().getProperty('event_id')
			contextmenubuilder.start(['calendaritem',self.specific_id])	

			
	def onClick(self,controlId):
		if controlId == 983:
			listControl = self.getControl(controlId)
			selected_date=listControl.getSelectedItem().getProperty('entry_date')
			self.date_string = selected_date
			self.fill_calendar(selected_date)
					
		elif controlId == 980 or controlId == 984 or controlId == 985 or controlId == 981:
			self.team = self.getControl(controlId).getSelectedItem().getProperty('team_id')
			teamview.start([self.team,self.sport,'','plotview'])
		


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
	
		
