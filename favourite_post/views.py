from django.shortcuts import render
from .models import FavouritePostPage

# Create your views here.
def favourite_post_page(request):
    """
    Renders the Favourite Post page
    """
    fav_page = FavouritePostPage.objects.all().order_by('-updated_on').first()
    return render(
        request,
        "favourite_post/favourite_post.html",
        {"fav_page": fav_page},
    )