# http://127.0.0.1:8000/post/create/

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Categorie(AbstractBaseModel):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Tag(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Posts(AbstractBaseModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    thumbnail_image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    body = RichTextUploadingField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE
    )
    categories = models.ForeignKey(
        Categorie, related_name="articles", on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag, related_name="posts")
    article_tags = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.user = kwargs.pop("user", None)
        super(Posts, self).save(*args, **kwargs)


class Preference(AbstractBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference"
    )
    categories = models.ManyToManyField("Categorie", related_name="preferences")

    def __str__(self):
        return f"User: {self.user} :- Categories: {', '.join(str(category) for category in self.categories.all())}"

class Comment(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"


class CreateBookmarkList(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return f"Bookmark List: {self.user.username} - {self.name}"

class Bookmark(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookmark_list = models.ForeignKey(CreateBookmarkList, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Posts, related_name="bookmarks")

    def __str__(self):
        return f'bookmarked : {self.user.username} - {self.bookmark_list.name}'
