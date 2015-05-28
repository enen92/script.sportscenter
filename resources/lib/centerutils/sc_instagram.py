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

import json
import urllib2

def get_recent_instagram_images(username):
	url = 'https://api.instagram.com/v1/users/search?q='+username+'&client_id=12838ddc295141b0b8243593c9ce3317'
	print url
	user_id = json.load(urllib2.urlopen(url))['data'][0]['id']
	url = 'https://api.instagram.com/v1/users/'+user_id+'/media/recent/?client_id=12838ddc295141b0b8243593c9ce3317'
	data_list = json.load(urllib2.urlopen(url))["data"]
	image_array = []
	for data in data_list:
 	   img_id = data["id"]
 	   url = 'https://api.instagram.com/v1/media/'+img_id+'?client_id=12838ddc295141b0b8243593c9ce3317'
 	   img_data = json.load(urllib2.urlopen(url))["data"]
 	   lowres = img_data["images"]["low_resolution"]["url"]
	   stdres = img_data["images"]["standard_resolution"]["url"]
	   try:caption = img_data["caption"]["text"]
	   except: caption = ''
	   print stdres
 	   image_array.append((caption,lowres,stdres))

	return image_array

