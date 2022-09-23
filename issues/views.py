from django.db.models import Count
from rest_framework import generics, permissions, filters
from qa_api.permissions import IsOwnerOrAssignedOrReadOnly
from .models import Issue
from .serializers import IssueSerializer


class IssueList(generics.ListCreateAPIView):
    """
    List Issue or create one if logged in
    The perform_create method associates the issue with the logged in user.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Issue.objects.annotate(
        journals_count=Count('journal', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
        'assigned_to__username',
    ]

    ordering_fields = [
        'journals_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an issue and edit or delete it if you own it.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrAssignedOrReadOnly]
    queryset = Issue.objects.annotate(
        journals_count=Count('journal', distinct=True)
    ).order_by('-created_at')
