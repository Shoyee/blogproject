from django import template
from django.db.models.aggregates import Count
from blog.models import Post, Category, Tag

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
    # 使用annotate和Count方法计算每个分类下面的文章数量，其接受的参数为需要计数的模型的名称Post的小写
    # 筛选数量大于零的分类，不大于零的不显示
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    # 统计每个标签下的文章数量
    # 筛选数量大于零的标签，不大于零的不显示
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)