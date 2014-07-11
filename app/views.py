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
	if 'page_num' not in session:
		session['page_num'] = 1
	if 'page_id' not in session:
		session['page_id'] = 1
	if 'length' not in session:
		session['length'] = 0
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

			res, time = process_query(search, agencies, categories, types)
			session['length'] = len(res)
			if session['length']:
				session['page_num'] = int(len(res)/10)+1
				res = res[:10]
				return render_template("results.html", search=search, results=res, time=time, length=session['length'], method='post', sort_method=sort_method, page_num=int(session['page_num']), page_id=int(session['page_id']))
			else:
				flash('No results found')
				return redirect(url_for('index'))

		if request.form['btn'] == "Refine Search":
			session['page_id'] = 1
			agencies = request.form.getlist('agency[]')
			session['ref_agencies'] = agencies
			categories = request.form.getlist('category[]')
			session['ref_categories'] = categories
			types = request.form.getlist('type[]')
			session['ref_types'] = types

			if request.form.getlist('agency[]') or request.form.getlist('category[]') or request.form.getlist('type[]'):
				res, time = process_query(session['search'], agencies, categories, types)
				session['length'] = len(res)
				session['page_num'] = int(len(res)/10)+1
			else:
				res, time = process_query(session['search'], [], [], [])
				session['length'] = len(res)
				session['page_num'] = int(len(res)/10)+1

	if 'ref_agencies' not in session:
		session['ref_agencies'] = session['agencies']
	if 'ref_categories' not in session:
		session['ref_categories'] = session['categories']
	if 'ref_types' not in session:
		session['ref_types'] = session['types']

	if request.method == 'GET':
		if request.args.get('back'):
			res, time = process_query(session['search'], session['ref_agencies'], session['ref_categories'], session['ref_types'])

		if request.args.get('sort'):
			res, time = process_query(session['search'], session['ref_agencies'], session['ref_categories'], session['ref_types'])
			session['sort'] = request.args.get('sort')
			session['page_id'] = 1

		if request.args.get('page_id'):
			session['page_id'] = request.args.get('page_id')
			res, time = process_query(session['search'], session['ref_agencies'], session['ref_categories'], session['ref_types'])

	start = (int(session['page_id'])*10)-10
	res = sort_search(res, session['sort'])
	res = res[start:start+9]

	return render_template("results.html", search=session['search'], results=res, time=time, length=session['length'], sort_method=session['sort'], page_num=int(session['page_num']), page_id=int(session['page_id']))


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

# @app.route('/whoosh_index_db')
# def whoosh_index_db():
# 	index_database()
# 	return redirect(url_for('index'))
#
# @app.route('/create_db')
# def create_db():
# 	db.drop_all()
# 	db.create_all()
# 	return redirect(url_for('index'))