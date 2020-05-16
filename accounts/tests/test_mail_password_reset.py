from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        url = reverse("accounts:password_reset")
        User.objects.create(username="test", email="test@email.com", password="Test123")
        self.res = self.client.post(url, {"email": "test@email.com"})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(
            "[Django Boards] Please reset your password", self.email.subject
        )

    def test_email_body(self):
        context = self.res.context
        token = context.get("token")
        uid = context.get("uid")
        password_reset_token_url = reverse(
            "accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token,}
        )
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn("test", self.email.body)
        self.assertIn("test@email.com", self.email.body)

    def test_email_to(self):
        self.assertEqual(["test@email.com",], self.email.to)
