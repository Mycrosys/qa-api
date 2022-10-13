from django.contrib.auth.models import User
from rest_framework import serializers
from issues.models import Issue
from followers.models import Follower


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    assigned_to = serializers.SlugRelatedField(
        queryset=User.objects.all(), many=True, slug_field="username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    journals_count = serializers.ReadOnlyField()
    following_id = serializers.SerializerMethodField()

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

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, issue_following=obj
            ).first()
            
            return following.id if following else None
        return None

    class Meta:
        model = Issue
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'description', 'image', 'due_date',
            'priority', 'category', 'state', 'overdue',
            'assigned_to', 'journals_count', 'following_id'
        ]
