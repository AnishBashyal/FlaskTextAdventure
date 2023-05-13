from flask import render_template, url_for, flash, redirect, request, Blueprint
from textadventure import db, bcrypt
from textadventure.user.forms import RegistrationForm, LoginForm, UpdateAcccountForm
from textadventure.models import User, StoryHead
from textadventure.user.utils import save_profile_pic
from flask_login import login_user, current_user, logout_user, login_required

user = Blueprint('user', __name__)

@user.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully Registered.... Now login  {form.username.data}!', category='success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@user.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {form.username.data}!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Sorry........ cannot remember you', category='danger')
    return render_template('login.html',form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAcccountForm()
    profile_pic = url_for('static', filename = 'profile_pics/' + current_user.profile_pic)
    if form.validate_on_submit():
        if form.profile_pic.data:
            image_filename = save_profile_pic(form.profile_pic.data, current_user.profile_pic)
            current_user.profile_pic = image_filename
        current_user.username = form.username.data
        db.session.commit()
        flash('Updated successfully', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        
    return render_template('account.html', profile_pic = profile_pic, form=form)

@user.route("/user/stories/<string:username>")
def user_stories(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    stories = StoryHead.query.filter_by(writer=user)\
        .order_by(StoryHead.date_created.desc())\
        .paginate(page = page, per_page = 4 )
    return render_template('user_stories.html', stories = stories, user = user)