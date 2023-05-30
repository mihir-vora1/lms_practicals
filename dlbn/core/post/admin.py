from django.contrib import admin
from .models import Tag, Posts, RelatedTopic, Categorie, Preference, Testing, Comment, Bookmark, CreateBookmarkList

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    pass

@admin.register(RelatedTopic)
class RelatedTopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    pass

@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(CreateBookmarkList)
class CreateBookmarkListAdmin(admin.ModelAdmin):
    pass

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass
