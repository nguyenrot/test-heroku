from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, GetPostSerializer
from .models import Post, Comment
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['comment_post', 'comment_delete']:
            return CommentSerializer
        if self.action == 'list':
            return GetPostSerializer
        return PostSerializer

    # serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        content = request.data.get('content')
        creator = request.user
        post = Post.objects.create(content=content, creator=creator)
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.creator == request.user:
            post.delete()
            return Response('Delete successful', status=status.HTTP_200_OK)

        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_name='like-get', url_path='like-get')
    def like_post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            list = post.like.all()
            for item in list:
                if item == request.user:
                    post.like.remove(request.user)
                    return Response('Unlike successful', status=status.HTTP_200_OK)
            post.like.add(request.user)
            return Response('Like successful', status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_name='comment-post', url_path='comment-post')
    def comment_post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            content = request.data.get('content')
            comment = Comment.objects.create(content=content, post=post, creator=request.user)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    comment_param_config = openapi.Parameter(
        'comment_id',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(manual_parameters=[comment_param_config])
    @action(methods=['get'], detail=True, url_name='comment-delete', url_path='comment-delete')
    def comment_delete(self, request, pk):
        try:
            comment_id = request.GET.get('comment_id')
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return Response('Delete successful', status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
