from django.urls import path
from boards.views import home, board_topics, new_topic, topic_posts


app_name = "boards"


urlpatterns = [
    path("", home, name="home"),
    path("boards/<int:pk>/", board_topics, name="board_topics"),
    path("boards/<int:pk>/new/", new_topic, name="new_topics"),
    path("boards/<int:pk>/topics/<int:topic_pk>/", topic_posts, name="topic_posts"),
]
