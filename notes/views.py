from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib import messages
from django.core.mail import send_mail
from django.core.cache import cache

from .models import Topic, Note, Comment, Tag
from .forms import CommentForm, SearchForm, ContactForm
from nfbooknotes import settings


class AnnualNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        year = self.kwargs['year']
        return cache.get_or_set('notes_by_year_' + str(year), Note.objects.filter(year=year))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        return context


class NoteDetailView(CreateView):
    template_name = 'notes/note_detail.html'
    model = Note
    form_class = CommentForm
    queryset = Note.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        note = Note.objects.get(slug=slug)
        context['note'] = note
        context['comments'] = cache.get_or_set('comments_to_' + slug, note.comments.all())
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        note = Note.objects.get(pk=self.request.POST['note'])
        comment.note = note
        parent = self.request.POST.get('parent', None)
        if parent:
            comment.parent = Comment.objects.get(pk=parent)
            comment.answer_to = Comment.objects.get(pk=self.request.POST.get('answer_to', None))
        comment.save()
        messages.success(self.request, 'Комментарий добавлен.', extra_tags='alert alert-success')
        return HttpResponseRedirect(reverse('notes:note_detail', kwargs={'slug': note.slug}))


class NotesView(ListView):
    model = Note
    queryset = Note.objects.filter(active=True)
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return cache.get_or_set('all_active_notes', self.queryset)


class TaggableNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        tag = self.kwargs['slug']
        return cache.get_or_set('notes_by_tag_' + tag, Note.objects.filter(tags__slug__in=[tag]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class TopicalNotesView(ListView):
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        slug = self.kwargs['slug']
        topic = Topic.objects.get(slug=slug)
        return cache.get_or_set('notes_by_topic_' + slug, topic.notes.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(slug=self.kwargs['slug'])
        return context


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


def search(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = SearchQuery(request.GET['query'])
            vector = SearchVector('title', weight='A') + SearchVector('author', weight='A') + \
                     SearchVector('body', weight='B')
            results = Note.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('-rank')
            if results:
                context = {'notes': results}
                return render(request, 'notes/note_list.html', context)
            else:
                return render(request, 'notes/not_found.html')
