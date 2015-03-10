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
