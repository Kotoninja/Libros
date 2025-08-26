from django.test import TestCase
from user.forms import LoginForm, RegistrationForm


class LoginFormTests(TestCase):
    def test_login_valid_data(self):
        form_data = {"username": "Bob", "password": "test"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class RegistrationFormTests(TestCase):
    def test_registaration_valid_data(self):
        form_data = {
            "username": "Bob",
            "email": "Bob@Bobemail.com",
            "password": "Bobqwerty",
            "repeat_password": "Bobqwerty",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_registration_invalid_email(self):
        form_data = {
            "username": "Bob",
            "email": "invalidemail",
            "password": "Bobqwerty",
            "repeat_password": "Bobqwerty",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        