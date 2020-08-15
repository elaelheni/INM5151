from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from economeuble.database import User


class RegistrationForm(FlaskForm):

    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=6, max=12)])
    email = StringField ('Adresse mail', validators=[DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField ('Confirmation du mot de passe', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Cette adresse mail est déjà utilisée.")




class LoginForm(FlaskForm):
	
    email = StringField ('Adresse mail', validators=[DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')

    submit = SubmitField('Se connecter')


class UpdateAccountForm(FlaskForm):
    username = StringField("Nom d'utilisateur",
                           validators=[DataRequired(), Length(min=6, max=12)])
    email = StringField('Adresse mail',
                        validators=[DataRequired(), Email()])
    picture = FileField('Mettre à jour la photo de profil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Mettre à jour')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Ce nom d'utilisateur est déjà pris.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Cette adresse mail est déjà utilisée.")

	
class PostForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField("Ajoutez une photo de l'article", validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    price = StringField('Prix', validators=[DataRequired(), Length(min=3, max=10)])

    submit = SubmitField('Publier')


class UpdateForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField("Mettre à jour la photo de l'article" , validators=[FileAllowed(['jpg', 'png'])])
    price = StringField ('Mettre à jour le prix',validators=[Length(min=3, max=10)])

    submit = SubmitField('Mettre à jour')

class RequestResetForm(FlaskForm):
    email = StringField('Adresse mail',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Récuperer le mot de passe')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Aucun compte n'est relié à cette adresse mail. Pensez à vous inscrire!")

class ResetPasswordForm(FlaskForm):
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField ('Confirmation du mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Changer le mot de passe')





