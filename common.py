import ConfigParser
import logging
import subprocess
import sys

VERSION = "v0.01"

CONFIGS_GENERAL = "general"
CONFIGS_FEED = "progfeed"

CONFIG_TEMPLATE_MAKE = "template-makefile"

CONFIG_LANG_COMPILE = "compile"
CONFIG_LANG_EXCUTE = "excute"
CONFIG_LANG_TARGET = "target"
CONFIG_LANG_TEMPLATE = "template"

CONFIG_FEED_EXCUTE = "ex"
CONFIG_FEED_INPUT_FILE = "if"
CONFIG_FEED_COUNT = "ic"
CONFIG_FEED_PATTERN = "pat"

def getconfig(path):
	config = ConfigParser.ConfigParser()
	config.read(path)
	return config

def printconfig(conf):
	for sec in conf.sections():
		print "[%s]"%sec
		for key, val in conf.items(sec):
			print "%-16s = %-s"%(key, val)

def errquit(msg, logger):
	logger.error(msg)
	sys.exit(1)

def cutoff(msg):
	print "--- %s --->"%msg

def output(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
	return p.communicate()[0].strip()

def fwrite(string, path):
	fil = open(path, "w")
	fil.write(string)
	fil.close()

def fread(path, raw=False):
	""" Convert a text file into a list of lines
	Args:
		path: Path to the target file
		raw: Lines remain the original form
	Returns:
		A list object consisting of lines in target file.
	"""

	inf = open(path, "r")
	lns = [x for x in inf]
	inf.close()
	if not raw:
		lns = [x.strip() for x in lns]
		lns = filter(lambda x: x, lns)
	return lns

def fcont(path):
	return "".join(fread(path, raw=True))

def getlogger(name):
	logger = logging.getLogger(name)

	loghandler = logging.StreamHandler()
	logformatter = logging.Formatter('%(asctime)s %(filename)s: %(funcName)s: %(lineno)d %(levelname)s %(message)s')
	loghandler.setFormatter(logformatter)

	logger.addHandler(loghandler)
	logger.setLevel(logging.INFO)

	return logger

config = getconfig("/home/wcc/Exhibition/easyprog/etc/easyprog.conf")

