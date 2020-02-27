from django import template
from django.db.models import Count
from django.db.models import F
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from ..models import Topic, Note, Tag, ViewsQuantity

register = template.Library()


@register.simple_tag
def show_topics_list():
    return cache.get_or_set('notes_numbers_by_topic',
                            Topic.objects.annotate(number=Count(F('notes'))).order_by('name'))


@register.simple_tag
def show_tags_list():
    return cache.get_or_set('tags_list', Tag.objects.all())


@cache_page(86400)
@register.simple_tag
def show_popular_notes(count=3):
    views = ViewsQuantity.objects.order_by('-quantity')[:count]
    notes = [Note.objects.get(pk=view.note_id) for view in views]
    return notes


@register.simple_tag
def show_notes_by_years():
    return cache.get_or_set('notes_numbers_by_year',
                            Note.objects.annotate(number=Count(F('year'))).order_by('-year'))
