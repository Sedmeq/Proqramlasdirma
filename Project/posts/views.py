from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from posts.forms import CommentForm 
from .models import Category, Post, Author, Book, Tag

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post(request, slug):
    post_obj = get_object_or_404(Post, slug=slug)
    # Get existing comments for display
    comments = post_obj.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a comment but don't save to DB yet
            new_comment = form.save(commit=False)
            # Associate the comment with the current post
            new_comment.post = post_obj
            new_comment.save()
            # Redirect to the same page after saving
            return redirect('post', slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post_obj,
        'comments': comments,
        'form': form
    }
    return render(request, 'post.html',context)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def tag(request):
    tag_siyahi = Tag.objects.all()
    return render(request , 'tag_list.html' , {'tag':tag_siyahi})

def tag_list(request):
    query = request.GET.get('q' , '').strip()

    if query:
        tags = Tag.objects.filter(name__icontains=query)
    else:
        tags = Tag.objects.all()

    return render(request , 'tag_list.html' , {'tag':tags , 'query':query})