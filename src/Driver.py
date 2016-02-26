#Jenny Steffens

from Analysis import *
import random, time



def main():

	
	# This list and dictionary are now the default in the Analyzer. They
	# do not need to be entered in a driver. However, if the dictionary is updated,
	# either do so in Analysis.py or when initializing, set kD= name of new dicitonary 
	# dictionary is the variable name of the updated dicitonary	

	keyword_list = ["HillaryClinton", "Hillary2016", "Hillary",
	"Lessig", "Lessig2016", "Lessig2016",
	"O'Malley", "OMalley2016", "MartinOMalley",
	"Bernie", "FeelTheBern", "Bernie2016",
	"Jeb", "JebBush", "Jeb2016",
	"Carson", "BC2DC16", "RealBenCarson",
	"Chris Christie", "Christie2016", "ChrisChristie",
	"Cruz", "CruzCrew", "TedCruz",
	"Fiorina", "Carly2016", "CarlyFiorina",
	"Jim Gilmore", "JimGilmore", "gov_gilmore",
	"Graham", "LindseyGraham", "LindseyGrahamSC", 
	"Huckabee", "ImWithHuck", "GovMikeHuckabee", 
	"Jindal", "BobbyJindal", "BobbyJindal", 
	"Kasich", "Kasich4Us", "JohnKasich", 
	"Rand Paul", "RandPaul2016", "RandPaul", 
	"Rubio", "MarcoRubio", 
	"Santorum", "RickSantorum", 
	"Trump", "DonaldTrump2016", "realDonaldTrump"]

	keyword_dictionary = dict([
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

	start_time = time.time()  #let's see the runtime of this


	v = Analyzer(state='NH') #the state here is New Hampshire


	filelist = v.make_file_list(02)  #tweet files for the month of February


	f = v.screen_and_combine(filelist, "february.txt", notify=True)

	# this will return the new name, in this case, "february.txt," of the output file, a combination of all the files
	# 	in filelist. Notify simply prints to the console when the file is screened

	# Demonstrating how one would call the functions. 

	a = v.write_csv("FebCandidate.csv", f, county_names=False, notify=True)
	b = v.write_csv("FebCandidate.tsv", f, county_names=False, labels=False)
	c = v.write_csv("FebCounty.csv", f, county_names=False, labels=False, group_by="county", notify=True)
	d = v.csv_convert("FebCounty.csv")




	
	print "New files: ", a,b,c
	print "done"
	
start_time = time.time()

main()

print("--- completed in %s seconds ---" % (time.time() - start_time))






































