# -*- coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    img_url = StringField('Image URL', validators=[DataRequired()])
    #relationship = StringField('Predicate', validators=[DataRequired()])
    #object = StringField('Object', validators=[DataRequired()])
    submit = SubmitField('Search')
