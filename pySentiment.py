import re
import tweepy
import time
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'jU6B8jHiMYQbOnknLsSUeK7lJ'
		consumer_secret = 'Wb9D3QsLQx5BCAuiozqqppEkJPhtztgJYbBDSlWIJS8tAfujnO'
		access_token = '771604896093044736-D8nkwRJahA1VVerfSbTBSVrcFXzvA4Y'
		access_token_secret = '10OdwNoVmSOj3zALywzp2C3ZVzN7ZPXKi1lo8XQWLvm1N'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def TweetAnalyse(searchTerm):

	api = TwitterClient()
	# calling function to get tweets
	tweets = api.get_tweets(query = searchTerm, count = 200)

	# calculating number of tweets checked
	lenTweets = 1 if len(tweets)==0 else len(tweets)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	sharePtweets = round(len(ptweets)/lenTweets,4)

	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	shareNtweets = round(len(ntweets)/lenTweets,4)

	return [lenTweets,sharePtweets,shareNtweets,ptweets[0:3],ntweets[0:3]]	

if __name__ == "__main__":
	searchTerm = input("Enter the Search Keyword: ")
	x = TweetAnalyse(searchTerm)
	print()
	print("Number of Tweets searched: " + str(x[0]))
	print("Postive Share is "+str(round(x[1]*100,2))+"%")
	print("Negative Share is "+str(round(x[2]*100,2))+"%")
	print("Completed for Search Term: "+searchTerm)