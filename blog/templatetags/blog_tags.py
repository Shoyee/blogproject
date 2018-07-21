from django import template
from ..models import Post, Category

# 导入了自定义标签函数类并实例化对象
register = template.Library()

# 使用自定义标签装饰器函数，以使函数变成可在模板中通过{% get_recent_tag %}调用的模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()