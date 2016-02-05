#remaining objective(s):
#need to create new file after certain amounts of tweets/time
#need to remove text filters and filter after applying geo-filter
#Visualization

import sys
import json
import datetime
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuth
import os.path



class StdOutListener(StreamListener):

	tweet_count = 0
	

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream


	def encode(text):

		
	#	For printing unicode characters to the console.
		
		return text.encode('utf-8')

	def on_data(self, data):

		j=json.loads(data)

		time_collected = j["created_at"]
		screenName=j["user"]["screen_name"] #twitter username
		text=j["text"] #text of tweet
		retweetCount=str(j["retweet_count"]) #for tweet
		followers=str(j["user"]["followers_count"]) #followers of user
		friends=str(j["user"]["friends_count"]) #number of people that user follows
		tweetCount=str(j["user"]["statuses_count"]) #total number of tweets for of user
		celeb=str(j["user"]["verified"]) #key individuals and brands as determined by Twitter
		location=str(j["place"]["full_name"]) #user-defined location
		coordinates=str(j["coordinates"]) #coordinates of tweet; note: it goes (longitude,latitude)

		'''
		print (screenName)+": "+(text)		#we don't need to do this anymore 
		print "Retweets: "+(retweetCount)
		print "Followers: "+(followers)
		print "Following: "+(friends)
		print "# of Tweets: "+(tweetCount)
		print "Verified: "+(celeb)
		print "Location: "+(location)
		print "Coordinates: "+(coordinates)+"\n"
		'''

		outputFile.write(time_collected.encode('ascii','igore')+"\n")
		outputFile.write(screenName.encode('ascii','ignore') + ": " + text.encode('ascii','ignore') + "\n")
		outputFile.write("Retweets: " + retweetCount.encode('ascii','ignore') + "\n")
		outputFile.write("Followers: " + followers.encode('ascii','ignore') + "\n")
		outputFile.write("Following: " + friends.encode('ascii','ignore') + "\n")
		outputFile.write("# of Tweets: " + tweetCount.encode('ascii','ignore') + "\n")
		outputFile.write("Verified: " + celeb.encode('ascii','ignore') + "\n")
		outputFile.write("Location: " + location.encode('ascii','ignore') + "\n")
		outputFile.write("Coordinates: " + coordinates.encode('ascii','ignore') + "\n\n")

		self.tweet_count = self.tweet_count+1
		
		b = self.tweet_count
		b = str(b)

		print ("\rTweets collected: " +b ) ,
		sys.stdout.flush()
    	



if __name__ == '__main__':
	try:
		def timeStamped(fname, fmt='%d-%m-%Y{fname}'):
				return datetime.datetime.now().strftime(fmt).format(fname=fname)
		
		if (os.path.isfile(timeStamped(".txt"))):
			outputFile = open(timeStamped(".txt"),"a")

		else:
			outputFile = open(timeStamped(".txt"),"w") #still need to implement way to output to new file every 24:00 hrs

		l = StdOutListener()
		auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

		stream = Stream(auth, l)
		
	#location stream filters
		reload(sys)
		sys.setdefaultencoding("utf-8")
		#stream.filter(locations=[-95.865,40.5,-91.0,43.5]) #Iowa (fixed square)
		#stream.filter(locations=[-91.0,41.529,-90.637,42.5]) #Added Dubuque + Quad Cities
		#stream.filter(locations=[-96.05,41.518,-95.865,43.5]) #Subtracted Omaha
		#stream.filter(locations=[-96.467,42.41,-96.05,41.518]) #Added Sioux City 
		#stream.filter(locations=[-90.637,41.808,-90.17,41.154]) #Added Clinton
		
		while True:  #Endless loop: personalize to suit your own purposes
			try: 
        		#stream.statuses.filter(track='foo bar,foobar,more search strings here')
				stream.filter(locations=[-72.6,42.5,-70.7,45.5]) #new hampshire square
			except:
        		#e = sys.exc_info()[0]  #Get exception info (optional)
        		#print 'ERROR:',e  #Print exception info (optional)
				continue

		# print("Streaming...")
		# stream.filter(locations=[
		# -95.865,40.5,-91.0,43.5,
		# -91.001,41.529,-90.637,42.5,
		# -96.05,41.518,-95.865,43.5,
		# -96.467,41.518,-96.05,42.41, 
		# -90.637,41.154,-90.17,41.808])
		

	#text stream filters (need to remove and put into percent.py file)
		#stream.filter(track=["HillaryClinton", "Hillary2016", "Hillary",
		 #   "Lessig", "Lessig2016", "Lessig2016",
			#"O'Malley", "OMalley2016", "MartinOMalley",
		  #  "Bernie", "FeelTheBern", "Bernie2016",
		  #  "Jeb", "JebBush", "Jeb2016",
		 #   "Carson", "BC2DC16", "RealBenCarson",
		  #  "Chris Christie", "Christie2016", "ChrisChristie",
		 #   "Cruz", "CruzCrew", "TedCruz",
		   # "Fiorina", "Carly2016", "CarlyFiorina",
		#    "Jim Gilmore", "JimGilmore", "gov_gilmore",
		#    "Graham", "LindseyGraham", "LindseyGrahamSC", 
		#    "Huckabee", "ImWithHuck", "GovMikeHuckabee", 
		#    "Jindal", "BobbyJindal", "BobbyJindal", 
		#    "Kasich", "Kasich4Us", "JohnKasich", 
		#   "Rand Paul", "RandPaul2016", "RandPaul", 
		   # "Rubio", "MarcoRubio", 
		 #   "Santorum", "RickSantorum", 
		 #   "Trump", "DonaldTrump2016", "realDonaldTrump"])


	except KeyboardInterrupt:
		outputFile.close()
		pass






	#TODO: create a map that pin points where in Iowa people are tweeting?
