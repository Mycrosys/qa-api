from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'followers'
    and 'followed_issue'
    """

    followers = serializers.ReadOnlyField(source='owner.username')
    followed_issue_name = serializers.ReadOnlyField(source='followed.title')

    class Meta:
        model = Follower
        fields = [
            'id', 'followers', 'created_at', 'followed_issue_name',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
