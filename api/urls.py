from django.urls import path

from . import views

app_name = 'v1'

urlpatterns = [
    path('notes/', views.NotesListView.as_view(), name='notes_list'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('tags/', views.TagsListView.as_view(), name='tags_list'),
    path('tags/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('topics/', views.TopicsListView.as_view(), name='topics_list'),
    path('topics/<str:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('comments_to/<int:note_id>/', views.CommentsListToNoteView.as_view(), name='comments_to_note'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('views/', views.ViewsQuantitiesListView.as_view(), name='views_list'),
    path('followers_quantities/', views.FollowersQuantitiesView.as_view(), name='followers_quantities'),
    path('followers/joined/', views.FollowersJoinedListView.as_view(), name='joined_followers'),
    path('followers/unsubscribed/', views.FollowersUnsubscribedListView.as_view(), name='unsubscribed_followers'),
]
