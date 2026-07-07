from django.shortcuts import render, get_object_or_404
from .models import NewsPost


def news_list(request):
    category = request.GET.get('category', '')
    posts = NewsPost.objects.filter(is_published=True)
    if category:
        posts = posts.filter(category=category)
    return render(request, 'news/news_list.html', {'posts': posts, 'category': category})


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    related = NewsPost.objects.filter(is_published=True, category=post.category).exclude(pk=post.pk)[:3]
    return render(request, 'news/news_detail.html', {'post': post, 'related': related})
