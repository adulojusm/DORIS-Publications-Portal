from models import db, Document
from flask.ext.elasticsearch import ElasticSearch
from sqlalchemy import or_,desc
es = ElasticSearch()

def process_query(search, _agency, _category, _types):
	#remove_stop_words(search)
	#remove unsafe characters
	unsafe_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',  "--", '.']
	for char in unsafe_chars:
		search = search.replace(char, '')
	search = search.split()

	if search:
		results_h = Document.query
		results_t = Document.query
		results_d = Document.query
		results_ts = Document.query
		for i in range(0, len(search)):
			results_h = results_t.filter(Document.title.like('% ' + search[i] + ' %'))
			results_t = results_t.filter(Document.title.like('%' + search[i] + '%'))
			results_ts = results_d.filter(Document.description.like('% ' + search[i] + ' %'))
			results_d = results_d.filter(Document.description.like('%' + search[i] + '%'))

		results = results_h.union(results_t).union(results_ts).union(results_d)
	else:
		results = Document.query

	if _agency != "All Agencies":
		results = results.filter(Document.agency == _agency)
	if _category != "All Categories":
		results = results.filter(Document.category == _category)
	if _types != "All Types":
		results = results.filter(Document.type == _types)

	results = results.all()

	return results