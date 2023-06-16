from django.contrib import admin
from .models import Tag, Posts, Categorie, Preference, Comment, Bookmark, CreateBookmarkList

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_filter = ("id", 'user', 'title', 'description', 'categories', 'article_tags')
    list_display = ["id", 'user', 'title', 'description', 'categories', 'article_tags']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_filter = ('category',)

@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('id', 'user', 'post', 'parent_comment', 'content')
    list_display = ['id', 'user', 'post', 'parent_comment', 'content']


@admin.register(CreateBookmarkList)
class CreateBookmarkListAdmin(admin.ModelAdmin):
    list_filter = ('user', 'name', 'description')
    list_display = ['id', 'user', 'name', 'description', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_filter = ('user', 'bookmark_list')
    list_display = ['id', 'user', 'bookmark_list', 'display_posts', 'created_at', 'updated_at']
    search_fields = ['user__username', 'bookmark_list__name']

    def display_posts(self, obj):
        return ', '.join([str(post.id) + " - " + str(post) for post in obj.posts.all()])

    display_posts.short_description = 'Posts'



