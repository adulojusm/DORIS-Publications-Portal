from app import app
from flask import Flask,render_template, request, flash, url_for,redirect,make_response,session,abort
from forms import SearchForm
from models import db, Document
import datetime

from query_functions import process_query


app.config['SECRET_KEY'] = 'F34TF$($e34D'

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
	session['active'] = True
	if request.method == 'POST':

		search = request.form['user_input']

		agency = request.form['agency']
		category = request.form['category']
		types = request.form['type']
		if not search and agency=='All Agencies' and category == 'All Categories' and types == 'All Types':
			flash('Please enter a search or select a filter.')
			return redirect(url_for('index'))
		results = process_query(search, agency, category, types)
		length = len(results)

		if length:
			return render_template("res.html", results=results, length=length, method='post')
		else:
			flash('No results found')
			return redirect(url_for('index'))

	else:

		return render_template("res.html",session=session)


@app.route('/publication/<int:id><title>', methods=['GET'])
def publication(id,title):
	if not session.get('active'):
		abort(401)

	document = Document.query.filter(Document.id == id).first()
	print document.num_access
	document.num_access += 1
	db.session.commit()
	print document.num_access
	document_title = document.title
	document_url = document.url
	# if len(document_title) > 70:
	# 	document_title = document_title[:70] + "..."
	return render_template("publication.html", id=id, document_title=document_title,document_url=document_url)

@app.route('/about')
def about():
	return render_template("about.html")

'''@app.route('/testdb')
def testdb():
	db.create_all()
	return redirect(url_for('index'))
'''
