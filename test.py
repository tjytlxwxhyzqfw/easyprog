#! /bin/python
""" OJ Solution Test Tool
	./test.py binary input-file script
"""

import os
import subprocess
import sys

import tcfparser
from common import *

def cutoff(msg):
	print "--- %s --->"%msg

logger = getlogger('test')

def judge(aout, bout, silence=False):
	if not silence:
		print aout
		print bout
	if aout == bout:
		print "Ok"
		return True
	print "Wrong Answer"
	return False

def feed(prog, data):
	out = output("echo '%s' | ./%s"%(data, prog))
	return out

def main(argv):
	prog, path, script = argv
	print "prog: %s"%prog
	print "path: %s"%path
	print "script: %s"%script

	cases = tcfparser.parse(path, script)
	cid = 1
	print
	for case in cases:
		print "Test Case #%d"%cid
		cutoff("input")
		case = "\n".join(case)
		print case
		cutoff("output")
		out = feed(prog, case)
		print out
		print
		cid += 1

if __name__ == '__main__':
	main(sys.argv[1:])
