def usage():
	return """
		Example usage
	"""

def parse(soup, vars, data_source):

	same_title = data_source.get('title') == soup.title

	if not same_title:
		data_source.insert('title',soup.title)
		to_return = {'param' : soup.title}

	return {'data' : to_return, 'updated' : not same_title}
