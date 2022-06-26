from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.decorators.http import require_POST
try:
	from django.utils import simplejson as json
except ImportError:
	import json
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.db.models import Count
from django.db.models.functions import Lower
@login_required
def feed(request):
	posts = Post.objects.all().order_by('-date')
	postform = PostForm()
	

	profileOfRequest = Profile.objects.get_or_create(
	user=request.user)[0]
	comments = Comment.objects.all()

	commentform = CommentForm()


	active_users = sorted(Profile.objects.all(), key=lambda t: t.total_posts, reverse=True)[:3]
	#active_users = Profile.objects.annotate(total_posts=Count('votes')).order_by('total_posts')
	

	if request.method == 'POST':

		if request.is_ajax():
			print("AJAX HERE")
		else:
			if 'post' not in request.POST:
				commentform = CommentForm(request.POST)
				

				if commentform.is_valid():
					name = request.POST.get('name')


					
					commentform.save(commit=False)
					commentform.instance.author = profileOfRequest
					commentform.instance.post = Post.objects.filter(id=request.POST.get('post_id'))[0]

					print(Post.objects.filter(id=request.POST.get('post_id'))[0])

					commentform.save()
					commentform = CommentForm()
					context = {"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments, "active_users": active_users}
					
					return HttpResponseRedirect(reverse('app:feed'))
	
			else:
				postform = PostForm(request.POST)
				

				if postform.is_valid():
					postform.save(commit=False)
					postform.instance.author = profileOfRequest
					
					postform.save()
					postform = PostForm()
					context = {"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments, "active_users": active_users}
					return HttpResponseRedirect(reverse('app:feed'))
	else:
		postform = PostForm()
		commentform = CommentForm()

	context = {"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments, "active_users": active_users}	

	
	return render(request, 'app/feed.html',context)

@login_required
def profile(request, profileWho):
	user1 = User.objects.all().filter(username=profileWho)

	profile = Profile.objects.get_or_create(
	user=user1[0])

	profileOfRequest = Profile.objects.get_or_create(
	user=request.user)[0]
	
	profile2 = Profile.objects.filter(user=user1[0])
	postform = PostForm()
	posts = Post.objects.filter(author=profile2[0])
	posts2 = Post.objects.filter(sharers=profile2[0])
	posts = posts.union(posts2).order_by('-date')
	comments = Comment.objects.all()

	commentform = CommentForm()

	if request.method == 'POST':
		if request.is_ajax():
			print("AJAX HERE")
		else:
			if 'post' not in request.POST:
				commentform = CommentForm(request.POST)
				

				if commentform.is_valid():
					name = request.POST.get('name')


					
					commentform.save(commit=False)
					commentform.instance.author = profileOfRequest
					commentform.instance.post = Post.objects.filter(id=request.POST.get('post_id'))[0]

					print(Post.objects.filter(id=request.POST.get('post_id'))[0])

					commentform.save()
					commentform = CommentForm()
					context = {"profile2":profile2,"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments}
					
					return HttpResponseRedirect(reverse('app:profile', kwargs={'profileWho':user1[0].username}))
	
			else:
				postform = PostForm(request.POST)
				

				if postform.is_valid():
					postform.save(commit=False)
					postform.instance.author = profile2[0]
					
					postform.save()
					postform = PostForm()
					context = {"profile2":profile2,"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments}
					return HttpResponseRedirect(reverse('app:profile', kwargs={'profileWho':user1[0].username}))
	else:
		postform = PostForm()
		commentform = CommentForm()

	context = {"profile2":profile2,"commentform": commentform,  "postform": postform, "posts": posts, "profileOfRequest": profileOfRequest, "comments": comments}	

	return render(request, 'app/profile.html',context)

	
  
@login_required
def edit(request, profileWho):
	user1 = User.objects.all().filter(username=profileWho)

	profile = Profile.objects.get_or_create(
	user=user1[0])
	
	profile2 = Profile.objects.filter(user=user1[0])
	edit = Profile.objects.get(user=request.user)
	form = ProfileEditForm(instance=edit)

  
	if request.method == 'POST':
		form = ProfileEditForm(request.POST, request.FILES, instance=edit)
		

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('app:profile', kwargs={'profileWho':user1[0].username}))
	else:
		form = ProfileEditForm()
	return render(request, 'app/image.html', {'form' : form})

@login_required
def search(request):
	
	profileOfRequest = Profile.objects.get(user=request.user) 
	posts = Post.objects.filter(text__contains=1)
	users = Profile.objects.filter(name__contains=1)
	comments = Comment.objects.all()
	searched = 0
	context = {"posts": posts, "profileOfRequest": profileOfRequest, "comments": comments,"users":users,"searched":searched}
	if request.method == 'GET':
		searched = request.GET.get('searched')
		print(searched)
		if searched:
			a=1
			posts = Post.objects.filter(text__contains=searched)
			users = Profile.objects.filter(name__contains=searched)

			context = {"posts": posts, "profileOfRequest": profileOfRequest, "comments": comments,"users":users,"searched":searched}

		
	
	return render(request, 'app/search.html', context)


def settings(request):
	
	

	context = {}

		
	
	return render(request, 'app/settings.html', context)  
  
@login_required
@require_POST
def like(request):
	if request.method == 'POST':
		user = request.user
		content_id = request.POST.get('content_id', None)
		post = get_object_or_404(Post, id=content_id)
		profile = get_object_or_404(Profile, user=user)

		if post.likers.filter(id=profile.id).exists():
			# user has already liked this company
			# remove like/user
			post.likers.remove(profile)
			message = 'You disliked this'
		else:
			# add a new like for a company
			post.likers.add(profile)
			message = 'You liked this'

	ctx = {'likes_count': post.total_likes}
	# use mimetype instead of content_type if django < 5
	return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def share(request):
	if request.method == 'POST':
		user = request.user
		content_id = request.POST.get('content_id', None)
		post = get_object_or_404(Post, id=content_id)
		profile = get_object_or_404(Profile, user=user)

		if post.sharers.filter(id=profile.id).exists():
			# user has already liked this company
			# remove like/user
			post.sharers.remove(profile)
			message = 'You unshared this'
		else:
			# add a new like for a company
			post.sharers.add(profile)
			message = 'You shared this'

	ctx = {'shares_count': post.total_sharers}
	# use mimetype instead of content_type if django < 5
	return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def follow(request):
	if request.method == 'POST':	
		user = request.user
		
		profile = get_object_or_404(Profile, user=user)
		profileToFollow = get_object_or_404(Profile, id=request.POST.get('content_id', None))

		if profileToFollow.followers.filter(id=profile.id).exists():
			# user has already liked this company
			# remove like/user
			print(1)
			profileToFollow.followers.remove(profile)
			profile.following.remove(profileToFollow)
			message = 'You unfollowed this'
		else:
			# add a new like for a company
			profileToFollow.followers.add(profile)
			profile.following.add(profileToFollow)
			message = 'You followed this'



	
	ctx = {'hehe': 1}


	return HttpResponse(json.dumps(ctx), content_type='application/json')