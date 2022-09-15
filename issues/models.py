from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    """
    Issue Model that contains all Information for an Issue
    -----------------------------------------------------------------
    title:           The Title of the Issue
    -----------------------------------------------------------------
    owner:           The creator of the Issue
    -----------------------------------------------------------------
    created_at:      Time the Issue was first created in the Database
    -----------------------------------------------------------------
    updated_at:      Time of last modification of the Database Entry.
    -----------------------------------------------------------------
    description:     The Bulk of the Information of said Issue. What
                     is the problem, reproducable steps to recreate
                     the Bug, etc.
    -----------------------------------------------------------------
    image:           A screenshot (if applicable) that shows the Bug.
    -----------------------------------------------------------------
    due_date:        The date when the issue needs to be resolved.
    -----------------------------------------------------------------
    priority:        The Urgence Level of the Bug (Low, Mid, High or
                     Critical).
    -----------------------------------------------------------------
    category:        The Category the Issue falls in (Bug, Not a Bug
                     Duplicate or Won't Fix).
    -----------------------------------------------------------------
    state:           The State of the Issue (Open, Assigned, Closed)
    -----------------------------------------------------------------
    overdue:         If the Issue is overdue, this needs to be set to
                     True.
    -----------------------------------------------------------------
    assigned_to:     Contains all the Users that are assigned to work
                     on this Issue.
    -----------------------------------------------------------------
    """

    # Priorities are listed here
    LOW = 'LOW'
    MID = 'MID'
    HIGH = 'HGH'
    CRITICAL = 'CRT'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MID, 'Mid'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical'),
    ]

    # Cathegories are listed here
    BUG = 'BUG'
    NOT_A_BUG = 'NAB'
    DUPLICATE = 'DUP'
    WONT_FIX = 'WFX'
    CATEGORY_CHOICES = [
        (BUG, 'Bug'),
        (NOT_A_BUG, 'Not a Bug'),
        (DUPLICATE, 'Duplicate'),
        (WONT_FIX, "Won't Fix"),
    ]

    # States are listed here
    OPEN = 'OPN'
    ASSIGNED = 'ASN'
    CLOSED = 'CLS'
    STATE_CHOICES = [
        (OPEN, 'Open'),
        (ASSIGNED, 'Assigned'),
        (CLOSED, 'Closed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_bxv0mn.jpg', blank=True)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    priority = models.CharField(
        max_length=3,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=BUG,
    )
    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
        default=OPEN,
    )
    overdue = models.BooleanField(default=False)
    assigned_to = models.ManyToManyField(User, related_name='issue_assigned',
                                         blank=True)

    class Meta:
        """
        Metaclass - Ordering by Time the Issues were created
        """

        ordering = ['-created_at']

    def __str__(self):
        """
        Returns the title and ID of an Issue
        """

        return f'{self.id} {self.title}'
