import json
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuth

class StdOutListener(StreamListener):

	def on_data(self, data):

		j=json.loads(data)

		screenName=j["user"]["screen_name"] #twitter username
		text=j["text"] #text of tweet
		retweetCount=str(j["retweet_count"]) #for tweet
		followers=str(j["user"]["followers_count"]) #followers of user
		friends=str(j["user"]["friends_count"]) #number of people that user follows
		tweetCount=str(j["user"]["statuses_count"]) #total number of tweets for of user
		celeb=str(j["user"]["verified"]) #key individuals and brands as determined by Twitter
		location=j["place"]["full_name"] #user-defined location
		coordinates=str(j["coordinates"]) #coordinates of tweet; note: it goes (longitude,latitude)

		print (screenName)+": "+(text)
		print "Retweets: "+(retweetCount)
		print "Followers: "+(followers)
		print "Following: "+(friends)
		print "# of Tweets: "+(tweetCount)
		print "Verified: "+(celeb)
		print "Location: "+(location)
		print "Coordinates: "+(coordinates)+"\n"

		outputFile.write(screenName.encode('ascii','ignore') + ": " + text.encode('ascii','ignore') + "\n")
		outputFile.write("Retweets: " + retweetCount.encode('ascii','ignore') + "\n")
		outputFile.write("Followers: " + followers.encode('ascii','ignore') + "\n")
		outputFile.write("Following: " + friends.encode('ascii','ignore') + "\n")
		outputFile.write("# of Tweets: " + tweetCount.encode('ascii','ignore') + "\n")
		outputFile.write("Verified: " + celeb.encode('ascii','ignore') + "\n")
		outputFile.write("Location: " + location.encode('ascii','ignore') + "\n")
		outputFile.write("Coordinates: " + coordinates.encode('ascii','ignore') + "\n\n")

if __name__ == '__main__':
	try:
		def timeStamped(fname, fmt='%d-%m-%Y{fname}'):
    			return datetime.datetime.now().strftime(fmt).format(fname=fname)
  
		outputFile = open(timeStamped(".txt"),"w") #still need to implement way to output to new file every 24:00 hrs

		l = StdOutListener()
		auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

		stream = Stream(auth, l)

    #location stream filters
		stream.filter(locations=[-95.865,40.5,-91.0,43.5]) #Iowa (fixed square)
		stream.filter(locations=[-91.0,41.529,-90.637,42.5]) #Added Dubuque + Quad Cities
		stream.filter(locations=[-96.05,41.518,-95.865,43.5]) #Subtracted Omaha
		stream.filter(locations=[-96.467,42.41,-96.05,41.518]) #Added Sioux City 
		stream.filter(locations=[-90.637,41.808,-90.17,41.154]) #Added Clinton

	except KeyboardInterrupt:
		pass

outputFile.close()
