from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import FavouritePostPage

# Register your models here.
@admin.register(FavouritePostPage)
class FavouritePostPageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)