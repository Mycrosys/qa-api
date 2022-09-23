from django.db.models import Count
from rest_framework import generics, filters
from qa_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    This provides a list of all Profiles
    There is no need for a create view, because its handled by django signals
    """

    queryset = Profile.objects.annotate(
        following_count=Count('owner__follower', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'following_count',
        'owner__follower__created_at',
    ]   

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    This provides a detail view of a single Profile as well as
    the capability to update the information and image if
    you are the owner of the profile
    """

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        following_count=Count('owner__follower', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
