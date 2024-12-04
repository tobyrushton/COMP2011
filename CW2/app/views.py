from app import app, login_manager, models, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .forms import SignUpForm, LogInForm
import json

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('pages/index.html', title="Home", user_authenticated=current_user.is_authenticated)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

@app.route("/auth/<string:auth_type>", methods=['GET', 'POST'])
def auth(auth_type):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LogInForm() if auth_type == "login" else SignUpForm()

    if form.validate_on_submit():
        if auth_type == "register":
            # check if the user already exists
            if db.session.query(models.User).filter_by(username=form.username.data).first():
                flash('User already exists.', 'danger')
                return redirect(url_for('auth', auth_type="login"))
            
            # create the new user
            new = models.User(username=form.username.data, password_hash=form.password.data)
            db.session.add(new)
            db.session.commit()

            return redirect(url_for('index'))
        else:
            user = db.session.query(models.User).filter_by(username=form.username.data).first()
            if user and user.password_hash == form.password.data:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('auth', auth_type="login"))
    
    return render_template('pages/auth.html', title="Auth", auth_type=auth_type, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth', auth_type="login"))

@app.route("/feed")
@login_required
def feed():
    return render_template('pages/feed.html', title="Feed", user_authenticated=current_user.is_authenticated)

@app.route("/post", methods=['POST'])
@login_required
def post():
    data = json.loads(request.data)
    body = data.get('body')

    if len(body) > 0:
        new_post = models.Post(body=body, user=current_user)
        db.session.add(new_post)
        db.session.commit()
    else:
        return jsonify({'status': 'error', 'message': 'Post cannot be empty.'}) 

    return jsonify({'status': 'success'})

@app.route("/profile")
@app.route("/profile/<string:username>")
@app.route("/profile/<string:username>/<string:likes>")
@login_required
def profile(username=None, likes=None):
    user = current_user if not username else db.session.query(models.User).filter_by(username=username).first()
    
    if user:
        posts = []

        if not likes:
            posts = db.session.query(models.Post).order_by(models.Post.posted_at.desc()).filter_by(user=user).all()
        return render_template('pages/profile.html', title="Profile", user_authenticated=current_user.is_authenticated, user=user, likes=likes, posts=posts)
    else:
        return redirect(url_for('feed'))