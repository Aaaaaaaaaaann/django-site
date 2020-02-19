from django import template
from django.db.models import Count
from django.db.models import F
from django.core.cache import cache

from ..models import Topic, Note, Tag

register = template.Library()


@register.simple_tag
def show_topics_list():
    return cache.get_or_set('notes_numbers_by_topic',
                            Topic.objects.annotate(number=Count(F('notes'))).order_by('name'))


@register.simple_tag
def show_tags_list():
    return cache.get_or_set('tags_list', Tag.objects.all())


@register.simple_tag
def show_most_commented_notes(count=3):
    return cache.get_or_set('most_commented_notes',
                            Note.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count])


@register.simple_tag
def show_notes_by_years():
    return cache.get_or_set('notes_numbers_by_year',
                            Note.objects.annotate(number=Count(F('year'))).order_by('-year'))
