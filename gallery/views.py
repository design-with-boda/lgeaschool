from django.shortcuts import render
from .models import GalleryCategory, GalleryImage


def gallery(request):
    categories = GalleryCategory.objects.all()
    category_slug = request.GET.get('category', '')
    images = GalleryImage.objects.all()
    active_category = None
    if category_slug:
        active_category = GalleryCategory.objects.filter(slug=category_slug).first()
        if active_category:
            images = images.filter(category=active_category)
    return render(request, 'gallery/gallery.html', {
        'images': images,
        'categories': categories,
        'active_category': active_category,
    })
