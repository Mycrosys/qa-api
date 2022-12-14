# Generated by Django 3.2.15 on 2022-09-22 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issues', '0003_alter_issue_due_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('issue_following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='issues.issue')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('issue_following', 'follower')},
            },
        ),
    ]
