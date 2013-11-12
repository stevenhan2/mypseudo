import scripts
import importlib
import os
import glob

dirpath = os.path.dirname(os.path.realpath(__file__))

def loadValid():
	a = []
	unfiltered = [os.path.basename(f)[:-3] for f in glob.glob(dirpath + "/scripts/*.py")]
	for s in unfiltered:
		if 'parse' in dir(importlib.import_module('scripts.' + s)):
			a.append(s)
	return a

def getParams(a):
	if a in loadValid():
		tmp = importlib.import_module('scripts.' + a)
		return tmp.parse.func_code.co_argcount, tmp.parse.func_code.co_varnames

def getUsage(a):
	x = {'name' : a}
	if a in loadValid():
		tmp = importlib.import_module('scripts.' + a)
		if 'usage' in dir(tmp):
			x['usage'] = tmp.usage()
		return x
