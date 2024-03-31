"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

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

    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

class Feedback(db.Model):
    """Feedback model"""

    __tablename__= "feedback"

    id = db.Column(db.Integer, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.text, nullable=False)
    username = db.Column(db.Foreign_key('users.username'))

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

    def __repr__(self):
        return f"<Feedback {self.id} title={self.title} content={self.content} username={self.username}"