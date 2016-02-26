#Jenny Steffens

'''
this program contains two objects, Analyzer, which can be used to screen and organize data, and 
a (proposed and not currently functioning) subclass, Visualizer, that is used when information is to be 
printed to the screen. Since it is a subclass, it also has all the necessary analyzer functions. 
Mostly, the distinction is made based on logic, (so the functions are easier to find in this file) 
and because if you don't plan on visualizing, it doesn't make a lot of sense to call on something named 'Visualizer.' 
Made for Python 2 but should be ok for Python 3

UPDATES:

	2.26

	* can now be used for any state
	* can now handle filelists
	* can now navigate through directories: storing results in Analysis_Results and reading
		state data from (of course) state_data, which is a folder that should be preloaded into 
		the same folder as Analysis.py

''' 

from graphics import *							#drawing
import os, sys
import csv

class Analyzer(object):
	
	def __init__(self, kD=None, state='ia'):

		# This list and dictionary are now the default in the Analyzer. They do not need to be entered in a driver. 
		#	However, if the dictionary is updated, either do so in Analysis.py, or when initializing set kD= name of new dicitonary 
		#	where dictionary is the variable name of the updated dicitonary. The default state is Iowa, however when initalized, this state
		#	can be set to any state in the US by entering its two letter representation, (e.g. 'NY' = New York, 'IL' = Illinois, etc.) 	


		self._state = state.upper()
		self._statefilename = state +'.txt'
		self._keywordlist = []
		self._countyAmount = 1
		self._countiesList = self.read_in()
		self._homeDirectory = os.getcwd()

		if kD is None:
			self._keyworddictionary = dict([
			('clinton',["HillaryClinton", "Hillary2016", "Hillary", 'clinton', 'hilary']),
			('lessig',["Lessig", "Lessig2016", "Lessig2016"]),
			('o\'malley',["O'Malley", "OMalley2016", "MartinOMalley", 'omalley']),
			('sanders',["Bernie", "FeelTheBern", "Bernie2016", 'sanders']),
			('bush',["Jeb", "JebBush", "Jeb2016"]),
			('carson',["Carson", "BC2DC16", "RealBenCarson"]),
			('christie', ["Chris Christie", "Christie2016", "ChrisChristie"]),
			('cruz',["Cruz", "CruzCrew", "TedCruz"]),
			('cruz',["Fiorina", "Carly2016", "CarlyFiorina"]),
			('gilmore',["Jim Gilmore", "JimGilmore", "gov_gilmore"]),
			('graham',["Graham", "LindseyGraham", "LindseyGrahamSC"]),
			('huckabee', ["Huckabee", "ImWithHuck", "GovMikeHuckabee"]), 
			('jindal', ["Jindal", "BobbyJindal", "BobbyJindal"]), 
			('kasich', ["Kasich", "Kasich4Us", "JohnKasich"]), 
			('paul', ["Rand Paul", "RandPaul2016", "RandPaul"]), 
			('rubio', ["Rubio", "MarcoRubio", "Rubio2016"]), 
			('santorum', ["Santorum", "RickSantorum"]),
			('trump', ["Trump", "DonaldTrump2016", "realDonaldTrump"])])

		
		else:
			self._keyworddictionary = kD

		
		self._outerBounds = []  #this is the box that contains the state


		
		for key in self._keyworddictionary:
			for word in self._keyworddictionary[key]:
				self._keywordlist.append(word)
		
		self.normalize_list(self._keywordlist) #So capital letters, punctuation, and other things don't interfere.
		
		

	def read_in(self, filename=None):	

		#Description: This function reads in the state data and stores it in the form of a 3D Array for the other funtions to make use of.

		os.chdir("state_data")             #The state data is in this folder
		if filename is None:
			filename = self._statefilename


		counties = []	# a list of 2D arrays  (A 3D array? kind of?)
		bounds = []
		

		f = open(filename, 'r')	#open the file, prep for reading
		x = f.readline()
		x = x[1:-1]
		xsplit = x.split("   ")
		y = f.readline()
		y = y[1:-1]
		ysplit = y.split("   ")

		bounds.append(xsplit)	#the first lines of the text file are the maximums and minimums for the coordinates.
		bounds.append(ysplit)

		self._outerBounds = bounds[:]   #a copy of bounds is stored in the object

		self._countyAmount = int(f.readline())	#stores the number of counties in the state.

		f.readline() #clears \n

		for i in range (self._countyAmount):	#now the fun begins
			
			coord = [] #empties coord every run through

			county = f.readline()
			county = county.replace("\n","")
			f.readline()                       #gets rid of the state, we don't need this information.
			size = int(f.readline())           #confirmed has correct data. 


			for k in range(size+1):		      #creates a space for each pair PLUS one to hold the name, size of the county
				coord.append(k)

			a = []		#some placeholder lists
			b = []
			c = []

			for j in range(size):		        	#confirmed correct loop iterations
				
				a.append(f.readline())
				b = a[j].split("   ")			  #breaks up the coordinates for easier access later.
				b[0] = b[0].replace(" ","")       #trims the data of what we don't want
				b[1] = b[1].replace("\n","")
				coord[j+1] = (b)                   #replaces the placeholder value in coord to what we really want it to be

			c.append(county)
			c.append(size)

			coord[0] = c


			

			counties.append(coord) 

			f.readline() #eats the new line 

		

		f.close()  #closes the input file

		os.chdir("..")  #returns home.

		return counties  #an array

	def get_county_name(self, index, counties=None):   

		#Description: will return the string stored in each coord (the county name)

		if counties is None:
			counties = self._countiesList   #unless told otherwise, use the already stored data.
		if (index == self._countyAmount):    
			return 'Other'
	
		coord = counties[index]
		name = coord[0][0]

		return name
		
	'''
	def get_county_name(self, s, size, counties=None):

		if counties is None:
			counties = self._countiesList
		a = []
		for i in range(self._countyAmount):
			peint
			coord = counties[i]
			if coord[0][1] == size:
				a.append(coord[0][0])

		return a    #in case there is more than one county of that size

	'''
	def get_index(self, name, counties=None):

		#Description: will return the index number in the array when given a county name.

		if counties is None:
			counties = self._countiesList
		for i in range(self._countyAmount):

			coord = counties[i]
			if coord[0][0] == name:

				return i
		return -1


	def get_size(self, index, counties=None):	

		#Description: will return how many [x,y] coords for the specified county

		if counties is None:
			counties = self._countiesList

		coord = counties[index]
		size = coord[0][1]

		return size
	'''
	def get_size(self, name, counties=None): #using the name of the county as a parameter

		if counties is None:
			counties = self._countiesList

		for i in range (self._countyAmount):

			coord = counties[i]
			if coord[0][0] == name:
				return coord[0][1]

		return 0
	'''

	def normalize(self, token):

		#Description: this will get rid of any strange punctuation in a string.

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

		#Description: the same thing as normalize, but to a list instead of a single string.

		for word in list_a:
			word = self.normalize(word)

		return list_a

	def read_tweet(self, inputFile):  
		
		#Description: when given an already opened inputfile, will analyze a single tweet, putting into a list where each
		#				element is a different part of the tweet, e.g. time, retweets, message, followers, etc. (This is used by later functions)

		tweet = []  # a list, each element will be a different part of tweet data
		more_message = True		#message reading loopbreaker

		time = False   #whether or not the tweet is timestamped

		firstline = inputFile.readline()

		if not firstline: return tweet   #end of file error
		if "+0000" in firstline:			#all these tweets are in GMT. If that changes, so does this. 
			time = True
			tweet.append(firstline)
			firstline = inputFile.readline()
			
		while more_message:

			
			check_message_done = inputFile.readline()	#peeks at the second line

			if 'Retweets: ' in check_message_done:		#if the message was only one line

				tweet.append(firstline)
				tweet.append(check_message_done)
				more_message = False				#loopbreaker

			else:

				firstline = firstline + check_message_done  #add to the firstline (message) and continue loop


		while True:		

			line = inputFile.readline()		#this loops reads the rest of the tweet data and stores each
			if line == "\n": break          #line (retweet #, followers, location etc)
			if not line:					#EoF
				more_text = False
				break		            	#breaks outer loop
				
			tweet.append(line)


		return tweet


	def screen_keywords(self, datedfilename, keywords_list=None, notify=False):

		#Description: this will read the data of a collected tweet file, grab the ones that concern the candidates, and
		#             copy them into a new text file with the prefix "screened_keywords_". It returns this new file name.

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
		if notify:
			print ("Screened for keywords.")  #notify will tell you when it completes this process. Good for debugging or monitoring.

		inputFile.close()
		outputFile.close()

		return new_file_name  #the name of the created file

	def screen_coord(self, datedfilename, notify=False):		

		#Description: takes in a collected tweet file, reads it, and copies the tweets that are geotagged into a new text file
		#				with the prefix "screened_location_". It returns this new file name.

		inputFile = open(datedfilename, 'r')

		new_file_name = "screened_location_"+ datedfilename

		outputFile = open(new_file_name, 'w')

		while True:

			text = self.read_tweet(inputFile)
			if not text: break
			c = text[-1]                #the last element is the coordinates	
			text.append('\n')       	#prettier when it prints
			if 'Coordinates' not in c:
				c = text[-2]
			
			if ("u'type': u'Point', u'coordinates'") in c:		#if there are coordinates to track
			
				               
				for i in range(len(text)):
					outputFile.write(text[i])   #saving the good tweets to a new .txt file
		if notify:
			print ("Screened for usable coordinates.") #notify will tell you when it completes this process. Good for debugging or monitoring.

		inputFile.close()
		outputFile.close()

		return new_file_name  #return the new file name.


	def double_screen(self, datedfilename, keywords_list=None, notify=False): 

		#Description: this will screen the file for relevant tweets that are also geotagged, copy them into
		#				a text file with the prefix "screened_", and then return the new file name. 

		if keywords_list is None:
			keywords_list = self._keywordlist
			new_file_name = self.screen_keywords(self.screen_coord(datedfilename, notify=notify), notify=notify)
		else:
			new_file_name = self.screen_keywords(self.screen_coord(datedfilename, notify=notify), keywords_list=keywords_list, notify=notify)

		os.rename(new_file_name, "screened_"+datedfilename)

		return ("screened_"+datedfilename) #a string

	def combine_files(self, filelist, new_name):

		#Description: this will take in a list of files and copy the contents of each one into the same output file.
		#				this is useful for recombining files that were split up. 

		output = open(new_name, 'w')

		for f in filelist:
			inputfile = open(f, 'r')
			text = inputfile.read()
			output.write(text)
			inputfile.close()

		output.close()
		return new_name #a string

	def screen_and_combine(self, filelist, new_name, keywords_list=None, notify=False):

		#Description: this will use both double_screen and combine_files on a filelist

		return (self.double_screen(self.combine_files(filelist, new_name), keywords_list=keywords_list, notify=notify))

	def dictionary_to_scores(self, dictionary=None, names=True):  #FIXED

		#Description: this will take in a keywords dictionary where the keys are the candidate names, and produces a new
		#				dictionary where instead of keywords, there is a list with an element for each county in the state.
		#				This will later be filled with the data in tally_scores

		ca = self._countyAmount

		if dictionary is None:
			dictionary = self._keyworddictionary.copy()

		s = []   # a list to hold the scores, to be assigned to each key in the dictionary
		scores = dictionary.copy()		#new dictionary
		for key in scores:
			
			for i in range(ca+1):			#placeholder for each county in Iowa plus one for those not in coordinates
				s.append([0])
				if names:
					s.append(self.get_county_name(i))

			scores[key] = s   
			s = []

		return scores  #a dictionary

	def get_coordinates(self, tweet): 

		#Description: takes in whole tweet (as a list) and returns the coordinates. If not geotagged, it returns zeros, which
		#				will result in the county option "Other"

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

		
		return coordinates  #A list of two float values


	def point_inside_polygon(self, x,y,poly):

		#Description: this program will determine if a set of points is inside of a polygon. This is usually used in 
		#				visualization, however we are using it to help determine which county a geotagged tweet comes from.

	    n = len(poly)
	    for i in range (n):
	    	poly[i][0] = float(poly[i][0])
	    	poly[i][1] = float(poly[i][1])

	    inside = False

	    p1x,p1y = poly[0]       
	   
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
	    
	    return inside #True/False

	def find_county(self, coordinates, county_list=None): 

		#Description: takes in county_list, which is a list of all counties and their coordinates, and coordinates which is
		#				a list of two float values to determine which county contains these coordinates. This uses 
		#				point_inside_polygon.

		
		if county_list is None:
			county_list = self._countiesList[:]
		

		x = float(coordinates[0])
		y = float(coordinates[1])

		foundit = False

		if y == 0.0 and x == 0.0:		  #if not in the counties
			return [self._countyAmount, 'Other']
		
		for i in range (self._countyAmount):

			county = county_list[i]
			name,size = county[0]
			
			foundit = self.point_inside_polygon(x, y, county[1:])

			if foundit:
				return [i, name]          #the index and name string of the county

		return[self._countyAmount, 'Other'] #If it is not in any of the counties, it stores the data in "Other"

		
	


	def tally_scores(self, filelist, dictionary=None, names=True, notify=False):   
		
		#Description: this creates a score dictionary (see dictionary_to_scores) and then opens the input file(s) and determines
		#				which candidate each tweet is about and which county it originates from, then returns the dictionary of
		#				this information. Names is asking whether or not you want the name of each county to also be stored. 
		#				Leaving it as true will make this dictionary easier to read for states that have many counties (Iowa has 99!). Notify
		#				will let you know (if it is a filelist) what file it is currently taking care of (1 file, 2 file, etc.)


		i=0

		if dictionary is None:
			dictionary = self._keyworddictionary.copy()
		
		score_dictionary = self.dictionary_to_scores(dictionary=dictionary, names=names) 
		
		if isinstance(filelist, str):	#checks to see how many files it is working with
			new_list = [filelist]
			filelist = new_list

		if isinstance(filelist, list):
			for filename in filelist:
				inputFile = open(filename, 'r')
				i += 1


				while True:

					tweet = self.read_tweet(inputFile)		#read each tweet
					if not tweet: break

					text = tweet[1]
					
					coordinates = self.get_coordinates(tweet)  #where is the tweet from

					for key in dictionary:
						
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
				if notify:
					print i, " files analyzed."
			return score_dictionary
		else:
			print("Wrong input type for tally_scores")
			return

	def make_file_list(self, month, year=2016):

		#Description: this will combine all text files with dated filenames that match the month and the year given. 
		#				It only looks for the input files in the current working directory.

		filelist = []

		month_string = str(month)
		if len(month_string) == 1:
			month_string = "0"+month_string
		year_string = str(year)

		for filename in os.listdir(os.getcwd()):

			if month_string in filename[:2] and year_string in filename[6:10]:
				filelist.append(filename)

		return filelist 	#a list of the filenames (strings)

	def check_if_filtered(self, filename):  

		#Description: this is for seeing how accurate the streaming is. It will see how many of the tweets are actually 
		#				in the correct state, and return it in terms of [ #  in the state, # not in the state]

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
				yes_no[0] += 1 			#if the coordinates are in iowa, yes
			else:
				yes_no[1] += 1  		#if not, no

		inputFile.close()
		return yes_no    #returns [how many in, how many out]

	'''
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

		red, blue = candidates
		

		redblue = []

		red_chatter = self.chatter(red, filename, dictionary)
		blue_chatter = self.chatter(blue, filename, dictionary)

		redblue.append(red_chatter)
		redblue.append(blue_chatter)

		return redblue
	'''

	def write_csv(self, destination, inputFile, group_by="candidate", text=True, score=True, county_names=False, score_tally=None, labels=True, notify=False):

		#Description: this is the major function. It takes in an input file/filelist and writes a csv or tsv file 
		#				(see tally_scores for a deeper explanation of exactly what/how things are scored). The defaulted
		#				parameters are as follows: group_by,     will determine the vertical axis. Defaulted to candidate, can also be "county"
		#										   county_names, will write the names of each county with its score. Can be an eyesore, but useful for reading in
		#										   labels,       will print the ordered county names or the ordered candidates (the candidate label is recommended when
		#															organizing by county, as dictionaries are not ordered, and the candidates can appear in any order)
		#										   notify,		 will notify you when the output file has been written. 

		ca = self._countyAmount
		output_type = destination[-4:]

		if score_tally is None:
			score_tally = self.tally_scores(inputFile, names=county_names)
			

		if "Analysis_Results" in os.listdir(os.getcwd()):
			os.chdir("Analysis_Results")
		elif os.getcwd() == "Analysis_Results":
			pass
		else:
			os.mkdir("Analysis_Results")
			os.chdir("Analysis_Results")

		with open(destination, 'wb') as csvfile:

			if output_type=='.tsv':
		
				outputFile = csv.writer(csvfile, delimiter='\t')

			elif output_type=='.csv':

				outputFile = csv.writer(csvfile)
			else:
				print "Only .csv and .tsv output supported currently"
				return


			if group_by=="candidate":

				if labels:
					labels_list = []
					labels_list.append("Candidate")
					labels_written = False

				
				for key in score_tally:
					
					if labels:
						if labels_written==False:
							#for key in score_tally:
							for i in range(ca+1):
								if county_names:
									labels_list.append("")
									#if (i<self._countyAmount):
									labels_list.append(score_tally[key][i][1])

								if not county_names:
									if (i < self._countyAmount):
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

				for i in range(ca+1):
					flipped_tally.append([])
					

				
				for key in score_tally:
					labels_list.append(key.title())

					for j in range(ca+1):
						  
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

		os.chdir('..') 
		if notify:
			print destination, " created."
		return destination

	def csv_convert(self, inputFile, output=None):

		#Description: will take in a .csv or .tsv file and convert it to the other format. Unless an output name is given,
		#				it will just keep the same name as the original and just change the extension at the end.

		if os.getcwd() == self._homeDirectory:
			os.chdir("Analysis_Results")
			

		filetype = inputFile[-4:]
		if output is None:
			name1 = inputFile[:-4]+".csv"
			name2 = inputFile[:-4]+".tsv"
		else:
			name1, name2 = output, output

		if filetype == '.csv':
			csv.writer(file(name2, 'w+'), delimiter='\t').writerows(csv.reader(open(inputFile)))
		elif filetype == '.tsv':
			csv.writer(file(name1, 'w+')).writerows(csv.reader(open(inputFile), delimiter='\t'))

