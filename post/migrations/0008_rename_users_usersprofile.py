# Generated by Django 4.1.3 on 2022-11-27 14:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0007_users'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='UsersProfile',
        ),
    ]