# Generated by Django 3.2.15 on 2022-09-23 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issues', '0003_alter_issue_due_date'),
        ('followers', '0003_auto_20220923_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='issue_following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='issues.issue'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
