from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from post.models import Posts
from .models import Follow
from .models import User as AbtsractUserInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source='follower.username')
    following_username = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ("following", "follower_username", "following_username")

    def validate(self, attrs):
        following = attrs.get('following')
        follower = self.context['request'].user

        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself.")

        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError("You are already following this user.")

        return attrs


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = AbtsractUserInfo
        fields = ('id', 'username', 'followers_count', 'following_count')

class FollowSerializerTest(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


