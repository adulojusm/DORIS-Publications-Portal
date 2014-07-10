from app import app
from flask import Flask,render_template, request, flash, url_for,redirect,make_response,session,abort,jsonify
from forms import SearchForm
from models import db, Document
from query_functions import process_query, sort_search
from index_database import index_database

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	session.clear()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
	if 'sort' not in session:
		session['sort'] = 'Relevance'

	if request.method == 'POST':
		if request.form['btn'] == "Search":

			sort_method = session['sort']
			search = request.form.get('user_input')
			session['search'] = request.form.get('user_input')
			agencies = request.form.getlist('agency[]')
			session['agencies'] = request.form.getlist('agency[]')
			categories = request.form.getlist('category[]')
			session['categories'] = request.form.getlist('category[]')
			types = request.form.getlist('type[]')
			session['types'] = request.form.getlist('type[]')

			if not search and not agencies and not categories and not types:
				flash('Please enter a search or select a filter.')
				return redirect(url_for('index'))

			results, time = process_query(search, agencies, categories, types)

			if len(results):
				return render_template("res.html", search=search, results=results, time=time, length=len(results), method='post', sort_method=sort_method,agencies=agencies,categories=categories,types=types)
			else:
				flash('No results found')
				return redirect(url_for('index'))

		if request.form['btn'] == "Refine Search":
			agencies = request.form.getlist('agency[]')
			session['ref_agencies'] = agencies
			categories = request.form.getlist('category[]')
			session['ref_categories'] = categories
			types = request.form.getlist('type[]')
			session['ref_types'] = types

			if request.form.getlist('agency[]') or request.form.getlist('category[]') or request.form.getlist('type[]'):
				results, time = process_query(session['search'], agencies, categories, types)
			else:
				results, time = process_query(session['search'], [], [], [])

	if 'ref_agencies' not in session:
		session['ref_agencies'] = session['agencies']
	if 'ref_categories' not in session:
		session['ref_categories'] = session['categories']
	if 'ref_types' not in session:
		session['ref_types'] = session['types']

	if request.method == 'GET':
		if request.args.get('back'):
			results, time = process_query(session['search'], session['ref_agencies'], session['ref_categories'], session['ref_types'])

		if request.args.get('sort'):
			results, time = process_query(session['search'], session['ref_agencies'], session['ref_categories'], session['ref_types'])
			session['sort'] = request.args.get('sort')

	results = sort_search(results, session['sort'])

	return render_template("res.html", search=session['search'], results=results, time=time, length=len(results), sort_method=session['sort'])


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


# @app.route('/testdb')
# def testdb():
# 	#db.create_all()
# 	index_database()
# 	return redirect(url_for('index'))
