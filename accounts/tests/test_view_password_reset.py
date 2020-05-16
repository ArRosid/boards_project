from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        self.url = reverse("accounts:password_reset")
        self.res = self.client.get(self.url)
        self.view = resolve(self.url)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view_func(self):
        self.assertEqual(self.view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.res, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.res.context.get("form")
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """
            the view must contain two inputs: csrf and email
        :return:
        """
        self.assertContains(self.res, "<input", 2)
        self.assertContains(self.res, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = "test@email.com"
        User.objects.create(username="test", email=email, password="Test123")
        url = reverse("accounts:password_reset")
        self.res = self.client.post(url, {"email": email})

    def test_redirection(self):
        """
            a valid form submission should redirect the user
            to 'password_reset_done' view
        :return:
        """
        done_url = reverse("accounts:password_reset_done")
        self.assertRedirects(self.res, done_url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse("accounts:password_reset")
        self.res = self.client.post(url, {"email": "donotexist@email.com"})

    def test_redirection(self):
        """
            even invalid emails in the database should
            redirect the user to 'password_reset-done' view
        :return:
        """
        done_url = reverse("accounts:password_reset_done")
        self.assertRedirects(self.res, done_url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        self.url = reverse("accounts:password_reset_done")
        self.res = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="test", email="test@email.com", password="Test123"
        )
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        self.url = reverse(
            "accounts:password_reset_confirm",
            kwargs={"uidb64": self.uid, "token": self.token},
        )
        self.res = self.client.get(self.url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view_func(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.res, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.res.context.get("form")
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        """
            the view must contain three inputs: csrf and two password fields
        :return:
        """
        self.assertContains(self.res, "<input", 3)
        self.assertContains(self.res, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="test", email="test@email.com", password="Test123"
        )
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        """
            invalidate the token by changin the password
        """
        user.set_password("NewPassword123")
        user.save()

        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={"uidb64": self.uid, "token": self.token},
        )
        self.res = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_html(self):
        password_reset_url = reverse("accounts:password_reset")
        self.assertContains(self.res, "invalid password reset link")
        self.assertContains(self.res, f'href="{password_reset_url}"')


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse("accounts:password_reset_complete")
        self.res = self.client.get(url)
        self.view = resolve(url)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view_function(self):
        self.assertEqual(
            self.view.func.view_class, auth_views.PasswordResetCompleteView
        )
