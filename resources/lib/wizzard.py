#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc,xbmcgui,xbmcaddon,xbmcplugin,xbmcvfs,os,threading,urllib
import thesportsdb
from centerutils.common_variables import *
from centerutils.iofile import *
from centerutils.downloadtools import *
from centerutils import keymaper

class wizzard:
	def __init__(self):
		print("Starting Wizzard")
		
		if not os.path.exists(favlogos): xbmcvfs.mkdir(favlogos)
		#
		if settings.getSetting('wizzard_check') == 'true':
			#delete previous data
			ficheiros = os.listdir(profilepath)
			for ficheiro in ficheiros:
				if ficheiro.endswith('.txt'): xbmcvfs.delete(os.path.join(profilepath,ficheiro))
		
			dialog = xbmcgui.Dialog()
			yes_no = dialog.yesno('Sports Center Wizzard', 'Do you have an account in thesportsdb.com?')
			if yes_no:
				nick = dialog.input('Please enter your nickname', type=xbmcgui.INPUT_ALPHANUM)
				xbmc.executebuiltin( "ActivateWindow(busydialog)" )
				settings.setSetting('username',nick)
				favourite_teams = thesportsdb.User(tsdbkey).get_favourite_teams(nick)
				football_favs = []
				basketball_favs = []
				baseball_favs = []
				motorsport_favs = []
				golf_favs = []
				icehockey_favs = []
				amfootball_favs = []
				rugby_favs = []
				motorsport_favs = []
				sport_favs = []
				if favourite_teams:
					for equipa in favourite_teams:
						team_dict = thesportsdb.Lookups(tsdbkey).lookupteam(equipa)['teams'][0]
						team_sport = thesportsdb.Teams().get_sport(team_dict)
						if settings.getSetting('team-naming')=='0': team_name = thesportsdb.Teams().get_name(team_dict)
						else: team_name = thesportsdb.Teams().get_alternativefirst(team_dict)
						team_badge = thesportsdb.Teams().get_badge(team_dict)
						team_fan_fanart = thesportsdb.Teams().get_fanart_fans(team_dict)
						team_logo_fanart = thesportsdb.Teams().get_fanart_general1(team_dict)
						if team_sport.lower() == 'soccer':
							football_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'rugby':
							rugby_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'motorsport':
							motorsport_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'basketball':
							basketball_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'american football':
							amfootball_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'ice hockey':
							icehockey_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'baseball':
							baseball_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
						elif team_sport.lower() == 'golf':
							golf_favs.append((equipa,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart))
							

					#decide heart team for each sport
					
					#football
					if football_favs:
							save(football_file,str(football_favs))
							sport_favs.append('Football')
					if len(football_favs) > 1 and settings.getSetting('enable-football') == 'true':
						foot_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in football_favs:
							foot_names.append(team_name)
						ret = dialog.select("Football favourite?", foot_names)
						save(football_fav_file,str(football_favs[ret]))
						if football_favs[ret][2]:
							try:
								t1 = threading.Thread(name='logodown1', target=Downloader , args=(football_favs[ret][2],os.path.join(favlogos,football_favs[ret][2].split('/')[-1]),))
								t1.start()
							except: pass
							try:
								t1fan = threading.Thread(name='logodownfan1', target=Downloader , args=(football_favs[ret][4],os.path.join(favlogos,football_favs[ret][4].split('/')[-1]),))
								t1fan.start()
							except: pass
							try:
								t1logo = threading.Thread(name='logodownlogo1', target=Downloader , args=(football_favs[ret][5],os.path.join(favlogos,football_favs[ret][5].split('/')[-1]),))
								t1logo.start()
							except: pass
					elif len(football_favs) == 1 and settings.getSetting('enable-football') == 'true':
						save(football_fav_file,str(football_favs[0]))
						try:
							t1 = threading.Thread(name='logodown1', target=Downloader , args=(football_favs[0][2],os.path.join(self.favlogos,football_favs[0][2].split('/')[-1]),))
							t1.start()
						except: pass
						try:
							t1fan = threading.Thread(name='logodownfan1', target=Downloader , args=(football_favs[0][4],os.path.join(favlogos,football_favs[0][4].split('/')[-1]),))
							t1fan.start()
						except: pass
						try:
							t1logo = threading.Thread(name='logodownlogo1', target=Downloader , args=(football_favs[0][5],os.path.join(favlogos,football_favs[0][5].split('/')[-1]),))
							t1logo.start()
						except: pass
					else: pass
					#rugby
					if rugby_favs:
							save(rugby_file,str(rugby_favs))
							sport_favs.append('Rugby')
					if len(rugby_favs) > 1 and settings.getSetting('enable-rugby') == 'true':
						rugby_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in rugby_favs:
							rugby_names.append(team_name)
						ret = dialog.select("Rugby favourite?", rugby_names)
						save(rugby_fav_file,str(rugby_favs[ret]))
						try:
							t2 = threading.Thread(name='logodown2', target=Downloader , args=(rugby_favs[ret][2],os.path.join(favlogos,rugby_favs[ret][2].split('/')[-1]),))
							t2.start()
						except: pass
						try:
							t2fan = threading.Thread(name='logodownfan2', target=Downloader , args=(rugby_favs[ret][4],os.path.join(favlogos,rugby_favs[ret][4].split('/')[-1]),))
							t2fan.start()
						except: pass
						try:
							t2logo = threading.Thread(name='logodownlogo2', target=Downloader , args=(rugby_favs[ret][5],os.path.join(favlogos,rugby_favs[ret][5].split('/')[-1]),))
							t2logo.start()
						except: pass
					elif len(rugby_favs) == 1 and settings.getSetting('enable-rugby') == 'true':
						save(rugby_fav_file,str(rugby_favs[0]))
						try:
							t2 = threading.Thread(name='logodown2', target=Downloader , args=(rugby_favs[0][2],os.path.join(favlogos,rugby_favs[0][2].split('/')[-1]),))
							t2.start()
						except: pass
						try:
							t2fan = threading.Thread(name='logodownfan2', target=Downloader , args=(rugby_favs[0][4],os.path.join(favlogos,rugby_favs[0][4].split('/')[-1]),))
							t2fan.start()
						except: pass
						try:
							t2logo = threading.Thread(name='logodownlogo2', target=Downloader , args=(rugby_favs[0][5],os.path.join(favlogos,rugby_favs[0][5].split('/')[-1]),))
							t2logo.start()
						except: pass
					else: pass
					#motorsport
					if motorsport_favs:
							save(motorsport_file,str(motorsport_favs))
							sport_favs.append('Motorsport')
					if len(motorsport_favs) > 1 and settings.getSetting('enable-motorsport') == 'true':
						motorsport_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in motorsport_favs:
							motorsport_names.append(team_name)
						ret = dialog.select("Motorsport favourite?", motorsport_names)
						save(motorsport_fav_file,str(motorsport_favs[ret]))
						try:
							t3 = threading.Thread(name='logodown3', target=Downloader , args=(motorsport_favs[ret][2],os.path.join(favlogos,motorsport_favs[ret][2].split('/')[-1]),))
							t3.start()
						except: pass
						try:
							t3fan = threading.Thread(name='logodownfan3', target=Downloader , args=(motorsport_favs[ret][4],os.path.join(favlogos,motorsport_favs[ret][4].split('/')[-1]),))
							t3fan.start()
						except: pass
						try:
							t3logo = threading.Thread(name='logodownlogo3', target=Downloader , args=(motorsport_favs[ret][5],os.path.join(favlogos,motorsport_favs[ret][5].split('/')[-1]),))
							t3logo.start()
						except: pass
					elif len(motorsport_favs) == 1 and settings.getSetting('enable-motorsport') == 'true':
						save(motorsport_fav_file,str(motorsport_favs[0]))
						try:
							t3 = threading.Thread(name='logodown3', target=Downloader , args=(motorsport_favs[0][2],os.path.join(favlogos,motorsport_favs[0][2].split('/')[-1]),))
							t3.start()
						except: pass
						try:
							t3fan = threading.Thread(name='logodownfan3', target=Downloader , args=(motorsport_favs[0][4],os.path.join(favlogos,motorsport_favs[0][4].split('/')[-1]),))
							t3fan.start()
						except: pass
						try:
							t3logo = threading.Thread(name='logodownlogo3', target=Downloader , args=(motorsport_favs[0][5],os.path.join(favlogos,motorsport_favs[0][5].split('/')[-1]),))
							t3logo.start()
						except: pass
					else: pass
					#basketball
					if basketball_favs:
							save(basketball_file,str(basketball_favs))
							sport_favs.append('Basketball')
					if len(basketball_favs) > 1 and settings.getSetting('enable-basketball') == 'true':
						basketball_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in basketball_favs:
							basketball_names.append(team_name)
						ret = dialog.select("Basketball favourite?", basketball_names)
						save(basketball_fav_file,str(basketball_favs[ret]))
						try:
							t4 = threading.Thread(name='logodown4', target=Downloader , args=(basketball_favs[ret][2],os.path.join(favlogos,basketball_favs[ret][2].split('/')[-1]),))
							t4.start()
						except: pass
						try:
							t4fan = threading.Thread(name='logodownfan4', target=Downloader , args=(basketball_favs[ret][4],os.path.join(favlogos,basketball_favs[ret][4].split('/')[-1]),))
							t4fan.start()
						except: pass
						try:
							t4logo = threading.Thread(name='logodownfan4', target=Downloader , args=(basketball_favs[ret][5],os.path.join(favlogos,basketball_favs[ret][5].split('/')[-1]),))
							t4logo.start()
						except: pass
						
					elif len(basketball_favs) == 1 and settings.getSetting('enable-basketball') == 'true':
						save(basketball_fav_file,str(basketball_favs[0]))
						try:
							t4 = threading.Thread(name='logodown4', target=Downloader , args=(basketball_favs[0][2],os.path.join(favlogos,basketball_favs[0][2].split('/')[-1]),))
							t4.start()
						except: pass
						try:
							t4fan = threading.Thread(name='logodownfan4', target=Downloader , args=(basketball_favs[0][4],os.path.join(favlogos,basketball_favs[0][4].split('/')[-1]),))
							t4fan.start()
						except: pass
						try:
							t4logo = threading.Thread(name='logodownfan4', target=Downloader , args=(basketball_favs[0][5],os.path.join(favlogos,basketball_favs[0][5].split('/')[-1]),))
							t4logo.start()
						except: pass
					else: pass
					#amfootball
					if amfootball_favs:
							save(amfootball_file,str(amfootball_favs))
							sport_favs.append('American Football')
					if len(amfootball_favs) > 1 and settings.getSetting('enable-amfootball') == 'true':
						amfootball_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in amfootball_favs:
							amfootball_names.append(team_name)
						ret = dialog.select("AM Football favourite?", amfootball_names)
						save(amfootball_fav_file,str(amfootball_favs[ret]))
						try:
							t5 = threading.Thread(name='logodown5', target=Downloader , args=(amfootball_favs[ret][2],os.path.join(favlogos,amfootball_favs[ret][2].split('/')[-1]),))
							t5.start()
						except: pass
						try:
							t5fan = threading.Thread(name='logodownfan5', target=Downloader , args=(amfootball_favs[ret][4],os.path.join(favlogos,amfootball_favs[ret][4].split('/')[-1]),))
							t5fan.start()
						except: pass
						try:
							t5logo = threading.Thread(name='logodownlogo5', target=Downloader , args=(amfootball_favs[ret][5],os.path.join(favlogos,amfootball_favs[ret][5].split('/')[-1]),))
							t5logo.start()
						except: pass
					elif len(amfootball_favs) == 1 and settings.getSetting('enable-amfootball') == 'true':
						save(amfootball_fav_file,str(amfootball_favs[0]))
						try:
							t5 = threading.Thread(name='logodown5', target=Downloader , args=(amfootball_favs[0][2],os.path.join(favlogos,amfootball_favs[0][2].split('/')[-1]),))
							t5.start()
						except: pass
						try:
							t5fan = threading.Thread(name='logodownfan5', target=Downloader , args=(amfootball_favs[0][4],os.path.join(favlogos,amfootball_favs[0][4].split('/')[-1]),))
							t5fan.start()
						except: pass
						try:
							t5logo = threading.Thread(name='logodownlogo5', target=Downloader , args=(amfootball_favs[0][5],os.path.join(favlogos,amfootball_favs[0][5].split('/')[-1]),))
							t5logo.start()
						except: pass
					else: pass
					#icehockey
					if icehockey_favs:
							save(icehockey_file,str(icehockey_favs))
							sport_favs.append('Ice Hockey')
					if len(icehockey_favs) > 1 and settings.getSetting('enable-icehockey') == 'true':
						icehockey_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in icehockey_favs:
							icehockey_names.append(team_name)
						ret = dialog.select("Ice Hockey favourite?", icehockey_names)
						save(icehockey_fav_file,str(icehockey_favs[ret]))
						try:
							t6 = threading.Thread(name='logodown6', target=Downloader , args=(icehockey_favs[ret][2],os.path.join(favlogos,icehockey_favs[ret][2].split('/')[-1]),))
							t6.start()
						except: pass
						try:
							t6fan = threading.Thread(name='logodownfan6', target=Downloader , args=(icehockey_favs[ret][4],os.path.join(favlogos,icehockey_favs[ret][4].split('/')[-1]),))
							t6fan.start()
						except: pass
						try:
							t6logo = threading.Thread(name='logodownlogo6', target=Downloader , args=(icehockey_favs[ret][5],os.path.join(favlogos,icehockey_favs[ret][5].split('/')[-1]),))
							t6logo.start()
						except: pass
					elif len(icehockey_favs) == 1 and settings.getSetting('enable-icehockey') == 'true':
						save(icehockey_fav_file,str(icehockey_favs[0]))
						try:
							t6 = threading.Thread(name='logodown6', target=Downloader , args=(icehockey_favs[0][2],os.path.join(favlogos,icehockey_favs[0][2].split('/')[-1]),))
							t6.start()
						except: pass
						try:
							t6fan = threading.Thread(name='logodownfan6', target=Downloader , args=(icehockey_favs[0][4],os.path.join(favlogos,icehockey_favs[0][4].split('/')[-1]),))
							t6fan.start()
						except: pass
						try:
							t6logo = threading.Thread(name='logodownlogo6', target=Downloader , args=(icehockey_favs[0][5],os.path.join(favlogos,icehockey_favs[0][5].split('/')[-1]),))
							t6logo.start()
						except: pass
					else: pass
					#baseball
					if baseball_favs:
							save(baseball_file,str(baseball_favs))
							sport_favs.append('Baseball')
					if len(baseball_favs) > 1 and settings.getSetting('enable-baseball') == 'true':
						baseball_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in baseball_favs:
							baseball_names.append(team_name)
						ret = dialog.select("Baseball favourite?", baseball_names)
						save(baseball_fav_file,str(baseball_favs[ret]))
						try:
							t7 = threading.Thread(name='logodown7', target=Downloader , args=(baseball_favs[ret][2],os.path.join(favlogos,baseball_favs[ret][2].split('/')[-1]),))
							t7.start()
						except: pass
						try:
							t7fan = threading.Thread(name='logodownfan7', target=Downloader , args=(baseball_favs[ret][4],os.path.join(favlogos,baseball_favs[ret][4].split('/')[-1]),))
							t7fan.start()
						except: pass
						try:
							t7logo = threading.Thread(name='logodownlogo7', target=Downloader , args=(baseball_favs[ret][5],os.path.join(favlogos,baseball_favs[ret][5].split('/')[-1]),))
							t7logo.start()
						except: pass
					elif len(baseball_favs) == 1 and settings.getSetting('enable-baseball') == 'true':
						save(baseball_fav_file,str(baseball_favs[0]))
						try:
							t7 = threading.Thread(name='logodown7', target=Downloader , args=(baseball_favs[0][2],os.path.join(favlogos,baseball_favs[0][2].split('/')[-1]),))
							t7.start()
						except: pass
						try:
							t7fan = threading.Thread(name='logodownfan7', target=Downloader , args=(baseball_favs[0][4],os.path.join(favlogos,baseball_favs[0][4].split('/')[-1]),))
							t7fan.start()
						except: pass
						try:
							t7logo = threading.Thread(name='logodownlogo7', target=Downloader , args=(baseball_favs[0][5],os.path.join(favlogos,baseball_favs[0][5].split('/')[-1]),))
							t7logo.start()
						except: pass
					else: pass
					#golf
					if golf_favs:
							save(golf_file,str(golf_favs))
							sport_favs.append('Golf')
					if len(golf_favs) > 1 and settings.getSetting('enable-golf') == 'true':
						golf_names = []
						for team_id,team_name,team_badge,team_sport,team_fan_fanart,team_logo_fanart in golf_favs:
							golf_names.append(team_name)
						ret = dialog.select("Favourite golfer?", golf_names)
						save(golf_fav_file,str(golf_favs[ret]))
						try:
							t8 = threading.Thread(name='logodown8', target=Downloader , args=(golf_favs[ret][2],os.path.join(favlogos,golf_favs[ret][2].split('/')[-1]),))
							t8.start()
						except: pass
						try:
							t8fan = threading.Thread(name='logodownfan8', target=Downloader , args=(golf_favs[ret][4],os.path.join(favlogos,golf_favs[ret][4].split('/')[-1]),))
							t8fan.start()
						except: pass
						try:
							t8logo = threading.Thread(name='logodownlogo8', target=Downloader , args=(golf_favs[ret][5],os.path.join(favlogos,golf_favs[ret][5].split('/')[-1]),))
							t8logo.start()
						except: pass
					elif len(golf_favs) == 1 and settings.getSetting('enable-golf') == 'true':
						save(golf_fav_file,str(golf_favs[0]))
						try:
							t8 = threading.Thread(name='logodown8', target=Downloader , args=(golf_favs[0][2],os.path.join(favlogos,golf_favs[0][2].split('/')[-1]),))
							t8.start()
						except: pass
						try:
							t8fan = threading.Thread(name='logodownfan8', target=Downloader , args=(golf_favs[0][4],os.path.join(favlogos,golf_favs[0][4].split('/')[-1]),))
							t8fan.start()
						except: pass
						try:
							t8logo = threading.Thread(name='logodownlogo8', target=Downloader , args=(golf_favs[0][5],os.path.join(favlogos,golf_favs[0][5].split('/')[-1]),))
							t8logo.start()
						except: pass
					else: pass
					
					#Let us find out what the user loves the most
					if sport_favs and len(sport_favs) > 1:
						ret = dialog.select("Favourite Sport?", sport_favs)
						save(sport_fav_file,str(urllib.quote(sport_favs[ret].lower())))
					elif sport_favs and len(sport_favs) == 1:
						save(sport_fav_file,str(urllib.quote(sport_favs[0].lower())))
					else: pass
					
					#waiting for badge download to finish
					try:t1.join()
					except:pass
					try:t1fan.join()
					except:pass
					try:t1logo.join()
					except:pass
					try:t2.join()
					except:pass
					try:t2fan.join()
					except:pass
					try:t2logo.join()
					except:pass
					try:t3.join()
					except:pass
					try:t3fan.join()
					except:pass
					try:t3logo.join()
					except:pass
					try:t4.join()
					except:pass
					try:t4fan.join()
					except:pass
					try:t4log.join()
					except:pass
					try:t5.join()
					except:pass
					try:t5fan.join()
					except:pass
					try:t5logo.join()
					except:pass
					try:t6.join()
					except:pass
					try:t6fan.join()
					except:pass
					try:t6logo.join()
					except:pass
					try:t7.join()
					except:pass
					try:t7fan.join()
					except:pass
					try:t7logo.join()
					except:pass
					try:t8.join()
					except:pass
					try:t8fan.join()
					except:pass
					try:t8logo.join()
					except:pass
					
					#Keymap stuff
					dialog = xbmcgui.Dialog()
					yes_no = dialog.yesno('Sports Center Wizzard', 'Do want to enable on-screen information and define a keymap?')
					if yes_no:
						settings.setSetting('enable-onscreenservice','true')
						keymaper.run()			
				settings.setSetting('wizzard_check','false')
				xbmc.executebuiltin( "Dialog.Close(busydialog)" )	
							
	
			else:
				mensagemok('Sports Center', 'Please consider to make one.', 'Register yourself at http://www.thesportsdb.com')
				mensagemok('Sports Center', "That's the only way you can follow your team(s)!")
				yes_no = dialog.yesno('Sports Center Wizzard', "Do you want the wizzard to run the next time?")
				if not yes_no: settings.setSetting('wizzard_check','false')
		return
