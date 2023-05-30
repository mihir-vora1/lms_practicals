from django.urls import path
from . import views


urlpatterns = [
    path('feed', views.home, name="home"),
    path("", views.create_article, name="create_article"),
    path('detail', views.blog_detail, name="blog_detail"),
    path('<int:post_id>', views.article_detail, name="article_detail"),
    path('tag', views.tag_posts, name="tag_posts"),
    path("category", views.categories_posts, name="category_post"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post"),

    # Create Main-Tags
    # path('categories/', views.CategoriesCreateAPIView.as_view(), name='categories_create_api'),

    # Tag
    path('tags', views.TagCreateAPIView.as_view(), name='sub_tag_create_api'),
    path('tags/<int:pk>', views.TagCreateAPIView.as_view(), name='sub_tag_create_api'),

    # Search Tags
    path('tags/search', views.TagSearchAPIView.as_view(), name='tag_search_api'),

    # User Preference 
    path('preferences', views.UserPreferenceAPIView.as_view(), name='user_preference_api'), # POST


    path('articles/feed', views.ArticleFeedAPIView.as_view(), name='article-feed'),

    # user comments
    path('<int:post_id>/comments', views.CommentListCreateAPIView.as_view(), name='comment-list'),
    path('<int:post_id>/comments/<int:id>/update', views.CommentListCreateAPIView.as_view(), name='comment-update'),
    path('<int:post_id>/comments/<int:parent_comment_id>/replies', views.CommentListCreateAPIView.as_view(), name='comment-reply'),
    path('<int:post_id>/comments/<int:id>/delete', views.CommentListCreateAPIView.as_view(), name='comment-update'),

    # bookmark
    # user
    path('bookmark-lists', views.BookmarkListAPIView.as_view(), name='bookmark-list-create'),
    path('bookmark-lists/<int:pk>/update', views.BookmarkListAPIView.as_view(), name='bookmark-update'),
    path('bookmark-lists/<int:id>/delete', views.BookmarkListAPIView.as_view(), name='bookmark-delete'),

    # user
    path('bookmarks', views.BookmarkCreateRemoveAPIView.as_view(), name='bookmark'),
    path('bookmarks/<int:id>/update', views.BookmarkCreateRemoveAPIView.as_view(), name='bookmark-update'),
    path('bookmarks/<int:id>/delete', views.BookmarkCreateRemoveAPIView.as_view(), name='bookmark-delete'),

]