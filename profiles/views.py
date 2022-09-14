from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from qa_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    This provides a list of all Profiles
    There is no need for a create view, because its handled by django signals
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    This provides a detail view of a single Profile as well as
    the capability to update the information and image if
    you are the owner of the profile
    """

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
