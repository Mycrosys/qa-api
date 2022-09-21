from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from journal.models import Journal


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

@receiver(pre_save, sender=Issue)
def create_journal(sender, instance, **kwargs):
    """
    Signal to create a new Journal entry when changing
    any field (except assigned_to).
    """
    try:
        obj = sender.objects.get(pk=instance.pk)

    # Newly created issue, so create no journal entry
    except sender.DoesNotExist:
        pass

    else:
        # Something was changed, create journal entry
        action = ""
        description = ""
        if not obj.title == instance.title:
            action += "Title, "
            description += f"Title changed from '{obj.title}' to "
            description += f"'{instance.title}'.\n"
        if not obj.description == instance.description:
            action += "Description, "
            description += "Description was changed.\n"
        if not obj.image == instance.image:
            action += "Image, "
            description += "Image was changed.\n"
        if not obj.due_date == instance.due_date:
            action += "Due Date, "
            description += "Due Date was changed.\n"
        if not obj.priority == instance.priority:
            action += "Priority, "
            description += f"Priority changed from '{obj.priority}' to "
            description += f"'{instance.priority}'.\n"
        if not obj.category == instance.category:
            action += "Category, "
            description += f"Category changed from '{obj.category}' to "
            description += f"'{instance.category}'.\n"
        if not obj.state == instance.state:
            action += "State, "
            description += f"State changed from '{obj.state}' to "
            description += f"'{instance.state}'.\n"
        if not obj.overdue == instance.overdue:
            action += "Overdue, "
            if instance.overdue:
                description += "Overdue changed to True.\n"
            else:
                description += "Overdue changed to False.\n"

        # remove the empty space and ',' at the end of the string
        action = action[:-2]
        # current_user = request.user
        Journal.objects.create(owner=instance.owner, issue=instance,
                               action=action, description=description)
