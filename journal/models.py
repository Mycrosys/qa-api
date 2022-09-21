from django.db import models
from django.contrib.auth.models import User
# from issues.models import Issue


class Journal(models.Model):
    """
    Journal Model, used to store history of changes
    of a certain Issue Model
    -----------------------------------------------------------------
    owner:           The creator of the Journal.
    -----------------------------------------------------------------
    created_at:      Time the Profile was first created in the
                     Database
    -----------------------------------------------------------------
    updated_at:      Time of last modification of the Database Entry.
    -----------------------------------------------------------------
    action:          The modifications that were made.
    -----------------------------------------------------------------
    description:     A short description why these changes were made.
    -----------------------------------------------------------------
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        """
        Metaclass - Ordering by Time the Issues were created
        """

        ordering = ['created_at']

    def __str__(self):
        """
        Returns the title and ID of an Issue
        """

        return self.content
