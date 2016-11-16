import logging
import subprocess

def output(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
	return p.communicate()[0].strip()

def fwrite(string, path):
	fil = open(path, "w")
	fil.write(string)
	fil.close()

def fread(path):
	""" Convert a text file into a list of lines

	Note that blank line will be expelled.

	Args:
		path: Path to the target file.

	Returns:
		A list object consisting of lines in target file.
	"""

	inf = open(path, "r")
	lns = [x.strip() for x in inf]
	inf.close()
	lns = filter(lambda x: x, lns)

	return lns

def getlogger(name):
	logger = logging.getLogger(name)
	loghandler = logging.StreamHandler()

	logformatter = logging.Formatter('%(asctime)s %(filename)s: %(funcName)s: %(lineno)d %(levelname)s %(message)s')
	loghandler.setFormatter(logformatter)
	logger.addHandler(loghandler)
	logger.setLevel(logging.INFO)

	return logger

