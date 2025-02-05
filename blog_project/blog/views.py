from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import BlogPost
from .forms import BlogPostForm, RegistrationForm

# Create your views here.

# Register a new user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # Check if form is submitted via POST
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log in the newly created user
            return redirect('blog_list')
    else:
        form = RegistrationForm() # If GET request, render empty form
    return render(request, 'register.html', {'form': form})

# Log in the user
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # Initialize the authentication form with POST data
        if form.is_valid():  # Check if credentials are valid
            user = form.get_user() # Get the user object from the form
            login(request, user) # Log in the user
            return redirect('blog_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Log out the user
@login_required # Make sure the user is logged in before they can log out
def user_logout(request):
    logout(request) # Log out
    return redirect('blog_list') # Redirect to the blog list page after logging out

# Display all blog posts
def blog_list(request):
    posts = BlogPost.objects.all() # Retrieve all blog posts from the database
    return render(request, 'blog_list.html', {'posts': posts}) # Render the blog list page with all posts

# View a specific blog post
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk) # Retrieve the post by its primary key (or 404 if not found)
    return render(request, 'blog_detail.html', {'post': post})

# Create a new blog post (only for logged-in users)
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES) # Create the form instance with POST data and files
        if form.is_valid():
            blog_post = form.save(commit=False) # Save the form data but don't commit yet
            blog_post.author = request.user  # Assign the current logged-in user as the author
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form})

# Update an existing blog post (only for the author)
@login_required  # Ensure the user is logged in to edit a blog post
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)  # Retrieve the post to be edited
    if request.user != post.author: # If the logged-in user is not the author
        return redirect('blog_list') # Redirect to the blog list page
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)  # Initialize the form with POST data and existing post
        if form.is_valid(): # Check if the form data is valid
            form.save()
            return redirect('blog_list') # Redirect to the blog list page after updating the post
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

# Delete a blog post (only for the author)
@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk) # Retrieve the post to be deleted
    if request.user == post.author: # If the logged-in user is the author
        post.delete()
    return redirect('blog_list')