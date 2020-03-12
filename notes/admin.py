from django.contrib import admin

from .models import Topic, Note, Comment, Tag


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'year', 'active')
    list_filter = ('title', 'author', 'topic', 'active')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('author', 'title'), 'authorAsSlug': ('author',)}
    list_editable = ('active',)
    ordering = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'note', 'user', 'body'[:15], 'parent', 'answerTo', 'added', 'notifications')
    list_filter = ('note', 'added')
    list_display_links = ('body'[:15],)
    ordering = ('-added',)
