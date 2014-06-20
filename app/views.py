from app import app
from flask import Flask, render_template, request, flash, url_for,redirect,make_response,session
from forms import SearchForm
from models import db, Document
import datetime
from sqlalchemy import or_
from query_functions import process_query


app.config['SECRET_KEY'] = 'F34TF$($e34D'

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
	session['active']= True
	if request.method == 'POST':

		search = request.form['user_input']
		if not search:
			flash('Please enter a search entry.')
			return redirect(url_for('index'))
		agency = request.form['agency']
		category = request.form['category']
		types = request.form['type']
		results = process_query(search, agency, category, types)
		length = len(results)

		return render_template("res.html", results = results, length=length, method='post')

	else:

		return render_template("res.html",session=session)


@app.route('/publication/<filename>', methods=['GET'])
def publication(filename):
	document = Document.query.filter(Document.filename == filename).first()
	document.num_access += 1
	db.session.commit()
	document_title = document.title
	# if len(document_title) > 70:
	# 	document_title = document_title[:70] + "..."
	return render_template("publication.html", filename=filename, document_title=document_title)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/testdb')
def testdb():
	db.create_all()
	return redirect(url_for('index'))

