from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm


def home(request):
    boards = Board.objects.all()

    return render(request, "boards/home.html", {"boards": boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, "boards/topics.html", {"board": board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user_id = request.user.id
    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                topic=topic, message=form.cleaned_data.get("message"), created_by=user,
            )

            return redirect("boards:board_topics", pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, "boards/new_topic.html", {"board": board, "form": form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, "boards/topic_posts.html", {"topic": topic})
