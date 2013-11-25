import MySQLdb
import json
import config
import datetime
import os

dbconfig = config.config['mysql']
# db = MySQLdb.connect(host=dbconfig['host'], user=dbconfig['user'], passwd=dbconfig['passwd'], db="mypseudo")

def getDB():
	return MySQLdb.connect(host=dbconfig['host'], user=dbconfig['user'], passwd=dbconfig['passwd'], db="mypseudo")

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

def listCallbacks():
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('CALL `list_callbacks` ();')
	toReturn = json.dumps(cursor.fetchall(), sort_keys=True, indent=4, separators=(',',': '), cls=DateTimeEncoder, ensure_ascii=True)
	cursor.close()
	return toReturn

def getCallback(in_id):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('CALL `get_callback` (%s);',(str(int(in_id))))

	# fetchone instead of fetchall
	tmp = cursor.fetchone()
	cursor.close()

	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('CALL `get_parser_vars` (%s)',(str(int(in_id))))

	tmp2 = cursor.fetchall()
	cursor.close()

	tmp['parser_vars'] = tmp2

	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('CALL `get_request_vars` (%s)',(str(int(in_id))))

	tmp2 = cursor.fetchall()
	cursor.close()

	tmp['request_vars'] = tmp2

	return json.dumps(tmp, sort_keys=True, indent=4, separators=(',',': '), cls=DateTimeEncoder, ensure_ascii=True)

def saveCallback(data):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	callback = json.loads(data)
	if "id" in callback:
		cursor.execute("update mypseudo.callbacks set script=%s, url=%s, callback_url=%s, enabled=%s where id=%s", (callback['script'], callback['url'], callback['callbacks_url'], callback['enabled'], callback['id']))
	else:
		cursor.execute("insert into mypseudo.callbacks (url, callback_url, script, period, enabled) values (%s, %s, %s, %s, %s)", (callback['url'], callback['callbacks_url'], callback['script'], 30, 1))
		callback['id'] = cursor.lastrowid

	for to_delete in callback['to_delete_parser_vars']:
		cursor.execute("delete from mypseudo.parser_vars where id=%s", (to_delete))

	for to_delete in callback['to_delete_request_vars']:
		cursor.execute("delete from mypseudo.request_vars where id=%s", (to_delete))

	for parser_var in callback['parser_vars']:
		if 'id' in parser_var:
			cursor.execute("insert into mypseudo.parser_vars (id, callbacks_id, keyword, value) values (%s,%s,%s,%s) on duplicate key update keyword=%s, value=%s", (parser_var['id'], callback['id'], parser_var['keyword'], parser_var['value'], parser_var['keyword'], parser_var['value']))
		else:
			cursor.execute("insert into mypseudo.parser_vars (callbacks_id, keyword, value) values (%s,%s,%s) on duplicate key update value=%s", (callback['id'], parser_var['keyword'], parser_var['value'], parser_var['keyword']))

	for request_var in callback['request_vars']:
		if 'id' in request_var:
			cursor.execute("insert into mypseudo.request_vars (id, callbacks_id, keyword, value) values (%s,%s,%s,%s) on duplicate key update keyword=%s, value=%s", (request_var['id'], callback['id'], request_var['keyword'], request_var['value'], request_var['keyword'], request_var['value']))
		else:
			cursor.execute("insert into mypseudo.request_vars (callbacks_id, keyword, value) values (%s,%s,%s) on duplicate key update value=%s", (callback['id'], request_var['keyword'], request_var['value'], request_var['keyword']))

	cursor.close()
	db.commit()
	return getCallback(callback['id'])

def deleteCallback(data):
	db = getDB()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	callback = json.loads(data)
	cursor.execute("delete from mypseudo.callbacks where mypseudo.callbacks.id=%s", (callback['id']))
	db.commit()
	cursor.close()
	return ""



