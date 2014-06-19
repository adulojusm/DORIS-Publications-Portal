from app import app
from flask import Flask, render_template, request, flash, url_for,redirect,make_response
from forms import SearchForm
from models import db, Document
import datetime
from sqlalchemy import or_
from query_functions import process_query

app.secret_key = 'development key'

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template("index.html", form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':

		search = request.form['user_input']
		if not search:
			flash('Please enter a search entry.')
			return redirect(url_for('index'))
		agency = request.form['agency']
		category = request.form['category']
		types = request.form['type']
		
		results = process_query(search, agency, category, types)
		
		return render_template("res.html", results = results, method='post')

	else:

		return render_template("res.html")


@app.route('/publication', methods=['GET'])
def publication():
	return render_template("publication.html")

@app.route('/about')
def about():
	return render_template("about.html")

'''@app.route('/testdb')
def testdb():
	db.create_all()
	return redirect(url_for('index'))
'''
