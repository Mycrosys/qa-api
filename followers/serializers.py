from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'follower'
    and 'followed_issue'
    """

    follower = serializers.ReadOnlyField(source='follower.username')
    followed_issue_name = serializers.ReadOnlyField(source='followed.title')

    class Meta:
        model = Follower
        fields = [
            'id', 'follower', 'created_at', 'followed_issue_name',
            'followed_issue'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
