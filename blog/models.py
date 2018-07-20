from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible

# Create your models here.

# 创建博客文章分类数据表
# 装饰器用于兼容python2版本
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100, help_text='分类名称')

    def __str__(self):
        return self.name


# 创建博客标签数据表
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100, help_text='标签名称')

    def __str__(self):
        return self.name


# 创建博客文章数据表
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100, help_text='文章标题')
    body = models.TextField(help_text='文章正文')
    created_time = models.DateTimeField(help_text='创建时间')
    modified_time = models.DateTimeField(help_text='最后修改时间')
    excerpt = models.CharField(max_length=200, blank=True, help_text='文章摘要')
    category = models.ForeignKey(Category, help_text='文章的分类')
    tags = models.ManyToManyField(Tag, blank=True, help_text='文章的标签')
    author = models.ForeignKey(User, help_text='文章的作者')

    def __str__(self):
        return self.title
