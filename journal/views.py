from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from qa_api.permissions import IsOwnerOrReadOnly
from .models import Journal
from .serializers import JournalSerializer


class JournalList(generics.ListAPIView):
    """
    This provides a list of all Journals
    There is no need for a create view, because its handled by django signals
    """

    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Journal.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue']


class JournalDetail(generics.RetrieveAPIView):
    """
    This provides a detail view of a single Journal as well as
    the capability to update the information
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = JournalSerializer
    queryset = Journal.objects.all()
