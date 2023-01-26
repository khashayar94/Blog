from django import forms

from .models import Topic, Post, UsersProfile


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic', 'topic_img']
        labels = {'topic':'Topic', 'topic_img':'Image'}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'text', 'post_img']
        labels = {'text':'Text', 'post_img':'Image'}

class UsersProfileForm(forms.ModelForm):
    class Meta:
        model = UsersProfile
        fields = ['user', 'user_image']
        labels = {'user':'Username', 'user_image':'Image'}
