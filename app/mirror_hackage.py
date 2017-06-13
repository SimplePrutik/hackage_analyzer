import requests
import urllib.request
import json
import re
import os

r = requests.get("https://hackage.haskell.org/packages/.json")
packages = json.loads(r.text)

if not os.path.exists('../hackage/'):
    	os.makedirs('../hackage/')

for pkg in packages:
	try:
		cabal = (requests.get("https://hackage.haskell.org/package/" + pkg['packageName'] + "/" + pkg['packageName'] + ".cabal")).text
	except:
		print("https://hackage.haskell.org/package/" + pkg['packageName'] + "/" + pkg['packageName'] + ".cabal")
		print(pkg['packageName'] + ' get_request couldnt be made')
	cabal = re.sub(re.compile("--.*?\n" ) ,"" ,cabal)
	try:
		version = re.search('(v|V)ersion\s*:?\s*(\d+(\.\d*)*)', cabal).group(2)
	except:
		print(pkg['packageName'] + ' smthg wrong with version')
	try:
		urllib.request.urlretrieve('https://hackage.haskell.org/package/' + pkg['packageName'] + '-' + version + '/' + pkg['packageName'] + '-' + version + '.tar.gz', '../hackage/' + pkg['packageName'] + '-' + version + '.tar.gz')
	except:
		print(pkg['packageName'] + ' download was interrupted')
		print('-----------------------------------------#')

	

	
