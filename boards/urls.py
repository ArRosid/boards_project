from django.urls import path
from boards.views import home, board_topics


app_name = "boards"


urlpatterns = [
    path("", home, name="home"),
    path("boards/<int:id>/", board_topics, name="board_topics"),
]
