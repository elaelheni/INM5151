from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
	email = StringField ('Email', validators=[DataRequired(), Email()])
	password = StringField ('Password', validators=[DataRequired()])
	confirm_password = StringField (' Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	
	email = StringField ('Email', validators=[DataRequired(), Email()])
	password = StringField ('Password', validators=[DataRequired()])
	remeber = BooleanField('Remember Me')

	submit = SubmitField('Sign Up')
	
