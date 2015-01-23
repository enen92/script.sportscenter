import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from centerutils.common_variables import *
import competlist as competlist

def start(focus_sport):
	if not focus_sport: focus_sport = 'soccer'
	window = dialog_home('DialogMainMenu.xml',addonpath,'Default',focus_sport)
	window.doModal()
	
class dialog_home(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = args[3]

	def onInit(self):
		table = [('Football','football.png','soccer'),('Rugby','Rugby.png','rugby'),('MotorSport','Racing.png','motorsport'),('Basketball','Basketball.png','basketball'),('AM Football','americanfootball.png','american%20football'),('Ice Hockey','IceHockey.png','ice%20hockey')]
			   
		for sport,img,sport_name in table:
			item = xbmcgui.ListItem(sport, iconImage = os.path.join(addonpath,art,img),path='ActivateWindow(Videos)')
			item.setProperty('sport_clearlogo', os.path.join(addonpath,art,img))
			item.setProperty('sport_name', sport_name)
			self.getControl(980).addItem(item)
		
		self.getControl(912).setImage(os.path.join(addonpath,'fanart.jpg'))
		self.setFocusId(980)
		i=0
		for sport,img,sport_name in table:
			if sport_name == self.sport:
				index = i
			else: i+=1
		self.getControl(980).selectItem(index)
			
	def onClick(self,controlId):
		if controlId == 980:
			listControl = self.getControl(controlId)
			seleccionado=listControl.getSelectedItem()
			self.close()
			competlist.start(seleccionado.getProperty('sport_name'))
			
			
			#self.close()
