#Jenny Steffens

from Analysis import *
import random, time

def main():

	
		
	
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

	v = Analyzer(keyword_dictionary)
	
	print (v.write_csv("Testing321.csv", v.screen_coord("28-01-2016.txt"))) 
	print (v.write_csv("Testing123.csv", v.screen_coord("28-01-2016.txt"), group_by="county")) 
	
	print "done"







































	'''
	f
	filelist.append(v.double_screen("26-01-2016.txt", keyword_list))
	filelist.append(v.double_screen("27-01-2016.txt", keyword_list))
	filelist.append(v.double_screen("28-01-2016.txt", keyword_list))
	filelist.append(v.double_screen("29-01-2016.txt", keyword_list))
	#v.screen_keywords("27-01-2016.txt", keyword_list)
	
	
	rb = v.red_blue_chatter(['trump','clinton'], filelist, keyword_dictionary)
	
	for county in range(99):

		c = v.create_points(county_list[county])
		#print c
		a = v.get_size(county_list, county)

		red = rb[0]['trump'][0][county]
		blue = rb[1]['clinton'][0][county]
		print red
		print blue, "\n"
		#bloop = v.gen_color(red, blue)
		

		##print y
		
			
	   # v.draw_county(c, bloop, test)

	
	#delete county_list

	#print(name)
	
	#v.set_menu("testing", 0, 5)
	test.getMouse()
	test.close()
	'''
	




main()