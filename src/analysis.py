def normalize(token):
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

f = open("output.txt", 'r')
tokens = f.read().split(" ")

normalized_text = []

for i in tokens:
    i = normalize(i)
    normalized_text.append(i)

print(normalized_text)

#Democrats
hillary =  []
omalley =  []
bernie =   []

#Republicans
trump =    []
jeb =      []
randpaul = []
santorum = []
christie = []
carson =   []
carly  =   []
cruz   =   []
huckabee = []
graham  =  []

for word in normalized_text:
    if word == "hillary" or word == "hillaryclinton" or word == "hillary2016" or word == "hillyes" or word == "hillary clinton":
        hillary.append(word)
    elif word == "trump" or word == "donaldtrump" or word == "trump2016" or word == "realDonaldTrump":
        trump.append(word)
    elif word == "bernie" or word == "berniesanders" or word == "feelthebern" or word == "berniesanders2016" or word == "sanders":
        bernie.append(word)
  elif word == "o'malley" or word == "omalley" or word == "omalley2016" or word == "martinomalley":
        omalley.append(word)
  elif word == "jeb" or word == "jebbush" or word == "jeb2016":
        jeb.append(word)
  elif word == "carson" or word == "bc2dc16" or word == "realbencarson" or word == "carson2016":
        carson.append(word)
  elif word == "cruz" or word == "cruzcrew" or word == "tedcruz" or word == "cruz2016":
        cruz.append(word)
  elif word == "kasich" or word == "kasich4us" or word == "johnkasich" or word == "kasich2016":
        kasich.append(word)
  elif word == "randpaul" or word == "randpaul2016" or word == "rand paul":
        randpaul.append(word)
  elif word == "fiorina" or word == "carly2016" or word == "carlyfiorina" or word == "carly fiorina":
        carly.append(word)
  elif word == "chris christie" or word == "christie2016" or word == "chrischristie":
        christie.append(word)
  elif word == "jim gilmore" or word == "jimgilmore" or word == "gov_gilmore" or word == "gilmore2016":
        gilmore.append(word)
  elif word == "graham" or word == "lindseygraham" or word == "lindsey graham" or word == "lindseygrahamsc":
        graham.append(word)
  elif word == "huckabee" or word == "imwithhuck" or word == "govmikehuckabee" or word == "huckabee2016":
        huckabee.append(word)
  elif word == "pataki" or word == "georgepataki" or word == "governorpataki" or word == "pataki2016":
        pataki.append(word)
  elif word == "rubio" or word == "marco rubio" or word == "rubio2016":
        rubio.append(word)
  elif word == "santorum" or word == "ricksantorum" or word == "rick santorum" or word == "santorum2016":
        santorum.append(word)

#print(hillary)
#print(trump)
#print(bernie)

total = len(bernie) + len(hillary) + len(trump)

percentb = len(bernie)*100 / total 
percenth = len(hillary)*100 / total
percentt = len(trump)*100 / total

print("Hillary: ")
print(percenth)
print("Bernie: ")
print(percentb)
print("Trump: ")
print(percentt)
