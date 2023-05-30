from django.contrib import admin
from .models import User, Profile, Follow, Follow1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass

@admin.register(Follow1)
class Follow1Admin(admin.ModelAdmin):
    pass
