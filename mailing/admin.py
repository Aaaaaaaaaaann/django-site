from django.contrib import admin

from .models import Follower


@admin.register(Follower)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('email', 'activated', 'joined', 'unsubscribed')
    list_filter = ('activated',)
    search_fields = ('joined', 'unsubscribed')
    ordering = ('joined',)
