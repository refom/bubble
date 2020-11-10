from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Search(FlaskForm):
	keyword = StringField('Search', validators=[DataRequired()])





