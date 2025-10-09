from django.shortcuts import render
from django.template.loader import select_template
from .models import FavouritePostPage

def favourite_post_page(request):
    """
    Renders the Favourite Post page. Tries multiple template locations so it won't 404
    if the file is in either the app-level folder or the project-level templates folder.
    """
    fav_page = FavouritePostPage.objects.order_by('-updated_on').first()

    # Try app-level first, then project-level fallback
    template = select_template([
        "favourite_post/favourite_post.html",  # app-level: favourite_post/templates/favourite_post/favourite_post.html
        "favourite_post.html",                 # app-level (flat): favourite_post/templates/favourite_post.html
        "templates/favourite_post/favourite_post.html",  # edge case
    ])

    return render(request, template.template.name, {"fav_page": fav_page})
