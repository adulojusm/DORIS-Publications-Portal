from app import app
from flask import Flask,render_template, request, flash, url_for,redirect,make_response,session,abort
from forms import SearchForm
from models import db, Document
from flask.sessions import SessionInterface


from query_functions import process_query


def redirect_url(default='index'):
	return request.args.get('next') or request.referrer or url_for(default)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():

	if request.method == 'POST':
		# if request.referrer == '':
		# 		pass
		# 	agencySelect = request.form['agencySelect']
		# 	print agencySelect
		if request.form['user_input']:
			search = request.form['user_input']

			agency = request.form['agency']
			category = request.form['category']
			types = request.form['type']
			if not search and agency=='All Agencies' and category == 'All Categories' and types == 'All Types' :
				flash('Please enter a search or select a filter.')
				return redirect(url_for('index'))

			results = process_query(search, agency, category, types)
			length = len(results)

			if length:
				return render_template("res.html", search=search, results=results, length=length, agency=agency, category=category, types=types, method='post')
			else:
				flash('No results found')
				return redirect(url_for('index'))

		print 'received post data'

	return render_template("res.html")



@app.route('/publication/<int:id>', methods=['GET'])
def publication(id):

	document = Document.query.filter(Document.id == id).first()
	print document.id
	#document.num_access += 1
	#db.session.commit()
	document_title = document.title
	print document_title
	document_url = document.url
	if len(document_title) > 115:
		document_title = document_title[:115] + "..."
	return render_template("publication.html", id=id, document_title=document_title, document_url=document_url)

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
