from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.
# 装饰器用于兼容python2版本
# 构建评论数据表
class Comment(models.Model):
    name = models.CharField(max_length=100, help_text='评论者的姓名')
    email = models.EmailField(max_length=255, help_text='评论者的邮箱')
    url = models.URLField(blank=True, help_text='评论者的url地址')
    text = models.TextField(help_text='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, help_text='评论添加的时间')
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

