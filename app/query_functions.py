from models import Document
from sqlalchemy.orm import defer
import time

def process_query(search, agencies_selected, categories_selected, types_selected):
	"""
	Retrieves search results based on search value and selected filters
	:param search: user input query
	:param agencies_selected: user-selected agencies from 'Filter' / 'Refine Search'
	:param categories_selected: user-selected categories from 'Filter' / 'Refine Search'
	:param types_selected: user-selected types from 'Filter' / 'Refine Search'
	:return: finalized results of the query, and the time it takes to execute this function
	"""
	process_time_start = time.clock()

	search = normalize(search)

	#initialize query or search based on user input
	if search:
		results = Document.query.options(defer('num_access')).whoosh_search(search)
	else:
		results = Document.query.options(defer('num_access'))

	#retrieve results object list
	results = results.all()

	#filter by user selections, if any
	initial_filter = []
	intermediate_filter = []
	final_filter = []
	
	if agencies_selected:
		for result in results:
			if result.agency in agencies_selected:
				initial_filter.append(result)
	else:
		initial_filter = results

	if categories_selected:
		for result in initial_filter:
			if result.category in categories_selected:
				intermediate_filter.append(result)
	else:
		intermediate_filter = initial_filter

	if types_selected:
		for result in intermediate_filter:
			if result.type in types_selected:
				final_filter.append(result)
	else:
		final_filter = intermediate_filter

	process_time_elapsed = (time.clock() - process_time_start)

	return final_filter, process_time_elapsed


def sort_search(results, sort_method):
	"""
	Sorts results of current set
	:param results: query results list
	:param sort_method: how to sort results
	:return: sorted results
	"""
	sort_by = {"Relevance": results,
				"Date: Newest": sorted(results, key=lambda r: r.date_created, reverse=True),
				"Date: Oldest": sorted(results, key=lambda r: r.date_created),
				"Title: A - Z": sorted(results, key=lambda r: r.title),
				"Title: Z - A": sorted(results, key=lambda r: r.title, reverse=True),
				"Agency: A - Z": sorted(results, key=lambda r: r.agency),
				"Agency: Z - A": sorted(results, key=lambda r: r.agency, reverse=True)}

	return sort_by[sort_method]


def normalize(_input):
	"""
	Standardizes passed value by removing unnecessary characters and words
	:param _input: string to be normalized
	:return: normalized value
	"""
	#remove stop words
	stop_words = []

	#remove stop characters
	stop_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',  "--", '.']
	for char in stop_chars:
		_input = _input.replace(char, '')

	return _input