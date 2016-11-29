import re

def despace(string):
	return re.sub(r"\s+", "", string)

# equation: (left)=(rght)
# left: [\w]+
# rght: .+
def eqtparser(equation):
	return equation.split("=", 1)

# ranges: single | range | ranges ","
# range: number "-" number|last
# single: number | last
# number: [1-9]\d*
# last: $
#
# Simple:
# 1, 3, 5-10	-----> [1, 3, 5, 6, 7, 8, 9, 10]
# 1-$		-----> [1, 2, 3, 4, 5, ..., 100]
RANGE_MAX = 100
def rgparser(ranges):
	ranges = despace(ranges)
	ranges = ranges.split(",")

	numbers = set()
	for ran in ranges:
		left, rght = ran, ran
		if "-" in ran:
			left, rght = ran.split("-")
		if rght == "$":
			rght = RANGE_MAX
		left, rght = int(left), int(rght)
		numbers |= set(range(left, rght+1))
	return sorted(list(numbers))

def debug():
	import getopt
	import sys
	opts, args = getopt.gnu_getopt(sys.argv[1:], "s:", ["set="])
	print "opts: %s"%opts
	print "args: %s"%args
	for opt, arg in opts:
		if opt in ("-s", "--set"):
			k, v = eqtparser(arg)
			print "key: %s, value: %s"%(k,v)
			if k == "count":
				print rgparser(v)

if __name__ == "__main__":
	debug()
