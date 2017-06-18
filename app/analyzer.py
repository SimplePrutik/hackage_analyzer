import glob, os, re, tarfile, shutil, codecs
import errno, stat

def onerror(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


build_depends_pattern = '(b|B)uild-(d|D)epends:?(\s*(\w|-)+([0-9.<>=&|*]|\s)*,)*\s*(\w|-)+'
imported_modules_pattern = 'import\s+(?:qualified )?(?:([a-zA-Z-_]+)\.)'
extentions_pattern = '\{-#\s*LANGUAGE\s+(\S+)\s*#-\}'

b_len = 13
tar_err = []
walk_err = []
read_err = []
delete_err = []


debug = open('debug.log', 'w')
dependencies = open('dependencies.log', 'w')
modules = open('modules.log', 'w')
extensions = open('extensions.log', 'w')

count = 0

tree = os.walk('../hackage/') 
for d, dir, files in tree:
    for f in files: 
        try:
            tar = tarfile.open('../hackage/' + f)
            tar.extractall()
        except:
            tar_err.append(f)
        arch = f[:-7] + '/'
        try:
            sub_tree = os.walk(arch)
        except:
            walk_err.append(f)
        for _d, _dir, _files in sub_tree:
            all_deps = []
            all_modules = []
            all_ext = []
            for _f in _files:
                if (_f.endswith('.cabal')):
                    debug.write('############################\n')
                    debug.write(_f + '\n')
                    try:
                        file = codecs.open(_d + '/' + _f, 'r', 'utf-8').read()
                        file = re.sub(re.compile("--.*?\n" ) ,"" ,file)
                        deps = re.search(build_depends_pattern, file)
                        while (deps):
                            depends = deps.group()[b_len + 1:]
                            deps_ = re.findall('[A-Za-z0-9-]*[A-Za-z]+[A-Za-z0-9-]*', depends)
                            for _deps in deps_:
                                all_deps.append(_deps)
                                debug.write(_deps + '\n')
                            file = file[deps.start() + 1:]
                            deps = re.search(build_depends_pattern, file)
                        unique = set(all_deps)
                        dependencies.write(arch + ' ')
                        for _deps in unique:
                            dependencies.write(_deps + ' ')
                        dependencies.write('\n')
                    except:
                        read_err.append(f)
                if (_f.endswith('.hs')):
                    try:
                        file = codecs.open(_d + '/' + _f, 'r', 'utf-8').read()
                        file = re.sub(re.compile("--.*?\n" ) ,"" ,file)
                        _file = file
                        mods = re.search(imported_modules_pattern, file)
                        while (mods):
                            module = mods.group(1)
                            all_modules.append(module)
                            # print(module)
                            file = file[mods.start() + 1:]
                            mods = re.search(imported_modules_pattern, file)
                        exts = re.search(extentions_pattern, _file)
                        while (exts):
                            ext = exts.group(1)
                            all_ext.append(ext)
                            _file = _file[exts.start() + 1:]
                            exts = re.search(extentions_pattern, _file)
                    except:
                        read_err.append(f)  
        unique = set(all_modules)
        # print(all_modules)
        # print(unique)
        modules.write(arch + ' ')
        for mods in unique:
            modules.write(mods + ' ') 
        modules.write('\n')
        unique = set(all_ext)
        # print(all_ext)
        extensions.write(arch + ' ')  
        for ext in unique:
            extensions.write(ext + ' ')
        extensions.write('\n')
        tar.close()
        try:
            shutil.rmtree(arch, ignore_errors=False, onerror=onerror)
        except:
            delete_err.append(f)
            continue

debug.write('\n\n###############\n\nTar error packages:\n\n')
for er_pkg in tar_err:
    debug.write(er_pkg)

debug.write('\n\n###############\n\nWalk error packages:\n\n')
for er_pkg in walk_err:
    debug.write(er_pkg)

debug.write('\n\n###############\n\nRead error packages:\n\n')
for er_pkg in read_err:
    debug.write(er_pkg)

debug.write('\n\n###############\n\nDelete error packages:\n\n')
for er_pkg in delete_err:
    debug.write(er_pkg)