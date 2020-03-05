from rest_framework.generics import ListAPIView, RetrieveAPIView

from notes.models import Topic, Tag, Note, Comment, ViewsQuantity
from .serializers import TopicSerializer, TagSerializer, NoteSerializer, CommentSerializer, ViewsQuantitySerializer


class NoteListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDetailView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class TopicListView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicDetailView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'slug'


class CommentListToNoteView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'note_id'


class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ViewsQuantityListView(ListAPIView):
    queryset = ViewsQuantity.objects.all()
    serializer_class = ViewsQuantitySerializer
