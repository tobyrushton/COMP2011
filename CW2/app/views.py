from app import app, login_manager, models, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import SignUpForm, LogInForm

@app.route("/")
def index():
    return render_template('pages/index.html', title="Home", user_authenticated=current_user.is_authenticated)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

@app.route("/auth/<string:auth_type>", methods=['GET', 'POST'])
def auth(auth_type):
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