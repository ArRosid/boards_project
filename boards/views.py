from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from boards.models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()

    return render(request, "boards/home.html", {"boards": boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, "boards/topics.html", {"board": board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        user_id = request.user.id
        user = User.objects.get(pk=user_id)

        topic = Topic.objects.create(subject=subject, board=board, starter=user)

        post = Post.objects.create(topic=topic, message=message, created_by=user,)

        return redirect("boards:board_topics", pk=board.pk)

    return render(request, "boards/new_topic.html", {"board": board})
