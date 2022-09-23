from rest_framework import serializers
from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    journals_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size can not be larger than 2MB.')
        if value.image.height > 2160:
            raise serializers.ValidationError(
                'Image height can not be larger than 2160px.'
            )
        if value.image.width > 3840:
            raise serializers.ValidationError(
                'Image width can not be larger than 3840px.'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Issue
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'description', 'image', 'due_date',
            'priority', 'category', 'state', 'overdue',
            'assigned_to', 'journals_count'
        ]
