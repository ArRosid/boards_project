from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from accounts.views import signup
from accounts.forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")
        self.view = resolve(self.url)
        self.res = self.client.get(self.url)

    def test_signup_success_status_code(self):
        """
            test signup success status code
        :return:
        """
        self.assertEqual(self.res.status_code, 200)

    def test_signup_view(self):
        """
            test signup view
        :return:
        """
        self.assertEqual(self.view.func, signup)

    def test_csrf(self):
        """
            test csrf
        :return:
        """
        self.assertContains(self.res, "csrfmiddlewaretoken")

    def test_contains_form(self):
        """
            test signup view contains form
        :return:
        """
        form = self.res.context.get("form")
        self.assertIsInstance(form, SignUpForm)

    def test_form_input(self):
        """
            the view must contains five inputs: csrf, username,
            password1, password2, email
        :return:
        """
        self.assertContains(self.res, "<input", 5)
        self.assertContains(self.res, 'type="text"', 1)
        self.assertContains(self.res, 'type="email"', 1)
        self.assertContains(self.res, 'type="password"', 2)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse("accounts:signup")
        self.res = self.client.post(url, {})

    def test_signup_status_code(self):
        """
            test post request with invalid data
            should return 200 to the same page
        :return:
        """
        self.assertEqual(self.res.status_code, 200)

    def test_form_errors(self):
        """
            test form error,
            form should contains errors
        :return:
        """
        form = self.res.context.get("form")
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        """
            user should not created
        :return:
        """
        self.assertFalse(User.objects.exists())


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse("accounts:signup")
        data = {
            "username": "test",
            "email": "test@email.com",
            "password1": "passw",
            "password2": "passw",
        }
        self.res = self.client.post(url, data)
        self.home_url = reverse("boards:home")
