from rest_framework import serializers
from .models import (
    Tag,
    Categorie,
    Preference,
    Posts,
    Comment,
    CreateBookmarkList,
    Bookmark,
)
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "user", "user_name", "categories", "name"]

    def get_user_name(self, obj):
        return obj.user.username


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"

    def create(self, validated_data):
        categories = Categorie.objects.create(**validated_data)
        return categories


class UserSerializer(serializers.ModelSerializer):
    preference = serializers.PrimaryKeyRelatedField(queryset=Preference.objects.all())

    class Meta:
        model = User
        fields = ("id", "username", "email")


class PreferenceSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(), many=True
    )

    class Meta:
        model = Preference
        fields = ["categories"]

    def create(self, validated_data):
        user = self.context["request"].user
        preference, _ = Preference.objects.get_or_create(user=user)
        preference.categories.set(validated_data["categories"])
        return preference


class UserPreferenceSerializerTest(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categorie.objects.all()
    )

    class Meta:
        model = Preference
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["category"]


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.username")
    categories = CategorySerializer(read_only=True)

    def get_tags(self, article):
        tags = article.tags.all()
        if tags.exists():
            return [tag.name for tag in tags]
        return None

    class Meta:
        model = Posts
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    parent_comment_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        parent_comment_id = validated_data.pop("parent_comment_id", None)
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                validated_data["parent_comment"] = parent_comment
            except Comment.DoesNotExist:
                pass
        return super().create(validated_data)

    def get_replies(self, comment):
        serializer = self.__class__(comment.replies.all(), many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "user",
            "user_name",
            "parent_comment",
            "parent_comment_id",
            "content",
            "created_at",
            "updated_at",
            "replies",
        )
        read_only_fields = ("id", "user_name", "post", "created_at", "updated_at")

    def get_user_name(self, obj):
        return obj.user.username


class CreateBookmarkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateBookmarkList
        fields = ["id", "name", "description"]


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ["id", "user", "user_name", "bookmark_list", "posts"]

    def get_user_name(self, obj):
        return obj.user.username
