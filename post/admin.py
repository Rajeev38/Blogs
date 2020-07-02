from django.contrib import admin
from . import models
# Register your models here.
my_models = [models.Blog,models.Response,models.Comment]
admin.site.register(my_models)