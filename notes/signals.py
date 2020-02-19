from django.db.models import signals
from django.dispatch import receiver
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Note, Comment


@receiver([signals.pre_save, signals.post_delete], sender=Note)
def invalidate_notes_related_caches(sender, instance, **kwargs):
    if not instance.id:
        old_caches = ['all_active_notes', 'notes_by_topic_' + instance.topic.slug, 'notes_by_year_' + instance.year,
                      'notes_numbers_by_topic', 'notes_numbers_by_year', 'tags_list']
        for tag in Note.objects.get(slug=instance.slug).tags.all():
            old_caches.append('notes_by_tag_' + tag.slug)
        cache.delete_many(old_caches)


@receiver([signals.post_save, signals.post_delete], sender=Comment)
def invalidate_comments_cache(sender, instance, **kwargs):
    cache.delete_many('comments_to_' + instance.note.slug, 'most_commented_notes')


@receiver(signals.post_save, sender=Comment)
def send_email_with_comment_answer(sender, instance, **kwargs):
    if instance.answer_to.notification:
        subject = 'На ваш комментарий ответили'
        message = render_to_string('notes/letter_with_comment_answer.html', {'instance': instance})
        sender = settings.EMAIL_HOST_USER
        recipient = instance.answer_to.email
        letter = EmailMessage(subject, message, sender, [recipient])
        letter.content_subtype = 'html'
        letter.send()
