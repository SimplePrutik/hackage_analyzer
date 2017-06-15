import glob, os, re

build_depends_pattern = '(b|B)uild-(d|D)epends:?(\s*((\w|-)*)[ 0-9.<>=&|]*,)*\s*((\w|-)*)'
b_len = 13

tree = os.walk('../hackage/') 
for d, dir, files in tree:
	for f in files:
		if (f.endswith('.cabal')):
			file = open(d + '/' + f, 'r').read()
			file = re.sub(re.compile("--.*?\n" ) ,"" ,file)
			deps = re.search(build_depends_pattern, file)
			while (deps):
				depends = deps.group()[b_len + 1:]
				deps_ = re.findall('[A-Za-z-]+', depends)
				print(deps_)
				file = file[deps.start() + 1:]
				deps = re.search(build_depends_pattern, file)