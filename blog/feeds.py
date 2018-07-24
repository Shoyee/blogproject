from django.contrib.syndication.views import Feed
from .models import Post

# 创建博客订阅功能类
class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = '博客天地'

    # 指定点击阅读器后跳转的地址
    link = '/'

    # 显示在聚合阅读器上的描述信息
    description = '博客天地，程序员的修炼场！'

    # 定义显示内容条目的函数
    def items(self):
        return Post.objects.all()

    # 定义显示的内容条目的标题的函数
    def item_title(self, item):
        return "[{category}] {title}".format(category=item.category, title=item.title)

    # 定义内容条目的描述信息
    def item_description(self, item):
        return item.body

