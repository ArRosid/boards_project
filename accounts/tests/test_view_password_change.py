from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = "test"
        password = "Test@123"
        user = User.objects.create(
            username=username, email="test@email.com", password=password
        )
        self.url = reverse("accounts:password_change")
        self.client.force_login(user=user)
        self.res = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_resolves_correct_views(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, auth_views.PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.res, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.res.context.get("form")
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        """
            the view must contain four inputs: csrf, old_password,
            new_password1, new_password2
        :return:
        """
        self.assertContains(self.res, "<input", 4)
        self.assertContains(self.res, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse("accounts:password_change")
        login_url = reverse("accounts:login")
        res = self.client.get(url)
        self.assertRedirects(res, f"{login_url}?next={url}")


# class PasswordChangeTestCase(TestCase):
#     """
#         Base test case for form processing
#         accepts a 'data' dict to POST to the view.
#     """
#     def setUp(self, data={}):
#         self.user = User.objects.create(username="user", email="user@email.com", password="old_password")
#         self.url = reverse("accounts:password_change")
#         self.client.force_login(user=self.user)
#         print(data)
#         self.res = self.client.post(self.url, data)
#
#
# class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
#     def setUp(self):
#         super().setUp({
#             'old_password': 'old_password',
#             'new_password1': 'NewPassword123',
#             'new_password2': 'NewPassword123'
#         })
#
#
#     def test_redirection(self):
#         """
#             a valid form submission should redrect the user
#         :return:
#         """
#         form = self.res.context.get('form')
#         print(form.errors)
#         self.assertRedirects(self.res, reverse("accounts:password_change_done"))
#
#     def test_password_changed(self):
#         """
#             refresh the user instance from database to get the new password
#             hash updated by line change password view
#         :return:
#         """
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password("NewPassword123"))
#
#     def test_user_authentication(self):
#         """
#             create a new request to an arbitrary page.
#             the resulting response should now have an 'user' to its' context.
#             after successful sign up
#         :return:
#         """
#         res = self.client.get(reverse('boards:home'))
#         user = res.context.get('user')
#         self.assertTrue(user.is_authenticated)
#
#
# class InvalidPasswordChangeTests(PasswordChangeTestCase):
#     def test_status_code(self):
#         """
#             an invalid form submission should return to the same page
#         :return:
#         """
#         self.assertEqual(self.res.status_code, 200)
#
#     def test_form_errors(self):
#         form = self.res.context.get('form')
#         self.assertTrue(form.errors)
#
#     def test_password_didnt_changed(self):
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password("Test123"))
