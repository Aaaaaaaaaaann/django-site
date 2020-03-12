from django.db.models import signals
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Comment


@receiver(signals.post_save, sender=Comment)
def send_email_with_comment_answer(sender, instance, **kwargs):
    if instance.answer_to.notifications:
        subject = 'На ваш комментарий ответили'
        message = render_to_string('notes/letter_with_comment_answer.html', {'instance': instance})
        sender = settings.EMAIL_HOST_USER
        recipient = instance.answer_to.email
        letter = EmailMessage(subject, message, sender, [recipient])
        letter.content_subtype = 'html'
        letter.send()
