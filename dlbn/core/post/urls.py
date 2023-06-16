from django.urls import path
from . import views


urlpatterns = [
    path('feed', views.home, name="home"),
    path("", views.create_article, name="create_article"),
    path('detail', views.blog_detail, name="blog_detail"),
    path('<int:post_id>', views.article_detail, name="article_detail"),
    path('tag', views.tag_posts, name="tag_posts"),
    path("category", views.categories_posts, name="category_post"),
    path("edit/<int:post_id>", views.edit_article, name="edit_post"),
    path("delete/<int:post_id>", views.delete_article, name="delete_post"),


    # Search Tags
    path('tags/search', views.TagSearchAPIView.as_view(), name='tag_search_api'),

    # User Preference 
    path('preferences', views.UserPreferenceAPIView.as_view(), name='user_preference_api'),

    path('articles/feed', views.ArticleFeedAPIView.as_view(), name='article-feed'),
    path('articles/feed/<int:pk>', views.ArticleFeedAPIViewRestrict.as_view(), name='article-feed'),

    # user comments
    path('<int:post_id>/comments', views.CommentListCreateAPIView.as_view(), name='comment-list'),
    path('<int:post_id>/comments/<int:parent_comment_id>/replies', views.CommentListCreateAPIView.as_view(), name='comment-reply'),
    path('<int:post_id>/comments/<int:id>', views.CommentListCreateAPIView.as_view(), name='comment-update-delete'),

    # bookmark-lists
    path('bookmark-lists', views.BookmarkListAPIView.as_view(), name='bookmark-list-create'),
    path('bookmark-lists/<int:id>', views.BookmarkListAPIView.as_view(), name='bookmark-update-delete'),

    # Bookmarks
    path('bookmarks', views.BookmarkCreateRemoveAPIView.as_view(), name='bookmark'),
    path('bookmarks/<int:id>', views.BookmarkCreateRemoveAPIView.as_view(), name='bookmark-update-delete'),

]