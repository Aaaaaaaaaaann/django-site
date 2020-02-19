from django.urls import path

from . import views


app_name = 'mailing'
urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('activate/<str:sign>/', views.activate, name='activate'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
]
