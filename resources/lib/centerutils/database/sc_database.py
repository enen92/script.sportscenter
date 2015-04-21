import thesportsdb
import sqlite3 as lite
import os

#command line use only!
sc_database = 'sc_database.db'
templatefolder =  os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')

class Creator:
	#variables
	def __init__(self,):
		self.team_template = os.path.join(templatefolder,'team.txt')
		self.league_template = os.path.join(templatefolder,'league.txt')
		self.event_template = os.path.join(templatefolder,'event.txt')
		return

	#all
	def create_table_all(self,):
		self.create_table_league()
		self.create_table_team()
		self.create_table_event()
		return
	
	def drop_and_create_table_all(self,):
		self.drop_and_create_table_league()
		self.drop_and_create_table_team()
		self.drop_and_create_table_event()
		return
	
	#league
	def create_table_league(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.league_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE League("+query_string+")")
		if con:
			print "SportsCenter: Table League created successfully!"
			con.close()
		return
	
	def drop_table_league(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS League")
		if con:
			print "SportsCenter: Table League dropped successfully!"
			con.close()
		return
		
		
	def drop_and_create_table_league(self,):
		self.drop_table_league()
		self.create_table_league()
		return
		
	#team
	def create_table_team(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.team_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE Team("+query_string+")")
		if con:
			print "SportsCenter: Table Team created successfully!"
			con.close()
		return
	
	def drop_table_team(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Team")
		if con:
			print "SportsCenter: Table Team dropped successfully!"
			con.close()
		return
		
	def drop_and_create_table_team(self,):
		self.drop_table_team()
		self.create_table_team()
		return
		
	#event
	def create_table_event(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.event_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE Event("+query_string+")")
		if con:
			print "SportsCenter: Table Event created successfully!"
			con.close()
		return
		
	def drop_table_event(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Event")
		if con:
			print "SportsCenter: Table Event dropped successfully!"
			con.close()
		return
		
	def drop_and_create_table_event(self,):
		self.drop_table_event()
		self.create_table_event()
		return
		
class Checker:
	def check_if_table_exists(self,table):
		con = lite.connect(sc_database)
		cur = con.cursor()		
		try:
			cur.execute("SELECT * FROM "+table)
			con.close()
			return True
		except: 
			con.close()
			return False

		
	def create_table_if_not_exists(self,table):
		if table == 'League': pass
		elif table == 'Team': pass
		elif table == 'Event': pass
		else: return
		check = self.check_if_table_exists(table)
		if not check:
			if table == 'League': Creator().create_table_league()
			elif table == 'Team': Creator().create_table_team()
			elif table == 'Event': Creator().create_table_event()
		return


class Inserter:
	def __init__(self,):
		pass
		
	def global_inserter(self,table,dictionary):
		pass
		
	def insert_team(self,_team_id_or_dict_):
		if _team_id_or_dict_ == str:
			team_dictionary = thesportsdb.Lookups().lookupteam(_team_id_or_dict_)["teams"][0]
		elif _team_id_or_dict_ == dict: team_dictionary = _team_id_or_dict_
		else: team_dictionary = None
		if team_dictionary:
			#here we check if the table exists
			pass
		
		
	def insert_league(self,_league_id_or_dict_):
		pass
		
	def insert_event(self,_event_id_or_dict_):
		pass	
		
class Remover:
	def __init__(self,):
		pass
		
	def global_remover(self,table,dict):
		pass
		
	def remove_team(self,_team_id_or_dict_):
		pass
		
	def remove_league(self,_league_id_or_dict_):
		pass
		
	def remove_event(self,_event_id_or_dict_):
		pass	
	
		
	
