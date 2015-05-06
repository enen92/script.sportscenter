import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,datetime
import thesportsdb,feedparser
from random import randint
from centerutils.common_variables import *
from centerutils.tweet import *


def tweets(tweeter_user):
	window = dialog_tweet('DialogTweeter.xml',addonpath,'Default',str(tweeter_user))
	window.doModal()

class dialog_tweet(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.mode = eval(args[3])[0]
		if self.mode == 'user':
			self.twitter_var = eval(args[3])[1]
			self.twitter_list = get_tweets(self.twitter_var)
		else:
			self.twitter_var = eval(args[3])[1]
			self.twitter_list = get_hashtag_tweets(self.twitter_var)


	def onInit(self):
		#set twitter logo
		self.getControl(3).setImage(os.path.join(addonpath,'resources','img','twitter.png'))
		#set twitter user name
		if self.mode == 'user':
			self.getControl(1).setLabel('@'+self.twitter_var)
		else:
			self.getControl(1).setLabel('#'+self.twitter_var.replace('#',''))
		for tweet_item,tweet_item_date in self.twitter_list:
			tweet = xbmcgui.ListItem(tweet_item)
			match = re.compile('(.+?) \+').findall(tweet_item_date)
			if match:
				tweet.setProperty('tweet_date',match[0])
			self.getControl(6).addItem(tweet)
		self.setFocusId(6)
		self.getControl(6).selectItem(0)

