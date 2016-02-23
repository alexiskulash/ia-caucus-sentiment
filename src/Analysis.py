#Jenny Steffens
#Notes:
#99 counties in IA
# -96.639389   40.375458		outer coordinates of iowa
# -90.139938   43.500713

'''
this program contains two objects, Analyzer, which can be used to screen and organize data, and a subclass,
Visualizer, that is used when information is to be printed to the screen. Since it is a subclass, it also has
all the necessary analyzer functions. Mostly, the distinction is made based on logic, (so the functions are
easier to find in this file) and because if you don't plan on visualizing, it doesn't make a lot of sense
to call something named 'Visualizer.' Right now it is only set up to read in Iowa counties/coords, but this will soon be
changed to include any state determined by an input. Made for Python 2 but should be ok for Python 3
''' 
from graphics import *							#drawing
import os, sys
import csv



class Analyzer(object):
	'''
		_state = ""
		_statefilename = ""
		_countiesList = ''
		_topstuff = ''    #useful for when we generalize
		_keyworddictionary = ''
		_keywordlist = []
	'''
	def __init__(self, kD, state='ia'):

		self._state = state.upper()
		self._statefilename = state +'.txt'
		self._keywordlist = []
	
		self._countiesList = self.read_in()
		self._keyworddictionary = kD

		
		for key in self._keyworddictionary:
			for word in self._keyworddictionary[key]:
				self._keywordlist.append(word)
		
		self.normalize_list(self._keywordlist)
		
		

	def read_in(self, filename=None):	#a function that stores the data from the txt file in a list.
							         #NOTE: I changed the text file to seperate the coordinates by ',' instead of '   ' and erased
						          	#the line that specified the state of Iowa. 

		if filename is None:
			filename = self._statefilename
		counties = []	# a list of 2D arrays  (A 3D array? kind of?)

		# i in range (99):
			#counties.append(i)	#creates a slot for each county

		f = open(filename, 'r')	#open the file, prep for reading

		for i in range (99):	#now the fun begins
			
			coord = [] #empties coord every run through

			county = f.readline()
			county = county.replace("\n","")
			f.readline()               #gets rid of \n
			size = int(f.readline())   #confirmed has correct data. 


			for k in range(size+1):		#creates a space for each pair PLUS one to hold the name of the county
				coord.append(k)

			a = []		#some placeholder lists
			b = []
			c = []

			for j in range(size):			#confirmed correct loop iterations
				
				a.append(f.readline())
				b = a[j].split(",")			  #breaks up the coordinates for easier access later.
				b[0] = b[0].replace(" ","")   #trims the data of what we don't want
				b[1] = b[1].replace("\n","")
				coord[j+1] = (b)             #replaces the placeholder value in coord to what we really want it to be

			c.append(county)
			c.append(size)

			coord[0] = c


			#print coord   #Huzzah! Success!

			counties.append(coord) 

			f.readline() #eats the new line 

		#print counties

		f.close()  #free up some memory

		#print "mep", counties[0]
		return counties

	def get_county_name(self, index, counties=None):   #will return the string stored in each coord


		if counties is None:
			counties = self._countiesList
		if (index == 99):
			return 'Other'
		#print counties, len(counties)
		coord = counties[index]
		name = coord[0][0]

		return name
		
	'''
	def get_county_name(self, s, size, counties=None):

		if counties is None:
			counties = self._countiesList
		a = []
		for i in range(99):
			peint
			coord = counties[i]
			if coord[0][1] == size:
				a.append(coord[0][0])

		return a    #in case there is more than one county of that size

	'''
	def get_index(self, name, counties=None):

		if counties is None:
			counties = self._countiesList
		for i in range(99):

			coord = counties[i]
			if coord[0][0] == name:

				return i
		return -1


	def get_size(self, index, counties=None):	#will return how many (x,y) coords for the specified county

		if counties is None:
			counties = self._countiesList

		coord = counties[index]
		size = coord[0][1]

		return size

	def get_size(self, name, counties=None): #using the name of the county as a parameter

		if counties is None:
			counties = self._countiesList

		for i in range (99):

			coord = counties[i]
			if coord[0][0] == name:
				return coord[0][1]

		return 0

	def normalize(self, token):

		#print (token)
		token = token.replace(".","")
		token = token.replace(",","")
		token = token.replace("'","")
		token = token.replace(";","")
		token = token.replace("\n","")
		token = token.replace("\'","")
		token = token.replace("\"","")
		token = token.replace("#","")
		token = token.lower()

		return token

	def normalize_list(self, list_a):

		for word in list_a:
			word = self.normalize(word)

		return list_a

	def read_tweet(self, inputFile):  ###DOES NOT OPEN FILE NEEDS TO BE DONE BEFORE CALLING
		
		tweet = []  # a list, each element will be a different part of tweet data
		more_message = True		#message reading loopbreaker

		time = False

		firstline = inputFile.readline()

		if not firstline: return tweet   #end of file error
		if "+0000" in firstline:			#all these tweets are in GMT. If that changes, so does this
			time = True
			tweet.append(firstline)
			firstline = inputFile.readline()
			
		while more_message:

			
			check_message_done = inputFile.readline()	#reads message first line

			if 'Retweets: ' in check_message_done:		#if the message was only one line

				tweet.append(firstline)
				tweet.append(check_message_done)
				more_message = False				#loopbreaker

			else:

				firstline = firstline + check_message_done  #append the first line and continue loop


		while True:		#only way i didn't get an error thrown

			line = inputFile.readline()		#this loops reads the rest of the tweet data and stores each
			if line == "\n": break         #line (retweet #, followers, location etc)
			if not line:					#EoF
				more_text = False
				break			#breaks outer loop
				
			tweet.append(line)

			#if not line: break         #in case something goes wrong or EoF
			#if not len(tweet): break    

		return tweet


	def screen_keywords(self, datedfilename, keywords_list=None):

		if keywords_list is None:
			keywords_list = self.normalize_list(self._keywordlist)

		if not keywords_list:
			return 0

		inputFile = open(datedfilename, 'r')

		new_file_name = "screened_keywords_"+ datedfilename
		outputFile = open(new_file_name, 'w')   

		while True:

			text = self.read_tweet(inputFile)
			if not text: break
			message = text[1]
			text.append('\n')

			for word in keywords_list:
				if word in message:
					for i in range(len(text)):
						outputFile.write(text[i])   #saving the good tweets to a new .txt file
				else:
					pass

		print ("Screened for keywords.") 

		inputFile.close()
		outputFile.close()

		return new_file_name




	def screen_coord(self, datedfilename):		#writes a file for the visualizer, that only contains tweets 
												#which have coordinates. WORKS FOR NEWFORMAT
		inputFile = open(datedfilename, 'r')

		new_file_name = "screened_location_"+ datedfilename

		outputFile = open(new_file_name, 'w')

		while True:

			text = self.read_tweet(inputFile)
			if not text: break
			c = text[-1]       #the last element is the coordinates	
			text.append('\n')	#prettier when it prints
			if 'Coordinates' not in c:
				c = text[-2]
			
			if ("u'type': u'Point', u'coordinates'") in c:		#if there are coordinates to track
			
				#print c                  #debugging
				for i in range(len(text)):
					outputFile.write(text[i])   #saving the good tweets to a new .txt file

		print ("Screened for usable coordinates.") 

		inputFile.close()
		outputFile.close()

		return new_file_name


	def double_screen(self, datedfilename, keywords_list=None): 

		if keywords_list is None:
			keywords_list = self._keywordlist
			new_file_name = self.screen_coord(self.screen_keywords(datedfilename))
		else:
			new_file_name = self.screen_coord(self.screen_keywords(datedfilename, keywords_list=keywords_list))

		new_new_file_name = os.rename(new_file_name, "screened_"+datedfilename)

		return "screened_"+datedfilename

	def combine_files(self, filelist, new_name):

		output = open(new_name, 'w')

		for f in filelist:
			inputfile = open(f, 'r')
			text = inputfile.read()
			output.write(text)
			inputfile.close()

		output.close()
		return new_name

	def screen_and_combine(self, filelist, new_name, keywords_list=None):

		if keywords_list is None:
			keywords_list = self._keywordlist

		new_files = []
		for f in filelist:
			name = self.double_screen(f, keywords_list)
			newfiles.append(name)
		self.combine_files(newfiles, new_name)
		for n in newfiles:
			os.remove(n)
		return new_name

	def dictionary_to_scores(self, dictionary=None, names=True):  #FIXED

		if dictionary is None:
			dictionary = self._keyworddictionary.copy()
		s = []   # a list to hold the scores, to be assigned to each key in the dictionary
		scores = dictionary.copy()		#new dictionary
		for key in scores:
			
			for i in range(100):			#placeholder for each county in Iowa plus one for those not in coordinates
				s.append([0])
				if names:
					s.append(self.get_county_name(i))

			scores[key] = s
			s = []

		return scores

	def get_coordinates(self, tweet):  #takes in whole tweet (list)

		coordinates = []

		line = tweet[-1]
		if 'None' in line:
			return [0,0]
		#line looks like Coordinates: {u'type': u'Point', u'coordinates': [-93.5614014, 41.6209946]}
		a = line.partition('[')
		b = a[2].partition(']')

		c = b[0]

		#Now coordinates should look like -93.5614014, 41.6209946
		d = c.split(',')

		coordinates.append(float(d[0]))
		coordinates.append(float(d[1]))


		return coordinates


	def point_inside_polygon(self, x,y,poly):

	    n = len(poly)
	    for i in range (n):
	    	poly[i][0] = float(poly[i][0])
	    	poly[i][1] = float(poly[i][1])

	    inside = False

	    p1x,p1y = poly[0]        #found online, fingers crossed
	    #print p1x,p1y
	    for i in range(n+1):
	        p2x,p2y = poly[i % n]
	        if y > min(p1y,p2y):
	            if y <= max(p1y,p2y):
	                if x <= max(p1x,p2x):
	                    if p1y != p2y:
	                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
	                    if p1x == p2x or x <= xinters:
	                        inside = not inside
	        p1x,p1y = p2x,p2y

	    return inside

	def find_county(self, coordinates, county_list=None): #coordinates is a list of two strings. 

		if county_list is None:
			county_list = self._countiesList[:]
		#length = len(county_list)

		x = float(coordinates[0])
		y = float(coordinates[1])

		foundit = False

		if y == 0.0 and x == 0.0:		#if not in the counties
			return [99, 'Other']
		#print len(county_list)
		for i in range (99):

			county = county_list[i]
			name,size = county[0]
			#print "bloop ", name
			foundit = self.point_inside_polygon(x, y, county[1:])

			if foundit:
				return [i, name] #the index and name string of the county

		return[99, 'Other']

		#return ("Not in usuable area")  #if it doesn't work
	


	def tally_scores(self, filename, dictionary=None, names=True):   #this file should be sorted coordinates and keywords
		

		if dictionary is None:
			dictionary = self._keyworddictionary.copy()

		score_dictionary = self.dictionary_to_scores(dictionary=dictionary, names=names) 
		#print "k", dictionary

		inputFile = open(filename, 'r')


		while True:

			tweet = self.read_tweet(inputFile)		#read each tweet
			if not tweet: break

			text = tweet[0]
			coordinates = self.get_coordinates(tweet)  #where is the tweet from

			for key in dictionary:
				#print "j", dictionary[key]
				keywords_list = self.normalize_list(dictionary[key])  #for each candidate

				for word in keywords_list:
					if word in text:
						candidate = key
						county_index = (self.find_county(coordinates))[0]
						if names:
							county_index = 2*county_index
						score_dictionary[candidate][county_index][0] += 1
						if text not in score_dictionary[candidate][county_index]:
							score_dictionary[candidate][county_index].append(text)
						break
		inputFile.close()
		return score_dictionary


	def check_if_filtered(self, filename):  #this is for debugging stream

		inputFile = open(filename, 'r')

		yes_no = [0,0]

		while True:

			tweet = self.read_tweet(inputFile)
			if not tweet: break
			c = self.get_coordinates(tweet)
			if not c: break
			c2 = self.find_county(c)
			if not c2: break
			if c2[1] == 'Other':
				yes_no[1] += 1 			#if the coordinates are in iowa, yes
			else:
				yes_no[0] += 1  		#if not, no

		inputFile.close()
		return yes_no    #returns [how many in, how many out]

	def chatter(self, candidate, filename, dictionary):  #filename is a list of files here of any size

		chatter_dictionary = {candidate: []}
		for i in range(100):
			chatter_dictionary[candidate].append(0)

		for f in range (len(filename)):
			score_dictionary = self.tally_scores(filename[f], dictionary)

			for i in range(len(chatter_dictionary[candidate])):
				chatter_dictionary[candidate][i] = score_dictionary[candidate]

		return chatter_dictionary

	def red_blue_chatter(self, candidates, filename, dictionary):

		red = candidates[0]
		blue = candidates[1]

		redblue = []

		red_chatter = self.chatter(red, filename, dictionary)
		blue_chatter = self.chatter(blue, filename, dictionary)

		redblue.append(red_chatter)
		redblue.append(blue_chatter)

		return redblue

	def write_csv(self, destination, inputFile, group_by="candidate", text=True, score=True, county_names=False, score_tally=None, labels=True):

		if score_tally is None:
			score_tally = self.tally_scores(inputFile, names=county_names)
		with open(destination, 'wb') as csvfile:
			#print (score_tally)
			#print score_tally
			outputFile = csv.writer(csvfile)


			if group_by=="candidate":

				if labels:
					labels_list = []
					labels_list.append("Candidate")
					labels_written = False

				
				for key in score_tally:
					
					if labels:
						if labels_written==False:
							#for key in score_tally:
							for i in range(100):
								if county_names:
									labels_list.append("")
									#if (i<99):
									labels_list.append(score_tally[key][i][1])

								if not county_names:
									if (i < 99):
										county = self._countiesList[:][i][0][0]
									else:
										county = 'Other'
									labels_list.append(county)
									
							for word in labels_list:
								word = word.title()
							outputFile.writerow(labels_list)
							labels_written = True
						else:
							pass

					score_tally[key].insert(0, key.title())
					outputFile.writerow(score_tally[key])

			elif group_by=="county":

				if not labels:
					print("You should really label these ... (labels=True)")

				county_list = self._countiesList[:]
				flipped_tally = []
				#reverse_dictionary = {}
				county_list_names = []
				labels_list = []

				if labels:
					
					labels_list.append("County")
					labels_written = False

				for i in county_list:

					county_list_names.append([i[0][0]])
				county_list_names.append(["Other"])

				for i in range(100):
					flipped_tally.append([])
					

				
				for key in score_tally:
					labels_list.append(key.title())

					for j in range(100):
						  
						if county_names:
							thing = score_tally[key][2*j]
							flipped_tally[j].append(thing)
						elif not county_names:
							thing = score_tally[key][j]
							flipped_tally[j].append(thing)


				for k in range(len(county_list_names)):
					flipped_tally[k].insert(0, county_list_names[k][0])

				if labels:
					for word in labels_list:
						word = word.title()
					outputFile.writerow(labels_list)

				for m in flipped_tally:
					outputFile.writerow(m)












		
		return destination



