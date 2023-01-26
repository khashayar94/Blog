from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from django.contrib import messages


from post.models import UsersProfile

def register(request):
    
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email', False)
        password = request.POST.get('pass', False)
        re_password = request.POST.get('re_pass', False)
    
        if password == re_password:

            if User.objects.filter(email=email).exists():
                messages.info(request, 'The email is already taken')
                return redirect('user:register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'The username is already taken')
                return redirect('user:register')

            else:
                user = User.objects.create_user(username=username, email=email ,password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                UsersProfile.objects.create(user=username)

                return redirect('post:index')
        else:
            messages.info(request, 'The password is not matched')
            return redirect('user:register')

    else:
        return render(request, 'registration/register.html')


def signin(request):

    if request.method == "POST":

        username = request.POST.get('your_username', False)
        password = request.POST.get('your_pass', False)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('post:index')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('user:login')
    else:
        return render(request, 'registration/login.html')