class Visualizer(Analyzer):

	'''
	   This is a proposed and incomplete subclass of Analyzer. The functions defined below are broken, and though are
	   are close to working, do not at the current time. Possibly will be fixed, possibly will just be deleted. We'll see.
	'''	
	def __init__(self, kD=None, state="IA"):

		super(Visualizer, self).__init__(kD=kD, state=state)
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
		#-90.13self._countyAmount38   43.500713
		bounds = self._outerBounds[:]
		#Note: this assumes (0,0) is the bottom right corner, and (max x, max y) is top left

		width_min = float(bounds[1][0])*-1
		height_min = float(bounds[0][1])

		width_max = float(bounds[0][0])*-1
		height_max = float(bounds[1][1])

		widthC = width_max - width_min
		heightC = height_max - height_min

		ratio_w = widthC / (800)		#every pixel is ___ degrees	
		ratio_h = heightC / (500)

	

		size = county[0]			#fetching the name and size of each county
		size = size[1]
		name = county[0]
		name = name[0]

		new_points = []

		for i in range(size):

			k = i+1
			px = int((width_max - (float((county[k][0]))*-1))/ratio_w)		#converting degees to pixels. NEED TO FIX FORMULA //FIXED :D

			
			py = int((height_max - (float(county[k][1])))/ratio_h)
			
			#each element new_points is a Point(px,py)


			#print py
			p = Point(px, py)			
			#p.append(px)
			#p.append(py)
			new_points.append(p)

		return new_points

	def draw_county(self, new_points, color, window): #NOTE the data needs to be converted before this function is used

		county = Polygon(new_points)
		
		county.setFill(color)
		county.draw(window)

	def gen_color(self, red, blue):

		red = float(red)
		blue = float(blue)
		
		R = int((red/(red+blue))*255)
		B = int((blue/(red+blue))*255)
		
		
		RGB = color_rgb(R, 0, B)

		return RGB

if __name__ == '__main__':

	print("No main() yet :) sorry. Use Driver.py")
	

	









	


		







