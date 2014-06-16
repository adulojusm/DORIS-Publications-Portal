from app import app
from flask import Flask, render_template, request, flash
from forms import SearchForm


app.secret_key = 'development key'

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
    form = SearchForm()
    '''if form.user_input is None:
        flash('Please enter a search entry.')
    else:'''
    return render_template("index.html", form=form)




@app.route('/results', methods=['GET', 'POST'])
def results():

        search = request.form['user_input']
        agency = request.form['agency']
        category = request.form['category']
        types = request.form['type']
        return render_template("res.html", search=search, agency=agency, category=category, types=types, method='post')


@app.route('/publication')
def publication():
    return render_template("publication.html")

@app.route('/about')
def about():
	return render_template("about.html")