from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from membership.models import Plan
from post.models import AbstractBaseModel


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, related_name='plan', blank=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_blog')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=1000, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def follow(self, user_to_follow):
        if not self.is_following(user_to_follow):
            Follow.objects.create(follower=self, following=user_to_follow)

    def unfollow(self, user_to_unfollow):
        Follow.objects.filter(follower=self, following=user_to_unfollow).delete()

    def is_following(self, user):
        return self.following.filter(following=user).exists()
    
    def is_followed_by(self, user):
        return self.followers.filter(follower=user).exists()
    
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        size = 300

        if img.height > size or img.width > size:
            output_size = (size, size)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CustomToken(Token):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_token')

class Follow(AbstractBaseModel):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'
