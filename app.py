"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = "Cats_are_cool!"
debug = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():
    """Shows the home page"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Displays a list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users-list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)


@app.route("/users/new")
def new_user_form():
    """Shows a form to a add a new user"""
    return render_template("new-user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds a new user to db and redirects to list of users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Shows edit user form."""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Updates user details in db"""
    user = User.query.filter(User.id == user_id).first()
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a user and redirects to users list"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/users")
