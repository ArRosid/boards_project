from django.contrib import admin
from boards.models import Board, Post, Topic


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
