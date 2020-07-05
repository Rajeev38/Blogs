from django import template

register = template.Library()

from ..models import *

@register.simple_tag
def get_comments(id=None,name=None):
    comment1 = Comment.objects.filter(blog__id=id,user__username=name)
    return comment1