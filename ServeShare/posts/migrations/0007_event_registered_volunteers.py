# Generated by Django 4.2.3 on 2023-08-18 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_volunteerprofile_badges'),
        ('posts', '0006_alter_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registered_volunteers',
            field=models.ManyToManyField(blank=True, related_name='events_registered', to='users.volunteerprofile'),
        ),
    ]