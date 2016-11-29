#! /bin/python
import getopt
import os
import re
import sys

from common import *

logger = getlogger("progconf")

# template name formatter
TEM_NM_FMT = "%s.%s.tem"
MAX_REPLACING_TIMES = 3

PLACEHOLDER = r'<[A-Z]*?>'

PH_NAME = "<NAME>"
PH_LANG = "<LANG>"
PH_TARGET = "<TARGET>"
PH_COMPILE = "<COMPILE>"
PH_EXCUTE = "<EXCUTE>"

def replace(source, dictionary, fromfile=False):
	if fromfile:
		source = fcont(source)
	for i in range(MAX_REPLACING_TIMES):
		for key, val in dictionary.items():
			source = source.replace(key, val)

	try:
		unresolved = re.findall(PLACEHOLDER, source)
		assert not unresolved
	except:
		print "Unresoved placeholders: %s"%unresolved

	return source

def generalph(name, lang):
	ph = {PH_NAME: name, PH_LANG: lang}
	ph[PH_COMPILE] = config.get(lang, CONFIG_LANG_COMPILE)
	ph[PH_EXCUTE] = config.get(lang, CONFIG_LANG_EXCUTE)
	ph[PH_TARGET] = config.get(lang, CONFIG_LANG_TARGET)
	return ph

def main(argv):
	opt_with_template = False

    	opts, args = getopt.gnu_getopt(argv, "t", ["with-template"])
	for k, v in opts:
		if k in ("-t", "--with-template"):
			opt_with_template = True	

	print "args: %s"%args
	name, lang = args[0].split(".")
	ph = generalph(name, lang)

	strmk = replace(config.get(CONFIGS_GENERAL, CONFIG_TEMPLATE_MAKE), ph, fromfile=True)
	fwrite(strmk, "Makefile")
	print "'Makefile' generated."

	info = {}
	for k, v in ph.items():
		info[k[1:-1]] = replace(v, ph)

	if opt_with_template:
		path = config.get(lang, CONFIG_LANG_TEMPLATE)
		info["--with-template"] = path
		strsrc = replace(path, ph, fromfile=True)
		temnam = TEM_NM_FMT%(name, lang)
		fwrite(strsrc, temnam)
		print "'%s' generated."%temnam

	print "\nDetails:"
	for k, v in sorted(info.items()):
		print "%32s: %-s"%(k, v)
	
	

if __name__ == "__main__":
	main(sys.argv[1:])
