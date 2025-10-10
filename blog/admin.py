from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, FavouritePost


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """Post admin with Summernote editor."""
    list_display = ("title", "slug", "author", "status", "created_on")
    list_filter = ("status", "created_on", "author")
    search_fields = ("title", "slug", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)
    date_hierarchy = "created_on"


class CommentAdmin(admin.ModelAdmin):
    """Readable comment admin with filters & search."""
    list_display = ("author", "post", "approved", "created_on")
    list_filter = ("approved", "created_on")
    search_fields = ("author__username", "body", "post__title")
    ordering = ("-created_on",)


@admin.register(FavouritePost)
class FavouritePostAdmin(admin.ModelAdmin):
    """
    This produces the form with Post + User select boxes (like your 2nd screenshot).
    Autocomplete makes large datasets easier to use.
    """
    list_display = ("post", "user", "created_on")
    list_select_related = ("post", "user")
    list_filter = ("created_on",)
    search_fields = ("post__title", "user__username", "user__email")
    autocomplete_fields = ("post", "user")
    ordering = ("-created_on",)


# Register Comment with the customized admin
admin.site.register(Comment, CommentAdmin)
