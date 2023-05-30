from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
                        Posts, 
                        Tag,  
                        Categorie, 
                        Preference, 
                        Comment, 
                        CreateBookmarkList, 
                        Posts, 
                        Bookmark
                    )
from user.models import User, Follow
from .forms import CreateBlogForm
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (
                            CategoriesSerializer, 
                            TagSerializer, 
                            PreferenceSerializer, 
                            UserPreferenceSerializerTest, 
                            ArticleSerializer, 
                            CommentSerializer, 
                            CreateBookmarkListSerializer,
BookmarkSerializer
                        )
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied


@login_required
def home(request):
    user = request.user
    try:
        # Retrieve the users that the current user is following
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

        # Retrieve the categories from the user's preference
        categories = user.preference.categories.all()

        # Filter posts based on following users OR preferred categories and order by created_at in descending order
        posts = Posts.objects.filter(Q(user__in=following_users) | Q(categories__in=categories)).order_by('-updated_at').distinct()
    except ObjectDoesNotExist:
        # Handle the case when the user does not have a preference
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        posts = Posts.objects.filter(user__in=following_users).order_by('-updated_at').distinct()

    category_lists = Categorie.objects.all()
    first_tag = Tag.objects.first()
    context = {
        'posts': posts,
        'category_lists': category_lists,
        'first_tag': first_tag,
    }
    return render(request, 'post/home.html', context)


