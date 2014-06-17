from app import app
from flask import Flask, render_template, request, flash, url_for,redirect,make_response
from forms import SearchForm
from models import db,Agency,Category,Type,Document
import datetime

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
            flash("Please enter a search")
            return redirect(url_for('index'))
        agency = request.form['agency']
        category = request.form['category']
        types = request.form['type']
        return render_template("res.html", search=search, agency=agency, category=category, types=types, method='post')

    else:

        return render_template("res.html")


@app.route('/publication', methods=['GET'])
def publication():
    return render_template("publication.html")

@app.route('/about')
def about():
	return render_template("about.html")

'''
@app.route('/testdb')
def testdb():
    date1 = datetime.date(2011,07,21)
    newdoc = Document(title='hello',description='this is a sample doc',datecreated=date1,filename='file',url='some url',
                      porf='FOIL',num_access=0)
    newdoc.aid=1
    newdoc.cid=1
    newdoc.tid=1
    db.session.add(newdoc)
    db.session.commit()
    return redirect(url_for('index')
    )
    '''