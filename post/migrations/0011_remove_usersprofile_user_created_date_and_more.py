# Generated by Django 4.1.3 on 2022-11-27 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0010_alter_usersprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersprofile',
            name='user_created_date',
        ),
        migrations.AddField(
            model_name='usersprofile',
            name='user_image',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='users_images'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
