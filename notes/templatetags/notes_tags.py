from django import template
from django.db.models import Count
from django.db.models import F
from django.core.cache import cache

from ..models import Topic, Note, Tag, ViewsQuantity

register = template.Library()


@register.simple_tag
def show_topics_list():
    return Topic.objects.annotate(number=Count(F('notes'))).order_by('name')


@register.simple_tag
def show_tags_list():
    return Tag.objects.all()


@register.simple_tag
def show_popular_notes(count=3):
    views = ViewsQuantity.objects.order_by('-quantity')[:count]
    return [Note.objects.get(pk=view.note_id) for view in views]


@register.simple_tag
def show_notes_by_years():
    return Note.objects.annotate(number=Count(F('year'))).order_by('-year')
