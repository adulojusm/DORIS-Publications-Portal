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


@app.route('/testdb')
def testdb():
    date1 = datetime.date(2011,07,21)
    category = Category('Education')
    db.session.add(category)
    newdoc = Document(title='hello',description='this is a sample doc',datecreated=date1,filename='file',url='some url',
                      puborfoil= 'FOIL',num_access=0)
    newdoc.category = category
    db.session.add(newdoc)
    aquery = Document.query.join(Category).filter(Document.id == 1).first()
    
    aqueryBeginning = Document.query.join()
    aqueryNextStep = aqueryBeginning.filter(Document == 1)
    aqueryFinalStep = aqueryNextStep.first()
    
    db.session.commit()
    flash(str(aquery.title) + ' ' + str(aquery.cid))
    return redirect(url_for('index'))


#GOES IN A MODULE (LATER) ...

def process_query(search, _agency, _category, _types):

	a_results = Agency.query.all()
	c_results = Category.query.all()
	t_results = Type.query.all()
	
	if _agency != "All Agencies":
		a_results = Agency.query.filter(Agency.agency == _agency).first() #name
	if _category != "All Categories":
		c_results = Category.query.filter(Category.category == _category).first()
	if _types != "All Types":
		t_results = Type.query.filter(Type.type == _types).first()

	
	
	return None