class Visualizer(Analyzer):

	
	   #in terms of pixels for later conversion.
	
	def __init__(self, state='ia'):

		super(Visualizer, self).__init__(state)
		map_width = .75    #the displayed map will be 50% of the screens width and height
		map_height = .75	#to be fixed later
		#window = GraphWin()
		

	def new_Window(self):

		win = GraphWin("Colored Iowa",1000,500)		#make a window

		return win

	def set_menu(self, name, blue, red):

		menu = Text(Point(900,250), "County Data: ")
		return menu

	def winWidth(self):

		'''
		pixels_x = NSScreen.mainScreen().frame().width*map_width
		return pixels_x
		'''

		return 800

	def winHeight(self):

		'''
		pixels_y = NSScreen.mainScreen().frame().height*map_height
		return pixels_y
		'''
		return 500


	def create_points(self, county):  #here county is counties[some index]


		#-96.639389   40.375458		outer coordinates of IA
		#-90.139938   43.500713

		#Note: this assumes (0,0) is the bottom right corner, and (max x, max y) is top left

		width_min = 90.139938
		height_min = 40.375458

		width_max = 96.639389
		height_max = 43.500713

		widthC = width_max - width_min
		heightC = height_max - height_min

		ratio_w = widthC / (800)		#every pixel is ___ degrees	
		ratio_h = heightC / (500)

		#print ratio_w
		#print ratio_h

		size = county[0]			#fetching the name and size of each county
		size = size[1]
		name = county[0]
		name = name[0]

		new_points = []

		for i in range(size):

			k = i+1
			px = int((width_max - (float((county[k][0]))*-1))/ratio_w)		#converting degees to pixels. NEED TO FIX FORMULA //FIXED :D

			#print float(county[k][1])
			py = int((height_max - (float(county[k][1])))/ratio_h)
			#print (float(county[k][1])/ratio_h)
			#each element new_points is a Point(px,py)


			#print py
			p = Point(px, py)			
			#p.append(px)
			#p.append(py)
			new_points.append(p)

		return new_points

	def draw_county(self, new_points, color, window): #NOTE the data needs to be converted before this function is used

		county = Polygon(new_points)
		#print new_points
		county.setFill(color)
		county.draw(window)

	def gen_color(self, red, blue):

		red = float(red)
		blue = float(blue)
		
		R = int((red/(red+blue))*255)
		B = int((blue/(red+blue))*255)
		
		#print red,blue
		#print R,B
		RGB = color_rgb(R, 0, B)

		return RGB

if __name__ == '__main__':

	print("No main() yet :) sorry. Use Driver.py")

	

	









	


		







