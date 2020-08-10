import os
import secrets
from PIL import Image
from flask import render_template, make_response, redirect, flash, url_for, abort, request
from economeuble import app, db, bcrypt
from flask import send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from economeuble.database import User, Article
from economeuble.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm




@app.route('/')
@app.route('/home')
def home():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@app.route("/about")
def about():
    return render_template('about.html', title='A propos')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Inscriptionr', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #si next_page existe on la retourne sinon on retourne la page d'acceiul
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Connexion impossible, merci de vérifier votre adresse mail et votre mot de passe.', 'danger')
    return render_template('login.html', title='Connexion', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):

    #au cas ou le nom de l'image existe sur mon disque
    random_hex = secrets.token_hex(8)

    #je n'aurais pas besoin d'utiliser f_name je la remplace par _ pour pas
    #lever d'erreurs
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #resizing the pic, pour eviter que le site soit leeent
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_article_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/articlepics', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_profile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Votre compte est à jour!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_profile)
    return render_template('account.html', title='Compte',
                           image_file=image_file, form=form)

@app.route("/article/new", methods=['GET', 'POST'])
@login_required
def new_article():
    form = PostForm()
    if form.validate_on_submit():
        
        picture_file = save_article_picture(form.picture.data)
        article = Article(title=form.title.data, description=form.description.data, picture=picture_file, price=form.price.data, author=current_user)
        db.session.add(article)
        db.session.commit()

        image_f = url_for('static', filename='articlepics/' + article.picture)
        flash('Votre article a été publié', 'success')
        return redirect(url_for('home'))


    return render_template('create_article.html', title='Nouvel article', form=form, legend='Nouveau poste')

@app.route("/article/<int:article_id>")
def article(article_id):
    #donne moi l'article si il existe sinon un 404
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', title=article.title, article=article)

@app.route("/article/<int:article_id>/update")
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form = PostForm()
    return render_template('create_article.html', title="Mettre à jour l'article", form=form, legend='Mettre à jour')

    



