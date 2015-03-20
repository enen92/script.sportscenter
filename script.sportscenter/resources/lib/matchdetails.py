# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import thesportsdb
import datetime
import re
from centerutils.common_variables import *
from centerutils.datemanipulation import *

			


def start(data_list):
	window = dialog_matchdetails('DialogMatchdetails.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_matchdetails(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.params = eval(args[3])

	def onInit(self):
		self.is_live = self.params[0]
		if self.is_live == False:
			self.event_id = self.params[1]
			self.event_details(self.event_id)
			
	def event_lineup(self,event_dict,home_away):
		xbmc.executebuiltin("ClearProperty(detail,Home)")
		xbmc.executebuiltin("ClearProperty(lineup,Home)")
		
		#reset all controls in range
		for i in xrange(32022,32203):
			try: self.getControl(i).setText('')
			except:
				try: self.getControl(i).setImage('')
				except: pass
			
		
		
		self.event_dict = event_dict
		#check wether we are trying to find the home or away team
		self.home_away = home_away
		if self.home_away == "home":
			self.jersey = self.hometeam_jersey
			self.badge = self.hometeam_badge
			self.team_name = self.hometeam_name
			self.formation = thesportsdb.Events().get_homeformation(self.event_dict)
			self.goalkeeper = thesportsdb.Events().get_homegoalkeeper(self.event_dict)
			self.defenders_raw = thesportsdb.Events().get_homedefense(self.event_dict)
			self.midfielders_raw = thesportsdb.Events().get_homemidfielders(self.event_dict)
			self.forwarders_raw = thesportsdb.Events().get_homeforward(self.event_dict)
			self.subs_raw = thesportsdb.Events().get_homesubs(self.event_dict)
			self.coach = thesportsdb.Teams().get_manager(self.hometeam_dict)
			#set button label to call away team lineup
			self.getControl(9027).setLabel('Away Team Lineup')
		
		elif self.home_away == "away":
			self.jersey = self.awayteam_jersey
			self.badge = self.awayteam_badge
			self.team_name = self.awayteam_name
			self.formation = thesportsdb.Events().get_awayformation(self.event_dict)
			self.goalkeeper = thesportsdb.Events().get_awaygoalkeeper(self.event_dict)
			self.defenders_raw = thesportsdb.Events().get_awaydefense(self.event_dict)
			self.midfielders_raw = thesportsdb.Events().get_awaymidfielders(self.event_dict)
			self.forwarders_raw = thesportsdb.Events().get_awayforward(self.event_dict)
			self.subs_raw = thesportsdb.Events().get_awaysubs(self.event_dict)
			self.coach = thesportsdb.Teams().get_manager(self.awayteam_dict)
			#set button label to call home team lineup
			self.getControl(9027).setLabel('Home Team Lineup')
		
			
		#set team info
		self.getControl(309).setText('[B]%s[/B]' % (self.formation))
		self.getControl(310).setText('[B]%s[/B]' % (self.team_name))
		self.getControl(306).setImage(self.badge)
		self.getControl(311).setText('[COLOR labelheader][B]Coach:[/B][/COLOR] %s' %(self.coach))
	
		#Prepare the data
		
		self.defenders = []
		self.midfielders = []
		self.forwarders = []
		self.subs = []
		
		for player in self.goalkeeper.split(';'):
			if player == '': pass
			else:
				if player.startswith(' '): player = player[1:]
				self.goalkeeper = player
		
		for player in self.defenders_raw.split(';'):
			if player == '': pass
			else:
				if player.startswith(' '): player = player[1:]
				self.defenders.append(player)
				
		for player in self.midfielders_raw.split(';'):
			if player == '': pass
			else:
				if player.startswith(' '): player = player[1:]
				self.midfielders.append(player)
				
		for player in self.forwarders_raw.split(';'):
			if player == '': pass
			else:
				if player.startswith(' '): player = player[1:]
				self.forwarders.append(player)
				
		for player in self.subs_raw.split(';'):
			if player == '': pass
			else:
				if player.startswith(' '): player = player[1:]
				self.subs.append(player)
				
		#set lineup and subs info
		lineup = self.goalkeeper + '[CR]'
		for player in self.defenders:
			lineup = lineup + player + '[CR]'
		for player in self.midfielders:
			lineup = lineup + player + '[CR]'
		for player in self.forwarders:
			lineup = lineup + player + '[CR]'
		
		subs = ''
		for player in self.subs:
			subs = subs + player + '[CR]'

		self.getControl(32150).setText(lineup)
		self.getControl(32151).setText(subs)
		
		#set goalkeeper
		self.getControl(32000).setImage(self.jersey)
		self.getControl(32001).setText(self.goalkeeper)
		
		#formation management 
		if self.formation == '4-4-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self.getControl(32047).setText(self.midfielders[0])
			self.getControl(32048).setImage(self.jersey)
			self.getControl(32049).setText(self.midfielders[1])
			self.getControl(32050).setImage(self.jersey)
			self.getControl(32051).setText(self.midfielders[2])
			self.getControl(32052).setImage(self.jersey)
			self.getControl(32053).setText(self.midfielders[3])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
		
		elif self.formation == '4-3-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[3])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[1])
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self.getControl(32055).setText(self.midfielders[0])
			self.getControl(32056).setImage(self.jersey)
			self.getControl(32057).setText(self.midfielders[1])
			self.getControl(32058).setImage(self.jersey)
			self.getControl(32059).setText(self.midfielders[2])
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self.getControl(32067).setText(self.forwarders[2])
			self.getControl(32068).setImage(self.jersey)
			self.getControl(32069).setText(self.forwarders[1])
			self.getControl(32070).setImage(self.jersey)
			self.getControl(32071).setText(self.forwarders[0])
			
		elif self.formation == '4-2-3-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32082).setImage(self.jersey)
			self.getControl(32083).setText(self.midfielders[0])
			self.getControl(32084).setImage(self.jersey)
			self.getControl(32085).setText(self.midfielders[1])
			self.getControl(32086).setImage(self.jersey)
			self.getControl(32087).setText(self.midfielders[2])
			self.getControl(32088).setImage(self.jersey)
			self.getControl(32089).setText(self.midfielders[3])
			self.getControl(32090).setImage(self.jersey)
			self.getControl(32091).setText(self.midfielders[4])			
			#forwarders
			self.getControl(32060).setImage(self.jersey)
			self.getControl(32061).setText(self.forwarders[0])
			
		elif self.formation == '4-1-2-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32092).setImage(self.jersey)
			self.getControl(32093).setText(self.midfielders[0])
			self.getControl(32094).setImage(self.jersey)
			self.getControl(32095).setText(self.midfielders[1])
			self.getControl(32096).setImage(self.jersey)
			self.getControl(32097).setText(self.midfielders[2])
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self.getControl(32067).setText(self.forwarders[0])
			self.getControl(32068).setImage(self.jersey)
			self.getControl(32069).setText(self.forwarders[1])
			self.getControl(32070).setImage(self.jersey)
			self.getControl(32071).setText(self.forwarders[2])
			
		elif self.formation == '4-1-4-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32098).setImage(self.jersey)
			self.getControl(32099).setText(self.midfielders[0])
			self.getControl(32100).setImage(self.jersey)
			self.getControl(32101).setText(self.midfielders[1])
			self.getControl(32102).setImage(self.jersey)
			self.getControl(32103).setText(self.midfielders[2])
			self.getControl(32104).setImage(self.jersey)
			self.getControl(32105).setText(self.midfielders[3])
			self.getControl(32106).setImage(self.jersey)
			self.getControl(32107).setText(self.midfielders[4])
			#forwarders
			self.getControl(32060).setImage(self.jersey)
			self.getControl(32061).setText(self.forwarders[0])
			
		elif self.formation == '4-4-1-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self.getControl(32047).setText(self.midfielders[0])
			self.getControl(32048).setImage(self.jersey)
			self.getControl(32049).setText(self.midfielders[1])
			self.getControl(32050).setImage(self.jersey)
			self.getControl(32051).setText(self.midfielders[2])
			self.getControl(32052).setImage(self.jersey)
			self.getControl(32053).setText(self.midfielders[3])
			self.getControl(32108).setImage(self.jersey)
			self.getControl(32109).setText(self.midfielders[4])
			#forwarders
			self.getControl(32110).setImage(self.jersey)
			self.getControl(32111).setText(self.forwarders[0])
			
		elif self.formation == '5-3-2':
			#defense
			self.getControl(32002).setImage(self.jersey)
			self.getControl(32003).setText(self.defenders[0])
			self.getControl(32004).setImage(self.jersey)
			self.getControl(32005).setText(self.defenders[1])
			self.getControl(32006).setImage(self.jersey)
			self.getControl(32007).setText(self.defenders[2])
			self.getControl(32008).setImage(self.jersey)
			self.getControl(32009).setText(self.defenders[3])
			self.getControl(32010).setImage(self.jersey)
			self.getControl(32011).setText(self.defenders[4])
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self.getControl(32055).setText(self.midfielders[0])
			self.getControl(32056).setImage(self.jersey)
			self.getControl(32057).setText(self.midfielders[1])
			self.getControl(32058).setImage(self.jersey)
			self.getControl(32059).setText(self.midfielders[2])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
			
		elif self.formation == '3-5-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielders
			self.getControl(32036).setImage(self.jersey)
			self.getControl(32037).setText(self.midfielders[0])
			self.getControl(32038).setImage(self.jersey)
			self.getControl(32039).setText(self.midfielders[1])
			self.getControl(32040).setImage(self.jersey)
			self.getControl(32041).setText(self.midfielders[2])
			self.getControl(32042).setImage(self.jersey)
			self.getControl(32043).setText(self.midfielders[3])
			self.getControl(32044).setImage(self.jersey)
			self.getControl(32045).setText(self.midfielders[4])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
			
		elif self.formation == '3-4-2-1':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self.getControl(32047).setText(self.midfielders[0])
			self.getControl(32048).setImage(self.jersey)
			self.getControl(32049).setText(self.midfielders[1])
			self.getControl(32050).setImage(self.jersey)
			self.getControl(32051).setText(self.midfielders[2])
			self.getControl(32052).setImage(self.jersey)
			self.getControl(32053).setText(self.midfielders[3])
			self.getControl(32112).setImage(self.jersey)
			self.getControl(32113).setText(self.midfielders[4])
			self.getControl(32114).setImage(self.jersey)
			self.getControl(32115).setText(self.midfielders[5])
			#forwarders
			self.getControl(32116).setImage(self.jersey)
			self.getControl(32117).setText(self.forwarders[0])
		
		elif self.formation == '3-4-1-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self.getControl(32047).setText(self.midfielders[0])
			self.getControl(32048).setImage(self.jersey)
			self.getControl(32049).setText(self.midfielders[1])
			self.getControl(32050).setImage(self.jersey)
			self.getControl(32051).setText(self.midfielders[2])
			self.getControl(32052).setImage(self.jersey)
			self.getControl(32053).setText(self.midfielders[3])
			self.getControl(32118).setImage(self.jersey)
			self.getControl(32119).setText(self.midfielders[0])
			#forwarders
			self.getControl(32120).setImage(self.jersey)
			self.getControl(32121).setText(self.forwarders[0])
			self.getControl(32122).setImage(self.jersey)
			self.getControl(32123).setText(self.forwarders[1])
			
		elif self.formation == '3-5-1-1':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielder
			self.getControl(32036).setImage(self.jersey)
			self.getControl(32037).setText(self.midfielders[0])
			self.getControl(32038).setImage(self.jersey)
			self.getControl(32039).setText(self.midfielders[1])
			self.getControl(32040).setImage(self.jersey)
			self.getControl(32041).setText(self.midfielders[2])
			self.getControl(32042).setImage(self.jersey)
			self.getControl(32043).setText(self.midfielders[3])
			self.getControl(32044).setImage(self.jersey)
			self.getControl(32045).setText(self.midfielders[4])
			#forwarders
			self.getControl(32108).setImage(self.jersey)
			self.getControl(32109).setText(self.forwarders[0])
			self.getControl(32110).setImage(self.jersey)
			self.getControl(32111).setText(self.forwarders[1])
			
		elif self.formation == '4-3-2-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self.getControl(32055).setText(self.midfielders[0])
			self.getControl(32056).setImage(self.jersey)
			self.getControl(32057).setText(self.midfielders[1])
			self.getControl(32058).setImage(self.jersey)
			self.getControl(32059).setText(self.midfielders[2])
			#forwarders
			self.getControl(32112).setImage(self.jersey)
			self.getControl(32113).setText(self.midfielders[3])
			self.getControl(32114).setImage(self.jersey)
			self.getControl(32115).setText(self.midfielders[4])
			self.getControl(32116).setImage(self.jersey)
			self.getControl(32117).setText(self.forwarders[0])
			
		elif self.formation == '4-5-1':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielder
			self.getControl(32036).setImage(self.jersey)
			self.getControl(32037).setText(self.midfielders[0])
			self.getControl(32038).setImage(self.jersey)
			self.getControl(32039).setText(self.midfielders[1])
			self.getControl(32040).setImage(self.jersey)
			self.getControl(32041).setText(self.midfielders[2])
			self.getControl(32042).setImage(self.jersey)
			self.getControl(32043).setText(self.midfielders[3])
			self.getControl(32044).setImage(self.jersey)
			self.getControl(32045).setText(self.midfielders[4])
			#forwarders
			self.getControl(32124).setImage(self.jersey)
			self.getControl(32125).setText(self.forwarders[0])
			
		elif self.formation == '3-4-3':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielders
			self.getControl(32046).setImage(self.jersey)
			self.getControl(32047).setText(self.midfielders[0])
			self.getControl(32048).setImage(self.jersey)
			self.getControl(32049).setText(self.midfielders[1])
			self.getControl(32050).setImage(self.jersey)
			self.getControl(32051).setText(self.midfielders[2])
			self.getControl(32052).setImage(self.jersey)
			self.getControl(32053).setText(self.midfielders[3])
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self.getControl(32067).setText(self.forwarders[0])
			self.getControl(32068).setImage(self.jersey)
			self.getControl(32069).setText(self.forwarders[1])
			self.getControl(32070).setImage(self.jersey)
			self.getControl(32071).setText(self.forwarders[2])
			
		elif self.formation == '4-3-1-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32054).setImage(self.jersey)
			self.getControl(32055).setText(self.midfielders[0])
			self.getControl(32056).setImage(self.jersey)
			self.getControl(32057).setText(self.midfielders[1])
			self.getControl(32058).setImage(self.jersey)
			self.getControl(32059).setText(self.midfielders[2])
			self.getControl(32118).setImage(self.jersey)
			self.getControl(32119).setText(self.midfielders[3])
			#forwarders
			self.getControl(32120).setImage(self.jersey)
			self.getControl(32121).setText(self.forwarders[0])
			self.getControl(32122).setImage(self.jersey)
			self.getControl(32123).setText(self.forwarders[1])
			
		elif self.formation == '4-2-1-3':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32126).setImage(self.jersey)
			self.getControl(32127).setText(self.midfielders[0])
			self.getControl(32128).setImage(self.jersey)
			self.getControl(32129).setText(self.midfielders[1])
			self.getControl(32130).setImage(self.jersey)
			self.getControl(32131).setText(self.midfielders[2])
			#forwarders
			self.getControl(32066).setImage(self.jersey)
			self.getControl(32067).setText(self.forwarders[0])
			self.getControl(32068).setImage(self.jersey)
			self.getControl(32069).setText(self.forwarders[1])
			self.getControl(32070).setImage(self.jersey)
			self.getControl(32071).setText(self.forwarders[2])
			
		elif self.formation == '4-1-3-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32132).setImage(self.jersey)
			self.getControl(32133).setText(self.midfielders[0])
			self.getControl(32134).setImage(self.jersey)
			self.getControl(32135).setText(self.midfielders[1])
			self.getControl(32136).setImage(self.jersey)
			self.getControl(32137).setText(self.midfielders[2])
			self.getControl(32138).setImage(self.jersey)
			self.getControl(32139).setText(self.midfielders[3])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
			
		elif self.formation == '4-1-2-1-2':
			#defense
			self.getControl(32022).setImage(self.jersey)
			self.getControl(32023).setText(self.defenders[0])
			self.getControl(32024).setImage(self.jersey)
			self.getControl(32025).setText(self.defenders[1])
			self.getControl(32026).setImage(self.jersey)
			self.getControl(32027).setText(self.defenders[2])
			self.getControl(32028).setImage(self.jersey)
			self.getControl(32029).setText(self.defenders[3])
			#midfielders
			self.getControl(32132).setImage(self.jersey)
			self.getControl(32133).setText(self.midfielders[0])
			self.getControl(32142).setImage(self.jersey)
			self.getControl(32143).setText(self.midfielders[1])
			self.getControl(32144).setImage(self.jersey)
			self.getControl(32145).setText(self.midfielders[2])
			self.getControl(32140).setImage(self.jersey)
			self.getControl(32141).setText(self.midfielders[3])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
			
		elif self.formation == '3-1-3-1-2':
			#defense
			self.getControl(32030).setImage(self.jersey)
			self.getControl(32031).setText(self.defenders[0])
			self.getControl(32032).setImage(self.jersey)
			self.getControl(32033).setText(self.defenders[1])
			self.getControl(32034).setImage(self.jersey)
			self.getControl(32035).setText(self.defenders[2])
			#midfielders
			self.getControl(32202).setImage(self.jersey)
			self.getControl(32203).setText(self.defenders[3])
			self.getControl(32140).setImage(self.jersey)
			self.getControl(32141).setText(self.midfielders[3])
			self.getControl(32146).setImage(self.jersey)
			self.getControl(32147).setText(self.midfielders[0])
			self.getControl(32148).setImage(self.jersey)
			self.getControl(32149).setText(self.midfielders[1])
			self.getControl(32200).setImage(self.jersey)
			self.getControl(32201).setText(self.midfielders[2])
			#forwarders
			self.getControl(32062).setImage(self.jersey)
			self.getControl(32063).setText(self.forwarders[0])
			self.getControl(32064).setImage(self.jersey)
			self.getControl(32065).setText(self.forwarders[1])
			
		xbmc.executebuiltin("SetProperty(lineup,1,home)")
		xbmc.sleep(200)
		self.setFocusId(9027)
		
					
	def event_details(self,event_id):
		xbmc.executebuiltin("ClearProperty(lineup,Home)")
		xbmc.executebuiltin("ClearProperty(detail,Home)")
		self.event_dict = thesportsdb.Lookups().lookupevent(event_id)["events"]
		if self.event_dict and self.event_dict != 'None':
			self.event_dict = self.event_dict[0]
			self.hometeam_id = thesportsdb.Events().get_hometeamid(self.event_dict)
			self.hometeam_dict = thesportsdb.Lookups().lookupteam(self.hometeam_id)["teams"][0]
			self.awayteam_id = thesportsdb.Events().get_awayteamid(self.event_dict)
			self.awayteam_dict = thesportsdb.Lookups().lookupteam(self.awayteam_id)["teams"][0]
			
			#Get both teams badge and jersey
			self.hometeam_badge = thesportsdb.Teams().get_badge(self.hometeam_dict)
			self.awayteam_badge = thesportsdb.Teams().get_badge(self.awayteam_dict)
			self.hometeam_jersey = thesportsdb.Teams().get_team_jersey(self.hometeam_dict)
			self.awayteam_jersey = thesportsdb.Teams().get_team_jersey(self.awayteam_dict)
			
			#Set badge and jersey (if it exists)
			if self.hometeam_jersey and self.hometeam_jersey != 'None':
				self.getControl(777).setImage(self.hometeam_badge)
				self.getControl(779).setImage(self.hometeam_jersey)
			else:
				self.getControl(778).setImage(self.hometeam_badge)
				
			if self.awayteam_jersey and self.awayteam_jersey != 'None':
				self.getControl(780).setImage(self.awayteam_badge)
				self.getControl(782).setImage(self.awayteam_jersey)
			else:
				self.getControl(781).setImage(self.awayteam_badge)
				
			#Set team name
			if settings.getSetting('team-naming')=='0': self.hometeam_name = thesportsdb.Teams().get_name(self.hometeam_dict)
			else: self.hometeam_name = thesportsdb.Teams().get_alternativefirst(self.hometeam_dict)
			if settings.getSetting('team-naming')=='0': self.awayteam_name = thesportsdb.Teams().get_name(self.awayteam_dict)
			else: self.awayteam_name = thesportsdb.Teams().get_alternativefirst(self.awayteam_dict)
			self.getControl(784).setText('[B]%s[/B]' % (self.hometeam_name))
			self.getControl(785).setText('[B]%s[/B]' % (self.awayteam_name))
			
			#event stadium and spectactors
			self.stadium = thesportsdb.Teams().get_stadium(self.hometeam_dict)
			self.getControl(792).setLabel('[B]%s[/B]' % (self.stadium))
			self.spectators = thesportsdb.Events().get_spectators(self.event_dict)
			if self.spectators != '0':
				try:
					i = 0
					spectators = ''
					lenght = len(self.spectators)
					for letter in reversed(self.spectators):
						i += 1
						if (float(i)/3).is_integer():	
							if lenght != i: spectators = ',' + letter + spectators
							else: spectators = letter + spectators
						else: spectators = letter + spectators
					self.getControl(793).setLabel('[B]Spectators[/B]: %s' % (spectators))
				except:
					self.getControl(793).setLabel('[B]Spectators[/B]: %s' % (self.spectators))
			
			#set match as finished as it is not live
			self.getControl(789).setLabel("[B]90'[/B]")
			self.getControl(790).setPercent(100)
			self.getControl(791).setImage(os.path.join(addonpath,art,'notlive.png'))
			
			#set date
			self.date = thesportsdb.Events().get_date(self.event_dict)
			try:
				if self.date and self.date != 'None':
					date_vector = self.date.split('/')
					if len(date_vector) == 3:
						day = date_vector[0]
						if len(date_vector[2]) == 2:
							year = '20'+date_vector[2]
						month = get_month_long(date_vector[1])
						self.getControl(788).setLabel('[B]%s %s %s[/B]' % (day,month,year))
			except: self.getControl(788).setLabel('[B]%s[/B]' % (self.date))
			
			#set event competition and round(if available)
			self.competition = thesportsdb.Events().get_league(self.event_dict)
			self.round = thesportsdb.Events().get_round(self.event_dict)
			if self.round and self.round != 'None': self.title = '[B]' + self.competition + ' - Round ' + str(self.round) + '[/B]'
			else: self.title = '[B]'+self.competition+'[/B]'
			self.getControl(787).setLabel(self.title)
			
			#set result
			self.home_scored = thesportsdb.Events().get_homescore(self.event_dict)
			self.away_scored = thesportsdb.Events().get_awayscore(self.event_dict)
			self.result = '[B]%s-%s[/B]' % (str(self.home_scored),str(self.away_scored))
			self.getControl(783).setLabel(self.result)
			
			#check number of shots
			self.home_shots = thesportsdb.Events().get_homeshots(self.event_dict)
			self.away_shots = thesportsdb.Events().get_awayshots(self.event_dict)
			if (self.home_shots and self.home_shots != 'None') and (self.away_shots and self.away_shots != 'None'):
				self.getControl(794).setLabel('[B]Shots[/B]')
				self.getControl(795).setLabel('[B]%s[/B]' %(str(self.home_shots)))
				self.getControl(796).setLabel('[B]%s[/B]' %(str(self.away_shots)))
			
			#fill home team match details
			self.home_details = {}
			
			self.home_goaldetails = thesportsdb.Events().get_homegoaldetails(self.event_dict).split(';')
			for goal in self.home_goaldetails:
				homegoaldetails = re.compile("(\d+).+?\:(.*)").findall(goal)
				if homegoaldetails:
					for minute,player in homegoaldetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'goal.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'goal.png'),player)]
							
			self.home_yellowcards = thesportsdb.Events().get_homeyellowcards(self.event_dict).split(';')
			for yellow in self.home_yellowcards:
				homeyellowdetails = re.compile("(\d+).+?\:(.*)").findall(yellow)
				if homeyellowdetails:
					for minute,player in homeyellowdetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'yellowcard2.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'yellowcard2.png'),player)]
							
			self.home_redcards = thesportsdb.Events().get_homeredcards(self.event_dict).split(';')
			for red in self.home_redcards:
				homereddetails = re.compile("(\d+).+?\:(.*)").findall(red)
				if homereddetails:
					for minute,player in homereddetails:
						if int(minute) in self.home_details.keys():
							if player != '&nbsp':
								self.home_details[int(minute)].append((os.path.join(addonpath,art,'redcard2.png'),player))
						else:
							if player != '&nbsp':
								self.home_details[int(minute)] = [(os.path.join(addonpath,art,'redcard2.png'),player)]
			
			self.home_details_listitems = []			
			for key in reversed(sorted(self.home_details.keys())):
				for detail in self.home_details[key]:
					detail_img = detail[0]
					detail_player = detail[1]
					
					detail_item = xbmcgui.ListItem(str(key))
					detail_item.setProperty('minute',"[B]%s': [/B]" % (str(key)))
					detail_item.setProperty('detail_img',detail_img)
					detail_item.setProperty('player',detail_player)
					self.home_details_listitems.append(detail_item)
					
			self.getControl(987).addItems(self.home_details_listitems)
			
			#fill away team match details
			self.away_details = {}
			
			self.away_goaldetails = thesportsdb.Events().get_awaygoaldetails(self.event_dict).split(';')
			for goal in self.away_goaldetails:
				awaygoaldetails = re.compile("(\d+).+?\:(.*)").findall(goal)
				if awaygoaldetails:
					for minute,player in awaygoaldetails:
						if int(minute) in self.away_details.keys():
							self.away_details[int(minute)].append((os.path.join(addonpath,art,'goal.png'),player))
						else:
							self.away_details[int(minute)] = [(os.path.join(addonpath,art,'goal.png'),player)]
							
			self.away_yellowcards = thesportsdb.Events().get_awayyellowcards(self.event_dict).split(';')
			for yellow in self.away_yellowcards:
				awayyellowdetails = re.compile("(\d+).+?\:(.*)").findall(yellow)
				if awayyellowdetails:
					for minute,player in awayyellowdetails:
						if int(minute) in self.away_details.keys():
							if player != '&nbsp':
								self.away_details[int(minute)].append((os.path.join(addonpath,art,'yellowcard2.png'),player))
						else:
							if player != '&nbsp':
								self.away_details[int(minute)] = [(os.path.join(addonpath,art,'yellowcard2.png'),player)]
							
			self.away_redcards = thesportsdb.Events().get_awayredcards(self.event_dict).split(';')
			for red in self.away_redcards:
				awayreddetails = re.compile("(\d+).+?\:(.*)").findall(red)
				if awayreddetails:
					for minute,player in awayreddetails:
						if int(minute) in self.away_details.keys():
							if player != '&nbsp':
								self.away_details[int(minute)].append((os.path.join(addonpath,art,'redcard2.png'),player))
						else:
							if player != '&nbsp':
								self.away_details[int(minute)] = [(os.path.join(addonpath,art,'redcard2.png'),player)]
			
			self.away_details_listitems = []			
			for key in reversed(sorted(self.away_details.keys())):
				for detail in self.away_details[key]:
					detail_img = detail[0]
					detail_player = detail[1]
					
					detail_item = xbmcgui.ListItem(str(key))
					detail_item.setProperty('minute',"[B]%s': [/B]" % (str(key)))
					detail_item.setProperty('detail_img',detail_img)
					detail_item.setProperty('player',detail_player)
					self.away_details_listitems.append(detail_item)
					
			self.getControl(988).addItems(self.away_details_listitems)
			xbmc.executebuiltin("SetProperty(detail,1,home)")
			xbmc.sleep(200)
			self.setFocusId(9022)
					

	def onClick(self,controlId):

		if controlId == 9022:
			self.event_lineup(self.event_dict,"home")
			
		elif controlId == 9023:
			self.event_lineup(self.event_dict,"away")
			
		elif controlId == 9024:
			#stadium
			import stadium as stadium
			stadium_hometeam = thesportsdb.Teams().get_stadium(self.hometeam_dict)
			if stadium_hometeam == self.stadium:
				stadium.start(self.hometeam_dict)
			
			
		elif controlId == 9027:
			if self.home_away == 'home':
				self.event_lineup(self.event_dict,"away")
			elif self.home_away == 'away':
				self.event_lineup(self.event_dict,"home")
			
		elif controlId == 9028:
			self.event_details(self.event_id)
			
	
		
