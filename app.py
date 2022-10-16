"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post, Tag
from sqlalchemy import desc


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
    flash(f"User '{ user.full_name }' has been edited!")

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
    tags = Tag.query.all()
    return render_template("new-post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('id')

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{ new_post.title }' added!")
    for tag_id in tag_ids:
        tag = Tag.query.get_or_404(tag_id)
        new_post.tags.append(tag)
        db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Shows form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit-post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    tag_ids = request.form.getlist('id')
    remove_ids = request.form.getlist('remove_ids')
    post.title = request.form['title']
    post.content = request.form['content']
    post.created_at = post.update_time()

    remove_list = [x for x in [str(tag.id)
                               for tag in post.tags] if x not in remove_ids]
    for id in remove_list:
        removed_tag = Tag.query.get_or_404(id)
        post.tags.remove(removed_tag)

    db.session.add(post)
    for tag_id in tag_ids:
        tag = Tag.query.get_or_404(tag_id)
        post.tags.append(tag)
    db.session.commit()
    flash(f"Post '{ post.title }' has been edited!")
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
    """displays custom 404"""
    return render_template('404.html'), 404


@app.route("/tags")
def list_tags():
    """Displays a list of tags"""
    tags = Tag.query.all()
    return render_template("tags-list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tags(tag_id):
    """Shows tag of a given id"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag-details.html", tag=tag, posts=posts)


@app.route("/tags/new")
def show_tags_form():
    """Shows form to add new tag"""
    posts = Post.query.all()
    return render_template("new-tag.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Adds a tag and adds posts associated with it"""
    post_ids = request.form.getlist('id')
    name = request.form['name']

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{name}' has been added!")
    if post_ids:
        for post_id in post_ids:
            post = Post.query.get_or_404(post_id)
            post.tags.append(new_tag)
            db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Shows form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("edit-tag.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edits a tag and adds or removes posts associated with it"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = request.form.getlist('id')
    remove_ids = request.form.getlist('remove_ids')
    remove_list = [x for x in [str(post.id)
                               for post in tag.posts] if x not in remove_ids]

    for id in remove_list:
        removed_post = Post.query.get_or_404(id)
        tag.posts.remove(removed_post)

    for post_id in post_ids:
        post = Post.query.get_or_404(post_id)
        post.tags.append(tag)

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' has been edited!")

    return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """Deletes post of a given id"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Post '{ tag.name }' has been deleted!")
    return redirect("/tags")
