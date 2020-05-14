from django.urls import path
from boards.views import home


app_name = "boards"


urlpatterns = [path("", home, name="home")]
