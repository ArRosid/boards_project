from django.test import TestCase
from django.urls import reverse, resolve
from boards.views import home


class HomeTests(TestCase):
    def setUp(self):
        self.url = reverse("boards:home")

    def test_home_status_code(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_home_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, home)
