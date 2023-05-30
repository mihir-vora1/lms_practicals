# http://127.0.0.1:8000/post/create/

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth import get_user_model


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Categorie(AbstractBaseModel):
    CHOICES = [
        ('family', 'Family'),
        ('mental_health', 'Mental Health'),
        ('business', 'Business'),
        ('health', 'Health'),
        ('productivity', 'Productivity'),
        ('marketing', 'Marketing'),
        ('relationships', 'Relationships'),
        ('mindfulness', 'Mindfulness'),
        ('leadership', 'Leadership'),
        ('programming', 'Programming'),
        ('data_science', 'Data Science'),
        ('dev_ops', 'DevOps'),
        ('gaming', 'Gaming'),
        ('artificial_intelligence', 'Artificial Intelligence'),
    ]

    category = models.CharField(max_length=50, choices=CHOICES)

    def __str__(self):
        return self.category

class Tag(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Posts(AbstractBaseModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    thumbnail_image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    body = RichTextUploadingField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categorie, related_name='articles',  on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    # tags = models.CharField(max_length=500, null=True, blank=True)


    # 'Post object' title fix
    def __str__(self):
        return self.title
    
    # Plural fix 'Postss' 
    class Meta:
        verbose_name_plural = "Posts"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.user = kwargs.pop('user', None)
        super(Posts, self).save(*args, **kwargs)

class RelatedTopic(AbstractBaseModel):
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='related_topics')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Preference(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preference')
    categories = models.ManyToManyField('Categorie', related_name='preferences')


class Testing(models.Model):
    tags = models.CharField(max_length=255)

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]

    def set_tags_list(self, tags_list):
        self.tags = ', '.join(tags_list)

    tags_list = property(get_tags_list, set_tags_list)

class Comment(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()


class CreateBookmarkList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookmark_list = models.ForeignKey(CreateBookmarkList, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Posts, related_name='bookmarks')

    # def __str__(self):
    #     return f'{self.user.username} bookmarked {self.bookmark_list.name}'