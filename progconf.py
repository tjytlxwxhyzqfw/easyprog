#! /bin/python
import getopt
import os
import re
import sys

from common import *

logger = getlogger("progconf")

# template name formatter
TEM_NM_FMT = "%s.%s.tem"

def replace(source, kvpairs, fromfile=False):
	max_replacing_times = 3
	if fromfile:
		source = fcont(source)
	for i in range(max_replacing_times):
		for key, val in kvpairs:
			source = source.replace(key, val)

	# check for circular dependencies
	try:
		unresolved = []
		for key, val in kvpairs:
			if key in source:
				unresolved.append(key)
		assert not unresolved
	except:
		print "Unresoved placeholders: %s"%unresolved

	return source

def configurations(name, lang):
	first = "./progconf.conf"
	home = config.get("DEFAULT", "home")
	second = os.path.join(home, "etc/%s.conf"%lang)
	return first, second

# configuration file of `progconf` must contains
# a (single) section named by using language:
# for example:
# --- progconf.conf ---
# [py]
# excute: xxx
# target: xxx
# --- end --

def main(argv):
	opt_with_template = False

    	opts, args = getopt.gnu_getopt(argv, "t", ["with-template"])
	for k, v in opts:
		if k in ("-t", "--with-template"):
			opt_with_template = True	

	#print "args: %s"%args

	assert len(args) == 1
	name, lang = args[0].split(".")

	# current and default configuration files 
	current, default = configurations(name, lang)
	confconfig = getconfig(current, default)

	# '{}' might be used for reference to the program name,
	# and we replace it now since we have got both the program name
	# and the configration file so far.
	for k, v in confconfig.items(lang):
		confconfig.set(lang, k, v.replace("{}", name))

	#logger.debug("confconfig:")
	#printconfig(confconfig)
	#print "end - confconfig"

	# we must specify name and language for configuring .conf file,
	# for that the default configuration file has no idea with
	# the source file currently used by us.
	kvpairs = [("<NAME>", name), ("<LANG>", lang)]
	for k, v in confconfig.items(lang):
		kvpairs.append(("<%s>"%k.upper(), v))
	#print "kvpairs: %s"%kvpairs

	temmk = config.get(CONFIGS_GENERAL, CONFIG_TEMPLATE_MAKE)
	strmk = replace(temmk, kvpairs, fromfile=True)
	fwrite(strmk, "Makefile")
	print "'Makefile' generated."

	if opt_with_template:
		temsrc = config.get(lang, CONFIG_LANG_TEMPLATE)
		strsrc = replace(temsrc, kvpairs, fromfile=True)
		temnam = TEM_NM_FMT%(name, lang)
		fwrite(strsrc, temnam)
		print "'%s' generated."%temnam

	print "'progconf.conf' generated:"
	printconfig(confconfig)

if __name__ == "__main__":
	print "progconf - easyprog-%s"%VERSION
	main(sys.argv[1:])
