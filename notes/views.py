from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.conf import settings

from .models import Topic, Note, Comment, ViewsQuantity
from .forms import CommentForm, SearchForm, ContactForm
from .extras import make_picture


def count_views(func):
    def views_counter(self, **kwargs):
        note = Note.objects.get(slug=self.kwargs['slug'])
        try:
            notes_views = ViewsQuantity.objects.get(note=note)
        except ObjectDoesNotExist:
            notes_views = ViewsQuantity(note=note)
        finally:
            notes_views.quantity += 1
            notes_views.save()
        return func(self, **kwargs)
    return views_counter


class AnnualNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.filter(year=self.kwargs['year'])


class AuthorsNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.filter(authorAsSlug=self.kwargs['authorAsSlug'])


class NoteDetailView(CreateView):
    template_name = 'notes/note_detail.html'
    model = Note
    form_class = CommentForm
    queryset = Note.objects.filter(active=True)

    @count_views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        note = Note.objects.get(slug=slug)
        context['note'] = note
        context['comments'] = note.comments.all()
        context['views'] = ViewsQuantity.objects.get(note=note).quantity
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        note = Note.objects.get(pk=self.request.POST['note'])
        comment.note = note
        parent = self.request.POST.get('parent', None)
        if parent:
            comment.parent = Comment.objects.get(pk=parent)
            comment.answer_to = Comment.objects.get(pk=self.request.POST.get('answer_to', None))
        comment.picture = make_picture(form.cleaned_data['user'])
        comment.save()
        messages.success(self.request, 'Комментарий добавлен.', extra_tags='alert alert-success')
        return HttpResponseRedirect(reverse('notes:note_detail', kwargs={'slug': note.slug}))


class NotesView(ListView):
    model = Note
    context_object_name = 'notes'
    paginate_by = 12


class TaggableNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.filter(tags__slug__in=[self.kwargs['slug']])


class TopicalNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Topic.objects.get(slug=self.kwargs['slug']).notes.all()


class SendMailToAdminView(FormView):
    form_class = ContactForm
    template_name = 'notes/contact.html'

    def form_valid(self, form):
        form_data = form.cleaned_data
        subject = 'booknotes: ' + form_data['subject']
        message = form_data['username'] + ', ' + form_data['sender'] + ':\n\n' + form_data['message']
        email = settings.EMAIL_HOST_USER
        send_mail(subject, message, email, [email])
        messages.success(self.request, 'Сообщение отправлено.', extra_tags='alert alert-success')
        return HttpResponseRedirect(reverse('notes:notes_list'))


class SubgenreNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.filter(subgenre=self.kwargs['subgenre'])


def search(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = SearchQuery(request.GET['query'])
            vector = SearchVector('title', weight='A') + SearchVector('author', weight='A') + \
                     SearchVector('body', weight='B')
            results = Note.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('-rank')
            if results:
                paginator = Paginator(results, 12)
                page_number = request.GET.get('page')
                page_content = paginator.get_page(page_number)
                context = {'notes': page_content}
                return render(request, 'notes/note_list.html', context)
            else:
                return render(request, 'notes/not_found.html')


def unsubscribe_from_answers(request, email):
    users = Comment.objects.filter(email=email)
    for user in users:
        if user.notification:
            user.notification = False
    return render(request, 'mailing/unsubscribed.html')
