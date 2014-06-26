from models import db, Document
from sqlalchemy import or_,desc


def process_query(search, _agency, _category, _types):
	#remove_stop_words(search)

	#remove unsafe characters
	unsafe_chars = ['"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',  "--", '.']
	for char in unsafe_chars:
		search = search.replace(char, '')

	split_search = search.split()

	if split_search:
		results_t1 = Document.query
		results_t2 = Document.query
		results_d1 = Document.query
		results_d2 = Document.query
		for word in split_search:
			if len(word)<4:
				results_t1 = results_t1.filter(Document.title.like('% ' + word + ' %'))
				results_d1 = results_d1.filter(Document.description.like('% ' + word + ' %'))
				results = results_t1.union(results_d1)
			else:
				results_t1 = results_t1.filter(Document.title.like('% ' + word + ' %'))
				results_t2 = results_t2.filter(Document.title.like('%' + word + '%'))
				results_d1 = results_d1.filter(Document.description.like('% ' + word + ' %'))
				results_d2 = results_d2.filter(Document.description.like('%' + word + '%'))
				results = results_t1.union(results_t2).union(results_d1).union(results_d2)
	else:

		results = Document.query

	agencies = ['Aging', 'Buildings', 'Campaign Finance', 'Children\'s Services', 'City Council', 'City Clerk', 'City Planning', 'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Community Assistance', 'Comptroller', 'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Correction', 'Criminal Justice Coordinator', 'Cultural Affairs', 'DOI - Investigation', 'Design/Construction', 'Disabilities', 'District Atty, NY County', 'Districting Commission', 'Domestic Violence', 'Economic Development', 'Education, Dept. of', 'Elections, Board of', 'Emergency Mgmt.', 'Employment', 'Empowerment Zone', 'Environmental - DEP', 'Environmental - OEC', 'Environmental - ECB', 'Equal Employment', 'Film/Theatre', 'Finance', 'Fire', 'FISA', 'Health and Mental Hyg.', 'HealthStat', 'Homeless Services', 'Hospitals - HHC', 'Housing - HPD', 'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget', 'Info. Tech. and Telecom.', 'Intergovernmental', 'International Affairs', 'Judiciary Committee', 'Juvenile Justice', 'Labor Relations', 'Landmarks', 'Law Department', 'Library - Brooklyn', 'Library - New York', 'Library - Queens', 'Loft Board', 'Management and Budget', 'Mayor', 'Metropolitan Transportation Authority', 'NYCERS', 'Operations', 'Parks and Recreation', 'Payroll Administration', 'Police', 'Police Pension Fund', 'Probation', 'Public Advocate', 'Public Health', 'Public Housing-NYCHA', 'Records', 'Rent Guidelines', 'Sanitation', 'School Construction', 'Small Business Svcs', 'Sports Commission', 'Standards and Appeal', 'Tax Appeals Tribunal', 'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings', 'Veterans - Military', 'Volunteer Center', 'Voter Assistance', 'Youth & Community']
	categories = ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment', 'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services', 'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology', 'Transportation']
	types = ['Annual Report', 'Audit Report', 'Bond Offering - Official Statements', 'Budget Report', 'Consultant Report', 'Guide - Manual', 'Hearing - Minutes', 'Legislative Document', 'Memoranda - Directive', 'Press Release', 'Serial Publication', 'Staff Report', 'Report']

	if _agency != "All Agencies":
		results = results.filter(Document.agency == _agency)
	else:
		for agency in agencies:
			if search.lower() == agency.lower():
				results_a = Document.query.filter(Document.agency == agency)
				results = results.union(results_a)
				results = results.all()
				return results

	if _category != "All Categories":
		results = results.filter(Document.category == _category)
	else:
		for category in categories:
			if search.lower() == category.lower():
				results_c = Document.query.filter(Document.agency == category)
				results = results.union(results_c)
				results = results.all()
				return results

	if _types != "All Types":
		results = results.filter(Document.type == _types)
	else:
		for type in types:
			if search.lower() == type.lower():
				results_types = Document.query.filter(Document.agency == type)
				results = results.union(results_types)
				results = results.all()
				return results

	results = results.all()

	return results