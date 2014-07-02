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
				results = results_t1.union(results_t2).union(results_t3).union(results_d1).all()
			else:
				results_t1 = results_t1.filter(Document.title.like('% ' + word + ' %'))
				results_t2 = results_t2.filter(Document.title.like('%' + word + '%'))
				results_d1 = results_d1.filter(Document.description.like('% ' + word + ' %'))
				results_d2 = results_d2.filter(Document.description.like('%' + word + '%'))
				results_ag = results_ag.filter(Document.agency.like('%' + search + '%'))
				results_cat = results_cat.filter(Document.category.like('%' + search + '%'))
				results_typ = results_typ.filter(Document.type.like('%' + search + '%'))
				results = results_t1.union(results_d1).union(results_t2).union(results_d2).union(results_ag).union(results_cat).union(results_typ).all()

	else:

		results = Document.query.all()

	agencies = ['aging', 'buildings', 'campaign finance', 'children\'s services', 'city council', 'city clerk', 'city planning', 'citywide admin svcs', 'civilian complaint', 'comm - police corr', 'community assistance', 'comptroller', 'conflicts of interest', 'consumer affairs', 'contracts', 'correction', 'criminal justice coordinator', 'cultural affairs', 'doi - investigation', 'design/construction', 'disabilities', 'district atty, ny county', 'districting commission', 'domestic violence', 'economic development', 'education, dept. of', 'elections, board of', 'emergency mgmt.', 'employment', 'empowerment zone', 'environmental - dep', 'environmental - oec', 'environmental - ecb', 'equal employment', 'film/theatre', 'finance', 'fire', 'fisa', 'health and mental hyg.', 'healthstat', 'homeless services', 'hospitals - hhc', 'housing - hpd', 'human rights', 'human rsrcs - hra', 'immigrant affairs', 'independent budget', 'info. tech. and telecom.', 'intergovernmental', 'international affairs', 'judiciary committee', 'juvenile justice', 'labor relations', 'landmarks', 'law department', 'library - brooklyn', 'library - new york', 'library - queens', 'loft board', 'management and budget', 'mayor', 'metropolitan transportation authority', 'nycers', 'operations', 'parks and recreation', 'payroll administration', 'police', 'police pension fund', 'probation', 'public advocate', 'public health', 'public housing-nycha', 'records', 'rent guidelines', 'sanitation', 'school construction', 'small business svcs', 'sports commission', 'standards and appeal', 'tax appeals tribunal', 'tax commission', 'taxi and limousine', 'transportation', 'trials and hearings', 'veterans - military', 'volunteer center', 'voter assistance', 'youth & community']
	categories = ['business and consumers', 'cultural/entertainment', 'education', 'environment', 'finance and budget', 'government policy', 'health', 'housing and buildings', 'human services', 'labor relations', 'public safety', 'recreation/parks', 'sanitation', 'technology', 'transportation']
	types = ['annual report', 'audit report', 'bond offering - official statements', 'budget report', 'consultant report', 'guide - manual', 'hearing - minutes', 'legislative document', 'memoranda - directive', 'press release', 'serial publication', 'staff report', 'report']
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