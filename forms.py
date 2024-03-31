
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddUserForm(FlaskForm):
    """Form for creating user."""

    username = StringField("", 
                validators=[InputRequired(message="Enter a valid username")])
    password = StringField("", 
                validators=[InputRequired(message="Enter a valid password")])
    email = StringField("", 
                validators=[InputRequired(message="Enter a valid email")])
    first_name = StringField("", 
                validators=[InputRequired()])
    last_name = StringField("", 
                validators=[InputRequired()])
    
class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField("", 
                validators=[InputRequired(message="Enter a valid username")])
    password = StringField("", 
                validators=[InputRequired(message="Enter a valid password")])
    
class FeedbackForm(FlaskForm):
    """Form for adding feedback"""

    title = StringField("Title",
                        validators=[InputRequired(message="Please provide a title")])
    content = StringField("Content",
                          validators=[InputRequired(message="Feedback must be provided")])
    