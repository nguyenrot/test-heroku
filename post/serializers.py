from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from .models import Post, Comment
import json


class CommentSerializer(ModelSerializer):
    creator = StringRelatedField(many=False)
    post = StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ["id", "content", "post", "creator"]


class PostSerializer(ModelSerializer):
    likes = SerializerMethodField()
    creator = StringRelatedField(many=False)

    def get_likes(self, post):
        return post.like.all().count()

    class Meta:
        model = Post
        fields = ["id", 'creator', "content", "created_at", "update_at", "likes"]


class GetPostSerializer(ModelSerializer):
    likes = SerializerMethodField()
    creator = StringRelatedField(many=False)
    # comments = StringRelatedField(many=True)
    post_comment = StringRelatedField(many=True)

    # def get_comments(self, post):
    #     # comment = Comment.objects.filter(post=post)
    #     return CommentSerializer(post.comments.content).data

    def get_likes(self, post):
        return post.like.all().count()

    class Meta:
        model = Post
        fields = ["id", 'creator', "content", "created_at", "update_at", "likes", "post_comment"]
