from models import db, Document


def process_query(search, _agency, _category, _types):
	#remove_stop_words(search)
	#remove unsafe characters
	unsafe_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`', "'"]
	for char in unsafe_chars:
		search = search.replace(char, '')
	print search
	search = search.split()

	results = Document.query.filter(Document.title.contains(search[0]))
	for i in range(1, len(search)):
		results = results.filter(Document.title.contains(search[i]))

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