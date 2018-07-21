from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'name', 'created_time', 'email', 'text']

# Register your models here.

admin.site.register(Comment, CommentAdmin)
