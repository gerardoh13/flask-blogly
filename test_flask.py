from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add test user and post."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Big", last_name="Chungus", image_url=None)
        db.session.add(user)
        db.session.commit()
        post = Post(title="Test Post",
                    content="This is a test of the emergency broadcast system", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """tests that users are listed in /users route"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Big Chungus', html)

    def test_show_user(self):
        """tests that user details are listed in /users/id route"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Big Chungus</h1>', html)

    def test_add_user(self):
        """tests that new users are added correctly"""
        with app.test_client() as client:
            d = {"first_name": "test", "last_name": "user", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/3">test user</a>', html)

    def test_edit_user(self):
        """tests that user details are modified correctly"""
        with app.test_client() as client:
            d = {"first_name": "Small", "last_name": "Chungus", "image_url": ""}
            resp = client.post(
                f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/users/{self.user_id}">Small Chungus</a>', html)

    def test_show_post(self):
        """tests that post details are displayed in /post/id route"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Post</h1>', html)

    def test_edit_post(self):
        """tests that post details are modified correctly"""
        with app.test_client() as client:
            d = {"title": "New Title", "content": "New Content"}
            resp = client.post(
                f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New Title</h1>', html)

    def test_add_post(self):
        """tests that new posts are added correctly"""
        with app.test_client() as client:
            d = {"title": "New Test Post", "content": "New Content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/posts/2">New Test Post</a>', html)
      
