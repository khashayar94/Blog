from django.contrib import admin

from .models import Post, Topic, Follow, UsersProfile


admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Follow)
admin.site.register(UsersProfile)