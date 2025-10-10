from django.shortcuts import render
from django.template.loader import select_template
from .models import FavouritePostPage
from blog.models import Post
from django.contrib.auth.decorators import login_required

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

@login_required
def favourite_post_page(request):
    """
    Shows the current user's favourited posts.
    """
    posts = (
        Post.objects
        .filter(favourites__user=request.user, status=1)
        .select_related('author')
        .prefetch_related('favourites')
        .order_by('-favourites__created_on')
    )
    return render(request, "favourite_post/favourite_post.html", {"posts": posts})

@login_required
def favourite_post_page(request):
    # All published posts favourited by the current user
    posts = (
        Post.objects
        .filter(favourites__user=request.user, status=1)
        .select_related('author')
        .order_by('-favourites__created_on')
    )
    return render(request, "favourite_post/favourite_post.html", {"posts": posts})