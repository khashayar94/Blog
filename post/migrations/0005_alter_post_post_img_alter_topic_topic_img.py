# Generated by Django 4.1.3 on 2022-11-21 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_post_img_alter_topic_topic_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_img',
            field=models.ImageField(blank=True, upload_to='posts_images'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_img',
            field=models.ImageField(blank=True, upload_to='topics_images'),
        ),
    ]