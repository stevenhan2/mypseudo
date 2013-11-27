import MySQLdb
import json
import datetime
import os
import config

dbconfig = config.config['mysql']
# db = MySQLdb.connect(host=dbconfig['host'], user=dbconfig['user'], passwd=dbconfig['passwd'], db="mypseudo")

def getDB():
	return MySQLdb.connect(host=dbconfig['host'], user=dbconfig['user'], passwd=dbconfig['passwd'], db="mypseudo")

def list():
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select enabled, id, period, last_time from mypseudo.callbacks")
	toReturn = cursor.fetchall()
	cursor.close()
	db.close()
	return toReturn

def getCallback(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select * from mypseudo.callbacks where id = %s limit 1", (id))
	toReturn = cursor.fetchone()
	cursor.close()
	db.close()
	return toReturn

def parserVars(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.parser_vars where callbacks_id=%s",(id))
	toReturn = cursor.fetchall()
	cursor.close()
	db.close()
	return toReturn

def requestVars(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.request_vars where callbacks_id=%s",(id))
	toReturn = cursor.fetchall()
	cursor.close()
	db.close()
	return toReturn

def callbackMarkUpdate(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set callbacks.last_update=now() where callbacks.id=%s limit 1",(id))
	db.commit()
	cursor.close()
	db.close()

def callbackMarkCheck(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set callbacks.last_time=now() where callbacks.id=%s limit 1",(id))
	db.commit()
	cursor.close()
	db.close()

def deleteAllCallbackData(id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("delete from mypseudo.callbacks_data where callbacks_id=%s",(id))
	db.commit()
	cursor.close()
	db.close()

def fetchCallbackData(id, key):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword, value from mypseudo.callbacks_data where callbacks_id=%s and keyword=%s limit 1",(id, key))
	toReturn = cursor.fetchone()
	cursor.close()
	db.close()
	return toReturn

def fetchAllCallbackData(id, key):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select keyword as key, value as value from mypseudo.callbacks_data where callbacks_id=%s",(id))
	toReturn = cursor.fetchall()
	cursor.close()
	db.close()
	return toReturn

def setCallbackData(id, key, value):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("insert into mypseudo.callbacks_data (callbacks_id, keyword, value) values (%s, %s, %s) on duplicate key update value=%s", (id, key, value, value))
	db.commit()
	cursor.close()
	db.close()

def deleteCallbackData(id, key):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("delete from mypseudo.callbacks_data where callbacks_id=%s and keyword=%s limit 1",(id,key))
	db.commit()
	cursor.close()
	db.close()

def setPeriod(id, period):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set callbacks.period=%s where callbacks.id=%s limit 1",(period,id))
	db.commit()
	cursor.close()
	db.close()

def setCallbackPeriod(id, period):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("update mypseudo.callbacks set period=%s where callbacks.id=%s limit 1",(id, period))
	db.commit()
	cursor.close()
	db.close()