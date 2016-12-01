#! /bin/python
""" Feed Binary With Inputs
	./feed.py binary input-file script
"""

#TODO specifiy number of feedings

import getopt
import os
import subprocess
import sys

import parser
import tcfparser
from common import *

logger = getlogger('feed')

def compare(aout, bout, silence=False):
	if not silence:
		print aout
		print bout
	print "Same" if aout == bout else "Different"

def feed(excute, data):
	out = output("echo '%s' | %s"%(data, excute))
	return out

def progfeed(conf):
	excute = conf.get(CONFIGS_FEED, CONFIG_FEED_EXCUTE)
	input_file = conf.get(CONFIGS_FEED, CONFIG_FEED_INPUT_FILE)
	count = conf.get(CONFIGS_FEED, CONFIG_FEED_COUNT)
	pattern = conf.get(CONFIGS_FEED, CONFIG_FEED_PATTERN)

	count = parser.rgparser(count)

	cases = tcfparser.parse(input_file, pattern)
	cid = 0
	print
	try:
		for case in cases:
			cid += 1
			if cid not in count:
				continue
			print "Test Case #%d"%cid
			cutoff("input")
			case = "\n".join(case)
			print case
			cutoff("output")
			out = feed(excute, case)
			print out
			print
	except IOError as e:
		errquit(str(e), logger)

def configurations():
	current = "progfeed.conf"
	home = config.get("DEFAULT", "home")
	default = os.path.join(home, "etc/progfeed-default.conf");
	return current, default

def main(argv):
	# we load the configuration file first
	# because we need't know anything about
	# the sourefile name and 
	current, default = configurations()
	feedconfig = getconfig(current, default)
	configkeys = [x[0] for x in feedconfig.items("progfeed")]

	opts, args = getopt.gnu_getopt(argv, "s:", ["set="])

	modes = [x[0] for x in opts]
	settingmode = "-s" in modes or "--set" in modes
	runningmode = not settingmode

	for opt, arg in opts:
		if opt in ("-s", "--set"):
			settingmode = True
			k, v = parser.eqtparser(arg)
			if k not in configkeys:
				print "** unknown key: %s"%k
				continue
			feedconfig.set("progfeed", k, v)

	printconfig(feedconfig)

	if settingmode:
		assert not runningmode
		with open("progfeed.conf", "w") as conffile:
			feedconfig.write(conffile)
			print "Configuration file written."

	if runningmode:
		assert not settingmode
		progfeed(feedconfig)
	
if __name__ == '__main__':
	cutoff("progfeed - easyprog-%s"%VERSION)
	import logging
	#logger.setLevel(logging.DEBUG)
	#tcfparser.logger.setLevel(logging.DEBUG)
	main(sys.argv[1:])
