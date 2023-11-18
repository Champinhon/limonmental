from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

def psychologists(request):
    psychologists_list = [
        {"name": "Psicólogo 1", "photo": "https://storage.googleapis.com/limonmental/Disen%CC%83o%20sin%20ti%CC%81tulo%20(5).png", "description": "Descripción del psicólogo 1"},
        {"name": "Psicólogo 2", "photo": "https://storage.googleapis.com/limonmental/53875233-04FA-4805-B538-43655913EC1C.jpg", "description": "Descripción del psicólogo 2"},
    ]

    return render(request, 'psychologists.html', {'psychologists_list': psychologists_list})

def is_admin(user):
    return user.is_staff

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_staff or request.user == comment.author:
        comment.delete()
    return redirect('posts')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_staff or request.user == post.author:
        post.delete()
        return redirect('posts') 

    return HttpResponse("No tienes permisos para borrar este post.")

def post_list(request):
    latest_posts = Post.objects.all().order_by('-created_at')

    return render(request, 'posts/post_list.html', {'latest_posts': latest_posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_list')
    else:
        form = CommentForm()

    return render(request, 'posts/create_comment.html', {'form': form, 'post': post})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home') 

    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
    else:
        posts = posts.order_by('-created_at')[:3]

    context = {'latest_posts': posts, 'query': query}
    return render(request, 'home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
        else:
            form = CommentForm()
    else:
        form = None

    context = {
        'post': post,
        'comment_form': form,
    }

    return render(request, 'posts/post_detail.html', context)