#!/usr/bin/python
# -*- coding: UTF-8 -*-

def get_month_short(month):
	if int(month) == 1: return "JAN"
	elif int(month) == 2: return "FEB"
	elif int(month) == 3: return "MAR"
	elif int(month) == 4: return "APR"
	elif int(month) == 5: return "MAY"
	elif int(month) == 6: return "JUN"
	elif int(month) == 7: return "JUL"
	elif int(month) == 8: return "AUG"
	elif int(month) == 9: return "SEP"
	elif int(month) == 10: return "OCT"
	elif int(month) == 11: return "NOV"
	elif int(month) == 12: return "DEC"
	else: return str(month)
	
def get_month_long(month):
	if int(month) == 1: return "January"
	elif int(month) == 2: return "February"
	elif int(month) == 3: return "March"
	elif int(month) == 4: return "April"
	elif int(month) == 5: return "May"
	elif int(month) == 6: return "June"
	elif int(month) == 7: return "July"
	elif int(month) == 8: return "August"
	elif int(month) == 9: return "September"
	elif int(month) == 10: return "October"
	elif int(month) == 11: return "November"
	elif int(month) == 12: return "December"
	else: return str(month)
	
def get_weekday(dayint):
	if dayint == 0: return "Monday"
	elif dayint == 1: return "Tuesday"
	elif dayint == 2: return "Wednesday"
	elif dayint == 3: return "Thursday"
	elif dayint == 4: return "Friday"
	elif dayint == 5: return "Saturday"
	elif dayint == 6: return "Sunday"
	
#returns the first part of settings defined for each sport	
def get_sport_setting(sport):
	sport = sport.lower()
	if sport == 'soccer' or sport == 'football': return 'football'
	elif sport == 'rugby': return 'rugby'
	elif sport == 'motorsport': return 'motorsport'
	elif sport == 'basketball': return 'basketball'
	elif sport == 'american%20football': return 'amfootball'
	elif sport == 'ice%20hockey': return 'icehockey'
	elif sport == 'baseball': return 'baseball'
	elif sport == 'golf': return 'golf'
	else: return None
	
def get_position_string(position):
	position = str(position)
	if position:
		if position[-1] == '1':
			if position == '11': return position +'th'
			else: return position +'st'
		elif position[-1] == '2': 
			if position == 12: return position + 'th'
			else: return position + 'nd'
		elif position[-1] == '3': 
			if position == '13': return position + 'th'
			else: return position+'rd'
		else: return position + 'th'
