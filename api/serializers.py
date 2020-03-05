from rest_framework import serializers

from notes.models import Topic, Tag, Note, Comment, ViewsQuantity


class TagSerializer(serializers.ModelSerializer):
    notes_number = serializers.SerializerMethodField('get_notes_number')
    notes = serializers.SerializerMethodField('get_notes')

    def get_notes_number(self, instance):
        return Tag.objects.get(pk=instance.pk).notes.count()

    def get_notes(self, instance):
        notes = Tag.objects.get(pk=instance.pk).notes.all()
        return [f'{note.author} «{note.title}»' for note in notes]

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'notes_number', 'notes']


class TopicSerializer(serializers.ModelSerializer):
    notes_number = serializers.SerializerMethodField('get_notes_number')
    notes = serializers.SerializerMethodField('get_notes')

    def get_notes_number(self, instance):
        return Topic.objects.get(pk=instance.pk).notes.count()

    def get_notes(self, instance):
        notes = Topic.objects.get(pk=instance.pk).notes.all()
        return [f'{note.author} «{note.title}»' for note in notes]

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'notes_number', 'notes']


class NoteSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    subgenre = serializers.SerializerMethodField('get_subgenre')
    views_quantity = serializers.SerializerMethodField('get_views_quantity')
    comments_number = serializers.SerializerMethodField('get_comments_number')

    def get_subgenre(self, instance):
        return Note.objects.get(pk=instance.pk).get_subgenre_display()

    def get_views_quantity(self, instance):
        return ViewsQuantity.objects.get(note=instance).quantity

    def get_comments_number(self, instance):
        return Note.objects.get(pk=instance.pk).comments.count()

    class Meta:
        model = Note
        fields = ['id', 'title', 'author', 'subgenre', 'topic', 'year', 'tags', 'views_quantity', 'comments_number']


class CommentSerializer(serializers.ModelSerializer):
    added = serializers.SerializerMethodField('get_human_datetime')

    def get_human_datetime(self, instance):
        return str(Comment.objects.get(pk=instance.pk).added).split('.')[0]

    class Meta:
        model = Comment
        fields = ['id', 'note', 'answer_to', 'user', 'body', 'added']


class ViewsQuantitySerializer(serializers.ModelSerializer):
    note = serializers.StringRelatedField()

    class Meta:
        model = ViewsQuantity
        fields = ['note', 'quantity']
