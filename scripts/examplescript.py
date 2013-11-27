def usage():
	return """
		Example usage
	"""

def parse(soup, vars, data_source):
	post_parameters = {}
	title_text = str(soup.title)

	same_title = data_source.get('title') == title_text

	if not same_title:
		data_source.insert('title', title_text)
		post_parameters['example_param'] = title_text

	return {'data' : post_parameters, 'updated' : not same_title}
