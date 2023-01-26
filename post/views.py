from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Topic, Post, Follow, UsersProfile
from .forms import PostForm

# Main methods
@login_required(login_url='user:login')
def index(request):

	topics = Topic.objects.filter(topic_owner=request.user.username)
	content = {'topics':topics}

	return render(request, 'post/index.html', content)


@login_required(login_url='user:login')
def topics(request):

	topic_owner = request.user.username
	topics = Topic.objects.filter(topic_owner=topic_owner)
	nums_and_pages = _paginator(request, topics)
	content = {'topics':topics,'nums':nums_and_pages[0], 'pages':nums_and_pages[1]}

	return render(request, 'post/topics.html', content)


@login_required(login_url='user:login')
def search_topic(request):
	
	topic_owner = request.user.username

	if request.method != "POST":
		topics = Topic.objects.filter(topic_owner=topic_owner)
		nums_and_pages = _paginator(request, topics)
		content = {'topics':topics, 'nums':nums_and_pages[0], 'pages':nums_and_pages[1]}
		return render(request, 'post/topics.html', content)
	else:
		searched = request.POST.get('searched', False)
		topics = Topic.objects.filter(topic__startswith=searched, topic_owner=topic_owner)
		nums_and_pages = _paginator(request, topics)
		content= {'topics':topics, 'nums':nums_and_pages[0], 'pages':nums_and_pages[1], 'searched':searched}
		return render(request, 'post/topics.html', content)


@login_required(login_url='user:login')
def new_topic(request):

	topic_owner = request.user.username
	topics = Topic.objects.filter(topic_owner=request.user.username)
	
	if request.method == "POST":

		if request.FILES.get('image') == None and request.POST.get('comment') == None:
				topic = request.POST.get('topic', False)
				new_topic = Topic.objects.create(topic_owner=topic_owner, topic=topic)
				new_topic.save()

		elif request.FILES.get('image') == None:
			topic = request.POST.get('topic', False)
			topic_body = request.POST.get('comment', False)
			new_topic = Topic.objects.create(topic_owner=topic_owner, topic=topic, topic_body=topic_body)
			new_topic.save()

		elif request.POST.get('comment') == None:
			topic = request.POST.get('topic', False)
			topic_img = request.FILES.get('image', False)
			new_topic = Topic.objects.create(topic_owner=topic_owner, topic=topic, topic_img=topic_img)
			new_topic.save()
		else:
			topic = request.POST.get('topic', False)
			topic_body = request.POST.get('comment', False)
			topic_img = request.FILES.get('image', False)
			new_topic = Topic.objects.create(topic_owner=topic_owner, topic=topic, topic_body=topic_body, topic_img=topic_img)
			new_topic.save()

		return redirect('post:topics')
			
	else:
		content = {'topics':topics}
		return render(request, 'post/new_topic.html', content)
		

@login_required(login_url='user:login')
def edit_topic(request, topic_id):

	original_topic = Topic.objects.get(id=topic_id)
	topics = Topic.objects.filter(topic_owner=request.user.username)

	if request.method == 'POST':

		if request.FILES.get('image') == None and request.POST.get('comment') == None:
			topic = request.POST.get('topic', False)
			
			original_topic.topic = topic
			original_topic.save()

		elif request.FILES.get('image') == None:
			topic = request.POST.get('topic', False)
			topic_body = request.POST.get('comment', False)

			original_topic.topic = topic
			original_topic.topic_body = topic_body
			original_topic.save()

		elif request.POST.get('comment') == None:
			topic = request.POST.get('topic', False)
			topic_img = request.FILES.get('image', False)

			original_topic.topic = topic
			original_topic.topic_img = topic_img
			original_topic.save() 
		else:
			topic = request.POST.get('topic', False)
			topic_body = request.POST.get('comment', False)
			topic_img = request.FILES.get('image', False)
			
			original_topic.topic = topic
			original_topic.topic_body = topic_body
			original_topic.topic_img = topic_img
			original_topic.save()

		return redirect('post:topics')

	else:
		content = {'original_topic':original_topic, 'topics':topics}
		return render(request, 'post/edit_topic.html', content)


@login_required(login_url='user:login')
def delete_topic(request, topic_id):

	topic = Topic.objects.get(id=topic_id)

	if request.user.username == topic.topic_owner:
		topic.delete()
		return redirect('post:topics')
	else:
		messages.error(request, "You can't delete other's topics")
		return redirect('post:topics')
	
	
