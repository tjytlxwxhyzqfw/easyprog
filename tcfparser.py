#! /bin/python

"""Test Case File Parser v0.01

Parse continuous test cases in a single file into separated ones.

This script reads the first line of each case and use this line to
determine the number of lines that the case occupies, then output
the whole case and read the next one.

Usage:
	./tcfparser.py [-d|--debug-info] path script
	./tcfparser.py [-h|--help] [-v|--version]

Arguments:
	path: Path to the test case file
	script: A mathematical expression yielding a positive integer
		which indicates the number of lines in the current case.

		Use [<number>] to reference numbers in the first line of the case.

Example:
	tcfparser Inputs/0000 2+#2
"""

import getopt
import logging
import os
import re
import sys

from common import *

VERSION = 'v0.01'
logger = getlogger('tcfparser')

class Interpreter(object):
	""" Script interpreter
	"""
	def __init__(self, script):
		
		self.script = script
		logger.debug("script: %s"%script)
		self.addends = re.split(r'\s*\+\s*', script)
		logger.debug("addends: %s"%self.addends)

		self.constant = False
		self.constval = None
		if re.search(r'\[\d+\]', self.script) == None:
			self.constant = True
			self.constval = self.__call__([])
			logger.info("const expression: %d", self.constval)

	def __call__(self, args):
		n = 0
		for x in self.addends:
			if x.startswith("["):
				try:
					assert x.endswith("]")
				except AssertionError:
					logger.error("unknown symbol '%s'"%x)
					sys.exit(1)
				n += int(args[int(x[1:-1])-1])
			else:
				n += int(x)
		return n

	def __str__(self):
		return self.script

def parse(path, script):
	""" Parse a test case file into seperated cases

	Args:
		path: Path to test case file
		getnlns: 
	"""
	lns = fread(path)
	cal = Interpreter(script)
	current, nlns = 0, len(lns)

	if cal.constval == 0:
		yield lns
	else:
		while current < nlns:
			first = re.split(r'\s+', lns[current])
			n = cal(first)
			if current + n > nlns:
				logger.warning("unexpected end of test case file: %s"%path)
				break
			yield lns[current:current+n]
			current += n
		
def parseopt(argv):
	opts, args = getopt.getopt(argv, 'dhv', ['debug-info', 'help', 'version'])
	for opt, arg in opts:
		if opt in ('-d', '--debug-info'):
			global logger
			logger.setLevel(logging.DEBUG)
		if opt in ('-h', '--help'):
			print __doc__
			return None, None
		if opt in ('-v', '--version'):
			print VERSION
			return None, None
	logger.debug("args: %s"%args)
	return args

def main(argv):
	try:
		path, script = parseopt(argv)
	except ValueError:
		#print __doc__
		return

	if path == None and script == None:
		return

	logger.debug("path: %s"%path)
	logger.debug("script: %s"%script)

	cases = parse(path, script)
	for case in cases:
		print "\n".join(case)
		print

if __name__ == '__main__':
	main(sys.argv[1:])
