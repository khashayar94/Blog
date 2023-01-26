from django.urls import path

from . import views


app_name = 'post'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('search_topic/', views.search_topic, name='search_topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('posts/<int:topic_id>/', views.posts, name='posts'),
    path('search_post/<int:topic_id>/', views.search_post, name='search_post'),
    path('new_post/<int:topic_id>/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('users/', views.users, name='users'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('security/', views.security, name='security'),
    path('delete_account/', views.delete_account, name="delete-account"),
]
