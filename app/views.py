from app import app
from flask import Flask,render_template, request, flash, url_for,redirect,make_response,session,abort
from forms import SearchForm
from models import db, Document
from query_functions import process_query, refine_search, sort_search


def redirect_url(default='index'):
	return request.args.get('next') or request.referrer or url_for(default)

active = {"0": "NOT ACTIVE", "1": "ACTIVE"}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
	if 'sort' not in session:
		session['sort'] = 'Relevance'

	if request.method == 'POST':
		sort_method = session['sort']
		search = request.form.get('user_input')
		session['search'] = request.form.get('user_input')
		print search
		agencies = request.form.getlist('agency[]')
		session['agencies'] = request.form.getlist('agency[]')
		categories = request.form.getlist('category[]')
		session['categories'] = request.form.getlist('category[]')
		types = request.form.getlist('type[]')
		session['types'] = request.form.getlist('type[]')

		if not search and not agencies and not categories and not types:
			flash('Please enter a search or select a filter.')
			return redirect(url_for('index'))

		results = process_query(search, agencies, categories, types)

		if len(results):
			return render_template("res.html", search=session['search'], results=results, length=len(results), method='post', sort_method=sort_method,agencies=agencies,categories=categories,types=types)
		else:
			flash('No results found')
			return redirect(url_for('index'))

	if request.method == 'GET':
		search = session['search']
		agencies = session['agencies']
		categories = session['categories']
		types = session['types']
		results = process_query(search, agencies, categories, types)

		# if request.args.get('sort'):
		# 	sort_method = request.args.get('sort')
		# 	session['sort'] = sort_method
		# 	results = sort_search(results, sort_method).all()
		# 	return render_template("res.html", search=search, results=results, length=len(results), sort_method=sort_method)
		# elif session['sort']:
		# 	sort_method = session['sort']
		# 	results = sort_search(results, sort_method).all()
		# 	return render_template("res.html", search=search, results=results, length=len(results), sort_method=sort_method)
		# sort_method = session['sort']
		return render_template("res.html", search=search, results=results, length=len(results), sort_method='Relevance')


# @app.route('/results/refined', methods=['GET'])
# def foo():
# 	search = session['search']
# 	# agencies = session['agencies']
# 	# categories = session['categories']
# 	# types = session['types']
#
# 	agencies = request.args.getlist('agency[]')
# 	categories = request.args.getlist('category[]')
# 	types = request.args.getlist('type[]')
# 	results = process_query(search, agencies, categories, types)
# 	if request.args.get('sort'):
# 		sort_method = request.args.get('sort')
# 		session['sort'] = sort_method
# 		refined_results = sort_search(refined_results, sort_method).all()
# 		return render_template("res.html", search=search, results=refined_results, length=len(refined_results), sort_method=sort_method)
# 	elif session['sort']:
# 		sort_method = session['sort']
# 		refined_results = sort_search(refined_results, sort_method).all()
# 		return render_template("res.html", search=search, results=refined_results, length=len(refined_results), sort_method=sort_method)
# 	if len(refined_results):
# 		return render_template("res.html", search=search, results=refined_results, length=len(refined_results), sort_method=session['sort'])
# 	else:
# 		flash('No results found')
# 		return redirect(url_for('index'))

@app.route('/publication/<int:id>', methods=['GET'])
def publication(id):
	document = Document.query.filter(Document.id == id).first()
	document_title = document.title
	document_url = document.url
	# document.num_access += 1
	# db.session.commit()
	# response = make_response(url)
	# response.headers['Content-Type'] = 'application/pdf'
	# response.headers['Content-Disposition'] = 'attachment; filename=%s.pdf' % document.filename
	# return response
	return render_template("publication.html", document_title=document_title, document_url=document_url)

@app.route('/about')
def about():
	return render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


'''@app.route('/testdb')
def testdb():
	db.create_all()
	return redirect(url_for('index'))
'''
