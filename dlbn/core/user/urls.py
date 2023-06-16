from django.urls import path
from user import views
from post import views as post
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('home', post.home, name="home"),
	path('register/', views.register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification', views.resend_verification_email, name='resend_verification'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Follow a user
    path('follow', views.FollowCreateAPIView.as_view(), name='user_follow'),
    path('unfollow/<int:id>', views.FollowCreateAPIView.as_view(), name='unfollow'),

]