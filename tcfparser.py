"""Test Case File Parser

Parse continuous test cases in a single file into separated ones.

This script reads the first line of each case and use this line to
determine the number of lines that the case occupies, then output
the whole case and read the next one.
"""

import logging
import os
import re
import sys

from common import *

logger = getlogger('tcfparser')

def get_calculator(script):
	addends = re.split(r'\s*\+\s*', script)
	logger.debug("script: %s"%script)
	logger.debug("addends: %s"%addends)

	def calculate(items):
		total = 0
		for adden in addends:
			if adden.startswith("["):
				try:
					index = int(adden[1:-1])
					assert index > 0
					adden = items[index-1]
				except:
					errquit("error on parsing symbol '%s'"%adden, logger)				
			total += int(adden)
		return total

	return calculate

def parse(path, script):
	""" Parse a test case file into seperated cases

	Args:
		path: Path to test case file
		script: Script used to parse test case file
	"""
	lns = fread(path)
	cal = get_calculator(script)
	current, nlns = 0, len(lns)

	while current < nlns:
		first = re.split(r'\s+', lns[current])
		n = cal(first)
		if n == 0:
			yield lns[current:]
			break
		if current + n > nlns:
			logger.warning("unexpected end of test case file: %s"%path)
			break
		yield lns[current:current+n]
		current += n

def test(path, script):
	logger.setLevel(logging.DEBUG)
	cases = parse(path, script)
	for case in cases:
		print "%s\n"%case

if __name__ == "__main__":
	import sys

	path, script = sys.argv[1:]
	test(path, script)

