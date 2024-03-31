"""Flask app for Authenticating and Authorizing"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_auth'
app.config['SECRET_KEY'] = "my_big_secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)

toolbar = DebugToolbarExtension(app)



@app.route('/')
def home():
    return render_template("/index.html", session=session)

###################################### User Routes ###############################################

@app.route("/register", methods=["GET", "POST"])
def register():
    """Shows form to register user, then adds user to the Db"""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect("/users/<username>")
    
    else: #If form is not valid, error messages flash, but user input remains on the page.
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate and login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/users/<user_id>")

        else:
            form.username.errors = ["Incorrect username or password"]
    
    return render_template("login.html", form=form)


@app.route("/users/<username>")
def secret(username):
    """Hidden page only accessed after authenticating and, if authorized"""

    if "user_id" not in session:
        flash("Please login to view")
        return redirect("/")
    
    user = User.query.get_or_404(username)
    feedback = Feedback.query.get_or_404(username)

    return render_template("secret.html", user=user, feedback=feedback)

@app.route("/logout")
def logout():
    """Logs user out, clears session, and returns to homepage"""
    
    session.pop("user_id")

    return redirect("/")

##################################  Feedback Routes ####################################

@app.route("/feedback/<feedback_id>/update", methods=["GET", "PATCH"])
def update_feedback(feedback_id):
    """Updates a feedback entry"""

    if "user_id" not in session:
        flash("Please login to view")
        return redirect("/")
    
    entry = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=entry)

    if form.validate_on_submit():
        entry.title = form.title.data
        entry.content = form.content.data
        entry = Feedback()
        db.session.add()
        db.session.commit()

        return redirect("/")

    return render_template("feedback.html", entry=entry)

@app.route("/users/<username>/delete")
def delete_user():
    """Deletes a user"""
    return redirect("/")


@app.route("/users/<username>/feedback/add")
def add_feedback():
    """Add feedback"""

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Feedback(title=title, content=content)

        db.session.add(post)
        db.session.commit()

        return redirect("/users/<username>")
    else: 
        return render_template("feedback.html")
    
@app.route("/feedback/<feedback_id>/delete", methods=["DELETE"])
def delete_feedback(id):
    """Deletes a specific feedback post"""

    feedback = Feedback.query.get_or_404(id)

    db.session.delete(feedback)
    db.session.commit()

    return redirect("/users/<username>")