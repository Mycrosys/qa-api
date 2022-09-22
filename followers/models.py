from django.db import models
from django.contrib.auth.models import User
from issues.models import Issue


class Follower(models.Model):
    """
    Follower Model that contains Follower Information.
    -----------------------------------------------------------------
    follower:        The User that follows the Issue.
    -----------------------------------------------------------------
    issue_following: The Issue that is being followed.
    -----------------------------------------------------------------
    created_at:      Time the Follower was first created in the
                     Database
    -----------------------------------------------------------------
    'unique_together' makes sure a user can't 'double follow' the
    same Issue.
    """

    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_following = models.ForeignKey(
        Issue, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['issue_following', 'follower']

    def __str__(self):
        return f'{self.follower} {self.issue_following}'
