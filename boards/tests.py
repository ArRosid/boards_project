from django.test import TestCase
from django.urls import reverse, resolve
from boards.views import home, board_topics
from boards.models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django board.")
        self.url = reverse("boards:home")
        self.res = self.client.get(self.url)

    def test_home_success_status_code(self):
        """
            Test home status code
        :return:
        """
        self.assertEqual(self.res.status_code, 200)

    def test_home_view(self):
        """
            test home view
        :return:
        """
        view = resolve(self.url)
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        """
            test home page contains link to tpics page
        """
        board_topics_url = reverse("boards:board_topics", kwargs={"id": self.board.id})
        self.assertContains(self.res, f'href="{board_topics_url}"')


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

    def test_board_topics_page_have_link_to_home_page(self):
        """
            test board page have link back to home page
        :return:
        """
        res = self.client.get(self.get_url(1))
        home_url = reverse("boards:home")
        self.assertContains(res, f'href="{home_url}"')
