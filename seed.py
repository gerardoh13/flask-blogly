"""Seed file to make sample data for blogly db."""

from models import User, db
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

# Add new objects to session, so they'll persist
db.session.add(jannah)
db.session.add(gerardo)
db.session.add(rafael)
db.session.add(samantha)


# Commit--otherwise, this never gets saved!
db.session.commit()
