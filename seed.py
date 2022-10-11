"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
jannah = User(first_name='Jannah', last_name="Huerta")
gerardo = User(first_name='Gerardo', last_name="Huerta")
rafael = User(first_name='Rafael', last_name="Huerta")
samantha = User(first_name='Samantha', last_name="Huerta")

db.session.add_all([jannah, gerardo, rafael, samantha])
db.session.commit()

post1 = Post(title="first Post", content="This is a test of the emergency broadcast system", user_id=jannah.id)
post2 = Post(title="Meow", content="I'm Sam the Cat. give me treats.", user_id=samantha.id)
post3 = Post(title="Hi I'm Gerardo!", content="I love my family and coding!", user_id=gerardo.id)
post4 = Post(title="Hi I'm Jannah!", content="I love my husband Gerardo, my baby Rafa, and my kitty Sam", user_id=jannah.id)
post5 = Post(title="Hi I'm Rafa!", content="I'm the cutest little baby!", user_id=rafael.id)
post6 = Post(title="It's Corn!", content="It's got the juice!", user_id=gerardo.id)

db.session.add_all([post1, post2, post3, post4, post5, post6])
# Commit--otherwise, this never gets saved!
db.session.commit()

tag1 = Tag(name="family")

db.session.add(tag1)
db.session.commit()

post_tag1 = PostTag(post_id=post3.id, tag_id=tag1.id)
db.session.add(post_tag1)
db.session.commit()