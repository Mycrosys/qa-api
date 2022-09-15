from rest_framework import generics, permissions
from qa_api.permissions import IsOwnerOrReadOnly
from .models import Issue
from .serializers import IssueSerializer


class IssueList(generics.ListCreateAPIView):
    """
    List Issue or create one if logged in
    The perform_create method associates the issue with the logged in user.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an issue and edit or delete it if you own it.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Issue.objects.all()
