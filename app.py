"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = "Cats_are_cool!"
debug = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():
    """Shows the home page"""
    posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    return render_template("home.html", posts=posts)


@app.route("/users")
def list_users():
    """Displays a list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users-list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user, posts=user.posts)


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
    flash(f"User '{ new_user.full_name }' added!")
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
    flash(f"User '{ user.full_name }' modified!")

    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a user and redirects to users list"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{ user.full_name }' has been deleted!")
    return redirect("/users")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Shows post of a given id"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post-details.html", post=post, user=user)

@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Shows form to add new post"""
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{ new_post.title }' added!")
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Shows form to edit a post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("edit-post.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    post.title = request.form['title']
    post.content = request.form['content']
    post.created_at = post.update_time()
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{ post.title }' modified!")
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Deletes post of a given id"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{ post.title }' has been deleted!")
    return redirect(f"/users/{user_id}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404