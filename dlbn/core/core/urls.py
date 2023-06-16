
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from post import views as post
from post import views as blog_post
from user import views as user

urlpatterns = [


    path("admin/", admin.site.urls),
    path("", post.home, name="home"),
    
    # user module
    path("", include("user.urls")),

    # article module
    path('post/', include("post.urls")),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('post/', blog_post.create_article, name="create-blog"),

    path("", include("membership.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)