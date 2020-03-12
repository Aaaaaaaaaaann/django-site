from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser

from notes.models import Topic, Tag, Note, Comment, ViewsQuantity
from mailing.models import Follower
from .serializers import TopicSerializer, TagSerializer, NoteSerializer, CommentSerializer, ViewsQuantitySerializer,\
    FollowersJoinedSerializer, FollowersUnsubscribedSerializer


class NotesListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['@title', '@author']


class NoteDetailView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class TagsListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class TagDetailView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class TopicsListView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class TopicDetailView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'slug'


class CommentsListToNoteView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'note_id'


class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ViewsQuantitiesListView(ListAPIView):
    queryset = ViewsQuantity.objects.all()
    serializer_class = ViewsQuantitySerializer


class FollowersQuantitiesView(APIView):
    def get(self, request):
        return Response({'all': Follower.objects.all().count(),
                         'active': Follower.objects.filter(activated=True).count(),
                         'unactivated': Follower.objects.filter(activated=False, unsubscribed=None).count(),
                         'former': Follower.objects.filter(activated=False, unsubscribed__isnull=False).count()})


@permission_classes([IsAdminUser])
class FollowersJoinedListView(ListAPIView):
    queryset = Follower.objects.filter(activated=True)
    serializer_class = FollowersJoinedSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=joined']


@permission_classes([IsAdminUser])
class FollowersUnsubscribedListView(ListAPIView):
    queryset = Follower.objects.filter(unsubscribed__isnull=False)
    serializer_class = FollowersUnsubscribedSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=unsubscribed']
