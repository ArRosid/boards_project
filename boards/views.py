from django.shortcuts import render, get_object_or_404
from boards.models import Board


def home(request):
    boards = Board.objects.all()

    return render(request, "boards/home.html", {"boards": boards})


def board_topics(request, id):
    board = get_object_or_404(Board, id=id)
    return render(request, "boards/topics.html", {"board": board})
