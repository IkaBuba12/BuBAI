from models import Chat
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ext import app, db
from forms import LoginForm, RegisterForm
from models import User
from chat import get_ai_reply


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Use another email.', 'danger')
            return redirect(url_for('register'))
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    reply = ""
    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            reply = get_ai_reply(user_message)

            chat_entry = Chat(
                user_id=current_user.id,
                message=user_message,
                reply=reply
            )
            db.session.add(chat_entry)
            db.session.commit()

    history = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.desc()).all()
    return render_template("chat.html", reply=reply, history=history)