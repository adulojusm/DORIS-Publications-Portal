from flask.ext.wtf import Form
from wtforms import StringField, SelectField,SubmitField, validators
from wtforms import ValidationError


class SearchForm(Form):
	user_input = StringField(validators.InputRequired("Please enter a search entry."))
