def usage():
	return """
		Example usage
	"""

def parse(soup, vars, data_source):
	data_source.insert('hello','world')
	to_return = {'param' : 'value'}
	return {'data' : to_return, 'updated' : True}
