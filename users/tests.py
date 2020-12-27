from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.http import Http404
from django.urls import resolve
import json
from django.urls.exceptions import Resolver404

from users.models import Profile
from users.views import RegistrationView
from users.forms import SignUpForm


class ProfileTest(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")

        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.__str__(), user.username)


class ProfileRegistrationFormsTest(TestCase):

    def test_invalid_forms(self):

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {
                'data':{
                    'username': 'foo/bar',
                    'first_name': "waht",
                    "last_name": "what",
                    'email': 'foo@example.com',
                    "birth_date": "2000-10-10",
                    'password1': 'secret3123',
                    'password2': 'secret3123'},
                'error':
                    ('username', [u'{"username": [{"message": "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.", "code": "invalid"}]}'])
            },
            # Mismatched passwords.
            {
                'data': {
                    'username': 'foo',
                    'email': 'foo@example.com',
                    "birth_date": "2000-10-10",
                    'first_name': "waht",
                    "last_name": "what",
                    'password1': 'alksjdflaks',
                    'password2': 'baragsdfds'
                        },
                'error':
                    ('__all__', [r'''{"password2": [{"message": "The two password fields didn\u2019t match.", "code": "password_mismatch"}]}'''])
            },
            # Too common password
            {
                'data':
                    {'username': 'foo',
                     'email': 'foo@example.com',
                     "birth_date": "2000-10-10",
                     'first_name': "waht",
                     "last_name": "what",
                     'password1': 'asdfasdf',
                     'password2': 'asdfasdf'},
                'error':
                    ('password2', ['{"password2": [{"message": "This password is too common.", "code": "password_too_common"}]}'])
            },
            # Too short password
            {
                'data': {
                        'username': 'fo12o12',
                        'email': 'fofadso@example.com',
                        "birth_date": "2000-10-10",
                        'first_name': "waht",
                        "last_name": "what",
                        'password1': 'foo',
                        'password2': 'foo'
                        },
                'error':
                    ('password2', ['{"password2": [{"message": "This password is too short. It must contain at least 8 characters.", "code": "password_too_short"}]}'])
            },
            # Password too similar to the username
            {
                'data': {
                    'username': 'foofoofoo1',
                    'email': 'fofadso@example.com',
                    "birth_date": "2000-10-10",
                    'first_name': "waht",
                    "last_name": "what",
                    'password1': 'foofoofoo1',
                    'password2': 'foofoofoo1'
                        },
                'error':
                    ('password2', [
                        '{"password2": [{"message": "The password is too similar to the username.", "code": "password_too_similar"}]}'])
            },
            # Password too similar to email
            {
                'data': {
                    'username': 'fo12o12',
                    'email': 'foofoofoo@example.com',
                    "birth_date": "2000-10-10",
                    'first_name': "waht",
                    "last_name": "what",
                    'password1': 'foofoofoo',
                    'password2': 'foofoofoo'
                        },
                'error':
                    ('password2', [
                        '{"password2": [{"message": "The password is too similar to the email address.", "code": "password_too_similar"}]}'])
            }
            ]

        for invalid_dict in invalid_data_dicts:
            form = SignUpForm(data=invalid_dict['data'])
            self.assertEqual(form.errors.as_json(), invalid_dict['error'][1][0])
            self.failIf(form.is_valid())

        User = get_user_model()
        user1 = User.objects.create(username="taskbuster22", password="django-tutorial")

        form = SignUpForm(data={
                    'username': 'taskbuster22',
                    'email': 'fofasdfaso@example.com',
                    "birth_date": "2000-10-10",
                    'first_name': "waht",
                    "last_name": "what",
                    'password1': 'foofgfgoo11',
                    'password2': 'foofgfgoo11'
                        },)
        self.assertEqual('{"username": [{"message": "User already exists.", "code": ""}]}', form.errors.as_json())
        self.failIf(form.is_valid())

    def test_valid_form(self):
        form = SignUpForm(data={'username': "twhataaa",
                                'password1': 'django-tutorial1',
                                'password2': 'django-tutorial1',
                                'first_name': "test",
                                "last_name": "test",
                                "email": "teste@test.pl",
                                "birth_date": "2000-10-10"})
        self.failUnless(form.is_valid())


class UsersViewsTest(TestCase):
    longMessage = True
    view_class = RegistrationView

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="taskbuster", password="django-tutorial")

    def test_home_page(self):
        request = self.factory.get('/home')
        request.user = self.user
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        request = self.factory.get('/register')
        request.user = self.user
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_register(self):
        data = {'username': "taskbuster1",
                'password1': 'django-tutorial1',
                'password2': 'django-tutorial1',
                'first_name': "test",
                "last_name": "test",
                "email": "teste@test.pl",
                "birth_date": "2000-10-10"}
        request = getattr(self.factory, 'post')('/', data)
        request.user = AnonymousUser()
        response = self.view_class.as_view()(request, data)
        self.assertIn(response.status_code, [301, 302], "User registration request was not redirected.")
        self.assertEqual(response.url, "/home/")

    def test_existing_user_register(self):
        data = {'username': "taskbuster",
                'password1': 'django-tutorial1',
                'password2': 'django-tutorial1',
                'first_name': "test",
                "last_name": "test",
                "email": "teste@test.pl",
                "birth_date": "2000-10-10"}
        request = getattr(self.factory, 'post')('/', data)
        request.user = AnonymousUser()
        response = self.view_class.as_view()(request, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_rendered, False)
