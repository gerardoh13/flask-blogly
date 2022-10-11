"""Models for Blogly."""
from ctypes.wintypes import tagSIZE
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png")

    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"

    def get_full_name(self):
        """returns users full name"""
        u = self
        return f"{u.first_name} {u.last_name}"

    full_name = property(fget=get_full_name)

class Post(db.Model):
    """Blog post class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts', cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

    def get_friendly_datetime(self):
        """returns date in standard format"""
        p = self
        return p.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

    def update_time(self):
        """returns current time for updated posts"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    friendly_datetime = property(fget=get_friendly_datetime)

class Tag(db.Model):
    """Tag class"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Show info about tag."""

        t = self
        return f"<Post {t.id} {t.name}>"

class PostTag(db.Model):
    """PostTag class"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        """Show info about tag."""

        pt = self
        return f"<Post {pt.id} {pt.name}>"