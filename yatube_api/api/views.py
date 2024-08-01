from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, Follow
from rest_framework import viewsets, permissions, filters, mixins, serializers
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, FollowSerializer,)
from api.permissions import IsAuthenticatedAuthorOrReadOnlyPermission


class CreateRetieveListViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return serializer.save(author=self.request.user,
                               post=post)


class FollowViewSet(CreateRetieveListViewSet):

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as error:
            if 'CHECK' in str(error):
                message = 'Sorry, you can not follow yourself.'
            else:
                message = 'This user-follower couple exists already.'
            raise serializers.ValidationError(message)
    
    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''
