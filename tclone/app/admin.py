from django.contrib import admin

from .models import Profile, Post, Comment

# Register all the models to the admin panel
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
