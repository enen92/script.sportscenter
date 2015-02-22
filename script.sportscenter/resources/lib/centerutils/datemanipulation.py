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
