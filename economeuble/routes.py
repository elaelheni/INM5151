import os
import secrets
from PIL import Image
from flask import render_template, make_response, redirect, flash, url_for, abort, request
from economeuble import app, db, bcrypt
from flask import send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from economeuble.database import User, Article
from economeuble.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', articles=articles)


@app.route('/user/<string:username>')
def user_articles(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    articles = Article.query.filter_by(author=user).order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', articles=articles, user=user)


@app.route("/about")
def about():
    return render_template('about.html', title='A propos')

@app.route("/deco")
def deco():
    return render_template('deco.html', title='Decoration')

@app.route("/lit")
def lit():
    return render_template('chambres.html', title='Chambres')

@app.route("/meuble")
def meuble():
    return render_template('meubles.html', title='Interieur')

@app.route("/faq")
def faq():
    return render_template('faq.html', title='Foire de questions')

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['mot_rech']
        search = "%{0}%".format(search_value)
        results = Article.query.filter(Article.title.like(search)).all()
        return render_template ('search.html', articles=results, title='Resultat de la recherche')
    else:
        return redirect('/')



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


    return render_template('create_article.html', title='Nouvel article', form=form, legend='Nouvel article')

@app.route("/article/<int:article_id>")
def article(article_id):
    #donne moi l'article si il existe sinon un 404
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', title=article.title, article=article)

@app.route("/article/<int:article_id>/update", methods=['GET', 'POST'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.description = form.description.data
        article.title = form.description.data
        if form.picture.data():
            picture_file = save_article_picture(form.picture.data)
        db.session.commit()
        flash ("L'article a été mis à jour!", 'success')
        return redirect(url_for('article'), article_id=article.id)
    elif request.method == 'GET':
        form.title.data = article.title
        form.description.data = article.description
        form.price.data = article.price

    return render_template('create_article.html', title="Mettre à jour l'article", form=form, legend='Mettre à jour')

@app.route("/article/<int:article_id>/delete", methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash('Votre article a été supprimé!', 'success')
    return redirect(url_for('home'))
    
@app.route("/wish", methods=['POST', 'GET'])
@login_required
def wish_list():
    return render_template('wish.html', title="Liste d'envies")

@app.route("/cart", methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':

        flash("L'article a été ajouté avec succès à votre panier", 'success')
        return redirect(url_for('home'))

    return render_template('cart.html', title="Panier")

