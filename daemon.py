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

class CallbackSource:
	def __init__(self, id):
		self.id = id

	def clearData(self):
		daemonutils.deleteAllCallbackData(id=self.id)

	def insert(self, key, value):
		daemonutils.setCallbackData(id=self.id, key=key, value=value)

	def get(self, key):
		pair = daemonutils.fetchCallbackData(id=self.id, key=key)
		if pair:
			return pair['value']
		else:
			return None

	def delete(self, key):
		daemonutils.deleteCallbackData(id=self.id, key=key)


def doCallback(callback, parser_vars, request_vars):
	try:
		config.log('Initialized thread for: %s' % str(callback))
		payload = dict([(x['keyword'] , x['value']) for x in request_vars])
		vars = dict([(x['keyword'], x['value']) for x in parser_vars])
		url_request = requests.get(callback['url'], params=payload)
		soup = BeautifulSoup(url_request.content)
		source = CallbackSource(id=callback['id'])

		# Run script
		try:
			result = importlib.import_module('scripts.' + callback['script']).parse(soup=soup, vars=vars, data_source=source)
		except ImportError as e:
			config.log('Error occured for ID=%d: %s' % (callback['id'],str(e)))

		if result['updated']:
			config.log('ID=%d has detected update at %s and will now request %s' % (callback['id'], callback['url'], callback['callback_url']))
			callback_url_request = requests.post(callback['callback_url'], data=result['data'], timeout=1)
			new_period = int(callback['period'] * 0.9 + config.config['min_period'] * 0.1)
			daemonutils.callbackMarkUpdate(id=callback['id'])		
		else:
			new_period = int(callback['period'] * 0.9 + config.config['max_period'] * 0.1)
			if new_period > config.config['max_period']:
				new_period = int(config.config['max_period'])

		config.log('Setting callback ID=%d period to %d' % (callback['id'], new_period))
		daemonutils.setPeriod(id=callback['id'], period=new_period)
	except requests.exceptions.RequestException as e:
		config.log('Error occured for ID=%d: %s' % (callback['id'],str(e)))
		config.log('Faulty callback details: %s' % str(callback))

if __name__ == '__main__':
	config.log('Starting mypseudo daemon.')
	while True:
		callbacks = [x for x in daemonutils.list() if x['enabled'] > 0 and (x['last_time'] is None or (datetime.datetime.now() - x['last_time']).seconds > x['period'])]
		for a in callbacks:
			config.log('Creating thread for ID=%d...' % a['id'])
			t = threading.Thread(target=doCallback, args=(daemonutils.getCallback(a['id']), daemonutils.parserVars(a['id']), daemonutils.requestVars(a['id'])))
			t.start()
		if not callbacks:
			config.log('No callbacks scheduled for execution.')

		config.log('Sleeping %s seconds.' % (config.config['min_period']))
		time.sleep(config.config['min_period'])
