# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

import re
import difflib
import thesportsdb

class Scrapper:
	def __init__(self,):
		pass


	def scrape_league(self,folder,sport):
		#check if [tsdbid:xxx] is defined first
		pass
		
	def scrape_season(self,folder,sport,league):
		pass
		
	def scrape_event(self,folder,sport,league,season):
		pass




class Parser:
	def __init__(self,):
		pass
		
	def from_string_get_home_and_away_teams(self,string,mode):
		home_away = []
		if mode == 'full' or mode == 'short':
			match = re.compile('(.+?) x (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? x .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) vs. (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? vs. .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) vs (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? vs .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			
			match = re.compile('(.+?) v (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? v .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
					
			match = re.compile('(.+?) at (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? at .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
					
			match = re.compile('(.+?) - (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? - .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
					
			match = re.compile('(.+?)-(.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+?-.+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
		
		if mode == 'full':
			match = re.compile('(.+?) face (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? face .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) take (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? take .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) play (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
			match = re.compile('(.+?) .+? play .+? (.+?) ').findall(string.lower())
			if match:
				for home,away in match:
					home_away.append((home.lower(),away.lower()))
		return home_away
