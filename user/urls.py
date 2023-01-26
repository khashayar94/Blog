from django.urls import path, include

from . import views


app_name = 'user'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
]
