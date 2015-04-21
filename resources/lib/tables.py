import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re
import thesportsdb
from centerutils.common_variables import *

def start(data_list):
	window = dialog_stadium('DialogTables.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_stadium(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.league_id = str(args[3])
		self.league_id = '4328'

	def onInit(self):
		teams_list = thesportsdb.Lookups().lookup_all_teams(self.league_id)["teams"]
		table_list = thesportsdb.Lookups().lookup_leaguetables(self.league_id,None)["table"]
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
						team_badge = thesportsdb.Teams().get_badge(teamfull)
						teamitem = xbmcgui.ListItem(team_name,iconImage=team_badge)
						teamitem.setProperty('team_name',team_name)
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
						self.getControl(980).addItem(teamitem)
		

	
		
