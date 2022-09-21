from rest_framework import generics
from qa_api.permissions import IsOwnerOrReadOnly
from .models import Journal
from .serializers import JournalSerializer


class JournalList(generics.ListAPIView):
    """
    This provides a list of all Journals
    There is no need for a create view, because its handled by django signals
    """

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalDetail(generics.RetrieveAPIView):
    """
    This provides a detail view of a single Journal as well as
    the capability to update the information
    """

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