@login_required(login_url='user:login')
def posts(request, topic_id):
	
	topics = Topic.objects.filter(topic_owner=request.user.username)
	topic = Topic.objects.get(id=topic_id)
	posts = Post.objects.filter(topic=topic)
	nums_and_pages = _paginator(request, posts)
	content = {'topics':topics, 'topic':topic, 'posts':posts, 'nums':nums_and_pages[0],'pages':nums_and_pages[1]}
	
	return render(request, 'post/posts.html', content)


@login_required(login_url='user:login')
def search_post(request, topic_id):
	
	topic = Topic.objects.get(id=topic_id)
	topics = Topic.objects.filter(topic_owner=request.user.username)


	if request.method != "POST":
		posts = Post.objects.filter(topic=topic)
		nums_and_pages = _paginator(request, posts)
		content = {'posts':posts, 'nums':nums_and_pages[0], 'pages':nums_and_pages[1]}
		return render(request, 'post/posts.html', content)
	else:
		
		searched = request.POST.get('searched', False)
		posts = Post.objects.filter(text__startswith=searched, topic=topic)
		nums_and_pages = _paginator(request, posts)
		content = {'topics':topics, 'topic':topic, 'posts':posts, 'nums':nums_and_pages[0], 'pages':nums_and_pages[1],  'searched':searched}
		return render(request, 'post/posts.html', content)


@login_required(login_url='user:login')
def new_post(request, topic_id):

	topics = Topic.objects.filter(topic_owner=request.user.username)
	topic = Topic.objects.get(id=topic_id)
	post_owner = request.user.username

	
	if request.method == "POST":

		if request.POST.get('comment') == None:
			messages.error('The comment field cannot be empty')
			return redirect('post:new-post', topic_id=topic.id)

		if request.FILES.get('image') == None:
			text = request.POST.get('comment', False)
			new_post = Post.objects.create(post_owner=post_owner, topic=topic, text=text)
			new_post.save()

		else:
			text = request.POST.get('comment', False)
			post_img = request.FILES.get('image', False)
			new_post = Post.objects.create(post_owner=post_owner, topic=topic, text=text ,post_img=post_img)
			new_post.save()

		return redirect('post:posts', topic_id=topic.id)
			
	else:
		content = {'topics':topics, 'topic':topic}
		return render(request, 'post/new_post.html', content)


@login_required(login_url='user:login')
def edit_post(request, post_id):

	topics = Topic.objects.filter(topic_owner=request.user.username)
	post = Post.objects.get(id=post_id)

	if request.method != "POST":
		form = PostForm(instance=post)
	else:
		form = PostForm(request.POST or None, request.FILES or None ,instance=post)
		if form.is_valid():
			form.save()
			return redirect('post:posts', topic_id=post.topic.id)
	
	content = {'form':form, 'topics':topics, 'post':post}
	return render(request, 'post/edit_post.html', content)


@login_required(login_url='user:login')
def delete_post(request, post_id):

	post = Post.objects.get(id=post_id)
	topic = post.topic

	if request.user.username == post.post_owner:
		post.delete()
		return redirect('post:posts',topic_id=topic.id)
	else:
		messages.error(request, "You can't delete other's posts")
		return redirect('post:topics')


@login_required(login_url='user:login')
def users(request):
	
	loggedin_user = request.user.username 
	
	all_usernames = _all_usernames(request)
	all_users_profiles = _all_users_profiles(loggedin_user)
	
	loggedin_user_followers_images = _loggedin_user_followers(loggedin_user, all_users_profiles)
	
	followings_usernames = _followers_followings(loggedin_user, all_users_profiles)[0]
	followings_usernames_images = _followers_followings(loggedin_user, all_users_profiles)[1]

	unfollowings_usernames_images = _unfollowings_usernames(all_usernames, followings_usernames, all_users_profiles)
	
	content = {'unfollowings_usernames_images':unfollowings_usernames_images, 'followings_usernames_images':followings_usernames_images, 'loggedin_user_followers_images':loggedin_user_followers_images}
	return render(request, 'post/users.html', content)


@login_required(login_url='user:login')
def follow(request, username):

	follower = request.user.username
	following = username
	Follow.objects.create(follower=follower, following=following)

	return redirect('post:users')


@login_required(login_url='user:login')
def unfollow(request, username):

	follower = request.user.username
	following = username
	Follow.objects.filter(follower=follower, following=following).delete()

	return redirect('post:users')


