from re import U
from click import password_option
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True, )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', cascade="all, delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hased password & return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into a normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')

        # return user with username and hashed password
        return cls(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_utf8)
    
    @classmethod
    def autenticate(cls, username, pwd):
        """Validate user and password. Return user if valid; else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

class Feedback(db.Model):

    __tablename__= "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))

    user = db.relationship('User', backref="feedback")

