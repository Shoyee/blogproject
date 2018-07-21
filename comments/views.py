from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

# 发布评论函数
def post_comment(request, post_pk):
    # 先获取博客文章
    post = get_object_or_404(Post, pk=post_pk)

    # 判断请求方法
    if request.method == 'POST':
        # 获取数据，传入表单，实例化CommentForm对象
        form = CommentForm(request.POST)
        # 判断数据是否符合表单格式的要求
        if form.is_valid():
            # 如果数据格式正确，生成Comment实例化对象，作为评论数据，但是，暂时先不commit提交到数据库中
            comment = form.save(commit=False)
            # 把comment的post与post关联起来
            comment.post = post
            # 然后再保存并提交到数据库中(django的save方法是默认commit=True的，也就是保存的同时，如果不设置为False，则自动提交到数据库中)
            comment.save()

            # 当redirect 函数接收一个模型的实例时，它会调用这个Post模型实例post的 get_absolute_url 方法,
            # 重定向到 post的 get_absolute_url 方法返回的 URL，也就是当前post对象的详情页
            return redirect(post)
        else:
            # 如果输入的数据格式不合法，则重新渲染模板，返回对应的页面
            # 获取文章下面的评论列表
            comment_list = post.comment_set.all()
            # 返回文章详情页面
            return render(request, 'blog/detail.html',
                          context={
                              'post': post,
                              'form': form,
                              'comment_list': comment_list,
                          })
    # 如果不是post请求方式的话，重定向返回到文章详情页
    return redirect(post)