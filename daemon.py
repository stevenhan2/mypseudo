#!/usr/bin/env python

import config
import scripts
import threading
import daemonutils
import requests
import os
import importlib
import time
from bs4 import BeautifulSoup
import datetime

DEBUGGING = False

class CallbackSource:
	def __init__(self, id):
		self.id = id

	def clearData(self):
		daemonutils.deleteAllCallbackData(id=self.id)

	def insert(self, key, value):
		daemonutils.setCallbackData(id=self.id, key=key, value=value)

	def delete(self, key):
		daemonutils.deleteCallbackData(id=self.id, key=key)


def doCallback(callback, parser_vars, request_vars):
	try:
		print request_vars
		payload = dict([(x['keyword'] , x['value']) for x in request_vars])
		vars = dict([(x['keyword'], x['value']) for x in parser_vars])
		url_request = requests.get(callback['url'], params=payload)
		soup = BeautifulSoup(url_request.content)
		source = CallbackSource(id=callback['id'])
		result = importlib.import_module('scripts.' + callback['script']).parse(soup=soup, vars=vars, data_source=source)

		if result['updated']:
			callback_url_request = requests.post(callback['callback_url'], data=result['data'], timeout=1)
			new_period = int(callback['period'] * 0.9 + config.config['min_period'] * 0.1)
			daemonutils.callbackMarkUpdate(id=callback['id'])		
		else:
			new_period = int(callback['period'] * 0.9 + config.config['max_period'] * 0.1)
			if new_period > config.config['max_period']:
				new_period = int(config.config['max_period'])

		daemonutils.setPeriod(id=callback['id'], period=new_period)
	except requests.exceptions.RequestException as e:
		log(str(e))

def log(message):
	if DEBUGGING:
		f = open(os.path.join(config.dirpath,'log.txt'), 'a+')
		f.write(str(datetime.datetime.now()) + ":\t" + message + "\n")
		f.close()

if __name__ == '__main__':
	log("Starting mypseudo daemon.")
	while True:
		callbacks = [x for x in daemonutils.list() if x['enabled'] > 0 and (x['last_time'] is None or (datetime.datetime.now() - x['last_time']).seconds > x['period'])]
		for a in callbacks:
			log("Creating thread for %s" % str(a))
			t = threading.Thread(target=doCallback, args=(daemonutils.getCallback(a['id']), daemonutils.parserVars(a['id']), daemonutils.requestVars(a['id'])))
			t.start()
		if not callbacks:
			log("No callbacks scheduled for execution.")

		log('Sleeping %s seconds.' % (config.config['min_period']))
		time.sleep(config.config['min_period'])
