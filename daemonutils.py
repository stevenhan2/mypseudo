import MySQLdb
import json
import datetime
import os
import config

dbconfig = config.config['mysql']
db = MySQLdb.connect(host=dbconfig['host'], user=dbconfig['user'], passwd=dbconfig['passwd'], db="mypseudo")

def list():
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select enabled, id, period, last_time from mypseudo.callbacks")
	return cursor.fetchall()

def getCallback(id):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select * from mypseudo.callbacks where id = %s limit 1", (id))
	return cursor.fetchone()

def parserVars(id):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.parser_vars where callbacks_id=%s",(id))
	return cursor.fetchall()

def requestVars(id):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.request_vars where callbacks_id=%s",(id))
	return cursor.fetchall()

def callbackMarkUpdate(id):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set callbacks.last_time=now() where callbacks.id=%s limit 1",(id))
	db.commit()

def deleteAllCallbackData(id):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("delete from mypseudo.callbacks_data where callbacks_id=%s",(id))
	db.commit()

def fetchCallbackData(id, key):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.callbacks_data where callbacks_id=%s and keyword=%s limit 1",(id, key))
	return cursor.fetchone()

def setCallbackData(id, key, value):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("insert into mypseudo.callbacks_data (callbacks_id, keyword, value) values (%s, %s, %s) on duplicate key update value=%s", (id, key, value, value))
	db.commit()

def deleteCallbackData(id, key):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("delete from mypseudo.callbacks_data where callbacks_id=%s and keyword=%s limit 1",(id,key))
	db.commit()

def setPeriod(id, period):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set callbacks.period=%s where callbacks.id=%s limit 1",(period,id))
	db.commit()



def setCallbackPeriod(id, period):
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set period=%s where callbacks.id=%s limit 1",(id, period))
	db.commit()