@login_required
def create_article(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save(user=request.user)
            form.save_m2m()
            return redirect('home')
    else:
        form = CreateBlogForm()
        context = {
            'form':form
        }

    return render(request, 'post/create_blog.html', context)

# @login_required
# def create_blog_post(request):
#     if request.method == 'POST':
#         form = CreateBlogForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user  # Assign the user to the post
#             post.save()
#             form.save_m2m()
#             return redirect('home')
#     else:
#         form = CreateBlogForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'post/create_blog.html', context)


@login_required
def blog_detail(request):
    all_blogs = Posts.objects.all().order_by('-created_at')[:10]
    tag = Tag.objects.first()
    context = {
        'all_blogs': all_blogs,
        'tag' : tag,
    }
    return render(request, "post/blog_detail.html", context)


@login_required
def article_detail(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    tags = Tag.objects.all()
    categories = Categorie.objects.all()

    # tag_category_zip = zip([post.tags.all(), post.categories.all()])
    context = {
        'post' : post,
        "tags" : tags,
        "categories" : categories,

        # "tag_category_zip" : tag_category_zip
    }

    return render(request, 'post/post_detail.html', context)
from django.contrib import messages

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    form = CreateBlogForm(request.POST or None, request.FILES or None, instance=post)


    if form.is_valid():
        form.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('post_detail', post_id=post_id)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'post/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.delete()
    return redirect("home")

@login_required
def tag_posts(request):
    category_name = request.GET.get('category')
    tag_name = request.GET.get('tag')
    tag = Tag.objects.get(name=tag_name)
    posts = Posts.objects.filter(tags=tag)
    tags = Tag.objects.filter(categories__category=category_name)

    # related_tags = Tag.objects.filter(posts__in=posts).distinct()
    context = {
        'posts': posts,
        "tags" : tags,
    }

    return render(request, 'post/tag_posts.html', context)


@login_required()
def categories_posts(request):
    category_name = request.GET.get('category')
    get_category = Categorie.objects.get(category=category_name)
    posts = Posts.objects.filter(categories=get_category)

    # tags
    tags = Tag.objects.filter(categories__category=category_name)

    context = {
        'posts': posts,
        "tags" : tags
    }
    return render(request, 'post/category_posts.html', context)

from rest_framework.permissions import IsAuthenticated

class CategoriesListAPIView(generics.ListAPIView):
    # queryset = Categorie.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Categorie.objects.filter(user=user)

class CategoriesCreateAPIView(generics.CreateAPIView):
    
    queryset = Categorie.objects.all()
    serializer_class = CategoriesSerializer

    def create(self, request, *args, **kwargs):
        category = request.data.get('category')
        if category:
            existing_tag = Categorie.objects.filter(category=category).exists()
            if existing_tag:
                return Response({"detail": "Tag with the same category already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class CategoriesRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubTagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagCreateAPIView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Tag.objects.filter(user=user)
        return Tag.objects.none()
    
    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        category = request.data.get("categories")
        if name and category:
            existing_subtag = Tag.objects.filter(name=name, categories=category).exists()
            if existing_subtag:
                return Response({"detail": "Sub-tag with the same name already exists within the category."}, status=status.HTTP_400_BAD_REQUEST)
            
            subtags_in_category = Tag.objects.filter(categories=category).values_list('name', flat=True)
            if name in subtags_in_category:
                return Response({"detail": "Sub-tag with the same name already exists within the category."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        tag_id = request.data.get("id")
        if tag_id is None:
            return Response({"detail": "Please provide the tag_id to delete."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if instance.user == user:
            self.perform_destroy(instance)
            return Response({"message": "Tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this tag."},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to update this tag."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class TagSearchAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        categories_id = self.request.query_params.get('categories_id')
        if categories_id:
            queryset = queryset.filter(categories_id=categories_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'message': 'No results found.'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class UserPreferenceAPIView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Categorie.objects.filter(user=user)
        return Categorie.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        preference, _ = Preference.objects.get_or_create(user=user)
        categories = serializer.validated_data['categories']
        preference.categories.add(*categories)

    def get(self, request, *args, **kwargs):
        user = request.user
        preference = get_object_or_404(Preference, user=user)
        serializer = self.get_serializer(preference)
        data = serializer.data
        # Retrieve category ids and names
        categories = Categorie.objects.filter(id__in=data['categories']).values('id', 'category')
        category_data = [{'id': category['id'], 'category': category['category']} for category in categories]
        data['categories'] = category_data
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Preferences created successfully'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = request.user
        preference = get_object_or_404(Preference, user=user)
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Preferences updated successfully'}, status=status.HTTP_200_OK)

    # def delete(self, request, *args, **kwargs):
    #     user = request.user
    #     preference = get_object_or_404(Preference, user=user)
    #     preference_id = request.data.get('categories')
    #     deleted_preference_id = preference.categories.filter(id=preference_id).first()
    #     if deleted_preference_id:
    #         preference.categories.remove(deleted_preference_id)
    #         return Response({'message': 'Preference deleted successfully'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': 'No matching preference found for deletion'}, status=status.HTTP_400_BAD_REQUEST)



    # def delete(self, request, *args, **kwargs):
    #     user = request.user
    #     preference = get_object_or_404(Preference, user=user)
    #     categories = request.data.get('categories', [])
    #     if not isinstance(categories, list):
    #         categories = [categories]

    #     deleted_categories = preference.categories.filter(id__in=categories)

    #     if deleted_categories.exists():
    #         preference.categories.remove(*deleted_categories)
    #         return Response({'message': 'Selected preferences deleted successfully'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': 'No matching categories found for deletion'}, status=status.HTTP_400_BAD_REQUEST)

class UserPreferenceAPIViewTest(generics.RetrieveUpdateAPIView):
    queryset = Preference.objects.all()
    serializer_class = UserPreferenceSerializerTest
    lookup_field = 'id'  # Update the lookup field to match your preference model's field

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class ArticleFeedAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user

        try:
            # Retrieve the users that the current user is following
            following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

            # Retrieve the categories from the user's preference
            categories = list(user.preference.categories.all())  # Convert single Categorie object to a list

            # Filter articles based on following users OR preferred categories
            queryset = Posts.objects.filter(Q(user__in=following_users) | Q(categories__in=categories)).order_by('-updated_at').distinct()
        except ObjectDoesNotExist:
            following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
            queryset = Posts.objects.filter(user__in=following_users).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No articles found in the feed."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        # Iterate over each article and retrieve their comments
        serialized_data = serializer.data
        for data in serialized_data:
            post_id = data['id']
            comments = Comment.objects.filter(post_id=post_id, parent_comment=None).distinct()  # Filter main comments only
            if comments.exists():
                comment_serializer = CommentSerializer(comments, many=True)
                data['comments'] = comment_serializer.data
            else:
                data['comments'] = "No Comment Found"
        return Response(serialized_data, status=status.HTTP_200_OK)


class CommentListCreateAPIView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            post_id = self.kwargs['post_id']
            return Comment.objects.filter(user=user, post_id=post_id, parent_comment=None)
        return Comment.objects.none()

    # def perform_create(self, serializer):
    #     post_id = self.kwargs['post_id']
    #     post = get_object_or_404(Posts, id=post_id)
    #     parent_comment_id = self.kwargs.get('parent_comment_id')
    #     if parent_comment_id:
    #         parent_comment = get_object_or_404(Comment, id=parent_comment_id, post=post)
    #         serializer.save(user=self.request.user, post=post, parent_comment=parent_comment)
    #     else:
    #         serializer.save(user=self.request.user, post=post)

    # def post(self, request, *args, **kwargs):
    #     post_id = self.kwargs['post_id']
    #     post = get_object_or_404(Posts, id=post_id)
    #     if post.comments.exists():
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         return Response({"message": "Cannot reply to comments as the post has no comments."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Posts, id=post_id)
        parent_comment_id = self.kwargs.get('parent_comment_id')
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id, post=post)
            serializer.save(user=self.request.user, post=post, parent_comment=parent_comment)
        else:
            serializer.save(user=self.request.user, post=post)

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Posts, id=post_id)
        parent_comment_id = self.kwargs.get('parent_comment_id')

        if post.comments.exists() or parent_comment_id:
            return super().post(request, *args, **kwargs)
        else:
            return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if comment.user != user:
            raise PermissionDenied("You do not have permission to update this comment.")

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def patch(self, request, *args, **kwargs):
        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if comment.user != user:
            raise PermissionDenied("You do not have permission to update this comment.")

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs.get("id")

        try:
            instance = get_object_or_404(Comment, id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if instance.user == user:
            self.perform_destroy(instance)
            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)


class BookmarkListAPIView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = CreateBookmarkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            if user.is_authenticated:
                queryset = CreateBookmarkList.objects.filter(user=user)
        except CreateBookmarkList.DoesNotExist:
            raise NotFound("Bookmark list not found.")

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except NotFound as e:
            return self.handle_exception(e)

        if not queryset.exists():
            return Response({"message": "Bookmark list not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        bookmark_list_id = kwargs.get("id")
        if bookmark_list_id:
            bookmark_list = get_object_or_404(CreateBookmarkList, pk=bookmark_list_id)
            if bookmark_list.user == request.user:
                bookmark_list.delete()
                return Response({"message": "Bookmark list deleted successfully."}, status=200)
            else:
                raise PermissionDenied("You do not have permission to delete this bookmark list.")
        else:
            return Response({"message": "Bookmark list ID is required."}, status=400)

    # def update(self, request, *args, **kwargs):
    #     user = request.user
    #     bookmark_list = self.get_object()
    #
    #     if bookmark_list.user == user:
    #         serializer = self.get_serializer(bookmark_list, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     else:
    #         return Response({"message": "You do not have permission to update this bookmark list."}, status=403)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to update this tag."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     user = request.user
    #     bookmark_list_id = request.data.get("id")
    #     # bookmark_list_id = self.kwargs.get("pk")
    #     bookmark_list = get_object_or_404(CreateBookmarkList, pk=bookmark_list_id)
    #
    #     if bookmark_list.user == user:
    #         serializer = self.get_serializer(bookmark_list, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     else:
    #         return Response({"message": "You do not have permission to update this bookmark list."}, status=403)

    # def update(self, request, *args, **kwargs):
    #     user = request.user
    #     bookmark_list_id = self.kwargs.get("pk")
    #     bookmark_list = get_object_or_404(CreateBookmarkList, pk=bookmark_list_id)
    #
    #     if bookmark_list.user == user:
    #         serializer = self.get_serializer(bookmark_list, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     else:
    #         return Response({"message": "You do not have permission to update this bookmark list."}, status=403)

    # def put(self, request, *args, **kwargs):
    #     # Delegate to the `update` method for PUT requests
    #     return self.update(request, *args, **kwargs)
    #
    # def patch(self, request, *args, **kwargs):
    #     # Delegate to the `update` method for PATCH requests
    #     return self.update(request, *args, **kwargs)


class BookmarkCreateRemoveAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        try:
            if user.is_authenticated:
                queryset = Bookmark.objects.filter(user=user)
        except CreateBookmarkList.DoesNotExist:
            raise NotFound("Bookmark not found.")

        return queryset


    def perform_create(self, serializer):
        user = self.request.user
        bookmark_list = serializer.validated_data['bookmark_list']
        posts = serializer.validated_data['posts']

        if len(posts) == 1:
            # Check if the requested user's bookmark list already contains the same posts
            if Bookmark.objects.filter(user=user, bookmark_list=bookmark_list, posts__in=posts).exists():
                raise serializers.ValidationError(
                    "The selected posts are already bookmarked in the specified bookmark list.")
        else:
            raise serializers.ValidationError(
                "at time single posts allowed to bookmark")

        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            bookmarks = self.get_queryset()
            serializer = self.get_serializer(bookmarks, many=True)
            return Response(serializer.data)
        except Http404:
            return Response({"message": "No bookmarks found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        bookmark_id = kwargs.get("id")
        if bookmark_id:
            bookmark_id = get_object_or_404(Bookmark, pk=bookmark_id)
            if bookmark_id.user == request.user:
                bookmark_id.delete()
                return Response({"message": "Bookmark deleted successfully."}, status=200)
            else:
                raise PermissionDenied("You do not have permission to delete this bookmark list.")
        else:
            return Response({"message": "Bookmark ID is required."}, status=400)