@login_required(login_url='user:login')
def profile(request, user_id):

	loggedin_user = request.user
	topics = Topic.objects.filter(topic_owner=request.user.username)
	
	user = User.objects.get(id=user_id)
	user_profile = UsersProfile.objects.get(user=user.username)
	image_exist = request.FILES.get('image', False)

	if request.method == 'POST':
		_update_profile(request, user, user_profile, image_exist)
		return redirect('post:index')
	else:
		content = {'user_profile':user_profile, 'loggedin_user':loggedin_user, 'topics':topics}
		return render(request, 'post/profile.html', content)


@login_required(login_url='user:login')
def security(request):

	loggedin_user = request.user
	topics = Topic.objects.filter(topic_owner=request.user.username)

	if request.method == 'POST':
		current_password = request.POST.get('currentPassword', False)

		if loggedin_user.check_password(current_password):
			new_password = request.POST.get('newPassword', False)
			confirm_password = request.POST.get('confirmPassword', False)

			if new_password == confirm_password:
				loggedin_user.set_password(new_password)
				loggedin_user.save()
				return redirect('post:index')
			else:
				messages.info(request, "The passwords didn't match")
				return redirect('post:security')

		else:
			messages.info(request, 'Invalid username or password')
			return redirect('post:security')
            
	else:
		content = {'loggedin_user':loggedin_user, 'topics':topics}
		return render(request, 'post/security.html', content)


@login_required(login_url='user:login')
def delete_account(request):

	loggedin_user = request.user
	user_profile = UsersProfile.objects.get(user=loggedin_user.username)

	if request.method == 'POST':
		user_profile.delete()
		loggedin_user.delete()
		return redirect('user:register')
	else:
		content = {'loggedin_user':loggedin_user}
		return render(request, 'post/security.html', content)


# Helper methods
def _paginator(request, object):

	p = Paginator(object, 3)
	page = request.GET.get('page')
	pages = p.get_page(page)
	nums = 'a' * pages.paginator.num_pages

	return nums, pages


def _all_usernames(request):

	all_users = User.objects.exclude(username=request.user.username)
	all_usernames = [z for z in all_users]
	all_usernames = [all_usernames[i].username for i in range(len(all_usernames))]
	all_usernames = set(all_usernames)

	return all_usernames


def _all_users_profiles(object):

	all_users_profiles = UsersProfile.objects.exclude(user=object)
	all_users_profiles = [y for y in all_users_profiles]
	all_users_profiles_usernames = [all_users_profiles[i].user for i in range(len(all_users_profiles))]
	all_users_profiles_images = [all_users_profiles[i].user_image for i in range(len(all_users_profiles))]
	all_users_profiles = list(zip(all_users_profiles_usernames, all_users_profiles_images))

	return all_users_profiles


def _loggedin_user_followers(object1, object2):

	loggedin_user_followers = Follow.objects.filter(following=object1)
	loggedin_user_followers = [x for x in loggedin_user_followers]
	loggedin_user_followers = [loggedin_user_followers[i].follower for i in range(len(loggedin_user_followers))]
	loggedin_user_followers_images = []
	for user, image in object2:
		if user in loggedin_user_followers:
			loggedin_user_followers_images.append((user, image))

	return loggedin_user_followers_images


def _followers_followings(object1, object2):

	followers_followings= [w for w in Follow.objects.filter(follower=object1)]
	followings_usernames= [followers_followings[i].following for i in range(len(followers_followings))]
	followings_usernames.reverse()
	followings_usernames = set(followings_usernames) - {object1}
	followings_usernames_images = []
	for user, image in object2:
		if user in followings_usernames:
			followings_usernames_images.append((user, image))
	
	return followings_usernames, followings_usernames_images


def _unfollowings_usernames(object1, object2, object3):

	unfollowings_usernames = object1 - object2
	unfollowings_usernames_images = []
	for user, image in object3:
		if user in unfollowings_usernames:
			unfollowings_usernames_images.append((user, image))

	return unfollowings_usernames_images
	

def _update_profile(request, user, profile, image):
	if image: 
		user_image = request.FILES.get('image', False)
		username = request.POST.get('username', False)
		first_name = request.POST.get('first_name', False)
		last_name = request.POST.get('last_name', False)
		email = request.POST.get('email', False)

		profile.user_image = user_image
		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()

		profile.user = username
		profile.save()
	else:
		username = request.POST.get('username', False)
		first_name = request.POST.get('first_name', False)
		last_name = request.POST.get('last_name', False)
		email = request.POST.get('email', False)

		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()

		profile.user = username
		profile.save()
