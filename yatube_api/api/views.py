from api.permissions import ReadAndOwner
from api.serializers import GroupSerializer, PostSerializer
from api.serializers import CommentSerializer, FollowSerializer
from posts.models import Group, Post, Follow
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .pagination import Pagination
# permission взято из 1 темы и 2 урока,
# КОТОРЫЙ БЫЛО БЫ НЕ ПЛОХО ВСТАВИТЬ В 8 СПРИНТ
# просто реально без Пачки не прошёл бы 8 спринт.


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Pagination


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReadAndOwner]
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReadAndOwner]
    pagination_class = Pagination

    def get_queryset(self):
        post = get_object_or_404(Post,
                                 pk=self.kwargs.get('post_id',))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post,
                                 pk=self.kwargs.get('post_id',))
        serializer.save(post=post,
                        author=self.request.user)


class FollowView(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)
# Класс SearchFilter поддерживает простой поиск на основе одного параметра
# запроса и основан на функциональности поиска администратора Django
# взято из документации django-rest-framework
# Можно и просто юзать from rest_framework.filters import SearchFilter
# без filters, разницы почему-то ноль.

    def get_queryset(self):
        user_who_follow = self.request.user
        return user_who_follow.follower

    def perform_create(self, serializer):
        user_who_follow = self.request.user
        serializer.save(user=user_who_follow)
# Практически то же самое, что и в comments
