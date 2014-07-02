from models import db, Document
from sqlalchemy import or_,desc, false, func
from sqlalchemy.orm import aliased


def process_query(search, agencies_selected, categories_selected, types_selected):
	#remove_stop_words(search)

	#remove unsafe characters
	unsafe_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',  "--", '.']
	for char in unsafe_chars:
		search = search.replace(char, '')

	split_search = search.split()
	if split_search:
		results = Document.query.filter(false())
		results_t1 = Document.query
		results_t2 = Document.query
		results_t3 = Document.query
		results_d1 = Document.query
		results_d2 = Document.query
		results_ag = Document.query
		results_cat = Document.query
		results_typ = Document.query
		for word in split_search:
			if len(word) < 4:
				results_t1 = results_t1.filter(Document.title.like('% ' + word + ' %'))
				results_t2 = results_t2.filter(Document.title.like(word + ' %'))
				results_t3 = results_t3.filter(Document.title.like('% ' + word))
				results_d1 = results_d1.filter(Document.description.like('% ' + word + ' %'))
				results = results.union(results_t1).union(results_t2).union(results_t3).union(results_d1)
			else:
				results_t1 = results_t1.filter(Document.title.like('% ' + word + ' %'))
				results_t2 = results_t2.filter(Document.title.like('%' + word + '%'))
				results_d1 = results_d1.filter(Document.description.like('% ' + word + ' %'))
				results_d2 = results_d2.filter(Document.description.like('%' + word + '%'))
				results_ag = results_ag.filter(Document.agency.like('%' + search + '%'))
				results_cat = results_cat.filter(Document.category.like('%' + search + '%'))
				results_typ = results_typ.filter(Document.type.like('%' + search + '%'))
				results = results.union(results_t1).union(results_d1).union(results_t2).union(results_d2).union(results_ag).union(results_cat).union(results_typ)
	else:
		results = Document.query

	results = results.all()
	a = []
	b = []
	c = []
	if agencies_selected:
		for result in results:
			if result.agency in agencies_selected:
				a.append(result)
	else:
		a = results

	if categories_selected:
		for result in a:
			if result.category in categories_selected:
				b.append(result)
	else:
		b = a

	if types_selected:
		for result in b:
			if result.type in types_selected:
				c.append(result)
	else:
		c = b

	return c


def sort_search(results, sort_method):
	sort_by = {"Relevance": results,
				"Date: Newest": sorted(results, key=lambda r: r.date_created, reverse=True),
				"Date: Oldest": sorted(results, key=lambda r: r.date_created),
				"Title: A - Z": sorted(results, key=lambda r: r.title),
				"Title: Z - A": sorted(results, key=lambda r: r.title, reverse=True),
				"Agency: A - Z": sorted(results, key=lambda r: r.agency),
				"Agency: Z - A": sorted(results, key=lambda r: r.agency, reverse=True)}

	return sort_by[sort_method]