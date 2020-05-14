from django.test import TestCase
from django.urls import reverse, resolve
from boards.views import home, board_topics
from boards.models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.url = reverse("boards:home")

    def test_home_success_status_code(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_home_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, home)


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")

    def get_url(self, id):
        return reverse("boards:board_topics", kwargs={"id": id})

    def test_board_topics_success_status_code(self):
        """
            test board topics success status code
        """
        res = self.client.get(self.get_url(1))
        self.assertEqual(res.status_code, 200)

    def test_board_topics_not_found_status_code(self):
        """
            test board topics not found status code
        """
        res = self.client.get(self.get_url(99))
        self.assertEqual(res.status_code, 404)

    def test_board_topics_view(self):
        """
            test board topics view
        """
        view = resolve(self.get_url(1))
        self.assertEqual(view.func, board_topics)
