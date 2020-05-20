from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Blog, Post
from .forms import BlogForm, PostForm

def check_blog_owner(owner, user):
	if owner != user:
		return Http404

# Create your views here.
def index(request):
	"""Home page for Blog"""
	return render(request, 'blogs/index.html')

@login_required
def blogs(request):
	"""Show all blogs"""
	blogs = Blog.objects.order_by('date_added')
	context = {'blogs':blogs}
	return render(request, 'blogs/blogs.html', context)

@login_required
def blog(request, blog_id):
	"""Show a single blog and all its posts"""
	blog = get_object_or_404(Blog, id=blog_id)
	if blog.public==False:
		check_blog_owner(blog.owner, request.user)
		posts = blog.post_set.order_by('-date_added')
		context = {'blog':blog, 'posts':posts}
		return render(request, 'blogs/blog.html', context)
	else:
		posts = blog.post_set.order_by('-date_added')
		context = {'blog':blog, 'posts':posts}
		return render(request, 'blogs/blog.html', context)

@login_required
def new_blog(request):
	"""Add a new blog"""
	if request.method != 'POST':
		# No data submitted; create a blank form
		form = BlogForm()
	else:
		# POST data submittesd; process data
		form = BlogForm(data=request.POST)
		if form.is_valid():
			new_blog = form.save(commit=False)
			new_blog.owner = request.user
			new_blog.save()
			return redirect('blogs:blogs')
	# Display a blank or invalid form
	context = {'form' : form}
	return render(request, 'blogs/new_blog.html', context)

@login_required
def new_post(request, blog_id):
	"""Add a new post to a blog"""
	blog = get_object_or_404(Blog, id=blog_id)

	if request.method != 'POST':
		# No data is submitted; create a blank form
		form = PostForm()
	else:
		# POST data submitted; process data
		form = PostForm(data=request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.blog = blog
			new_post.save()
			return redirect('blogs:blog', blog_id=blog_id)

	# Display a blank or invalid form
	context = {'blog':blog, 'form':form}
	return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
	"""Edit an existing post"""
	post = get_object_or_404(Post, id=post_id)
	blog = post.blog
	check_blog_owner(blog.owner, request.user)

	if request.method != 'POST' and check_blog_owner(blog.owner, request.user) != Http404:
		# Initial request; pre-fill form with current post
		form = PostForm(instance=post)
	elif check_blog_owner(blog.owner, request.user)!=Http404:
		# POST data submitted; process data.
		form = PostForm(instance = post, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('blogs:blog', blog_id=blog.id)

	context = {'post':post, 'blog':blog, 'form':form}
	return render(request, 'blogs/edit_post.html', context)