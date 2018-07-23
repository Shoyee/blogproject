import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.views.generic import ListView, DetailView

from comments.forms import CommentForm

# Create your views here.

# 首页信息页面类视图函数
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

# 文章详情页面函数
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 浏览详情页，调用函数，使文章阅读量加1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    form = CommentForm()
    comment_list = post.comment_set.all()
    return render(request, 'blog/detail.html', context={
        'post': post,
        'form': form,
        'comment_list': comment_list,
    })

# 归档分类信息列表显示类视图函数
# def archives(request, year, month):
#
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request, 'blog/index.html',
#                   context={
#                       'post_list': post_list,
#                   })

class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))

#  分类信息列表显示类视图函数
class CategoryView(IndexView):
# def category(request, pk):
    # cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate)
    # return render(request, 'blog/index.html',
    #               context={
    #                   'post_list': post_list,
    #               })

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
