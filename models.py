"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database and set app context"""
    db.app = app
    db.init_app(app)
    app_ctx = app.app_context()
    app_ctx.push()
    db.create_all()

class User(db.Model):
    """User model"""

    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.Column(db.ForeignKey('feedback.id'))

    @classmethod
    def register(cls, username, pwd):
        """Register user w/ hashed password & return user."""

        hashed_pwd = bcrypt.generate_password_hash(pwd)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8_pwd = hashed_pwd.decode("utf8")

        # return instance of user w/ username and hashed password.
        return cls(username=username, password=hashed_utf8_pwd)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user and password."""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            #password hash checked; return user instance.
            return u
        else:
            return False



class Feedback(db.Model):
    """Feedback model"""

    __tablename__= "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey('users.username'))

    user = db.relationship(
        'User',
        secondary="users",
        backref="feedback"
    )

    def serialize(self):
        """Serializes the feedback into a dict, which can be JSONified"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'username': self.username
        }

    # def __repr__(self):
    #     return f"<Feedback {self.id} title={self.title} content={self.content} username={self.username}"