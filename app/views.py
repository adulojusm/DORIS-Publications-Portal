from app import app
from flask import Flask,render_template, request, flash, url_for, redirect, make_response, session, abort
from forms import SearchForm
from models import db, Document
from query_functions import process_query, sort_search
from index_database import index_database
from flask.ext.paginate import Pagination


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)
		


@app.route('/results', methods=['GET', 'POST'])
def results():
	session['fulltext'] = ''
	#Set initial session variables
	if 'sort' not in session:
		session['sort'] = 'Relevance'
	if 'length' not in session:
		session['length'] = 0
		
	#On POST request
	if request.method == 'POST':
	
		#POST - Search
		if request.form['btn'] == "Search":
			session['search'] = request.form.get('user_input')
			session['agencies'] = request.form.getlist('agency[]')
			session['categories'] = request.form.getlist('category[]')
			session['types'] = request.form.getlist('type[]')

			if not session['search'] and not session['agencies'] and not session['categories'] and not session['types']:
				flash('Enter a search entry')
				return redirect(url_for('index'))
					
		#POST - Refine Search
		if request.form['btn'] == "Refine / Search":
			if request.form.get('user_input'):
				session['search'] = request.form.get('user_input')
			session['agencies'] = request.form.getlist('agency[]')
			session['categories'] = request.form.getlist('category[]')
			session['types'] = request.form.getlist('type[]')
			if request.form.get('fulltext'):
				session['fulltext'] = request.form.get('text_search')

	#On GET Request
	if request.method == 'GET':
		
		#GET - Sort
		if request.args.get('sort'):
			session['sort'] = request.args.get('sort')

	#retrieve results
	res, time = process_query(session['search'], session['agencies'], session['categories'], session['types'])
	res = sort_search(res, session['sort'])
	session['length'] = len(res)
	
	#initiate pagination
	try:
		page = int(request.args.get('page',1))
	except ValueError:
		page = 1
	pagination = Pagination(page=page, total=session['length'], per_page=10, css_framework="boostrap3")
	start = (page*10)-10
	res = res[start:start+9]
	
	#RENDER!
	return render_template("results.html", 
							search=session['search'], 
							results=res, 
							time=time, 
							length=session['length'], 
							method='post', 
							sort_method=session['sort'], 
							pagination=pagination,
							fulltext=session['fulltext'])


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