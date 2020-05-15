from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm


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
        board_topics_url = reverse("boards:board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.res, f'href="{board_topics_url}"')


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django board.")

    def get_url(self, pk=1):
        return reverse("boards:board_topics", kwargs={"pk": pk})

    def test_board_topics_success_status_code(self):
        """
            test board topics success status code
        """
        res = self.client.get(self.get_url())
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
        view = resolve(self.get_url())
        self.assertEqual(view.func, board_topics)

    def test_board_topics_page_have_navigation_link(self):
        """
            test board page have navigation link
        :return:
        """
        res = self.client.get(self.get_url())
        home_url = reverse("boards:home")
        new_topic_url = reverse("boards:new_topics", kwargs={"pk": self.board.pk})
        self.assertContains(res, f'href="{home_url}"')
        self.assertContains(res, f'href="{new_topic_url}"')


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")
        user = User.objects.create(username="test", password="password123",)
        self.client.force_login(user=user)

    def get_url(self, pk=1):
        return reverse("boards:new_topics", kwargs={"pk": pk})

    def test_new_topic_success_status_code(self):
        """
            test new topic success status code
        :return:
        """
        res = self.client.get(self.get_url())
        self.assertEqual(res.status_code, 200)

    def test_new_topic_not_found_status_code(self):
        """
            test new topic not found status code
        :return:
        """
        res = self.client.get(self.get_url(99))
        self.assertEqual(res.status_code, 404)

    def test_new_topic_view(self):
        """
            test new topic view
        :return:
        """
        view = resolve(self.get_url())
        self.assertEqual(view.func, new_topic)

    def test_new_topic_containes_link_back_to_board_view(self):
        """
            test new topic page have link back to board page
        :return:
        """
        board_topic_url = reverse("boards:board_topics", kwargs={"pk": 1})
        res = self.client.get(self.get_url())
        self.assertContains(res, f'href="{board_topic_url}"')

    def test_csrf(self):
        """
            test csrf
        :return:
        """
        res = self.client.get(self.get_url())
        self.assertContains(res, "csrfmiddlewaretoken")

    def test_new_topic_vlaid_post_data(self):
        """
            test new topic valid post data
        :return:
        """
        subject = "Test subject"
        message = "Test message"
        data = {
            "subject": subject,
            "message": message,
        }
        self.client.post(self.get_url(), data)
        topic = Topic.objects.get(subject=subject)
        post = Post.objects.get(message=message)
        self.assertEqual(topic.subject, subject)
        self.assertEqual(post.message, message)

    def test_new_topic_invalid_post_data(self):
        """
            invalid post data should not redirect
            the expected behavior is to show the form again with validation errors
        :return:
        """
        res = self.client.post(self.get_url(), {})
        form = res.context.get("form")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
            invalid post data should not redirect
            if the field empty, topic & post should not created
        :return:
        """
        data = {"subject": "", "message": ""}
        res = self.client.post(self.get_url(), data)
        form = res.context.get("form")
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        self.assertTrue(form.errors)

    def test_contains_form(self):
        """
            test new topic page contains form
        :return:
        """
        res = self.client.get(self.get_url())
        form = res.context.get("form")
        self.assertIsInstance(form, NewTopicForm)
