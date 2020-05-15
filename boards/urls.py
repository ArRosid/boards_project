from django.urls import path
from boards.views import home, board_topics, new_topic


app_name = "boards"


urlpatterns = [
    path("", home, name="home"),
    path("boards/<int:pk>/", board_topics, name="board_topics"),
    path("boards/<int:pk>/new/", new_topic, name="new_topics"),
]
