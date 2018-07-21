from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import pytz
from django.utils.timezone import now

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
tz = pytz.timezone('Asia/Shanghai')
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100, help_text='文章标题')
    body = models.TextField(help_text='文章正文')
    created_time = models.DateTimeField(default=now(), help_text='创建时间')
    modified_time = models.DateTimeField(default=now(), help_text='最后修改时间')
    excerpt = models.CharField(max_length=200, blank=True, help_text='文章摘要')
    category = models.ForeignKey(Category, help_text='文章的分类')
    tags = models.ManyToManyField(Tag, blank=True, help_text='文章的标签')
    author = models.ForeignKey(User, help_text='文章的作者')

    views = models.PositiveIntegerField(default=0, help_text='文章阅读量')

    # 设置文章阅读量统计函数，每浏览一次，阅读量加1
    def increase_views(self):
        # 每被调用一次，阅读量加1
        self.views += 1
        # 更新保存到数据库
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 定义一个Meta类，指定post对象的排列顺序为先按照created_time的逆序排列,相同的对象再按照title的正序排列
    class Meta:
        ordering = ['-created_time', 'title']