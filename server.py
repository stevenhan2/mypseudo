#!/usr/bin/env python
from flask import Flask, request, make_response, render_template, redirect, session, url_for
import json
import os
import datetime
import config
import loader
import dbutils

mypseudo = Flask(__name__, static_folder="static", template_folder="templates")
mypseudo.debug = True
mypseudo.secret_key = os.urandom(24)

@mypseudo.route('/')
def index():
	if 'user' in session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

@mypseudo.route('/callbacks', methods=['GET'])
def callbacks():
	if 'user' in session:
		return dbutils.listCallbacks()
	else:
		return redirect(url_for('login'))

@mypseudo.route('/callback/<id>', methods=['GET','POST', 'DELETE'])
def callback(id=False):
	if 'user' in session:
		if request.method == 'GET':
			return dbutils.getCallback(id)
		elif request.method =='POST':
			return dbutils.saveCallback(request.data)
		elif request.method=='DELETE':
			return dbutils.deleteCallback(request.data)
	else:
		return redirect(url_for('login'))

@mypseudo.route('/script/<name>')
def script(name=""):
	if 'user' in session:
		return json.dumps(loader.getUsage(name), sort_keys=True, indent=4, separators=(',',': '), cls=dbutils.DateTimeEncoder, ensure_ascii=True)
	else:
		return redirect(url_for('index'))

@mypseudo.route('/scripts')
def scripts():
	if 'user' in session:
		return json.dumps(loader.loadValid(), sort_keys=True, indent=4, separators=(',',': '))
	else:
		return redirect(url_for('login'))

@mypseudo.route('/login', methods=['POST','GET'])
def login():
	if 'user' in session:
		return redirect(url_for('index'))
	else:
		if request.method == 'POST':
			if 'user' in request.form and 'passwd' in request.form:
				if request.form['user'] == config.config['user'] and request.form['passwd'] == config.config['passwd']:
					session['user'] = request.form['user']
					return redirect(url_for('index'))
		return render_template('login.html')

@mypseudo.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))

if __name__ == '__main__':
	mypseudo.run(host='0.0.0.0')

