from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginPageTest(TestCase):
    USERNAME = "Bob"
    PASSWORD = "Bobqwerty"
    EMAIL = "Bob@Bob.com"

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.USERNAME, password=cls.PASSWORD, email=cls.EMAIL
        )

    def test_status_code_and_template_login_page(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_send_full_form(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(str(response.context["user"]), "AnonymousUser")

        response = self.client.post(
            reverse("user:login"),
            {"username": self.USERNAME, "password": self.PASSWORD},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("library:home"))

        response = self.client.get(reverse("user:profile"))
        self.assertEqual(str(response.context["user"]), self.USERNAME)

    def test_send_invalid_username_but_correct_password(self):
        response = self.client.post(
            reverse("user:login"), {"username": "blalba", "password": self.PASSWORD}
        )
        self.assertContains(
            response, "Incorrect username or password. Please submit the form again."
        )

    def test_send_invalid_password_but_correct_username(self):
        response = self.client.post(
            reverse("user:login"), {"username": self.USERNAME, "password": "blabla"}
        )
        self.assertContains(
            response, "Incorrect username or password. Please submit the form again."
        )

    def test_send_invalid_password_but_invalid_username(self):
        response = self.client.post(
            reverse("user:login"), {"username": "blabla", "password": "blabla"}
        )
        self.assertContains(
            response, "Incorrect username or password. Please submit the form again."
        )


class RegistrationPageTest(TestCase):
    USERNAME = "Omarov"
    PASSWORD = "Omarovqwerty"
    EMAIL = "Omarov@omarov.com"

    USERNAME_SECOND = "Bob"
    PASSWORD_SECOND = "Bobqwerty"
    EMAIL_SECOND = "TestEmail@example.com"

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.USERNAME_SECOND,
            password=cls.PASSWORD_SECOND,
            email=cls.EMAIL_SECOND,
        )

    def test_status_code_and_template_registration_page(self):
        response = self.client.get(reverse("user:registration"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/registration.html")

    def test_send_full_form(self):
        users_before = User.objects.count()
        response = self.client.post(
            reverse("user:registration"),
            {
                "username": self.USERNAME,
                "email": self.EMAIL,
                "password": self.PASSWORD,
                "repeat_password": self.PASSWORD,
            },
        )
        users_after = User.objects.count()
        self.assertEqual((users_after - users_before), 1)
        self.assertRedirects(response, reverse("user:login"))

    def test_invalid_repeat_password(self):
        response = self.client.post(
            reverse("user:registration"),
            {
                "username": self.USERNAME,
                "email": self.EMAIL,
                "password": self.PASSWORD,
                "repeat_password": "blabla",
            },
        )
        self.assertContains(
            response,
            "Passwords did not occur. Please enter the same passwords in both fields.",
        )
        self.assertEqual(response.status_code, 200)

    def test_already_username_exist(self):
        response = self.client.post(
            reverse("user:registration"),
            {
                "username": self.USERNAME_SECOND,
                "email": self.EMAIL,
                "password": self.PASSWORD,
                "repeat_password": self.PASSWORD,
            },
        )
        self.assertContains(response, "This Username already exist")
        self.assertEqual(response.status_code, 200)

    def test_already_email_exist(self):
        response = self.client.post(
            reverse("user:registration"),
            {
                "username": self.USERNAME,
                "email": self.EMAIL_SECOND,
                "password": self.PASSWORD,
                "repeat_password": self.PASSWORD,
            },
        )
        self.assertContains(response, "This Email already exist")
        self.assertEqual(response.status_code, 200)


class ProfilePageTest(TestCase):
    USERNAME = "Bob"
    PASSWORD = "Bobqwerty"
    EMAIL = "Bob@Bob.com"

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.USERNAME, password=cls.PASSWORD, email=cls.EMAIL
        )

    def test_for_non_auth_user(self):
        response = self.client.get(reverse("user:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('user:login')}?next={reverse('user:profile')}"
        )

    def test_for_auth_user(self):
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.get(reverse("user:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")
        self.assertContains(response, str(reverse("user:logout")))


class LogoutTest(TestCase):
    USERNAME = "Bob"
    PASSWORD = "Bobqwerty"
    EMAIL = "Bob@Bob.com"

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.USERNAME, password=cls.PASSWORD, email=cls.EMAIL
        )

    def test_logout(self):
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.post(reverse("user:logout"))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("user:login"))
        response = self.client.get(reverse("library:home"))
        self.assertEqual(str(response.context["user"]),"AnonymousUser")