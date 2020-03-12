from tinymce.models import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField

from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from .extras import translate_and_slugify


class Topic(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = translate_and_slugify(self.name)
        super().save(self, *args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = translate_and_slugify(self.name)
        super().save(self, *args, **kwargs)


class NoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Note(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    authorAsSlug = models.SlugField(max_length=50, null=True)
    subgenre = models.CharField(max_length=20, null=True, choices=(('popular_science', 'Научпоп'),
                                                                   ('self-development', 'Саморазвитие')))
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='notes')
    image = ThumbnailerImageField(upload_to='notes/', null=True, resize_source={'size': (0, 170), 'crop': 'scale'})
    description = models.TextField(max_length=200)
    issue = HTMLField()
    year = models.IntegerField(validators=[RegexValidator(regex='\d{4}')])
    body = HTMLField(null=True, blank=True)
    shouldRead = HTMLField(null=True, unique=True)
    active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')

    objects = NoteManager()

    class Meta:
        ordering = ['-year', 'title']
        unique_together = ['title', 'author']

    def __str__(self):
        return f'{self.author} «{self.title}»'

    def get_absolute_url(self):
        return reverse('notes:note_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='answers')
    answerTo = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='get_answer_from')
    user = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='users/', null=True)
    email = models.EmailField()
    body = models.TextField(max_length=500)
    added = models.DateTimeField(auto_now_add=True)
    notifications = models.BooleanField(default=False)

    class Meta:
        ordering = ('added',)

    def __str__(self):
        return f'{self.user}: «{self.body}...»'


class ViewsQuantity(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='views_quantity')
    quantity = models.IntegerField(default=0)
