import os
import json

dirpath = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(os.path.join(dirpath,'config.json'),'r').read())

def log(message):
	if config['debugging']:
		f = open(os.path.join(config.dirpath,'log.txt'), 'a+')
		f.write(str(datetime.datetime.now()) + ':\t' + message + '\n')
		f.close()