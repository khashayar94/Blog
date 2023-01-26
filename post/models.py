from django.db import models
from django.contrib.auth.models import User

class UsersProfile(models.Model):
	user = models.CharField(max_length=20)
	user_image = models.ImageField(upload_to='users_images', default='blank-profile-picture.png')
	
	def __str__(self):
		return self.user

class Topic(models.Model):
	topic_owner = models.CharField(max_length=20)
	topic = models.CharField(max_length=20)
	topic_body = models.TextField(blank=True)
	topic_img = models.ImageField(upload_to='topics_images', blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['topic']

	def __str__(self):
		self.topic = self.topic.capitalize()
		return self.topic


class Post(models.Model):
	post_owner = models.CharField(max_length=20)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	text = models.TextField()
	post_img = models.ImageField(upload_to='posts_images', blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_added']

	def __str__(self):
		self.text = self.text[:20]
		return f"{self.text}..."

class Follow(models.Model):
	follower = models.CharField(max_length=20)
	following = models.CharField(max_length=20)
	
	def __str__(self):
		return self.follower