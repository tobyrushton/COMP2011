from app import app, login_manager, models, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .forms import SignUpForm, LogInForm, CreatePostForm
import json
from .posts import get_posts, get_recommendations

@app.route("/")
def index():
    # redirect authenticated users to feed 
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('pages/index.html', title="Home", user_authenticated=current_user.is_authenticated)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

@app.route("/auth/<string:auth_type>", methods=['GET', 'POST'])
def auth(auth_type):
    # redirect authenticated users to feed
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    # create the form based on the auth type
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

            return redirect(url_for('auth', auth_type="login"))
        else:
            # find the user and check the password
            user = db.session.query(models.User).filter_by(username=form.username.data).first()
            if user and user.password_hash == form.password.data:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')
    
    return render_template('pages/auth.html', title="Auth", auth_type=auth_type, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth', auth_type="login"))

@app.route("/feed")
@login_required
def feed():
    # get random list of posts
    posts = get_recommendations(current_user)
    return render_template('pages/feed.html', title="Feed", user_authenticated=current_user.is_authenticated, posts=posts)

@app.route("/post", methods=['POST'])
@login_required
def post():
    # get the post body from the request
    data = json.loads(request.data)
    body = data.get('body')

    # check if the post is empty
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
    # get the user based on the username
    user = current_user if not username else db.session.query(models.User).filter_by(username=username).first()
    
    if user:
        posts = []

        #  set the posts
        if not likes:
            posts = get_posts(current_user).order_by(models.Post.posted_at.desc()).filter(models.Post.user_id == user.id).all()
        else:
            posts = get_posts(current_user).filter_by(user_id=user.id).all()
        return render_template('pages/profile.html', title="Profile", user_authenticated=current_user.is_authenticated, user=user, likes=likes, posts=posts)
    else: # if user does not exist take them back to the feed
        return redirect(url_for('feed'))

@app.route("/like", methods=['POST'])
@login_required
def like():
    # get the post id from the request
    data = json.loads(request.data)
    post_id = data.get('id')
    post = db.session.query(models.Post).get(post_id)

    if post:
        # check if the user has already liked the post
        like = db.session.query(models.Like).filter_by(post=post, user=current_user).first()
        operation = "delete" if like else "add"

        # delete/add accordingly
        if like:
            db.session.delete(like)
        else:
            new_like = models.Like(post=post, user=current_user)
            db.session.add(new_like)
        
        db.session.commit()
        return jsonify({'status': 'success', 'operation': operation})
    else:
        return jsonify({'status': 'error', 'message': 'Post does not exist.'})

@app.route("/post/<int:id>", methods=['GET', 'POST'])
@login_required
def post_detail(id):
    # get the post and comments
    post = get_posts(current_user).filter(models.Post.id == id).first()
    comments = db.session.query(models.Comment).filter(models.Comment.post_id == id).all()
    # create the form
    form = CreatePostForm()

    # check if the form is submitted and create a new comment if so
    if form.validate_on_submit():
        new_comment = models.Comment(body=form.body.data, user_id=current_user.id, post_id=id)
        db.session.add(new_comment)
        db.session.commit()

    return render_template('pages/post.html', title="Post", user_authenticated=current_user.is_authenticated, post=post, form=form, comments=comments)