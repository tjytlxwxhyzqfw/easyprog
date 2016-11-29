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


def loadconfig():
	if os.path.exists("progfeed.conf"):
		print "Use ./progfeed.conf"
		feedconfig = getconfig("progfeed.conf")
	else:
		path = os.path.join(config.get("DEFAULT", "home"), "etc/progfeed-default.conf")
		print "Use default: %s"%path
		feedconfig = getconfig(path)
		print "Defalt configuration file loaded."
	return feedconfig

def main(argv):
	feedconfig = loadconfig()
	opts, args = getopt.gnu_getopt(argv, "s:", ["set="])

	modes = [x[0] for x in opts]
	settingmode = "-s" in modes or "--set" in modes
	runningmode = not settingmode

	for opt, arg in opts:
		if opt in ("-s", "--set"):
			settingmode = True
			k, v = parser.eqtparser(arg)
			feedconfig.set("progfeed", k, v)

	printconfig(feedconfig)

	if settingmode:
		assert not runningmode
		print "Settings: "
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
