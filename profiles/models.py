from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile Model that contains User Information.
    -----------------------------------------------------------------
    owner:           The creator of the Profile
    -----------------------------------------------------------------
    created_at:      Time the Profile was first created in the
                     Database
    -----------------------------------------------------------------
    updated_at:      Time of last modification of the Database Entry.
    -----------------------------------------------------------------
    name:            The Name of the User.
    -----------------------------------------------------------------
    description:     A short description of the User (e.g. Bio).
    -----------------------------------------------------------------
    image:           A User Profile Picture.
    -----------------------------------------------------------------
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_tbffwu.jpg'
    )

    class Meta:
        """
        Metaclass - Ordering by Creation Time (reverse)
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns the Profile's Username
        """

        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Creates a new Profile. Used for Signals.
    """

    if created:
        Profile.objects.create(owner=instance)


# Signals. Connecting a newly created User with a profile
post_save.connect(create_profile, sender=User)
