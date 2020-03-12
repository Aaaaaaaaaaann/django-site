from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.NotesListView.as_view(), name='notes_list'),
    path('search/', views.search, name='search'),
    path('contact/', views.SendMailToAdminView.as_view(), name='contact'),
    path('about', TemplateView.as_view(template_name='notes/about.html'), name='about'),
    path('<slug:slug>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('by_subgenre/<str:subgenre>/', views.SubgenreNotesView.as_view(), name='notes_by_subgenre'),
    path('by_topic/<slug:slug>/', views.TopicalNotesView.as_view(), name='notes_by_topic'),
    path('by_tag/<slug:slug>/', views.TaggableNotesView.as_view(), name='notes_by_tag'),
    path('by_year/<int:year>/', views.AnnualNotesView.as_view(), name='notes_by_year'),
    path('by_author/<str:authorAsSlug>/', views.AuthorsNotesView.as_view(), name='notes_by_author'),
    path('unsubscribe_from_answers/<str:email>/', views.unsubscribe_from_answers, name='unsubscribe_from_answers'),
]
