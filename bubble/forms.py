from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Search(FlaskForm):
	keyword = StringField('Search', validators=[DataRequired()])





