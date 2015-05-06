from twitter import *

con_secret='h7hSFO1BNKzyB2EabYf7RXXd5'
con_secret_key='tVbNWktkILCHu9CcENhXaUnLOrZWhJIHvBNcSEwgaczR8adZwU'
token='1226187432-3Tn0Euwt604LvNXGsVYWrgBrXa2xboo3UFgbrha'
token_key='KccVJ7kUFJhG7uZgJeQNizEbf9Z9spZDhEKGP3b3ogrH2'

t = Twitter(
    auth=OAuth(token, token_key, con_secret, con_secret_key))

def get_tweets(twitter_user):
	return_twitter = []
	tweet_list = t.statuses.user_timeline(screen_name=twitter_user,count=10)
	for tweet in tweet_list:
		return_twitter.append([tweet['text'],tweet['created_at']])
	return return_twitter
	
def get_hashtag_tweets(twitter_hash):
	return_twitter = []
	tweet_list = t.search.tweets(q=twitter_hash.replace('#',''),count=20)['statuses']
	for tweet in tweet_list:
		return_twitter.append([tweet['user']['name']+'-'+tweet['text'],tweet['created_at']])
	return return_twitter
