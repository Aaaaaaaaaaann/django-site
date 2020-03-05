from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('notes/', views.NoteListView.as_view(), name='notes_list'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('tags/', views.TagListView.as_view(), name='tags_list'),
    path('tags/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('topics/', views.TopicListView.as_view(), name='topics_list'),
    path('topics/<str:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('comments_to/<int:note_id>/', views.CommentListToNoteView.as_view(), name='comments_to_note'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('views/', views.ViewsQuantityListView.as_view(), name='views_list'),
]
