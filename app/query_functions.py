from models import db, Document


def process_query(search, _agency, _category, _types):
	#remove_stop_words(search)
	#remove unsafe characters
	unsafe_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`', "'",  "--"]
	for char in unsafe_chars:
		search = search.replace(char, '')
	print search
	search = search.split()

	results_t = Document.query
	results_d = Document.query
	for i in range(0, len(search)):
		results_t = results_t.filter(Document.title.contains(search[i]))
		results_d = results_d.filter(Document.description.contains(search[i]))
	results = results_t.union(results_d)
	if _agency != "All Agencies":
		results = results.filter(Document.agency == _agency)
	if _category != "All Categories":
		results = results.filter(Document.category == _category)
	if _types != "All Types":
		results = results.filter(Document.type == _types)

	results = results.all()

	for result in results:
		print result.agency, result.category, result.type
		print result.title + '\n'

	return results