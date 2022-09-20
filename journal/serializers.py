from rest_framework import serializers
from .models import Journal


class JournalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Journal model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Journal
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'issue', 'created_at', 'updated_at', 'action', 'description'
        ]

class JournalDetailSerializer(JournalSerializer):
    """
    Serializer for the Journal model used in Detail view
    """

    issue = serializers.ReadOnlyField(source='issue.id')
