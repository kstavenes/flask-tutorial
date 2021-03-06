# The Testing Skeleton
import os
import flask
import Flaskr
import unittest
import tempfile

from flask import Response

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        Flaskr.app.config['TESTING'] = True
        self.app = Flaskr.app.test_client()
        Flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()

# The First Test
class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = Flaskr.app.test_client()
        Flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data


#Logging In and Out
    #Add the following two methods to your FlaskrTestCase class:

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

#Now we can easily test that logging in and out works and that it fails with invalid credentials.
    # Add this new test to the class:

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    # Test Adding Messages¶
    # We should also test that adding messages works. Add a new test method like this:

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

        # Here we check that HTML is allowed in the text but not in the title, which is the intended behavior.
        # Running that should now give us three passing tests:


        # Other Testing Tricks
        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Peter'):
            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'Peter'

    # All the other objects that are context bound can be used in the same way.

        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Peter'):
            app.preprocess_request()
            ...

    # This can be necessary to open database connections or something similar depending on how your application was designed.

        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Peter'):
            resp = Response('...')
            resp = app.process_response(resp)
            ...

# Faking Resources and Context
    def get_user(self):
        pass
        # user = getattr(g, 'user', None)
        # if user is None:
        #     user = fetch_current_user_from_database()
        #     g.user = user
        # return user

# # For a test it would be nice to override this user from the outside without having to change some code.
#     # This can trivially be accomplished with hooking the flask.appcontext_pushed signal:
#
# from contextlib import contextmanager
# from flask import appcontext_pushed
#
# @contextmanager
# def user_set(app, user):
#     def handler(sender, **kwargs):
#         g.user = user
#     with appcontext_pushed.connected_to(handler, app):
#         yield
#
# # And then to use it:
#
# from flask import json, jsonify
#
# @app.route('/users/me')
# def users_me():
#     return jsonify(username=g.user.username)
#
# with user_set(app, my_user):
#     with app.test_client() as c:
#         resp = c.get('/users/me')
#         data = json.loads(resp.data)
#         self.assert_equal(data['username'], my_user.username)
#
#  # Keeping the Context Around
#  # New in version 0.4.
#
#       app = flask.Flask(__name__)
#
#         with app.test_client() as c:
#             rv = c.get('/?tequila=42')
#             assert request.args['tequila'] == '42'
#
# # Accessing and Modifying Sessions
# # New in version 0.8.
#
# with app.test_client() as c:
#     rv = c.get('/')
#     assert flask.session['foo'] == 42
#
# # This however does not make it possible to also modify the session or to access the session before a request was fired.
# # Starting with Flask 0.8 we provide a so called “session transaction” which simulates the appropriate calls to open
# # a session in the context of the test client and to modify it. At the end of the transaction the session is stored.
# # This works independently of the session backend used:
#
# with app.test_client() as c:
#     with c.session_transaction() as sess:
#         sess['a_key'] = 'a value'
#
#     # once this is reached the session was stored
#
# # Note that in this case you have to use the sess object instead of the flask.session proxy.
# # The object however itself will provide the same interface.