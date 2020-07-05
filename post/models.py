from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_modified = models.BooleanField(default=False)

    def __str__(self):
        return (self.name)

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.blog.name)

class Response(models.Model) :
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like_or_not = models.BooleanField()
    response_date = models.DateTimeField(auto_now_add=True)
