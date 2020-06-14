import flask
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    '''
    - functia returneaza template-ul ce reprezinta pagina de home a site-ului

    '''
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    - functia ce realizeaza inregistrarea unui cont
    - 'curent_user' ce este preluat din flask_login
    - cu ajutorul 'is_authenticated' se verifica daca contul
        ce incearca a se inregistra este deja in baza de date
        in caz pozitiv este redirectionat la pagina de home,
        altfel vor urma o serie de pasi explicati mai jos
    - se va crea un formular(acest formular reprezinta o clasa
        creata in documentul forms.py). Acesta va contine o parola
        criptata cu ajutorul 'bcrypt' ce provine din 'flaskblog',
        zona de confirmare a parolei, e-mail-ul propietarului
        si un username. Daca formularul este completat corect va
        aparea mesajul 'Your account has been created! You are now
        able to log in' si va fi redirectionat catre pagina de
        'login'. Alttfel se va reintra in pagina de register


    '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''

    - functia ce realizeaza login-ul pe pagina
    - cu ajutorul 'is_authenticated' se verifica daca contul
        ce incearca a se loga este deja logat pe pagina
        in caz pozitiv este redirectionat la pagina de home,
        altfel vor urma o serie de pasi explicati mai jos
    - se va crea un formular(acest formular reprezinta o clasa
        creata in documentul forms.py). In acest formular se va
        completa e-mail-ul, parola si de asemenea, va exista
        preferinta de a ramane tot timpul conectat, de a se retine
        datele de mai sus. 'generate_password_hash' scoate parola
        din forma criptata ce se afla in baza de date. Daca formularul
        este completat corect se accesa contul, in caz contrar va fi retrimis
        la pagina de log-in


    '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    '''
    - functia de log-out a paginii
    - se foloseste de functia logout_user() care este
        o functie provenita din flask_login
    - la final este redirectionat spre pagina de 'home'
    '''
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    '''
    - prin intermediul acesteia setam poza
        de profil a contului
    - poza primeste un nume randomizat si este
        salvata ca 125/125
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    '''
    - functia aceasta priveste modificarile ce se pot face
        la un cont
    - se va crea un formular(acest formular reprezinta o clasa
        creata in documentul forms.py). Acest formular contine
        username, e-mail si poza de profil. Formularul este
        completat tot timpul cu username-ul si e-mailul curent,
        iar in cazul in care se doreste a fi modificat, campul
        username-ului poate fi modificat, de asemenea si cel al
        e-mailului. Butonul de update verifica daca noul username
        sau e-mail se regasesc deja in baza de date, altfel sunt
        modificate pentru contul respectiv
    '''
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    '''
    - functia aceasta realizeaza o postare noua
        pe pagina
    - creeaza formularul care dupa ce este completat
        apare pe pagina de 'home' ca o noua postare
    '''
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    '''
    - functia prin care se creeaza o noua postare
    - returneaza template-ul post.html unde se poate
        creea o noua postare
    '''
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    '''
    - aceasta functie realizeaza modificari la o postare
    - precum in functiile de mai sus se creeaza un formular
        ce contine titlul si continutul postarii. Aceste
        campuri pot fi modificate.
    - db.session.commit() realizeaza modificarile
    - la final apare pagina cu postarea modificata

    '''
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    '''
    - aceasta functie sterge o postare anterioara
    - db.session.delete() sterge postarea
    - db.session.commit() realizeaza modificarile
    - la final este redirectionat catre pagina de home

    '''
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    '''
    - aceasta functie arata postarile unui
        user de pe pagina
    '''
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

