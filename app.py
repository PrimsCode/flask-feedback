from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECRET_KEY']="FEEDBACK"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/', methods=['GET'])
def root():
    return redirect('/register')  

@app.route('/register', methods=['GET', 'POST'])
def register_user_form():
    """Show register form and let user register"""
    
    if "user_id" in session:
        flash('Already logged in')
        userid = session['user_id']
        user = User.query.get_or_404(userid)
        return redirect(f'/users/{user.username}')

    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        flash('Registered')        
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Show login form and authenticate user login"""

    if "user_id" in session:
        flash('Already logged in')
        userid = session['user_id']
        user = User.query.get_or_404(userid)
        return redirect(f'/users/{user.username}')
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.autenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.first_name}")
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username or password']

    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout_user():
    """Log user out"""

    session.pop('user_id')
    return redirect('/')

@app.route('/users/<username>', methods=['GET'])
def show_secret(username):
    """Check autentication before showing the page"""

    user = User.query.filter_by(username=username).first()

    if "user_id" not in session:
        flash('Please login first')
        return redirect('/login')

    return render_template('secret.html', user=user, username=user.username)

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def feedback_form(username):
    """Show feedback form and authenticate user login"""

    user = User.query.filter_by(username=username).first()
    session['user_id'] = user.id
    feedbacks = Feedback.query.all()

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback has been added')
        return redirect(f'/feedback/{feedback.id}/update')
       
    if "user_id" not in session:
        flash('Please login first')
        return redirect('/login')
    
    return render_template('feedback_form.html', feedbacks=feedbacks, form=form, user=user)


@app.route('/users/<username>/delete')
def delete_user(username):
    """Check autentication before showing the page"""
    
    if "user_id" not in session:
        flash('Please login first')
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')

    flash(f'{user.username} is deleted')

    return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Update feedback and autenticate user login"""

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback has been added')
        return redirect(f'/users/{user.username}/feedback/add')
    
    if "user_id" not in session:
        flash('Please login first')
        return redirect('/login')
    
    return render_template('update_feedback.html', form=form, feedback=feedback, user=user)

@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    """Delete feedback and autenticate user login"""

    if "user_id" not in session:
        flash('Please login first')
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()

    flash('Feedback is deleted')

    return redirect('/')


