import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import signing
from django.core import mail
from django.core.signing import BadSignature
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string

from .forms import EmailForm
from .models import Follower


def send_confirmation(recipient):
    host = 'http//127.0.0.1.8000'
    subject = 'Подтверждение подписки'
    message = render_to_string('mailing/confirm_email.html', {'sign': signing.dumps(recipient), host: 'host'})
    sender = settings.EMAIL_HOST_USER
    letter = mail.EmailMessage(subject, message, sender, [recipient])
    letter.content_subtype = 'html'
    letter.send()


def subscribe(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        previous_url = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if form.is_valid():
            email = form.cleaned_data['email']
            found_follower = Follower.objects.filter(email=email)
            if found_follower:
                follower = found_follower[0]
                if follower.activated:
                    messages.info(request, 'Хорошая новость: вы уже подписаны.', extra_tags='alert alert-primary')
                    return previous_url
                else:
                    send_confirmation(email)
                    messages.success(request, 'Вам отправлено сообщение: нужно подтвердить подписку.',
                                     extra_tags='alert alert-success')
                    return previous_url
            else:
                Follower.objects.create(email=email)
                send_confirmation(email)
                messages.success(request, 'Вам отправлено сообщение: нужно подтвердить подписку.',
                                 extra_tags='alert alert-success')
                return previous_url
        else:
            messages.error(request, 'Кажется, это неправильный email.', extra_tags='alert alert-danger')
            return previous_url


def activate(request, sign):
    try:
        email = signing.loads(sign, max_age=86400)
    except BadSignature:
        return render(request, 'mailing/bad_signature.html')
    follower = Follower.objects.get(email=email)
    follower.activated = True
    follower.joined = datetime.date.today().isoformat()
    follower.save()
    return render(request, 'mailing/successfully.html')


def unsubscribe(request, email):
    follower = Follower.objects.get(email=email)
    if follower.activated:
        follower.activated = False
        follower.save()
        return render(request, 'mailing/unsubscribed.html')
    else:
        return render(request, 'mailing/unsubscribed.html')


def send_letter(subject):
    followers = Follower.objects.filter(activated=True)
    connection = mail.get_connection()
    connection.open()
    sender = settings.EMAIL_HOST_USER
    for follower in followers:
        recipient = follower.email
        message = render_to_string('mailing/letter_itself.html', {'email': recipient})
        letter = mail.EmailMessage(subject, message, sender, [recipient])
        letter.content_subtype = 'html'
        letter.send()
    connection.close()
