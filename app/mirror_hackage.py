import requests
import urllib.request
import json
import re

r = requests.get("https://hackage.haskell.org/packages/.json")
packages = json.loads(r.text)

# cabal = (requests.get("https://hackage.haskell.org/package/" + packages[0]['packageName'] + "/" + packages[0]['packageName'] + ".cabal")).text
# version = cabal.find('Version:')
# print(version)
# end_of_line = cabal.find('\n', version)
# print(end_of_line)
# ver_str = cabal[version:end_of_line]
# print(ver_str)
# digits = re.search('\d', ver_str)
# print(ver_str[digits.start():len(ver_str)])


# version = cabal[version + int(digits) : len(ver_str) - digits]

# print(version)
count = 0

for pkg in packages:
	cabal = (requests.get("https://hackage.haskell.org/package/" + pkg['packageName'] + "/" + pkg['packageName'] + ".cabal")).text
	version = cabal.find('ersion:')
	end_of_line = cabal.find('\n', version)
	ver_str = cabal[version:end_of_line]
	digits = re.search('\d', ver_str)
	version = ver_str[digits.start():len(ver_str)]
	print(pkg['packageName'])
	print('https://hackage.haskell.org/package/')
	print('https://hackage.haskell.org/package/' + pkg['packageName'])
	print('https://hackage.haskell.org/package/' + pkg['packageName'] + '-' + version)
	ggg = 'https://hackage.haskell.org/package/' + pkg['packageName'] + '-' + version
	print(ggg + '/' + pkg['packageName'])
	print(ggg	 + '/' + pkg['packageName'] + '-' + version + '.tar.gz')
	# print('https://hackage.haskell.org/package/' + pkg['packageName'] + '-' + version + '/' + pkg['packageName'] + '-' + version)
	# urllib.request.urlretrieve('https://hackage.haskell.org/package/' + pkg['packageName'] + '-' + version + '/' + pkg['packageName'] + '-' + version + '.tar.gz', 'hackage/' + pkg['packageName'] + '-' + version + '.tar.gz')
	count = count + 1
	if (count == 10):
		break

	

# urllib.request.urlretrieve('http://github.com/jonpetterbergman/bgmax/archive/master.zip', 'hackage/bgmax.zip')

# r = requests.get("https://hackage.haskell.org/package/bgmax/bgmax.cabal")
# print(r.text)