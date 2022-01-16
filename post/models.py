from django.db import models
from authentication.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='comment_user')

    class Meta:
        db_table = "Post"
        ordering = ['-update_at', 'created_at']

    def __str__(self):
        return self.content[0:50]


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Comment"
        ordering = ['-update_at', 'created_at']

    def __str__(self):
        return self.content + " by " + str(self.creator)
