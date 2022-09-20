from rest_framework import generics
from qa_api.permissions import IsOwnerOrReadOnly
from .models import Journal
from .serializers import JournalSerializer


class JournalList(generics.ListAPIView):
    """
    This provides a list of all Profiles
    There is no need for a create view, because its handled by django signals
    """

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalDetail(generics.RetrieveUpdateAPIView):
    """
    This provides a detail view of a single Profile as well as
    the capability to update the information and image if
    you are the owner of the profile
    """

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
