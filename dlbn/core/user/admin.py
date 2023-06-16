from django.contrib import admin
from .models import User, Follow

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'date_joined')
    list_display = ['id', 'username', 'email', 'email_verified', 'is_active', 'plan', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = ('follower', 'following')
    list_display = ['id', 'follower', 'following', 'created_at', 'updated_at']
    search_fields = ['follower__username', 'following__username']

